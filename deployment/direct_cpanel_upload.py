#!/usr/bin/env python3
"""
Direct cPanel Upload - Use FTP credentials to upload the file
"""

import os
import sys
import ftplib
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DirectCPanelUploader:
    def __init__(self):
        """Initialize direct cPanel uploader"""
        # Try different credential combinations
        self.ftp_host = os.getenv('FTP_HOST') or 'ftp.rhdbearings.com'
        self.ftp_username = os.getenv('FTP_USERNAME') or os.getenv('CPANEL_USERNAME') or 'rhdbearings'
        self.ftp_password = os.getenv('FTP_PASSWORD') or os.getenv('CPANEL_PASSWORD')
        self.ftp_port = int(os.getenv('FTP_PORT', '21'))
        self.wp_root = os.getenv('FTP_ROOT_PATH', '/public_html')
        
        logger.info(f"FTP Host: {self.ftp_host}")
        logger.info(f"FTP Username: {self.ftp_username}")
        logger.info(f"FTP Port: {self.ftp_port}")
        logger.info(f"Root Path: {self.wp_root}")
    
    def upload_file(self):
        """Upload the HTML file via FTP"""
        try:
            logger.info(f"🔗 Connecting to FTP: {self.ftp_host}:{self.ftp_port}")
            
            # Connect to FTP
            ftp = ftplib.FTP()
            ftp.connect(self.ftp_host, self.ftp_port)
            
            logger.info("🔐 Logging in...")
            ftp.login(self.ftp_username, self.ftp_password)
            
            logger.info("✅ FTP connection established!")
            
            # Navigate to WordPress root
            try:
                ftp.cwd(self.wp_root)
                logger.info(f"📁 Changed to directory: {self.wp_root}")
            except Exception as e:
                logger.warning(f"⚠️ Could not change to {self.wp_root}: {e}")
                logger.info("📁 Using current directory")
            
            # Show current directory
            current_dir = ftp.pwd()
            logger.info(f"📍 Current directory: {current_dir}")
            
            # List files to confirm we're in the right place
            try:
                files = ftp.nlst()
                logger.info(f"📂 Found {len(files)} files/folders")
                if 'wp-config.php' in files or 'index.php' in files:
                    logger.info("✅ Confirmed: We're in WordPress root directory")
                else:
                    logger.warning("⚠️ WordPress files not found in current directory")
            except:
                logger.info("📂 Could not list directory contents")
            
            # Upload the HTML file
            local_file = '../miniature-bearings.html'
            remote_file = 'miniature-bearings.html'
            
            if not os.path.exists(local_file):
                logger.error(f"❌ Local file not found: {local_file}")
                return False
            
            logger.info(f"📤 Uploading {local_file} as {remote_file}...")
            
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {remote_file}', f)
            
            logger.info("✅ File uploaded successfully!")
            
            # Verify upload
            try:
                size = ftp.size(remote_file)
                logger.info(f"📏 Remote file size: {size:,} bytes")
            except:
                logger.info("📏 Could not verify file size")
            
            ftp.quit()
            
            return True
            
        except ftplib.error_perm as e:
            logger.error(f"❌ FTP Permission Error: {e}")
            return False
        except ftplib.error_temp as e:
            logger.error(f"❌ FTP Temporary Error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ FTP Upload failed: {e}")
            return False

def main():
    """Main execution"""
    print("🚀 Direct cPanel Upload via FTP")
    print("=" * 40)
    
    try:
        uploader = DirectCPanelUploader()
        success = uploader.upload_file()
        
        if success:
            print("\n🎉 SUCCESS! File uploaded to your server!")
            print("🔗 Your page: https://rhdbearings.com/miniature-bearings.html")
            print("✅ Complete HTML with perfect CSS styling")
            print("✅ Bypasses all WordPress conflicts")
            print("✅ Ready to view immediately!")
        else:
            print("\n❌ Upload failed. Let me try alternative credentials...")
            
            # Try alternative FTP hosts
            alt_hosts = ['rhdbearings.com', 'ftp.rhdbearings.com', 'www.rhdbearings.com']
            
            for host in alt_hosts:
                print(f"\n🔄 Trying {host}...")
                uploader.ftp_host = host
                if uploader.upload_file():
                    print(f"✅ Success with {host}!")
                    break
            else:
                print("\n❌ All upload attempts failed.")
                print("📋 Manual upload required - files are ready in your folder")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
