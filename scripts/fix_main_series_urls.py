#!/usr/bin/env python3
"""
Fix Main Series Page URLs Script
===============================

This script fixes the missing /specs path in the main series page URLs.
The issue is that URLs like "/6800-series/6801" should be "/specs/6800-series/6801".

This script:
1. Scans all main series pages in webpages/{series}SeriesWebPage/index.html
2. Updates the JavaScript data arrays to include the correct /specs path
3. Preserves all other data while fixing the URL format

USAGE:
======
python3 scripts/fix_main_series_urls.py

REQUIREMENTS:
=============
- Run from root workspace directory
- All main series pages should exist in webpages/{series}SeriesWebPage/
"""

import os
import re
from pathlib import Path

def get_series_directories():
    """Get all series directories that contain main pages"""
    webpages_dir = Path("webpages")
    series_dirs = []
    
    for item in webpages_dir.iterdir():
        if item.is_dir() and item.name.endswith("SeriesWebPage"):
            series_dirs.append(item)
    
    return series_dirs

def fix_urls_in_file(file_path):
    """Fix URLs in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match URLs in JavaScript data arrays
        # Matches: "url": "/6800-series/6801" -> "url": "/specs/6800-series/6801"
        url_pattern = r'"url":\s*"/([^"]*)"'
        
        def replace_url(match):
            url_path = match.group(1)
            # Only add /specs if it's not already there and it's a series/model URL
            if not url_path.startswith('specs/') and '/' in url_path:
                return f'"url": "/specs/{url_path}"'
            return match.group(0)
        
        # Apply the replacement
        content = re.sub(url_pattern, replace_url, content)
        
        # Check if any changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix URLs in all main series pages"""
    print("🔧 FIXING MAIN SERIES PAGE URLs")
    print("=" * 50)
    print("This script will add the missing /specs path to all model URLs")
    print("=" * 50)
    
    # Get all series directories
    series_dirs = get_series_directories()
    
    if not series_dirs:
        print("❌ No series directories found in webpages/")
        return False
    
    print(f"📋 Found {len(series_dirs)} series directories:")
    for series_dir in series_dirs:
        print(f"   • {series_dir.name}")
    
    print(f"\n🚀 PROCESSING SERIES PAGES")
    print("-" * 30)
    
    fixed_count = 0
    total_count = 0
    
    for series_dir in series_dirs:
        index_file = series_dir / "index.html"
        
        if not index_file.exists():
            print(f"⚠️  {series_dir.name}: index.html not found")
            continue
        
        print(f"🔧 Processing {series_dir.name}...")
        total_count += 1
        
        try:
            fixed = fix_urls_in_file(index_file)
            if fixed:
                print(f"   ✅ Fixed URLs in {series_dir.name}")
                fixed_count += 1
            else:
                print(f"   ℹ️  No URL changes needed in {series_dir.name}")
        except Exception as e:
            print(f"   ❌ Error processing {series_dir.name}: {e}")
    
    print(f"\n" + "=" * 50)
    print(f"📊 SUMMARY")
    print(f"=" * 50)
    print(f"✅ Files processed: {total_count}")
    print(f"🔧 Files fixed: {fixed_count}")
    print(f"ℹ️  Files unchanged: {total_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n🎉 Successfully fixed URLs in {fixed_count} series page(s)!")
        print(f"✅ All model URLs now include the correct /specs path")
        return True
    else:
        print(f"\nℹ️  No URL fixes were needed")
        return True

if __name__ == "__main__":
    main()
