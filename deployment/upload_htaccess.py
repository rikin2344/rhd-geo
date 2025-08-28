#!/usr/bin/env python3
"""
Upload .htaccess file to server for RHD Bearings
This script uploads the .htaccess file to enable clean URLs
"""

import ftplib
import os
from pathlib import Path

def upload_htaccess():
    """Upload .htaccess file to server"""
    
    # FTP credentials from .env file
    host = "ftp.rhdbearings.com"
    username = "rikin@rhdbearings.com"
    password = "Rikin@@2025##"
    root_path = "/public_html"
    
    try:
        # Check if .htaccess file exists locally
        htaccess_file = Path("new_htaccess")
        if not htaccess_file.exists():
            print("❌ Error: new_htaccess file not found!")
            print("💡 Make sure you're running this script from the deployment/ directory")
            return False
        
        print("🔐 Connecting to FTP server...")
        ftp = ftplib.FTP(host)
        ftp.login(username, password)
        print("✅ Connected successfully!")
        
        # Change to the root directory
        print(f"📁 Changing to directory: {root_path}")
        ftp.cwd(root_path)
        print("✅ Changed to public_html directory")
        
        # Check current .htaccess file size (if it exists)
        try:
            current_size = ftp.size(".htaccess")
            print(f"📊 Current .htaccess file size: {current_size} bytes")
        except:
            print("📊 No existing .htaccess file found (will create new one)")
        
        print("📤 Uploading .htaccess file...")
        with open(htaccess_file, "rb") as file:
            ftp.storbinary(f"STOR .htaccess", file)
        
        print("✅ .htaccess file uploaded successfully!")
        
        # Verify the file was uploaded and get its size
        print("🔍 Verifying upload...")
        files = ftp.nlst()
        if ".htaccess" in files:
            new_size = ftp.size(".htaccess")
            print(f"✅ .htaccess file confirmed on server! Size: {new_size} bytes")
            
            # Test if the file is accessible
            print("🧪 Testing file accessibility...")
            try:
                ftp.retrbinary("RETR .htaccess", lambda x: None)
                print("✅ File is accessible and readable")
            except Exception as e:
                print(f"⚠️  Warning: File uploaded but may have permission issues: {e}")
        else:
            print("❌ Error: .htaccess file not found in server listing after upload")
            return False
        
        ftp.quit()
        print("🔒 FTP connection closed")
        print("\n🎉 .htaccess file successfully uploaded!")
        print("🌐 Clean URLs are now enabled for all series pages:")
        print("   • https://rhdbearings.com/specs/6000-series/")
        print("   • https://rhdbearings.com/specs/6200-series/")
        print("   • https://rhdbearings.com/specs/miniature-series/")
        print("   • And all other series pages...")
        return True
        
    except ftplib.error_perm as e:
        print(f"❌ FTP Permission Error: {e}")
        print("💡 Check if your FTP user has write permissions to the public_html directory")
        return False
    except ftplib.error_temp as e:
        print(f"❌ FTP Temporary Error: {e}")
        print("💡 This might be a temporary server issue, try again later")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 RHD BEARINGS - .htaccess UPLOAD SCRIPT")
    print("=" * 50)
    print("This script will upload the .htaccess file to enable clean URLs")
    print("for all series and model pages on your website.")
    print("=" * 50)
    
    success = upload_htaccess()
    
    if success:
        print("\n✅ Upload completed successfully!")
        print("🌐 Your website now supports clean URLs for all series pages")
    else:
        print("\n❌ Upload failed. Please check the error messages above.")
        print("💡 Common issues:")
        print("   • FTP credentials are incorrect")
        print("   • FTP user doesn't have write permissions")
        print("   • Server is temporarily unavailable")
        print("   • .htaccess file doesn't exist locally")
        exit(1)
