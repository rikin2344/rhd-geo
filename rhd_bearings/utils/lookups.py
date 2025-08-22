"""
Lookup table management for clearance, vibration, and noise data.
"""

from typing import Dict, Any, Optional
from pathlib import Path

from .data_loader import DataLoader


class LookupManager:
    """Manages lookup tables for bearing specifications."""
    
    def __init__(self, clearance_file: Path, vibration_file: Path, noise_file: Path):
        """
        Initialize lookup manager with data files.
        
        Args:
            clearance_file: Path to clearance lookup table
            vibration_file: Path to vibration lookup table  
            noise_file: Path to noise lookup table
        """
        self.clearance_table = DataLoader.load_json(clearance_file)
        self.vibration_table = DataLoader.load_json(vibration_file)
        self.noise_table = DataLoader.load_json(noise_file)
    
    def get_clearance_data(self, bore_diameter: int) -> Optional[Dict[str, int]]:
        """
        Get clearance data for a given bore diameter.
        
        Args:
            bore_diameter: Bearing bore diameter in mm
            
        Returns:
            Dictionary with min_microns and max_microns, or None if not found
        """
        bore_str = str(bore_diameter)
        
        if bore_str in self.clearance_table:
            data = self.clearance_table[bore_str]
            return {
                "min_microns": data.get("min", 0),
                "max_microns": data.get("max", 0)
            }
        
        return None
    
    def get_vibration_data(self, bore_diameter: int) -> Optional[Dict[str, str]]:
        """
        Get vibration data for a given bore diameter.
        
        Args:
            bore_diameter: Bearing bore diameter in mm
            
        Returns:
            Dictionary with V2, V3, V4 values, or None if not found
        """
        bore_str = str(bore_diameter)
        
        if bore_str in self.vibration_table:
            return self.vibration_table[bore_str]
        
        return None
    
    def get_noise_data(self, bore_diameter: int, model_number: str) -> Optional[Dict[str, str]]:
        """
        Get noise data for a given bore diameter and bearing series.
        
        Args:
            bore_diameter: Bearing bore diameter in mm
            model_number: Bearing model number to determine series
            
        Returns:
            Dictionary with Z2, Z3, Z4 values, or None if not found
        """
        bore_str = str(bore_diameter)
        series = self._get_bearing_series_for_noise(model_number)
        
        if bore_str in self.noise_table and series in self.noise_table[bore_str]:
            return self.noise_table[bore_str][series]
        
        return None
    
    def _get_bearing_series_for_noise(self, model_number: str) -> str:
        """
        Determine bearing series for noise lookup table.
        
        Args:
            model_number: Bearing model number
            
        Returns:
            Series identifier for noise lookup
        """
        model = model_number.strip()
        
        # 3-digit miniature bearings
        if len(model) == 3 and model.isdigit():
            return '6000_series'  # Treat miniature as 6000 series for noise lookup
        
        # 6000 series patterns
        if (model.startswith('60') and len(model) == 4) or model in ['600', '601', '602', '603', '604', '605', '606', '607', '608', '609']:
            return '6000_series'
        
        # 6200 series (including 62200 subseries)
        if model.startswith('62'):
            return '6200_series'
            
        # 6300 series (including 62300 subseries)  
        if model.startswith('63'):
            return '6300_series'
        
        # All others default to 6000 series for noise lookup
        return '6000_series'
