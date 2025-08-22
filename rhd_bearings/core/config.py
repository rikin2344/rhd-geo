"""
Configuration settings for RHD Bearings catalog generator.
"""

import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration management for the bearing catalog generator."""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DATA_DIR = PROJECT_ROOT / "rhd_bearings" / "data"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    DOCS_DIR = PROJECT_ROOT / "docs"
    
    # Company information
    COMPANY = {
        "name": "RHD Bearings",
        "website": "https://rhdbearings.com",
        "email": "sales@rhdenterprise.in",
        "oem_email": "oemsales@rhdenterprise.in",
        "phone": "+91-9702081858",
        "address": {
            "street": "203 Vihar Estate, Off. Saki Vihar Road",
            "area": "Next to Autohanger, Sakinaka",
            "city": "Andheri East Mumbai",
            "postal_code": "400072",
            "country": "India"
        }
    }
    
    # Technical drawing configuration
    TECHNICAL_DRAWING = {
        "base_url": "https://rhdbearings.com/wp-content/uploads/2025/08/0901d19680398aff_svg_preview.svg",
        "file_format": "SVG",
        "drawing_type": "Cross-sectional technical diagram"
    }
    
    # URL structure
    URL_STRUCTURE = {
        "base_url": "https://rhdbearings.com",
        "series_pattern": "/{series}",
        "bearing_pattern": "/{series}/{model}"
    }
    
    # File paths
    FILES = {
        "bearing_database": DATA_DIR / "bearing_database.json",
        "clearance_lookup": DATA_DIR / "clearance_lookup_table.json",
        "vibration_lookup": DATA_DIR / "vibration_lookup_table.json", 
        "noise_lookup": DATA_DIR / "noise_lookup_table.json",
        "witty_descriptions": DATA_DIR / "witty_bearing_descriptions.json",
        "extraction_guide": DATA_DIR / "bearing_extraction_guide.md"
    }
    
    # Output files
    OUTPUT_FILES = {
        "bearings_catalog": OUTPUT_DIR / "generated_bearings_complete.json",
        "series_pages": OUTPUT_DIR / "enhanced_bearing_series_pages.json"
    }
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all necessary directories exist."""
        for directory in [cls.DATA_DIR, cls.OUTPUT_DIR, cls.DOCS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_series_url(cls, model: str) -> str:
        """Get the series URL slug for a bearing model."""
        model = model.strip()
        
        # 3-digit miniature bearings
        if len(model) == 3:
            return "miniature-bearings"
        
        # 5-digit series
        elif model.startswith('6230') or model.startswith('6231') or model.startswith('6232'):
            return "62300-series"
        elif model.startswith('6220') or model.startswith('6221') or model.startswith('6222'):
            return "62200-series"
        
        # 4-digit series
        elif model.startswith('1600'):
            return "16000-series"
        elif model.startswith('600') and len(model) == 4:
            return "6000-series"
        elif model.startswith('620') or model.startswith('621') or model.startswith('622'):
            return "6200-series"
        elif model.startswith('630') or model.startswith('631') or model.startswith('632'):
            return "6300-series"
        elif model.startswith('68'):
            return "6800-series"
        elif model.startswith('69'):
            return "6900-series"
        
        # Default fallback
        else:
            return "bearings"
    
    @classmethod
    def get_canonical_url(cls, model: str) -> str:
        """Generate canonical URL for a bearing model."""
        series = cls.get_series_url(model)
        return f"{cls.URL_STRUCTURE['base_url']}/{series}/{model}"
