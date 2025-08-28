#!/usr/bin/env python3
"""
Batch Generate All Model Pages

This script generates HTML pages for all bearing models using the existing generate_bearing_page.py script.
"""

import os
import subprocess
import sys
from pathlib import Path

def get_all_models():
    """Get list of all model numbers from the models directory"""
    models_dir = Path("../models")
    models = []
    
    if models_dir.exists():
        for file in models_dir.glob("*.json"):
            model_name = file.stem
            if model_name.isdigit():
                models.append(model_name)
    
    # Sort models numerically
    models.sort(key=int)
    return models

def generate_model_page(model_number):
    """Generate a single model page"""
    print(f"🔧 Generating page for model {model_number}...")
    
    # Define paths
    json_file = f"../models/{model_number}.json"
    template_file = "../webpages/templates/index_new_claude.html"
    output_file = f"../webpages/internalwebpages/specs/miniature-series/{model_number}/index.html"
    
    # Check if template exists
    if not os.path.exists(template_file):
        print(f"❌ Template file not found: {template_file}")
        return False
    
    # Check if JSON file exists
    if not os.path.exists(json_file):
        print(f"❌ JSON file not found: {json_file}")
        return False
    
    try:
        # Run the generate_bearing_page.py script
        cmd = [
            "python3", "generate_bearing_page.py",
            json_file,
            template_file,
            output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print(f"✅ Successfully generated {model_number} page")
            return True
        else:
            print(f"❌ Failed to generate {model_number} page:")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating {model_number} page: {e}")
        return False

def main():
    """Main execution"""
    print("🚀 BATCH GENERATING ALL MODEL PAGES")
    print("=" * 50)
    
    # Get all models
    models = get_all_models()
    
    if not models:
        print("❌ No model JSON files found in ../models/ directory")
        sys.exit(1)
    
    print(f"📋 Found {len(models)} models: {', '.join(models)}")
    print()
    
    # Generate pages for each model
    successful_generations = []
    failed_generations = []
    
    for model in models:
        success = generate_model_page(model)
        if success:
            successful_generations.append(model)
        else:
            failed_generations.append(model)
        print()
    
    # Summary
    print("=" * 50)
    print("📊 GENERATION SUMMARY")
    print("=" * 50)
    
    if successful_generations:
        print(f"✅ Successfully generated ({len(successful_generations)}):")
        for model in successful_generations:
            print(f"   • {model}")
    
    if failed_generations:
        print(f"\n❌ Failed to generate ({len(failed_generations)}):")
        for model in failed_generations:
            print(f"   • {model}")
    
    print(f"\n🎯 Total: {len(successful_generations)}/{len(models)} pages generated successfully")
    
    if failed_generations:
        print(f"\n⚠️  {len(failed_generations)} pages failed to generate")
        sys.exit(1)
    else:
        print(f"\n🎉 All {len(models)} model pages generated successfully!")
        print("📁 Pages are ready in ../webpages/internalwebpages/specs/miniature-series/")

if __name__ == "__main__":
    main()
