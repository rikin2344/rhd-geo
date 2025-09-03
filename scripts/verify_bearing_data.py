#!/usr/bin/env python3
"""
Script to verify bearing dimensional data in JSON files against bearing_database.json
Checks: bore_diameter_d_mm, outer_diameter_D_mm, width_B_mm, weight_kg
"""

import json
import os
import glob

def load_bearing_database():
    """Load the bearing database for reference data."""
    try:
        with open('docs/bearing_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['bearings']
    except Exception as e:
        print(f"Error loading bearing database: {e}")
        return []

def get_model_data_from_database(bearings_db, model_number):
    """Get bearing data from database for a specific model."""
    for bearing in bearings_db:
        if bearing['model'] == model_number:
            return bearing
    return None

def verify_model_file(file_path, bearings_db):
    """Verify a single model JSON file against the database."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            model_data = json.load(f)
        
        model_number = model_data.get('model_number', '')
        if not model_number:
            return None, f"No model_number found in {file_path}"
        
        # Get reference data from database
        db_data = get_model_data_from_database(bearings_db, model_number)
        if not db_data:
            return None, f"Model {model_number} not found in bearing database"
        
        # Check each field
        discrepancies = []
        
        # Check bore diameter (d)
        json_bore = model_data.get('dimensions', {}).get('bore_diameter_d_mm')
        db_bore = db_data.get('d')
        if json_bore != db_bore:
            discrepancies.append(f"bore_diameter_d_mm: JSON={json_bore}, DB={db_bore}")
        
        # Check outer diameter (D)
        json_outer = model_data.get('dimensions', {}).get('outer_diameter_D_mm')
        db_outer = db_data.get('D')
        if json_outer != db_outer:
            discrepancies.append(f"outer_diameter_D_mm: JSON={json_outer}, DB={db_outer}")
        
        # Check width (B)
        json_width = model_data.get('dimensions', {}).get('width_B_mm')
        db_width = db_data.get('B')
        if json_width != db_width:
            discrepancies.append(f"width_B_mm: JSON={json_width}, DB={db_width}")
        
        # Check weight
        json_weight = model_data.get('dimensions', {}).get('weight_kg')
        db_weight = db_data.get('weight')
        if json_weight != db_weight:
            discrepancies.append(f"weight_kg: JSON={json_weight}, DB={db_weight}")
        
        # Check dynamic load rating (Cr)
        json_cr = model_data.get('load_ratings', {}).get('dynamic_load_Cr_kN')
        db_cr = db_data.get('Cr')
        if json_cr != db_cr:
            discrepancies.append(f"dynamic_load_Cr_kN: JSON={json_cr}, DB={db_cr}")
        
        # Check static load rating (Cor)
        json_cor = model_data.get('load_ratings', {}).get('static_load_Cor_kN')
        db_cor = db_data.get('Cor')
        if json_cor != db_cor:
            discrepancies.append(f"static_load_Cor_kN: JSON={json_cor}, DB={db_cor}")
        
        # Check grease RPM
        json_grease_rpm = model_data.get('speed_limits', {}).get('grease_rpm')
        db_grease_rpm = db_data.get('grease_rpm')
        if json_grease_rpm != db_grease_rpm:
            discrepancies.append(f"grease_rpm: JSON={json_grease_rpm}, DB={db_grease_rpm}")
        
        # Check oil RPM
        json_oil_rpm = model_data.get('speed_limits', {}).get('oil_rpm')
        db_oil_rpm = db_data.get('oil_rpm')
        if json_oil_rpm != db_oil_rpm:
            discrepancies.append(f"oil_rpm: JSON={json_oil_rpm}, DB={db_oil_rpm}")
        
        # Check recommended_max_rpm is 90% of grease_rpm
        json_recommended_max = model_data.get('speed_limits', {}).get('recommended_max_rpm')
        if db_grease_rpm and json_recommended_max:
            expected_max_rpm = int(db_grease_rpm * 0.9)
            if json_recommended_max != expected_max_rpm:
                discrepancies.append(f"recommended_max_rpm: JSON={json_recommended_max}, Expected={expected_max_rpm} (90% of grease_rpm={db_grease_rpm})")
        
        # Check load_capacity_kg conversion (Cr_kN * 1000 / 9.81)
        json_load_capacity = model_data.get('load_ratings', {}).get('load_capacity_kg')
        if db_cr and json_load_capacity:
            expected_load_capacity = int(db_cr * 1000 / 9.81)
            if json_load_capacity != expected_load_capacity:
                discrepancies.append(f"load_capacity_kg: JSON={json_load_capacity}, Expected={expected_load_capacity} (Cr={db_cr}kN * 1000 / 9.81)")
        
        return model_number, discrepancies
        
    except Exception as e:
        return None, f"Error processing {file_path}: {e}"

def fix_model_file(file_path, bearings_db):
    """Fix discrepancies in a model JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            model_data = json.load(f)
        
        model_number = model_data.get('model_number', '')
        db_data = get_model_data_from_database(bearings_db, model_number)
        
        if not db_data:
            return False, f"Model {model_number} not found in database"
        
        # Fix the dimensions
        if 'dimensions' not in model_data:
            model_data['dimensions'] = {}
        
        model_data['dimensions']['bore_diameter_d_mm'] = db_data['d']
        model_data['dimensions']['outer_diameter_D_mm'] = db_data['D']
        model_data['dimensions']['width_B_mm'] = db_data['B']
        model_data['dimensions']['weight_kg'] = db_data['weight']
        
        # Fix the load ratings
        if 'load_ratings' not in model_data:
            model_data['load_ratings'] = {}
        
        model_data['load_ratings']['dynamic_load_Cr_kN'] = db_data['Cr']
        model_data['load_ratings']['static_load_Cor_kN'] = db_data['Cor']
        model_data['load_ratings']['load_capacity_kg'] = int(db_data['Cr'] * 1000 / 9.81)
        
        # Fix the speed limits
        if 'speed_limits' not in model_data:
            model_data['speed_limits'] = {}
        
        model_data['speed_limits']['grease_rpm'] = db_data['grease_rpm']
        model_data['speed_limits']['oil_rpm'] = db_data['oil_rpm']
        model_data['speed_limits']['recommended_max_rpm'] = int(db_data['grease_rpm'] * 0.9)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, indent=2, ensure_ascii=False)
        
        return True, f"Fixed {model_number}"
        
    except Exception as e:
        return False, f"Error fixing {file_path}: {e}"

def main():
    """Main function to verify and fix bearing data."""
    print("Loading bearing database...")
    bearings_db = load_bearing_database()
    
    if not bearings_db:
        print("Failed to load bearing database. Exiting.")
        return
    
    print(f"Loaded {len(bearings_db)} bearings from database")
    
    # Get all model JSON files
    model_files = glob.glob('models/*.json')
    model_files.sort()
    
    print(f"\nFound {len(model_files)} model files to verify")
    
    # Track results
    correct_models = []
    incorrect_models = []
    not_found_models = []
    error_models = []
    
    print("\n" + "="*80)
    print("VERIFICATION RESULTS")
    print("="*80)
    
    for file_path in model_files:
        model_number, result = verify_model_file(file_path, bearings_db)
        
        if model_number is None:
            error_models.append((file_path, result))
            print(f"❌ ERROR: {result}")
        elif isinstance(result, list) and len(result) == 0:
            correct_models.append(model_number)
            print(f"✅ {model_number}: All data correct")
        elif isinstance(result, list):
            incorrect_models.append((model_number, result))
            print(f"❌ {model_number}: {len(result)} discrepancies")
            for discrepancy in result:
                print(f"   - {discrepancy}")
        else:
            not_found_models.append((model_number, result))
            print(f"⚠️  {model_number}: {result}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ Correct models: {len(correct_models)}")
    print(f"❌ Incorrect models: {len(incorrect_models)}")
    print(f"⚠️  Not found in database: {len(not_found_models)}")
    print(f"🚫 Error processing: {len(error_models)}")
    
    if incorrect_models:
        print(f"\n📋 INCORRECT MODELS TO FIX:")
        for model_number, discrepancies in incorrect_models:
            print(f"   - {model_number} ({len(discrepancies)} issues)")
    
    if not_found_models:
        print(f"\n⚠️  MODELS NOT FOUND IN DATABASE:")
        for model_number, reason in not_found_models:
            print(f"   - {model_number}: {reason}")
    
    if error_models:
        print(f"\n🚫 MODELS WITH ERRORS:")
        for file_path, error in error_models:
            print(f"   - {file_path}: {error}")
    
    # Ask if user wants to fix the incorrect models
    if incorrect_models:
        print(f"\n" + "="*80)
        response = input(f"Do you want to fix the {len(incorrect_models)} incorrect models? (y/n): ").lower().strip()
        
        if response == 'y':
            print("\nFixing incorrect models...")
            fixed_count = 0
            failed_count = 0
            
            for model_number, discrepancies in incorrect_models:
                file_path = f"models/{model_number}.json"
                success, message = fix_model_file(file_path, bearings_db)
                
                if success:
                    fixed_count += 1
                    print(f"✅ {message}")
                else:
                    failed_count += 1
                    print(f"❌ {message}")
            
            print(f"\nFix Summary:")
            print(f"✅ Successfully fixed: {fixed_count}")
            print(f"❌ Failed to fix: {failed_count}")
        else:
            print("Skipping fixes.")

if __name__ == "__main__":
    main()
