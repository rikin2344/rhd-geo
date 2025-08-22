"""
Bearing data model for RHD Bearings catalog.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class BearingDimensions:
    """Bearing dimensions in millimeters."""
    bore_diameter: int
    outer_diameter: int
    width: float
    
    def __str__(self) -> str:
        return f"{self.bore_diameter}x{self.outer_diameter}x{self.width}mm"


@dataclass 
class LoadRatings:
    """Bearing load ratings in kN."""
    dynamic_load: float
    static_load: float


@dataclass
class SpeedLimits:
    """Speed limits in RPM for different lubrication types."""
    grease_rpm: int
    oil_rpm: int


@dataclass
class Bearing:
    """Complete bearing specification data model."""
    model_number: str
    dimensions: BearingDimensions
    load_ratings: LoadRatings
    speed_limits: SpeedLimits
    weight_kg: float
    bearing_type: str = "Deep Groove Ball Bearing"
    
    @property
    def size_category(self) -> str:
        """Determine size category based on bore diameter."""
        bore = self.dimensions.bore_diameter
        if bore <= 5:
            return "miniature"
        elif bore <= 12:
            return "small"
        elif bore <= 25:
            return "medium"
        else:
            return "large"
    
    @property
    def series_name(self) -> str:
        """Determine bearing series from model number."""
        model = self.model_number.strip()
        
        # 3-digit miniature bearings
        if len(model) == 3:
            return "miniature"
        
        # Series identification logic
        if model.startswith('6230') or model.startswith('6231') or model.startswith('6232'):
            return "62300"
        elif model.startswith('6220') or model.startswith('6221') or model.startswith('6222'):
            return "62200"
        elif model.startswith('1600'):
            return "16000"
        elif model.startswith('600') and len(model) == 4:
            return "6000"
        elif model.startswith('620') or model.startswith('621') or model.startswith('622'):
            return "6200"
        elif model.startswith('630') or model.startswith('631') or model.startswith('632'):
            return "6300"
        elif model.startswith('68'):
            return "6800"
        elif model.startswith('69'):
            return "6900"
        else:
            return "unknown"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert bearing to dictionary format."""
        return {
            "model_number": self.model_number,
            "bearing_type": self.bearing_type,
            "dimensions": {
                "bore_diameter_d_mm": self.dimensions.bore_diameter,
                "outer_diameter_D_mm": self.dimensions.outer_diameter,
                "width_B_mm": self.dimensions.width
            },
            "load_ratings": {
                "dynamic_load_Cr_kN": self.load_ratings.dynamic_load,
                "static_load_Cor_kN": self.load_ratings.static_load
            },
            "speed_limits": {
                "grease_rpm": self.speed_limits.grease_rpm,
                "oil_rpm": self.speed_limits.oil_rpm
            },
            "weight_kg": self.weight_kg
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Bearing':
        """Create Bearing instance from dictionary data."""
        dimensions = BearingDimensions(
            bore_diameter=data['d'],
            outer_diameter=data['D'],
            width=data['B']
        )
        
        load_ratings = LoadRatings(
            dynamic_load=data['Cr'],
            static_load=data['Cor']
        )
        
        speed_limits = SpeedLimits(
            grease_rpm=data['grease_rpm'],
            oil_rpm=data['oil_rpm']
        )
        
        return cls(
            model_number=data['model'],
            dimensions=dimensions,
            load_ratings=load_ratings,
            speed_limits=speed_limits,
            weight_kg=data['weight']
        )
