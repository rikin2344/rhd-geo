#!/usr/bin/env python3
"""
Upload shared assets (CSS, HTML, JS) to server for RHD Bearings
This script uploads the shared footer.css, footer.html, navbar.css, etc. to the server
"""

import subprocess
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def upload_shared_assets():
    """Upload all shared assets using curl"""
    
    username = os.getenv('FTP_USERNAME', 'rikin@rhdbearings.com')
    password = os.getenv('FTP_PASSWORD')
    host = os.getenv('FTP_HOST', 'ftp.rhdbearings.com')
    
    if not password:
        print("❌ FTP_PASSWORD environment variable not found!")
        print("💡 Make sure you have a .env file with FTP_PASSWORD=your_password")
        return False
    
    # Define shared assets to upload (from deployment/shared directory)
    shared_assets = [
        ('shared/footer.css', 'shared/footer.css'),
        ('shared/footer.html', 'shared/footer.html'),
        ('shared/navbar.css', 'shared/navbar.css'),
        ('shared/navbar.html', 'shared/navbar.html'),
        ('shared/cta-model.css', 'shared/cta-model.css'),
        ('shared/cta-model.html', 'shared/cta-model.html'),
        ('shared/cta-model.js', 'shared/cta-model.js'),
        ('shared/watermark.css', 'shared/watermark.css'),
        ('shared/watermark.html', 'shared/watermark.html'),
    ]
    
    print("🚀 UPLOADING SHARED ASSETS TO SERVER")
    print("=" * 50)
    
    successful_uploads = []
    failed_uploads = []
    
    for local_file, remote_file in shared_assets:
        local_path = Path(local_file)
        
        if not local_path.exists():
            print(f"⚠️  Skipping {local_file} - file not found")
            continue
            
        print(f"📤 Uploading {local_file}...")
        
        try:
            cmd = [
                'curl',
                '--ftp-create-dirs',
                '-T', str(local_path),
                '-u', f"{username}:{password}",
                f"ftp://{host}/public_html/{remote_file}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Successfully uploaded {local_file}")
                successful_uploads.append(local_file)
            else:
                print(f"❌ Failed to upload {local_file}: {result.stderr}")
                failed_uploads.append(local_file)
                
        except Exception as e:
            print(f"❌ Error uploading {local_file}: {e}")
            failed_uploads.append(local_file)
    
    print("=" * 50)
    print("📊 UPLOAD SUMMARY")
    print("=" * 50)
    print(f"✅ Successfully uploaded: {len(successful_uploads)}")
    print(f"❌ Failed: {len(failed_uploads)}")
    
    if successful_uploads:
        print("\n✅ Successful uploads:")
        for file in successful_uploads:
            print(f"   • {file}")
    
    if failed_uploads:
        print("\n❌ Failed uploads:")
        for file in failed_uploads:
            print(f"   • {file}")
    
    return len(failed_uploads) == 0

def main():
    """Main function"""
    print("🌐 RHD Bearings - Shared Assets Upload")
    print("=" * 50)
    
    success = upload_shared_assets()
    
    if success:
        print("\n🎉 All shared assets uploaded successfully!")
        print("🔗 Your pages should now have working dynamic footers and navbars!")
    else:
        print("\n⚠️  Some uploads failed. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
