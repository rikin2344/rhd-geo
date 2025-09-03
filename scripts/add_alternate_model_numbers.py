#!/usr/bin/env python3
"""
Script to add alternate_model_number attribute to 6800 series bearing JSON files.
6800 -> 61800, 6801 -> 61801, etc.
"""

import json
import os

def add_alternate_model_numbers():
    """Add alternate_model_number to all 6800 series JSON files."""
    
    # Explicitly define the 6800 series model numbers
    model_numbers = []
    for i in range(21):  # 6800 to 6820
        if i < 10:
            model_numbers.append(f"680{i}")
        else:
            model_numbers.append(f"68{i}")
    
    # Get all 6800 series JSON files
    series_files = []
    for model_num in model_numbers:
        file_path = f"models/{model_num}.json"
        if os.path.exists(file_path):
            series_files.append(file_path)
    
    print(f"Found {len(series_files)} 6800 series files to process:")
    
    for file_path in series_files:
        try:
            # Extract model number from filename
            filename = os.path.basename(file_path)
            model_number = filename.replace('.json', '')
            
            # Calculate alternate model number (add 55000 to original)
            # 6800 + 55000 = 61800, 6801 + 55000 = 61801, etc.
            alternate_model_number = int(model_number) + 55000
            
            print(f"Processing {model_number} -> {alternate_model_number}")
            
            # Read the JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Add alternate_model_number after model_number
            if 'model_number' in data:
                # Create new ordered dict to maintain position
                new_data = {}
                
                # Copy all keys up to and including model_number
                for key, value in data.items():
                    new_data[key] = value
                    if key == 'model_number':
                        # Add alternate_model_number right after model_number
                        new_data['alternate_model_number'] = str(alternate_model_number)
                
                # Write back to file with proper formatting
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(new_data, f, indent=2, ensure_ascii=False)
                
                print(f"  ✓ Added alternate_model_number: {alternate_model_number}")
            else:
                print(f"  ✗ No model_number found in {file_path}")
                
        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {e}")
    
    print(f"\nCompleted processing {len(series_files)} files.")

if __name__ == "__main__":
    add_alternate_model_numbers()
