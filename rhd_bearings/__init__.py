"""
RHD Bearings Product Catalog Generator
=====================================

A comprehensive Python package for generating structured JSON data for RHD Bearings' 
complete product catalog, optimized for web implementation, SEO, and LLM recommendations.

Author: RHD Bearings
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "RHD Bearings"
__email__ = "sales@rhdenterprise.in"

from .core.bearing import Bearing
from .generators.json_generator import BearingJSONGenerator

__all__ = [
    "Bearing",
    "BearingJSONGenerator"
]
