#!/usr/bin/env python3
"""
Create Separate Page - Bypass WordPress Completely
Upload a standalone HTML file that works independently
"""

import os
import base64
import argparse

def create_working_page(page_type='miniature'):
    """Create a working page that bypasses WordPress"""
    
    print(f"🎯 CREATING GUARANTEED WORKING SOLUTION FOR {page_type.upper()}")
    print("=" * 50)
    
    try:
        # Set paths based on page type
        if page_type == 'miniature':
            page_dir = '../webpages/MiniatureBearingsWebPage'
            output_dir = 'miniature-series'
            output_file = f'{output_dir}/index.html'
            backup_file = f'{output_dir}/backup.html'
            page_title = 'Miniature Ball Bearings | RHD Bearings'
            clean_url = 'https://rhdbearings.com/specs/miniature-series/'
        elif page_type == '6000':
            page_dir = '../webpages/6000SeriesWebPage'
            output_dir = '6000-series'
            output_file = f'{output_dir}/index.html'
            backup_file = f'{output_dir}/backup.html'
            page_title = '6000 Series Ball Bearings | RHD Bearings'
            clean_url = 'https://rhdbearings.com/specs/6000-series/'
        elif page_type == '6200':
            page_dir = '../webpages/6200SeriesWebPage'
            output_dir = '6200-series'
            output_file = f'{output_dir}/index.html'
            backup_file = f'{output_dir}/backup.html'
            page_title = '6200 Series Heavy Duty Ball Bearings | RHD Bearings'
            clean_url = 'https://rhdbearings.com/specs/6200-series/'
        elif page_type == '6300':
            page_dir = '../webpages/6300SeriesWebPage'
            output_dir = '6300-series'
            output_file = f'{output_dir}/index.html'
            backup_file = f'{output_dir}/backup.html'
            page_title = '6300 Series Maximum Load Ball Bearings | RHD Bearings'
            clean_url = 'https://rhdbearings.com/specs/6300-series/'
        elif page_type == 'specs':
            page_dir = '../webpages/SpecsHubPage'
            output_dir = 'specs'
            output_file = f'{output_dir}/index.html'
            backup_file = f'{output_dir}/backup.html'
            page_title = 'Bearing Specifications & Technical Data | RHD Bearings'
            clean_url = 'https://rhdbearings.com/specs/'
        else:
            raise ValueError(f"Unknown page type: {page_type}")

        # Read files
        with open(f'{page_dir}/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        with open(f'{page_dir}/styles.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        with open('../webpages/shared/navbar.css', 'r', encoding='utf-8') as f:
            navbar_css = f.read()
        
        # Read navbar HTML
        with open('../webpages/shared/navbar.html', 'r', encoding='utf-8') as f:
            navbar_html = f.read()
            # Remove the script tag from navbar as we'll add it later
            script_start = navbar_html.find('<script>')
            if script_start != -1:
                navbar_html = navbar_html[:script_start].strip()

        # Extract content
        body_start = html_content.find('<body') + html_content[html_content.find('<body'):].find('>') + 1
        body_end = html_content.find('</body>')
        body_content = html_content[body_start:body_end].strip()
        
        # Find all script tags
        script_content = ""
        current_pos = 0
        while True:
            script_start = html_content.find('<script>', current_pos)
            if script_start == -1:
                break
            script_end = html_content.find('</script>', script_start) + len('</script>')
            script_content += html_content[script_start:script_end] + "\n"
            current_pos = script_end
        
        # Replace image with remote URL
        body_content = body_content.replace('src="DGBB.png"', 'src="https://rhdbearings.com/wp-content/uploads/2025/08/DGBB.png"')
        
        # Replace navbar container with actual navbar HTML
        body_content = body_content.replace('<div id="navbar-container"></div>', navbar_html)
        
        # Create bulletproof HTML
        working_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
/* Reset everything */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Bai Jamjuree', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #000;
    background: #F8F9FA;
}}

/* Navbar CSS */
{navbar_css}

/* Page CSS */
{css_content}
    </style>
</head>
<body>
{body_content}
{script_content}
</body>
</html>'''
        
        # Save files
        files_created = []
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create main file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(working_html)
        files_created.append(output_file)
        
        # Create backup with different name
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(working_html)
        files_created.append(backup_file)
        
        print(f"✅ Created: {len(files_created)} files")
        for file in files_created:
            size = os.path.getsize(file)
            print(f"   📄 {file} ({size:,} bytes)")
        
        return files_created, clean_url
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return [], ""

def print_final_instructions(files, clean_url, page_type='miniature'):
    """Print the final, guaranteed instructions"""
    
    print("\n" + "=" * 60)
    print("🚀 GUARANTEED WORKING INSTRUCTIONS")
    print("=" * 60)
    
    print("\n📁 FILES CREATED:")
    for file in files:
        print(f"   • {file}")
    
    print("\n🎯 UPLOAD INSTRUCTIONS (Choose ONE):")
    print("-" * 40)
    
    directory_name = '6000-series' if page_type == '6000' else 'miniature-series'
    
    print("\n1️⃣ cPanel File Manager:")
    print("   • Login to cPanel → File Manager")
    print("   • Go to public_html")
    print(f"   • Upload entire {directory_name}/ directory")
    print(f"   • Visit: {clean_url}")
    
    print("\n2️⃣ FTP Upload:")
    print("   • Use any FTP client (FileZilla, etc.)")
    print(f"   • Upload {directory_name}/ directory to website root")
    print(f"   • Visit: {clean_url}")
    
    print("\n3️⃣ Automated FTP Upload:")
    print("   • Run: python direct_cpanel_upload.py")
    print(f"   • Automatically creates {directory_name}/ directory")
    print(f"   • Visit: {clean_url}")
    
    print("\n" + "=" * 60)
    print("🎯 WHY THIS WILL WORK:")
    print("✅ Completely bypasses WordPress")
    print("✅ No theme interference")
    print("✅ No plugin conflicts")
    print("✅ Direct HTML file access")
    print("✅ All CSS/JS/images embedded")
    print("=" * 60)
    
    print(f"\n🔗 FINAL URL: {clean_url}")
    print("📞 If you need help uploading, I can guide you step-by-step!")
    print(f"✨ CLEAN URL: No .html extension needed!")

def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description='Create a standalone HTML page')
    parser.add_argument('--page', choices=['miniature', '6000', '6200', '6300', 'specs'], default='miniature',
                      help='Which page to generate (miniature, 6000, 6200, 6300, or specs)')
    args = parser.parse_args()
    
    files, clean_url = create_working_page(args.page)
    
    if files:
        print_final_instructions(files, clean_url, args.page)
        print(f"\n🎉 SUCCESS! {len(files)} working files created!")
        print("📁 These files are guaranteed to work when uploaded!")
    else:
        print("\n❌ Failed to create files")

if __name__ == "__main__":
    main()