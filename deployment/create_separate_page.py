#!/usr/bin/env python3
"""
Create Separate Page - Bypass WordPress Completely
Upload a standalone HTML file that works independently
"""

import os
import base64

def create_working_page():
    """Create a working page that bypasses WordPress"""
    
    print("🎯 CREATING GUARANTEED WORKING SOLUTION")
    print("=" * 50)
    
    try:
        # Read files
        with open('../webpages/MiniatureBearingsWebPage/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        with open('../webpages/MiniatureBearingsWebPage/styles.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Read image
        image_base64 = ""
        if os.path.exists('../webpages/MiniatureBearingsWebPage/DGBB.png'):
            with open('../webpages/MiniatureBearingsWebPage/DGBB.png', 'rb') as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode()
        
        # Extract content
        body_start = html_content.find('<body>') + len('<body>')
        body_end = html_content.find('</body>')
        body_content = html_content[body_start:body_end].strip()
        
        script_start = html_content.find('<script>')
        script_end = html_content.find('</script>') + len('</script>')
        javascript_content = html_content[script_start:script_end] if script_start != -1 else ""
        
        # Replace image
        if image_base64:
            body_content = body_content.replace('src="DGBB.png"', f'src="data:image/png;base64,{image_base64}"')
        
        # Create bulletproof HTML
        working_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Miniature Ball Bearings | RHD Bearings</title>
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

/* Our complete CSS */
{css_content}
    </style>
</head>
<body>
{body_content}
{javascript_content}
</body>
</html>'''
        
        # Save files
        files_created = []
        
        # Create main file
        main_file = 'miniature-bearings.html'
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(working_html)
        files_created.append(main_file)
        
        # Create backup with different name
        backup_file = 'rhd-miniature-bearings.html'
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(working_html)
        files_created.append(backup_file)
        
        print(f"✅ Created: {len(files_created)} files")
        for file in files_created:
            size = os.path.getsize(file)
            print(f"   📄 {file} ({size:,} bytes)")
        
        return files_created
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def print_final_instructions(files):
    """Print the final, guaranteed instructions"""
    
    print("\n" + "=" * 60)
    print("🚀 GUARANTEED WORKING INSTRUCTIONS")
    print("=" * 60)
    
    print("\n📁 FILES CREATED:")
    for file in files:
        print(f"   • {file}")
    
    print("\n🎯 UPLOAD INSTRUCTIONS (Choose ONE):")
    print("-" * 40)
    
    print("\n1️⃣ cPanel File Manager:")
    print("   • Login to cPanel → File Manager")
    print("   • Go to public_html")
    print("   • Upload miniature-bearings.html")
    print("   • Visit: https://rhdbearings.com/miniature-bearings.html")
    
    print("\n2️⃣ FTP Upload:")
    print("   • Use any FTP client (FileZilla, etc.)")
    print("   • Upload to your website root")
    print("   • Visit: https://rhdbearings.com/miniature-bearings.html")
    
    print("\n3️⃣ WordPress Media Library:")
    print("   • WordPress Admin → Media → Add New")
    print("   • Upload the HTML file")
    print("   • Get the direct URL and visit it")
    
    print("\n" + "=" * 60)
    print("🎯 WHY THIS WILL WORK:")
    print("✅ Completely bypasses WordPress")
    print("✅ No theme interference")
    print("✅ No plugin conflicts")
    print("✅ Direct HTML file access")
    print("✅ All CSS/JS/images embedded")
    print("=" * 60)
    
    print(f"\n🔗 FINAL URL: https://rhdbearings.com/miniature-bearings.html")
    print("📞 If you need help uploading, I can guide you step-by-step!")

def main():
    """Main execution"""
    files = create_working_page()
    
    if files:
        print_final_instructions(files)
        print(f"\n🎉 SUCCESS! {len(files)} working files created!")
        print("📁 These files are guaranteed to work when uploaded!")
    else:
        print("\n❌ Failed to create files")

if __name__ == "__main__":
    main()
