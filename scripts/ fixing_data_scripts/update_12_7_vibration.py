#!/usr/bin/env python3
# update_12_7_vibration.py
import json
import os
from pathlib import Path

def update_12_7_data():
    """Copy vibration, noise, clearance, and SKF data from standard models to their 12.7mm variants"""
    
    models_dir = Path('models/')
    
    # Define the mappings: 12.7mm variant -> standard model
    mappings = {
        '6201 12.7.json': '6201.json',
        '6202 12.7.json': '6202.json', 
        '6203 12.7.json': '6203.json'
    }
    
    print('=== UPDATING 12.7MM VARIANT DATA (VIBRATION, NOISE, CLEARANCE, SKF) ===\n')
    
    for variant_file, standard_file in mappings.items():
        variant_path = models_dir / variant_file
        standard_path = models_dir / standard_file
        
        if not variant_path.exists():
            print(f'❌ Variant file not found: {variant_file}')
            continue
            
        if not standard_path.exists():
            print(f'❌ Standard file not found: {standard_file}')
            continue
        
        # Load both files
        with open(variant_path, 'r', encoding='utf-8') as f:
            variant_data = json.load(f)
            
        with open(standard_path, 'r', encoding='utf-8') as f:
            standard_data = json.load(f)
        
        print(f'--- Processing {variant_file} ---')
        
        # Copy vibration data
        old_vibration = variant_data['vibration']
        new_vibration = standard_data['vibration']
        variant_data['vibration'] = new_vibration
        print(f'   Vibration - Updated from standard model')
        
        # Copy noise data (only if variant has null values)
        old_noise = variant_data['noise']
        if (old_noise['Z2'] is None or old_noise['Z3'] is None or old_noise['Z4'] is None):
            new_noise = standard_data['noise']
            variant_data['noise'] = new_noise
            print(f'   Noise     - Updated from standard model')
        else:
            print(f'   Noise     - Already has correct data')
        
        # Copy clearance data
        if 'clearance' in variant_data and 'clearance' in standard_data:
            old_clearance = variant_data['clearance']
            new_clearance = standard_data['clearance']
            variant_data['clearance'] = new_clearance
            print(f'   Clearance - Updated from standard model')
        else:
            print(f'   Clearance - Field not found, skipping')
        
        # Copy SKF extended dimensions
        if 'dimensions' in standard_data and 'skf_extended_dimensions' in standard_data['dimensions']:
            # Create SKF data structure from standard model
            skf_data = standard_data['dimensions']['skf_extended_dimensions']
            if 'dimensions' not in variant_data:
                variant_data['dimensions'] = {}
            variant_data['dimensions']['skf_extended_dimensions'] = skf_data
            print(f'   SKF       - Updated from standard model')
        else:
            print(f'   SKF       - Field not found in standard model, skipping')
        
        # Save updated variant file
        with open(variant_path, 'w', encoding='utf-8') as f:
            json.dump(variant_data, f, indent=2, ensure_ascii=False)
        
        print(f'✅ Updated {variant_file} with all data from {standard_file}')
        print()
    
    print('=== 12.7MM VARIANT DATA UPDATE COMPLETED ===')

if __name__ == '__main__':
    update_12_7_data()
