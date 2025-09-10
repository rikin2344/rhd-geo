#!/usr/bin/env python3
"""
Upload shared assets (navbar, footer, CTA, etc.) to the server using curl
"""

import os
import subprocess
import glob
from dotenv import load_dotenv

load_dotenv()

def curl_upload_file(local_file, remote_file):
    """Upload a single file using curl"""
    
    username = os.getenv('FTP_USERNAME', 'rhdbearings')
    password = os.getenv('FTP_PASSWORD')
    host = os.getenv('FTP_HOST', 'ftp.rhdbearings.com')
    
    # Check if password is available
    if not password:
        print("❌ FTP_PASSWORD environment variable not found!")
        print("💡 Make sure you have a .env file with FTP_PASSWORD=your_password")
        return False
    
    # Check if the local file exists
    if not os.path.exists(local_file):
        print(f"⚠️  Warning: Local file {local_file} not found!")
        return False
    
    try:
        # Build curl command with directory creation
        cmd = [
            'curl',
            '--ftp-create-dirs',
            '-T', local_file,
            '-u', f"{username}:{password}",
            f"ftp://{host}/public_html/{remote_file}"
        ]
        
        print(f"📤 Uploading {os.path.basename(local_file)}...")
        
        # Execute curl
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Success: {remote_file}")
            return True
        else:
            print(f"   ❌ Failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def upload_shared_assets():
    """Upload all shared assets from deployment/shared/ to server"""
    
    shared_dir = './deployment/shared'
    
    if not os.path.exists(shared_dir):
        print(f"❌ Shared assets directory not found: {shared_dir}")
        print("💡 Make sure you've copied files from webpages/shared/ to deployment/shared/")
        return False
    
    print("🚀 Uploading shared assets...")
    print("=" * 50)
    
    # Get all files in the shared directory
    shared_files = glob.glob(f'{shared_dir}/*')
    shared_files = [f for f in shared_files if os.path.isfile(f)]  # Only files, not directories
    
    if not shared_files:
        print("⚠️  No shared assets found to upload!")
        return False
    
    successful_uploads = []
    failed_uploads = []
    
    # Upload each shared asset
    for local_file in shared_files:
        filename = os.path.basename(local_file)
        remote_file = f'shared/{filename}'  # Upload to /shared/ directory on server
        
        success = curl_upload_file(local_file, remote_file)
        
        if success:
            successful_uploads.append(filename)
        else:
            failed_uploads.append(filename)
    
    print("\n" + "=" * 50)
    print("📊 UPLOAD SUMMARY")
    print("=" * 50)
    
    if successful_uploads:
        print(f"✅ Successfully uploaded ({len(successful_uploads)}):")
        for filename in successful_uploads:
            print(f"   • {filename}")
    
    if failed_uploads:
        print(f"\n❌ Failed uploads ({len(failed_uploads)}):")
        for filename in failed_uploads:
            print(f"   • {filename}")
        print(f"\n⚠️  {len(failed_uploads)} file(s) failed to upload!")
        return False
    else:
        print(f"\n🎉 All {len(successful_uploads)} shared assets uploaded successfully!")
        print("🔗 Shared assets are now available at: https://rhdbearings.com/shared/")
        print("✅ Pages using dynamic loading will now have updated components!")
        return True

def upload_specific_asset(asset_name):
    """Upload a specific shared asset by name"""
    
    shared_dir = './deployment/shared'
    local_file = os.path.join(shared_dir, asset_name)
    
    if not os.path.exists(local_file):
        print(f"❌ Asset not found: {local_file}")
        return False
    
    remote_file = f'shared/{asset_name}'
    print(f"🚀 Uploading specific asset: {asset_name}")
    print("=" * 50)
    
    success = curl_upload_file(local_file, remote_file)
    
    if success:
        print(f"\n🎉 {asset_name} uploaded successfully!")
        print(f"🔗 Available at: https://rhdbearings.com/shared/{asset_name}")
    
    return success

def main():
    """Main function with command line argument support"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Upload shared assets to server')
    parser.add_argument('--asset', 
                       help='Upload specific asset (e.g., navbar.html, navbar.css, footer.html)')
    
    args = parser.parse_args()
    
    if args.asset:
        # Upload specific asset
        success = upload_specific_asset(args.asset)
    else:
        # Upload all shared assets
        success = upload_shared_assets()
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main()