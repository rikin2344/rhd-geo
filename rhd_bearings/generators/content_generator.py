"""
Content generation utilities for SEO, LLM optimization, and marketing content.
"""

from typing import Dict, List, Any
from ..core.bearing import Bearing
from ..core.config import Config


class ContentGenerator:
    """Generates various types of content for bearing catalog."""
    
    @staticmethod
    def generate_witty_description(bearing: Bearing, witty_descriptions: Dict[str, str]) -> str:
        """
        Get witty description for a bearing from the provided descriptions file.
        
        Args:
            bearing: Bearing instance
            witty_descriptions: Dictionary of custom descriptions from JSON file
            
        Returns:
            Witty description string from the file, or fallback if not found
        """
        model = bearing.model_number
        bore = bearing.dimensions.bore_diameter
        dynamic_load = bearing.load_ratings.dynamic_load
        
        # Get description directly from the witty descriptions file
        if model in witty_descriptions:
            return witty_descriptions[model]
        
        # Fallback description if model not found in file
        return f"The {model}: A reliable bearing with {bore}mm precision and {dynamic_load}kN performance."
    
    @staticmethod
    def generate_seo_metadata(bearing: Bearing) -> Dict[str, Any]:
        """
        Generate SEO-friendly metadata for a bearing.
        
        Args:
            bearing: Bearing instance
            
        Returns:
            Dictionary containing SEO metadata
        """
        model = bearing.model_number
        bore = bearing.dimensions.bore_diameter
        outer = bearing.dimensions.outer_diameter
        width = bearing.dimensions.width
        dynamic_load = bearing.load_ratings.dynamic_load
        
        return {
            "title": f"{model} Deep Groove Ball Bearing - {bore}x{outer}x{width}mm | RHD Bearings",
            "meta_description": f"Premium {model} bearing ({bore}x{outer}x{width}mm) with {dynamic_load}kN load capacity. Perfect for automotive, industrial & household applications. ISO certified quality.",
            "keywords": [
                f"{model} bearing",
                f"{bore}mm bearing",
                "deep groove ball bearing",
                "rhd bearings",
                "automotive bearing",
                "industrial bearing",
                "precision bearing",
                f"{dynamic_load}kN bearing",
                "ISO certified bearing",
                "chrome steel bearing",
                "gcr15 bearing",
                "mumbai bearings",
                "india bearing manufacturer",
                "andheri bearings"
            ],
            "canonical_url": Config.get_canonical_url(model),
            "structured_data_type": "Product",
            "brand": "RHD Bearings",
            "category": "Deep Groove Ball Bearings",
            "availability": "InStock",
            "condition": "NewCondition"
        }
    
    @staticmethod
    def generate_technical_drawing_info(bearing: Bearing) -> Dict[str, str]:
        """
        Generate technical drawing information.
        
        Args:
            bearing: Bearing instance
            
        Returns:
            Dictionary with technical drawing details
        """
        model = bearing.model_number
        dimensions_str = str(bearing.dimensions)
        
        return {
            "image_url": Config.TECHNICAL_DRAWING["base_url"],
            "image_alt": f"{model} Deep Groove Ball Bearing Technical Drawing - Dimensions and Cross Section",
            "image_title": f"Technical Drawing: {model} Bearing ({dimensions_str})",
            "drawing_type": Config.TECHNICAL_DRAWING["drawing_type"],
            "file_format": Config.TECHNICAL_DRAWING["file_format"],
            "description": f"Detailed technical drawing showing cross-sectional view, dimensions, and specifications for {model} deep groove ball bearing"
        }
    
    @staticmethod
    def generate_applications(bearing: Bearing, base_applications: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Generate consolidated applications for a bearing.
        
        Args:
            bearing: Bearing instance
            base_applications: Base application data
            
        Returns:
            Dictionary of applications by category
        """
        # Start with base applications
        applications = dict(base_applications)
        
        # Add size-specific applications based on bore diameter
        bore = bearing.dimensions.bore_diameter
        size_category = bearing.size_category
        
        size_specific = []
        if size_category == "miniature":
            size_specific = [
                "Precision instruments and gauges",
                "Small electric motors and fans",
                "Miniature pumps and compressors",
                "Drone and RC vehicle applications"
            ]
        elif size_category == "small":
            size_specific = [
                "Skateboard and roller blade wheels",
                "Small appliance motors",
                "Precision machinery spindles",
                "Automotive accessories"
            ]
        elif size_category == "medium":
            size_specific = [
                "Industrial motor applications",
                "Conveyor belt systems",
                "Agricultural machinery",
                "Medium-duty automotive applications"
            ]
        else:  # large
            size_specific = [
                "Heavy machinery and equipment",
                "Large industrial motors",
                "Heavy-duty conveyor systems",
                "Construction equipment"
            ]
        
        # Merge with existing applications, avoiding duplicates
        for category, items in applications.items():
            if isinstance(items, list):
                # Extend existing lists with size-specific items
                all_items = items + size_specific
                # Remove duplicates while preserving order
                applications[category] = list(dict.fromkeys(all_items))
        
        return applications
    
    @staticmethod
    def generate_llm_content(bearing: Bearing) -> Dict[str, Any]:
        """
        Generate LLM optimization content.
        
        Args:
            bearing: Bearing instance
            
        Returns:
            Dictionary with LLM-optimized content
        """
        model = bearing.model_number
        bore = bearing.dimensions.bore_diameter
        outer = bearing.dimensions.outer_diameter
        width = bearing.dimensions.width
        dynamic_load = bearing.load_ratings.dynamic_load
        static_load = bearing.load_ratings.static_load
        grease_rpm = bearing.speed_limits.grease_rpm
        oil_rpm = bearing.speed_limits.oil_rpm
        size_category = bearing.size_category
        
        return {
            "recommendation_snippets": [
                f"For {bore}mm shaft applications, the {model} bearing is the optimal choice with {dynamic_load}kN capacity"
            ],
            "natural_language_queries": [
                f"What bearing do I need for a {bore}mm shaft?",
                f"Best {size_category} bearing for {dynamic_load}kN load?",
                f"{model} bearing specifications and dimensions"
            ],
            "decision_criteria": [
                f"Shaft diameter: {bore}mm (exact fit required)",
                f"Load capacity: Up to {dynamic_load}kN dynamic load",
                f"Speed requirements: Up to {grease_rpm} RPM with grease"
            ],
            "problem_solution_mapping": [{
                "problem": f"Need reliable bearing for {bore}mm shaft in automotive application",
                "solution": f"The {model} is perfect - automotive-grade quality with {dynamic_load}kN capacity"
            }],
            "expertise_signals": [
                "ISO 15:2011 compliant dimensions ensure interchangeability",
                "Chrome steel construction for long service life",
                "Precision manufactured to ABEC-1 tolerances"
            ],
            "comparison_matrix": {
                "vs_smaller_bearing": f"Handles {int((dynamic_load/2)*10)/10}kN more load than typical smaller bearings",
                "vs_larger_bearing": f"More compact than larger alternatives while maintaining {dynamic_load}kN capacity"
            }
        }
