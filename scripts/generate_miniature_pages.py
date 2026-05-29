#!/usr/bin/env python3
"""
Miniature Series Page Generator Script
=====================================

This script takes bearing JSON files from the models/ directory and generates
HTML pages in the appropriate miniature-series/ subdirectories.

DIRECTORY STRUCTURE & EXECUTION:
===============================
This script should be run from the ROOT WORKSPACE DIRECTORY (e.g., /Users/rdesai/Desktop/RHD GEO)

Expected directory structure:
├── models/                                    # Source JSON files for all bearing models
├── webpages/
│   ├── templates/
│   │   ├── index_new_claude.html            # HTML template for bearing pages
│   │   └── styles.css                       # Main CSS file for bearing pages
│   ├── shared/                              # Shared components (navbar, footer, CTA, watermark)
│   │   ├── navbar.css, navbar.html
│   │   ├── footer.css, footer.html
│   │   ├── cta-model.css, cta-model.html
│   │   └── watermark.css, watermark.html
│   └── MiniatureBearingsWebPage/
│       ├── index.html                       # Main miniature series page
│       ├── styles.css                       # Main page styles
│       └── internalpages/                   # Individual model pages (generated here)
│           ├── 604/
│           │   ├── index.html               # Generated HTML page
│           │   └── styles.css               # Copied CSS file
│           ├── 605/
│           └── ... (29 total model directories)
├── deployment/                               # Final deployment files
│   ├── miniature-series-internal-pages/     # Standalone pages with embedded CSS
│   │   ├── 604/
│   │   │   └── index.html                   # Standalone HTML with all CSS embedded
│   │   ├── 605/
│   │   └── ... (29 total model directories)
│   └── miniature-series/                    # Main page standalone version
│       └── index.html                       # Main page with embedded CSS
└── scripts/
    └── generate_miniature_pages.py          # This script

WORKFLOW STEPS:
===============
1. GENERATION: Read JSON from models/, create HTML pages in webpages/MiniatureBearingsWebPage/internalpages/
2. STANDALONE: Create standalone pages with embedded CSS in deployment/miniature-series-internal-pages/
3. UPLOAD: Upload standalone pages to server from deployment/ directory
4. MAIN PAGE: Process and upload main MiniatureBearingsWebPage

USAGE:
======
From ROOT WORKSPACE DIRECTORY:
- Complete workflow: python3 scripts/generate_miniature_pages.py
- Generate only: python3 scripts/generate_miniature_pages.py --generate-only
- Standalone only: python3 scripts/generate_miniature_pages.py --standalone-only
- Upload only: python3 scripts/generate_miniature_pages.py --upload-only
- Webpage only: python3 scripts/generate_miniature_pages.py --webpage-only

REQUIREMENTS:
=============
- .env file with FTP_PASSWORD
- deployment/curl_upload.py available
- All directories and files in expected locations
- Run from root workspace directory
"""

import json
import sys
import os
import re
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Import the curl_upload function from deployment/curl_upload.py
import importlib.util
spec = importlib.util.spec_from_file_location("curl_upload", "deployment/curl_upload.py")
curl_upload_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(curl_upload_module)
curl_upload = curl_upload_module.curl_upload

# Load environment variables for FTP credentials
load_dotenv()

class MiniaturePageGenerator:
    def __init__(self, json_file: str, template_file: str, output_file: str):
        self.json_file = json_file
        self.template_file = template_file
        self.output_file = output_file
        self.data = {}
        self.template_content = ""
        
    def load_json_data(self) -> bool:
        """Load bearing data from JSON file"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✅ Loaded JSON data from {self.json_file}")
            return True
        except Exception as e:
            print(f"❌ Error loading JSON file: {e}")
            return False
    
    def load_template(self) -> bool:
        """Load HTML template file"""
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                self.template_content = f.read()
            print(f"✅ Loaded HTML template from {self.template_file}")
            return True
        except Exception as e:
            print(f"❌ Error loading template file: {e}")
            return False
    
    def get_series_from_model(self, model_number):
        """
        Determine the series from the model number automatically.
        This avoids the need to edit JSON files.
        """
        if not model_number:
            return "miniature-series"  # Default fallback
            
        model_str = str(model_number)
        
        # Miniature series: 3-digit models starting with 6
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
        
        # Default fallback
        else:
            return "miniature-series"
    
    def convert_kn_to_kg(self, value, field_name=""):
        """
        Convert kN values to kg while keeping kN in parentheses for reference.
        
        Args:
            value: The value to process (string or number)
            field_name: The field name (kept for compatibility)
        
        Returns:
            Converted value in kg (kN) format, or original value if no conversion needed
        """
        # Skip conversion for load_ratings fields (keep them in kN)
        if 'load_ratings' in field_name:
            return str(value)
        
        # Convert string values containing kN
        if isinstance(value, str):
            # Look for patterns like "0.75kN" or "1.2 kN"
            import re
            kn_pattern = r'(\d+\.?\d*)\s*kN'
            match = re.search(kn_pattern, value)
            if match:
                kn_value = float(match.group(1))
                kg_value = round(kn_value * 102, 2)  # Convert kN to kg (1 kN = 102 kg)
                return value.replace(match.group(0), f"{kg_value}kg ({match.group(1)}kN)")
        
        # Convert numeric values that are likely kN (assuming values < 1000 are kN)
        if isinstance(value, (int, float)) and value < 1000:
            kg_value = round(value * 102, 2)  # Convert kN to kg
            return f"{kg_value}kg ({value}kN)"
        
        # Return original value if no conversion needed
        return str(value)
    
    def generate_page(self) -> bool:
        """Generate the complete HTML page"""
        try:
            # Load data and template
            if not self.load_json_data() or not self.load_template():
                return False
            
            content = self.template_content
            
            # 1. Replace grid class placeholder
            content = self._replace_grid_class(content)
            
            # 2. Replace conditional SKF dimensions
            content = self._replace_skf_conditionals(content)
            
            # 3. Replace clearance conditionals
            content = self._replace_clearance_conditionals(content)
            
            # 4. Replace applications
            content = self._replace_applications(content)
            
            # 5. Replace FAQs
            content = self._replace_faqs(content)
            
            # 6. Replace cross references
            content = self._replace_cross_references(content)
            
            # 7. Replace expertise signals
            content = self._replace_expertise_signals(content)
            
            # 8. Replace LLM optimization sections
            content = self._replace_llm_optimization_sections(content)
            
            # 9. Replace simple placeholders
            content = self._replace_simple_placeholders(content)

            # 9b. Fix broken breadcrumb series slug
            content = self._fix_breadcrumb_series(content)

            # 10. Inject BreadcrumbList + FAQPage structured data
            content = self._inject_structured_data(content)

            # Create output directory if it doesn't exist
            output_path = Path(self.output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the generated HTML
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Generated HTML page: {self.output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error generating page: {e}")
            return False
    
    def _replace_grid_class(self, content: str) -> str:
        """Replace the dynamic grid class placeholder"""
        skf_data = self.data.get('dimensions', {}).get('skf_extended_dimensions', {})
        has_skf_data = any(skf_data.values())
        
        if has_skf_data:
            content = content.replace('dimensions-grid-{{#if dimensions.skf_extended_dimensions.d1_shoulder_diameter}}3x2{{else}}3x1{{/if}}', 'dimensions-grid-3x2')
        else:
            content = content.replace('dimensions-grid-{{#if dimensions.skf_extended_dimensions.d1_shoulder_diameter}}3x2{{else}}3x1{{/if}}', 'dimensions-grid-3x1')
        
        return content
    
    def _replace_skf_conditionals(self, content: str) -> str:
        """Replace SKF conditional blocks"""
        skf_data = self.data.get('dimensions', {}).get('skf_extended_dimensions', {})
        has_skf_data = any(skf_data.values())
        
        if has_skf_data:
            # Remove the conditional markers but keep content
            content = re.sub(r'\{\{#if dimensions\.skf_extended_dimensions\.[^}]+\}\}', '', content)
            content = re.sub(r'\{\{/if\}\}', '', content)
        else:
            # Remove all SKF conditional blocks
            content = re.sub(r'\{\{#if dimensions\.skf_extended_dimensions\.[^}]+\}\}.*?\{\{/if\}\}', '', content, flags=re.DOTALL)
        
        return content
    
    def _replace_clearance_conditionals(self, content: str) -> str:
        """Replace clearance conditional blocks"""
        clearance_data = self.data.get('clearance', {})
        
        # Handle C4 conditional
        if clearance_data.get('C4', {}).get('min_microns'):
            # Remove the conditional markers but keep content
            content = re.sub(r'\{\{#clearance\.C4\.min_microns\}\}', '', content)
            content = re.sub(r'\{\{/clearance\.C4\.min_microns\}\}', '', content)
        else:
            # Remove the entire C4 conditional block
            content = re.sub(r'\{\{#clearance\.C4\.min_microns\}\}.*?\{\{/clearance\.C4\.min_microns\}\}', '', content, flags=re.DOTALL)
        
        # Handle C5 conditional
        if clearance_data.get('C5', {}).get('min_microns'):
            # Remove the conditional markers but keep content
            content = re.sub(r'\{\{#clearance\.C5\.min_microns\}\}', '', content)
            content = re.sub(r'\{\{/clearance\.C5\.min_microns\}\}', '', content)
        else:
            # Remove the entire C5 conditional block
            content = re.sub(r'\{\{#clearance\.C5\.min_microns\}\}.*?\{\{/clearance\.C5\.min_microns\}\}', '', content, flags=re.DOTALL)
        
        return content
    
    def _replace_applications(self, content: str) -> str:
        """Replace applications placeholders"""
        applications = self.data.get('applications', {})
        
        for i in range(1, 4):
            app_key = f"application{i}"
            if app_key in applications:
                app_data = applications[app_key]
                
                # Replace title and requirements (without kN to kg conversion)
                title = app_data.get('title', '')
                requirements = app_data.get('requirements', '')
                
                content = content.replace(f"{{{{applications.{app_key}.title}}}}", title)
                content = content.replace(f"{{{{applications.{app_key}.requirements}}}}", requirements)
                
                # Replace applications list
                app_list = app_data.get('applications', [])
                app_list_html = '\n'.join([f'<li>{item}</li>' for item in app_list])
                
                # Find and replace the loop
                loop_pattern = f"{{{{#applications.{app_key}.applications}}}}.*?{{{{/applications.{app_key}.applications}}}}"
                replacement = app_list_html
                
                content = re.sub(loop_pattern, replacement, content, flags=re.DOTALL)
        
        return content
    
    def _replace_faqs(self, content: str) -> str:
        """Replace FAQ placeholders"""
        faqs = self.data.get('faqs', {})
        
        for category_key, category_data in faqs.items():
            if category_key in ['selection_replacement', 'installation_maintenance', 'troubleshooting', 'cost_performance']:
                # Replace category title
                content = content.replace(f"{{{{faqs.{category_key}.title}}}}", category_data.get('title', ''))
                
                # Generate questions HTML
                questions = category_data.get('questions', [])
                questions_html = ""
                for question_data in questions:
                    # Convert kN to kg in FAQ content using the function
                    question = question_data.get('question', '')
                    direct_answer = self.convert_kn_to_kg(question_data.get('direct_answer', ''), f"faqs.{category_key}.questions.direct_answer")
                    why_matters = self.convert_kn_to_kg(question_data.get('why_matters', ''), f"faqs.{category_key}.questions.why_matters")
                    how_to_handle = self.convert_kn_to_kg(question_data.get('how_to_handle', ''), f"faqs.{category_key}.questions.how_to_handle")
                    pro_tip = self.convert_kn_to_kg(question_data.get('pro_tip', ''), f"faqs.{category_key}.questions.pro_tip")
                    
                    question_html = f"""
                        <div class="faq-question">
                            <h4 class="faq-question-title">{question}</h4>
                            <div class="faq-direct-answer">{direct_answer}</div>
                            
                            <div class="faq-section">
                                <div class="faq-section-title">Why This Matters</div>
                                <div class="faq-section-content">{why_matters}</div>
                            </div>
                            
                            <div class="faq-section">
                                <div class="faq-section-title">How To Handle It</div>
                                <div class="faq-section-content">{how_to_handle}</div>
                            </div>
                            
                            <div class="faq-pro-tip">{pro_tip}</div>
                        </div>
                        """
                    questions_html += question_html
                
                # Replace the questions loop
                loop_pattern = f"{{{{#faqs.{category_key}.questions}}}}.*?{{{{/faqs.{category_key}.questions}}}}"
                content = re.sub(loop_pattern, questions_html, content, flags=re.DOTALL)
        
        return content
    
    def _replace_cross_references(self, content: str) -> str:
        """Replace cross references placeholders"""
        cross_refs = self.data.get('cross_references', {})
        
        # Related models - generate proper URLs with dimensions loaded from JSON files
        related_models = cross_refs.get('related_models', [])
        if related_models:
            models_html = '\n'.join([
                f'<a href="https://rhdbearings.com/specs/{self.get_series_from_model(model)}/{model}/" class="model-link">{model} ({self._get_model_dimensions(model)})</a>' 
                for model in related_models
            ])
            content = re.sub(r'\{\{#cross_references\.related_models\}\}.*?\{\{/cross_references\.related_models\}\}', models_html, content, flags=re.DOTALL)
        
        # Shaft requirements - handle individual fields
        shaft_reqs = cross_refs.get('shaft_requirements', {})
        if shaft_reqs:
            # Replace individual shaft requirement placeholders
            content = content.replace('{{cross_references.shaft_requirements.nominal_diameter}}', str(shaft_reqs.get('nominal_diameter', '')))
            content = content.replace('{{cross_references.shaft_requirements.tolerance_grade}}', str(shaft_reqs.get('tolerance_grade', '')))
            content = content.replace('{{cross_references.shaft_requirements.surface_finish}}', str(shaft_reqs.get('surface_finish', '')))
            content = content.replace('{{cross_references.shaft_requirements.runout_tolerance}}', str(shaft_reqs.get('runout_tolerance', '')))
        
        # Application specific alternatives - handle individual fields
        app_alternatives = cross_refs.get('application_specific_alternatives', {})
        if app_alternatives:
            # Replace individual alternative placeholders
            content = content.replace('{{cross_references.application_specific_alternatives.high_temperature}}', str(app_alternatives.get('high_temperature', '')))
            content = content.replace('{{cross_references.application_specific_alternatives.high_speed}}', str(app_alternatives.get('high_speed', '')))
            content = content.replace('{{cross_references.application_specific_alternatives.corrosive_environment}}', str(app_alternatives.get('corrosive_environment', '')))
                
        return content
    
    def _replace_expertise_signals(self, content: str) -> str:
        """Replace expertise signals placeholders"""
        expertise_signals = self.data.get('llm_optimization', {}).get('expertise_signals', [])
        
        if expertise_signals:
            expertise_html = '\n'.join([f'<div class="expertise-card"><h3><span class="expertise-icon">{signal.get("icon", "")}</span>{signal.get("title", "")}</h3><p>{signal.get("description", "")}</p></div>' for signal in expertise_signals])
            content = re.sub(r'\{\{#llm_optimization\.expertise_signals\}\}.*?\{\{/llm_optimization\.expertise_signals\}\}', expertise_html, content, flags=re.DOTALL)
        
        return content
    
    def _replace_llm_optimization_sections(self, content: str) -> str:
        """Replace all LLM optimization section placeholders"""
        
        # Replace Search Optimization Tags
        natural_language_queries = self.data.get('llm_optimization', {}).get('natural_language_queries', [])
        if natural_language_queries:
            search_tags_html = '\n'.join([
                f'<span class="search-tag">{query}</span>' 
                for query in natural_language_queries
            ])
            content = re.sub(r'\{\{#llm_optimization\.natural_language_queries\}\}.*?\{\{/llm_optimization\.natural_language_queries\}\}', search_tags_html, content, flags=re.DOTALL)
        else:
            # Remove the entire search optimization section if no queries
            content = re.sub(r'<!-- Search Optimization Tags -->.*?<!-- Dimensions and Image Section -->', '<!-- Dimensions and Image Section -->', content, flags=re.DOTALL)
        
        return content
    
    def _replace_simple_placeholders(self, content: str) -> str:
        """Replace simple {{key}} placeholders"""
        # Handle keywords array
        if 'seo_metadata' in self.data and 'keywords' in self.data['seo_metadata']:
            keywords = self.data['seo_metadata']['keywords']
            if isinstance(keywords, list):
                keywords_string = ', '.join(keywords)
                content = content.replace('{{seo_metadata.keywords_string}}', keywords_string)
        
        # Handle alternate_model_number placeholder - remove it if it doesn't exist in data
        if 'alternate_model_number' not in self.data:
            content = content.replace('{{alternate_model_number}}', '')
        
        # Create a mapping for old field names to new field names
        field_mapping = {
            'd': 'bore_diameter_d_mm',
            'D': 'outer_diameter_D_mm', 
            'B': 'width_B_mm',
            'Cr': 'dynamic_load_Cr_kN',
            'Cor': 'static_load_Cor_kN',
            'weight': 'weight_kg'
        }
        
        # Replace all other placeholders, but EXCLUDE FAQ content to preserve kN to kg conversion
        for key, value in self._flatten_dict(self.data).items():
            # Skip FAQ content to preserve the kN to kg conversion done in _replace_faqs
            if key.startswith('faqs.'):
                continue
                
            placeholder = f"{{{{{key}}}}}"
            if placeholder in content:
                if value is None:
                    content = content.replace(placeholder, "N/A")
                else:
                    # Use original value without conversion
                    content = content.replace(placeholder, str(value))
        
        # Also replace old field name placeholders with new field values
        for old_name, new_name in field_mapping.items():
            if new_name in self.data.get('dimensions', {}):
                old_placeholder = f"{{{{{old_name}}}}}"
                new_value = self.data['dimensions'][new_name]
                if old_placeholder in content:
                    # Use original value without conversion
                    content = content.replace(old_placeholder, str(new_value))
            elif new_name in self.data.get('load_ratings', {}):
                old_placeholder = f"{{{{{old_name}}}}}"
                new_value = self.data['load_ratings'][new_name]
                if old_placeholder in content:
                    # Use original value without conversion
                    content = content.replace(old_placeholder, str(new_value))
        
        return content
    
    def _get_model_dimensions(self, model_number: str) -> str:
        """Get dimensions for a related model by loading its JSON file"""
        try:
            # Construct the path to the model's JSON file
            json_file = Path(self.json_file).parent / f"{model_number}.json"
            
            if json_file.exists():
                with open(json_file, 'r', encoding='utf-8') as f:
                    model_data = json.load(f)
                
                dimensions = model_data.get('dimensions', {})
                bore = dimensions.get('bore_diameter_d_mm', 'N/A')
                outer = dimensions.get('outer_diameter_D_mm', 'N/A')
                width = dimensions.get('width_B_mm', 'N/A')
                
                return f"{bore}×{outer}×{width}mm"
            else:
                # Fallback to placeholder if JSON file doesn't exist
                return "dimensions"
                
        except Exception as e:
            print(f"⚠️ Warning: Could not load dimensions for model {model_number}: {e}")
            return "dimensions"
    
    def _flatten_dict(self, d: dict, parent_key: str = '', sep: str = '.') -> dict:
        """Flatten nested dictionary for easier placeholder replacement"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def _series_slug(self) -> str:
        """Resolve the series URL slug from the canonical URL (source of truth)."""
        canonical = self.data.get('seo_metadata', {}).get('canonical_url', '') or ''
        if '/specs/' in canonical:
            slug = canonical.split('/specs/')[1].split('/')[0]
            if slug:
                return slug
        return str(self.data.get('bearing_series_name') or 'miniature-series')

    def _fix_breadcrumb_series(self, content: str) -> str:
        """Resolve the {{bearing_series}} placeholder (otherwise a broken link)."""
        return content.replace('{{bearing_series}}', self._series_slug())

    def _inject_structured_data(self, content: str) -> str:
        """Build BreadcrumbList + FAQPage JSON-LD and inject at {{ADDITIONAL_JSONLD}}."""
        import json as _json
        website = self.data.get('company_metadata', {}).get('website', 'https://rhdbearings.com')
        slug = self._series_slug()
        series_name = str(self.data.get('bearing_series_name') or slug)
        model = str(self.data.get('model_number', ''))
        canonical = self.data.get('seo_metadata', {}).get('canonical_url', '') \
            or f"{website}/specs/{slug}/{model}/"

        blocks = [{
            "@context": "https://schema.org/",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{website}/"},
                {"@type": "ListItem", "position": 2, "name": series_name,
                 "item": f"{website}/specs/{slug}/"},
                {"@type": "ListItem", "position": 3, "name": f"{model} Bearing",
                 "item": canonical},
            ],
        }]

        faq_entities = []
        for category_key, category_data in self.data.get('faqs', {}).items():
            if category_key not in ['selection_replacement', 'installation_maintenance',
                                    'troubleshooting', 'cost_performance']:
                continue
            for q in category_data.get('questions', []):
                question = q.get('question', '')
                if not question:
                    continue
                parts = []
                da = self.convert_kn_to_kg(q.get('direct_answer', ''), f"faqs.{category_key}.questions.direct_answer")
                wm = self.convert_kn_to_kg(q.get('why_matters', ''), f"faqs.{category_key}.questions.why_matters")
                hh = self.convert_kn_to_kg(q.get('how_to_handle', ''), f"faqs.{category_key}.questions.how_to_handle")
                pt = self.convert_kn_to_kg(q.get('pro_tip', ''), f"faqs.{category_key}.questions.pro_tip")
                if da:
                    parts.append(da)
                if wm:
                    parts.append(wm)
                if hh:
                    parts.append(hh)
                if pt:
                    parts.append(f"Pro tip: {pt}")
                answer = ' '.join(p.strip() for p in parts if p).strip()
                if not answer:
                    continue
                faq_entities.append({
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {"@type": "Answer", "text": answer},
                })
        if faq_entities:
            blocks.append({
                "@context": "https://schema.org/",
                "@type": "FAQPage",
                "mainEntity": faq_entities,
            })

        scripts = '\n'.join(
            f'<script type="application/ld+json">\n{_json.dumps(b, ensure_ascii=False, indent=2)}\n</script>'
            for b in blocks
        )
        return content.replace('{{ADDITIONAL_JSONLD}}', scripts)

def generate_miniature_pages():
    """
    STEP 1: Generate HTML pages from JSON files
    
    This function:
    1. Scans the models/ directory for all JSON files
    2. Filters for 3-digit models starting with '6' (604, 605, 606, etc.)
    3. Generates HTML pages using the template from webpages/templates/index_new_claude.html
    4. Outputs pages to webpages/MiniatureBearingsWebPage/internalpages/
    5. Copies styles.css to each model directory for proper styling
    
    Input: models/*.json files
    Output: webpages/MiniatureBearingsWebPage/internalpages/[model]/index.html + styles.css
    """
    models_dir = Path("models")
    template_file = Path("webpages/templates/index_new_claude.html")
    output_base_dir = Path("webpages/MiniatureBearingsWebPage/internalpages")
    
    # Check if required files exist
    if not models_dir.exists():
        print(f"❌ Models directory not found: {models_dir}")
        return False
    
    if not template_file.exists():
        print(f"❌ Template file not found: {template_file}")
        return False
    
    # Create output directory
    output_base_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all JSON files
    all_json_files = list(models_dir.glob("*.json"))
    if not all_json_files:
        print(f"❌ No JSON files found in {models_dir}")
        return False
    
    print(f"🔍 SCANNING MODELS DIRECTORY")
    print(f"📋 Found {len(all_json_files)} total JSON files")
    
    miniature_models = []
    skipped_models = []
    
    for json_file in all_json_files:
        model_name = json_file.stem
        
        if model_name.startswith('6') and len(model_name) == 3:
            miniature_models.append(json_file)
            print(f"   ✅ MINIATURE: {model_name} (3-digit, starts with 6)")
        else:
            skipped_models.append(json_file)
            if not model_name.startswith('6'):
                print(f"   ⏭️  SKIP: {model_name} (doesn't start with 6)")
            elif len(model_name) != 3:
                print(f"   ⏭️  SKIP: {model_name} (not 3 digits, has {len(model_name)} digits)")
            else:
                print(f"   ⏭️  SKIP: {model_name} (unknown reason)")
    
    print(f"\n📊 FILTERING RESULTS:")
    print(f"   ✅ MINIATURE SERIES: {len(miniature_models)} models")
    print(f"   ⏭️  SKIPPED: {len(skipped_models)} models")
    print(f"   📋 TOTAL PROCESSED: {len(all_json_files)} models")
    
    if not miniature_models:
        print(f"\n❌ No miniature series models found in {models_dir}")
        print(f"   Miniature series models should be 3-digit numbers starting with 6 (e.g., 604, 605, 608)")
        return False
    
    print(f"\n🚀 GENERATING MINIATURE SERIES PAGES ONLY")
    print(f"==================================================")
    print(f"📁 Template: {template_file}")
    print(f"📁 Output base: {output_base_dir}")
    print(f"==================================================")
    
    print(f"\n🎯 MODELS TO PROCESS:")
    model_names = [f.stem for f in miniature_models]
    model_names.sort()
    for i, model in enumerate(model_names, 1):
        print(f"   {i:2d}. {model}")
    print(f"==================================================")
    
    success_count = 0
    failed_count = 0
    
    for json_file in miniature_models:
        model_name = json_file.stem
        output_dir = output_base_dir / model_name
        output_dir.mkdir(exist_ok=True)
        
        print(f"\n🔧 Generating page for miniature model {model_name}...")
        print(f"   📁 Output: {output_dir}/index.html")
        
        try:
            # Use the built-in MiniaturePageGenerator class
            output_file = output_dir / "index.html"
            generator = MiniaturePageGenerator(str(json_file), str(template_file), str(output_file))
            
            success = generator.generate_page()
            
            if success:
                # Copy styles.css to the model directory
                styles_source = Path("webpages/templates/styles.css")
                styles_dest = output_dir / "styles.css"
                if styles_source.exists():
                    import shutil
                    shutil.copy2(styles_source, styles_dest)
                    print(f"   ✅ Successfully generated {model_name} page")
                    print(f"   📁 Copied styles.css to {model_name}/")
                    success_count += 1
                else:
                    print(f"   ⚠️  Generated {model_name} page but styles.css not found")
                    success_count += 1
            else:
                print(f"   ❌ Failed to generate {model_name} page")
                failed_count += 1
                
        except Exception as e:
            print(f"   ❌ Error generating {model_name} page: {e}")
            failed_count += 1
    
    print(f"\n==================================================")
    print(f"📊 GENERATION SUMMARY")
    print(f"==================================================")
    print(f"✅ Successfully generated: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"🎯 Total: {len(miniature_models)}")
    
    if failed_count == 0:
        print(f"\n🎉 All {len(miniature_models)} miniature series pages generated successfully!")
        print(f"📁 Pages are ready in {output_base_dir}/")
        return True
    else:
        print(f"\n⚠️  {failed_count} page(s) failed to generate. Check the errors above.")
        return False

def create_standalone_pages():
    """
    STEP 2: Create standalone pages with embedded CSS
    
    This function:
    1. Reads the generated HTML pages from webpages/MiniatureBearingsWebPage/internalpages/
    2. Embeds all shared CSS (navbar, footer, CTA, watermark) directly into the HTML
    3. Embeds the main styles.css content for complete styling
    4. Creates completely standalone HTML files with no external dependencies
    5. Outputs to deployment/miniature-series-internal-pages/
    
    Input: webpages/MiniatureBearingsWebPage/internalpages/[model]/index.html + styles.css
    Output: deployment/miniature-series-internal-pages/[model]/index.html (standalone)
    """
    print(f"\n🚀 CREATING STANDALONE PAGES")
    print(f"==================================================")
    
    miniature_base_dir = Path("webpages/MiniatureBearingsWebPage/internalpages")
    if not miniature_base_dir.exists():
        print(f"❌ Miniature base directory not found: {miniature_base_dir}")
        print("💡 Make sure to run generate_miniature_pages() first")
        return False
    
    # Get all model directories
    model_dirs = [d for d in miniature_base_dir.iterdir() if d.is_dir()]
    if not model_dirs:
        print(f"❌ No model directories found in {miniature_base_dir}")
        print("💡 Make sure to run generate_miniature_pages() first")
        return False
    
    print(f"📋 Found {len(model_dirs)} model directories to process")
    
    failed_count = 0
    successful_count = 0
    
    for model_dir in model_dirs:
        model_name = model_dir.name
        print(f"\n🔧 Creating standalone page for {model_name}...")
        
        try:
            success = create_standalone_model_page(model_name, model_dir)
            if success:
                print(f"   ✅ Successfully created standalone page for {model_name}")
                successful_count += 1
            else:
                print(f"   ❌ Failed to create standalone page for {model_name}")
                failed_count += 1
                
        except Exception as e:
            print(f"   ❌ Error processing {model_name}: {e}")
            failed_count += 1
    
    print(f"\n==================================================")
    print(f"📊 STANDALONE PAGE CREATION SUMMARY")
    print(f"==================================================")
    print(f"✅ Successfully created: {successful_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"🎯 Total: {len(model_dirs)}")
    
    if failed_count == 0:
        print(f"\n🎉 All {successful_count} standalone pages created successfully!")
        print(f"📁 Pages are ready in deployment/miniature-series-internal-pages/")
        return True
    else:
        print(f"\n⚠️  {failed_count} page(s) failed to create. Check the errors above.")
        return False

def extract_seo_head_tags(html_content: str) -> str:
    """Extract SEO / structured-data tags (meta description/keywords/robots,
    canonical, Open Graph, Twitter, and all JSON-LD scripts) from a generated
    page's <head>, so they can be carried over to the standalone deploy page."""
    import re as _re
    head_match = _re.search(r'<head[^>]*>(.*?)</head>', html_content,
                            _re.DOTALL | _re.IGNORECASE)
    if not head_match:
        return ""
    head_inner = head_match.group(1)
    parts = []
    parts += _re.findall(
        r'<meta\s+name=["\'](?:description|keywords|robots)["\'][^>]*>',
        head_inner, _re.IGNORECASE)
    parts += _re.findall(r'<link\s+rel=["\']canonical["\'][^>]*>',
                         head_inner, _re.IGNORECASE)
    parts += _re.findall(r'<meta\s+property=["\']og:[^"\']*["\'][^>]*>',
                         head_inner, _re.IGNORECASE)
    parts += _re.findall(r'<meta\s+name=["\']twitter:[^"\']*["\'][^>]*>',
                         head_inner, _re.IGNORECASE)
    parts += _re.findall(
        r'<script\s+type=["\']application/ld\+json["\'][^>]*>.*?</script>',
        head_inner, _re.DOTALL | _re.IGNORECASE)
    if not parts:
        return ""
    return "    " + "\n    ".join(tag.strip() for tag in parts)


def create_standalone_model_page(model_name, model_dir):
    """
    Helper function for create_standalone_pages()
    
    This function:
    1. Reads the HTML content from a specific model directory
    2. Reads and embeds all shared CSS files (navbar, footer, CTA, watermark)
    3. Reads and embeds the main styles.css for the specific model
    4. Replaces component placeholders with actual HTML content
    5. Creates a completely standalone HTML file with all CSS embedded
    
    Input: model_dir/index.html + styles.css + shared components
    Output: deployment/miniature-series-internal-pages/[model]/index.html (standalone)
    """
    try:
        # Load model dimensions for proper title
        model_dimensions = "Bearing"
        try:
            json_file = Path("models") / f"{model_name}.json"
            if json_file.exists():
                with open(json_file, 'r', encoding='utf-8') as f:
                    model_data = json.load(f)
                
                dimensions = model_data.get('dimensions', {})
                bore = dimensions.get('bore_diameter_d_mm', 'N/A')
                outer = dimensions.get('outer_diameter_D_mm', 'N/A')
                width = dimensions.get('width_B_mm', 'N/A')
                
                if bore != 'N/A' and outer != 'N/A' and width != 'N/A':
                    model_dimensions = f"Bearing {bore}×{outer}×{width}mm"
        except:
            pass  # Use fallback if dimensions can't be loaded
        # Read the generated HTML file
        index_file = model_dir / "index.html"
        if not index_file.exists():
            print(f"      ❌ index.html not found in {model_dir}")
            return False
        
        with open(index_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Carry SEO/structured-data tags from the generated head into the standalone page
        seo_head = extract_seo_head_tags(html_content)
        
        # Read shared CSS files
        shared_dir = Path("webpages/shared")
        navbar_css = ""
        footer_css = ""
        cta_css = ""
        watermark_css = ""
        
        # Read the main styles.css file
        styles_css = ""
        try:
            styles_file = model_dir / "styles.css"
            with open(styles_file, 'r', encoding='utf-8') as f:
                styles_css = f.read()
        except:
            print(f"      ⚠️  styles.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "navbar.css", 'r', encoding='utf-8') as f:
                navbar_css = f.read()
        except:
            print(f"      ⚠️  navbar.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "footer.css", 'r', encoding='utf-8') as f:
                footer_css = f.read()
        except:
            print(f"      ⚠️  footer.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "cta-model.css", 'r', encoding='utf-8') as f:
                cta_css = f.read()
        except:
            print(f"      ⚠️  cta-model.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "watermark.css", 'r', encoding='utf-8') as f:
                watermark_css = f.read()
        except:
            print(f"      ⚠️  watermark.css not found, using empty CSS")
        
        # Read shared HTML files
        navbar_html = ""
        footer_html = ""
        cta_html = ""
        watermark_html = ""
        
        try:
            with open(shared_dir / "navbar.html", 'r', encoding='utf-8') as f:
                navbar_html = f.read()
                # Remove script tag from navbar
                script_start = navbar_html.find('<script>')
                if script_start != -1:
                    navbar_html = navbar_html[:script_start].strip()
        except:
            print(f"      ⚠️  navbar.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "footer.html", 'r', encoding='utf-8') as f:
                footer_html = f.read()
        except:
            print(f"      ⚠️  footer.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "cta-model.html", 'r', encoding='utf-8') as f:
                cta_html = f.read()
                # Replace [MODEL] placeholder with actual model number
                cta_html = cta_html.replace('[MODEL]', model_name)
        except:
            print(f"      ⚠️  cta-model.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "watermark.html", 'r', encoding='utf-8') as f:
                watermark_html = f.read()
        except:
            print(f"      ⚠️  watermark.html not found, using empty HTML")
        
        # Extract body content and scripts
        body_start = html_content.find('<body')
        if body_start == -1:
            print(f"      ❌ No <body> tag found in HTML")
            return False
        
        body_start = body_start + html_content[body_start:].find('>') + 1
        body_end = html_content.find('</body>')
        if body_end == -1:
            print(f"      ❌ No </body> tag found in HTML")
            return False
        
        body_content = html_content[body_start:body_end].strip()
        
        # Extract script content
        script_content = ""
        current_pos = 0
        while True:
            script_start = html_content.find('<script>', current_pos)
            if script_start == -1:
                break
            script_end = html_content.find('</script>', script_start) + len('</script>')
            script_content += html_content[script_start:script_end] + "\n"
            current_pos = script_end
        
        # Replace image with remote URL
        body_content = body_content.replace('src="DGBB.png"', 'src="https://rhdbearings.com/wp-content/uploads/2025/08/DGBB.png"')
        
        # Replace navbar container with actual navbar HTML
        body_content = body_content.replace('<div id="navbar-container"></div>', navbar_html)
        
        # Replace component containers with actual HTML
        body_content = body_content.replace('<div id="cta-container"></div>', cta_html)
        if 'id="footer-container"' in body_content:
            body_content = body_content.replace('<div id="footer-container"></div>', footer_html)
        if 'id="watermark-container"' in body_content:
            body_content = body_content.replace('<div id="watermark-container"></div>', watermark_html)
        
        # Remove all fetch calls and problematic patterns
        import re
        
        # Remove complete fetch blocks for shared components (fetch + .then() chains)
        # This handles multi-line fetch blocks with various formatting
        body_content = re.sub(r'fetch\([\'"][^\'"]*\.\./shared/[^\'"]*[\'"]\)[\s\S]*?\.then\([^{]*\{[\s\S]*?\}\);', '// Component loading removed - HTML already embedded', body_content)
        
         # Remove fetch calls to shared components
        body_content = re.sub(r'fetch\([\'"][^\'"]*\.\./shared/[^\'"]*[\'"]\)', '// fetch call removed - component already embedded', body_content)
        
        # Remove script blocks that load shared components
        body_content = re.sub(r'<script>[^<]*fetch\([^<]*\.\./shared/[^<]*</script>', '<!-- Shared component loading script removed -->', body_content, flags=re.DOTALL)
        
        # Remove any remaining references to ../shared/ paths
        body_content = body_content.replace('../shared/', '// shared path removed - components embedded')
        
        # Remove console.error calls related to failed fetches
        body_content = re.sub(r'console\.error\([^)]*\)', '// error logging removed', body_content)
        
        # Clean up empty script tags
        body_content = re.sub(r'<script>\s*</script>', '', body_content)
        
        # Create standalone HTML
        standalone_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{model_name} {model_dimensions} | RHD Bearings</title>
{seo_head}
    <link href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
/* Reset and base styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Bai Jamjuree', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #000;
    background: #F8F9FA;
}}

/* Navbar CSS */
{navbar_css}

/* Footer CSS */
{footer_css}

/* CTA CSS */
{cta_css}

/* Watermark CSS */
{watermark_css}

/* Main Page Styles */
{styles_css}
    </style>
</head>
<body>
{body_content}
{script_content}
</body>
</html>'''
        
        # Create deployment directory
        deployment_dir = Path("deployment/miniature-series-internal-pages")
        deployment_dir.mkdir(parents=True, exist_ok=True)
        
        # Save standalone page
        output_file = deployment_dir / model_name / "index.html"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(standalone_html)
        
        print(f"      ✅ Created standalone page: {output_file}")
        return True
        
    except Exception as e:
        print(f"      ❌ Error creating standalone page: {e}")
        return False

def create_standalone_miniature_webpage():
    """
    Helper function for process_miniature_webpage()
    
    This function:
    1. Reads the main MiniatureBearingsWebPage index.html and styles.css
    2. Embeds shared components (navbar, footer, CTA, watermark)
    3. Creates a standalone version of the main page
    4. Outputs to deployment/miniature-series/index.html
    
    Input: webpages/MiniatureBearingsWebPage/index.html + styles.css + shared components
    Output: deployment/miniature-series/index.html (standalone)
    """
    try:
        # Source directory (MiniatureBearingsWebPage)
        source_dir = Path("webpages/MiniatureBearingsWebPage")
        source_index = source_dir / "index.html"
        source_styles = source_dir / "styles.css"
        
        # Read source files
        with open(source_index, 'r', encoding='utf-8') as f:
            html_content = f.read()
        with open(source_styles, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Read shared CSS files
        shared_dir = Path("webpages/shared")
        navbar_css = ""
        footer_css = ""
        cta_css = ""
        watermark_css = ""
        
        try:
            with open(shared_dir / "navbar.css", 'r', encoding='utf-8') as f:
                navbar_css = f.read()
        except:
            print(f"      ⚠️  navbar.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "footer.css", 'r', encoding='utf-8') as f:
                footer_css = f.read()
        except:
            print(f"      ⚠️  footer.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "cta-model.css", 'r', encoding='utf-8') as f:
                cta_css = f.read()
        except:
            print(f"      ⚠️  cta-model.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "watermark.css", 'r', encoding='utf-8') as f:
                watermark_css = f.read()
        except:
            print(f"      ⚠️  watermark.css not found, using empty CSS")
        
        # Read shared HTML files
        navbar_html = ""
        footer_html = ""
        cta_html = ""
        watermark_html = ""
        
        try:
            with open(shared_dir / "navbar.html", 'r', encoding='utf-8') as f:
                navbar_html = f.read()
                # Remove script tag from navbar
                script_start = navbar_html.find('<script>')
                if script_start != -1:
                    navbar_html = navbar_html[:script_start].strip()
        except:
            print(f"      ⚠️  navbar.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "footer.html", 'r', encoding='utf-8') as f:
                footer_html = f.read()
        except:
            print(f"      ⚠️  footer.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "cta-model.html", 'r', encoding='utf-8') as f:
                cta_html = f.read()
        except:
            print(f"      ⚠️  cta-model.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "watermark.html", 'r', encoding='utf-8') as f:
                watermark_html = f.read()
        except:
            print(f"      ⚠️  watermark.html not found, using empty HTML")
        
        # Extract body content
        body_start = html_content.find('<body')
        if body_start == -1:
            print(f"      ❌ No <body> tag found in HTML")
            return False
        
        body_start = body_start + html_content[body_start:].find('>') + 1
        body_end = html_content.find('</body>')
        if body_end == -1:
            print(f"      ❌ No </body> tag found in HTML")
            return False
        
        body_content = html_content[body_start:body_end].strip()
        
        # Extract script content
        script_content = ""
        current_pos = 0
        while True:
            script_start = html_content.find('<script>', current_pos)
            if script_start == -1:
                break
            script_end = html_content.find('</script>', script_start) + len('</script>')
            script_content += html_content[script_start:script_end] + "\n"
            current_pos = script_end
        
        # Replace image with remote URL
        body_content = body_content.replace('src="DGBB.png"', 'src="https://rhdbearings.com/wp-content/uploads/2025/08/DGBB.png"')
        
        # Replace navbar container with actual navbar HTML
        body_content = body_content.replace('<div id="navbar-container"></div>', navbar_html)
        
        # Replace component containers with actual HTML
        body_content = body_content.replace('<div id="cta-container"></div>', cta_html)
        if 'id="footer-container"' in body_content:
            body_content = body_content.replace('<div id="footer-container"></div>', footer_html)
        if 'id="watermark-container"' in body_content:
            body_content = body_content.replace('<div id="watermark-container"></div>', watermark_html)
        
        # Remove all fetch calls and problematic patterns
        import re
        
        # Remove complete fetch blocks for shared components (fetch + .then() chains)
        # This handles multi-line fetch blocks with various formatting
        body_content = re.sub(r'fetch\([\'"][^\'"]*\.\./shared/[^\'"]*[\'"]\)[\s\S]*?\.then\([^{]*\{[\s\S]*?\}\);', '// Component loading removed - HTML already embedded', body_content)
        
        # Remove fetch calls to shared components
        body_content = re.sub(r'fetch\([\'"][^\'"]*\.\./shared/[^\'"]*[\'"]\)', '// fetch call removed - component already embedded', body_content)
        
        # Remove script blocks that load shared components
        body_content = re.sub(r'<script>[^<]*fetch\([^<]*\.\./shared/[^<]*</script>', '<!-- Shared component loading script removed -->', body_content, flags=re.DOTALL)
        
        # Remove any remaining references to ../shared/ paths
        body_content = body_content.replace('../shared/', '// shared path removed - components embedded')
        
        # Remove console.error calls related to failed fetches
        body_content = re.sub(r'console\.error\([^)]*\)', '// error logging removed', body_content)
        
        # Clean up empty script tags
        body_content = re.sub(r'<script>\s*</script>', '', body_content)
        
        # Create standalone HTML
        standalone_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Miniature Ball Bearings | RHD Bearings</title>
    <link href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
/* Reset and base styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Bai Jamjuree', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #000;
    background: #F8F9FA;
}}

/* Navbar CSS */
{navbar_css}

/* Footer CSS */
{footer_css}

/* CTA CSS */
{cta_css}

/* Watermark CSS */
{watermark_css}

/* Page CSS */
{css_content}
    </style>
</head>
<body>
{body_content}
{script_content}
</body>
</html>'''
        
        # Create deployment directory
        deployment_dir = Path("deployment/miniature-series")
        deployment_dir.mkdir(parents=True, exist_ok=True)
        
        # Save standalone page
        output_file = deployment_dir / "index.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(standalone_html)
        
        print(f"      ✅ Created standalone page: {output_file}")
        return True
        
    except Exception as e:
        print(f"      ❌ Error creating standalone page: {e}")
        return False

def upload_pages():
    """
    STEP 3: Upload standalone pages to server
    
    This function:
    1. Reads standalone HTML files from deployment/miniature-series-internal-pages/
    2. Uploads each model page to the server using curl FTP
    3. Creates proper directory structure on server: specs/miniature-series/[model]/
    4. Generates live URLs: https://rhdbearings.com/specs/miniature-series/[model]/
    
    IMPORTANT: This uploads from deployment/ directory (standalone pages with embedded CSS)
    NOT from the source directory (pages with external CSS dependencies)
    
    Input: deployment/miniature-series-internal-pages/[model]/index.html (standalone)
    Output: Live server URLs for all 29 model pages
    """
    print(f"\n🚀 UPLOADING PAGES TO SERVER")
    print(f"==================================================")
    
    # No need for FTP credentials - curl_upload handles that
    
    source_dir = Path("deployment/miniature-series-internal-pages")
    if not source_dir.exists():
        print(f"   ❌ Source directory not found: {source_dir}")
        return False
    
    # Get all model directories
    model_dirs = [d for d in source_dir.iterdir() if d.is_dir()]
    if not model_dirs:
        print(f"   ❌ No model directories found in {source_dir}")
        return False
    
        print(f"📋 Found {len(model_dirs)} model directories to upload")
    print(f"🔧 Using deployment/curl_upload.py for reliable uploads")
    
    failed_count = 0
    successful_count = 0
    
    for model_dir in model_dirs:
        model_name = model_dir.name
        index_file = model_dir / "index.html"
        
        if not index_file.exists():
            print(f"   ❌ index.html not found for {model_name}")
            failed_count += 1
            continue
        
        print(f"\n📤 Uploading {model_name}...")
        
        try:
            # Use the imported curl_upload function (run from root directory)
            success = curl_upload(model_name)
            
            if success:
                print(f"   ✅ Successfully uploaded {model_name}")
                print(f"   🔗 URL: https://rhdbearings.com/specs/miniature-series/{model_name}/")
                successful_count += 1
            else:
                print(f"   ❌ Failed to upload {model_name}")
                failed_count += 1
                
        except Exception as e:
            print(f"   ❌ Error uploading {model_name}: {e}")
            failed_count += 1
    
    print(f"\n==================================================")
    print(f"📊 UPLOAD SUMMARY")
    print(f"==================================================")
    print(f"✅ Successfully uploaded: {successful_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"🎯 Total: {len(model_dirs)}")
    
    if failed_count == 0:
        print(f"\n🎉 All {successful_count} pages uploaded successfully!")
        print(f"✅ Your website is fully updated!")
        return True
    else:
        print(f"\n⚠️  {failed_count} page(s) failed to upload!")
        return False

def process_miniature_webpage():
    """
    STEP 4: Process and upload main MiniatureBearingsWebPage
    
    This function:
    1. Reads the main MiniatureBearingsWebPage from webpages/MiniatureBearingsWebPage/
    2. Creates a standalone version with embedded CSS in deployment/miniature-series/
    3. Uploads the standalone main page to the server
    4. Generates live URL: https://rhdbearings.com/specs/miniature-series.html
    
    Input: webpages/MiniatureBearingsWebPage/index.html + styles.css + shared components
    Output: Live server URL for main miniature series page
    """
    print(f"\n🚀 PROCESSING MINIATURE WEBPAGE")
    print(f"==================================================")
    
    # Source directory (MiniatureBearingsWebPage)
    source_dir = Path("webpages/MiniatureBearingsWebPage")
    if not source_dir.exists():
        print(f"   ❌ Source directory not found: {source_dir}")
        return False
    
    # Check if index.html exists in source
    source_index = source_dir / "index.html"
    if not source_index.exists():
        print(f"   ❌ Source index.html not found: {source_index}")
        return False
    
    # Check if styles.css exists in source
    source_styles = source_dir / "styles.css"
    if not source_styles.exists():
        print(f"   ❌ Source styles.css not found: {source_styles}")
        return False
    
    print(f"📁 Source: {source_dir}")
    print(f"✅ Found source files:")
    print(f"   📄 {source_index.name}")
    print(f"   🎨 {source_styles.name}")
    
    # Create standalone page directly in this script
    print(f"\n🔧 Creating standalone page for MiniatureBearingsWebPage...")
    
    try:
        success = create_standalone_miniature_webpage()
        if success:
            print(f"   ✅ Successfully created standalone page")
            print(f"   📁 Output: deployment/miniature-series/index.html")
        else:
            print(f"   ❌ Failed to create standalone page")
            return False
            
    except Exception as e:
        print(f"   ❌ Error processing MiniatureBearingsWebPage: {e}")
        return False
    
    # Upload the page to the server
    print(f"\n📤 Uploading MiniatureBearingsWebPage to server...")
    
    # No need for FTP credentials - curl_upload handles that
    print(f"   🔧 Using deployment/curl_upload.py for reliable upload")
    
    try:
        # Use the imported curl_upload function for the main page (run from root directory)
        success = curl_upload('miniature')
        
        if success:
            print(f"   ✅ Successfully uploaded MiniatureBearingsWebPage")
            print(f"   🔗 URL: https://rhdbearings.com/specs/miniature-series.html")
        else:
            print(f"   ❌ Failed to upload MiniatureBearingsWebPage")
            return False
            
    except Exception as e:
        print(f"   ❌ Error uploading: {e}")
        return False
    
    print(f"\n🎉 MiniatureBearingsWebPage processed and uploaded successfully!")
    print(f"📁 Standalone page ready in: deployment/miniature-series/")
    print(f"🌐 Live on server at: https://rhdbearings.com/specs/miniature-series.html")
    return True

def main():
    """
    Main function - Complete workflow execution
    
    This function orchestrates the entire 4-step process:
    1. Generate HTML pages from JSON files
    2. Create standalone pages with embedded CSS
    3. Upload all pages to the server
    4. Process and upload main MiniatureBearingsWebPage
    
    COMMAND LINE USAGE:
    - No arguments: Run complete workflow (all 4 steps)
    - --generate-only: Run only step 1 (HTML generation)
    - --standalone-only: Run only step 2 (standalone page creation)
    - --upload-only: Run only step 3 (server upload)
    - --webpage-only: Run only step 4 (main page processing)
    - --help: Show usage information
    
    EXECUTION ORDER:
    The steps must be run in sequence for the complete workflow to work properly.
    Each step depends on the output of the previous step.
    """
    if len(sys.argv) > 1:
        step = sys.argv[1].lower()
        
        if step == '--generate-only':
            print("📝 RUNNING GENERATION STEP ONLY")
            print("-" * 40)
            success = generate_miniature_pages()
            sys.exit(0 if success else 1)
            
        elif step == '--standalone-only':
            print("📝 RUNNING STANDALONE PAGE CREATION ONLY")
            print("-" * 40)
            success = create_standalone_pages()
            sys.exit(0 if success else 1)
            
        elif step == '--upload-only':
            print("📝 RUNNING UPLOAD STEP ONLY")
            print("-" * 40)
            success = upload_pages()
            sys.exit(0 if success else 1)
            
        elif step == '--webpage-only':
            print("📝 RUNNING MINIATURE WEBPAGE PROCESSING ONLY")
            print("-" * 40)
            success = process_miniature_webpage()
            sys.exit(0 if success else 1)
            
        elif step == '--help' or step == '-h':
            print("🚀 MINIATURE SERIES COMPLETE WORKFLOW SCRIPT")
            print("=" * 60)
            print("✅ Uses deployment/curl_upload.py for reliable uploads!")
            print("=" * 60)
            print("Usage:")
            print("  python generate_miniature_pages.py              # Run complete workflow")
            print("  python generate_miniature_pages.py --generate-only    # Generate HTML pages only")
            print("  python generate_miniature_pages.py --standalone-only  # Create standalone pages only")
            print("  python generate_miniature_pages.py --upload-only      # Upload pages only")
            print("  python generate_miniature_pages.py --webpage-only     # Process MiniatureBearingsWebPage only")
            print("  python generate_miniature_pages.py --help             # Show this help")
            print("\nComplete workflow:")
            print("1. Generate HTML pages from JSON files")
            print("2. Create standalone pages (bypassing WordPress)")
            print("3. Upload all pages to the server")
            print("4. Process MiniatureBearingsWebPage to deployment/miniature-series/")
            print("=" * 60)
            sys.exit(0)
            
        else:
            print(f"❌ Unknown option: {step}")
            print("💡 Use --help to see available options")
            sys.exit(1)
    
    print("🚀 MINIATURE SERIES COMPLETE WORKFLOW")
    print("=" * 60)
    print("This script will:")
    print("1. Generate HTML pages from JSON files")
    print("2. Create standalone pages (bypassing WordPress)")
    print("3. Upload all pages to the server")
    print("4. Process MiniatureBearingsWebPage to deployment/miniature-series/")
    print("=" * 60)
    print("\n📋 REQUIREMENTS:")
    print("   • .env file with FTP credentials (FTP_PASSWORD)")
    print("   • deployment/curl_upload.py available")
    print("   • MiniatureBearingsWebPage in webpages/")
    print("   • Shared components in webpages/shared/")
    print("=" * 60)
    
    # Step 1: Generate HTML pages
    print("\n📝 STEP 1: GENERATING HTML PAGES")
    print("-" * 40)
    success = generate_miniature_pages()
    
    if not success:
        print("💥 HTML generation failed. Stopping workflow.")
        sys.exit(1)
    
    # Step 2: Create standalone pages
    print("\n📝 STEP 2: CREATING STANDALONE PAGES")
    print("-" * 40)
    success = create_standalone_pages()
    
    if not success:
        print("💥 Standalone page creation failed. Stopping workflow.")
        sys.exit(1)
    
    # Step 3: Upload pages
    print("\n📝 STEP 3: UPLOADING PAGES TO SERVER")
    print("-" * 40)
    success = upload_pages()
    
    if not success:
        print("💥 Upload failed. Check the errors above.")
        sys.exit(1)
    
    # Step 4: Process MiniatureBearingsWebPage
    print("\n📝 STEP 4: PROCESSING MINIATURE WEBPAGE")
    print("-" * 40)
    success = process_miniature_webpage()
    
    if not success:
        print("💥 Miniature webpage processing failed. Check the errors above.")
        sys.exit(1)
    
    # All steps completed successfully
    print("\n" + "=" * 60)
    print("🎉 COMPLETE WORKFLOW SUCCESSFUL!")
    print("=" * 60)
    print("✅ All miniature series pages have been:")
    print("   • Generated from JSON files")
    print("   • Converted to standalone pages (completely independent)")
    print("   • Uploaded to the server")
    print("   • MiniatureBearingsWebPage processed to deployment/miniature-series/")
    print("\n🌐 Your website is now fully updated!")
    print("🔗 Visit: https://rhdbearings.com/specs/miniature-series/")
    print("🔗 Visit: https://rhdbearings.com/specs/miniature-series.html")
    print("=" * 60)
    
    """
    WORKFLOW COMPLETION SUMMARY:
    ===========================
    
    WHAT WAS ACCOMPLISHED:
    - 29 miniature series model pages generated from JSON data
    - All pages converted to standalone format with embedded CSS
    - All pages uploaded to live server with proper URLs
    - Main miniature series page processed and uploaded
    
    FINAL OUTPUT LOCATIONS:
    - Source pages: webpages/MiniatureBearingsWebPage/internalpages/
    - Standalone pages: deployment/miniature-series-internal-pages/
    - Main page: deployment/miniature-series/
    - Live URLs: https://rhdbearings.com/specs/miniature-series/[model]/
    
    NEXT STEPS:
    - Verify all pages are displaying correctly on the live server
    - Check that CSS styling is working properly
    - Monitor for any issues or errors
    - Repeat workflow when new models are added or updates are needed
    """

if __name__ == "__main__":
    main()
