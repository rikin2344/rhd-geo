"""
Data loading utilities for JSON files and configurations.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class DataLoader:
    """Handles loading and validation of JSON data files."""
    
    @staticmethod
    def load_json(filepath: Path) -> Dict[str, Any]:
        """
        Load and parse JSON file with error handling.
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            Parsed JSON data as dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {filepath}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in {filepath}: {e}")
        except Exception as e:
            raise Exception(f"Error loading {filepath}: {e}")
    
    @staticmethod
    def save_json(data: Dict[str, Any], filepath: Path, indent: int = 2) -> None:
        """
        Save data to JSON file with proper formatting.
        
        Args:
            data: Dictionary data to save
            filepath: Path where to save the file
            indent: JSON indentation level
        """
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
    
    @classmethod
    def load_bearing_database(cls, filepath: Path) -> List[Dict[str, Any]]:
        """
        Load and validate bearing database.
        
        Args:
            filepath: Path to bearing database JSON
            
        Returns:
            List of bearing data dictionaries
        """
        data = cls.load_json(filepath)
        
        if 'bearings' not in data:
            raise ValueError("Bearing database must contain 'bearings' key")
        
        bearings = data['bearings']
        
        # Validate required fields
        required_fields = ['model', 'd', 'D', 'B', 'Cr', 'Cor', 'grease_rpm', 'oil_rpm', 'weight']
        
        for i, bearing in enumerate(bearings):
            for field in required_fields:
                if field not in bearing:
                    raise ValueError(f"Bearing {i} missing required field: {field}")
        
        return bearings
    
    @classmethod
    def load_witty_descriptions(cls, filepath: Path) -> Dict[str, str]:
        """
        Load witty descriptions and convert to model -> description mapping.
        
        Args:
            filepath: Path to witty descriptions JSON
            
        Returns:
            Dictionary mapping model numbers to descriptions
        """
        try:
            data = cls.load_json(filepath)
            
            if 'witty_bearing_descriptions' not in data:
                print(f"Warning: No witty descriptions found in {filepath}")
                return {}
            
            descriptions = {}
            for item in data['witty_bearing_descriptions']:
                if 'model' in item and 'description' in item:
                    descriptions[item['model']] = item['description']
            
            return descriptions
            
        except FileNotFoundError:
            print(f"Warning: Witty descriptions file not found: {filepath}")
            return {}
        except Exception as e:
            print(f"Warning: Error loading witty descriptions: {e}")
            return {}
