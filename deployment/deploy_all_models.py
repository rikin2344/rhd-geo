#!/usr/bin/env python3
"""
Master Deployment Script - Generate and Deploy All Model Pages

This script:
1. Generates all model pages using generate_all_models.py
2. Uploads all pages to the server using curl_upload.py
"""

import os
import subprocess
import sys
from pathlib import Path

def run_script(script_path, args=None):
    """Run a Python script and return success status"""
    try:
        cmd = [sys.executable, script_path]
        if args:
            cmd.extend(args)
        
        print(f"🚀 Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ Script completed successfully")
            return True
        else:
            print(f"❌ Script failed with error:")
            print(f"   {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return False

def check_template_exists():
    """Check if the required template file exists"""
    template_path = "../webpages/templates/index_new_claude.html"
    if not os.path.exists(template_path):
        print(f"❌ Template file not found: {template_path}")
        print("💡 Please ensure the template file exists before running this script")
        return False
    return True

def main():
    """Main deployment process"""
    print("🚀 MASTER DEPLOYMENT: GENERATE AND DEPLOY ALL MODEL PAGES")
    print("=" * 70)
    
    # Check prerequisites
    print("🔍 Checking prerequisites...")
    if not check_template_exists():
        sys.exit(1)
    
    print("✅ All prerequisites met")
    print()
    
    # Step 1: Generate all model pages
    print("📋 STEP 1: GENERATING ALL MODEL PAGES")
    print("-" * 50)
    
    generate_script = "../scripts/generate_all_models.py"
    if not os.path.exists(generate_script):
        print(f"❌ Generate script not found: {generate_script}")
        sys.exit(1)
    
    if not run_script(generate_script):
        print("❌ Failed to generate model pages")
        sys.exit(1)
    
    print("✅ All model pages generated successfully")
    print()
    
    # Step 2: Upload all pages to server
    print("📤 STEP 2: UPLOADING ALL PAGES TO SERVER")
    print("-" * 50)
    
    upload_script = "curl_upload.py"
    if not os.path.exists(upload_script):
        print(f"❌ Upload script not found: {upload_script}")
        sys.exit(1)
    
    # Get list of all models
    models_dir = Path("../models")
    models = []
    if models_dir.exists():
        for file in models_dir.glob("*.json"):
            model_name = file.stem
            if model_name.isdigit():
                models.append(model_name)
    
    models.sort(key=int)
    print(f"📋 Found {len(models)} models to upload: {', '.join(models)}")
    print()
    
    # Upload each model page
    successful_uploads = []
    failed_uploads = []
    
    for model in models:
        print(f"📤 Uploading {model}...")
        if run_script(upload_script, [model]):
            successful_uploads.append(model)
        else:
            failed_uploads.append(model)
        print()
    
    # Final summary
    print("=" * 70)
    print("📊 DEPLOYMENT SUMMARY")
    print("=" * 70)
    
    if successful_uploads:
        print(f"✅ Successfully uploaded ({len(successful_uploads)}):")
        for model in successful_uploads:
            print(f"   • {model}: https://rhdbearings.com/specs/miniature-series/{model}/")
    
    if failed_uploads:
        print(f"\n❌ Failed to upload ({len(failed_uploads)}):")
        for model in failed_uploads:
            print(f"   • {model}")
    
    print(f"\n🎯 Total: {len(successful_uploads)}/{len(models)} pages deployed successfully")
    
    if failed_uploads:
        print(f"\n⚠️  {len(failed_uploads)} page(s) failed to upload")
        print("💡 Check the error messages above and try uploading individual pages")
        sys.exit(1)
    else:
        print(f"\n🎉 SUCCESS! All {len(models)} model pages deployed!")
        print("🌐 Your website is fully updated with all model pages!")
        print("\n🔗 Quick Links:")
        for model in models[:5]:  # Show first 5 models
            print(f"   • {model}: https://rhdbearings.com/specs/miniature-series/{model}/")
        if len(models) > 5:
            print(f"   • ... and {len(models) - 5} more models")

if __name__ == "__main__":
    main()
