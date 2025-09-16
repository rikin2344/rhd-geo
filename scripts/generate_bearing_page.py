#!/usr/bin/env python3
"""
Bearing Page Generator Script

This script takes a bearing JSON file and an HTML template, then generates
a complete HTML page by replacing all placeholders with actual data.
"""

import json
import sys
import os
import re
from pathlib import Path

class BearingPageGenerator:
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
            
            # 8. Replace simple placeholders
            content = self._replace_simple_placeholders(content)
            
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
    
    def _replace_simple_placeholders(self, content: str) -> str:
        """Replace simple {{key}} placeholders"""
        # Handle keywords array
        if 'seo_metadata' in self.data and 'keywords' in self.data['seo_metadata']:
            keywords = self.data['seo_metadata']['keywords']
            if isinstance(keywords, list):
                keywords_string = ', '.join(keywords)
                content = content.replace('{{seo_metadata.keywords_string}}', keywords_string)
        
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

def main():
    if len(sys.argv) != 4:
        print("Usage: python generate_bearing_page.py <bearing_json> <template_html> <output_html>")
        print("Example: python generate_bearing_page.py models/604.json webpages/internalwebpages/specs/miniature-series/template/claude_template/index_new_claude.html webpages/internalwebpages/specs/miniature-series/604/index.html")
        sys.exit(1)
    
    json_file = sys.argv[1]
    template_file = sys.argv[2]
    output_file = sys.argv[3]
    
    # Validate input files
    if not os.path.exists(json_file):
        print(f"❌ JSON file not found: {json_file}")
        sys.exit(1)
    
    if not os.path.exists(template_file):
        print(f"❌ Template file not found: {template_file}")
        sys.exit(1)
    
    # Generate the page
    generator = BearingPageGenerator(json_file, template_file, output_file)
    if generator.generate_page():
        print("🎉 Bearing page generated successfully!")
    else:
        print("💥 Failed to generate bearing page")
        sys.exit(1)

if __name__ == "__main__":
    main()
