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
    """Check if this is a model-specific page (vs series page)"""
    # Check if it's a 3-digit model number (604, 605, etc.)
    if page_type.isdigit() and len(page_type) == 3:
        return True
    # Check if it's a 4-digit model number (6001, 6002, 6201, 6202, etc.)
    # BUT NOT 6200, 6300, 6800, 6900 which are series names
    if page_type.isdigit() and len(page_type) == 4:
        # Exclude series names that end with "00"
        if page_type.endswith('00'):
            return False
        return True
    # Check if it's a 5-digit model number (16000, 62200, 62300, etc.)
    if page_type.isdigit() and len(page_type) == 5:
        return True
    # Check specific model numbers
    return page_type in ['604', '605', '606', '607', '608', '609', '623', '624', '625', '626', '627', '628', '629', '634', '635', '683', '684', '685', '686', '687', '688', '689', '693', '694', '695', '696', '697', '698', '699', '6001', '6002', '6201 12.7', '6202 12.7', '6203 12.7', '6203A42']

def get_model_upload_info(page_type):
    """Get model page upload information"""
    model_configs = {
        # Miniature series (3-digit models)
        '604': {'series': 'miniature-series-internal-pages', 'model': '604'},
        '605': {'series': 'miniature-series-internal-pages', 'model': '605'},
        '606': {'series': 'miniature-series-internal-pages', 'model': '606'},
        '607': {'series': 'miniature-series-internal-pages', 'model': '607'},
        '608': {'series': 'miniature-series-internal-pages', 'model': '608'},
        '609': {'series': 'miniature-series-internal-pages', 'model': '609'},
        '623': {'series': 'miniature-series-internal-pages', 'model': '623'},
        '624': {'series': 'miniature-series-internal-pages', 'model': '624'},
        '625': {'series': 'miniature-series-internal-pages', 'model': '625'},
        '626': {'series': 'miniature-series-internal-pages', 'model': '626'},
        '627': {'series': 'miniature-series-internal-pages', 'model': '627'},
        '628': {'series': 'miniature-series-internal-pages', 'model': '628'},
        '629': {'series': 'miniature-series-internal-pages', 'model': '629'},
        '634': {'series': 'miniature-series-internal-pages', 'model': '634'},
        '635': {'series': 'miniature-series-internal-pages', 'model': '635'},
        '683': {'series': 'miniature-series-internal-pages', 'model': '683'},
        '684': {'series': 'miniature-series-internal-pages', 'model': '684'},
        '685': {'series': 'miniature-series-internal-pages', 'model': '685'},
        '686': {'series': 'miniature-series-internal-pages', 'model': '686'},
        '687': {'series': 'miniature-series-internal-pages', 'model': '687'},
        '688': {'series': 'miniature-series-internal-pages', 'model': '688'},
        '689': {'series': 'miniature-series-internal-pages', 'model': '689'},
        '693': {'series': 'miniature-series-internal-pages', 'model': '693'},
        '694': {'series': 'miniature-series-internal-pages', 'model': '694'},
        '695': {'series': 'miniature-series-internal-pages', 'model': '695'},
        '696': {'series': 'miniature-series-internal-pages', 'model': '696'},
        '697': {'series': 'miniature-series-internal-pages', 'model': '697'},
        '698': {'series': 'miniature-series-internal-pages', 'model': '698'},
        '699': {'series': 'miniature-series-internal-pages', 'model': '699'},
        
        # 6200 series (4-digit models starting with 62)
        '6200': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6200'},
        '6201': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6201'},
        '6202': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6202'},
        '6203': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6203'},
        '6204': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6204'},
        '6205': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6205'},
        '6206': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6206'},
        '6207': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6207'},
        '6208': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6208'},
        '6209': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6209'},
        '6210': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6210'},
        '6211': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6211'},
        '6212': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6212'},
        '6213': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6213'},
        '6214': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6214'},
        '6215': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6215'},
        '6216': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6216'},
        '6217': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6217'},
        '6218': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6218'},
        '6219': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6219'},
        '6220': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6220'},
        
        # Special 12.7mm bore variants and special models
        '6201 12.7': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6201 12.7'},
        '6202 12.7': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6202 12.7'},
        '6203 12.7': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6203 12.7'},
        '6203A42': {'series': '6200-series/6200-series-internal-pages-deployment', 'model': '6203A42'}
    }
    
    if page_type in model_configs:
        return model_configs[page_type]
    
    # Default fallback - try to determine series from model number
    if page_type.isdigit():
        if len(page_type) == 3 and page_type.startswith('6'):
            return {'series': 'miniature-series-internal-pages', 'model': page_type}
        elif len(page_type) == 4 and page_type.startswith('62'):
            return {'series': '6200-series/6200-series-internal-pages-deployment', 'model': page_type}
        elif len(page_type) == 4 and page_type.startswith('60'):
            return {'series': '6000-series/6000-series-internal-pages-deployment', 'model': page_type}
        elif len(page_type) == 4 and page_type.startswith('63'):
            return {'series': '6300-series/6300-series-internal-pages-deployment', 'model': page_type}
        elif len(page_type) == 4 and page_type.startswith('68'):
            return {'series': '6800-series/6800-series-internal-pages-deployment', 'model': page_type}
        elif len(page_type) == 4 and page_type.startswith('69'):
            return {'series': '6900-series/6900-series-internal-pages-deployment', 'model': page_type}
        elif len(page_type) == 5 and page_type.startswith('16'):
            return {'series': '16000-series/16000-series-internal-pages-deployment', 'model': page_type}
        elif len(page_type) == 5 and page_type.startswith('622'):
            return {'series': '62200-series/62200-series-internal-pages-deployment', 'model': page_type}
        elif len(page_type) == 5 and page_type.startswith('623'):
            return {'series': '62300-series/62300-series-internal-pages-deployment', 'model': page_type}
    
    return {
        'series': 'miniature-series-internal-pages',
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
    

    if is_model_page(page_type):
        # Handle any model page dynamically
        model_info = get_model_upload_info(page_type)
        local_file = f'./{model_info["series"]}/{model_info["model"]}/index.html'
        
        # Determine the correct remote path and URL based on series
        if '6200-series' in model_info["series"]:
            # Replace spaces with hyphens for cleaner URLs
            clean_model = model_info["model"].replace(' ', '-')
            remote_file = f'specs/6200-series/{clean_model}/index.html'
            clean_url = f'https://rhdbearings.com/specs/6200-series/{clean_model}'
        elif '6000-series' in model_info["series"]:
            remote_file = f'specs/6000-series/{model_info["model"]}/index.html'
            clean_url = f'https://rhdbearings.com/specs/6000-series/{model_info["model"]}'
        elif '6300-series' in model_info["series"]:
            remote_file = f'specs/6300-series/{model_info["model"]}/index.html'
            clean_url = f'https://rhdbearings.com/specs/6300-series/{model_info["model"]}'
        elif '6800-series' in model_info["series"]:
            remote_file = f'specs/6800-series/{model_info["model"]}/index.html'
            clean_url = f'https://rhdbearings.com/specs/6800-series/{model_info["model"]}'
        elif '6900-series' in model_info["series"]:
            remote_file = f'specs/6900-series/{model_info["model"]}/index.html'
            clean_url = f'https://rhdbearings.com/specs/6900-series/{model_info["model"]}'
        elif '16000-series' in model_info["series"]:
            remote_file = f'specs/16000-series/{model_info["model"]}/index.html'
            clean_url = f'https://rhdbearings.com/specs/16000-series/{model_info["model"]}'
        elif '62200-series' in model_info["series"]:
            remote_file = f'specs/62200-series/{model_info["model"]}/index.html'
            clean_url = f'https://rhdbearings.com/specs/62200-series/{model_info["model"]}'
        elif '62300-series' in model_info["series"]:
            remote_file = f'specs/62300-series/{model_info["model"]}/index.html'
            clean_url = f'https://rhdbearings.com/specs/62300-series/{model_info["model"]}'
        else:
            # Default to miniature series
            remote_file = f'specs/miniature-series/{model_info["model"]}/index.html'
            clean_url = f'https://rhdbearings.com/specs/miniature-series/{model_info["model"]}'
        
        # Check if the local file exists
        if not os.path.exists(local_file):
            print(f"⚠️  Warning: Local file {local_file} not found!")
            print(f"💡 Make sure to run generate_all_models.py first to create the model pages")
            return False
    elif page_type == 'miniature':
        local_file = './miniature-series/index.html'
        remote_file = 'specs/miniature-series.html'
        clean_url = 'https://rhdbearings.com/specs/miniature-series.html'
    elif page_type == '6000':
        local_file = './6000-series/index.html'
        remote_file = 'specs/6000-series.html'
        clean_url = 'https://rhdbearings.com/specs/6000-series.html'
    elif page_type == '6200':
        # Check if this is a request for the 6200 model page (not the series page)
        # If someone wants the model page, they should use '6200-model' instead
        local_file = './6200-series/index.html'
        remote_file = 'specs/6200-series.html'
        clean_url = 'https://rhdbearings.com/specs/6200-series.html'
    elif page_type == '6200-model':
        # Special case for the 6200 model page
        local_file = './deployment/6200-series/6200-series-internal-pages-deployment/6200/index.html'
        remote_file = 'specs/6200-series/6200/index.html'
        clean_url = 'https://rhdbearings.com/specs/6200-series/6200/'
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
    elif page_type == '6300':
        local_file = './6300-series/index.html'
        remote_file = 'specs/6300-series.html'
        clean_url = 'https://rhdbearings.com/specs/6300-series.html'
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
    parser.add_argument('--page', choices=['miniature', '6000', '6200', '6300', '62200', '62300', '16000', '6800', '6900', 'specs', '604', '605', '606', '607', '608', '609', '623', '624', '625', '626', '627', '628', '629', '634', '635', '683', '684', '685', '686', '687', '688', '689', '693', '694', '695', '696', '697', '698', '699', '6200', '6201', '6202', '6203', '6204', '6205', '6206', '6207', '6208', '6209', '6210', '6211', '6212', '6213', '6214', '6215', '6216', '6217', '6218', '6219', '6220', '62200', '62201', '62202', '62203', '62204', '62205', '62206', '62207', '62208', '62209', '62210', '62211', '62212', '62213', '62214', '62215', '62216', '62217', '62218', '62219', '62220'], 
                       help='Which page to upload (miniature, series, or model pages like 604, 607, 608, 6200, 6201, 62200, 62201, etc.). If not specified, uploads all pages.')
    args = parser.parse_args()
    
    if args.page:
        # Upload single page
        success = curl_upload(args.page)
        if not success:
            exit(1)
    else:
        # Upload all pages
        all_pages = ['miniature', '6000', '6200', '6300', '62200', '62300', '16000', '6800', '6900', 'specs', '604', '605', '606', '607', '608', '609', '623', '624', '625', '626', '627', '628', '629', '634', '635', '683', '684', '685', '686', '687', '688', '689', '693', '694', '695', '696', '697', '698', '699', '62200', '62201', '62202', '62203', '62204', '62205', '62206', '62207', '62208', '62209', '62210', '62211', '62212', '62213', '62214', '62215', '62216', '62217', '62218', '62219', '62220']
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
