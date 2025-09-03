#!/usr/bin/env python3
"""
Fix Duplicate Scripts in Deployment Files
========================================

This script fixes duplicate JavaScript content in deployment files.
The issue occurs when the universal bearing page generator duplicates
script blocks when creating standalone pages.

USAGE:
======
python3 scripts/fix_duplicate_scripts.py

REQUIREMENTS:
=============
- Run from root workspace directory
"""

import os
import re
from pathlib import Path

def fix_duplicate_scripts_in_file(file_path):
    """Fix duplicate scripts in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find all script blocks
        script_pattern = r'<script>.*?</script>'
        scripts = re.findall(script_pattern, content, flags=re.DOTALL)
        
        if len(scripts) <= 1:
            # No duplicates found
            return False
        
        print(f"   Found {len(scripts)} script blocks in {file_path.name}")
        
        # Keep only the first occurrence of each unique script
        seen_scripts = set()
        unique_scripts = []
        
        for script in scripts:
            # Normalize script content for comparison (remove whitespace differences)
            normalized_script = re.sub(r'\s+', ' ', script.strip())
            if normalized_script not in seen_scripts:
                seen_scripts.add(normalized_script)
                unique_scripts.append(script)
        
        if len(unique_scripts) < len(scripts):
            print(f"   Removing {len(scripts) - len(unique_scripts)} duplicate script(s)")
            
            # Replace all scripts with unique scripts
            # First, remove all script blocks
            content = re.sub(script_pattern, '<!-- SCRIPT_PLACEHOLDER -->', content, flags=re.DOTALL)
            
            # Then add back the unique scripts
            for script in unique_scripts:
                content = content.replace('<!-- SCRIPT_PLACEHOLDER -->', script, 1)
            
            # Remove any remaining placeholders
            content = content.replace('<!-- SCRIPT_PLACEHOLDER -->', '')
            
            # Write the fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix duplicate scripts in deployment files"""
    print("🔧 FIXING DUPLICATE SCRIPTS IN DEPLOYMENT FILES")
    print("=" * 50)
    
    # Find all deployment directories
    deployment_dir = Path("deployment")
    if not deployment_dir.exists():
        print("❌ Deployment directory not found")
        return False
    
    fixed_count = 0
    total_count = 0
    
    # Process all series directories
    for series_dir in deployment_dir.iterdir():
        if series_dir.is_dir():
            index_file = series_dir / "index.html"
            if index_file.exists():
                print(f"🔧 Processing {series_dir.name}...")
                total_count += 1
                
                try:
                    fixed = fix_duplicate_scripts_in_file(index_file)
                    if fixed:
                        print(f"   ✅ Fixed duplicate scripts in {series_dir.name}")
                        fixed_count += 1
                    else:
                        print(f"   ℹ️  No duplicate scripts found in {series_dir.name}")
                except Exception as e:
                    print(f"   ❌ Error processing {series_dir.name}: {e}")
    
    print(f"\n" + "=" * 50)
    print(f"📊 SUMMARY")
    print(f"=" * 50)
    print(f"✅ Files processed: {total_count}")
    print(f"🔧 Files fixed: {fixed_count}")
    print(f"ℹ️  Files unchanged: {total_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n🎉 Successfully fixed duplicate scripts in {fixed_count} file(s)!")
        return True
    else:
        print(f"\nℹ️  No duplicate scripts were found")
        return True

if __name__ == "__main__":
    main()
