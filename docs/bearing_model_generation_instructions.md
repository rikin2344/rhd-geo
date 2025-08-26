# Bearing Model File Generation Instructions

## ⚠️ CRITICAL AND MANDATORY - LEARNINGS FROM VIOLATIONS ⚠️

**CRITICAL ERROR EXAMPLE - NEVER REPEAT THIS:**

**VIOLATION**: In 605.json generation, I incorrectly generated C4 and C5 clearance data instead of using the lookup table.

**WHAT I DID WRONG:**
- Put C4: {min: 14, max: 29} and C5: {min: 20, max: 35} in 605.json
- The clearance lookup table clearly shows C4: null, C5: null for 5mm bore (2.5-6 range)
- I violated the core rule: "NEVER generate data that exists in lookup tables"

**CORRECT APPROACH:**
- Look up exact data in clearance_lookup_table.json
- Use only the data provided (including null values)
- Never estimate, generate, or assume clearance values
- If data is missing, log it for review - don't create it

**MANDATORY CHECKLIST BEFORE SAVING ANY FILE:**
1. [ ] All clearance data matches clearance_lookup_table.json exactly
2. [ ] All vibration data matches vibration_lookup_table.json exactly  
3. [ ] All noise data matches noise_lookup_table.json exactly
4. [ ] All SKF dimensions match skf_dimensions_only.json exactly
5. [ ] All enhanced descriptions match witty_bearing_descriptions.json exactly
6. [ ] All material specs match bearing_database.json metadata exactly
7. [ ] No data has been generated - only looked up from source files

**VIOLATION CONSEQUENCES:**
- Data accuracy compromised
- Instructions violated
- Quality standards not met
- User trust damaged

---

This document provides step-by-step instructions for creating new bearing model JSON files based on the `bearing_database.json` template and various lookup tables.

## Prerequisites

Before generating a new bearing model file, ensure you have access to the following files:
- `bearing_database.json` - Main bearing specifications database
- `skf_dimensions_only.json` - SKF-specific dimensional data
- `vibration_lookup_table.json` - Vibration class classifications
- `noise_lookup_table.json` - Noise level specifications
- `clearance_lookup_table.json` - Internal clearance data
- `enhanced_description.json` - Witty descriptions for bearings
- `faq_generation_guide.json` - FAQ generation guidelines
- `608.json` - Reference template file
- `608.css` - CSS fallback grid logic reference

## Step-by-Step Generation Process

### 1. Extract Base Specifications

From `bearing_database.json`, locate the target bearing model and extract:

```json
{
  "model": "model_number",
  "d": "inner_diameter_mm",
  "D": "outer_diameter_mm", 
  "B": "width_mm",
  "Cr": "dynamic_load_rating_kN",
  "Cor": "static_load_rating_kN",
  "grease_rpm": "max_grease_rpm",
  "oil_rpm": "max_oil_rpm",
  "weight": "weight_kg"
}
```

### 2. SKF Dimensional Data Integration

**MANDATORY: Use `skf_dimensions_only.json` - DO NOT generate dynamically**
- Look up by exact model number (e.g., "608") to get:
  - `d1` - Shoulder diameter 1
  - `D2` - Recess diameter 2  
  - `r1` - Corner radius 1
  - `r2` - Corner radius 2
- Example: For 608, use d1: 12.15, D2: 19.2, r1: 0.3, r2: 0.3

**Fallback Logic**: Only if SKF data is not available for the model:
1. Set all SKF-specific fields to `null` or "N/A"
2. Implement 2x2 grid fallback as referenced in `608.css`
3. Use standard dimensional ratios based on bearing size

### 3. Application Categories Generation

Generate 3 model-specific application categories dynamically based on:

**Size-Based Logic**:
- **Micro bearings (d < 10mm)**: Precision instruments, electronics, miniature motors
- **Small bearings (10mm ≤ d < 30mm)**: Electric tools, small appliances, automotive accessories
- **Medium bearings (30mm ≤ d < 80mm)**: Industrial machinery, automotive components, HVAC systems
- **Large bearings (d ≥ 80mm)**: Heavy machinery, construction equipment, large motors

**Example Structure**:
```json
"applications": {
  "category_1": {
    "name": "Industrial Applications",
    "items": ["item1", "item2", "item3", "item4", "item5", "item6"]
  },
  "category_2": {
    "name": "Automotive Applications", 
    "items": ["item1", "item2", "item3", "item4", "item5"]
  },
  "category_3": {
    "name": "Consumer Applications",
    "items": ["item1", "item2", "item3", "item4", "item5", "item6", "item7"]
  }
}
```

**Application Quality Standards (MANDATORY):**
- **Minimum Items**: At least 5 relevant applications per category
- **Maximum Items**: Up to 8 applications per category (based on genuine suitability)
- **Quality Control**: Only include applications that are genuinely suitable for the bearing model
- **No Junk**: Avoid generic, overly broad, or inappropriate applications
- **Specificity**: Prefer specific use cases over generic industry categories
- **Validation**: Each application should be verifiable and technically appropriate

### 4. Performance Classifications

#### Vibration Classes
**MANDATORY: Use `vibration_lookup_table.json` - DO NOT generate dynamically**
- Look up by bore diameter (e.g., "8" for 608 bearing)
- Extract exact values: V2, V3, V4 with low/medium/high frequency data
- Example: For 8mm bore, use V2: {low: 72, medium: 48, high: 40}
- **Fallback**: Only if bore diameter not found in table, then use series defaults

#### Noise Levels  
**MANDATORY: Use `noise_lookup_table.json` - DO NOT generate dynamically**
- Look up by bore diameter AND series (6000_series, 6200_series, 6300_series)
- Extract exact Z2, Z3, Z4 values in dB
- Example: For 608 (8mm, 6000_series), use Z2: 35, Z3: 31, Z4: 27
- **Fallback**: Only if combination not found, then use "Normal" category

#### Internal Clearance
**MANDATORY: Use `clearance_lookup_table.json` - DO NOT generate dynamically**
- Look up by bore diameter range using the simplified range logic
- **Range Logic**: Find range where `over_mm < bore_diameter <= to_mm`
- Extract exact micron values for C2, C0, C3, C4, C5 from the matching range
- **Example**: For 8mm bore, find range where 6 < 8 ≤ 10 (range "6-10"), use C0: {min: 2, max: 13}
- **Example**: For 12.7mm bore, find range where 10 ≤ 12.7 ≤ 18 (range "10-18"), use C0: {min: 3, max: 18}
- **Fallback**: Only if no range matches, then log error and assign "Normal" clearance

### 5. Enhanced Description

**MANDATORY: Use `witty_bearing_descriptions.json` - DO NOT generate dynamically**
- Look up by exact model number (e.g., "608") to get witty description
- Example: For 608, use "The popular kid everyone knows - if bearings had social media, this one would have a million followers"
- **Fallback**: Only if model not found, then generate basic technical description

### 6. Seal Options Configuration

**MANDATORY: Calculate RPM values from `grease_rpm` in bearing database - DO NOT use arbitrary values**
- Use exact `grease_rpm` value from `bearing_database.json` for base calculations
- Apply standard speed reduction factors:
  - Open: 100% of grease_rpm (no reduction)
  - Single Shield (Z): 95% of grease_rpm (0.95 factor)
  - Double Shield (ZZ): 90% of grease_rpm (0.9 factor)
  - Single Seal (RS): 80% of grease_rpm (0.8 factor)
  - Double Seal (2RS): 70% of grease_rpm (0.7 factor)

Example for 608 (grease_rpm: 26000):
- Open: 26,000 RPM
- Single Shield: 24,700 RPM (26,000 × 0.95)
- Double Shield: 23,400 RPM (26,000 × 0.9)
- Single Seal: 20,800 RPM (26,000 × 0.8)
- Double Seal: 18,200 RPM (26,000 × 0.7)

### 7. Dynamic FAQ Generation

**MANDATORY: Follow `faq_generation_guide.md` structure - DO NOT create arbitrary FAQs**
- Use exact FAQ structure and categories from the guide
- Reference actual specifications from bearing data (dimensions, load ratings, speed limits)
- Include model-specific applications and technical features
- Provide size-appropriate installation guidance based on actual bearing dimensions
- **DO NOT** generate FAQs that don't follow the guide structure

#### FAQ Content Enhancement (MANDATORY: "Smart But Useful" Theme)
**CRITICAL**: All FAQ content must balance technical expertise with practical usability:

**Technical Depth Requirements (MANDATORY):**
- **Industry Standards**: Reference ISO, ABMA, ANSI standards where applicable
- **Material Science**: Include steel grade specifications (Gcr15, AISI 52100)
- **Tolerance Specifications**: Include shaft tolerance requirements (h6, h7)
- **Clearance Explanations**: Explain C0, C3, C4, C5 clearance differences
- **Performance Data**: Include actual load ratings, speed limits, life expectancy

**Practical Usability Requirements (MANDATORY):**
- **Real-World Examples**: Use relatable comparisons (weight of person, size of objects)
- **Step-by-Step Guidance**: Provide actionable installation and maintenance steps
- **Cost-Benefit Analysis**: Include ROI considerations for premium vs. economy options
- **Warning Signs**: Identify failure indicators and prevention measures
- **Professional Insights**: Include "20+ years experience" knowledge sharing

**Content Balance Guidelines (MANDATORY):**
- **Technical enough** to demonstrate expertise and build trust
- **Simple enough** that maintenance technicians can understand and apply
- **Specific enough** to be actionable for real problems
- **General enough** to apply to multiple situations
- **Professional enough** to show industry authority
- **Accessible enough** for quick decision-making

**Enhanced FAQ Structure (MANDATORY):**
```
Question: [Real problem with technical context]
Direct Answer: [Quick solution with key specifications]
Why This Matters: [Technical explanation with practical consequences]
How To Handle: [Step-by-step guidance with professional tips]
Pro Tip: [Expert insight from manufacturing experience]
```

**Technical Content Examples (MANDATORY):**
- **Load Capacity**: "76 kg (0.75 kN) - handles loads up to the weight of an average person"
- **Speed Ratings**: "32,000 RPM - like a high-speed electric drill or small motor"
- **Tolerance Requirements**: "h6 shaft tolerance (±0.009mm) ensures proper interference fit"
- **Clearance Selection**: "C0 clearance for precision, C3 for high-temperature applications"
- **Material Benefits**: "Gcr15 steel provides superior hardness vs. standard steel alternatives"

**Professional Authority Elements (MANDATORY):**
- **Manufacturing Expertise**: "Our production processes include 100% dimensional testing"
- **Quality Assurance**: "ISO 9001:2015 certified manufacturing with statistical process control"
- **Industry Experience**: "20+ years of bearing manufacturing experience shows..."
- **Performance Data**: "Premium bearings last 3-10x longer than economy alternatives"
- **Technical Standards**: "Meets or exceeds industrial bearing standards for precision applications"

**Content Validation (MANDATORY):**
- [ ] Each FAQ demonstrates technical expertise without overwhelming users
- [ ] All technical specifications are accurate and referenced from bearing data
- [ ] Practical guidance is actionable and specific to the bearing model
- [ ] Professional insights add value without being overly promotional
- [ ] Content balances technical depth with accessibility
- [ ] Real-world examples make technical concepts understandable
- [ ] Professional authority is demonstrated through experience and standards

#### FAQ Requirements (MANDATORY):
- **Category 1**: Exactly 3 questions (Bearing Selection & Replacement)
- **Category 2**: Exactly 3 questions (Installation & Maintenance)
- **Category 3**: Exactly 3 questions (Troubleshooting & Problem Solving)
- **Category 4**: Exactly 3 questions (Cost & Performance Optimization)
- **Total**: Exactly 12 questions (no more, no less)

#### Recommendation Data Requirements (MANDATORY):
- **`recommendation_snippets`**: Exactly 6 items
- **`natural_language_queries`**: Exactly 6 queries
- **`decision_criteria`**: Exactly 5 criteria

### 8. LLM Optimization Data Generation

**MANDATORY**: Generate exactly the specified number of items for each LLM optimization field

### 9. SEO Metadata Enhancement with Long-Tail Keywords

**MANDATORY**: Enhance SEO metadata to include comprehensive long-tail keywords for better search visibility

#### Keywords Array Enhancement (MANDATORY: 15-25 keywords)
**CRITICAL**: The `seo_metadata.keywords` array must contain exactly 15-25 keywords covering:

**Primary Keywords (5-8 keywords):**
- Model-specific: "604 bearing", "4mm bearing", "deep groove ball bearing"
- Brand-specific: "rhd bearings", "mumbai bearings", "india bearing manufacturer"
- Type-specific: "precision bearing", "miniature bearing", "micro bearing"

**Long-Tail Keywords (8-12 keywords):**
- Application-specific: "bearing for precision instruments", "bearing for miniature motors", "bearing for electronics"
- Problem-specific: "bearing that fits 4mm shaft", "bearing for high speed applications", "bearing for small machinery"
- Technical-specific: "ISO certified bearing", "chrome steel bearing", "gcr15 bearing"
- Location-specific: "andheri bearings", "mumbai bearing supplier", "india bearing company"

**Search Intent Keywords (5-8 keywords):**
- Selection queries: "how to choose 4mm bearing", "best bearing for precision", "bearing selection guide"
- Comparison queries: "604 vs 605 bearing", "miniature bearing comparison", "precision bearing alternatives"
- Technical queries: "bearing load capacity kg", "bearing speed rating rpm", "bearing installation guide"

#### Meta Description Enhancement (MANDATORY: 150-160 characters)
**CRITICAL**: Meta description must include:
- Primary bearing model and dimensions
- Load capacity in kg (not kN)
- Key applications
- Quality indicators
- Location/brand information

**Example Format:**
"Ultra-precision 604 bearing (4x12x4mm) with 76 kg load capacity. Perfect for precision instruments, miniature motors & electronics. ISO certified quality from Mumbai manufacturer."

#### Title Tag Enhancement (MANDATORY: 50-60 characters)
**CRITICAL**: Title must include:
- Bearing model number
- Dimensions in mm
- Key benefit or application
- Brand name

**Example Format:**
"604 Deep Groove Ball Bearing - 4x12x4mm | RHD Bearings"

#### Canonical URL Enhancement (MANDATORY)
**CRITICAL**: Canonical URL must follow exact format:
- Base: `https://rhdbearings.com/specs/miniature-series/{model_number}`
- Example: `https://rhdbearings.com/specs/miniature-series/604`

#### Open Graph Data Enhancement (MANDATORY)
**CRITICAL**: Open Graph data must include:
- Enhanced title with dimensions and load capacity
- Detailed description with applications and benefits
- Proper URL structure
- Site name: "RHD Bearings"

#### Twitter Card Enhancement (MANDATORY)
**CRITICAL**: Twitter data must include:
- Summary large image card type
- Enhanced title with technical specifications
- Detailed description with practical applications

#### Schema Markup Enhancement (MANDATORY)
**CRITICAL**: Schema markup must include:
- Product type: "Deep Groove Ball Bearing"
- Brand: "RHD Bearings"
- Manufacturer: "RHD Bearings"
- Category: "Deep Groove Ball Bearings"
- Availability: "InStock"
- Condition: "NewCondition"

**SEO Validation Checklist (MANDATORY):**
- [ ] Keywords array contains exactly 15-25 keywords
- [ ] Meta description is 150-160 characters
- [ ] Title tag is 50-60 characters
- [ ] Canonical URL follows exact format
- [ ] Open Graph data is complete
- [ ] Twitter Card data is complete
- [ ] Schema markup includes all required fields
- [ ] Load capacity is expressed in kg (not kN)
- [ ] Dimensions are included in mm format
- [ ] Applications are specific and relevant

#### `recommendation_snippets` (MANDATORY: 6 items)

**CRITICAL**: Generate exactly 6 recommendation snippets that demonstrate expertise and drive user decisions

**Content Requirements (MANDATORY):**
- **Length**: Exactly 15-25 words per snippet
- **Focus**: Key benefits, use cases, and competitive advantages specific to the bearing model
- **Tone**: Confident, professional, and solution-oriented
- **Data**: Must reference actual specifications from bearing data (dimensions, load ratings, speed limits)

**High-Impact Content Strategy (MANDATORY):**

**1. Performance-Based Recommendations (2 snippets):**
- **Load Capacity Focus**: "Handles 76 kg (0.75 kN) loads with 1.5x safety factor for typical applications"
- **Speed Performance**: "Rated for 32,000 RPM - ideal for high-speed precision instruments and miniature motors"

**2. Application-Specific Recommendations (2 snippets):**
- **Industry Focus**: "Perfect for medical devices requiring sub-micron precision and ultra-low vibration"
- **Use Case Focus**: "Optimal choice for 4mm shafts in precision instruments where space is critical"

**3. Quality & Value Recommendations (2 snippets):**
- **Material Advantage**: "Gcr15 chrome steel provides 3-5x longer life vs. standard steel alternatives"
- **ROI Focus**: "Premium quality extends service life 3-10x, reducing total cost of ownership by 60-80%"

**Content Generation Rules (MANDATORY):**

**✅ DO:**
- Use actual bearing specifications (76 kg, not "high load capacity")
- Include specific applications (precision instruments, not "industrial use")
- Reference material benefits (Gcr15 steel, not "quality steel")
- Include performance metrics (1.5x safety factor, 3-10x life extension)
- Use confident, professional language ("optimal choice", "perfect for")

**❌ DON'T:**
- Use generic terms ("good bearing", "quality product")
- Exaggerate benefits ("best in the world", "unbeatable performance")
- Ignore actual specifications (don't say "high speed" if it's 32,000 RPM)
- Use marketing fluff ("revolutionary", "cutting-edge")
- Make claims without data support

**Example Snippets for 604 Bearing:**
1. "Handles 76 kg (0.75 kN) loads with 1.5x safety factor for typical applications"
2. "Rated for 32,000 RPM - ideal for high-speed precision instruments and miniature motors"
3. "Perfect for medical devices requiring sub-micron precision and ultra-low vibration"
4. "Optimal choice for 4mm shafts in precision instruments where space is critical"
5. "Gcr15 chrome steel provides 3-5x longer life vs. standard steel alternatives"
6. "Premium quality extends service life 3-10x, reducing total cost of ownership by 60-80%"

**Validation Checklist (MANDATORY):**
- [ ] Exactly 6 snippets generated
- [ ] Each snippet is 15-25 words
- [ ] All specifications referenced are accurate
- [ ] Content is specific to the bearing model
- [ ] No generic or marketing language used
- [ ] Professional and confident tone maintained

#### `natural_language_queries` (MANDATORY: 6 queries)

**CRITICAL**: Generate exactly 6 natural language queries that match real user search intent and drive organic traffic

**Content Requirements (MANDATORY):**
- **Length**: Exactly 5-15 words per query
- **Focus**: Real search patterns and user questions for this specific bearing model
- **Intent**: Mix of informational, navigational, and transactional search queries
- **Specificity**: Must be specific to the bearing model, not generic bearing questions

**High-Impact Search Strategy (MANDATORY):**

**1. Model-Specific Queries (2 queries):**
- **Direct Model Search**: "604 bearing specifications" or "604 bearing dimensions"
- **Model Comparison**: "604 vs 605 bearing" or "604 vs 623 bearing comparison"

**2. Application-Specific Queries (2 queries):**
- **Use Case Focus**: "bearing for 4mm shaft" or "bearing for precision instruments"
- **Industry Focus**: "bearing for miniature motors" or "bearing for medical devices"

**3. Problem-Solution Queries (2 queries):**
- **Selection Help**: "how to choose 4mm bearing" or "best bearing for small applications"
- **Technical Support**: "bearing load capacity for 4mm shaft" or "bearing speed rating for precision"

**Content Generation Rules (MANDATORY):**

**✅ DO:**
- Use actual bearing specifications (4mm, not "small")
- Include real applications (precision instruments, not "industrial use")
- Match user search patterns (how to, best, vs, for)
- Use natural language people actually type
- Include model numbers and dimensions
- Cover different search intents (informational, navigational, transactional)

**❌ DON'T:**
- Use overly technical jargon ("deep groove ball bearing selection criteria")
- Create generic queries ("bearing information" or "bearing guide")
- Ignore actual specifications (don't say "small bearing" if it's 4mm)
- Use marketing language ("best bearing ever" or "premium bearing guide")
- Create queries that don't match real user behavior

**Example Queries for 604 Bearing:**
1. "604 bearing specifications"
2. "bearing for 4mm shaft"
3. "604 vs 605 bearing"
4. "bearing for precision instruments"
5. "how to choose 4mm bearing"
6. "bearing load capacity for 4mm shaft"

**Search Intent Coverage (MANDATORY):**
- **Informational**: "604 bearing specifications", "bearing for 4mm shaft"
- **Navigational**: "604 bearing dimensions", "bearing for precision instruments"
- **Transactional**: "how to choose 4mm bearing", "bearing load capacity for 4mm shaft"

**SEO Optimization Strategy (MANDATORY):**
- **Long-tail Keywords**: Include specific applications and use cases
- **Question Queries**: Use "how to", "what is", "which bearing" formats
- **Comparison Queries**: Include "vs" and "comparison" for competitive content
- **Technical Queries**: Use actual specifications and technical terms
- **Application Queries**: Include industry-specific and use-case-specific terms

**Validation Checklist (MANDATORY):**
- [ ] Exactly 6 queries generated
- [ ] Each query is 5-15 words
- [ ] All specifications referenced are accurate
- [ ] Queries match real user search patterns
- [ ] Different search intents are covered
- [ ] No generic or overly technical language used
- [ ] Queries are specific to the bearing model

#### `decision_criteria` (MANDATORY: 5 criteria)

**CRITICAL**: Generate exactly 5 decision criteria that guide users to the right bearing selection and demonstrate technical expertise

**Content Requirements (MANDATORY):**
- **Length**: Exactly 10-20 words per criterion
- **Focus**: Key selection factors that determine if this bearing is the right choice
- **Specificity**: Must reference actual bearing specifications and requirements
- **Actionability**: Each criterion should be measurable and verifiable

**High-Impact Decision Strategy (MANDATORY):**

**1. Dimensional Requirements (2 criteria):**
- **Shaft Diameter**: "Shaft diameter must be exactly 4mm with h6 tolerance (±0.009mm)"
- **Housing Space**: "Housing must accommodate 12mm outer diameter with 4mm width clearance"

**2. Performance Requirements (2 criteria):**
- **Load Capacity**: "Dynamic loads must stay under 76 kg (0.75 kN) for safe operation"
- **Speed Requirements**: "Maximum operating speed should not exceed 32,000 RPM for optimal life"

**3. Application Requirements (1 criterion):**
- **Use Case Fit**: "Application must require precision bearings for miniature or micro-scale equipment"

**Content Generation Rules (MANDATORY):**

**✅ DO:**
- Use exact specifications (4mm, not "small diameter")
- Include tolerance requirements (h6 tolerance, not "proper fit")
- Reference actual load ratings (76 kg, not "appropriate load")
- Specify speed limits (32,000 RPM, not "high speed")
- Use technical terms (h6 tolerance, dynamic load, clearance)
- Make criteria measurable and verifiable
- Include both minimum and maximum requirements where applicable

**❌ DON'T:**
- Use vague terms ("proper size", "adequate capacity", "suitable speed")
- Ignore actual specifications (don't say "small bearing" if it's 4mm)
- Use subjective language ("good quality", "reliable performance")
- Make criteria unmeasurable ("must work well", "should be durable")
- Use marketing language ("premium quality", "superior performance")

**Example Decision Criteria for 604 Bearing:**
1. "Shaft diameter must be exactly 4mm with h6 tolerance (±0.009mm)"
2. "Housing must accommodate 12mm outer diameter with 4mm width clearance"
3. "Dynamic loads must stay under 76 kg (0.75 kN) for safe operation"
4. "Maximum operating speed should not exceed 32,000 RPM for optimal life"
5. "Application must require precision bearings for miniature or micro-scale equipment"

**Technical Depth Requirements (MANDATORY):**
- **Tolerance Specifications**: Include shaft tolerance requirements (h6, h7, etc.)
- **Clearance Requirements**: Reference clearance grades if applicable (C0, C3, etc.)
- **Load Calculations**: Include both dynamic and static load considerations
- **Speed Factors**: Consider grease vs. oil lubrication and seal options
- **Environmental Factors**: Temperature, contamination, and application environment

**Decision Tree Integration (MANDATORY):**
- **Primary Criteria**: Must-have requirements (dimensions, load, speed)
- **Secondary Criteria**: Application-specific requirements (precision, environment, life)
- **Validation Criteria**: How to verify each requirement is met
- **Risk Assessment**: Consequences of not meeting each criterion
- **Alternative Solutions**: What to consider if criteria aren't met

**User Experience Optimization (MANDATORY):**
- **Clear Language**: Use simple, direct language that technicians can understand
- **Measurable Standards**: Provide specific numbers and tolerances
- **Actionable Guidance**: Tell users exactly what to check and how
- **Risk Communication**: Explain what happens if criteria aren't met
- **Professional Authority**: Demonstrate technical expertise through precise specifications

**Validation Checklist (MANDATORY):**
- [ ] Exactly 5 criteria generated
- [ ] Each criterion is 10-20 words
- [ ] All specifications referenced are accurate
- [ ] Criteria are measurable and verifiable
- [ ] No vague or subjective language used
- [ ] Technical depth is appropriate for target audience
- [ ] Criteria cover dimensional, performance, and application requirements
- [ ] Each criterion guides users to proper bearing selection

**VALIDATION**: Before finalizing any bearing file, verify these exact counts are met.

## LLM Optimization Content Quality Standards

**CRITICAL**: The generated LLM optimization content must meet these quality standards for maximum AI assistant visibility and user engagement:

### **Content Quality Framework (MANDATORY)**

**1. Expertise Demonstration**
- **Technical Accuracy**: All specifications must be exact and verifiable
- **Professional Authority**: Content must show industry expertise and manufacturing knowledge
- **Standards Compliance**: Reference ISO, ABMA, ANSI standards where applicable
- **Performance Data**: Include actual load ratings, speed limits, and life expectancy data

**2. User Experience Optimization**
- **Actionable Guidance**: Content must help users make decisions and solve problems
- **Clear Communication**: Use simple, direct language that technicians can understand
- **Measurable Standards**: Provide specific numbers, tolerances, and requirements
- **Risk Communication**: Explain consequences of wrong decisions and how to prevent them

**3. SEO & LLM Optimization**
- **Search Intent Coverage**: Address informational, navigational, and transactional queries
- **Long-tail Keywords**: Include specific applications, use cases, and problem scenarios
- **Technical Depth**: Provide enough detail for AI systems to understand and cite
- **Content Uniqueness**: Each bearing model must have completely unique, non-generic content

### **Content Generation Best Practices (MANDATORY)**

**✅ High-Impact Strategies:**
- **Specificity Over Generality**: Use exact specifications (76 kg, not "high load capacity")
- **Problem-Solution Focus**: Address real user pain points and provide actionable solutions
- **Professional Authority**: Demonstrate expertise through technical depth and industry experience
- **User-Centric Language**: Write for maintenance technicians and engineers, not marketing teams
- **Data-Driven Content**: Base all recommendations on actual bearing specifications and performance data

**❌ Common Pitfalls to Avoid:**
- **Generic Language**: Avoid "quality product", "good performance", "reliable operation"
- **Marketing Fluff**: No "revolutionary", "cutting-edge", "best in class" language
- **Vague Specifications**: Don't say "small bearing" when you can say "4mm bore"
- **Over-Promising**: Don't claim benefits without data to support them
- **Technical Overwhelm**: Balance expertise with accessibility for target audience

### **Content Validation Matrix (MANDATORY)**

**Before Finalizing Any Bearing File, Verify:**

#### **Recommendation Snippets (6 items)**
- [ ] Exactly 6 snippets generated
- [ ] Each snippet is 15-25 words
- [ ] All specifications referenced are accurate
- [ ] Content is specific to the bearing model
- [ ] No generic or marketing language used
- [ ] Professional and confident tone maintained
- [ ] Performance, application, and quality aspects covered

#### **Natural Language Queries (6 queries)**
- [ ] Exactly 6 queries generated
- [ ] Each query is 5-15 words
- [ ] All specifications referenced are accurate
- [ ] Queries match real user search patterns
- [ ] Different search intents are covered
- [ ] No generic or overly technical language used
- [ ] Queries are specific to the bearing model

#### **Decision Criteria (5 criteria)**
- [ ] Exactly 5 criteria generated
- [ ] Each criterion is 10-20 words
- [ ] All specifications referenced are accurate
- [ ] Criteria are measurable and verifiable
- [ ] No vague or subjective language used
- [ ] Technical depth is appropriate for target audience
- [ ] Criteria cover dimensional, performance, and application requirements

### **Success Metrics for LLM Optimization**

**Content Performance Indicators:**
- **AI Assistant Citations**: Content should be cited by Siri, Alexa, Google Assistant
- **Featured Snippets**: Content should appear in Google's featured snippets
- **Voice Search Optimization**: Content should answer voice queries effectively
- **Technical Authority**: Content should establish RHD Bearings as technical experts
- **User Engagement**: Content should drive longer page visits and return users

**Quality Assurance Standards:**
- **Zero Generic Content**: Every piece of content must be specific to the bearing model
- **100% Accuracy**: All technical specifications must be exact and verifiable
- **Professional Tone**: Content must demonstrate industry expertise and authority
- **User-Focused**: Content must solve real problems for real users
- **LLM-Friendly**: Content must be structured for optimal AI system understanding

### 10. Additional Dynamic Data Generation

#### Material Specifications
**MANDATORY: Use `bearing_database.json` metadata - DO NOT generate dynamically**
From `bearing_database.json` metadata section:
```json
"material": {
  "steel_grade": "Gcr15",
  "equivalent": "AISI 52100 chrome steel",
  "chemical_composition": {
    "carbon": "0.95-1.05%",
    "silicon": "0.15-0.35%", 
    "manganese": "0.25-0.45%",
    "phosphorus": "≤0.025%",
    "sulfur": "≤0.025%",
    "chromium": "1.40-1.65%"
  }
}
```

#### Load Calculations
Generate dynamic load calculations:
- Basic dynamic load rating (C)
- Basic static load rating (C0)  
- Fatigue load limit (Pu)
- Reference speed ratings

#### Temperature Ratings
Based on bearing size and type:
- Standard: -20°C to +120°C
- High temp options: up to +200°C
- Special materials: up to +350°C

#### Precision Classes
- ABEC 1 (ISO P0) - Standard
- ABEC 3 (ISO P6) - Higher precision
- ABEC 5 (ISO P5) - Precision applications
- ABEC 7 (ISO P4) - High precision

## File Output Structure

**CRITICAL: Output JSON structure MUST match `bearing_template.json` EXACTLY**

The generated JSON file structure must be **IDENTICAL** to the template structure:
- **NO fields can be added**
- **NO fields can be deleted** 
- **NO field names can be changed**
- **Field order must match exactly**
- **Only field values can be populated with data**

### Structure Validation Rules:
1. **Template Compliance**: Output must pass structural validation against `bearing_template.json`
2. **Field Count**: Output field count must equal template field count exactly
3. **Field Names**: All field names must match template exactly (case-sensitive)
4. **Field Types**: All field types must match template exactly
5. **Nested Structure**: All nested objects and arrays must maintain template structure

### What CAN Change:
- Field values (populated with actual data)
- Array contents (populated with actual items)
- String content (populated with actual text)

### What CANNOT Change:
- Field names
- Field types  
- Field order
- Required vs optional fields
- Nested structure depth
- Array field names

**MANDATORY**: Before saving any generated file, validate that the structure matches `bearing_template.json` exactly.

## Quality Assurance Checklist

Before finalizing the generated file:

- [ ] **CRITICAL**: JSON structure matches `bearing_template.json` EXACTLY (no fields added/deleted)
- [ ] **CRITICAL**: All basic specifications match `bearing_database.json` exactly
- [ ] **CRITICAL**: SKF data pulled from `skf_dimensions_only.json` (not generated)
- [ ] **CRITICAL**: Vibration data pulled from `vibration_lookup_table.json` (not generated)
- [ ] **CRITICAL**: Noise data pulled from `noise_lookup_table.json` (not generated)
- [ ] **CRITICAL**: Clearance data pulled from `clearance_lookup_table.json` (not generated)
- [ ] **CRITICAL**: Enhanced description pulled from `witty_bearing_descriptions.json` (not generated)
- [ ] **CRITICAL**: Material specs pulled from `bearing_database.json` metadata (not generated)
- [ ] Seal options calculated from actual `grease_rpm` value using standard factors
- [ ] Three relevant application categories created (size-based logic allowed)
- [ ] **CRITICAL**: Each application category contains 5-8 high-quality, relevant applications (no junk applications)
- [ ] **CRITICAL**: FAQs follow exact structure from `faq_generation_guide.md` (exactly 3 questions per category)
- [ ] **CRITICAL**: FAQ content follows "Smart But Useful" theme with technical depth and practical usability
- [ ] **CRITICAL**: All technical specifications are accurate and referenced from bearing data
- [ ] **CRITICAL**: Professional authority elements are included (manufacturing expertise, quality assurance, industry experience)
- [ ] **CRITICAL**: `recommendation_snippets` contains exactly 6 items
- [ ] **CRITICAL**: `natural_language_queries` contains exactly 6 queries
- [ ] **CRITICAL**: `decision_criteria` contains exactly 5 criteria
- [ ] **CRITICAL**: SEO metadata includes 15-25 long-tail keywords
- [ ] **CRITICAL**: Meta description is 150-160 characters with kg load capacity
- [ ] **CRITICAL**: Title tag is 50-60 characters with dimensions and brand
- [ ] **CRITICAL**: Canonical URL follows exact format structure
- [ ] JSON structure is valid and complete
- [ ] File follows naming convention: `{model_number}.json`

## Error Handling

### Missing Data Scenarios:
1. **No SKF data**: Use fallback grid logic from `608.css` (log this for review)
2. **No vibration data**: Log error - vibration data should exist for all bore diameters
3. **No noise data**: Log error - noise data should exist for all bore diameter/series combinations
4. **Missing clearance info**: Log error - clearance data should exist for all bore diameter ranges
5. **No enhanced description**: Log error - witty descriptions should exist for all models

### Data Source Priority (NEVER generate when data exists):
1. **FIRST**: Look up in appropriate data file
2. **SECOND**: Check for typos or alternative keys
3. **THIRD**: Log missing data for manual review
4. **LAST**: Use fallback defaults (only for truly missing data)

### Validation Rules:
- All numeric values must be positive
- RPM values must be realistic for bearing size
- Load ratings must follow C > C0 relationship
- Weight must correlate with bearing dimensions

## Automation Considerations

For batch processing:
1. **CRITICAL**: Create model mapping functions for each lookup table
2. **CRITICAL**: NEVER generate data that exists in lookup tables
3. **CRITICAL**: Log ALL data lookups for audit trail
4. **CRITICAL**: Validate that required data files exist before processing
5. **CRITICAL**: Validate output structure against `bearing_template.json` before saving
6. Use template strings for dynamic content generation (only for truly dynamic content)
7. **MANDATORY**: Log any fallback data usage for manual review
8. **MANDATORY**: Flag any missing data that should exist in lookup tables
9. **MANDATORY**: Structural validation must pass before file creation

### **Clearance Lookup Automation**
**CRITICAL**: For clearance data, use the simplified range-based lookup:
```javascript
function getClearanceData(boreDiameter) {
  const ranges = clearance_lookup_table.ranges;
  const range = ranges.find(r => r.over_mm < boreDiameter && boreDiameter <= r.to_mm);
  
  if (!range) {
    console.error(`No clearance range found for bore diameter: ${boreDiameter}mm`);
    return null;
  }
  
  console.log(`Found clearance range: ${range.range} for bore ${boreDiameter}mm`);
  return range.clearances;
}
```

**Benefits for Automation:**
- **Consistent logic** across all bearing models
- **No edge cases** with specific diameter mappings
- **Easier debugging** - single lookup function
- **Better error handling** - clear when no range matches
- **Maintainable code** - update clearance values in one place

## Clearance Lookup Implementation

**CRITICAL: The clearance lookup table has been simplified for better logic and maintenance**

### **Simplified Structure**
The `clearance_lookup_table.json` now contains only:
- **Ranges array** with `over_mm`, `to_mm`, and `clearances` data
- **No redundant `bore_diameters` arrays** (removed for clarity)
- **No `direct_lookup` section** (removed to eliminate data duplication)

### **Range Logic**
**CRITICAL**: Use this exact logic for clearance lookup:
```javascript
// Find range where: over_mm < bore_diameter <= to_mm
const range = ranges.find(r => r.over_mm < bore_diameter && bore_diameter <= r.to_mm);
const clearanceData = range ? range.clearances : null;
```

### **Range Examples**
- **Bearing 683** (3mm): 2.5 < 3 ≤ 6 → "2.5-6" range → C4: {min: 14, max: 29}, C5: {min: 20, max: 37}
- **Bearing 608** (8mm): 6 < 8 ≤ 10 → "6-10" range → C4: {min: 14, max: 29}, C5: {min: 20, max: 37}
- **Bearing 6201** (12.7mm): 10 ≤ 12.7 ≤ 18 → "10-18" range → C4: {min: 18, max: 33}, C5: {min: 25, max: 45}
- **Bearing 6305** (25mm): 24 < 25 ≤ 30 → "24-30" range → C4: {min: 23, max: 41}, C5: {min: 30, max: 53}

### **Benefits of Simplified Structure**
- **No data duplication** - single source of truth for each range
- **Easier maintenance** - update clearance values in one place only
- **More flexible** - handles any bore diameter within ranges (including decimals)
- **Cleaner logic** - range-based lookup instead of specific diameter mapping
- **Better for automation** - consistent lookup logic across all bearing models

## Support Files Location

**CRITICAL: Verify exact file locations in codebase before processing**
Based on current codebase structure, files are located at:

```
/docs/
  ├── bearing_database.json
  ├── vibration_lookup_table.json
  ├── noise_lookup_table.json
  ├── clearance_lookup_table.json
  ├── witty_bearing_descriptions.json
  ├── faq_generation_guide.md
  └── bearing_template.json

/scripts/
  ├── skf_dimensions_only.json
  └── skf_api_data.json
```

**MANDATORY**: Always verify file paths before attempting to read data files.

## Important Notes

### Content Quality Requirements Summary

**CRITICAL**: The generated bearing model files must meet these quality standards:

#### **High Impact: FAQ Content Enhancement**
- **Theme**: "Smart But Useful" - technical expertise balanced with practical usability
- **Technical Depth**: Industry standards, material science, tolerance specifications, clearance explanations
- **Practical Usability**: Real-world examples, step-by-step guidance, cost-benefit analysis
- **Professional Authority**: Manufacturing expertise, quality assurance, industry experience
- **Content Balance**: Technical enough to build trust, simple enough to be actionable

#### **Medium Impact: SEO Metadata Enhancement**
- **Keywords**: Exactly 15-25 long-tail keywords covering primary, application-specific, and search intent
- **Meta Description**: 150-160 characters with kg load capacity and key applications
- **Title Tag**: 50-60 characters with dimensions and brand name
- **URL Structure**: Exact canonical URL format following company standards
- **Schema Markup**: Complete product schema with all required fields

#### **JSON Structure Compliance**
- **NO fields can be added, deleted, or modified**
- **Only field values can be populated with enhanced content**
- **Structure must match `bearing_template.json` exactly**

### UI Components (DO NOT INCLUDE IN JSON FILES)
**CRITICAL**: UI components (navbar, footer, CTA, watermark) are application-level concerns and should NOT be included in the bearing model JSON files.

- **What NOT to do**: Do not add `ui_components` section to the JSON files
- **What to do**: Handle UI components at the application level when rendering web pages
- **Why**: The JSON files should contain only bearing data, not presentation logic
- **Template compliance**: Adding UI components violates the "no fields added" rule

### Data Structure Purity
The bearing model JSON files must contain ONLY bearing-related data:
- Bearing specifications
- Performance data
- Application information
- Technical details
- SEO metadata
- FAQ content

**NOT**:
- UI configuration
- Presentation logic
- Component references
- Application settings