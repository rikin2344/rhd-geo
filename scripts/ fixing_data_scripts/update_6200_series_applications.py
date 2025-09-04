#!/usr/bin/env python3
# update_6200_series_applications.py
import json
import os
from pathlib import Path

def update_6200_series_applications():
    """Update applications section in all 6900-6920 model JSON files"""
    
    # Load the applications data from the reference file
    applications_file = Path('docs/6200 Series Applications.json')
    models_dir = Path('models/')
    
    print('=== UPDATING 6900 SERIES APPLICATIONS ===\n')
    
    # Read the applications data
    with open(applications_file, 'r', encoding='utf-8') as f:
        applications_data = json.load(f)
    
    # Process each model from 6900 to 6920
    updated_count = 0
    total_count = 0
    
    for model_num in range(6900, 6921):
        model_file = models_dir / f'{model_num}.json'
        
        if not model_file.exists():
            print(f'⚠️  Model {model_num}.json not found, skipping...')
            continue
            
        total_count += 1
        print(f'--- Processing {model_num}.json ---')
        
        # Read the model JSON file
        with open(model_file, 'r', encoding='utf-8') as f:
            model_data = json.load(f)
        
        # Check if this model has applications data
        if str(model_num) in applications_data:
            # Get the applications data for this model
            model_applications = applications_data[str(model_num)]['applications']
            
            # Update the applications section in the model file
            model_data['applications'] = model_applications
            
            # Write the updated data back to the file
            with open(model_file, 'w', encoding='utf-8') as f:
                json.dump(model_data, f, indent=2, ensure_ascii=False)
            
            print(f'✅ Updated {model_num}.json with new applications data')
            updated_count += 1
            
            # Show what was updated
            for app_key, app_data in model_applications.items():
                print(f'   {app_data["title"]}: {len(app_data["applications"])} applications')
        else:
            print(f'⚠️  No applications data found for model {model_num}')
    
    print(f'\n=== APPLICATIONS UPDATE COMPLETED ===')
    print(f'Total models processed: {total_count}')
    print(f'Successfully updated: {updated_count}')
    print(f'Models with no data: {total_count - updated_count}')

if __name__ == '__main__':
    update_6200_series_applications()
