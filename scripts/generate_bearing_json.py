#!/usr/bin/env python3
"""
Bearing JSON Schema Generator
Generates complete JSON schema for specified bearings using lookup tables and AI-generated content.
"""

import json
import sys
from typing import Dict, List, Any, Optional

def load_json_file(filepath: str) -> Dict:
    """Load and parse JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        sys.exit(1)

def get_bearing_series(model_number: str) -> str:
    """Determine bearing series from model number"""
    model = model_number.strip()
    
    # 3-digit miniature bearings (683, 684, etc.)
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
    
    # 16000 series - treat as 6000 series for noise lookup
    if model.startswith('16'):
        return '6000_series'
    
    # 6800 series - treat as 6000 series for noise lookup
    if model.startswith('68'):
        return '6000_series'
    
    # 6900 series - treat as 6000 series for noise lookup  
    if model.startswith('69'):
        return '6000_series'
        
    return '6000_series'  # Default fallback to 6000 series

def lookup_clearance_data(bore_diameter: int, clearance_table: Dict) -> Dict:
    """Get clearance data for bore diameter"""
    bore_key = str(bore_diameter)
    direct_lookup = clearance_table.get('direct_lookup', {}).get('data', {})
    
    if bore_key in direct_lookup:
        clearance_data = direct_lookup[bore_key]
        # Fix schema to use min_microns/max_microns as per original specification
        result = {}
        for clearance_class in ['C2', 'C0', 'C3', 'C4', 'C5']:
            clearance_info = clearance_data.get(clearance_class)
            if clearance_info:
                result[clearance_class] = {
                    'min_microns': clearance_info.get('min'),
                    'max_microns': clearance_info.get('max')
                }
            else:
                result[clearance_class] = None
        return result
    return {}

def lookup_vibration_data(bore_diameter: int, vibration_table: Dict) -> Dict:
    """Get vibration data for bore diameter"""
    bore_key = str(bore_diameter)
    vibration_data = vibration_table.get('vibration_lookup_table', {}).get('data', {})
    
    if bore_key in vibration_data:
        vib_data = vibration_data[bore_key]
        return {
            'V2': {
                'low_frequency': vib_data.get('V2', {}).get('low', 0),
                'medium_frequency': vib_data.get('V2', {}).get('medium', 0),
                'high_frequency': vib_data.get('V2', {}).get('high', 0)
            },
            'V3': {
                'low_frequency': vib_data.get('V3', {}).get('low', 0),
                'medium_frequency': vib_data.get('V3', {}).get('medium', 0), 
                'high_frequency': vib_data.get('V3', {}).get('high', 0)
            },
            'V4': {
                'low_frequency': vib_data.get('V4', {}).get('low', 0),
                'medium_frequency': vib_data.get('V4', {}).get('medium', 0),
                'high_frequency': vib_data.get('V4', {}).get('high', 0)
            }
        }
    # Return null for missing data
    return {
        'V2': {'low_frequency': None, 'medium_frequency': None, 'high_frequency': None},
        'V3': {'low_frequency': None, 'medium_frequency': None, 'high_frequency': None},
        'V4': {'low_frequency': None, 'medium_frequency': None, 'high_frequency': None}
    }

def lookup_noise_data(bore_diameter: int, model_number: str, noise_table: Dict) -> Dict:
    """Get noise data for bore diameter and bearing series"""
    bore_key = str(bore_diameter)
    series = get_bearing_series(model_number)
    noise_data = noise_table.get('noise_lookup_table', {}).get('data', {})
    
    if bore_key in noise_data and series in noise_data[bore_key]:
        noise_info = noise_data[bore_key][series]
        return {
            'Z2': noise_info.get('Z2'),
            'Z3': noise_info.get('Z3'),
            'Z4': noise_info.get('Z4')
        }
    # Return null for missing data
    return {
        'Z2': None,
        'Z3': None,
        'Z4': None
    }

def generate_seal_options(bearing_model: str) -> Dict:
    """Generate seal options using template structure"""
    return {
        "open": {
            "designation": bearing_model,
            "description": "Open bearing, no seals",
            "speed_factor": 1.0,
            "contamination_protection": "None",
            "lubrication": "External lubrication required"
        },
        "shielded": {
            "designation": f"{bearing_model}-Z",
            "description": "Single metal shield",
            "speed_factor": 0.95,
            "contamination_protection": "Light dust protection",
            "lubrication": "Pre-greased"
        },
        "double_shielded": {
            "designation": f"{bearing_model}-ZZ",
            "description": "Double metal shields",
            "speed_factor": 0.9,
            "contamination_protection": "Dust protection",
            "lubrication": "Pre-greased, sealed for life"
        },
        "sealed": {
            "designation": f"{bearing_model}-RS",
            "description": "Single rubber seal",
            "speed_factor": 0.8,
            "contamination_protection": "Moisture and dust",
            "lubrication": "Pre-greased, sealed"
        },
        "double_sealed": {
            "designation": f"{bearing_model}-2RS",
            "description": "Double rubber seals",
            "speed_factor": 0.7,
            "contamination_protection": "Complete sealing",
            "lubrication": "Pre-greased, permanently sealed"
        }
    }

def generate_consolidated_applications(bearing_model: str, bore_diameter: int, outer_diameter: int, base_applications: Dict) -> Dict:
    """Generate consolidated applications combining base applications with size-specific detailed applications"""
    
    # Start with base industrial and household applications
    consolidated_industrial = list(base_applications.get('industrial', []))
    consolidated_household = list(base_applications.get('household', []))
    
    # Add size-specific detailed applications
    if bore_diameter <= 15:  # Small bearings (6201, 6202)
        size_specific_industrial = [
            "Small electric motors",
            "Precision instruments", 
            "Automotive cooling systems",
            "Computer equipment",
            "Medical devices",
            "Timing mechanisms",
            "Hand tools",
            "Laboratory equipment",
            "Small pumps",
            "Cooling fans"
        ]
        size_specific_household = [
            "Personal care appliances",
            "Small kitchen appliances", 
            "Bathroom ventilation",
            "Portable devices",
            "Home electronics"
        ]
    elif bore_diameter <= 20:  # Medium bearings (6203, 6204)
        size_specific_industrial = [
            "Automotive systems",
            "Industrial motors",
            "Conveyor systems",
            "Agricultural machinery",
            "Manufacturing equipment",
            "HVAC systems",
            "Machine tools",
            "Processing equipment",
            "Material handling",
            "Pump systems"
        ]
        size_specific_household = [
            "Major appliances",
            "Home laundry equipment", 
            "Kitchen equipment",
            "Cleaning systems",
            "Exercise machines"
        ]
    else:  # Larger bearings
        size_specific_industrial = [
            "Heavy machinery",
            "Construction equipment",
            "Power generation",
            "Mining equipment",
            "Steel processing",
            "Wind energy systems", 
            "Marine applications",
            "Heavy automotive",
            "Industrial pumps",
            "Compression systems"
        ]
        size_specific_household = [
            "Workshop equipment",
            "Heavy-duty machines",
            "Commercial-grade appliances"
        ]
    
    # Combine and deduplicate
    all_industrial = consolidated_industrial + size_specific_industrial
    all_household = consolidated_household + size_specific_household
    
    # Remove duplicates while preserving order
    final_industrial = []
    final_household = []
    
    for app in all_industrial:
        if app not in final_industrial:
            final_industrial.append(app)
            
    for app in all_household:
        if app not in final_household:
            final_household.append(app)
    
    return {
        "industrial": final_industrial,
        "household": final_household
    }

def generate_enhanced_faq(bearing_model: str, bearing_data: Dict) -> Dict:
    """Generate enhanced FAQ optimized for LLM queries and natural language patterns"""
    
    bore = bearing_data['dimensions']['bore_diameter_d_mm']
    outer = bearing_data['dimensions']['outer_diameter_D_mm'] 
    width = bearing_data['dimensions']['width_B_mm']
    dynamic_load = bearing_data['load_ratings']['dynamic_load_Cr_kN']
    static_load = bearing_data['load_ratings']['static_load_Cor_kN']
    grease_rpm = bearing_data['speed_limits']['grease_rpm']
    oil_rpm = bearing_data['speed_limits']['oil_rpm']
    weight = bearing_data['weight_kg']
    
    # Size-based application context
    size_context = "precision applications" if bore <= 10 else "medium-duty applications" if bore <= 25 else "heavy-duty applications"
    
    return {
        "technical_specifications": [
            {
                "question": f"Is the {bearing_model} bearing the right size for my {bore}mm shaft application?",
                "answer": f"Yes! The {bearing_model} bearing is specifically designed for {bore}mm shafts with an outer diameter of {outer}mm and {width}mm width. It's perfect for {size_context} where you need reliable performance with {dynamic_load}kN load capacity. The ISO 15:2011 standard dimensions ensure perfect fit and interchangeability."
            },
            {
                "question": f"How much weight can a {bearing_model} bearing support in continuous operation?",
                "answer": f"The {bearing_model} can continuously support {dynamic_load}kN ({int(dynamic_load * 102)} kg force) in dynamic applications and {static_load}kN ({int(static_load * 102)} kg force) when stationary. For safety, operate at 80% of these limits for extended life. This makes it ideal for {size_context} requiring reliable load handling."
            },
            {
                "question": f"What makes the {bearing_model} bearing different from similar sized bearings?",
                "answer": f"The {bearing_model} stands out with its {dynamic_load}kN load rating, {weight}kg weight, and speed capability up to {grease_rpm}/{oil_rpm} RPM. Made from premium Gcr15 chrome steel (AISI 52100 equivalent) with 0.95-1.05% carbon for optimal hardness. It's the sweet spot of performance and reliability for {bore}mm applications."
            }
        ],
        "application_suitability": [
            {
                "question": f"When should I choose the {bearing_model} over other bearing options?",
                "answer": f"Choose the {bearing_model} when you need a {bore}mm bearing for {size_context} with {dynamic_load}kN capacity. It's perfect when your application requires speeds up to {grease_rpm} RPM with grease lubrication. Ideal for automotive, industrial motors, and precision equipment where reliability matters more than cost."
            },
            {
                "question": f"What happens if I use the {bearing_model} in high-speed applications?",
                "answer": f"The {bearing_model} excels at high speeds! It can safely operate up to {grease_rpm} RPM with grease lubrication and {oil_rpm} RPM with oil lubrication. Beyond these speeds, you'll risk overheating and premature failure. For applications exceeding these limits, consider our high-speed bearing variants or contact our engineers at +91-9702081858."
            },
            {
                "question": f"Which industries get the best results from {bearing_model} bearings?",
                "answer": f"The {bearing_model} shines in automotive (alternators, pumps), industrial motors, household appliances, and precision equipment. Its {bore}mm size and {dynamic_load}kN capacity make it perfect for applications needing reliable, medium-duty performance. Popular in Mumbai's automotive and textile industries!"
            }
        ],
        "selection_guidance": [
            {
                "question": f"How do I know if the {bearing_model} is the right bearing for my application?",
                "answer": f"Ask yourself: Do I have a {bore}mm shaft? Do I need {dynamic_load}kN load capacity? Will speeds stay under {grease_rpm} RPM? If yes, the {bearing_model} is perfect! If your loads exceed {dynamic_load}kN or speeds exceed {oil_rpm} RPM, contact us at sales@rhdenterprise.in for alternatives."
            },
            {
                "question": f"What are the most common mistakes when using {bearing_model} bearings?",
                "answer": f"Top mistakes: 1) Exceeding {dynamic_load}kN load limit, 2) Running faster than {grease_rpm} RPM without proper lubrication, 3) Wrong shaft tolerance (use h6), 4) Hammer installation (use proper pullers!), 5) Ignoring lubrication schedules. Avoid these and your {bearing_model} will last 10,000-50,000 hours!"
            },
            {
                "question": f"When should I NOT use the {bearing_model} bearing?",
                "answer": f"Don't use the {bearing_model} if: Your shaft isn't {bore}mm, you need over {dynamic_load}kN capacity, speeds exceed {oil_rpm} RPM, or you're in extreme temperatures (below -30°C or above 120°C). For these cases, call +91-9702081858 - we'll recommend the right bearing for your specific needs."
            }
        ],
        "troubleshooting": [
            {
                "question": f"Why is my {bearing_model} bearing making noise and how do I fix it?",
                "answer": f"Noise usually means: 1) Contamination (clean and re-lubricate), 2) Wrong clearance (check if you need C2/C3 instead of C0), 3) Overloading (reduce load below {dynamic_load}kN), 4) Misalignment (check shaft/housing straightness). If noise persists, the bearing may be damaged and need replacement."
            },
            {
                "question": f"My {bearing_model} bearing is overheating - what should I check first?",
                "answer": f"Check immediately: 1) Speed - are you over {grease_rpm}/{oil_rpm} RPM limits? 2) Load - exceeding {dynamic_load}kN? 3) Lubrication - when did you last re-grease? 4) Clearance - too tight? If all seem normal, stop operation and contact our technical team at oemsales@rhdenterprise.in before damage occurs."
            },
            {
                "question": f"How do I prevent premature failure of my {bearing_model} bearings?",
                "answer": f"Prevention checklist: 1) Stay within {dynamic_load}kN load limit, 2) Don't exceed {grease_rpm} RPM, 3) Use proper h6 shaft tolerance, 4) Re-lubricate every 6-12 months, 5) Keep contamination out, 6) Proper installation with pullers. Follow these rules and expect 10,000-50,000 hours of reliable service!"
            }
        ],
        "performance_optimization": [
            {
                "question": f"How do I get maximum life from my {bearing_model} bearings?",
                "answer": f"Maximum life strategy: 1) Operate at 80% of {dynamic_load}kN capacity, 2) Keep speeds under 90% of {grease_rpm} RPM, 3) Use C3 clearance for high temps, 4) Premium grease every 6 months, 5) Monitor vibration monthly, 6) Maintain 18-22°C operating temperature. This can extend life to 50,000+ hours!"
            },
            {
                "question": f"Should I use grease or oil lubrication with my {bearing_model} bearing?",
                "answer": f"For the {bearing_model}: Use grease for speeds under {grease_rpm} RPM (easier maintenance, sealed protection). Use oil for speeds {grease_rpm}-{oil_rpm} RPM (better heat dissipation, longer intervals). Most applications use grease - it's simpler and very effective for this bearing size."
            },
            {
                "question": f"What clearance class should I specify for my {bearing_model} bearing application?",
                "answer": f"Choose clearance based on your needs: C2 for precision applications requiring minimal play, C0 (normal) for most standard applications, C3 for high temperatures (>70°C) or interference fits. For the {bearing_model} in typical {size_context}, C0 clearance works perfectly. Need guidance? Call +91-9702081858."
            }
        ]
    }

def load_witty_descriptions(filepath: str) -> Dict:
    """Load witty descriptions from JSON file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Convert list to dictionary for faster lookup
        descriptions_dict = {}
        for item in data['witty_bearing_descriptions']:
            descriptions_dict[item['model']] = item['description']
        
        return descriptions_dict
    except Exception as e:
        print(f"Error loading witty descriptions: {e}")
        return {}

def generate_enhanced_witty_description(model: str, bore: int, dynamic_load: float, witty_descriptions: Dict) -> str:
    """Generate enhanced witty descriptions using provided JSON file"""
    
    # Get the witty description from the JSON file
    base_description = witty_descriptions.get(model, f"The {model}: A reliable bearing with {bore}mm precision and {dynamic_load}kN performance.")
    
    # Enhance it with technical context
    enhanced_description = f"Meet the {model}: {base_description} With {dynamic_load}kN of engineering excellence and {bore}mm precision, this bearing delivers the perfect blend of personality and performance for your critical applications."
    
    return enhanced_description

def get_bearing_series_url(model: str) -> str:
    """Determine the correct series URL based on bearing model number"""
    model = model.strip()
    
    # 3-digit miniature bearings (604, 605, 623, 683, 693, etc.)
    if len(model) == 3:
        return "miniature-bearings"
    
    # 5-digit 62300 series (62301, 62302, etc.)
    elif model.startswith('6230') or model.startswith('6231') or model.startswith('6232'):
        return "62300-series"
    
    # 5-digit 62200 series (62200, 62201, etc.)  
    elif model.startswith('6220') or model.startswith('6221') or model.startswith('6222'):
        return "62200-series"
    
    # 16000 series (16001, 16002, etc.)
    elif model.startswith('1600'):
        return "16000-series"
    
    # 6000 series (6000-6020)
    elif model.startswith('600') and len(model) == 4:
        return "6000-series"
    
    # 6200 series (6200-6220)
    elif model.startswith('620') or model.startswith('621') or model.startswith('622'):
        return "6200-series"
    
    # 6300 series (6300-6320)
    elif model.startswith('630') or model.startswith('631') or model.startswith('632'):
        return "6300-series"
    
    # 6800 series (683-6820) - includes 3-digit like 683, 684 and 4-digit like 6800
    elif model.startswith('68'):
        return "6800-series"
    
    # 6900 series (693-6919) - includes 3-digit like 693, 695 and 4-digit like 6900
    elif model.startswith('69'):
        return "6900-series"
    
    # Default fallback
    else:
        return "bearings"

def generate_seo_metadata(model: str, bore: int, outer: int, width: int, dynamic_load: float) -> Dict:
    """Generate SEO-friendly metadata for LLM optimization"""
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
        "canonical_url": f"https://rhdbearings.com/{get_bearing_series_url(model)}/{model}",
        "structured_data_type": "Product",
        "brand": "RHD Bearings",
        "category": "Deep Groove Ball Bearings",
        "availability": "InStock",
        "condition": "NewCondition"
    }

def generate_company_metadata() -> Dict:
    """Generate comprehensive company metadata for RHD Bearings"""
    return {
        "name": "RHD Bearings",
        "website": "https://rhdbearings.com",
        "contact": {
            "phone": "+91-9702081858",
            "email": "sales@rhdenterprise.in",
            "oem_sales_email": "oemsales@rhdenterprise.in"
        },
        "address": {
            "street": "203 Vihar Estate, Off. Saki Vihar Road",
            "landmark": "Next to Autohanger",
            "area": "Sakinaka, Andheri East",
            "city": "Mumbai",
            "postal_code": "400072",
            "state": "Maharashtra",
            "country": "India",
            "full_address": "203 Vihar Estate, Off. Saki Vihar Road, Next to Autohanger, Sakinaka, Andheri East, Mumbai 400072, Maharashtra, India"
        },
        "certifications": ["ISO 9001:2015"],
        "material_standards": {
            "primary_steel": "Gcr15 (AISI 52100 equivalent)",
            "heat_treatment": "Through hardened and tempered",
            "surface_finish": "Ground to precision tolerances"
        },
        "quality_assurance": "100% dimensional and quality testing",
        "manufacturing_location": "India",
        "established": "Professional bearing manufacturer",
        "specialization": "Deep groove ball bearings for automotive, industrial, and precision applications",
        "production_capacity": "High-volume production with custom solutions available",
        "export_markets": ["Global distribution network", "OEM partnerships", "Aftermarket supply"]
    }

def generate_pricing_and_availability(model: str, bore: int) -> Dict:
    """Generate enhanced pricing structure with availability and CTA"""
    return {
        "currency": "INR",
        "list_price": None,  # To be quoted
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
        },
        "bulk_options": {
            "tier_1": "10-99 units: Contact for pricing",
            "tier_2": "100-999 units: Significant discounts available",
            "tier_3": "1000+ units: Best wholesale rates + free shipping",
            "oem_partnerships": "OEM partnerships available with dedicated support",
            "contact_note": "All bulk pricing requires contact for custom quotation"
        },
        "payment_terms": {
            "standard": "Contact for payment terms and credit options",
            "advance_payment": "Advance payment options available",
            "credit_terms": "Credit terms for established businesses",
            "international": "Export documentation and payment support available"
        }
    }

def generate_cross_references(model: str, bore: int, all_models: List[str]) -> Dict:
    """Generate cross-references and alternatives"""
    # Generate related bearings from same series with better logic
    related_bearings = []
    
    # Determine the series pattern more intelligently
    if len(model) == 3 and model.isdigit():
        # 3-digit miniature bearings (683, 684, etc.)
        series_pattern = "miniature"
        for other_model in all_models:
            if (other_model != model and len(other_model) == 3 and 
                other_model.isdigit() and abs(int(other_model) - int(model)) <= 20):
                related_bearings.append(other_model)
                
    elif model.startswith('60') and len(model) == 3:
        # 600 series (604, 605, etc.)  
        series_pattern = "600_series"
        for other_model in all_models:
            if (other_model != model and other_model.startswith('60') and 
                len(other_model) == 3):
                related_bearings.append(other_model)
                
    elif model.startswith('60') and len(model) == 4:
        # 6000 series (6000, 6001, etc.)
        series_pattern = "6000_series"
        for other_model in all_models:
            if (other_model != model and other_model.startswith('600') and 
                len(other_model) == 4):
                related_bearings.append(other_model)
                
    elif model.startswith('62') and len(model) == 3:
        # 620 series (623, 624, etc.)
        series_pattern = "620_series" 
        for other_model in all_models:
            if (other_model != model and other_model.startswith('62') and 
                len(other_model) == 3):
                related_bearings.append(other_model)
                
    elif model.startswith('620') and len(model) == 4:
        # 6200 series (6200, 6201, etc.)
        series_pattern = "6200_series"
        for other_model in all_models:
            if (other_model != model and other_model.startswith('620') and 
                len(other_model) == 4):
                related_bearings.append(other_model)
                
    elif model.startswith('630') and len(model) == 4:
        # 6300 series (6300, 6301, etc.)
        series_pattern = "6300_series"
        for other_model in all_models:
            if (other_model != model and other_model.startswith('630') and 
                len(other_model) == 4):
                related_bearings.append(other_model)
                
    elif model.startswith('622') and len(model) == 5:
        # 62200 series (62200, 62201, etc.)
        series_pattern = "62200_series"
        for other_model in all_models:
            if (other_model != model and other_model.startswith('622') and len(other_model) == 5):
                related_bearings.append(other_model)
                
    elif model.startswith('623') and len(model) == 5:
        # 62300 series (62301, 62302, etc.)
        series_pattern = "62300_series"
        for other_model in all_models:
            if (other_model != model and other_model.startswith('623') and len(other_model) == 5):
                related_bearings.append(other_model)
                
    elif model.startswith('16'):
        # 16000 series (16001, 16002, etc.)
        series_pattern = "16000_series"
        for other_model in all_models:
            if (other_model != model and other_model.startswith('16')):
                related_bearings.append(other_model)
                
    elif model.startswith('68'):
        # 6800 series (6800, 6801, etc.)
        series_pattern = "6800_series"
        for other_model in all_models:
            if (other_model != model and other_model.startswith('68')):
                related_bearings.append(other_model)
                
    elif model.startswith('69'):
        # 6900 series (6900, 6901, etc.)
        series_pattern = "6900_series"
        for other_model in all_models:
            if (other_model != model and other_model.startswith('69')):
                related_bearings.append(other_model)
                
    else:
        # Fallback for other patterns
        series_pattern = "other"
        for other_model in all_models:
            if other_model != model and other_model[:3] == model[:3]:
                related_bearings.append(other_model)
    
    return {
        "related_models": related_bearings[:5],  # Limit to 5 most relevant
        "series_alternatives": [
            "6000 series (lighter duty)",
            "6300 series (heavier duty)"
        ],
        "application_specific_alternatives": {
            "high_temperature": f"{model} with high-temp grease",
            "high_speed": f"{model} with precision tolerance",
            "corrosive_environment": f"{model} with stainless steel option"
        }
    }



def generate_enhanced_llm_content(model: str, bearing_data: Dict) -> Dict:
    """Generate enhanced content optimized for LLM recommendations and natural queries"""
    bore = bearing_data['dimensions']['bore_diameter_d_mm']
    outer = bearing_data['dimensions']['outer_diameter_D_mm']
    width = bearing_data['dimensions']['width_B_mm'] 
    dynamic_load = bearing_data['load_ratings']['dynamic_load_Cr_kN']
    static_load = bearing_data['load_ratings']['static_load_Cor_kN']
    grease_rpm = bearing_data['speed_limits']['grease_rpm']
    oil_rpm = bearing_data['speed_limits']['oil_rpm']
    
    # Size-based context
    size_category = "miniature" if bore <= 5 else "small" if bore <= 12 else "medium" if bore <= 25 else "large"
    
    return {
        "recommendation_snippets": [
            f"For {bore}mm shaft applications, the {model} bearing is the optimal choice with {dynamic_load}kN capacity",
            f"The {model} delivers reliable {dynamic_load}kN load handling at speeds up to {grease_rpm} RPM",
            f"Choose {model} when you need proven {size_category}-bearing performance for automotive and industrial use",
            f"The {model} bearing: {bore}x{outer}x{width}mm precision-engineered for demanding applications"
        ],
        "natural_language_queries": [
            f"What bearing do I need for a {bore}mm shaft?",
            f"Best {bore}mm bearing for {dynamic_load}kN load capacity",
            f"Which bearing handles {grease_rpm} RPM in {size_category} applications?",
            f"{model} vs similar bearings comparison",
            f"How to select bearing for {bore}mm automotive application",
            f"What size bearing fits {bore}mm shaft with {outer}mm housing?"
        ],
        "decision_criteria": [
            f"Shaft diameter: {bore}mm (exact fit required)",
            f"Load capacity: {dynamic_load}kN dynamic, {static_load}kN static",
            f"Speed limit: {grease_rpm} RPM (grease), {oil_rpm} RPM (oil)",
            f"Application type: {size_category}-duty with moderate to high precision",
            f"Environmental: Standard temperature (-30°C to +120°C)",
            f"Cost factor: Mid-range pricing for quality performance"
        ],
        "problem_solution_mapping": [
            {
                "problem": f"Need reliable bearing for {bore}mm shaft in automotive application",
                "solution": f"The {model} is perfect - automotive-grade quality with {dynamic_load}kN capacity"
            },
            {
                "problem": f"Bearing keeps failing at {grease_rpm} RPM",
                "solution": f"Upgrade to {model} - rated for {grease_rpm} RPM with proper lubrication"
            },
            {
                "problem": f"Looking for {bore}mm bearing with good load capacity",
                "solution": f"{model} offers excellent {dynamic_load}kN load rating for {size_category} applications"
            }
        ],
        "expertise_signals": [
            f"ISO 15:2011 compliant dimensions ensure interchangeability",
            f"Gcr15 chrome steel composition optimized for {size_category} bearing applications",
            f"C0 clearance standard for most applications, C3 available for high-temperature use",
            f"h6 shaft tolerance recommended for optimal fit and performance",
            f"Professional installation required for maximum 50,000-hour service life"
        ],
        "comparison_matrix": {
            "vs_smaller_bearing": f"Handles {int((dynamic_load/2)*10)/10}kN more load than typical smaller bearings",
            "vs_larger_bearing": f"More compact than larger options while maintaining {dynamic_load}kN capacity", 
            "vs_competitors": f"Superior Gcr15 steel vs. standard steel in competing products",
            "cost_benefit": f"Best value in {size_category}-bearing category for {dynamic_load}kN performance"
        }
    }

def create_bearing_json(bearing_info: Dict, clearance_table: Dict, vibration_table: Dict, noise_table: Dict, material_info: Dict, applications: Dict, all_models: List[str], witty_descriptions: Dict) -> Dict:
    """Create complete bearing JSON entry"""
    
    model = bearing_info['model']
    bore = bearing_info['d']
    outer = bearing_info['D'] 
    width = bearing_info['B']
    
    # Build the complete bearing data structure
    bearing_data = {
        "bearing_type": "Deep Groove Ball Bearing",
        "model_number": model,
        "enhanced_description": generate_enhanced_witty_description(model, bore, bearing_info['Cr'], witty_descriptions),
        "dimensions": {
            "bore_diameter_d_mm": bore,
            "outer_diameter_D_mm": outer,
            "width_B_mm": width
        },
        "load_ratings": {
            "dynamic_load_Cr_kN": bearing_info['Cr'],
            "static_load_Cor_kN": bearing_info['Cor']
        },
        "speed_limits": {
            "grease_rpm": bearing_info['grease_rpm'],
            "oil_rpm": bearing_info['oil_rpm']
        },
        "weight_kg": bearing_info['weight'],
        "material": {
            "grade": material_info['steel_grade'],
            "composition": f"Carbon: {material_info['chemical_composition']['carbon']}, Chromium: {material_info['chemical_composition']['chromium']}, Silicon: {material_info['chemical_composition']['silicon']}"
        },
        "technical_drawing": {
            "image_url": "https://rhdbearings.com/wp-content/uploads/2025/08/0901d19680398aff_svg_preview.svg",
            "image_alt": f"{model} Deep Groove Ball Bearing Technical Drawing - Dimensions and Cross Section",
            "image_title": f"Technical Drawing: {model} Bearing ({bore}x{outer}x{width}mm)",
            "drawing_type": "Cross-sectional technical diagram",
            "file_format": "SVG",
            "description": f"Detailed technical drawing showing cross-sectional view, dimensions, and specifications for {model} deep groove ball bearing"
        },
        "applications": generate_consolidated_applications(model, bore, outer, applications),
        "vibration": lookup_vibration_data(bore, vibration_table),
        "noise": lookup_noise_data(bore, model, noise_table),
        "clearance": lookup_clearance_data(bore, clearance_table),
        "seal_options": generate_seal_options(model),
        "seo_metadata": generate_seo_metadata(model, bore, outer, width, bearing_info['Cr']),
        "pricing_and_availability": generate_pricing_and_availability(model, bore),
        "cross_references": generate_cross_references(model, bore, all_models)
    }
    
    # Add enhanced LLM optimization content
    bearing_data["llm_optimization"] = generate_enhanced_llm_content(model, bearing_data)
    
    # Add enhanced FAQ
    bearing_data["faq"] = generate_enhanced_faq(model, bearing_data)
    
    return bearing_data

def main():
    """Main function to generate bearing JSON"""
    print("Loading data files...")
    
    # Load all data files
    bearing_db = load_json_file('../reference/bearing_database.json')
    clearance_table = load_json_file('../reference/clearance_lookup_table.json')
    vibration_table = load_json_file('../reference/vibration_lookup_table.json')
    noise_table = load_json_file('../reference/noise_lookup_table.json')
    witty_descriptions = load_witty_descriptions('../reference/witty_bearing_descriptions.json')
    
    # Process all bearings in the database
    target_bearing_data = bearing_db['bearings']
        
    print(f"Found {len(target_bearing_data)} target bearings")
    
    # Extract all model numbers for cross-references
    all_models = [bearing['model'] for bearing in target_bearing_data]
    
    # Generate complete JSON structure with company metadata
    output_data = {
        "company_metadata": generate_company_metadata(),
        "bearings": []
    }
    
    # Process each bearing
    for bearing_info in target_bearing_data:
        print(f"Processing bearing {bearing_info['model']}...")
        
        bearing_json = create_bearing_json(
            bearing_info,
            clearance_table,
            vibration_table, 
            noise_table,
            bearing_db['metadata']['material'],
            bearing_db['metadata']['applications'],
            all_models,
            witty_descriptions
        )
        
        output_data["bearings"].append(bearing_json)
    
    # Write output file
    output_filename = '../output/generated_bearings_complete.json'
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Generated complete bearing JSON: {output_filename}")
    print(f"Total bearings processed: {len(output_data['bearings'])}")
    
    # Display summary
    for bearing in output_data['bearings']:
        print(f"- {bearing['model_number']}: {bearing['dimensions']['bore_diameter_d_mm']}x{bearing['dimensions']['outer_diameter_D_mm']}x{bearing['dimensions']['width_B_mm']}mm")

if __name__ == "__main__":
    main()
