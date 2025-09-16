#!/usr/bin/env python3
"""
Sitemap Generator for RHD Bearings Specification Pages
=====================================================

This script generates a comprehensive sitemap-specs.xml file for all bearing
specification pages that are hosted as static files. This sitemap will be
added to the existing WordPress sitemap structure without replacing it.

Features:
- Discovers all deployed specification pages automatically
- Generates proper XML sitemap format
- Includes priority and changefreq for SEO optimization
- Uploads the sitemap to the server
- Works alongside existing WordPress sitemaps

Usage:
    python3 scripts/generate_sitemap.py
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom
import importlib.util

# Import the curl_upload function
spec = importlib.util.spec_from_file_location("curl_upload", "deployment/curl_upload.py")
curl_upload_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(curl_upload_module)

class SpecsSitemapGenerator:
    def __init__(self):
        self.base_url = "https://rhdbearings.com"
        self.deployment_dir = Path("deployment")
        self.models_dir = Path("models")
        self.urls = []
        
    def get_series_from_model_number(self, model_number):
        """Determine series from model number"""
        if not model_number:
            return None
            
        model_str = str(model_number)
        
        # Special handling for 12.7mm bore variants and special models
        special_models = {
            "6201 12.7": "6200-series",
            "6202 12.7": "6200-series", 
            "6203 12.7": "6200-series",
            "6203A42": "6200-series"
        }
        
        # Check if this is a special model first
        if model_str in special_models:
            return special_models[model_str]
        
        # Exclude miniature series (3-digit models starting with 6)
        if model_str.startswith('6') and len(model_str) == 3:
            return "miniature-series"
        
        # 6000 series: 4-digit models starting with 60
        elif model_str.startswith('60') and len(model_str) == 4:
            return "6000-series"
        
        # 6200 series: 4-digit models starting with 62
        elif model_str.startswith('62') and len(model_str) == 4:
            return "6200-series"
        
        # 6300 series: 4-digit models starting with 63
        elif model_str.startswith('63') and len(model_str) == 4:
            return "6300-series"
        
        # 6800 series: 4-digit models starting with 68
        elif model_str.startswith('68') and len(model_str) == 4:
            return "6800-series"
        
        # 6900 series: 4-digit models starting with 69
        elif model_str.startswith('69') and len(model_str) == 4:
            return "6900-series"
        
        # 62200 series: 5-digit models starting with 622
        elif model_str.startswith('622') and len(model_str) == 5:
            return "62200-series"
        
        # 62300 series: 5-digit models starting with 623
        elif model_str.startswith('623') and len(model_str) == 5:
            return "62300-series"
        
        # 16000 series: 5-digit models starting with 16
        elif model_str.startswith('16') and len(model_str) == 5:
            return "16000-series"
        
        return None

    def discover_specification_pages(self):
        """Discover all specification pages from deployment directory and models"""
        print("🔍 Discovering specification pages...")
        
        # 1. Add main specs hub page
        self.urls.append({
            'url': f"{self.base_url}/specs/",
            'priority': '1.0',
            'changefreq': 'weekly',
            'title': 'Bearing Specifications Hub - Technical Data & Performance Grades'
        })
        
        # Alternative URL for specs page
        self.urls.append({
            'url': f"{self.base_url}/specs.html",
            'priority': '1.0',
            'changefreq': 'weekly',
            'title': 'Bearing Specifications Hub - Technical Data & Performance Grades'
        })
        
        # 2. Add main series pages
        series_info = {
            "6000-series": {"name": "6000 Series", "priority": "0.9"},
            "6200-series": {"name": "6200 Series", "priority": "0.9"},
            "6300-series": {"name": "6300 Series", "priority": "0.9"},
            "16000-series": {"name": "16000 Series", "priority": "0.9"},
            "62200-series": {"name": "62200 Series", "priority": "0.9"},
            "62300-series": {"name": "62300 Series", "priority": "0.9"},
            "6800-series": {"name": "6800 Series", "priority": "0.9"},
            "6900-series": {"name": "6900 Series", "priority": "0.9"},
            "miniature-series": {"name": "Miniature Series", "priority": "0.9"}
        }
        
        for series, info in series_info.items():
            if series == "miniature-series":
                self.urls.append({
                    'url': f"{self.base_url}/specs/miniature-series.html",
                    'priority': info['priority'],
                    'changefreq': 'monthly',
                    'title': f"{info['name']} Ball Bearings"
                })
            else:
                # Check if deployment directory exists for this series
                series_dir = self.deployment_dir / series
                if series_dir.exists():
                    self.urls.append({
                        'url': f"{self.base_url}/specs/{series}/",
                        'priority': info['priority'],
                        'changefreq': 'monthly',
                        'title': f"{info['name']} Ball Bearings"
                    })
        
        # 3. Add individual model pages
        if self.models_dir.exists():
            model_files = list(self.models_dir.glob("*.json"))
            print(f"   📋 Found {len(model_files)} model files")
            
            for model_file in model_files:
                model_number = model_file.stem
                series = self.get_series_from_model_number(model_number)
                
                if series:
                    if series == "miniature-series":
                        # Miniature series models
                        url = f"{self.base_url}/specs/miniature-series/{model_number}/"
                        priority = "0.8"
                    else:
                        # Regular series models
                        url = f"{self.base_url}/specs/{series}/{model_number}/"
                        priority = "0.8"
                    
                    self.urls.append({
                        'url': url,
                        'priority': priority,
                        'changefreq': 'monthly',
                        'title': f"{model_number} Bearing Specifications"
                    })
                    
                    print(f"   ✅ Added: {model_number} ({series})")
                else:
                    print(f"   ⏭️  Skipped: {model_number} (unknown series)")
        
        print(f"✅ Discovered {len(self.urls)} specification pages")
        return len(self.urls)

    def generate_sitemap_xml(self):
        """Generate the XML sitemap content"""
        print("🔧 Generating sitemap XML...")
        
        # Create root element
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        # Add each URL
        for url_info in self.urls:
            url_element = ET.SubElement(urlset, 'url')
            
            # Add location
            loc = ET.SubElement(url_element, 'loc')
            loc.text = url_info['url']
            
            # Add last modified (current date)
            lastmod = ET.SubElement(url_element, 'lastmod')
            lastmod.text = datetime.now().strftime('%Y-%m-%d')
            
            # Add change frequency
            changefreq = ET.SubElement(url_element, 'changefreq')
            changefreq.text = url_info['changefreq']
            
            # Add priority
            priority = ET.SubElement(url_element, 'priority')
            priority.text = url_info['priority']
        
        # Pretty print the XML
        rough_string = ET.tostring(urlset, 'unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Remove empty lines and fix formatting
        lines = [line for line in pretty_xml.split('\n') if line.strip()]
        formatted_xml = '\n'.join(lines)
        
        print(f"✅ Generated XML sitemap with {len(self.urls)} URLs")
        return formatted_xml

    def save_sitemap(self, xml_content):
        """Save the sitemap to deployment directory"""
        sitemap_path = self.deployment_dir / "sitemap-specs.xml"
        
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✅ Saved sitemap: {sitemap_path}")
        return sitemap_path

    def upload_sitemap(self, sitemap_path):
        """Upload the sitemap to the server"""
        print("📤 Uploading sitemap to server...")
        
        try:
            # Create a custom upload function for the sitemap
            import subprocess
            import os
            from dotenv import load_dotenv
            
            load_dotenv()
            ftp_password = os.getenv('FTP_PASSWORD')
            
            if not ftp_password:
                print("❌ FTP_PASSWORD not found in .env file")
                return False
            
            # Upload using curl
            cmd = [
                'curl', '-T', str(sitemap_path),
                '-u', f'rhdbear1:{ftp_password}',
                'ftp://rhdbearings.com/public_html/sitemap-specs.xml'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Sitemap uploaded successfully!")
                print(f"🔗 Available at: {self.base_url}/sitemap-specs.xml")
                return True
            else:
                print(f"❌ Upload failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error uploading sitemap: {e}")
            return False

    def generate_robots_txt_addition(self):
        """Generate the addition needed for robots.txt"""
        robots_addition = f"""
# Additional sitemap for bearing specification pages
Sitemap: {self.base_url}/sitemap-specs.xml
"""
        
        robots_path = self.deployment_dir / "robots-addition.txt"
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write(robots_addition.strip())
        
        print(f"✅ Generated robots.txt addition: {robots_path}")
        print("\n📋 ADD THIS TO YOUR EXISTING ROBOTS.TXT:")
        print("=" * 50)
        print(robots_addition.strip())
        print("=" * 50)
        
        return robots_addition

    def generate_wordpress_integration_guide(self):
        """Generate instructions for WordPress/RankMath integration"""
        guide = f"""
🔧 WORDPRESS & RANKMATH INTEGRATION GUIDE
========================================

Your sitemap-specs.xml has been created and uploaded. Here's how to integrate it:

1. RANKMATH SITEMAP INTEGRATION:
   - Go to RankMath → Sitemap Settings
   - Navigate to "Sitemap Index" 
   - Add custom sitemap: {self.base_url}/sitemap-specs.xml
   - Or add this to your sitemap index manually

2. ROBOTS.TXT UPDATE:
   - Add this line to your WordPress robots.txt:
   Sitemap: {self.base_url}/sitemap-specs.xml

3. GOOGLE SEARCH CONSOLE:
   - Submit the new sitemap: {self.base_url}/sitemap-specs.xml
   - This will help Google discover your specification pages

4. WORDPRESS SITEMAP INDEX:
   If you have a sitemap index (sitemap.xml), add this entry:
   <sitemap>
       <loc>{self.base_url}/sitemap-specs.xml</loc>
       <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
   </sitemap>

📊 SITEMAP STATISTICS:
- Total specification pages: {len(self.urls)}
- Main hub pages: 2
- Series pages: 9  
- Individual model pages: {len(self.urls) - 11}

🔗 LIVE SITEMAP: {self.base_url}/sitemap-specs.xml
"""
        
        guide_path = self.deployment_dir / "wordpress-integration-guide.txt"
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        print(f"✅ Generated integration guide: {guide_path}")
        return guide

    def run(self):
        """Run the complete sitemap generation process"""
        print("🚀 RHD BEARINGS SITEMAP GENERATOR")
        print("=" * 50)
        print("Generating sitemap for specification pages...")
        print("This will NOT replace your existing WordPress sitemaps.")
        print("=" * 50)
        
        # Step 1: Discover pages
        page_count = self.discover_specification_pages()
        if page_count == 0:
            print("❌ No pages found to include in sitemap")
            return False
        
        # Step 2: Generate XML
        xml_content = self.generate_sitemap_xml()
        
        # Step 3: Save sitemap
        sitemap_path = self.save_sitemap(xml_content)
        
        # Step 4: Upload sitemap
        upload_success = self.upload_sitemap(sitemap_path)
        
        # Step 5: Generate robots.txt addition
        self.generate_robots_txt_addition()
        
        # Step 6: Generate WordPress integration guide
        self.generate_wordpress_integration_guide()
        
        print("\n" + "=" * 50)
        print("🎉 SITEMAP GENERATION COMPLETE!")
        print("=" * 50)
        
        if upload_success:
            print(f"✅ Sitemap uploaded: {self.base_url}/sitemap-specs.xml")
            print(f"📊 Total pages: {len(self.urls)}")
            print("📋 Next steps:")
            print("   1. Add the sitemap to your robots.txt")
            print("   2. Submit to Google Search Console")
            print("   3. Add to RankMath sitemap index")
            print("\nCheck the generated integration guide for detailed instructions.")
        else:
            print("⚠️  Sitemap generated but upload failed")
            print("Please upload deployment/sitemap-specs.xml manually")
        
        return upload_success

def main():
    generator = SpecsSitemapGenerator()
    success = generator.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
