# Bearing Model File Generation Instructions

## CRITICAL RULES - NON-NEGOTIABLE

### Data Source Rules (ABSOLUTELY MANDATORY)
- **NEVER generate clearance, vibration, noise, SKF, or material data** - use lookup tables ONLY
- **NEVER estimate or assume technical specifications** - use actual data or null values
- **If data exists in lookup tables, you MUST use it - never create alternatives**

### Application Generation Rules (ABSOLUTELY MANDATORY)
- **ABSOLUTELY FORBIDDEN**: Grouping bearings by bore diameter ranges, using generic titles like "Industrial/Automotive", copy-pasting entire application group blocks
- **MANDATORY**: Analyze each bearing's complete specification profile individually, generate applications based on exact d×D×B×Cr×Cor×RPM combination, individual applications may overlap when technically appropriate

### JSON Structure Rules (ABSOLUTELY MANDATORY)
- **JSON structure MUST match `bearing_template.json` exactly - NO modifications allowed**

### Content Count Rules (ABSOLUTELY MANDATORY)
- **FAQ questions**: Exactly 12 total, **Recommendation snippets**: Exactly 6 items, **Natural language queries**: Exactly 6 items, **Decision criteria**: Exactly 5 items, **SEO keywords**: 15-25 items

## MANDATORY REQUIREMENTS

### Prerequisites
Required files: `bearing_database.json`, `skf_dimensions_only.json`, `vibration_lookup_table.json`, `noise_lookup_table.json`, `clearance_lookup_table.json`, `witty_bearing_descriptions.json`, `faq_generation_guide.json`, `bearing_template.json`

### Data Extraction Rules
1. **Base specifications**: Extract from `bearing_database.json` by exact model match
2. **SKF dimensions**: Look up by exact model number in `skf_dimensions_only.json` (use null if not found)
3. **Vibration data**: Look up by bore diameter in `vibration_lookup_table.json`
4. **Noise data**: Look up by bore diameter AND series in `noise_lookup_table.json`
5. **Clearance data**: Use range logic in `clearance_lookup_table.json` (over_mm < bore ≤ to_mm)
6. **Enhanced description**: Look up by exact model number in `witty_bearing_descriptions.json`
7. **Load capacity conversion**: Convert all load references from kN to kg for user understanding (multiply kN × 102 to get kg approximately), include kN values in parentheses for technical reference. **Exception**: The load_ratings section maintains original kN values

## STEP-BY-STEP GENERATION PROCESS

### Step 1: Extract Base Specifications
From `bearing_database.json`, locate target bearing model and extract all specifications.

### Step 2: Performance Data Lookup
**SKF Dimensions**: Search `skf_dimensions_only.json` for exact model number. If found, use exact d1, D2, r1, r2 values. If not found, set all SKF fields to null.

**Vibration Classes**: Search `vibration_lookup_table.json` by bore diameter for exact V2, V3, V4 values.

**Noise Levels**: Search `noise_lookup_table.json` by bore diameter AND series for exact Z2, Z3, Z4 values.

**Internal Clearance**: Search `clearance_lookup_table.json` using range logic for exact C2, C0, C3, C4, C5 values.

### Step 3: Application Group Generation
**CRITICAL**: Each bearing model must generate applications based on its specific characteristics, not reuse existing application patterns from other models.

**ABSOLUTELY FORBIDDEN - WILL CAUSE IMMEDIATE FAILURE:**
- Copying identical application lists (4+ matching items) from any other bearing model
- Using identical application group titles across different bearing models
- Rotating/rearranging the same application blocks between different bearing models
- Creating systematic patterns of shared content across multiple models

**MANDATORY REQUIREMENTS:**
- Analyze bearing's complete specification profile (d×D×B×load×speed×weight) individually
- Generate applications that genuinely reflect THIS bearing's specific capabilities
- Applications must reference the bearing's actual specifications in requirements text
- Each model must have genuinely different application focus based on its characteristics

**Application Generation Rules:**
- **Individual applications may overlap** when technically justified (e.g., "small motors" can appear for multiple bearings)
- **Application lists with 4+ identical items are prohibited** regardless of order or position
- **Application group titles must be model-specific** (not generic like "Precision Instruments" used across multiple models)
- **Requirements text must reference actual bearing specifications** (bore size, load capacity, speed rating)
- **Focus on common, relatable applications** that people encounter in industrial, automotive, household, automation, and consumer products

**Application Focus Guidelines:**
- **Industrial/Manufacturing**: Common machinery, production equipment, factory automation, conveyor systems
- **Automotive**: Vehicle components, engine parts, transmission systems, steering mechanisms
- **Household/Consumer**: Appliances, power tools, garden equipment, exercise equipment, home automation
- **Automation**: Robotics, CNC machines, assembly lines, material handling, packaging equipment
- **Electronics**: Computer components, cooling fans, drives, printers, consumer electronics

**Avoid overly specialized applications** like:
- Highly technical medical devices (surgical instruments, endoscopic tools)
- Laboratory/analytical equipment (spectrophotometers, chromatography systems)
- Aerospace/defense applications
- Research/scientific instruments
- Niche industrial processes

**Preferred application examples**:
- Small motors, cooling fans, pumps, gearboxes, conveyor rollers, power tools, automotive components, appliances, printers, robots, assembly machines, packaging equipment

**Acceptable vs. Prohibited Overlap:**

**ACCEPTABLE - Individual item overlap:**
```
605: ["optical instruments", "measuring devices", "calibration tools", "dental equipment", "micro-motors"]
606: ["optical instruments", "laboratory scales", "precision fixtures", "sensor assemblies", "test equipment"]
// Only 1 overlapping item out of 5-6 items
```

**PROHIBITED - List pattern reuse:**
```
605: ["optical instruments", "measuring devices", "laboratory equipment", "calibration tools", "microscopes", "surveying instruments"]
607: ["optical instruments", "measuring devices", "laboratory equipment", "calibration tools", "microscopes", "surveying instruments"]
// Identical 6-item list - this is wholesale copying regardless of application group position
```

**Icon Selection**: Choose from: cog, zap, target, layers, settings, cpu, compass, gauge

### Step 4: Cross-References and Shaft Requirements Generation

**Cross-References Structure:**
```json
"cross_references": {
  "related_models": [...],
  "shaft_requirements": {
    "nominal_diameter": "8.000mm",
    "tolerance_grade": "h6 (7.991-8.009mm)", 
    "surface_finish": "Ra 0.8μm max",
    "runout_tolerance": "0.013mm max"
  },
  "application_specific_alternatives": {
    "high_temperature": "C3 clearance recommended",
    "high_speed": "RHD V3 & V4 bearings recommended", 
    "corrosive_environment": "SS (Stainless Steel) bearings recommended"
  }
}
```

**Related Models Logic:**

**For Miniature Series** (3-digit models):
- Last digit = bore size in mm, cross-reference within miniature series only
- **604 bearing** (4mm): Related models from 624, 634, 684, 694 (exclude current model)
- **608 bearing** (8mm): Related models from 628, 638, 688, 698 (exclude current model)

**For Standard Series** (4-digit models):
- Last 2 digits × 5 = bore size in mm, cross-reference across 4-digit series
- **6004 bearing** (20mm): Related models from 6204, 6304, 6804, 6904
- **6208 bearing** (40mm): Related models from 6308, 6808, 6908, 16008

**Shaft Requirements Generation (DYNAMIC):**
Generate based on bearing's actual bore diameter (d value):

**nominal_diameter**: Use exact bore diameter with .000mm precision (e.g., "8.000mm")

**tolerance_grade**: Calculate h6 tolerance using standard ISO ranges:
- 3-6mm bore: h6 = -0.008/0mm 
- 6-10mm bore: h6 = -0.009/0mm
- 10-18mm bore: h6 = -0.011/0mm
- 18-30mm bore: h6 = -0.013/0mm
- Format as "h6 ({min}-{max}mm)" where min = bore - tolerance, max = bore

**surface_finish**: "Ra 0.8μm max" (universal for all bearing sizes)

**runout_tolerance**: "0.013mm max" (universal for all bearing sizes)

**Application-Specific Alternatives (HARDCODED):**
Use exact standardized text for ALL bearing models - no modifications allowed.

### Step 5: Application-Specific Alternatives (HARDCODED)
Use exact values for all models:
```json
"application_specific_alternatives": {
  "high_temperature": "C3 clearance recommended",
  "high_speed": "RHD V3 & V4 bearings recommended", 
  "corrosive_environment": "SS (Stainless Steel) bearings recommended"
}
```

### Step 6: Seal Options Configuration
Calculate RPM values from actual `grease_rpm` in bearing database:
- Open: 100%, Single Shield (Z): 95%, Double Shield (ZZ): 90%, Single Seal (RS): 80%, Double Seal (2RS): 70%

### Step 7: FAQ Generation
Generate exactly 12 questions following "Smart But Useful" theme:
- Category 1: Bearing Selection & Replacement (3 questions)
- Category 2: Installation & Maintenance (3 questions)  
- Category 3: Troubleshooting & Problem Solving (3 questions)
- Category 4: Cost & Performance Optimization (3 questions)

Balance technical expertise with practical usability. Include industry standards, material specifications, real-world examples, and professional authority elements.

### Step 8: LLM Optimization Content
**Recommendation Snippets** (6 items, 15-25 words): Performance-based, application-specific, quality/value focus using actual specifications.

**Natural Language Queries** (6 items, 5-15 words): Cover informational, navigational, transactional search intent with real user patterns.

**Decision Criteria** (5 items, 10-20 words): Dimensional requirements, performance requirements, application requirements with exact specifications.

### Step 9: SEO Metadata Enhancement
**Keywords** (15-25): Primary keywords, long-tail keywords, search intent keywords covering model-specific, application-specific, and technical terms.

**Meta Description** (150-160 characters): Include model, dimensions, load capacity in kg, applications, brand/location.

**Title Tag** (50-60 characters): Model number, dimensions, key benefit, brand name.

### Step 10: Final Assembly
Match `bearing_template.json` structure exactly. Validate all field names, types, and nested structure. Populate values only - never modify structure.

## VALIDATION BEFORE SAVING

- [ ] All technical data from lookup tables or null values
- [ ] JSON structure matches template exactly
- [ ] Applications technically appropriate for bearing specifications
- [ ] No wholesale copying of application group blocks
- [ ] All content counts met (12 FAQ, 6 snippets, 6 queries, 5 criteria, 15-25 keywords)
- [ ] Cross-references populated with related models (same bore) and series alternatives

## QUALITY ASSURANCE

### Data Source Compliance
All clearance, vibration, noise, SKF data matches lookup tables exactly. Material specs from bearing_database.json metadata. Enhanced descriptions from witty_bearing_descriptions.json.

### Content Quality  
Applications technically appropriate for bearing specifications. No wholesale block copying. FAQ content follows "Smart But Useful" theme. All specifications accurate and verifiable.

---

**File follows naming convention: `{model_number}.json`**