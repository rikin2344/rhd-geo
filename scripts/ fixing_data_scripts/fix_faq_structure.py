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
import re

def fix_faq_structure(file_path):
    """Fix FAQ structure in a JSON file"""
    print(f"Fixing {file_path}...")
    
    # Read the file as text first to handle the malformed JSON
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if faqs exist
    if '"faqs"' not in content:
        print(f"  No FAQs found in {file_path}")
        return False
    
    fixed = False
    
    # Define the correct structure for each FAQ category
    faq_categories = {
        'selection_replacement': 'Bearing Selection & Replacement',
        'installation_maintenance': 'Installation & Maintenance', 
        'troubleshooting': 'Troubleshooting',
        'cost_performance': 'Cost & Performance'
    }
    
    # Fix each category by finding and replacing duplicate title/questions structures
    for category_key, title in faq_categories.items():
        # Look for the category in the content
        category_pattern = f'"{category_key}":\\s*{{'
        if re.search(category_pattern, content):
            # Count how many times title and questions appear in this category
            # Find the category section - need to be more precise about boundaries
            # Look for the category and find its closing brace by counting braces
            category_start = content.find(f'"{category_key}": {{')
            if category_start != -1:
                # Find the matching closing brace
                brace_count = 0
                category_end = category_start
                in_category = False
                
                for i, char in enumerate(content[category_start:], category_start):
                    if char == '{':
                        brace_count += 1
                        in_category = True
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0 and in_category:
                            category_end = i + 1
                            break
                
                category_section = content[category_start:category_end]
                title_count = category_section.count('"title":')
                questions_count = category_section.count('"questions":')
                
                if title_count > 1 or questions_count > 1:
                    print(f"  Fixing duplicate title/questions structure in {category_key}...")
                elif category_section.count('      {') > 0 or category_section.count('            "') > 0:
                    print(f"  Fixing indentation issues in {category_key}...")
                    
                    # Extract all question objects from the malformed structure
                    all_questions = []
                    
                    # Find all questions arrays in this category
                    questions_pattern = r'"questions":\s*\[(.*?)\]'
                    questions_matches = re.findall(questions_pattern, category_section, re.DOTALL)
                    
                    for questions_content in questions_matches:
                        # Extract individual question objects
                        question_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                        question_matches = re.findall(question_pattern, questions_content)
                        
                        for question_str in question_matches:
                            try:
                                question_obj = json.loads(question_str)
                                all_questions.append(question_obj)
                            except json.JSONDecodeError:
                                # Try to fix common JSON issues
                                try:
                                    # Remove trailing commas
                                    question_str = re.sub(r',\s*}', '}', question_str)
                                    question_str = re.sub(r',\s*]', ']', question_str)
                                    question_obj = json.loads(question_str)
                                    all_questions.append(question_obj)
                                except:
                                    print(f"    Warning: Could not parse question object")
                                    continue
                    
                    # Create the corrected category structure with proper indentation
                    # First, create the corrected category as a Python dict
                    corrected_category_dict = {
                        "title": title,
                        "questions": all_questions
                    }
                    
                    # Format it with proper 2-space indentation to match the JSON file
                    category_json = json.dumps(corrected_category_dict, indent=2, ensure_ascii=False)
                    # Add the proper indentation for the category key (4 spaces)
                    corrected_category = f'    "{category_key}": {category_json}'
                    
                    # Replace the malformed category with the corrected one
                    content = content[:category_start] + corrected_category + content[category_end:]
                    fixed = True
                else:
                    print(f"  {category_key} already has correct structure")
    
    # Write back to file if changes were made
    if fixed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
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
        # Generate file lists for 6900 series (6900-6920) and 16000 series (16001-16020)
        files_to_fix = []
        
        # 6900 series files (6900-6920)
        for i in range(6900, 6921):
            file_path = f'models/{i}.json'
            if os.path.exists(file_path):
                files_to_fix.append(file_path)
        
        # 16000 series files (16001-16020)
        for i in range(16001, 16021):
            file_path = f'models/{i}.json'
            if os.path.exists(file_path):
                files_to_fix.append(file_path)
        
        print("🔧 Fixing FAQ data structure in 6900 series (6900-6920) and 16000 series (16001-16020) files...")
        print("=" * 80)
        
        fixed_count = 0
        for file_path in files_to_fix:
            if fix_faq_structure(file_path):
                fixed_count += 1
        
        print("=" * 80)
        print(f"✅ Fixed {fixed_count} out of {len(files_to_fix)} files")
        print("🎉 FAQ structure fix completed!")

if __name__ == "__main__":
    main()
