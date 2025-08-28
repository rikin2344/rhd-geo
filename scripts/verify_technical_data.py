#!/usr/bin/env python3
"""
Technical Data Verification and Fix Script for Bearing Model JSON Files

This script scans through all JSON files in the models/ directory and verifies:
1. Noise data against noise_lookup_table.json
2. Clearance data against clearance_lookup_table.json  
3. Vibration data against vibration_lookup_table.json
4. SKF extended dimensions against skf_dimensions_only.json

If discrepancies are found, the script automatically fixes the JSON files with accurate data.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

class TechnicalDataVerifier:
    def __init__(self, models_dir: str = "models", docs_dir: str = "docs", scripts_dir: str = "scripts"):
        self.models_dir = Path(models_dir)
        self.docs_dir = Path(docs_dir)
        self.scripts_dir = Path(scripts_dir)
        
        # Load lookup tables
        self.noise_lookup = self.load_json_file(self.docs_dir / "noise_lookup_table.json")
        self.clearance_lookup = self.load_json_file(self.docs_dir / "clearance_lookup_table.json")
        self.vibration_lookup = self.load_json_file(self.docs_dir / "vibration_lookup_table.json")
        self.skf_lookup = self.load_json_file(self.scripts_dir / "skf_dimensions_only.json")
        
        # Statistics
        self.stats = {
            "total_files": 0,
            "files_verified": 0,
            "files_fixed": 0,
            "errors": []
        }

    def load_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Load and parse a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return {}

    def get_bearing_series(self, model_number: str) -> str:
        """Determine bearing series from model number."""
        model = str(model_number)
        if model.startswith('60') and len(model) >= 3:
            return '6000_series'
        elif model.startswith('62'):
            return '6200_series'
        elif model.startswith('63'):
            return '6300_series'
        else:
            return '6000_series'  # Default fallback

    def get_noise_data(self, bore_diameter: int, model_number: str) -> Dict[str, Optional[int]]:
        """Get noise data from lookup table based on bore diameter and bearing series."""
        try:
            series = self.get_bearing_series(model_number)
            bore_key = str(bore_diameter)
            
            if bore_key in self.noise_lookup.get("noise_lookup_table", {}).get("data", {}):
                series_data = self.noise_lookup["noise_lookup_table"]["data"][bore_key].get(series, {})
                return {
                    "Z2": series_data.get("Z2"),
                    "Z3": series_data.get("Z3"),
                    "Z4": series_data.get("Z4")
                }
        except Exception as e:
            print(f"Error getting noise data for bore {bore_diameter}, model {model_number}: {e}")
        
        return {"Z2": None, "Z3": None, "Z4": None}

    def get_clearance_data(self, bore_diameter: int) -> Dict[str, Dict[str, int]]:
        """Get clearance data from lookup table based on bore diameter."""
        try:
            ranges = self.clearance_lookup.get("clearance_lookup_table", {}).get("ranges", [])
            
            for range_data in ranges:
                over_mm = range_data["over_mm"]
                to_mm = range_data["to_mm"]
                
                if over_mm < bore_diameter <= to_mm:
                    return range_data["clearances"]
        except Exception as e:
            print(f"Error getting clearance data for bore {bore_diameter}: {e}")
        
        return {}

    def get_vibration_data(self, bore_diameter: int) -> Dict[str, Dict[str, int]]:
        """Get vibration data from lookup table based on bore diameter."""
        try:
            bore_key = str(bore_diameter)
            if bore_key in self.vibration_lookup.get("vibration_lookup_table", {}).get("data", {}):
                return self.vibration_lookup["vibration_lookup_table"]["data"][bore_key]
        except Exception as e:
            print(f"Error getting vibration data for bore {bore_diameter}: {e}")
        
        return {}

    def get_skf_data(self, model_number: str) -> Optional[Dict[str, float]]:
        """Get SKF extended dimensions from lookup table based on model number."""
        try:
            if model_number in self.skf_lookup:
                skf_data = self.skf_lookup[model_number]
                return {
                    "d1_shoulder_diameter": skf_data.get("d1"),
                    "D2_recess_diameter": skf_data.get("D2"),
                    "r1_chamfer_radius": skf_data.get("r1"),
                    "r2_chamfer_radius": skf_data.get("r2")
                }
        except Exception as e:
            print(f"Error getting SKF data for model {model_number}: {e}")
        
        return None

    def verify_and_fix_file(self, file_path: Path) -> bool:
        """Verify and fix a single JSON file."""
        try:
            # Load the JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            model_number = data.get("model_number", "")
            bore_diameter = data.get("dimensions", {}).get("bore_diameter_d_mm", 0)
            
            if not model_number or not bore_diameter:
                self.stats["errors"].append(f"{file_path.name}: Missing model_number or bore_diameter")
                return False
            
            needs_fix = False
            
            # Verify and fix noise data
            expected_noise = self.get_noise_data(bore_diameter, model_number)
            current_noise = data.get("noise", {})
            
            if current_noise != expected_noise:
                print(f"Fixing noise data in {file_path.name}")
                print(f"  Expected: {expected_noise}")
                print(f"  Current:  {current_noise}")
                data["noise"] = expected_noise
                needs_fix = True
            
            # Verify and fix clearance data
            expected_clearance = self.get_clearance_data(bore_diameter)
            current_clearance = data.get("clearance", {})
            
            if expected_clearance and current_clearance != expected_clearance:
                print(f"Fixing clearance data in {file_path.name}")
                print(f"  Expected: {expected_clearance}")
                print(f"  Current:  {current_clearance}")
                data["clearance"] = expected_clearance
                needs_fix = True
            
            # Verify and fix vibration data - FIXED LOGIC
            expected_vibration = self.get_vibration_data(bore_diameter)
            current_vibration = data.get("vibration", {})
            
            # Debug logging
            print(f"🔍 Checking vibration data for {model_number} (bore: {bore_diameter}mm)")
            print(f"  Current:  {current_vibration}")
            print(f"  Expected: {expected_vibration}")
            
            # Only fix if there's a real discrepancy, not just overwrite correct data
            if expected_vibration and self._has_vibration_discrepancy(current_vibration, expected_vibration):
                print(f"❌ Vibration discrepancy detected - fixing")
                print(f"  Expected: {expected_vibration}")
                print(f"  Current:  {current_vibration}")
                data["vibration"] = expected_vibration
                needs_fix = True
            else:
                print(f"✅ Vibration data is correct")
            
            print()
            
            # Verify and fix SKF data
            expected_skf = self.get_skf_data(model_number)
            current_skf = data.get("dimensions", {}).get("skf_extended_dimensions", {})
            
            if expected_skf is None and current_skf:
                # Model doesn't exist in SKF lookup, should be null
                print(f"Fixing SKF data in {file_path.name} - setting to null")
                data["dimensions"]["skf_extended_dimensions"] = None
                needs_fix = True
            elif expected_skf and current_skf != expected_skf:
                print(f"Fixing SKF data in {file_path.name}")
                print(f"  Expected: {expected_skf}")
                print(f"  Current:  {current_skf}")
                data["dimensions"]["skf_extended_dimensions"] = expected_skf
                needs_fix = True
            
            # Save the file if fixes were made
            if needs_fix:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                self.stats["files_fixed"] += 1
                print(f"✅ Fixed {file_path.name}")
            else:
                print(f"✅ {file_path.name} - All data verified")
            
            self.stats["files_verified"] += 1
            return True
            
        except Exception as e:
            error_msg = f"Error processing {file_path.name}: {e}"
            self.stats["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return False

    def _has_vibration_discrepancy(self, current: Dict, expected: Dict) -> bool:
        """Check if there's a real discrepancy in vibration data that needs fixing."""
        try:
            # Check if the structure is different (e.g., wrong field names)
            if set(current.keys()) != set(expected.keys()):
                return True
            
            # Check if any values are actually different
            for v_class in expected:
                if v_class not in current:
                    return True
                
                for freq in expected[v_class]:
                    if freq not in current[v_class]:
                        return True
                    
                    if current[v_class][freq] != expected[v_class][freq]:
                        return True
            
            return False
            
        except Exception:
            # If there's any error in comparison, assume there's a discrepancy
            return True

    def scan_and_verify_all(self) -> None:
        """Scan through all JSON files and verify/fix them."""
        print("🔍 Starting technical data verification...")
        print(f"📁 Scanning directory: {self.models_dir}")
        print()
        
        # Get all JSON files
        json_files = list(self.models_dir.glob("*.json"))
        self.stats["total_files"] = len(json_files)
        
        if not json_files:
            print("❌ No JSON files found in models directory")
            return
        
        print(f"📊 Found {len(json_files)} JSON files to verify")
        print()
        
        # Process each file
        for file_path in sorted(json_files):
            if file_path.name == ".DS_Store":
                continue
            self.verify_and_fix_file(file_path)
            print()
        
        # Print summary
        self.print_summary()

    def print_summary(self) -> None:
        """Print verification summary."""
        print("=" * 60)
        print("📋 VERIFICATION SUMMARY")
        print("=" * 60)
        print(f"Total files found: {self.stats['total_files']}")
        print(f"Files verified: {self.stats['files_verified']}")
        print(f"Files fixed: {self.stats['files_fixed']}")
        print(f"Errors encountered: {len(self.stats['errors'])}")
        
        if self.stats["errors"]:
            print("\n❌ ERRORS:")
            for error in self.stats["errors"]:
                print(f"  - {error}")
        
        if self.stats["files_fixed"] > 0:
            print(f"\n✅ Successfully fixed {self.stats['files_fixed']} files")
        else:
            print("\n✅ All files are already accurate - no fixes needed")
        
        print("=" * 60)

    def run_verification(self) -> None:
        """Main method to run the verification process."""
        try:
            # Verify lookup tables are loaded
            if not all([self.noise_lookup, self.clearance_lookup, self.vibration_lookup, self.skf_lookup]):
                print("❌ Failed to load one or more lookup tables")
                return
            
            print("✅ All lookup tables loaded successfully")
            print()
            
            # Run verification
            self.scan_and_verify_all()
            
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            sys.exit(1)

def main():
    """Main entry point."""
    print("🔧 Technical Data Verification Script for Bearing Models")
    print("=" * 60)
    
    # Create verifier instance
    verifier = TechnicalDataVerifier()
    
    # Run verification
    verifier.run_verification()

if __name__ == "__main__":
    main()
