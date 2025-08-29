#!/usr/bin/env python3
# clearance_fix_script.py
import json
import os
from pathlib import Path

def find_clearance_range(bore_diameter, clearance_table):
    """Find clearance range where: over_mm < bore_diameter <= to_mm"""
    for range_data in clearance_table['clearance_lookup_table']['ranges']:
        if range_data['over_mm'] < bore_diameter <= range_data['to_mm']:
            return range_data['clearances']
    return None

def fix_clearance_data():
    # Load clearance lookup table
    with open('docs/clearance_lookup_table.json', 'r', encoding='utf-8') as f:
        clearance_table = json.load(f)
    
    models_dir = Path('models/')
    json_files = list(models_dir.glob('*.json'))
    
    print('=== CLEARANCE DATA FIX SCRIPT ===\n')
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        bore_diameter = content['dimensions']['bore_diameter_d_mm']
        model_number = content['model_number']
        
        print(f'--- Processing {model_number} ({json_file.name}) ---')
        print(f'Bore diameter: {bore_diameter}mm')
        
        # Find clearance data
        clearance_data = find_clearance_range(bore_diameter, clearance_table)
        
        if clearance_data:
            print(f'Found clearance data for range: {bore_diameter}mm')
            print(f'C2: {clearance_data["C2"]["min"]}-{clearance_data["C2"]["max"]} microns')
            print(f'C0: {clearance_data["C0"]["min"]}-{clearance_data["C0"]["max"]} microns')
            print(f'C3: {clearance_data["C3"]["min"]}-{clearance_data["C3"]["max"]} microns')
            print(f'C4: {clearance_data["C4"]["min"]}-{clearance_data["C4"]["max"]} microns')
            print(f'C5: {clearance_data["C5"]["min"]}-{clearance_data["C5"]["max"]} microns')
            
            # Update the file
            content['clearance'] = {
                'C2': {'min_microns': clearance_data['C2']['min'], 'max_microns': clearance_data['C2']['max']},
                'C0': {'min_microns': clearance_data['C0']['min'], 'max_microns': clearance_data['C0']['max']},
                'C3': {'min_microns': clearance_data['C3']['min'], 'max_microns': clearance_data['C3']['max']},
                'C4': {'min_microns': clearance_data['C4']['min'], 'max_microns': clearance_data['C4']['max']},
                'C5': {'min_microns': clearance_data['C5']['min'], 'max_microns': clearance_data['C5']['max']}
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2)
            print(f'✅ Updated {json_file.name} with correct clearance data')
        else:
            print(f'❌ No clearance data found for {bore_diameter}mm bore')
            print(f'Setting all clearance values to null')
            
            content['clearance'] = {
                'C2': {'min_microns': None, 'max_microns': None},
                'C0': {'min_microns': None, 'max_microns': None},
                'C3': {'min_microns': None, 'max_microns': None},
                'C4': {'min_microns': None, 'max_microns': None},
                'C5': {'min_microns': None, 'max_microns': None}
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2)
            print(f'✅ Updated {json_file.name} with null clearance values')
    
    print('\n=== CLEARANCE FIX COMPLETED ===')

if __name__ == '__main__':
    fix_clearance_data()
