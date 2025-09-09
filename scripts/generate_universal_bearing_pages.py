#!/usr/bin/env python3
"""
Universal Bearing Series Page Generator Script
=============================================

This script generates HTML pages for ALL bearing series (excluding miniature series)
using the same workflow as the miniature script but for 6200, 6300, 16000, etc.

DIRECTORY STRUCTURE:
===================
models/ → webpages/{series}SeriesWebPage/internalpages/{model}/ → deployment/{series}-series/{series}-series-internal-pages-deployment/{model}/

EXCLUDED SERIES:
================
- Miniature series (604, 605, 606, 607, 608, 609, 623, 624, 625, 626, 627, 628, 629, 634, 635, 683, 684, 685, 686, 687, 688, 689, 693, 694, 695, 696, 697, 698, 699)

INCLUDED SERIES:
================
- 6000 series (6000, 6001, 6002, 6003, 6004, 6005, 6006, 6007, 6008, 6009, 6010, 6011, 6012, 6013, 6014, 6015, 6016, 6017, 6018, 6019, 6020)
- 6200 series (6200, 6201, 6202, 6203, 6204, 6205, 6206, 6207, 6208, 6209, 6210, 6211, 6212, 6213, 6214, 6215, 6216, 6217, 6218, 6219, 6220)
- 6300 series (6300, 6301, 6302, 6303, 6304, 6305, 6306, 6307, 6308, 6309, 6310, 6311, 6312, 6313, 6314, 6315, 6316, 6317, 6318, 6319, 6320)
- 16000 series (16000, 16001, 16002, 16003, 16004, 16005, 16006, 16007, 16008, 16009, 16010, 16011, 16012, 16013, 16014, 16015, 16016, 16017, 16018, 16019, 16020)
- 62200 series (62200, 62201, 62202, 62203, 62204, 62205, 62206, 62207, 62208, 62209, 62210, 62211, 62212, 62213, 62214, 62215, 62216, 62217, 62218, 62219, 62220)
- 62300 series (62300, 62301, 62302, 62303, 62304, 62305, 62306, 62307, 62308, 62309, 62310, 62311, 62312, 62313, 62314, 62315, 62316, 62317, 62318, 62319, 62320)
- 6800 series (6800, 6801, 6802, 6803, 6804, 6805, 6806, 6807, 6808, 6809, 6810, 6811, 6812, 6813, 6814, 6815, 6816, 6817, 6818, 6819, 6820)
- 6900 series (6900, 6901, 6902, 6903, 6904, 6905, 6906, 6907, 6908, 6909, 6910, 6911, 6912, 6913, 6914, 6915, 6916, 6917, 6918, 6919, 6920)

USAGE:
======
# Run ALL non-miniature series (complete 3-step workflow)
python3 scripts/generate_universal_bearing_pages.py

# Run specific series
python3 scripts/generate_universal_bearing_pages.py --6000-series
python3 scripts/generate_universal_bearing_pages.py --6200-series
python3 scripts/generate_universal_bearing_pages.py --6300-series
python3 scripts/generate_universal_bearing_pages.py --16000-series

# Run multiple series
python3 scripts/generate_universal_bearing_pages.py --6000-series --6200-series
python3 scripts/generate_universal_bearing_pages.py --6200-series --6300-series

# Run individual steps
python3 scripts/generate_universal_bearing_pages.py --generate-only
python3 scripts/generate_universal_bearing_pages.py --standalone-only
python3 scripts/generate_universal_bearing_pages.py --upload-only
python3 scripts/generate_universal_bearing_pages.py --standalone-main-only  # Create standalone main pages only (fast!)
python3 scripts/generate_universal_bearing_pages.py --upload-main-only      # Upload only main series pages (fast!)

REQUIREMENTS:
=============
- .env file with FTP credentials (FTP_PASSWORD)
- deployment/curl_upload.py available
- All directories and files in expected locations
- Run from root workspace directory
"""

import json
import sys
import os
import re
import subprocess
import argparse
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

class UniversalBearingPageGenerator:
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
            return "universal-series"  # Default fallback
            
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
            return None  # Exclude these
        
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
            return "universal-series"
    
    def convert_kn_to_kg(self, value, field_name=""):
        """
        Convert kN values to kg while keeping kN in parentheses for reference.
        """
        # Skip conversion for load_ratings fields (keep them in kN)
        if 'load_ratings' in field_name:
            return str(value)
        
        # Convert string values containing kN
        if isinstance(value, str):
            # Look for patterns like "0.75kN" or "1.2 kN"
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
            
            # Validate LLM data structure
            self._validate_llm_data_structure()
            
            content = self.template_content
            
            # 1. Replace grid class placeholder
            content = self._replace_grid_class(content)
            
            # 2. Replace conditional SKF dimensions
            content = self._replace_skf_conditionals(content)
            
            # 3. Replace clearance conditionals
            content = self._replace_clearance_conditionals(content)
            
            # 4. Replace applications
            content = self._replace_applications(content)
            
            # 5. Replace SEO metadata
            content = self._replace_seo_metadata(content)
            
            # 6. Replace pricing and availability
            content = self._replace_pricing_availability(content)
            
            # 7. Replace FAQs
            content = self._replace_faqs(content)
            
            # 8. Replace cross references
            content = self._replace_cross_references(content)
            
            # 9. Replace expertise signals
            content = self._replace_expertise_signals(content)
            
            # 10. Replace LLM optimization sections
            content = self._replace_llm_optimization_sections(content)
            
            # 11. Handle missing LLM data gracefully
            content = self._handle_missing_llm_data(content)
            
            # 12. Replace simple placeholders
            content = self._replace_simple_placeholders(content)
            

            
            # 14. Sanitize HTML content for security
            content = self._sanitize_html_content(content)
            
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
        
        # Related models - generate proper URLs based on series detection
        related_models = cross_refs.get('related_models', [])
        if related_models:
            models_html = '\n'.join([
                f'<a href="https://rhdbearings.com/specs/{self.get_series_from_model(model)}/{model}/" class="model-link">{model}</a>' 
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
    
    def _replace_seo_metadata(self, content: str) -> str:
        """Replace SEO metadata placeholders"""
        seo_data = self.data.get('seo_metadata', {})
        
        # Basic SEO fields
        if seo_data:
            # Title
            if seo_data.get('title'):
                content = content.replace('{{seo_metadata.title}}', str(seo_data['title']))
            else:
                # Generate default title from model number
                model_number = self.data.get('model_number', 'Bearing')
                content = content.replace('{{seo_metadata.title}}', f"{model_number} Deep Groove Ball Bearing | RHD Bearings")
            
            # Meta description
            if seo_data.get('meta_description'):
                content = content.replace('{{seo_metadata.meta_description}}', str(seo_data['meta_description']))
            else:
                # Generate default description
                model_number = self.data.get('model_number', 'Bearing')
                content = content.replace('{{seo_metadata.meta_description}}', f"High-quality {model_number} deep groove ball bearing. Technical specifications, dimensions, load ratings, and applications. ISO compliant, precision engineered.")
            
            # Keywords
            if seo_data.get('keywords'):
                keywords = seo_data['keywords']
                if isinstance(keywords, list):
                    keywords_string = ', '.join(keywords)
                    content = content.replace('{{seo_metadata.keywords_string}}', keywords_string)
                else:
                    content = content.replace('{{seo_metadata.keywords_string}}', str(keywords))
            else:
                # Generate default keywords
                model_number = self.data.get('model_number', 'Bearing')
                default_keywords = f"{model_number}, deep groove ball bearing, ball bearing, industrial bearing, precision bearing, ISO compliant"
                content = content.replace('{{seo_metadata.keywords_string}}', default_keywords)
            
            # Canonical URL
            if seo_data.get('canonical_url'):
                content = content.replace('{{seo_metadata.canonical_url}}', str(seo_data['canonical_url']))
            else:
                # Generate default canonical URL
                model_number = self.data.get('model_number', 'bearing')
                series_name = self.get_series_from_model(model_number)
                content = content.replace('{{seo_metadata.canonical_url}}', f"https://rhdbearings.com/specs/{series_name}/{model_number}/")
            
            # Open Graph data
            og_data = seo_data.get('og_data', {})
            if og_data:
                if og_data.get('title'):
                    content = content.replace('{{seo_metadata.og_data.title}}', str(og_data['title']))
                else:
                    content = content.replace('{{seo_metadata.og_data.title}}', '{{seo_metadata.title}}')
                
                if og_data.get('description'):
                    content = content.replace('{{seo_metadata.og_data.description}}', str(og_data['description']))
                else:
                    content = content.replace('{{seo_metadata.og_data.description}}', '{{seo_metadata.meta_description}}')
                
                if og_data.get('url'):
                    content = content.replace('{{seo_metadata.og_data.url}}', str(og_data['url']))
                else:
                    content = content.replace('{{seo_metadata.og_data.url}}', '{{seo_metadata.canonical_url}}')
                
                if og_data.get('type'):
                    content = content.replace('{{seo_metadata.og_data.type}}', str(og_data['type']))
                else:
                    content = content.replace('{{seo_metadata.og_data.type}}', 'product')
                
                if og_data.get('site_name'):
                    content = content.replace('{{seo_metadata.og_data.site_name}}', str(og_data['site_name']))
                else:
                    content = content.replace('{{seo_metadata.og_data.site_name}}', 'RHD Bearings')
            
            # Twitter data
            twitter_data = seo_data.get('twitter_data', {})
            if twitter_data:
                if twitter_data.get('card'):
                    content = content.replace('{{seo_metadata.twitter_data.card}}', str(twitter_data['card']))
                else:
                    content = content.replace('{{seo_metadata.twitter_data.card}}', 'summary_large_image')
                
                if twitter_data.get('title'):
                    content = content.replace('{{seo_metadata.twitter_data.title}}', str(twitter_data['title']))
                else:
                    content = content.replace('{{seo_metadata.twitter_data.title}}', '{{seo_metadata.title}}')
                
                if twitter_data.get('description'):
                    content = content.replace('{{seo_metadata.twitter_data.description}}', str(twitter_data['description']))
                else:
                    content = content.replace('{{seo_metadata.twitter_data.description}}', '{{seo_metadata.meta_description}}')
            
            # Schema markup
            schema_data = seo_data.get('schema_markup', {})
            if schema_data:
                # Fix the @context issue by using a valid JSON-LD structure
                if schema_data.get('@context'):
                    content = content.replace('{{seo_metadata.schema_markup.@context}}', str(schema_data['@context']))
                else:
                    content = content.replace('{{seo_metadata.schema_markup.@context}}', 'https://schema.org/')
                
                if schema_data.get('@type'):
                    content = content.replace('{{seo_metadata.schema_markup.@type}}', str(schema_data['@type']))
                else:
                    content = content.replace('{{seo_metadata.schema_markup.@type}}', 'Product')
                
                if schema_data.get('name'):
                    content = content.replace('{{seo_metadata.schema_markup.name}}', str(schema_data['name']))
                else:
                    content = content.replace('{{seo_metadata.schema_markup.name}}', '{{model_number}} Deep Groove Ball Bearing')
                
                if schema_data.get('description'):
                    content = content.replace('{{seo_metadata.schema_markup.description}}', str(schema_data['description']))
                else:
                    content = content.replace('{{seo_metadata.schema_markup.description}}', '{{seo_metadata.meta_description}}')
                
                if schema_data.get('sku'):
                    content = content.replace('{{seo_metadata.schema_markup.sku}}', str(schema_data['sku']))
                else:
                    content = content.replace('{{seo_metadata.schema_markup.sku}}', '{{model_number}}')
                
                if schema_data.get('mpn'):
                    content = content.replace('{{seo_metadata.schema_markup.mpn}}', str(schema_data['mpn']))
                else:
                    content = content.replace('{{seo_metadata.schema_markup.mpn}}', '{{model_number}}')
                
                if schema_data.get('category'):
                    content = content.replace('{{seo_metadata.schema_markup.category}}', str(schema_data['category']))
                else:
                    content = content.replace('{{seo_metadata.schema_markup.category}}', 'Deep Groove Ball Bearings')
        
        return content
    
    def _replace_pricing_availability(self, content: str) -> str:
        """Replace pricing and availability placeholders"""
        pricing_data = self.data.get('pricing_and_availability', {})
        
        if pricing_data:
            # Currency
            if pricing_data.get('currency'):
                content = content.replace('{{pricing_and_availability.currency}}', str(pricing_data['currency']))
            else:
                content = content.replace('{{pricing_and_availability.currency}}', 'INR')
            
            # Quote required
            if pricing_data.get('quote_required'):
                content = content.replace('{{pricing_and_availability.quote_required}}', str(pricing_data['quote_required']))
            else:
                content = content.replace('{{pricing_and_availability.quote_required}}', 'true')
            
            # Stock status
            availability = pricing_data.get('availability', {})
            if availability:
                if availability.get('stock_status'):
                    content = content.replace('{{pricing_and_availability.availability.stock_status}}', str(availability['stock_status']))
                else:
                    content = content.replace('{{pricing_and_availability.availability.stock_status}}', 'Available for immediate dispatch')
                
                # Call to action
                call_to_action = availability.get('call_to_action', {})
                if call_to_action:
                    if call_to_action.get('primary'):
                        content = content.replace('{{pricing_and_availability.availability.call_to_action.primary}}', str(call_to_action['primary']))
                    else:
                        content = content.replace('{{pricing_and_availability.availability.call_to_action.primary}}', '📞 Call +91-9702081858 for immediate pricing and availability')
                    
                    if call_to_action.get('secondary'):
                        content = content.replace('{{pricing_and_availability.availability.call_to_action.secondary}}', str(call_to_action['secondary']))
                    else:
                        content = content.replace('{{pricing_and_availability.availability.call_to_action.secondary}}', '📧 Email sales@rhdenterprise.in for detailed quotation')
                    
                    if call_to_action.get('oem_sales'):
                        content = content.replace('{{pricing_and_availability.availability.call_to_action.oem_sales}}', str(call_to_action['oem_sales']))
                    else:
                        content = content.replace('{{pricing_and_availability.availability.call_to_action.oem_sales}}', '🏭 OEM/Bulk orders: oemsales@rhdenterprise.in')
                    
                    if call_to_action.get('urgency'):
                        content = content.replace('{{pricing_and_availability.availability.call_to_action.urgency}}', str(call_to_action['urgency']))
                    else:
                        content = content.replace('{{pricing_and_availability.availability.call_to_action.urgency}}', 'Need it today? Call now - we dispatch same day!')
        
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
        
        # Note: Expert Recommendations section has been removed from the HTML template
        
        # 2. Replace Search Optimization Tags
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
        
        # Note: Decision Criteria section has been removed from the HTML template
        
        # Note: Problem-Solution Mapping section has been removed from the HTML template
        
        # Note: Performance Comparison section has been removed from the HTML template
        
        return content
    
    def _handle_missing_llm_data(self, content: str) -> str:
        """Handle cases where LLM optimization data is missing or incomplete"""
        
        # Check if any LLM optimization data exists
        llm_data = self.data.get('llm_optimization', {})
        has_any_llm_data = any([
            llm_data.get('natural_language_queries'),
            llm_data.get('expertise_signals')
        ])
        
        if not has_any_llm_data:
            print(f"      ⚠️  No LLM optimization data found for {self.json_file}")
            # Remove all LLM optimization sections if no data exists
            sections_to_remove = [
                '<!-- Search Optimization Tags -->'
            ]
            
            for section in sections_to_remove:
                # Find the section and remove it along with its content
                section_start = content.find(section)
                if section_start != -1:
                    # Find the next section or end of content
                    next_section = None
                    for next_section_name in sections_to_remove:
                        if next_section_name != section:
                            next_pos = content.find(next_section_name, section_start + 1)
                            if next_pos != -1 and (next_section is None or next_pos < next_section):
                                next_section = next_pos
                    
                    if next_section is None:
                        # If no next section found, remove to the end
                        content = content[:section_start]
                    else:
                        # Remove the section and its content
                        content = content[:section_start] + content[next_section:]
        
        return content
    
    def _validate_llm_data_structure(self):
        """Validate and log LLM optimization data structure"""
        llm_data = self.data.get('llm_optimization', {})
        
        if not llm_data:
            return
        
        print(f"      📊 LLM Optimization Data Structure:")
        
        # Check each section
        sections = {
            'natural_language_queries': 'Search Optimization Tags',
            'expertise_signals': 'Expertise Signals'
        }
        
        for key, display_name in sections.items():
            data = llm_data.get(key)
            if data:
                if isinstance(data, list):
                    print(f"         ✅ {display_name}: {len(data)} items")
                elif isinstance(data, dict):
                    print(f"         ✅ {display_name}: {len(data)} key-value pairs")
                else:
                    print(f"         ⚠️  {display_name}: {type(data).__name__} (unexpected type)")
            else:
                print(f"         ❌ {display_name}: Missing")
        
        return True
    
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
    

    
    def _sanitize_html_content(self, content: str) -> str:
        """Sanitize HTML content to prevent XSS and ensure valid HTML"""
        import html
        
        # Only escape content that comes from JSON data, not static template HTML
        # This prevents breaking icon spans and other static HTML elements
        
        # Find and escape only the content that was dynamically inserted from JSON
        # Look for patterns that indicate JSON data was inserted
        
        # Escape content in dynamically generated sections (LLM optimization, etc.)
        # but preserve static template HTML like icon spans
        
        # For now, disable aggressive HTML escaping to preserve template structure
        # The content is already sanitized when generated in the specific methods
        
        return content
    
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

def get_series_mapping():
    """Get mapping of series to their directory names"""
    return {
        "6200-series": "6200SeriesWebPage",
        "6300-series": "6300SeriesWebPage", 
        "16000-series": "16000SeriesWebPage",
        "62200-series": "62200SeriesWebPage",
        "62300-series": "62300SeriesWebPage",
        "6800-series": "6800SeriesWebPage",
        "6900-series": "6900SeriesWebPage",
        "6000-series": "6000SeriesWebPage",
        "specs-hub": "SpecsHubPage"
    }

def get_series_from_model_number(model_number):
    """Determine series from model number (same logic as the class)"""
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
        return None  # Exclude these
    
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
        return "universal-series"

def generate_universal_pages(selected_series=None):
    """
    STEP 1: Generate HTML pages from JSON files
    
    This function:
    1. Scans the models/ directory for all JSON files
    2. Filters for non-miniature series models
    3. Generates HTML pages using the template
    4. Outputs pages to webpages/{series}SeriesWebPage/internalpages/
    5. Copies styles.css to each model directory
    """
    models_dir = Path("models")
    template_file = Path("webpages/templates/index_new_claude.html")
    
    # Check if required files exist
    if not models_dir.exists():
        print(f"❌ Models directory not found: {models_dir}")
        return False
    
    if not template_file.exists():
        print(f"❌ Template file not found: {template_file}")
        return False
    
    # Get all JSON files
    all_json_files = list(models_dir.glob("*.json"))
    if not all_json_files:
        print(f"❌ No JSON files found in {models_dir}")
        return False
    
    print(f"🔍 SCANNING MODELS DIRECTORY")
    print(f"📋 Found {len(all_json_files)} total JSON files")
    
    # Group models by series
    series_models = {}
    skipped_models = []
    
    for json_file in all_json_files:
        model_name = json_file.stem
        series = get_series_from_model_number(model_name)
        
        if series and series != "universal-series":
            if selected_series is None or series in selected_series:
                if series not in series_models:
                    series_models[series] = []
                series_models[series].append(json_file)
                print(f"   ✅ {series.upper()}: {model_name}")
        else:
            skipped_models.append(json_file)
            if series is None:
                print(f"   ⏭️  SKIP: {model_name} (miniature series)")
            else:
                print(f"   ⏭️  SKIP: {model_name} (unknown series)")
    
    print(f"\n📊 FILTERING RESULTS:")
    print(f"   ✅ INCLUDED SERIES: {len(series_models)} series")
    for series, models in series_models.items():
        print(f"      • {series}: {len(models)} models")
    print(f"   ⏭️  SKIPPED: {len(skipped_models)} models")
    
    # Add SpecsHubPage to the series_models if it's selected
    if selected_series is None or "specs-hub" in selected_series:
        if "specs-hub" not in series_models:
            series_models["specs-hub"] = []  # Empty list since SpecsHubPage has no JSON models
    
    if not series_models:
        print(f"\n❌ No valid series found in {models_dir}")
        return False
    
    print(f"\n🚀 GENERATING PAGES FOR SELECTED SERIES")
    print(f"==================================================")
    print(f"📁 Template: {template_file}")
    print(f"==================================================")
    
    series_mapping = get_series_mapping()
    success_count = 0
    failed_count = 0
    
    for series, models in series_models.items():
        if series not in series_mapping:
            print(f"⚠️  No directory mapping for {series}, skipping...")
            continue
        
        # Special handling for SpecsHubPage (no JSON models to process)
        if series == "specs-hub":
            print(f"\n🔧 Processing {series} series...")
            print(f"   📋 SpecsHubPage has no JSON models to process (single page)")
            success_count += 1  # Mark as successful since it's handled in standalone creation
            continue
            
        series_dir_name = series_mapping[series]
        output_base_dir = Path(f"webpages/{series_dir_name}/internalpages")
        
        # Create output directory
        output_base_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n🔧 Processing {series} series...")
        print(f"   📁 Output base: {output_base_dir}")
        
        for json_file in models:
            model_name = json_file.stem
            output_dir = output_base_dir / model_name
            output_dir.mkdir(exist_ok=True)
            
            print(f"      🔧 Generating page for {model_name}...")
            
            try:
                output_file = output_dir / "index.html"
                generator = UniversalBearingPageGenerator(str(json_file), str(template_file), str(output_file))
                
                success = generator.generate_page()
                
                if success:
                    # Copy styles.css to the model directory
                    styles_source = Path("webpages/templates/styles.css")
                    styles_dest = output_dir / "styles.css"
                    if styles_source.exists():
                        import shutil
                        shutil.copy2(styles_source, styles_dest)
                        print(f"         ✅ Successfully generated {model_name} page")
                        print(f"         📁 Copied styles.css to {model_name}/")
                        success_count += 1
                    else:
                        print(f"         ⚠️  Generated {model_name} page but styles.css not found")
                        success_count += 1
                else:
                    print(f"         ❌ Failed to generate {model_name} page")
                    failed_count += 1
                    
            except Exception as e:
                print(f"         ❌ Error generating {model_name} page: {e}")
                failed_count += 1
    
    print(f"\n==================================================")
    print(f"📊 GENERATION SUMMARY")
    print(f"==================================================")
    print(f"✅ Successfully generated: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"🎯 Total: {success_count + failed_count}")
    
    if failed_count == 0:
        print(f"\n🎉 All {success_count} pages generated successfully!")
        return True
    else:
        print(f"\n⚠️  {failed_count} page(s) failed to generate. Check the errors above.")
        return False

def create_standalone_pages(selected_series=None):
    """
    STEP 2: Create standalone pages with embedded CSS
    
    This function:
    1. Creates standalone main series pages (from existing HTML/CSS)
    2. Creates standalone individual model pages (from generated HTML)
    3. Embeds all shared CSS and HTML components
    4. Creates completely standalone HTML files
    5. Outputs to deployment/{series}-series/ and deployment/{series}-series/{series}-series-internal-pages-deployment/
    """
    print(f"\n🚀 CREATING STANDALONE PAGES")
    print(f"==================================================")
    
    series_mapping = get_series_mapping()
    failed_count = 0
    successful_count = 0
    
    for series, series_dir_name in series_mapping.items():
        if selected_series is None or series in selected_series:
            print(f"\n🔧 Creating standalone pages for {series} series...")
            
            # Special handling for SpecsHubPage (no internal model pages)
            if series == "specs-hub":
                print(f"   📋 Processing SpecsHubPage (single page)...")
                try:
                    success = create_standalone_specs_hub_page(series, series_dir_name)
                    if success:
                        print(f"      ✅ Successfully created standalone SpecsHubPage")
                        successful_count += 1
                    else:
                        print(f"      ❌ Failed to create standalone SpecsHubPage")
                        failed_count += 1
                except Exception as e:
                    print(f"      ❌ Error processing SpecsHubPage: {e}")
                    failed_count += 1
                continue
            
            # STEP 2A: Create standalone main series page
            print(f"   📋 Processing main series page...")
            try:
                success = create_standalone_main_series_page(series, series_dir_name)
                if success:
                    print(f"      ✅ Successfully created standalone main series page")
                    successful_count += 1
                else:
                    print(f"      ❌ Failed to create standalone main series page")
                    failed_count += 1
            except Exception as e:
                print(f"      ❌ Error processing main series page: {e}")
                failed_count += 1
            
            # STEP 2B: Create standalone individual model pages
            series_base_dir = Path(f"webpages/{series_dir_name}/internalpages")
            if not series_base_dir.exists():
                print(f"   ⚠️  Internal pages directory not found: {series_base_dir}")
                continue
            
            # Get all model directories
            model_dirs = [d for d in series_base_dir.iterdir() if d.is_dir()]
            if not model_dirs:
                print(f"   ⚠️  No model directories found in {series_base_dir}")
                continue
            
            print(f"   📋 Found {len(model_dirs)} model directories")
            
            for model_dir in model_dirs:
                model_name = model_dir.name
                print(f"      🔧 Creating standalone page for {model_name}...")
                
                try:
                    success = create_standalone_model_page(model_name, model_dir, series)
                    if success:
                        print(f"         ✅ Successfully created standalone page for {model_name}")
                        successful_count += 1
                    else:
                        print(f"         ❌ Failed to create standalone page for {model_name}")
                        failed_count += 1
                        
                except Exception as e:
                    print(f"         ❌ Error processing {model_name}: {e}")
                    failed_count += 1
    
    print(f"\n==================================================")
    print(f"📊 STANDALONE PAGE CREATION SUMMARY")
    print(f"==================================================")
    print(f"✅ Successfully created: {successful_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"🎯 Total: {successful_count + failed_count}")
    
    if failed_count == 0:
        print(f"\n🎉 All {successful_count} standalone pages created successfully!")
        return True
    else:
        print(f"\n⚠️  {failed_count} page(s) failed to create. Check the errors above.")
        return False

def create_standalone_main_series_page(series, series_dir_name):
    """Helper function for create_standalone_pages() - creates standalone main series page"""
    try:
        # Read the existing main series HTML file
        series_dir = Path(f"webpages/{series_dir_name}")
        index_file = series_dir / "index.html"
        styles_file = series_dir / "styles.css"
        
        if not index_file.exists():
            print(f"            ❌ index.html not found in {series_dir}")
            return False
        
        with open(index_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Read the main styles.css file
        styles_css = ""
        if styles_file.exists():
            try:
                with open(styles_file, 'r', encoding='utf-8') as f:
                    styles_css = f.read()
                print(f"            ✅ Loaded main series CSS: {len(styles_css)} characters")
            except:
                print(f"            ⚠️  styles.css not found, using empty CSS")
                styles_css = ""
        
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
            print(f"            ⚠️  navbar.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "footer.css", 'r', encoding='utf-8') as f:
                footer_css = f.read()
        except:
            print(f"            ⚠️  footer.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "cta-model.css", 'r', encoding='utf-8') as f:
                cta_css = f.read()
        except:
            print(f"            ⚠️  cta-model.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "watermark.css", 'r', encoding='utf-8') as f:
                watermark_css = f.read()
            print(f"            ✅ Loaded watermark CSS: {len(watermark_css)} characters")
        except:
            print(f"            ⚠️  watermark.css not found, using empty CSS")
            watermark_css = ""
        
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
            print(f"            ⚠️  navbar.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "footer.html", 'r', encoding='utf-8') as f:
                footer_html = f.read()
        except:
            print(f"            ⚠️  footer.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "cta-model.html", 'r', encoding='utf-8') as f:
                cta_html = f.read()
                # Replace [MODEL] placeholder with series name
                cta_html = cta_html.replace('[MODEL]', series.replace('-series', '').upper())
        except:
            print(f"            ⚠️  cta-model.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "watermark.html", 'r', encoding='utf-8') as f:
                watermark_html = f.read()
            print(f"            ✅ Loaded watermark HTML: {len(watermark_html)} characters")
        except:
            print(f"            ⚠️  watermark.html not found, using empty HTML")
            watermark_html = ""
        
        # Extract body content and scripts
        body_start = html_content.find('<body')
        if body_start == -1:
            print(f"            ❌ No <body> tag found in HTML")
            return False
        
        body_start = body_start + html_content[body_start:].find('>') + 1
        body_end = html_content.find('</body>')
        if body_end == -1:
            print(f"            ❌ No </body> tag found in HTML")
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
        
        # Remove fetch calls to shared components
        body_content = re.sub(r'fetch\([\'"][^\'"]*\.\./shared/[^\'"]*[\'"]\)', '// fetch call removed - component already embedded', body_content)
        
        # Remove script blocks that load shared components
        body_content = re.sub(r'<script>[^<]*fetch\([^<]*\.\./shared/[^<]*</script>', '<!-- Shared component loading script removed -->', body_content, flags=re.DOTALL)
        
        # Remove external script tags (script tags with src attribute)
        body_content = re.sub(r'<script[^>]*src=[^>]*></script>', '<!-- External script removed -->', body_content)
        
        # Remove any remaining references to ../shared/ paths (handle multiple levels)
        body_content = re.sub(r'\.\./shared/', '// shared path removed - components embedded', body_content)
        
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
    <title>{series.replace('-series', '').upper()} Series Deep Groove Ball Bearings | RHD Bearings</title>
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
        deployment_dir = Path(f"deployment/{series}")
        deployment_dir.mkdir(parents=True, exist_ok=True)
        
        # Save standalone main series page
        output_file = deployment_dir / "index.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(standalone_html)
        
        print(f"            ✅ Created standalone main series page: {output_file}")
        return True
        
    except Exception as e:
        print(f"            ❌ Error creating standalone main series page: {e}")
        return False

def create_standalone_specs_hub_page(series, series_dir_name):
    """Helper function for create_standalone_pages() - creates standalone SpecsHubPage"""
    try:
        # Read the existing SpecsHubPage HTML file
        series_dir = Path(f"webpages/{series_dir_name}")
        index_file = series_dir / "index.html"
        styles_file = series_dir / "styles.css"
        
        if not index_file.exists():
            print(f"            ❌ index.html not found in {series_dir}")
            return False
        
        with open(index_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Read the main styles.css file
        styles_css = ""
        if styles_file.exists():
            try:
                with open(styles_file, 'r', encoding='utf-8') as f:
                    styles_css = f.read()
                print(f"            ✅ Loaded SpecsHubPage CSS: {len(styles_css)} characters")
            except:
                print(f"            ⚠️  styles.css not found, using empty CSS")
                styles_css = ""
        
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
            print(f"            ⚠️  navbar.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "footer.css", 'r', encoding='utf-8') as f:
                footer_css = f.read()
        except:
            print(f"            ⚠️  footer.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "cta-model.css", 'r', encoding='utf-8') as f:
                cta_css = f.read()
        except:
            print(f"            ⚠️  cta-model.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "watermark.css", 'r', encoding='utf-8') as f:
                watermark_css = f.read()
            print(f"            ✅ Loaded watermark CSS: {len(watermark_css)} characters")
        except:
            print(f"            ⚠️  watermark.css not found, using empty CSS")
            watermark_css = ""
        
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
            print(f"            ⚠️  navbar.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "footer.html", 'r', encoding='utf-8') as f:
                footer_html = f.read()
        except:
            print(f"            ⚠️  footer.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "cta-model.html", 'r', encoding='utf-8') as f:
                cta_html = f.read()
                # Replace [MODEL] placeholder with "Specs Hub"
                cta_html = cta_html.replace('[MODEL]', 'Specs Hub')
        except:
            print(f"            ⚠️  cta-model.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "watermark.html", 'r', encoding='utf-8') as f:
                watermark_html = f.read()
            print(f"            ✅ Loaded watermark HTML: {len(watermark_html)} characters")
        except:
            print(f"            ⚠️  watermark.html not found, using empty HTML")
            watermark_html = ""
        
        # Extract body content and scripts
        body_start = html_content.find('<body')
        if body_start == -1:
            print(f"            ❌ No <body> tag found in HTML")
            return False
        
        body_start = body_start + html_content[body_start:].find('>') + 1
        body_end = html_content.find('</body>')
        if body_end == -1:
            print(f"            ❌ No </body> tag found in HTML")
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
        
        # Remove fetch calls to shared components
        body_content = re.sub(r'fetch\([\'"][^\'"]*\.\./shared/[^\'"]*[\'"]\)', '// fetch call removed - component already embedded', body_content)
        
        # Remove script blocks that load shared components
        body_content = re.sub(r'<script>[^<]*fetch\([^<]*\.\./shared/[^<]*</script>', '<!-- Shared component loading script removed -->', body_content, flags=re.DOTALL)
        
        # Remove external script tags (script tags with src attribute)
        body_content = re.sub(r'<script[^>]*src=[^>]*></script>', '<!-- External script removed -->', body_content)
        
        # Remove any remaining references to ../shared/ paths (handle multiple levels)
        body_content = re.sub(r'\.\./shared/', '// shared path removed - components embedded', body_content)
        
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
    <title>Bearing Specifications Hub | Technical Data & Performance Grades | RHD Bearings</title>
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

/* SpecsHubPage Styles */
{styles_css}
    </style>
</head>
<body>
{body_content}
{script_content}
</body>
</html>'''
        
        # Create deployment directory
        deployment_dir = Path(f"deployment/specs")
        deployment_dir.mkdir(parents=True, exist_ok=True)
        
        # Save standalone SpecsHubPage
        output_file = deployment_dir / "index.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(standalone_html)
        
        print(f"            ✅ Created standalone SpecsHubPage: {output_file}")
        return True
        
    except Exception as e:
        print(f"            ❌ Error creating standalone SpecsHubPage: {e}")
        return False

def create_standalone_model_page(model_name, model_dir, series):
    """Helper function for create_standalone_pages() - creates standalone individual model pages"""
    try:
        # Instead of reading the existing HTML file, regenerate it from the template
        # to ensure all template processing (including alternate_model_number) is applied
        json_file = Path(f"models/{model_name}.json")
        template_file = Path("webpages/templates/index_new_claude.html")
        
        if not json_file.exists():
            print(f"            ❌ JSON file not found: {json_file}")
            return False
        
        if not template_file.exists():
            print(f"            ❌ Template file not found: {template_file}")
            return False
        
        # Generate HTML from template
        generator = UniversalBearingPageGenerator(str(json_file), str(template_file), str(model_dir / "index.html"))
        success = generator.generate_page()
        
        if not success:
            print(f"            ❌ Failed to generate HTML from template")
            return False
        
        # Now read the generated HTML file
        index_file = model_dir / "index.html"
        with open(index_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
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
            print(f"            ⚠️  styles.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "navbar.css", 'r', encoding='utf-8') as f:
                navbar_css = f.read()
        except:
            print(f"            ⚠️  navbar.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "footer.css", 'r', encoding='utf-8') as f:
                footer_css = f.read()
        except:
            print(f"            ⚠️  footer.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "cta-model.css", 'r', encoding='utf-8') as f:
                cta_css = f.read()
        except:
            print(f"            ⚠️  cta-model.css not found, using empty CSS")
        
        try:
            with open(shared_dir / "watermark.css", 'r', encoding='utf-8') as f:
                watermark_css = f.read()
            print(f"            ✅ Loaded watermark CSS: {len(watermark_css)} characters")
        except:
            print(f"            ⚠️  watermark.css not found, using empty CSS")
            watermark_css = ""
        
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
            print(f"            ⚠️  navbar.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "footer.html", 'r', encoding='utf-8') as f:
                footer_html = f.read()
        except:
            print(f"            ⚠️  footer.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "cta-model.html", 'r', encoding='utf-8') as f:
                cta_html = f.read()
                # Replace [MODEL] placeholder with actual model number
                cta_html = cta_html.replace('[MODEL]', model_name)
        except:
            print(f"            ⚠️  cta-model.html not found, using empty HTML")
        
        try:
            with open(shared_dir / "watermark.html", 'r', encoding='utf-8') as f:
                watermark_html = f.read()
            print(f"            ✅ Loaded watermark HTML: {len(watermark_html)} characters")
        except:
            print(f"            ⚠️  watermark.html not found, using empty HTML")
            watermark_html = ""
        
        # Extract body content and scripts
        body_start = html_content.find('<body')
        if body_start == -1:
            print(f"            ❌ No <body> tag found in HTML")
            return False
        
        body_tag_end = body_start + html_content[body_start:].find('>') + 1
        body_end = html_content.find('</body>')
        if body_end == -1:
            print(f"            ❌ No </body> tag found in HTML")
            return False
        
        # Extract the body tag with attributes and the body content
        body_tag = html_content[body_start:body_tag_end]
        body_content = html_content[body_tag_end:body_end].strip()
        
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
        
        # Remove fetch calls to shared components
        body_content = re.sub(r'fetch\([\'"][^\'"]*\.\./shared/[^\'"]*[\'"]\)', '// fetch call removed - component already embedded', body_content)
        
        # Remove script blocks that load shared components
        body_content = re.sub(r'<script>[^<]*fetch\([^<]*\.\./shared/[^<]*</script>', '<!-- Shared component loading script removed -->', body_content, flags=re.DOTALL)
        
        # Remove external script tags (script tags with src attribute)
        body_content = re.sub(r'<script[^>]*src=[^>]*></script>', '<!-- External script removed -->', body_content)
        
        # Remove any remaining references to ../shared/ paths (handle multiple levels)
        body_content = re.sub(r'\.\./shared/', '// shared path removed - components embedded', body_content)
        
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
    <title>{model_name} Deep Groove Ball Bearing | RHD Bearings</title>
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
{body_tag}
{body_content}
{script_content}
</body>
</html>'''
        
        # Create deployment directory
        deployment_dir = Path(f"deployment/{series}/{series}-internal-pages-deployment")
        deployment_dir.mkdir(parents=True, exist_ok=True)
        
        # Save standalone page
        output_file = deployment_dir / model_name / "index.html"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(standalone_html)
        
        print(f"            ✅ Created standalone page: {output_file}")
        return True
        
    except Exception as e:
        print(f"            ❌ Error creating standalone page: {e}")
        return False

def upload_pages(selected_series=None):
    """
    STEP 3: Upload standalone pages to server
    
    This function:
    1. Uploads the main series page to the server
    2. Reads standalone HTML files from deployment/{series}/{series}-internal-pages-deployment/
    3. Uploads each model page to the server using curl_upload
    4. Creates proper directory structure on server
    """
    print(f"\n🚀 UPLOADING PAGES TO SERVER")
    print(f"==================================================")
    
    series_mapping = get_series_mapping()
    failed_count = 0
    successful_count = 0
    
    for series, series_dir_name in series_mapping.items():
        if selected_series is None or series in selected_series:
            # Special handling for SpecsHubPage (single page upload)
            if series == "specs-hub":
                print(f"\n🔧 Uploading SpecsHubPage...")
                deployment_dir = Path(f"deployment/specs")
                index_file = deployment_dir / "index.html"
                
                if not index_file.exists():
                    print(f"   ❌ SpecsHubPage index.html not found: {index_file}")
                    failed_count += 1
                    continue
                
                print(f"   📤 Uploading SpecsHubPage...")
                
                try:
                    # Upload to both specs.html and specs/index.html for maximum compatibility
                    print(f"      📤 Uploading to specs.html...")
                    success1 = curl_upload('specs')
                    
                    # Temporarily modify the upload path for specs/index.html
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("curl_upload", "deployment/curl_upload.py")
                    curl_upload_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(curl_upload_module)
                    original_get_upload_paths = curl_upload_module.get_upload_paths
                    
                    def modified_get_upload_paths(page_type):
                        local_file, remote_file, clean_url = original_get_upload_paths(page_type)
                        if page_type == 'specs':
                            remote_file = 'specs/index.html'
                            clean_url = 'https://rhdbearings.com/specs/'
                        return local_file, remote_file, clean_url
                    
                    curl_upload_module.get_upload_paths = modified_get_upload_paths
                    print(f"      📤 Uploading to specs/index.html...")
                    success2 = curl_upload_module.curl_upload('specs')
                    
                    # Restore original function
                    curl_upload_module.get_upload_paths = original_get_upload_paths
                    
                    if success1 and success2:
                        print(f"      ✅ Successfully uploaded SpecsHubPage to both locations")
                        print(f"      🔗 URLs: https://rhdbearings.com/specs.html and https://rhdbearings.com/specs/")
                        successful_count += 1
                    else:
                        print(f"      ⚠️  Partial upload success - check individual results above")
                        successful_count += 1
                    
                except Exception as e:
                    print(f"      ❌ Error uploading SpecsHubPage: {e}")
                    failed_count += 1
                continue
            
            deployment_dir = Path(f"deployment/{series}/{series}-internal-pages-deployment")
            if not deployment_dir.exists():
                print(f"⚠️  Deployment directory not found: {deployment_dir}")
                continue
            
            # Get all model directories
            model_dirs = [d for d in deployment_dir.iterdir() if d.is_dir()]
            if not model_dirs:
                print(f"⚠️  No model directories found in {deployment_dir}")
                continue
            
            print(f"\n🔧 Uploading {series} series...")
            print(f"   📋 Found {len(model_dirs)} model directories")
            
            for model_dir in model_dirs:
                model_name = model_dir.name
                index_file = model_dir / "index.html"
                
                if not index_file.exists():
                    print(f"      ❌ index.html not found for {model_name}")
                    failed_count += 1
                    continue
                
                print(f"      📤 Uploading {model_name}...")
                
                try:
                    # Use the imported curl_upload function (run from root directory)
                    success = curl_upload(model_name)
                    
                    if success:
                        print(f"         ✅ Successfully uploaded {model_name}")
                        # Display clean URL with hyphens instead of spaces
                        clean_url_display = f"https://rhdbearings.com/specs/{series}/{model_name.replace(' ', '-')}/"
                        print(f"         🔗 URL: {clean_url_display}")
                        successful_count += 1
                    else:
                        print(f"         ❌ Failed to upload {model_name}")
                        failed_count += 1
                        
                except Exception as e:
                    print(f"         ❌ Error uploading {model_name}: {e}")
                    failed_count += 1
    
    print(f"\n==================================================")
    print(f"📊 UPLOAD SUMMARY")
    print(f"==================================================")
    print(f"✅ Successfully uploaded: {successful_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"🎯 Total: {successful_count + failed_count}")
    
    if failed_count == 0:
        print(f"\n🎉 All {successful_count} pages uploaded successfully!")
        print(f"✅ Your website is fully updated!")
        return True
    else:
        print(f"\n⚠️  {failed_count} page(s) failed to upload!")
        return False

def upload_main_pages_only(selected_series=None):
    """
    Upload only main series pages (not individual model pages)
    
    This function:
    1. Uploads only the main series pages to the server
    2. Skips all individual model pages
    3. Much faster than full upload when you only need to update main pages
    """
    print(f"\n🚀 UPLOADING MAIN SERIES PAGES ONLY")
    print(f"==================================================")
    
    series_mapping = get_series_mapping()
    failed_count = 0
    successful_count = 0
    
    for series, series_dir_name in series_mapping.items():
        if selected_series is None or series in selected_series:
            print(f"\n🔧 Uploading {series} main page...")
            
            # Special handling for SpecsHubPage
            if series == "specs-hub":
                deployment_dir = Path(f"deployment/specs")
                index_file = deployment_dir / "index.html"
                
                if not index_file.exists():
                    print(f"   ❌ SpecsHubPage index.html not found: {index_file}")
                    failed_count += 1
                    continue
                
                print(f"   📤 Uploading SpecsHubPage...")
                
                try:
                    # Upload to both specs.html and specs/index.html for maximum compatibility
                    print(f"      📤 Uploading to specs.html...")
                    success1 = curl_upload('specs')
                    
                    # Temporarily modify the upload path for specs/index.html
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("curl_upload", "deployment/curl_upload.py")
                    curl_upload_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(curl_upload_module)
                    original_get_upload_paths = curl_upload_module.get_upload_paths
                    
                    def modified_get_upload_paths(page_type):
                        local_file, remote_file, clean_url = original_get_upload_paths(page_type)
                        if page_type == 'specs':
                            remote_file = 'specs/index.html'
                            clean_url = 'https://rhdbearings.com/specs/'
                        return local_file, remote_file, clean_url
                    
                    curl_upload_module.get_upload_paths = modified_get_upload_paths
                    print(f"      📤 Uploading to specs/index.html...")
                    success2 = curl_upload_module.curl_upload('specs')
                    
                    # Restore original function
                    curl_upload_module.get_upload_paths = original_get_upload_paths
                    
                    if success1 and success2:
                        print(f"      ✅ Successfully uploaded SpecsHubPage to both locations")
                        print(f"      🔗 URLs: https://rhdbearings.com/specs.html and https://rhdbearings.com/specs/")
                        successful_count += 1
                    else:
                        print(f"      ⚠️  Partial upload success - check individual results above")
                        successful_count += 1
                    
                except Exception as e:
                    print(f"      ❌ Error uploading SpecsHubPage: {e}")
                    failed_count += 1
                continue
            
            # Upload main series page
            deployment_dir = Path(f"deployment/{series}")
            index_file = deployment_dir / "index.html"
            
            if not index_file.exists():
                print(f"   ❌ Main series page not found: {index_file}")
                failed_count += 1
                continue
            
            try:
                # Extract the series number for curl_upload (e.g., "6200-series" -> "6200")
                series_number = series.replace('-series', '')
                
                # Use the series number to upload main page
                success = curl_upload(series_number)
                
                if success:
                    print(f"   ✅ Successfully uploaded {series} main page")
                    print(f"   🔗 URL: https://rhdbearings.com/specs/{series}.html")
                    successful_count += 1
                else:
                    print(f"   ❌ Failed to upload {series} main page")
                    failed_count += 1
                    
            except Exception as e:
                print(f"   ❌ Error uploading {series} main page: {e}")
                failed_count += 1
    
    print(f"\n==================================================")
    print(f"📊 MAIN PAGES UPLOAD SUMMARY")
    print(f"==================================================")
    print(f"✅ Successfully uploaded: {successful_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"🎯 Total: {successful_count + failed_count}")
    
    if failed_count == 0:
        print(f"\n🎉 All {successful_count} main pages uploaded successfully!")
        print(f"✅ Main series pages are updated!")
        return True
    else:
        print(f"\n⚠️  {failed_count} main page(s) failed to upload!")
        return False

def create_standalone_main_pages_only(selected_series=None):
    """
    Create standalone pages for main series pages only (not individual model pages)
    
    This function:
    1. Creates standalone main series pages only (from existing HTML/CSS)
    2. Skips all individual model pages
    3. Much faster than full standalone creation when you only need main pages
    4. Outputs to deployment/{series}-series/
    """
    print(f"\n🚀 CREATING STANDALONE MAIN PAGES ONLY")
    print(f"==================================================")
    
    series_mapping = get_series_mapping()
    failed_count = 0
    successful_count = 0
    
    for series, series_dir_name in series_mapping.items():
        if selected_series is None or series in selected_series:
            print(f"\n🔧 Creating standalone main page for {series} series...")
            
            # Special handling for SpecsHubPage (single page)
            if series == "specs-hub":
                print(f"   📋 Processing SpecsHubPage (single page)...")
                try:
                    success = create_standalone_specs_hub_page(series, series_dir_name)
                    if success:
                        print(f"      ✅ Successfully created standalone SpecsHubPage")
                        successful_count += 1
                    else:
                        print(f"      ❌ Failed to create standalone SpecsHubPage")
                        failed_count += 1
                except Exception as e:
                    print(f"      ❌ Error processing SpecsHubPage: {e}")
                    failed_count += 1
                continue
            
            # Create standalone main series page only (skip individual models)
            print(f"   📋 Processing main series page only...")
            try:
                success = create_standalone_main_series_page(series, series_dir_name)
                if success:
                    print(f"      ✅ Successfully created standalone main series page")
                    successful_count += 1
                else:
                    print(f"      ❌ Failed to create standalone main series page")
                    failed_count += 1
            except Exception as e:
                print(f"      ❌ Error processing main series page: {e}")
                failed_count += 1
    
    print(f"\n==================================================")
    print(f"📊 STANDALONE MAIN PAGES CREATION SUMMARY")
    print(f"==================================================")
    print(f"✅ Successfully created: {successful_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"🎯 Total: {successful_count + failed_count}")
    
    if failed_count == 0:
        print(f"\n🎉 All {successful_count} standalone main pages created successfully!")
        return True
    else:
        print(f"\n⚠️  {failed_count} main page(s) failed to create. Check the errors above.")
        return False

def main():
    """
    Main function - Complete workflow execution
    
    This function orchestrates the entire 3-step process:
    1. Generate HTML pages from JSON files
    2. Create standalone pages with embedded CSS
    3. Upload all pages to the server
    """
    parser = argparse.ArgumentParser(description='Generate and deploy universal bearing series pages')
    parser.add_argument('--6200-series', action='store_true', help='Process only 6200 series')
    parser.add_argument('--6300-series', action='store_true', help='Process only 6300 series')
    parser.add_argument('--16000-series', action='store_true', help='Process only 16000 series')
    parser.add_argument('--62200-series', action='store_true', help='Process only 62200 series')
    parser.add_argument('--62300-series', action='store_true', help='Process only 62300 series')
    parser.add_argument('--6800-series', action='store_true', help='Process only 6800 series')
    parser.add_argument('--6900-series', action='store_true', help='Process only 6900 series')
    parser.add_argument('--6000-series', action='store_true', help='Process only 6000 series')
    parser.add_argument('--specs-hub', action='store_true', help='Process only SpecsHubPage')
    parser.add_argument('--generate-only', action='store_true', help='Run only step 1 (HTML generation)')
    parser.add_argument('--standalone-only', action='store_true', help='Run only step 2 (standalone page creation)')
    parser.add_argument('--upload-only', action='store_true', help='Run only step 3 (server upload)')
    parser.add_argument('--upload-main-only', action='store_true', help='Upload only main series pages (not individual model pages)')
    parser.add_argument('--standalone-main-only', action='store_true', help='Create standalone pages for main series pages only (not individual model pages)')
    
    args = parser.parse_args()
    
    # Determine which series to process
    selected_series = []
    if args.__dict__.get('6200_series'):
        selected_series.append('6200-series')
    if args.__dict__.get('6300_series'):
        selected_series.append('6300-series')
    if args.__dict__.get('16000_series'):
        selected_series.append('16000-series')
    if args.__dict__.get('62200_series'):
        selected_series.append('62200-series')
    if args.__dict__.get('62300_series'):
        selected_series.append('62300-series')
    if args.__dict__.get('6800_series'):
        selected_series.append('6800-series')
    if args.__dict__.get('6900_series'):
        selected_series.append('6900-series')
    if args.__dict__.get('6000_series'):
        selected_series.append('6000-series')
    if args.__dict__.get('specs_hub'):
        selected_series.append('specs-hub')
    
    # If no specific series selected, process all
    if not selected_series:
        selected_series = None
        print("🚀 UNIVERSAL BEARING SERIES COMPLETE WORKFLOW")
        print("=" * 60)
        print("This script will process ALL non-miniature series:")
        print("• 6200, 6300, 16000, 62200, 62300, 6800, 6900, 6000 series")
        print("• SpecsHubPage")
        print("=" * 60)
    else:
        print(f"🚀 PROCESSING SELECTED SERIES: {', '.join(selected_series)}")
        print("=" * 60)
    
    print("\n📋 REQUIREMENTS:")
    print("   • .env file with FTP credentials (FTP_PASSWORD)")
    print("   • deployment/curl_upload.py available")
    print("   • All directories and files in expected locations")
    print("   • Run from root workspace directory")
    print("=" * 60)
    
    # Check if running specific steps only
    if args.generate_only:
        print("\n📝 RUNNING GENERATION STEP ONLY")
        print("-" * 40)
        success = generate_universal_pages(selected_series)
        sys.exit(0 if success else 1)
        
    elif args.standalone_only:
        print("\n📝 RUNNING STANDALONE PAGE CREATION ONLY")
        print("-" * 40)
        success = create_standalone_pages(selected_series)
        sys.exit(0 if success else 1)
        
    elif args.upload_only:
        print("\n📝 RUNNING UPLOAD STEP ONLY")
        print("-" * 40)
        success = upload_pages(selected_series)
        sys.exit(0 if success else 1)
        
    elif args.upload_main_only:
        print("\n📝 UPLOADING MAIN SERIES PAGES ONLY")
        print("-" * 40)
        success = upload_main_pages_only(selected_series)
        sys.exit(0 if success else 1)
        
    elif args.standalone_main_only:
        print("\n📝 CREATING STANDALONE MAIN PAGES ONLY")
        print("-" * 40)
        success = create_standalone_main_pages_only(selected_series)
        sys.exit(0 if success else 1)
    
    # Step 1: Generate HTML pages
    print("\n📝 STEP 1: GENERATING HTML PAGES")
    print("-" * 40)
    success = generate_universal_pages(selected_series)
    
    if not success:
        print("💥 HTML generation failed. Stopping workflow.")
        sys.exit(1)
    
    # Step 2: Create standalone pages
    print("\n📝 STEP 2: CREATING STANDALONE PAGES")
    print("-" * 40)
    success = create_standalone_pages(selected_series)
    
    if not success:
        print("💥 Standalone page creation failed. Stopping workflow.")
        sys.exit(1)
    
    # Step 3: Upload pages
    print("\n📝 STEP 3: UPLOADING PAGES TO SERVER")
    print("-" * 40)
    success = upload_pages(selected_series)
    
    if not success:
        print("💥 Upload failed. Check the errors above.")
        sys.exit(1)
    
    # All steps completed successfully
    print("\n" + "=" * 60)
    print("🎉 COMPLETE WORKFLOW SUCCESSFUL!")
    print("=" * 60)
    print("✅ All selected series pages have been:")
    print("   • Generated from JSON files")
    print("   • Converted to standalone pages (completely independent)")
    print("   • Uploaded to the server")
    print("\n🌐 Your website is now fully updated!")
    print("=" * 60)

if __name__ == "__main__":
    main()
