# RHD Bearings Catalog Generator

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Professional](https://img.shields.io/badge/Quality-Professional-green.svg)](https://rhdbearings.com)

A comprehensive Python package for generating structured JSON data for RHD Bearings' complete product catalog, optimized for web implementation, SEO, and LLM recommendations.

## 🚀 Quick Start

### Installation

```bash
# Install the package
pip install -e .

# Or install in development mode
pip install -e ".[dev]"
```

### Basic Usage

```bash
# Generate complete bearing catalog
rhd-bearings generate

# Generate to custom directory
rhd-bearings generate --output /path/to/output/

# Show project information
rhd-bearings info
```

### Python API

```python
from rhd_bearings import BearingJSONGenerator

# Initialize generator
generator = BearingJSONGenerator()

# Generate complete catalog
catalog = generator.generate_complete_catalog()

# Save to file
generator.save_catalog()
```

## 📁 Project Structure

```
rhd_bearings/
├── __init__.py                    # Package initialization
├── cli.py                         # Command line interface
├── core/                          # Core data models
│   ├── __init__.py
│   ├── bearing.py                 # Bearing data model
│   └── config.py                  # Configuration management
├── generators/                    # Content generators
│   ├── __init__.py
│   ├── content_generator.py       # SEO/LLM content generation
│   └── json_generator.py          # Main catalog generator
├── utils/                         # Utility functions
│   ├── __init__.py
│   ├── data_loader.py             # JSON file handling
│   └── lookups.py                 # Lookup table management
└── data/                          # Source data files
    ├── bearing_database.json      # Raw bearing specifications
    ├── clearance_lookup_table.json
    ├── noise_lookup_table.json
    ├── vibration_lookup_table.json
    ├── witty_bearing_descriptions.json
    └── bearing_extraction_guide.md
```

## 📊 Generated Output

### Individual Bearing Pages
- **194 bearing models** across 9 series
- Complete technical specifications
- Witty descriptions for brand personality
- SEO-optimized metadata
- Technical drawing URLs
- LLM optimization content
- Pricing and availability information
- Comprehensive FAQs

### Series Landing Pages
- **9 bearing series** overview pages
- Comprehensive applications by industry
- Detailed FAQs (6 categories, 3 questions each)
- Model listings with internal links
- SEO metadata and LLM optimization

## 🏗️ URL Structure

The system generates a hierarchical URL structure perfect for SEO:

```
Series Pages:
├── /miniature-bearings        # 3-digit bearings (604, 608, 683, etc.)
├── /6000-series              # 6000-6020 bearings
├── /6200-series              # 6200-6220 bearings
├── /6300-series              # 6300-6320 bearings
├── /62200-series             # 62200-62220 bearings
├── /62300-series             # 62301-62320 bearings
├── /16000-series             # 16001-16020 bearings
├── /6800-series              # 683-6820 bearings
└── /6900-series              # 693-6919 bearings

Individual Bearing Pages:
├── /miniature-bearings/608
├── /6000-series/6004
├── /6200-series/6202
└── ...
```

## 🎯 Features

### SEO Optimization
- ✅ Canonical URLs with proper hierarchy
- ✅ Meta descriptions with specifications
- ✅ Keyword optimization for each bearing
- ✅ Structured data for search engines
- ✅ Technical drawing alt text

### LLM Optimization
- ✅ Natural language queries
- ✅ Decision criteria for selection
- ✅ Problem-solution mapping
- ✅ Expertise signals
- ✅ Comparison matrices

### Business Features
- ✅ Dynamic pricing with CTAs
- ✅ Cross-references between models
- ✅ Comprehensive FAQs
- ✅ Technical specifications
- ✅ Industry-specific applications
- ✅ Witty brand personality descriptions

## 🛠️ Development

### Setup Development Environment

```bash
# Clone and install
git clone <repository>
cd rhd-bearings-catalog
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black rhd_bearings/
isort rhd_bearings/

# Type checking
mypy rhd_bearings/
```

### Project Commands

```bash
# Generate catalog
python -m rhd_bearings.cli generate

# Show package info
python -m rhd_bearings.cli info

# Run with custom output
python -m rhd_bearings.cli generate --output custom/
```

## 📈 Technical Details

### Dependencies
- **Python 3.7+** (no external dependencies)
- Uses only Python standard library
- Optional development dependencies for testing/linting

### Data Sources
- Raw bearing specifications from database
- Lookup tables for clearance, noise, and vibration data
- Custom witty descriptions for brand personality
- Comprehensive FAQ templates

### Output Format
- JSON files optimized for web implementation
- Ready for CMS integration
- Compatible with headless CMS systems
- Structured for API consumption

## 📞 Company Information

**RHD Bearings**
- 🌐 Website: https://rhdbearings.com
- 📧 Email: sales@rhdenterprise.in
- 🏭 OEM Sales: oemsales@rhdenterprise.in
- 📞 Phone: +91-9702081858
- 📍 Address: 203 Vihar Estate, Off. Saki Vihar Road, Next to Autohanger, Sakinaka, Andheri East Mumbai 400072

## 📈 Usage Stats

- **194 bearing models** processed
- **9 series pages** generated
- **Complete specifications** for all models
- **Technical drawings** included
- **SEO ready** for immediate deployment

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Generated by RHD Bearings Product Catalog Generator - Optimized for SEO, LLM recommendations, and professional web implementation.*