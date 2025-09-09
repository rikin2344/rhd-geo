#!/usr/bin/env python3
"""
Reliable upload using curl command
"""

import os
import subprocess
import argparse
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

def is_model_page(page_type):
    """Check if this is a model-specific page (vs series page) by examining file content"""
    
    # Special cases that are always series pages
    if page_type in {'specs'}:
        return False
    
    # Get the local file path to check content
    local_file = get_local_file_path(page_type)
    
    if not local_file or not os.path.exists(local_file):
        # If file doesn't exist, fall back to pattern matching
        return fallback_model_check(page_type)
    
    try:
        with open(local_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the page contains bearingsData array (indicates series main page)
        if 'const bearingsData = [' in content or 'bearingsData = [' in content:
            return False  # This is a series main page
        
        # Check if the page contains single model data (indicates internal model page)
        if ('model": "' + page_type + '"' in content or 
            f'model": "{page_type}"' in content or
            f'data-model="{page_type}"' in content):
            return True  # This is an internal model page
        
        # If we can't determine from content, fall back to pattern matching
        return fallback_model_check(page_type)
        
    except Exception as e:
        print(f"⚠️  Warning: Could not read file {local_file}: {e}")
        return fallback_model_check(page_type)

def get_local_file_path(page_type):
    """Get the local file path for a given page type"""
    # Handle special cases first
    if page_type == 'specs':
        return './deployment/specs/index.html'
    
    # First, check if this is a series main page by checking the series directory
    if page_type in {'miniature', '6000', '6200', '6300', '6800', '62200', '62300', '16000', '6900'}:
        # Check if main series page exists first
        series_path = f'./deployment/{page_type}-series/index.html'
        if os.path.exists(series_path):
            return series_path
    
    # If not a series page or series page doesn't exist, try to determine if this is a model page
    if page_type.isdigit():
        if len(page_type) == 3:
            # Miniature series - only use deployment directory
            deployment_path = f'./deployment/miniature-series-internal-pages/{page_type}/index.html'
            return deployment_path
                
        elif len(page_type) == 4:
            if page_type.startswith('60'):
                deployment_path = f'./deployment/6000-series/6000-series-internal-pages-deployment/{page_type}/index.html'
            elif page_type.startswith('62'):
                deployment_path = f'./deployment/6200-series/6200-series-internal-pages-deployment/{page_type}/index.html'
            elif page_type.startswith('63'):
                deployment_path = f'./deployment/6300-series/6300-series-internal-pages-deployment/{page_type}/index.html'
            elif page_type.startswith('68'):
                deployment_path = f'./deployment/6800-series/6800-series-internal-pages-deployment/{page_type}/index.html'
            elif page_type.startswith('69'):
                deployment_path = f'./deployment/6900-series/6900-series-internal-pages-deployment/{page_type}/index.html'
            else:
                return None
                
            return deployment_path
                
        elif len(page_type) == 5:
            if page_type.startswith('622'):
                deployment_path = f'./deployment/62200-series/62200-series-internal-pages-deployment/{page_type}/index.html'
            elif page_type.startswith('623'):
                deployment_path = f'./deployment/62300-series/62300-series-internal-pages-deployment/{page_type}/index.html'
            elif page_type.startswith('160'):
                deployment_path = f'./deployment/16000-series/16000-series-internal-pages-deployment/{page_type}/index.html'
            else:
                return None
                
            return deployment_path
    else:
        # Handle special model names with spaces or special characters
        # These are typically in the 6200 series
        if ' ' in page_type or 'A' in page_type:
            # Special models like "6203 12.7" or "6203A42"
            deployment_path = f'./deployment/6200-series/6200-series-internal-pages-deployment/{page_type}/index.html'
            return deployment_path
    
    
    return None

def fallback_model_check(page_type):
    """Fallback logic for determining if a page is a model page"""
    if page_type.isdigit():
        # 3-digit numbers are typically models
        if len(page_type) == 3:
            return True
        # 4-digit numbers ending in 00 are series, others are models
        if len(page_type) == 4:
            return not page_type.endswith('00')
        # 5-digit numbers ending in 00 are series, others are models
        if len(page_type) == 5:
            return not page_type.endswith('00')
    else:
        # Handle special model names with spaces or special characters
        if ' ' in page_type or 'A' in page_type:
            return True  # These are model pages
    
    # Default to not being a model page
    return False

def get_upload_paths(page_type):
    """Get local file, remote file, and clean URL paths for any page type"""
    
    # Get the local file path
    local_file = get_local_file_path(page_type)
    
    if not local_file:
        return None, None, None
    
    # Determine if this is a series main page or model page
    is_model = is_model_page(page_type)
    
    if is_model:
        # This is an internal model page
        series_name = get_series_name_from_model(page_type)
        model_name = page_type.replace(' ', '-')  # Clean model name
        
        remote_file = f'specs/{series_name}/{model_name}/index.html'
        clean_url = f'https://rhdbearings.com/specs/{series_name}/{model_name}/'
        
    else:
        # This is a series main page
        if page_type == 'specs':
            remote_file = 'specs.html'
            clean_url = 'https://rhdbearings.com/specs.html'
        else:
            # For series pages, just add '-series' suffix
            series_name = f'{page_type}-series'
            remote_file = f'specs/{series_name}.html'
            clean_url = f'https://rhdbearings.com/specs/{series_name}.html'
    
    return local_file, remote_file, clean_url

def discover_all_pages():
    """Discover all available pages by scanning the deployment directory"""
    import glob
    
    all_pages = []
    
    # Add series pages
    series_dirs = glob.glob('./deployment/*-series')
    for series_dir in series_dirs:
        series_name = series_dir.split('/')[-1].replace('-series', '')
        if series_name not in all_pages:
            all_pages.append(series_name)
    
    # Add specs page
    if os.path.exists('./deployment/specs'):
        all_pages.append('specs')
    
    # Add model pages by scanning internal pages directories
    internal_dirs = glob.glob('./deployment/*-series/*-internal-pages-deployment')
    for internal_dir in internal_dirs:
        model_dirs = glob.glob(f'{internal_dir}/*')
        for model_dir in model_dirs:
            model_name = model_dir.split('/')[-1]
            if model_name not in all_pages:
                all_pages.append(model_name)
    
    # Add miniature series models
    miniature_dir = './deployment/miniature-series-internal-pages'
    if os.path.exists(miniature_dir):
        miniature_models = glob.glob(f'{miniature_dir}/*')
        for model_dir in miniature_models:
            model_name = model_dir.split('/')[-1]
            if model_name not in all_pages:
                all_pages.append(model_name)
    
    return sorted(all_pages)

def get_series_name_from_model(page_type):
    """Dynamically determine series name from model number using pattern matching"""
    
    # Hardcoded mapping for special models to ensure correct series assignment
    special_models = {
        "6201 12.7": "6200-series",
        "6202 12.7": "6200-series", 
        "6203 12.7": "6200-series",
        "6203A42": "6200-series"
    }
    
    # Check if this is a special model first
    if page_type in special_models:
        return special_models[page_type]
    
    if not page_type.isdigit():
        return 'miniature-series'
    
    # Extract series prefix and convert to series name
    if len(page_type) == 3:
        return 'miniature-series'
    elif len(page_type) == 4:
        prefix = page_type[:2]  # Get first 2 digits
        return f'{prefix}00-series'
    elif len(page_type) == 5:
        if page_type.startswith('160'):
            return '16000-series'
        else:
            prefix = page_type[:3]  # Get first 3 digits
            return f'{prefix}00-series'  # Fixed: should be 62300-series, not 6230-series
    
    return 'miniature-series'

def curl_upload(page_type='miniature'):
    """Upload using curl - much more reliable than Python FTP"""
    
    username = os.getenv('FTP_USERNAME', 'rikin@rhdbearings.com')
    password = os.getenv('FTP_PASSWORD')
    host = os.getenv('FTP_HOST', 'ftp.rhdbearings.com')
    
    # Check if password is available
    if not password:
        print("❌ FTP_PASSWORD environment variable not found!")
        print("💡 Make sure you have a .env file with FTP_PASSWORD=your_password")
        return False
    
    # Get file paths dynamically based on content detection
    local_file, remote_file, clean_url = get_upload_paths(page_type)
    
    if not local_file:
        print(f"❌ Could not determine file paths for {page_type}")
        return False
    
    # Check if the local file exists
    if not os.path.exists(local_file):
        print(f"⚠️  Warning: Local file {local_file} not found!")
        print(f"💡 Make sure to run generate_universal_bearing_pages.py first to create the standalone pages in deployment directory")
        return False
    
    print(f"🚀 Uploading {page_type.upper()} via curl...")
    
    try:
        # Build curl command with directory creation
        cmd = [
            'curl',
            '--ftp-create-dirs',
            '-T', local_file,
            '-u', f"{username}:{password}",
            f"ftp://{host}/public_html/{remote_file}"
        ]
        
        print(f"📤 Uploading {local_file} to {remote_file}...")
        
        # Execute curl
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Upload successful!")
            print(f"🔗 Your page: {clean_url}")
            print("✅ Ready to view immediately!")
            return True
        else:
            print(f"❌ Upload failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Upload bearing page via curl')
    parser.add_argument('--page', 
                       help='Which page to upload (any series or model page). Examples: 62300, 62301, 6200, 6201, miniature, specs, etc. If not specified, uploads all pages.')
    args = parser.parse_args()
    
    if args.page:
        # Upload single page
        success = curl_upload(args.page)
        if not success:
            exit(1)
    else:
        # Upload all pages - discover them dynamically
        all_pages = discover_all_pages()
        print("🚀 No specific page specified. Uploading ALL pages...")
        print("=" * 60)
        
        failed_uploads = []
        successful_uploads = []
        
        for page in all_pages:
            print(f"\n📦 Processing {page.upper()}...")
            success = curl_upload(page)
            if success:
                successful_uploads.append(page)
            else:
                failed_uploads.append(page)
        
        print("\n" + "=" * 60)
        print("📊 UPLOAD SUMMARY")
        print("=" * 60)
        
        if successful_uploads:
            print(f"✅ Successful uploads ({len(successful_uploads)}):")
            for page in successful_uploads:
                print(f"   • {page.upper()}")
        
        if failed_uploads:
            print(f"\n❌ Failed uploads ({len(failed_uploads)}):")
            for page in failed_uploads:
                print(f"   • {page.upper()}")
            print(f"\n⚠️  {len(failed_uploads)} page(s) failed to upload!")
            exit(1)
        else:
            print(f"\n🎉 All {len(successful_uploads)} pages uploaded successfully!")
            print("✅ Your website is fully updated!")

if __name__ == "__main__":
    main()
