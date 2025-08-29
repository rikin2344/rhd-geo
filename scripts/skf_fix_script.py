#!/usr/bin/env python3
# skf_fix_script.py
import json
import os
from pathlib import Path

def get_skf_data(model_number, skf_table):
    """Get SKF extended dimensions for a specific model number"""
    if model_number in skf_table:
        skf_data = skf_table[model_number]
        return {
            "d1_shoulder_diameter": skf_data.get("d1"),
            "D2_recess_diameter": skf_data.get("D2"),
            "r1_chamfer_radius": skf_data.get("r1"),
            "r2_chamfer_radius": skf_data.get("r2")
        }
    return None

def fix_skf_data():
    # Load SKF dimensions lookup table
    with open('scripts/skf_dimensions_only.json', 'r', encoding='utf-8') as f:
        skf_table = json.load(f)
    
    models_dir = Path('models/')
    json_files = list(models_dir.glob('*.json'))
    
    print('=== SKF EXTENDED DIMENSIONS FIX SCRIPT ===\n')
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        model_number = content['model_number']
        
        print(f'--- Processing {model_number} ({json_file.name}) ---')
        
        # Get expected SKF data
        expected_skf = get_skf_data(model_number, skf_table)
        current_skf = content.get('dimensions', {}).get('skf_extended_dimensions')
        
        if expected_skf:
            print(f'Found SKF data for {model_number}:')
            print(f'  d1: {expected_skf["d1_shoulder_diameter"]}mm')
            print(f'  D2: {expected_skf["D2_recess_diameter"]}mm')
            print(f'  r1: {expected_skf["r1_chamfer_radius"]}mm')
            print(f'  r2: {expected_skf["r2_chamfer_radius"]}mm')
            
            # Check if current data is different from expected
            if current_skf != expected_skf:
                print(f'❌ SKF data mismatch detected!')
                if current_skf:
                    print(f'  Current: {current_skf}')
                else:
                    print(f'  Current: None/null')
                print(f'  Expected: {expected_skf}')
                
                # Update the file with correct SKF data
                if 'dimensions' not in content:
                    content['dimensions'] = {}
                content['dimensions']['skf_extended_dimensions'] = expected_skf
                
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2)
                print(f'✅ Updated {json_file.name} with correct SKF data')
            else:
                print(f'✅ SKF data is already correct')
        else:
            print(f'❌ No SKF data found for {model_number}')
            # If no SKF data exists for this model, set individual fields to null
            if current_skf:
                print(f'  Current SKF data exists but should be null')
                if 'dimensions' not in content:
                    content['dimensions'] = {}
                content['dimensions']['skf_extended_dimensions'] = {
                    "d1_shoulder_diameter": None,
                    "D2_recess_diameter": None,
                    "r1_chamfer_radius": None,
                    "r2_chamfer_radius": None
                }
                
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2)
                print(f'✅ Updated {json_file.name} - set SKF data fields to null')
            else:
                print(f'  SKF data already null - no change needed')
        
        print()
    
    print('=== SKF EXTENDED DIMENSIONS FIX COMPLETED ===')

if __name__ == '__main__':
    fix_skf_data()
