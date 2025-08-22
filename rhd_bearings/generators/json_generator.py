"""
Main JSON generator for bearing catalog.
"""

import json
from typing import Dict, List, Any
from pathlib import Path

from ..core.bearing import Bearing
from ..core.config import Config
from ..utils.data_loader import DataLoader
from ..utils.lookups import LookupManager
from .content_generator import ContentGenerator


class BearingJSONGenerator:
    """Generates complete bearing catalog JSON with all metadata and optimizations."""
    
    def __init__(self):
        """Initialize the generator with data sources."""
        # Ensure directories exist
        Config.ensure_directories()
        
        # Initialize lookup manager
        self.lookup_manager = LookupManager(
            Config.FILES["clearance_lookup"],
            Config.FILES["vibration_lookup"],
            Config.FILES["noise_lookup"]
        )
        
        # Load witty descriptions
        self.witty_descriptions = DataLoader.load_witty_descriptions(
            Config.FILES["witty_descriptions"]
        )
        
        # Content generator
        self.content_generator = ContentGenerator()
    
    def load_bearings(self) -> List[Bearing]:
        """
        Load all bearings from the database.
        
        Returns:
            List of Bearing instances
        """
        bearing_data = DataLoader.load_bearing_database(Config.FILES["bearing_database"])
        return [Bearing.from_dict(data) for data in bearing_data]
    
    def generate_bearing_json(self, bearing: Bearing, all_models: List[str]) -> Dict[str, Any]:
        """
        Generate complete JSON for a single bearing.
        
        Args:
            bearing: Bearing instance
            all_models: List of all bearing model numbers for cross-references
            
        Returns:
            Complete bearing JSON dictionary
        """
        # Start with basic bearing data
        bearing_data = bearing.to_dict()
        
        # Add enhanced content
        bearing_data.update({
            "enhanced_description": self.content_generator.generate_witty_description(
                bearing, self.witty_descriptions
            ),
            "material": self._generate_material_info(),
            "technical_drawing": self.content_generator.generate_technical_drawing_info(bearing),
            "applications": self._generate_applications(bearing),
            "vibration": self.lookup_manager.get_vibration_data(bearing.dimensions.bore_diameter),
            "noise": self.lookup_manager.get_noise_data(
                bearing.dimensions.bore_diameter, 
                bearing.model_number
            ),
            "clearance": self.lookup_manager.get_clearance_data(bearing.dimensions.bore_diameter),
            "seal_options": self._generate_seal_options(bearing),
            "seo_metadata": self.content_generator.generate_seo_metadata(bearing),
            "pricing_and_availability": self._generate_pricing_info(bearing),
            "cross_references": self._generate_cross_references(bearing, all_models),
            "llm_optimization": self.content_generator.generate_llm_content(bearing),
            "faq": self._generate_faq(bearing)
        })
        
        return bearing_data
    
    def generate_complete_catalog(self) -> Dict[str, Any]:
        """
        Generate complete bearing catalog JSON.
        
        Returns:
            Complete catalog dictionary
        """
        print("Loading bearings from database...")
        bearings = self.load_bearings()
        all_models = [b.model_number for b in bearings]
        
        print(f"Found {len(bearings)} bearings to process")
        
        catalog_data = {
            "company_metadata": self._generate_company_metadata(),
            "bearings": []
        }
        
        for bearing in bearings:
            print(f"Processing bearing {bearing.model_number}...")
            bearing_json = self.generate_bearing_json(bearing, all_models)
            catalog_data["bearings"].append(bearing_json)
        
        return catalog_data
    
    def save_catalog(self, output_path: Path = None) -> None:
        """
        Generate and save complete catalog to file.
        
        Args:
            output_path: Optional custom output path
        """
        catalog_data = self.generate_complete_catalog()
        
        if output_path is None:
            output_path = Config.OUTPUT_FILES["bearings_catalog"]
        
        DataLoader.save_json(catalog_data, output_path)
        
        print(f"Generated complete bearing JSON: {output_path}")
        print(f"Total bearings processed: {len(catalog_data['bearings'])}")
        
        # Print summary
        for bearing in catalog_data['bearings']:
            model = bearing['model_number']
            dims = bearing['dimensions']
            bore = dims['bore_diameter_d_mm']
            outer = dims['outer_diameter_D_mm'] 
            width = dims['width_B_mm']
            print(f"- {model}: {bore}x{outer}x{width}mm")
    
    def _generate_material_info(self) -> Dict[str, str]:
        """Generate material information."""
        return {
            "grade": "GCr15 (100Cr6)",
            "composition": "Carbon: 0.95-1.05%, Chromium: 1.40-1.65%, Silicon: 0.15-0.35%"
        }
    
    def _generate_applications(self, bearing: Bearing) -> Dict[str, List[str]]:
        """Generate applications for a bearing."""
        # Base applications (could be loaded from data file)
        base_applications = {
            "automotive": [
                "Engine components",
                "Transmission systems", 
                "Wheel assemblies",
                "Power steering systems"
            ],
            "industrial": [
                "Electric motors",
                "Pumps and compressors",
                "Machine tools",
                "Conveyor systems"
            ],
            "household": [
                "Appliance motors",
                "Fan assemblies",
                "Exercise equipment",
                "Small machinery"
            ]
        }
        
        return self.content_generator.generate_applications(bearing, base_applications)
    
    def _generate_seal_options(self, bearing: Bearing) -> Dict[str, Any]:
        """Generate seal options for a bearing."""
        model = bearing.model_number
        
        return {
            "open_bearing": {
                "designation": model,
                "description": "Open bearing without seals for easy maintenance and high-speed applications",
                "advantages": ["Easy relubrication", "High speed capability", "Lower torque"],
                "applications": ["Clean environments", "Frequent maintenance schedules"]
            },
            "sealed_options": {
                "single_seal": {
                    "designation": f"{model}-2RS1",
                    "description": "Single lip rubber seal on one side",
                    "protection_level": "Basic contamination protection"
                },
                "double_seal": {
                    "designation": f"{model}-2RS",
                    "description": "Double lip rubber seals on both sides", 
                    "protection_level": "Maximum contamination protection"
                }
            }
        }
    
    def _generate_pricing_info(self, bearing: Bearing) -> Dict[str, Any]:
        """Generate pricing and availability information."""
        model = bearing.model_number
        
        return {
            "currency": "INR",
            "list_price": None,
            "quote_required": True,
            "price_notes": f"Get instant {model} pricing and availability",
            "minimum_order_quantity": 1,
            "availability": {
                "stock_status": "Available for immediate dispatch",
                "lead_time": "Same day dispatch for orders before 2 PM",
                "bulk_availability": "Large quantities available - contact for bulk pricing",
                "custom_orders": "Custom specifications and modifications available",
                "call_to_action": {
                    "primary": "📞 Call +91-9702081858 for immediate pricing and availability",
                    "secondary": "📧 Email sales@rhdenterprise.in for detailed quotation",
                    "oem_sales": "🏭 OEM/Bulk orders: oemsales@rhdenterprise.in",
                    "urgency": "Need it today? Call now - we dispatch same day!"
                }
            }
        }
    
    def _generate_cross_references(self, bearing: Bearing, all_models: List[str]) -> Dict[str, Any]:
        """Generate cross-references to related bearings."""
        model = bearing.model_number
        series = bearing.series_name
        
        # Find related models in the same series
        related_models = []
        for other_model in all_models:
            if other_model != model:
                other_bearing = Bearing(
                    model_number=other_model,
                    dimensions=bearing.dimensions,  # Placeholder
                    load_ratings=bearing.load_ratings,  # Placeholder  
                    speed_limits=bearing.speed_limits,  # Placeholder
                    weight_kg=bearing.weight_kg  # Placeholder
                )
                if other_bearing.series_name == series:
                    related_models.append(other_model)
        
        # Limit to first 5 related models
        related_models = related_models[:5]
        
        return {
            "related_models": related_models,
            "series_alternatives": self._get_series_alternatives(series),
            "application_specific_alternatives": {
                "high_temperature": f"{model} with high-temp grease",
                "high_speed": f"{model} with precision tolerance", 
                "corrosive_environment": f"{model} with stainless steel option"
            }
        }
    
    def _get_series_alternatives(self, current_series: str) -> List[str]:
        """Get alternative bearing series."""
        series_map = {
            "6000": ["6200 series (heavier duty)", "miniature series (lighter duty)"],
            "6200": ["6000 series (lighter duty)", "6300 series (heavier duty)"],
            "6300": ["6200 series (lighter duty)", "62200 series (deeper section)"],
            "miniature": ["6000 series (heavier duty)", "6800 series (thin section)"],
            "62200": ["6200 series (standard)", "62300 series (heavier duty)"],
            "62300": ["62200 series (lighter duty)", "6300 series (standard)"],
            "16000": ["6000 series (standard)", "6800 series (thin section)"],
            "6800": ["6000 series (standard)", "6900 series (similar thin)"],
            "6900": ["6800 series (similar thin)", "6000 series (standard)"]
        }
        
        return series_map.get(current_series, [])
    
    def _generate_faq(self, bearing: Bearing) -> Dict[str, List[Dict[str, str]]]:
        """Generate comprehensive FAQ for a bearing."""
        model = bearing.model_number
        bore = bearing.dimensions.bore_diameter
        outer = bearing.dimensions.outer_diameter
        width = bearing.dimensions.width
        dynamic_load = bearing.load_ratings.dynamic_load
        grease_rpm = bearing.speed_limits.grease_rpm
        
        return {
            "technical_specifications": [{
                "question": f"Is the {model} bearing the right size for my {bore}mm shaft application?",
                "answer": f"Yes! The {model} bearing is specifically designed for {bore}mm shafts with an outer diameter of {outer}mm and {width}mm width. It's perfect for applications where you need reliable performance with {dynamic_load}kN load capacity."
            }],
            "application_suitability": [{
                "question": f"When should I choose the {model} over other bearing options?",
                "answer": f"Choose the {model} when you need a {bore}mm bearing with {dynamic_load}kN capacity. It's perfect when your application requires speeds up to {grease_rpm} RPM with grease lubrication."
            }],
            "selection_guidance": [{
                "question": f"How do I know if the {model} is the right bearing for my application?",
                "answer": f"Ask yourself: Do I have a {bore}mm shaft? Do I need {dynamic_load}kN load capacity? Will speeds stay under {grease_rpm} RPM? If yes, the {model} is perfect!"
            }]
        }
    
    def _generate_company_metadata(self) -> Dict[str, Any]:
        """Generate company metadata."""
        return {
            "name": Config.COMPANY["name"],
            "website": Config.COMPANY["website"],
            "contact": {
                "email": Config.COMPANY["email"],
                "oem_sales_email": Config.COMPANY["oem_email"],
                "phone": Config.COMPANY["phone"]
            },
            "address": Config.COMPANY["address"],
            "certifications": ["ISO 9001:2015"],
            "established": "Premium bearing manufacturer",
            "specialization": "Deep groove ball bearings for automotive, industrial, and household applications"
        }
