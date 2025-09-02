#!/usr/bin/env python3
"""
Script to fix FAQ data structure in bearing JSON files
Converts direct arrays to proper structure with title and questions fields

This script addresses the issue where some JSON files have FAQ data as direct arrays
instead of the expected structure with 'title' and 'questions' fields.

Usage:
    python3 fix_faq_structure.py [file_path]
    
If no file_path is provided, it will fix the known problematic 62200 series files.
"""

import json
import os
import sys

def fix_faq_structure(file_path):
    """Fix FAQ structure in a JSON file"""
    print(f"Fixing {file_path}...")
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if faqs exist
    if 'faqs' not in data:
        print(f"  No FAQs found in {file_path}")
        return False
    
    faqs = data['faqs']
    fixed = False
    
    # Define the correct structure for each FAQ category
    faq_categories = {
        'selection_replacement': 'Bearing Selection & Replacement',
        'installation_maintenance': 'Installation & Maintenance', 
        'troubleshooting': 'Troubleshooting',
        'cost_performance': 'Cost & Performance'
    }
    
    # Fix each category
    for category_key, title in faq_categories.items():
        if category_key in faqs:
            category_data = faqs[category_key]
            
            # Check if it's already in correct format
            if isinstance(category_data, dict) and 'title' in category_data and 'questions' in category_data:
                print(f"  {category_key} already has correct structure")
                continue
            
            # Check if it's a direct array (incorrect format)
            if isinstance(category_data, list):
                print(f"  Fixing {category_key} structure...")
                faqs[category_key] = {
                    "title": title,
                    "questions": category_data
                }
                fixed = True
            else:
                print(f"  {category_key} has unexpected structure: {type(category_data)}")
    
    # Write back to file if changes were made
    if fixed:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Fixed {file_path}")
        return True
    else:
        print(f"  No changes needed for {file_path}")
        return False

def main():
    """Main function to fix FAQ structure"""
    if len(sys.argv) > 1:
        # Fix specific file provided as argument
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            fix_faq_structure(file_path)
        else:
            print(f"❌ File not found: {file_path}")
    else:
        # Fix known problematic files
        problematic_files = [
            'models/62216.json',
            'models/62217.json',
            'models/62218.json', 
            'models/62219.json',
            'models/62220.json'
        ]
        
        print("🔧 Fixing FAQ data structure in 62200 series files...")
        print("=" * 60)
        
        fixed_count = 0
        for file_path in problematic_files:
            if os.path.exists(file_path):
                if fix_faq_structure(file_path):
                    fixed_count += 1
            else:
                print(f"❌ File not found: {file_path}")
        
        print("=" * 60)
        print(f"✅ Fixed {fixed_count} files")
        print("🎉 FAQ structure fix completed!")

if __name__ == "__main__":
    main()
