#!/usr/bin/env python3
# fix_null_skf_structure.py
import json
import os
from pathlib import Path

def fix_null_skf_structure():
    """Replace simple null SKF extended dimensions with structured null fields"""
    
    models_dir = Path('models/')
    json_files = list(models_dir.glob('*.json'))
    
    print('=== FIXING NULL SKF EXTENDED DIMENSIONS STRUCTURE ===\n')
    
    fixed_count = 0
    total_count = 0
    
    for json_file in json_files:
        total_count += 1
        with open(json_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        model_number = content['model_number']
        
        # Check if dimensions section exists
        if 'dimensions' not in content:
            continue
            
        # Check if skf_extended_dimensions is exactly null
        current_skf = content['dimensions'].get('skf_extended_dimensions')
        
        if current_skf is None:
            print(f'--- Processing {model_number} ({json_file.name}) ---')
            print(f'  Found simple null SKF data - converting to structured null')
            
            # Replace null with structured null object
            content['dimensions']['skf_extended_dimensions'] = {
                "d1_shoulder_diameter": None,
                "D2_recess_diameter": None,
                "r1_chamfer_radius": None,
                "r2_chamfer_radius": None
            }
            
            # Save the updated file
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2)
            
            print(f'✅ Updated {json_file.name} with structured null SKF data')
            fixed_count += 1
            print()
    
    print('=== NULL SKF STRUCTURE FIX COMPLETED ===')
    print(f'Total files processed: {total_count}')
    print(f'Files fixed: {fixed_count}')
    print(f'Files unchanged: {total_count - fixed_count}')

if __name__ == '__main__':
    fix_null_skf_structure()
