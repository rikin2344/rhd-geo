#!/usr/bin/env python3
# vibration_fix_script.py
import json
import os
from pathlib import Path

def find_vibration_data(bore_diameter, vibration_table):
    """Look up vibration data by bore diameter as key"""
    key = str(bore_diameter)
    return vibration_table['vibration_lookup_table']['data'].get(key)

def fix_vibration_data():
    # Load vibration lookup table
    with open('docs/vibration_lookup_table.json', 'r', encoding='utf-8') as f:
        vibration_table = json.load(f)
    
    models_dir = Path('models/')
    json_files = list(models_dir.glob('*.json'))
    
    print('=== VIBRATION DATA FIX SCRIPT ===\n')
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        bore_diameter = content['dimensions']['bore_diameter_d_mm']
        model_number = content['model_number']
        
        print(f'--- Processing {model_number} ({json_file.name}) ---')
        print(f'Bore diameter: {bore_diameter}mm')
        
        # Find vibration data
        vibration_data = find_vibration_data(bore_diameter, vibration_table)
        
        if vibration_data:
            print(f'Found vibration data for {bore_diameter}mm bore')
            print(f'V2: Low={vibration_data["V2"]["low"]}, Medium={vibration_data["V2"]["medium"]}, High={vibration_data["V2"]["high"]}')
            print(f'V3: Low={vibration_data["V3"]["low"]}, Medium={vibration_data["V3"]["medium"]}, High={vibration_data["V3"]["high"]}')
            print(f'V4: Low={vibration_data["V4"]["low"]}, Medium={vibration_data["V4"]["medium"]}, High={vibration_data["V4"]["high"]}')
            
            # Update the file
            content['vibration'] = {
                'V2': {
                    'low_frequency': vibration_data['V2']['low'],
                    'medium_frequency': vibration_data['V2']['medium'],
                    'high_frequency': vibration_data['V2']['high']
                },
                'V3': {
                    'low_frequency': vibration_data['V3']['low'],
                    'medium_frequency': vibration_data['V3']['medium'],
                    'high_frequency': vibration_data['V3']['high']
                },
                'V4': {
                    'low_frequency': vibration_data['V4']['low'],
                    'medium_frequency': vibration_data['V4']['medium'],
                    'high_frequency': vibration_data['V4']['high']
                }
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2)
            print(f'✅ Updated {json_file.name} with correct vibration data')
        else:
            print(f'❌ No vibration data found for {bore_diameter}mm bore')
            print(f'Setting all vibration values to null')
            
            content['vibration'] = {
                'V2': {'low_frequency': None, 'medium_frequency': None, 'high_frequency': None},
                'V3': {'low_frequency': None, 'medium_frequency': None, 'high_frequency': None},
                'V4': {'low_frequency': None, 'medium_frequency': None, 'high_frequency': None}
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2)
            print(f'✅ Updated {json_file.name} with null vibration values')
    
    print('\n=== VIBRATION FIX COMPLETED ===')

if __name__ == '__main__':
    fix_vibration_data()
