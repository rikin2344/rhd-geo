#!/usr/bin/env python3
"""
Series Pages Generator from Enhanced JSON
=========================================

This script generates HTML series pages from the enhanced_bearing_series_pages.json file.
The generated HTML pages will be identical to the existing series pages structure.

Usage:
    python3 generate_series_pages_from_json.py [--series SERIES_NAME] [--output-dir OUTPUT_DIR]
"""

import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class SeriesPageGenerator:
    """Generates HTML series pages from enhanced_bearing_series_pages.json"""
    
    def __init__(self, json_file: str, output_dir: str = "webpages"):
        self.json_file = Path(json_file)
        self.output_dir = Path(output_dir)
        self.data = {}
        
        # Series mapping for directory names
        self.series_mapping = {
            'miniature_bearings': 'miniature-series',
            '6000_series': '6000-series',
            '6200_series': '6200-series',
            '6300_series': '6300-series',
            '6800_series': '6800-series',
            '6900_series': '6900-series',
            '16000_series': '16000-series',
            '62200_series': '62200-series',
            '62300_series': '62300-series'
        }
        
        # Series display names
        self.series_display_names = {
            'miniature_bearings': 'Miniature Ball Bearings',
            '6000_series': '6000 Series Deep Groove Ball Bearings',
            '6200_series': '6200 Series Heavy Duty Ball Bearings',
            '6300_series': '6300 Series Extra Heavy Duty Ball Bearings',
            '6800_series': '6800 Series Thin Section Light Ball Bearings',
            '6900_series': '6900 Series Thin Section Medium Ball Bearings',
            '16000_series': '16000 Series Angular Contact Ball Bearings',
            '62200_series': '62200 Series Heavy Duty Ball Bearings',
            '62300_series': '62300 Series Extra Heavy Duty Ball Bearings'
        }
    
    def load_json_data(self) -> bool:
        """Load the enhanced bearing series pages JSON data"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✅ Loaded JSON data from {self.json_file}")
            return True
        except Exception as e:
            print(f"❌ Error loading JSON file: {e}")
            return False
    
    def get_series_data(self, series_key: str) -> Optional[Dict[str, Any]]:
        """Get data for a specific series"""
        if 'series_pages' not in self.data:
            return None
        
        series_pages = self.data['series_pages']
        if series_key in series_pages:
            return series_pages[series_key]
        
        return None
    
    def generate_hero_section(self, series_data: Dict[str, Any], series_key: str) -> str:
        """Generate the hero section HTML"""
        series_name = series_data.get('series_name', '')
        series_code = series_data.get('series_code', '')
        description = series_data.get('description', '')
        
        # Extract specifications
        bore_range = series_data.get('bore_range', 'N/A')
        total_models = series_data.get('total_models', 0)
        
        # Get max load and RPM from specifications if available
        specs = series_data.get('specifications', {})
        max_rpm = specs.get('speed_range', 'N/A')
        if isinstance(max_rpm, str) and '-' in max_rpm:
            max_rpm = max_rpm.split('-')[-1].strip()
        
        # Get max load from load capacity range
        load_capacity = specs.get('load_capacity_range', 'N/A')
        if isinstance(load_capacity, str) and '-' in load_capacity:
            max_load = load_capacity.split('-')[-1].strip()
        else:
            max_load = 'N/A'
        
        # Generate title based on series
        if series_key == 'miniature_bearings':
            title = "Miniature Ball Bearings"
            subtitle = "Ultra-precision for space-critical applications"
        elif series_key == '6800_series':
            title = "6800 (61800) Series Bearings"
            subtitle = "Ultra-lightweight precision for miniature applications"
        elif series_key == '6900_series':
            title = "6900 (61900) Series Bearings"
            subtitle = "Medium-duty precision for compact applications"
        else:
            # Extract series number from series_name
            series_match = re.search(r'(\d+)', series_name)
            if series_match:
                series_num = series_match.group(1)
                title = f"{series_num} Series Bearings"
            else:
                title = series_name
            
            # Generate subtitle based on series characteristics
            if 'heavy' in series_name.lower():
                subtitle = "Heavy-duty engineering for enhanced performance"
            elif 'extra heavy' in series_name.lower():
                subtitle = "Extra heavy-duty engineering for maximum performance"
            elif 'angular' in series_name.lower():
                subtitle = "Angular contact precision for axial load applications"
            else:
                subtitle = "Deep groove precision for industrial applications"
        
        hero_html = f'''    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <div class="hero-container">
                <!-- Main Content (60%) -->
                <div class="hero-main">
                    <h1 class="hero-title">{title}</h1>
                    <p class="hero-subtitle">
                        {subtitle}
                    </p>
                    <p class="hero-description">
                        {description}
                    </p>
                    
                    <div class="hero-specs">
                        <div class="specs-compact">
                            <div class="spec-item">
                                <div class="spec-value">{bore_range}</div>
                                <div class="spec-label">Bore Range</div>
                            </div>
                            <div class="spec-item">
                                <div class="spec-value">{max_rpm}</div>
                                <div class="spec-label">Max RPM</div>
                            </div>
                            <div class="spec-item">
                                <div class="spec-value">{total_models}</div>
                                <div class="spec-label">Models</div>
                            </div>
                            <div class="spec-item">
                                <div class="spec-value">{max_load}</div>
                                <div class="spec-label">Max Load</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="hero-actions">
                        <a href="#models" class="btn btn-primary">View All Models</a>
                        <a href="#specifications" class="btn btn-secondary">Technical Specifications</a>
                    </div>
                </div>
                
                <!-- Hero Image -->
                <div class="hero-image">
                    <img src="https://rhdbearings.com/wp-content/uploads/2025/08/DGBB.png" alt="Deep Groove Ball Bearing - RHD Bearings" />
                </div>
            </div>
        </div>
    </section>'''
        
        return hero_html
    
    def generate_performance_grades_section(self, series_data: Dict[str, Any], series_key: str) -> str:
        """Generate the RHD Performance Grades section"""
        performance_grades = series_data.get('rhd_performance_grades', {})
        
        if not performance_grades:
            return ""
        
        # Generate section header
        if series_key == 'miniature_bearings':
            section_subtitle = "Engineered for ultra-precision miniature applications & space-critical requirements"
        elif series_key == '6800_series':
            section_subtitle = "Engineered for ultra-lightweight applications & miniature precision requirements"
        elif series_key == '6900_series':
            section_subtitle = "Engineered for medium-duty applications & compact precision requirements"
        elif 'heavy' in series_data.get('series_name', '').lower():
            section_subtitle = "Enhanced capacity engineering for heavy-duty industrial solutions"
        else:
            section_subtitle = "Engineered for industrial applications & enhanced performance requirements"
        
        grades_html = f'''    <!-- RHD Performance Grades -->
    <section class="section">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">RHD PERFORMANCE GRADES</h2>
                <p class="section-subtitle">{section_subtitle}</p>
            </div>
            
            <div class="performance-grades-grid">'''
        
        # Generate grade cards
        for grade_key, grade_data in performance_grades.items():
            if grade_key == 'power_tool_focus':
                continue  # Skip the power tool focus section for now
            
            grade_name = grade_data.get('name', '')
            rpm = grade_data.get('rpm', 'N/A')
            description = grade_data.get('description', '')
            applications = grade_data.get('applications', [])
            is_featured = grade_data.get('featured', False)
            badge = grade_data.get('badge', '')
            
            # Extract RPM number
            rpm_match = re.search(r'([\d,]+)', rpm)
            rpm_display = rpm_match.group(1) if rpm_match else rpm
            
            # Generate grade card HTML
            featured_class = " grade-featured" if is_featured else ""
            badge_html = f'<div class="grade-badge">{badge}</div>' if badge else ''
            
            # Generate application tags
            app_tags = ''.join([f'<span class="application-tag">{app}</span>' for app in applications])
            
            grades_html += f'''
                <div class="grade-card{featured_class}">
                    {badge_html}
                    <div class="grade-header">
                        <div class="grade-rpm">{rpm_display} RPM</div>
                        <h3 class="grade-title">{grade_name}</h3>
                        <div class="grade-subtitle">{series_data.get('series_name', '')}</div>
                    </div>
                    <div class="grade-description">
                        <p>{description}</p>
                    </div>
                    <div class="grade-applications">
                        {app_tags}
                    </div>
                </div>'''
        
        grades_html += '''
            </div>
        </div>
    </section>'''
        
        return grades_html
    
    def generate_applications_section(self, series_data: Dict[str, Any]) -> str:
        """Generate the detailed applications section"""
        applications = series_data.get('detailed_applications', {})
        
        if not applications:
            return ""
        
        apps_html = '''    <!-- Detailed Applications -->
    <section class="section">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">DETAILED APPLICATIONS</h2>
                <p class="section-subtitle">Comprehensive application coverage across industries</p>
            </div>
            
            <div class="applications-grid">'''
        
        for app_key, app_data in applications.items():
            category = app_data.get('category', '')
            app_list = app_data.get('applications', [])
            requirements = app_data.get('key_requirements', '')
            
            apps_html += f'''
                <div class="application-category">
                    <h3 class="category-title">{category}</h3>
                    <ul class="application-list">'''
            
            for app in app_list:
                apps_html += f'<li>{app}</li>'
            
            apps_html += f'''
                    </ul>
                    <div class="key-requirements">
                        <strong>Key Requirements:</strong> {requirements}
                    </div>
                </div>'''
        
        apps_html += '''
            </div>
        </div>
    </section>'''
        
        return apps_html
    
    def generate_models_section(self, series_data: Dict[str, Any], series_key: str) -> str:
        """Generate the models section with JavaScript data"""
        models = series_data.get('models_with_links', [])
        
        if not models:
            return ""
        
        # Generate JavaScript data
        js_data = []
        for model in models:
            js_data.append({
                'model': model.get('model', ''),
                'id': model.get('id', ''),
                'od': model.get('od', ''),
                'width': model.get('width', ''),
                'dynamic_load': model.get('dynamic_load', ''),
                'static_load': model.get('static_load', ''),
                'grease_speed': model.get('grease_speed', ''),
                'oil_speed': model.get('oil_speed', ''),
                'weight': model.get('weight', '')
            })
        
        # Convert to JavaScript format
        js_data_str = json.dumps(js_data, indent=8)
        
        models_html = f'''    <!-- Models Section -->
    <section id="models" class="section">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">AVAILABLE MODELS</h2>
                <p class="section-subtitle">Complete range of {series_data.get('series_name', '')} bearings</p>
            </div>
            
            <div class="models-container">
                <div class="models-grid" id="modelsGrid">
                    <!-- Models will be populated by JavaScript -->
                </div>
            </div>
        </div>
    </section>

    <script>
        // Models data
        const bearingsData = {js_data_str};
        
        // Generate models grid
        function generateModelsGrid() {{
            const grid = document.getElementById('modelsGrid');
            if (!grid) return;
            
            grid.innerHTML = '';
            
            bearingsData.forEach(bearing => {{
                const modelCard = document.createElement('div');
                modelCard.className = 'model-card';
                modelCard.innerHTML = `
                    <div class="model-header">
                        <h3 class="model-number">${{bearing.model}}</h3>
                        <div class="model-specs">
                            <span class="spec">ID: ${{bearing.id}}</span>
                            <span class="spec">OD: ${{bearing.od}}</span>
                            <span class="spec">W: ${{bearing.width}}</span>
                        </div>
                    </div>
                    <div class="model-details">
                        <div class="detail-row">
                            <span class="label">Dynamic Load:</span>
                            <span class="value">${{bearing.dynamic_load}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Static Load:</span>
                            <span class="value">${{bearing.static_load}}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Grease Speed:</span>
                            <span class="value">${{bearing.grease_speed}} RPM</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Oil Speed:</span>
                            <span class="value">${{bearing.oil_speed}} RPM</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Weight:</span>
                            <span class="value">${{bearing.weight}}</span>
                        </div>
                    </div>
                    <div class="model-actions">
                        <a href="/specs/${{bearing.model}}" class="btn btn-primary btn-sm">View Details</a>
                    </div>
                `;
                grid.appendChild(modelCard);
            }});
        }}
        
        // Initialize when page loads
        document.addEventListener('DOMContentLoaded', generateModelsGrid);
    </script>'''
        
        return models_html
    
    def generate_specifications_section(self, series_data: Dict[str, Any]) -> str:
        """Generate the specifications section"""
        specs = series_data.get('specifications', {})
        
        if not specs:
            return ""
        
        specs_html = '''    <!-- Specifications Section -->
    <section id="specifications" class="section">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">TECHNICAL SPECIFICATIONS</h2>
                <p class="section-subtitle">Complete technical data and specifications</p>
            </div>
            
            <div class="specifications-grid">'''
        
        # Generate specification cards
        spec_items = [
            ('Bore Diameter Range', specs.get('bore_diameter_range', 'N/A')),
            ('Outer Diameter Range', specs.get('outer_diameter_range', 'N/A')),
            ('Width Range', specs.get('width_range', 'N/A')),
            ('Load Capacity Range', specs.get('load_capacity_range', 'N/A')),
            ('Speed Range', specs.get('speed_range', 'N/A')),
            ('Temperature Range', specs.get('temperature_range', 'N/A'))
        ]
        
        for spec_name, spec_value in spec_items:
            if spec_value != 'N/A':
                specs_html += f'''
                <div class="spec-card">
                    <h3 class="spec-title">{spec_name}</h3>
                    <p class="spec-value">{spec_value}</p>
                </div>'''
        
        # Add precision grades if available
        precision_grades = specs.get('precision_grades', [])
        if precision_grades:
            specs_html += f'''
                <div class="spec-card">
                    <h3 class="spec-title">Precision Grades</h3>
                    <ul class="spec-list">'''
            for grade in precision_grades:
                specs_html += f'<li>{grade}</li>'
            specs_html += '''
                    </ul>
                </div>'''
        
        # Add materials if available
        materials = specs.get('materials', [])
        if materials:
            specs_html += f'''
                <div class="spec-card">
                    <h3 class="spec-title">Materials</h3>
                    <ul class="spec-list">'''
            for material in materials:
                specs_html += f'<li>{material}</li>'
            specs_html += '''
                    </ul>
                </div>'''
        
        # Add sealing options if available
        sealing_options = specs.get('sealing_options', [])
        if sealing_options:
            specs_html += f'''
                <div class="spec-card">
                    <h3 class="spec-title">Sealing Options</h3>
                    <ul class="spec-list">'''
            for option in sealing_options:
                specs_html += f'<li>{option}</li>'
            specs_html += '''
                    </ul>
                </div>'''
        
        specs_html += '''
            </div>
        </div>
    </section>'''
        
        return specs_html
    
    def generate_complete_page(self, series_key: str) -> str:
        """Generate the complete HTML page for a series"""
        series_data = self.get_series_data(series_key)
        if not series_data:
            print(f"❌ No data found for series: {series_key}")
            return ""
        
        # Generate page title and meta description
        series_name = series_data.get('series_name', '')
        description = series_data.get('description', '')
        
        # Create SEO-friendly title
        if series_key == 'miniature_bearings':
            title = "Miniature Ball Bearings | 3-9mm Bore | Ultra-Precision | RHD Bearings Mumbai"
            meta_desc = "Miniature ball bearings (604-699) for space-critical applications. 3-9mm bore, ultra-precision design. Made in India."
        elif series_key == '6800_series':
            title = "6800 Series Thin Section Light Ball Bearings | 3-100mm Bore | Ultra-Lightweight | RHD Bearings Mumbai"
            meta_desc = "6800 series ultra-thin section ball bearings (683-6820) for weight-sensitive applications. 3-100mm bore, ultra-lightweight design. Made in India."
        elif series_key == '6900_series':
            title = "6900 Series Thin Section Medium Ball Bearings | 3-100mm Bore | Medium-Duty | RHD Bearings Mumbai"
            meta_desc = "6900 series thin section ball bearings (693-6920) for compact applications. 3-100mm bore, medium-duty design. Made in India."
        else:
            # Extract series number for title
            series_match = re.search(r'(\d+)', series_name)
            if series_match:
                series_num = series_match.group(1)
                if 'heavy' in series_name.lower():
                    title = f"{series_num} Series Heavy Duty Ball Bearings | Enhanced Load Capacity | RHD Bearings Mumbai"
                    meta_desc = f"{series_num} series heavy-duty deep groove ball bearings for industrial, automotive, and commercial applications. Enhanced load capacity. Made in India."
                else:
                    title = f"{series_num} Series Deep Groove Ball Bearings | Industrial Applications | RHD Bearings Mumbai"
                    meta_desc = f"{series_num} series deep groove ball bearings for industrial, automotive, and commercial applications. Standard dimensions. Made in India."
            else:
                title = f"{series_name} | RHD Bearings Mumbai"
                meta_desc = f"{series_name} - {description[:100]}..."
        
        # Generate all sections
        hero_section = self.generate_hero_section(series_data, series_key)
        performance_grades = self.generate_performance_grades_section(series_data, series_key)
        applications = self.generate_applications_section(series_data)
        models = self.generate_models_section(series_data, series_key)
        specifications = self.generate_specifications_section(series_data)
        
        # Complete HTML page
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_desc}">
    
    <!-- External fonts first -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- CSS files -->
    <link rel="stylesheet" href="../shared/navbar.css">
    <link rel="stylesheet" href="../shared/footer.css">
    <link rel="stylesheet" href="../shared/watermark.css">
    <link rel="stylesheet" href="styles.css">
</head>
<body data-page="{series_key.replace('_series', '').replace('miniature_bearings', 'miniature')}">
    <!-- Navigation Header -->
    <div id="navbar-container"></div>

{hero_section}

{performance_grades}

{applications}

{models}

{specifications}

    <!-- Footer -->
    <div id="footer-container"></div>

    <!-- JavaScript -->
    <script src="../shared/navbar.js"></script>
    <script src="../shared/footer.js"></script>
</body>
</html>'''
        
        return html_content
    
    def generate_series_page(self, series_key: str) -> bool:
        """Generate HTML page for a specific series"""
        if series_key not in self.series_mapping:
            print(f"❌ Unknown series: {series_key}")
            return False
        
        # Get the output directory for this series
        series_dir = self.output_dir / self.series_mapping[series_key]
        series_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate the HTML content
        html_content = self.generate_complete_page(series_key)
        if not html_content:
            return False
        
        # Write the HTML file
        output_file = series_dir / "index.html"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ Generated {series_key} page: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error writing {series_key} page: {e}")
            return False
    
    def generate_all_series_pages(self) -> bool:
        """Generate HTML pages for all series"""
        if not self.load_json_data():
            return False
        
        success_count = 0
        failed_count = 0
        
        print(f"\n🚀 GENERATING SERIES PAGES FROM JSON")
        print(f"==================================================")
        
        for series_key in self.series_mapping.keys():
            print(f"\n🔧 Generating {series_key}...")
            success = self.generate_series_page(series_key)
            if success:
                success_count += 1
            else:
                failed_count += 1
        
        print(f"\n==================================================")
        print(f"📊 GENERATION SUMMARY")
        print(f"==================================================")
        print(f"✅ Successfully generated: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"🎯 Total: {success_count + failed_count}")
        
        if failed_count == 0:
            print(f"\n🎉 All series pages generated successfully!")
            return True
        else:
            print(f"\n⚠️  {failed_count} series page(s) failed. Check the errors above.")
            return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Generate HTML series pages from enhanced_bearing_series_pages.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 generate_series_pages_from_json.py                    # Generate all series pages
  python3 generate_series_pages_from_json.py --series 6200_series  # Generate specific series
  python3 generate_series_pages_from_json.py --output-dir custom/  # Custom output directory
        """
    )
    
    parser.add_argument(
        "--series",
        type=str,
        help="Generate specific series page (e.g., 6200_series, miniature_bearings)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="webpages",
        help="Output directory for generated pages (default: webpages)"
    )
    
    parser.add_argument(
        "--json-file",
        type=str,
        default="webpages/enhanced_bearing_series_pages.json",
        help="Path to enhanced_bearing_series_pages.json file"
    )
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = SeriesPageGenerator(args.json_file, args.output_dir)
    
    if args.series:
        # Generate specific series
        if not generator.load_json_data():
            return False
        
        success = generator.generate_series_page(args.series)
        if success:
            print(f"\n🎉 {args.series} page generated successfully!")
        else:
            print(f"\n❌ Failed to generate {args.series} page")
        return success
    else:
        # Generate all series
        return generator.generate_all_series_pages()


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
