#!/usr/bin/env python3
"""
Reliable upload using curl command
"""

import os
import subprocess
import argparse
from dotenv import load_dotenv

load_dotenv()

def curl_upload(page_type='miniature'):
    """Upload using curl - much more reliable than Python FTP"""
    
    username = os.getenv('FTP_USERNAME', 'rikin@rhdbearings.com')
    password = os.getenv('FTP_PASSWORD')
    host = os.getenv('FTP_HOST', 'ftp.rhdbearings.com')
    
    if page_type == 'miniature':
        local_file = './miniature-series/index.html'
        remote_file = 'miniature-series.html'
        clean_url = 'https://rhdbearings.com/miniature-series.html'
    elif page_type == '6000':
        local_file = './6000-series/index.html'
        remote_file = '6000-series.html'
        clean_url = 'https://rhdbearings.com/6000-series.html'
    
    print(f"🚀 Uploading {page_type.upper()} series via curl...")
    
    try:
        # Build curl command
        cmd = [
            'curl',
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
    parser.add_argument('--page', choices=['miniature', '6000'], default='miniature',
                       help='Which page to upload (miniature or 6000)')
    args = parser.parse_args()
    
    success = curl_upload(args.page)
    if not success:
        exit(1)

if __name__ == "__main__":
    main()
