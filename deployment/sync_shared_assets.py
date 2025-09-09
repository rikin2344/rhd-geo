#!/usr/bin/env python3
"""
Sync shared assets from webpages/shared to deployment/shared
This maintains clean separation between development and deployment files
"""

import shutil
import os
from pathlib import Path

def sync_shared_assets():
    """Copy all shared assets from webpages/shared to deployment/shared"""
    
    source_dir = Path("../webpages/shared")
    dest_dir = Path("shared")
    
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return False
    
    if not dest_dir.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created deployment/shared directory")
    
    print("🔄 SYNCING SHARED ASSETS")
    print("=" * 40)
    print(f"📂 From: {source_dir}")
    print(f"📂 To: {dest_dir}")
    print("=" * 40)
    
    synced_files = []
    
    # Copy all files from webpages/shared to deployment/shared
    for source_file in source_dir.glob("*"):
        if source_file.is_file():
            dest_file = dest_dir / source_file.name
            
            try:
                shutil.copy2(source_file, dest_file)
                print(f"✅ Synced: {source_file.name}")
                synced_files.append(source_file.name)
            except Exception as e:
                print(f"❌ Failed to sync {source_file.name}: {e}")
                return False
    
    print("=" * 40)
    print(f"📊 SYNC SUMMARY: {len(synced_files)} files synced")
    print("=" * 40)
    
    if synced_files:
        print("✅ Synced files:")
        for file in synced_files:
            print(f"   • {file}")
    
    print("\n💡 Next steps:")
    print("   1. Run: python3 upload_shared_assets.py")
    print("   2. Or run your deployment script to upload everything")
    
    return True

def main():
    """Main function"""
    print("🌐 RHD Bearings - Shared Assets Sync")
    print("=" * 50)
    
    success = sync_shared_assets()
    
    if success:
        print("\n🎉 All shared assets synced successfully!")
    else:
        print("\n❌ Sync failed. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
