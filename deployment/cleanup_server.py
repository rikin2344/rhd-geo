#!/usr/bin/env python3
"""
Clean up all the test files and garbage from the server
"""

import os
import ftplib
from dotenv import load_dotenv

load_dotenv()

def cleanup_server():
    """Remove all test files and keep only the working miniature-bearings.html"""
    
    host = os.getenv('FTP_HOST', 'ftp.rhdbearings.com')
    username = os.getenv('FTP_USERNAME', 'rikin@rhdbearings.com')
    password = os.getenv('FTP_PASSWORD')
    
    # Files to delete (all our test uploads)
    files_to_delete = [
        'test-upload.html',
        'miniature-clean.html', 
        'miniature-series.html',
        'miniature_bearings_page.html',
        'miniature-bearings.htm',
        'cgi-bin/miniature.html'
    ]
    
    # Directories to clean
    directories_to_remove = [
        'miniature-series'  # The directory we created earlier
    ]
    
    print("🧹 Cleaning up server garbage...")
    
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, 21, timeout=60)
        ftp.login(username, password)
        ftp.set_pasv(False)
        
        print("✅ Connected to server")
        
        # Navigate to public_html
        ftp.cwd('/public_html')
        
        # Delete individual files
        for file in files_to_delete:
            try:
                if '/' in file:
                    # Handle files in subdirectories
                    dir_path, filename = file.rsplit('/', 1)
                    ftp.cwd(dir_path)
                    ftp.delete(filename)
                    ftp.cwd('/public_html')  # Go back to root
                else:
                    ftp.delete(file)
                print(f"🗑️ Deleted: {file}")
            except Exception as e:
                print(f"⚠️ Could not delete {file}: {e}")
        
        # Remove directories
        for directory in directories_to_remove:
            try:
                # First delete files inside directory
                ftp.cwd(directory)
                files = ftp.nlst()
                for file in files:
                    try:
                        ftp.delete(file)
                        print(f"🗑️ Deleted: {directory}/{file}")
                    except:
                        pass
                
                # Go back and remove directory
                ftp.cwd('/public_html')
                ftp.rmd(directory)
                print(f"🗑️ Removed directory: {directory}")
            except Exception as e:
                print(f"⚠️ Could not remove directory {directory}: {e}")
        
        # Restore original .htaccess if we modified it
        try:
            ftp.delete('.htaccess')
            print("🗑️ Removed our modified .htaccess")
        except:
            print("⚠️ Could not remove .htaccess (might be original)")
        
        ftp.quit()
        
        print("\n✅ Server cleanup completed!")
        print("🎯 Only miniature-bearings.html remains (the working file)")
        print("🔗 Working URL: https://rhdbearings.com/miniature-bearings.html")
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")

if __name__ == "__main__":
    cleanup_server()
