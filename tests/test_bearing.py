"""Tests for the Bearing data model."""

import pytest
from rhd_bearings.core.bearing import Bearing, BearingDimensions, LoadRatings, SpeedLimits


def test_bearing_creation():
    """Test basic bearing creation."""
    dimensions = BearingDimensions(bore_diameter=20, outer_diameter=42, width=12)
    load_ratings = LoadRatings(dynamic_load=12.8, static_load=6.5)
    speed_limits = SpeedLimits(grease_rpm=18000, oil_rpm=22000)
    
    bearing = Bearing(
        model_number="6004",
        dimensions=dimensions,
        load_ratings=load_ratings,
        speed_limits=speed_limits,
        weight_kg=0.069
    )
    
    assert bearing.model_number == "6004"
    assert bearing.dimensions.bore_diameter == 20
    assert bearing.size_category == "medium"
    assert bearing.series_name == "6000"


def test_bearing_from_dict():
    """Test creating bearing from dictionary data."""
    data = {
        "model": "6202",
        "d": 15,
        "D": 35,
        "B": 11,
        "Cr": 9.6,
        "Cor": 4.8,
        "grease_rpm": 20000,
        "oil_rpm": 24000,
        "weight": 0.044
    }
    
    bearing = Bearing.from_dict(data)
    
    assert bearing.model_number == "6202"
    assert bearing.dimensions.bore_diameter == 15
    assert bearing.load_ratings.dynamic_load == 9.6
    assert bearing.series_name == "6200"


def test_size_categories():
    """Test size category determination."""
    # Miniature
    mini_dims = BearingDimensions(3, 8, 3)
    mini_bearing = Bearing("693", mini_dims, LoadRatings(1, 0.5), SpeedLimits(50000, 60000), 0.001)
    assert mini_bearing.size_category == "miniature"
    
    # Small  
    small_dims = BearingDimensions(8, 22, 7)
    small_bearing = Bearing("608", small_dims, LoadRatings(5, 2.5), SpeedLimits(30000, 36000), 0.012)
    assert small_bearing.size_category == "small"
    
    # Medium
    medium_dims = BearingDimensions(20, 42, 12)
    medium_bearing = Bearing("6004", medium_dims, LoadRatings(12.8, 6.5), SpeedLimits(18000, 22000), 0.069)
    assert medium_bearing.size_category == "medium"
    
    # Large
    large_dims = BearingDimensions(100, 150, 24)
    large_bearing = Bearing("6020", large_dims, LoadRatings(55.3, 37.1), SpeedLimits(3600, 4500), 1.46)
    assert large_bearing.size_category == "large"


def test_series_identification():
    """Test bearing series identification."""
    test_cases = [
        ("604", "miniature"),
        ("6004", "6000"),
        ("6202", "6200"),
        ("6305", "6300"),
        ("62201", "62200"),
        ("62301", "62300"),
        ("16005", "16000"),
        ("683", "miniature"),
        ("6801", "6800"),
        ("6905", "6900")
    ]
    
    for model, expected_series in test_cases:
        dims = BearingDimensions(10, 26, 8)
        ratings = LoadRatings(10, 5)
        speeds = SpeedLimits(20000, 24000)
        bearing = Bearing(model, dims, ratings, speeds, 0.1)
        assert bearing.series_name == expected_series, f"Model {model} should be series {expected_series}"
