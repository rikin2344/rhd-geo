# Bearing Data Extraction Guide for Cursor

## Overview
This guide provides specific prompts and instructions for extracting bearing specifications from Ningbo Giant Bearings Manufacturing Co., Ltd. PDF catalogs into structured JSON format.

## Data Structure Requirements

### Target JSON Schema
```json
{
  "bearings": [
    {
      "bearing_type": "string",
      "model_number": "string",
      "dimensions": {
        "bore_diameter_d_mm": "number",
        "outer_diameter_D_mm": "number", 
        "width_B_mm": "number"
      },
      "load_ratings": {
        "dynamic_load_Cr_kN": "number",
        "static_load_Cor_kN": "number"
      },
      "speed_limits": {
        "grease_rpm": "number",
        "oil_rpm": "number"
      },
      "weight_kg": "number",
      "material": {
        "grade": "string",
        "composition": "string"
      },
      "applications": {
        "industrial": ["array_of_strings"],
        "household": ["array_of_strings"]
      },
      "vibration": {
        "V2": {
          "low_frequency": "number",
          "medium_frequency": "number", 
          "high_frequency": "number"
        },
        "V3": {
          "low_frequency": "number",
          "medium_frequency": "number",
          "high_frequency": "number"
        },
        "V4": {
          "low_frequency": "number",
          "medium_frequency": "number",
          "high_frequency": "number"
        }
      },
      "noise": {
        "Z2": "number",
        "Z3": "number", 
        "Z4": "number"
      },
      "clearance": {
        "C2": {
          "min_microns": "number",
          "max_microns": "number"
        },
        "C0": {
          "min_microns": "number", 
          "max_microns": "number"
        },
        "C3": {
          "min_microns": "number",
          "max_microns": "number"
        },
        "C4": {
          "min_microns": "number",
          "max_microns": "number"
        },
        "C5": {
          "min_microns": "number",
          "max_microns": "number"
        }
      },
      "seal_options": {
        "open": {
          "designation": "string",
          "description": "string",
          "speed_factor": "number",
          "contamination_protection": "string",
          "lubrication": "string"
        },
        "shielded": {
          "designation": "string",
          "description": "string", 
          "speed_factor": "number",
          "contamination_protection": "string",
          "lubrication": "string"
        },
        "double_shielded": {
          "designation": "string",
          "description": "string",
          "speed_factor": "number",
          "contamination_protection": "string",
          "lubrication": "string"
        },
        "sealed": {
          "designation": "string",
          "description": "string",
          "speed_factor": "number",
          "contamination_protection": "string",
          "lubrication": "string"
        },
        "double_sealed": {
          "designation": "string",
          "description": "string",
          "speed_factor": "number",
          "contamination_protection": "string",
          "lubrication": "string"
        }
      },
      "dynamic_applications": ["array_of_strings_generated_by_ai"],
      "faq": {
        "technical_specifications": [
          {
            "question": "string",
            "answer": "string"
          }
        ],
        "application_suitability": [
          {
            "question": "string", 
            "answer": "string"
          }
        ],
        "installation_maintenance": [
          {
            "question": "string",
            "answer": "string"
          }
        ],
        "troubleshooting": [
          {
            "question": "string",
            "answer": "string"
          }
        ],
        "performance_optimization": [
          {
            "question": "string",
            "answer": "string"
          }
        ]
      }
    }
  ]
}
```

## Extraction Instructions for Cursor

#### Prompt 3: Extract Application Categories  
```
From page 5 (page 11 in document), extract application information:
- Industrial applications from left side diagram (应用领域 Product Application)
- Household applications from right side diagram (部分家用产品应用 Household Products Applications)
- Create arrays of application categories in both Chinese and English where available
```

#### Prompt 7: Generate Dynamic Content (Seal Options, Applications, FAQ)
```
IMPORTANT: This step requires AI generation using Claude API within Cursor. Use the following templates and generation rules:

SEAL OPTIONS GENERATION:
For each bearing, generate seal options using this template structure:

```javascript
function generateSealOptions(bearingModel) {
  return {
    open: {
      designation: bearingModel,
      description: "Open bearing, no seals",
      speed_factor: 1.0,
      contamination_protection: "None",
      lubrication: "External lubrication required"
    },
    shielded: {
      designation: bearingModel + "-Z",
      description: "Single metal shield",
      speed_factor: 0.95,
      contamination_protection: "Light dust protection", 
      lubrication: "Pre-greased"
    },
    double_shielded: {
      designation: bearingModel + "-ZZ",
      description: "Double metal shields",
      speed_factor: 0.9,
      contamination_protection: "Dust protection",
      lubrication: "Pre-greased, sealed for life"
    },
    sealed: {
      designation: bearingModel + "-RS", 
      description: "Single rubber seal",
      speed_factor: 0.8,
      contamination_protection: "Moisture and dust",
      lubrication: "Pre-greased, sealed"
    },
    double_sealed: {
      designation: bearingModel + "-2RS",
      description: "Double rubber seals", 
      speed_factor: 0.7,
      contamination_protection: "Complete sealing",
      lubrication: "Pre-greased, permanently sealed"
    }
  };
}
```

DYNAMIC APPLICATIONS GENERATION:
Generate size-appropriate applications based on bearing dimensions:

FAQ GENERATION:
Generate comprehensive FAQ using Claude API with this template structure. Here is says use API, but since we are in Cursor using Claude, you can generate these FAQ's here without needing the API.

```javascript
async function generateFAQ(bearing) {
  const prompt = `Generate a comprehensive FAQ for ${bearing.model_number} bearing with these specifications:
  
  Bearing Details:
  - Model: ${bearing.model_number}
  - Dimensions: ${bearing.dimensions.bore_diameter_d_mm} x ${bearing.dimensions.outer_diameter_D_mm} x ${bearing.dimensions.width_B_mm}mm
  - Dynamic Load: ${bearing.load_ratings.dynamic_load_Cr_kN}kN
  - Speed Limit: ${bearing.speed_limits.grease_rpm}RPM (grease), ${bearing.speed_limits.oil_rpm}RPM (oil)
  - Weight: ${bearing.weight_kg}kg
  
  Generate exactly 3 questions and answers for each category:
  
  1. technical_specifications - Focus on dimensions, nomenclature, specifications
  2. application_suitability - Focus on load handling, suitability for different uses
  3. installation_maintenance - Focus on installation, tolerances, service life
  4. troubleshooting - Focus on common problems, noise, failure causes
  5. performance_optimization - Focus on clearance selection, temperature, life maximization
  
  Make answers specific to this bearing size and realistic. Return as JSON object matching the FAQ schema.`;
  
  const response = await callClaudeAPI(prompt);
  return JSON.parse(response);
}
```

GOAL:
Combine all data into final JSON structure


### Step 4: Data Validation Rules

#### Required Fields Validation
- All dimension values (d, D, B) must be positive numbers
- Load ratings (Cr, Cor) must be positive numbers  
- Speed limits must be positive integers
- Weight must be positive number
- Bearing type must be non-empty string

#### Data Type Conversion
- Convert dimension strings like "12" to number 12
- Convert load ratings like "5.10" to number 5.10
- Convert speeds like "32000" to number 32000
- Convert weights like "0.0025" to number 0.0025

#### Missing Data Handling
- Use null for missing numeric values (marked with "-" in tables)
- Use empty string for missing text values
- Preserve original bearing type exactly as written

### Step 5: Quality Checks

#### Post-Extraction Validation
1. Verify bearing count matches table rows
2. Check for duplicate bearing model numbers
3. Validate dimensional relationships (D > d, reasonable B values)
4. Ensure load ratings are within expected ranges
5. Verify speed limits are realistic for bearing sizes

#### Expected Data Ranges
- Bore diameter (d): 3-100mm typically
- Outer diameter (D): 7-250mm typically  
- Width (B): 2-50mm typically
- Dynamic load (Cr): 0.3-200 kN typically
- Static load (Cor): 0.1-300 kN typically
- Grease speed: 3000-70000 RPM typically
- Oil speed: 4000-90000 RPM typically
- Weight: 0.0007-15 kg typically
- Vibration V2: Low 90-640, Medium 60-570, High 50-750 typically
- Vibration V3: Low 55-400, Medium 35-350, High 30-480 typically  
- Vibration V4: Low 45-290, Medium 14-260, High 15-350 typically

## Implementation Notes

### Critical Reading Rules

1. **Bore Diameter Lookup**: Always use the bearing's inner diameter (d) to find the correct row
2. **Column Selection**: Only extract V2, V3, and V4 data (ignore V and V1 columns)
3. **Sub-column Order**: Each V column has 3 values in order: 低频(Low), 中频(Medium), 高频(High)

### Practical Examples from Table

**Example 1: Bearing 6201 (bore = 12mm)**
- Locate row: bore diameter = 12mm
- V2 column: 90, 60, 50 → Low=90, Medium=60, High=50
- V3 column: 55, 35, 30 → Low=55, Medium=35, High=30  
- V4 column: 45, 14, 15 → Low=45, Medium=14, High=15

**Example 2: Bearing 6204 (bore = 20mm)**
- Locate row: bore diameter = 20mm
- V2 column: 130, 100, 75 → Low=130, Medium=100, High=75
- V3 column: 80, 60, 45 → Low=80, Medium=60, High=45
- V4 column: 60, 25, 25 → Low=60, Medium=25, High=25

**Example 3: Bearing 6300 (bore = 10mm)**
- Locate row: bore diameter = 10mm  
- V2 column: 90, 60, 50 → Low=90, Medium=60, High=50
- V3 column: 55, 35, 30 → Low=55, Medium=35, High=30
- V4 column: 45, 14, 15 → Low=45, Medium=14, High=15


### Data Validation for Vibration Values

- All vibration values should be positive integers
- V2 values are typically higher than V3 values  
- V3 values are typically higher than V4 values
- Low frequency values are typically higher than medium frequency values
- Medium frequency values are typically higher than high frequency values

### Table Structure Variations
- Some tables span multiple pages
- Headers may be in Chinese with English translations
- Numeric formatting may include decimals or integers
- Some cells may contain "-" for unavailable data

### Special Cases to Handle
1. **Bearing series transitions**: Different bearing types (600, 6200, 6300, etc.) may have different table structures
2. **Unit conversions**: Ensure all measurements are in specified units (mm, kN, RPM, kg)
3. **Model number formats**: Preserve exact formatting (604, 6004, 62304, etc.)

### Error Handling
- Log any rows that fail to parse completely
- Continue processing remaining rows if individual row fails
- Report summary of successful vs failed extractions

## Next Steps
This guide will be expanded to include:
- Tolerance specifications extraction
- Vibration and noise parameter extraction  
- Additional bearing series as needed
- Cross-reference validation between different table sections