#!/usr/bin/env python3
"""
Add bearing_series_name field to all miniature series JSON files
==============================================================

This script adds the missing bearing_series_name field to all miniature series JSON files
to fix the speed limits conditional logic in the HTML template.

The field will be added before the model_number field in each JSON file.
"""

import json
import os
from pathlib import Path

def add_bearing_series_name_to_miniature_files():
    """Add bearing_series_name field to all miniature series JSON files"""
    
    # Path to models directory
    models_dir = Path("models")
    
    # Miniature series model numbers (3-digit models)
    miniature_series_models = [
        "604", "605", "606", "607", "608", "609",
        "623", "624", "625", "626", "627", "628", "629",
        "634", "635",
        "683", "684", "685", "686", "687", "688", "689",
        "693", "694", "695", "696", "697", "698", "699"
    ]
    
    print("🔧 Adding bearing_series_name to miniature series JSON files...")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    
    for model in miniature_series_models:
        json_file = models_dir / f"{model}.json"
        
        if not json_file.exists():
            print(f"⚠️  File not found: {json_file}")
            continue
            
        try:
            # Read the JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if bearing_series_name already exists
            if 'bearing_series_name' in data:
                print(f"✅ {model}: bearing_series_name already exists")
                continue
            
            # Create new data with bearing_series_name inserted before model_number
            new_data = {}
            for key, value in data.items():
                if key == 'model_number':
                    # Insert bearing_series_name before model_number
                    new_data['bearing_series_name'] = 'miniature-series'
                    new_data[key] = value
                else:
                    new_data[key] = value
            
            # Write the updated JSON back to file
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {model}: Added bearing_series_name = 'miniature-series'")
            success_count += 1
            
        except Exception as e:
            print(f"❌ {model}: Error processing file - {e}")
            error_count += 1
    
    print("=" * 60)
    print(f"📊 SUMMARY:")
    print(f"   ✅ Successfully updated: {success_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   🎯 Total miniature series models: {len(miniature_series_models)}")
    
    if success_count > 0:
        print(f"\n🎉 bearing_series_name field has been added to {success_count} files!")
        print("   This will fix the speed limits conditional logic in the HTML template.")
    else:
        print(f"\n⚠️  No files were updated. Check if the files already contain the field.")

if __name__ == "__main__":
    add_bearing_series_name_to_miniature_files()
