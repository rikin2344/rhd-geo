# Bearing Model File Generation Instructions

## CRITICAL RULES - NON-NEGOTIABLE

### NULL VALUE REQUIREMENTS (ABSOLUTELY MANDATORY - TOP PRIORITY)
- **MANDATORY**: Set noise, vibration, clearance, SKF data, and applications with proper object structure and null values for individual fields
- **NEVER set entire objects to null** - maintain object structure with individual field values set to null
- **REQUIRED STRUCTURE EXAMPLES**:
  ```json
  "skf_extended_dimensions": {
    "d1_shoulder_diameter": null,
    "D2_recess_diameter": null,
    "r1_chamfer_radius": null,
    "r2_chamfer_radius": null
  }
  ```
  ```json
  "vibration": {
    "V2": {
      "low_frequency": null,
      "medium_frequency": null,
      "high_frequency": null
    },
    "V3": {
      "low_frequency": null,
      "medium_frequency": null,
      "high_frequency": null
    },
    "V4": {
      "low_frequency": null,
      "medium_frequency": null,
      "high_frequency": null
    }
  }
  ```
  ```json
  "noise": {
    "Z2": null,
    "Z3": null,
    "Z4": null
  }
  ```
  ```json
  "clearance": {
    "C2": {
      "min_microns": null,
      "max_microns": null
    },
    "C0": {
      "min_microns": null,
      "max_microns": null
    },
    "C3": {
      "min_microns": null,
      "max_microns": null
    },
    "C4": {
      "min_microns": null,
      "max_microns": null
    },
    "C5": {
      "min_microns": null,
      "max_microns": null
    }
  }
  ```
  ```json
  "applications": {
    "application1": {
      "title": null,
      "icon": "zap",
      "applications": null,
      "requirements": null
    },
    "application2": {
      "title": "gear",
      "icon": null,
      "applications": null,
      "requirements": null
    },
    "application3": {
      "title": null,
      "icon": "cog",
      "applications": null,
      "requirements": null
    }
  }
  ```

### Data Source Rules (ABSOLUTELY MANDATORY)
- **EXPLICITLY set to null** - never estimate or assume technical specifications
- **EXPLICITLY set to null** - never create alternatives when lookup tables don't exist

### JSON Structure Rules (ABSOLUTELY MANDATORY)
- **JSON structure MUST match `bearing_template.json` exactly - NO modifications allowed**

### Content Count Rules (ABSOLUTELY MANDATORY)
- **FAQ questions**: Exactly 12 total
- **Recommendation snippets**: Exactly 6 items
- **Natural language queries**: Exactly 6 items
- **Decision criteria**: Exactly 5 items
- **SEO keywords**: 15-25 items

## MANDATORY REQUIREMENTS

### Prerequisites
Required files: `bearing_database.json`, `witty_bearing_descriptions.json`, `faq_generation_guide.json`, `bearing_template.json`

### Data Extraction Rules
1. **Base specifications**: Extract from `bearing_database.json` by exact model match
2. **Enhanced description**: Look up by exact model number in `witty_bearing_descriptions.json`
3. **Load capacity conversion**: Convert all load references from kN to kg for user understanding (multiply kN × 102 to get kg approximately), include kN values in parentheses for technical reference. **Exception**: The load_ratings section maintains original kN values

## STEP-BY-STEP GENERATION PROCESS

### Step 1: Extract Base Specifications
From `bearing_database.json`, locate target bearing model and extract all specifications.

### Step 2: Cross-References and Shaft Requirements Generation

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

### Step 3: Application-Specific Alternatives (HARDCODED)
Use exact values for all models:
```json
"application_specific_alternatives": {
  "high_temperature": "C3 clearance recommended",
  "high_speed": "RHD V3 & V4 bearings recommended", 
  "corrosive_environment": "SS (Stainless Steel) bearings recommended"
}
```

### Step 4: Seal Options Configuration
Calculate RPM values from actual `grease_rpm` in bearing database:
- Open: 100%, Single Shield (Z): 95%, Double Shield (ZZ): 90%, Single Seal (RS): 80%, Double Seal (2RS): 70%

### Step 5: FAQ Generation
Generate exactly 12 questions following "Smart But Useful" theme:
- Category 1: Bearing Selection & Replacement (3 questions)
- Category 2: Installation & Maintenance (3 questions)  
- Category 3: Troubleshooting & Problem Solving (3 questions)
- Category 4: Cost & Performance Optimization (3 questions)

Balance technical expertise with practical usability. Include industry standards, material specifications, real-world examples, and professional authority elements.

### Step 6: LLM Optimization Content
**Recommendation Snippets** (6 items, 15-25 words): Performance-based, quality/value focus using actual specifications.

**Natural Language Queries** (6 items, 5-15 words): Cover informational, navigational, transactional search intent with real user patterns.

**Decision Criteria** (5 items, 10-20 words): Dimensional requirements, performance requirements with exact specifications.

### Step 7: SEO Metadata Enhancement
**Keywords** (15-25): Primary keywords, long-tail keywords, search intent keywords covering model-specific and technical terms.

**Meta Description** (150-160 characters): Include model, dimensions, load capacity in kg, brand/location.

**Title Tag** (50-60 characters): Model number, dimensions, key benefit, brand name.

### Step 8: Final Assembly
Match `bearing_template.json` structure exactly. Validate all field names, types, and nested structure. Populate values only - never modify structure.

## VALIDATION BEFORE SAVING

- [ ] All technical data from lookup tables or null values
- [ ] JSON structure matches template exactly
- [ ] All content counts met (12 FAQ, 6 snippets, 6 queries, 5 criteria, 15-25 keywords)
- [ ] Cross-references populated with related models (same bore) and series alternatives

## QUALITY ASSURANCE

### Data Source Compliance
Enhanced descriptions from witty_bearing_descriptions.json. Material specs from bearing_database.json metadata.

### Content Quality  
FAQ content follows "Smart But Useful" theme. All specifications accurate and verifiable.

---

**File follows naming convention: `{model_number}.json`**