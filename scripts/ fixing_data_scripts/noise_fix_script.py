#!/usr/bin/env python3
# noise_fix_script.py
import json
import os
from pathlib import Path

def get_bearing_series(model_number):
    """Determine bearing series from model number"""
    model = str(model_number)
    
    # For 3-digit models (604, 623, 689, 698, etc.)
    if len(model) == 3 and model.isdigit():
        return '6000_series'
    
    # For 4-digit models
    if model.startswith('60'):
        return '6000_series'
    if model.startswith('62'):
        return '6200_series'
    if model.startswith('63'):
        return '6300_series'
    
    # Default fallback
    return '6200_series'

def find_noise_data(bore_diameter, series, noise_table):
    """Find noise data based on bore diameter and bearing series"""
    key = str(bore_diameter)
    series_data = noise_table['noise_lookup_table']['data'].get(key, {})
    
    if series_data and series in series_data:
        return series_data[series]
    
    return None

def fix_noise_data():
    # Load noise lookup table
    with open('docs/noise_lookup_table.json', 'r', encoding='utf-8') as f:
        noise_table = json.load(f)
    
    models_dir = Path('models/')
    json_files = list(models_dir.glob('*.json'))
    
    print('=== NOISE DATA FIX SCRIPT ===\n')
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        bore_diameter = content['dimensions']['bore_diameter_d_mm']
        model_number = content['model_number']
        
        print(f'--- Processing {model_number} ({json_file.name}) ---')
        print(f'Bore diameter: {bore_diameter}mm')
        
        # Determine bearing series
        series = get_bearing_series(model_number)
        print(f'Bearing series: {series}')
        
        # Find noise data
        noise_data = find_noise_data(bore_diameter, series, noise_table)
        
        if noise_data:
            print(f'Found noise data for {bore_diameter}mm bore in {series}')
            print(f'Z2: {noise_data["Z2"]}')
            print(f'Z3: {noise_data["Z3"]}')
            print(f'Z4: {noise_data["Z4"]}')
            
            # Update the file
            content['noise'] = {
                'Z2': noise_data['Z2'],
                'Z3': noise_data['Z3'],
                'Z4': noise_data['Z4']
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2)
            print(f'✅ Updated {json_file.name} with correct noise data')
        else:
            print(f'❌ No noise data found for {bore_diameter}mm bore in {series}')
            print(f'Setting all noise values to null')
            
            content['noise'] = {
                'Z2': None,
                'Z3': None,
                'Z4': None
            }
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2)
            print(f'✅ Updated {json_file.name} with null noise values')
    
    print('\n=== NOISE FIX COMPLETED ===')

if __name__ == '__main__':
    fix_noise_data()
