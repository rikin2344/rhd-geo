#!/usr/bin/env python3
"""
Reliable upload using curl command
"""

import os
import subprocess
import argparse
from dotenv import load_dotenv

load_dotenv()

def is_model_page(page_type):
    """Check if this is a model-specific page (vs series page)"""
    return page_type.isdigit() or page_type in ['604', '605', '606', '607', '608', '609', '623', '624', '625', '626', '627', '628', '629', '634', '635', '683', '684', '685', '686', '687', '688', '689', '693', '694', '695', '696', '697', '698', '699', '6001', '6002']

def get_model_upload_info(page_type):
    """Get model page upload information"""
    model_configs = {
        '604': {'series': 'miniature-series', 'model': '604'},
        '605': {'series': 'miniature-series', 'model': '605'},
        '606': {'series': 'miniature-series', 'model': '606'},
        '607': {'series': 'miniature-series', 'model': '607'},
        '608': {'series': 'miniature-series', 'model': '608'},
        '609': {'series': 'miniature-series', 'model': '609'},
        '623': {'series': 'miniature-series', 'model': '623'},
        '624': {'series': 'miniature-series', 'model': '624'},
        '625': {'series': 'miniature-series', 'model': '625'},
        '626': {'series': 'miniature-series', 'model': '626'},
        '627': {'series': 'miniature-series', 'model': '627'},
        '628': {'series': 'miniature-series', 'model': '628'},
        '629': {'series': 'miniature-series', 'model': '629'},
        '634': {'series': 'miniature-series', 'model': '634'},
        '635': {'series': 'miniature-series', 'model': '635'},
        '683': {'series': 'miniature-series', 'model': '683'},
        '684': {'series': 'miniature-series', 'model': '684'},
        '685': {'series': 'miniature-series', 'model': '685'},
        '686': {'series': 'miniature-series', 'model': '686'},
        '687': {'series': 'miniature-series', 'model': '687'},
        '688': {'series': 'miniature-series', 'model': '688'},
        '689': {'series': 'miniature-series', 'model': '689'},
        '693': {'series': 'miniature-series', 'model': '693'},
        '694': {'series': 'miniature-series', 'model': '694'},
        '695': {'series': 'miniature-series', 'model': '695'},
        '696': {'series': 'miniature-series', 'model': '696'},
        '697': {'series': 'miniature-series', 'model': '697'},
        '698': {'series': 'miniature-series', 'model': '698'},
        '699': {'series': 'miniature-series', 'model': '699'}
    }
    
    if page_type in model_configs:
        return model_configs[page_type]
    
    return {
        'series': 'miniature-series',
        'model': page_type
    }

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
    

    if page_type == 'miniature':
        local_file = './miniature-series/index.html'
        remote_file = 'specs/miniature-series.html'
        clean_url = 'https://rhdbearings.com/specs/miniature-series.html'
    elif page_type == '6000':
        local_file = './6000-series/index.html'
        remote_file = 'specs/6000-series.html'
        clean_url = 'https://rhdbearings.com/specs/6000-series.html'
    elif page_type == '6200':
        local_file = './6200-series/index.html'
        remote_file = 'specs/6200-series.html'
        clean_url = 'https://rhdbearings.com/specs/6200-series.html'
    elif page_type == '6300':
        local_file = './6300-series/index.html'
        remote_file = 'specs/6300-series.html'
        clean_url = 'https://rhdbearings.com/specs/6300-series.html'
    elif page_type == '62200':
        local_file = './62200-series/index.html'
        remote_file = 'specs/62200-series.html'
        clean_url = 'https://rhdbearings.com/specs/62200-series.html'
    elif page_type == '62300':
        local_file = './62300-series/index.html'
        remote_file = 'specs/62300-series.html'
        clean_url = 'https://rhdbearings.com/specs/62300-series.html'
    elif page_type == '16000':
        local_file = './16000-series/index.html'
        remote_file = 'specs/16000-series.html'
        clean_url = 'https://rhdbearings.com/specs/16000-series.html'
    elif page_type == '6800':
        local_file = './6800-series/index.html'
        remote_file = 'specs/6800-series.html'
        clean_url = 'https://rhdbearings.com/specs/6800-series.html'
    elif page_type == '6900':
        local_file = './6900-series/index.html'
        remote_file = 'specs/6900-series.html'
        clean_url = 'https://rhdbearings.com/specs/6900-series.html'
    elif page_type == 'specs':
        local_file = './specs/index.html'
        remote_file = 'specs.html'
        clean_url = 'https://rhdbearings.com/specs.html'
    elif is_model_page(page_type):
        # Handle any model page dynamically
        model_info = get_model_upload_info(page_type)
        local_file = f'./specs/{model_info["series"]}/{model_info["model"]}/index.html'
        remote_file = f'specs/{model_info["series"]}/{model_info["model"]}/index.html'
        clean_url = f'https://rhdbearings.com/specs/{model_info["series"]}/{model_info["model"]}'
    else:
        raise ValueError(f"Unknown page type: {page_type}")
    
    print(f"🚀 Uploading {page_type.upper()} series via curl...")
    
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
    parser.add_argument('--page', choices=['miniature', '6000', '6200', '6300', '62200', '62300', '16000', '6800', '6900', 'specs', '604', '605', '606', '607', '608', '609', '623', '624', '625', '626', '627', '628', '629', '634', '635', '683', '684', '685', '686', '687', '688', '689', '693', '694', '695', '696', '697', '698', '699'], 
                       help='Which page to upload (miniature, series, or model pages like 604, 607, 608, etc.). If not specified, uploads all pages.')
    args = parser.parse_args()
    
    if args.page:
        # Upload single page
        success = curl_upload(args.page)
        if not success:
            exit(1)
    else:
        # Upload all pages
        all_pages = ['miniature', '6000', '6200', '6300', '62200', '62300', '16000', '6800', '6900', 'specs', '604', '605', '606', '607', '608', '609', '623', '624', '625', '626', '627', '628', '629', '634', '635', '683', '684', '685', '686', '687', '688', '689', '693', '694', '695', '696', '697', '698', '699']
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
