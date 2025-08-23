#!/usr/bin/env python3
"""
FTP File Manager - Utility for managing files on the server
Useful for cleanup, maintenance, and file operations
"""

import os
import ftplib
import sys
import argparse
from dotenv import load_dotenv

load_dotenv()

class FTPManager:
    def __init__(self):
        self.username = os.getenv('FTP_USERNAME', 'rikin@rhdbearings.com')
        self.password = os.getenv('FTP_PASSWORD')
        self.host = os.getenv('FTP_HOST', 'ftp.rhdbearings.com')
        self.ftp = None
        
        if not self.password:
            print("❌ FTP_PASSWORD environment variable not found!")
            sys.exit(1)
    
    def connect(self):
        """Connect to FTP server"""
        try:
            print(f"🔌 Connecting to {self.host}...")
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.username, self.password)
            self.ftp.cwd('public_html')
            print("✅ Connected and navigated to public_html")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from FTP server"""
        if self.ftp:
            self.ftp.quit()
            print("🔌 FTP connection closed")
    
    def list_files(self, pattern=None):
        """List files on server, optionally filtered by pattern"""
        if not self.ftp:
            return []
        
        try:
            files = self.ftp.nlst()
            if pattern:
                files = [f for f in files if pattern.lower() in f.lower()]
            return files
        except Exception as e:
            print(f"❌ Error listing files: {e}")
            return []
    
    def delete_files(self, file_list, confirm=True):
        """Delete multiple files from server"""
        if not self.ftp:
            print("❌ Not connected to FTP server")
            return False
        
        if confirm:
            print(f"🚨 About to delete {len(file_list)} files:")
            for file in file_list:
                print(f"   • {file}")
            
            response = input("Type 'DELETE' to confirm: ")
            if response != 'DELETE':
                print("❌ Deletion cancelled")
                return False
        
        print(f"\n🗑️  Deleting {len(file_list)} files...")
        removed_files = []
        failed_files = []
        
        for file in file_list:
            try:
                self.ftp.delete(file)
                print(f"   ✅ Deleted: {file}")
                removed_files.append(file)
            except ftplib.error_perm as e:
                if "550" in str(e):  # File not found
                    print(f"   ⚠️  File not found: {file}")
                else:
                    print(f"   ❌ Permission error deleting {file}: {e}")
                    failed_files.append(file)
            except Exception as e:
                print(f"   ❌ Error deleting {file}: {e}")
                failed_files.append(file)
        
        # Summary
        print(f"\n📊 DELETION SUMMARY")
        print("=" * 30)
        
        if removed_files:
            print(f"✅ Successfully deleted ({len(removed_files)}):")
            for file in removed_files:
                print(f"   • {file}")
        
        if failed_files:
            print(f"\n❌ Failed to delete ({len(failed_files)}):")
            for file in failed_files:
                print(f"   • {file}")
        
        return len(failed_files) == 0
    
    def delete_directory(self, directory, recursive=False):
        """Delete directory from server"""
        if not self.ftp:
            print("❌ Not connected to FTP server")
            return False
        
        try:
            if recursive:
                # First delete contents
                original_cwd = self.ftp.pwd()
                self.ftp.cwd(directory)
                files = self.ftp.nlst()
                files = [f for f in files if f not in ['.', '..']]
                
                if files:
                    print(f"   📁 {directory}/ contains: {files}")
                    for file in files:
                        try:
                            self.ftp.delete(file)
                            print(f"   ✅ Deleted from directory: {file}")
                        except Exception as e:
                            print(f"   ❌ Could not delete {file}: {e}")
                
                self.ftp.cwd(original_cwd)
            
            # Remove directory
            self.ftp.rmd(directory)
            print(f"   ✅ Removed directory: {directory}/")
            return True
            
        except ftplib.error_perm:
            print(f"   ⚠️  Directory {directory}/ not found or already empty")
            return False
        except Exception as e:
            print(f"   ❌ Error removing directory: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='FTP File Manager for server maintenance')
    parser.add_argument('action', choices=['list', 'delete', 'cleanup'], 
                       help='Action to perform')
    parser.add_argument('--pattern', 
                       help='Pattern to filter files (for list/delete)')
    parser.add_argument('--files', nargs='+',
                       help='Specific files to delete')
    parser.add_argument('--directory',
                       help='Directory to delete')
    parser.add_argument('--recursive', action='store_true',
                       help='Recursively delete directory contents')
    parser.add_argument('--no-confirm', action='store_true',
                       help='Skip confirmation prompts')
    
    args = parser.parse_args()
    
    # Create FTP manager
    ftp_manager = FTPManager()
    
    if not ftp_manager.connect():
        sys.exit(1)
    
    try:
        if args.action == 'list':
            print("📂 Files on server:")
            files = ftp_manager.list_files(args.pattern)
            for file in files:
                print(f"   • {file}")
            print(f"\nTotal: {len(files)} files")
        
        elif args.action == 'delete':
            if args.files:
                ftp_manager.delete_files(args.files, not args.no_confirm)
            elif args.directory:
                if not args.no_confirm:
                    response = input(f"Delete directory '{args.directory}'? Type 'DELETE': ")
                    if response != 'DELETE':
                        print("❌ Deletion cancelled")
                        sys.exit(0)
                ftp_manager.delete_directory(args.directory, args.recursive)
            else:
                print("❌ Must specify --files or --directory for delete action")
        
        elif args.action == 'cleanup':
            # Interactive cleanup mode
            print("🧹 INTERACTIVE CLEANUP MODE")
            print("=" * 40)
            files = ftp_manager.list_files()
            
            if not files:
                print("No files found for cleanup")
                return
            
            print("Files on server:")
            for i, file in enumerate(files, 1):
                print(f"{i:2d}. {file}")
            
            print("\nEnter file numbers to delete (comma-separated) or 'q' to quit:")
            selection = input("Selection: ")
            
            if selection.lower() == 'q':
                print("Cleanup cancelled")
                return
            
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                files_to_delete = [files[i] for i in indices if 0 <= i < len(files)]
                
                if files_to_delete:
                    ftp_manager.delete_files(files_to_delete, not args.no_confirm)
                else:
                    print("No valid files selected")
            except ValueError:
                print("Invalid selection format")
    
    finally:
        ftp_manager.disconnect()

if __name__ == "__main__":
    main()
