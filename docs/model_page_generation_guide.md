# Model Page Generation Guide for Ball Bearing Specifications

## Overview
This comprehensive guide documents the process for creating individual bearing model pages based on the successful 608 bearing page implementation. The 608 page serves as the **single source of truth** for UI/UX patterns, component structure, and technical implementation across all model pages.

## Table of Contents
1. [Data Sources & Architecture](#data-sources--architecture)
2. [Page Structure & Components](#page-structure--components)
3. [JSON Data Integration](#json-data-integration)
4. [Dynamic FAQ Generation](#dynamic-faq-generation)
5. [Reusable Components](#reusable-components)
6. [UI/UX Standards](#uiux-standards)
7. [Technical Implementation](#technical-implementation)
8. [Deployment Process](#deployment-process)
9. [Quality Checklist](#quality-checklist)
10. [Troubleshooting](#troubleshooting)

## Data Sources & Architecture

### Primary Data Source
- **File**: `output/generated_bearings_complete.json`
- **Purpose**: Contains all technical specifications, material data, applications, vibration/noise/clearance data, cross-references, and SEO metadata
- **Usage**: Extract ALL data except FAQs from this file

### Dynamic FAQ Generation
- **Guide**: `docs/faq_generation_guide.md`
- **Purpose**: Generate model-specific FAQs using AI/LLM based on bearing specifications
- **Approach**: Create 4 questions per category (16 total) tailored to the specific model
- **Categories**: Selection & Replacement, Installation & Maintenance, Troubleshooting, Cost & Performance Optimization

### What NOT to Use from JSON
- ❌ **FAQs from JSON**: These are generic and not model-specific
- ❌ **LLM Optimization content**: Replace with dynamic generation
- ❌ **Generic descriptions**: Enhance with model-specific context
- ❌ **Applications from JSON**: These are identical across models and not model-specific

### What MUST Be Dynamically Generated
- ✅ **Hero Description**: Enhanced model-specific description beyond JSON `enhanced_description`
- ✅ **Flip Card Explanations**: Plain English explanations for all 6 specification cards
- ✅ **Load Capacity Calculations**: Convert kN to kg and real-world examples
- ✅ **Speed Context**: Convert RPM to rotations per second and practical comparisons
- ✅ **Application Context**: Model-specific application guidance
- ✅ **Applications Section**: Generate model-specific applications based on bearing size, load capacity, and typical use cases
- ✅ **Extended Dimensional Data**: Use SKF API to get d₁, D₂, r₁, r₂ values with fallback strategy
- ✅ **Breadcrumb Navigation**: Model-specific breadcrumbs
- ✅ **Related Model Lists**: Dynamically determine related models from JSON cross-references
- ✅ **Section Headers**: All section titles must include model number (e.g., "608 BEARING SPECIFICATIONS")
- ✅ **Button Links**: Navigation links in hero actions for internal page navigation

## Page Structure & Components

### 1. Hero Section
```html
<section class="hero">
    <div class="container">
        <div class="hero-content">
            <h1>[MODEL] Deep Groove Ball Bearing</h1>
            <p class="hero-subtitle">[DIMENSIONS] - [DESCRIPTION]</p>
            <div class="hero-stats">
                <!-- Load capacity, speed, applications count -->
            </div>
            
            <!-- Hero Actions (CRITICAL - often missing) -->
            <div class="hero-actions">
                <a href="#specifications" class="btn btn-primary">Technical Specifications</a>
                <a href="#applications" class="btn btn-secondary">Applications</a>
                <a href="tel:+91-9702081858" class="btn btn-accent">📞 Call +91-9702081858</a>
            </div>
        </div>
        <div class="hero-image">
            <!-- Technical drawing image -->
        </div>
    </div>
</section>
```

### 2. Specifications Section
```html
<section class="section" id="specifications">
    <div class="container">
        <div class="section-header">
            <h2 class="section-title">[MODEL] BEARING SPECIFICATIONS</h2>
            <p class="section-subtitle">Precision-engineered for reliability and performance</p>
        </div>
        
        <!-- Dimensions and Image Section (70% / 30% split) -->
        <div class="specs-main-section">
            <div class="dimensions-table">
                <div class="spec-card dimensions-card">
                    <h3><span class="spec-icon">📏</span>Dimensions</h3>
                    <div class="dimensions-grid">
                        <!-- Row 1: Basic dimensions -->
                        <div class="dimension-item">
                            <div class="dimension-label">d - ID (Bore Diameter)</div>
                            <div class="dimension-value">[bore_diameter]mm</div>
                        </div>
                        <div class="dimension-item">
                            <div class="dimension-label">D - OD (Outer Diameter)</div>
                            <div class="dimension-value">[outer_diameter]mm</div>
                        </div>
                        <div class="dimension-item">
                            <div class="dimension-label">B - Width</div>
                            <div class="dimension-value">[width]mm</div>
                        </div>
                        <!-- Row 2: Extended dimensions (if available from SKF API) -->
                        <div class="dimension-item">
                            <div class="dimension-label">d₁ - Shoulder Diameter</div>
                            <div class="dimension-value">≈[d1]mm</div>
                        </div>
                        <div class="dimension-item">
                            <div class="dimension-label">D₂ - Recess Diameter</div>
                            <div class="dimension-value">≈[D2]mm</div>
                        </div>
                        <div class="dimension-item">
                            <div class="dimension-label">r₁,₂ - Chamfer Radius</div>
                            <div class="dimension-value">min. [r1]mm</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="specs-image">
                <h3 class="specs-image-title">Ball Bearing Cross Section</h3>
                <img src="[technical_drawing.image_url]" alt="[technical_drawing.image_alt]" />
            </div>
        </div>
        
        <!-- Flip Cards Row 1: Load Ratings, Speed Limits, Material & Quality -->
        <div class="specs-cards-row">
            <!-- 3 flip cards -->
        </div>
        
        <!-- Flip Cards Row 2: Vibration Classes, Noise Levels, Internal Clearance -->
        <div class="specs-cards-row">
            <!-- 3 flip cards -->
        </div>
    </div>
</section>
```

### 3. Interactive Flip Cards
- **Front**: Technical specifications
- **Back**: Plain English explanations with neon green background
- **Mobile**: Tap to flip functionality
- **Desktop**: Hover to flip functionality

### 4. Seal Options
- **Two-tier system**: First row uses flip cards, second row uses modal popups
- **First Row (Popular)**: ZZ and 2RS options as flip cards with hover-to-flip functionality
- **Second Row (Others)**: Open, -Z, -RS options with modal popup system  
- **Popular badges** for ZZ and 2RS options
- **Grid layout** with 2 popular options on top row, 3 other options on bottom row
- **Detailed specifications** for each seal type
- **Modal explanations** for second row options with usage guidance
- **Clean interface** that maintains consistent card heights and layout

### 5. Applications Section
- **Compressed card design** matching 6000 series style
- **Sticky requirements** at bottom of cards
- **Icon colors** matching brand theme
- **Industrial and household categories**

### 6. FAQs Section
- **Collapsible categories** (none expanded by default)
- **4 questions per category** (16 total)
- **Structured format**: Direct Answer, Why This Matters, How To Handle It, Pro Tip

### 7. Cross References & Alternatives
- **Related models** with direct links
- **Series alternatives** for different applications
- **Application-specific options**

### 8. Expertise Signals
- **6 professional insight cards**
- **Technical credibility indicators**
- **Manufacturing experience highlights**

### 9. Shared Components
- **Header**: Reusable navbar
- **Footer**: Modern contained footer card
- **CTA**: Dynamic model-specific call-to-action
- **Watermark**: Bottom page branding element

## SKF API Integration for Extended Dimensions

### Overview
To provide complete dimensional specifications, integrate with SKF's API to fetch additional dimensional parameters (d₁, D₂, r₁, r₂) that are not available in our internal JSON data.

### API Endpoint
```
https://search.skf.com/prod/search-skfcom/rest/apps/commercial_catalogue_v1/searchers/details
```

### Required Parameters
- `designation`: Model number (e.g., "607", "608")
- `language`: "en"
- `system`: "metric" (preferred) or "imperial"
- `searcher`: "details"
- `site`: "319" (SKF Australia)

### Implementation Strategy

#### 1. SKF API Tool
Use the provided `scripts/skf_api_call.py` tool to extract dimensional data:

```python
# Example usage
from scripts.skf_api_call import SKFAPIBearingScraper

scraper = SKFAPIBearingScraper()
result = scraper.get_complete_bearing_info("607")

if result and 'dimensions' in result:
    d1 = result['dimensions'].get('d1')      # Shoulder diameter
    D2 = result['dimensions'].get('D2')      # Recess diameter  
    r1 = result['dimensions'].get('r1')      # Chamfer radius
    r2 = result['dimensions'].get('r2')      # Chamfer radius (usually = r1)
```

#### 2. Fallback Strategy
**Always implement graceful fallback**:

```html
<!-- If SKF API successful -->
<div class="dimension-item">
    <div class="dimension-label">d₁ - Shoulder Diameter</div>
    <div class="dimension-value">≈[d1]mm</div>
</div>
<div class="dimension-item">
    <div class="dimension-label">D₂ - Recess Diameter</div>
    <div class="dimension-value">≈[D2]mm</div>
</div>
<div class="dimension-item">
    <div class="dimension-label">r₁,₂ - Chamfer Radius</div>
    <div class="dimension-value">min. [r1]mm</div>
</div>

<!-- If SKF API fails, show only basic dimensions -->
<!-- Standard d, D, B, Weight layout -->
```

#### 3. Data Validation
- **Verify reasonable values**: d₁ should be > d, D₂ should be < D
- **Check for null/missing data**: Handle gracefully
- **Cache results**: Store successful API responses to avoid repeated calls

#### 4. Error Handling
```python
try:
    api_dimensions = scraper.get_complete_bearing_info(model_number)
    if api_dimensions and 'dimensions' in api_dimensions:
        # Use extended dimensions
        use_extended_dimensions = True
    else:
        # Fall back to basic dimensions only
        use_extended_dimensions = False
except Exception as e:
    print(f"SKF API failed for {model_number}: {e}")
    use_extended_dimensions = False
```

### Expected Values by Model
Based on successful API extractions:

| Model | d₁ (mm) | D₂ (mm) | r₁,₂ (mm) |
|-------|---------|---------|-----------|
| 607   | 11.1    | 16.5    | 0.3       |
| 608   | 12.15   | 19.2    | 0.3       |
| 6205  | 34.35   | 46.21   | 1.0       |
| 609   | 14.45   | 21.2    | 0.3       |

### Display Format
- **d₁, D₂**: Use "≈" prefix to indicate approximate values
- **r₁,₂**: Use "min." prefix for minimum chamfer radius
- **Layout**: 3×2 grid (3 columns, 2 rows) for 6 dimensional parameters
- **Order**: Row 1: d, D, B | Row 2: d₁, D₂, r₁,₂
- **Weight**: Excluded from dimensions card (already shown in hero section)

### Required CSS for Dimensions Grid
```css
.dimensions-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);  /* 3 columns for desktop */
    gap: var(--space-micro-2);
    margin-bottom: var(--space-micro-2);
}

/* Mobile responsive: 2 columns */
@media (max-width: 768px) {
    .dimensions-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
```

### Required CSS for Specs Image Title
```css
.specs-image {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: var(--space-component-1);
}

.specs-image-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 25px 0;
    text-align: center;
    font-family: 'Bai Jamjuree', sans-serif;
}
```

## JSON Data Integration

### Data Extraction Map

#### From `generated_bearings_complete.json`:

**Basic Information**:
```json
{
  "model_number": "608",
  "bearing_type": "Deep Groove Ball Bearing",
  "enhanced_description": "[Use as hero subtitle]"
}
```

**Dimensions**:
```json
{
  "dimensions": {
    "bore_diameter_d_mm": 8,
    "outer_diameter_D_mm": 22,
    "width_B_mm": 7
  },
  "weight_kg": 0.015
}
```

**Load Ratings**:
```json
{
  "load_ratings": {
    "dynamic_load_Cr_kN": 3.32,
    "static_load_Cor_kN": 1.38
  }
}
```

**Speed Limits**:
```json
{
  "speed_limits": {
    "grease_rpm": 26000,
    "oil_rpm": 34000
  }
}
```

**Material Composition**:
```json
{
  "material": {
    "grade": "Gcr15",
    "composition": "Carbon: 0.95-1.05%, Chromium: 1.40-1.65%, Silicon: 0.15-0.35%"
  }
}
```

**Technical Drawing**:
```json
{
  "technical_drawing": {
    "image_url": "[SVG URL]",
    "image_alt": "[Alt text]",
    "image_title": "[Title]"
  }
}
```

**Vibration Data**:
```json
{
  "vibration": {
    "V2": {"low_frequency": 72, "medium_frequency": 48, "high_frequency": 40},
    "V3": {"low_frequency": 44, "medium_frequency": 28, "high_frequency": 24},
    "V4": {"low_frequency": 38, "medium_frequency": 12, "high_frequency": 12}
  }
}
```

**Noise Data**:
```json
{
  "noise": {
    "Z2": 35,
    "Z3": 31,
    "Z4": 27
  }
}
```

**Clearance Data**:
```json
{
  "clearance": {
    "C2": {"min_microns": 0, "max_microns": 7},
    "C0": {"min_microns": 2, "max_microns": 13},
    "C3": {"min_microns": 8, "max_microns": 23},
    "C4": {"min_microns": 14, "max_microns": 29},
    "C5": {"min_microns": 20, "max_microns": 37}
  }
}
```

**Seal Options**:
```json
{
  "seal_options": {
    "open": {"designation": "608", "description": "..."},
    "double_shielded": {"designation": "608-ZZ", "description": "..."},
    "double_sealed": {"designation": "608-2RS", "description": "..."}
  }
}
```

**Applications** (❌ DO NOT USE - Generate dynamically instead):
```json
{
  "applications": {
    "industrial": ["automobiles", "motorcycles", "motors", ...],
    "household": ["refrigerators", "air conditioners", ...]
  }
}
```

**Cross References**:
```json
{
  "cross_references": {
    "related_models": ["604", "605", "606", "607", "609"],
    "series_alternatives": ["6000 Series", "6300 Series"],
    "application_specific": [...]
  }
}
```

### Critical Data Processing Steps

#### 1. Material Composition Parsing
**JSON Format**: `"composition": "Carbon: 0.95-1.05%, Chromium: 1.40-1.65%, Silicon: 0.15-0.35%"`
**Parse into separate values**:
- Carbon Content: 0.95-1.05%
- Chromium Content: 1.40-1.65% 
- Silicon Content: 0.15-0.35%

#### 2. Vibration Data Formatting
**Convert frequency data to display format**:
```
V2: < 72/48/40 μm/s (Low/Med/High Hz)
V3: < 44/28/24 μm/s (Low/Med/High Hz)  
V4: < 38/12/12 μm/s (Low/Med/High Hz)
```

#### 3. Noise Data Formatting
**Add "<" prefix to all noise values**:
```
Z2: < 35 dB
Z3: < 31 dB
Z4: < 27 dB
```

#### 4. Clearance Data Handling
**Check for null values** and display accordingly:
- If C4/C5 are null: Don't display them
- If present: Show range as "14-29 μm"

#### 5. Applications Processing
**Convert arrays to structured cards**:
- Split industrial vs household
- Create application requirement mappings
- Generate appropriate icons and descriptions

**SEO Metadata**:
```json
{
  "seo_metadata": {
    "title": "[Page title]",
    "meta_description": "[Description]",
    "keywords": ["keyword1", "keyword2", ...],
    "canonical_url": "[URL]",
    "og_data": {...},
    "twitter_data": {...},
    "schema_markup": {...}
  }
}
```

## Dynamic Content Generation

### 1. Dynamic Applications Generation (CRITICAL)

#### Why Generate Applications Dynamically
The JSON applications data is **identical across all models**, making it unsuitable for model-specific pages. Each bearing model has unique characteristics that determine optimal applications:

- **Size constraints** (607: 7x19x6mm vs 608: 8x22x7mm)
- **Load capacity** (607: 2.86kN vs 608: 3.32kN)
- **Speed capabilities** (607: 28,000 RPM vs 608: 26,000 RPM)
- **Market positioning** and typical use cases

#### Application Generation Strategy
Create **3 distinct application categories** based on model characteristics:

**Category 1: Primary Strength Applications**
- Focus on the model's key advantages
- Match applications to load/speed/size profile
- Example for 607: Precision instruments, medical devices

**Category 2: Secondary Market Applications**
- Broader applications where model performs well
- More general industrial/commercial uses
- Example for 607: Compact motors, electronics

**Category 3: Specialty/Niche Applications**
- Unique applications leveraging specific characteristics
- Consumer/hobby applications
- Example for 607: Watch mechanisms, gaming devices

#### Model-Specific Application Examples

**607 Bearing (7x19x6mm, 2.86kN)** - Compact Precision Focus:
- **Precision Instruments & Medical**: Measurement tools, lab equipment, medical devices
- **Compact Motors & Electronics**: Servo motors, cooling fans, actuators
- **Specialty & Consumer**: Watch mechanisms, timing devices, hobby applications

**608 Bearing (8x22x7mm, 3.32kN)** - Versatile Performance:
- **Industrial & Precision**: Small motors, precision instruments, computer equipment
- **Automotive & Transportation**: Cooling systems, motorcycles, HVAC
- **Home Appliances**: Washing machines, refrigerators, air conditioners

#### Implementation Guidelines
1. **Research actual applications** for each bearing size
2. **Consider load/speed requirements** for each application
3. **Create custom SVG icons** representing each category
4. **Write specific requirements** for each category
5. **Avoid generic lists** - make each model unique

### 1.1. Seal Options System (ENHANCED TWO-TIER DESIGN)

#### Purpose
Provide optimal user experience with different interaction methods for popular vs specialty seal options. **Popular seals** (ZZ, 2RS) use engaging flip cards similar to specifications, while **specialty seals** (Open, -Z, -RS) use clean modal popups for detailed guidance.

#### Two-Tier Implementation Structure

**First Row (Popular Seals) - Flip Cards:**
```html
<div class="seal-options-popular">
    <div class="seal-card featured flip-card">
        <div class="flip-card-inner">
            <!-- Front Side (Technical Specs) -->
            <div class="flip-card-front">
                <div class="seal-header">
                    <h3>[MODEL]-ZZ</h3>
                    <div class="seal-badge popular">Most Popular</div>
                </div>
                <p class="seal-description">Double metal shields</p>
                <div class="seal-specs">
                    <!-- Speed, protection, lubrication specs -->
                </div>
                <div class="flip-hint"></div>
            </div>
            <!-- Back Side (Usage Guide) -->
            <div class="flip-card-back">
                <h4>When to Use [MODEL]-ZZ</h4>
                <div class="explanation-content">
                    <!-- Detailed usage guidance -->
                </div>
            </div>
        </div>
    </div>
</div>
```

**Second Row (Other Seals) - Modal Popups:**
```html
<div class="seal-options-others">
    <div class="seal-card" data-seal-type="[MODEL]-[SEAL]">
        <!-- Existing seal content -->
        <button class="seal-info-btn" onclick="openSealModal('[MODEL]-[SEAL]')">
            ℹ️ Usage Guide
        </button>
    </div>
</div>
```

#### Modal HTML Structure
Add before closing `</body>` tag:
```html
<!-- Seal Usage Modal -->
<div id="seal-modal" class="seal-modal">
    <div class="seal-modal-dialog">
        <div class="seal-modal-header">
            <button class="seal-modal-close" onclick="closeSealModal()">&times;</button>
        </div>
        <div id="seal-modal-content" class="seal-modal-body">
            <!-- Dynamic content will be inserted here -->
        </div>
    </div>
</div>
```

#### Seal-Specific Content Guidelines

**Open Bearing (No Seals)**:
- **Best For**: High-speed applications, controlled clean environments
- **Conditions**: Clean rooms, precision machinery, specialized equipment
- **Achieves**: Maximum speed potential and custom lubrication optimization
- **Requires**: External protection system and regular maintenance

**Single Shield (-Z)**:
- **Best For**: Semi-clean environments needing re-lubrication access
- **Conditions**: Equipment requiring periodic maintenance, moderate dust
- **Achieves**: Balance between protection and serviceability
- **Note**: One side accessible for lubrication, one side protected

**Double Shield (-ZZ)**:
- **Best For**: Clean to moderate dust environments
- **Conditions**: Electronics, precision instruments, general machinery
- **Achieves**: Maintenance-free operation with good speed performance
- **Avoid When**: High moisture, chemical exposure, washdown environments

**Single Seal (-RS)**:
- **Best For**: Moderate contamination with maintenance access needs
- **Conditions**: Light moisture exposure, serviceable locations
- **Achieves**: Good protection while maintaining lubrication access
- **Ideal**: When you need protection but want maintenance flexibility

**Double Seal (-2RS)**:
- **Best For**: Harsh environments with dust, moisture, contamination
- **Conditions**: Outdoor applications, food processing, washdown areas
- **Achieves**: Maximum protection and completely maintenance-free operation
- **Trade-off**: Lower speed capability due to seal friction

#### CSS Implementation
```css
.seal-hover-card {
    position: relative;
    overflow: visible;
}

.seal-explanation {
    position: absolute;
    top: 100%;
    background: var(--accent-neon);
    color: #000000;
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all var(--transition-smooth);
    z-index: 10;
}

.seal-hover-card:hover .seal-explanation {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}
```

#### JavaScript for Mobile Support
```javascript
// Mobile seal card touch support
document.addEventListener('DOMContentLoaded', function() {
    const sealCards = document.querySelectorAll('.seal-hover-card');
    
    sealCards.forEach(card => {
        card.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                // Close other explanations, toggle this one
                sealCards.forEach(otherCard => {
                    if (otherCard !== this) {
                        otherCard.classList.remove('active');
                    }
                });
                this.classList.toggle('active');
            }
        });
    });
});
```

#### Responsive Behavior
- **Desktop**: Hover to show explanations with smooth animation
- **Mobile**: Tap to toggle explanations with accordion-style expansion
- **Hint text**: "Hover for usage guide" (desktop) / "Tap for details" (mobile)

### 2. Hero Section Dynamic Content

#### Hero Description Generation
**Source**: `enhanced_description` from JSON + model-specific enhancements
**Example for 608**:
```html
<p class="hero-description">
    Meet the 608: With 3.32kN of engineering excellence and 8mm precision, 
    this bearing delivers the perfect blend of personality and performance 
    for your critical applications. The most widely used bearing in electronics, 
    small motors, and precision instruments.
</p>
```

#### Hero Stats Calculations
```html
<div class="hero-specs">
    <div class="spec-item">
        <div class="spec-value">[bore_diameter]mm</div>
        <div class="spec-label">Bore Diameter</div>
    </div>
    <div class="spec-item">
        <div class="spec-value">[outer_diameter]mm</div>
        <div class="spec-label">Outer Diameter</div>
    </div>
    <div class="spec-item">
        <div class="spec-value">[dynamic_load_Cr]kN</div>
        <div class="spec-label">Load Capacity</div>
    </div>
    <div class="spec-item">
        <div class="spec-value">[grease_rpm/1000]K RPM</div>
        <div class="spec-label">Max Speed</div>
    </div>
</div>
```

#### Breadcrumb Generation
```html
<div class="breadcrumb">
    <a href="https://rhdbearings.com/">Home</a> > 
    <a href="https://rhdbearings.com/specs/miniature-series.html">Miniature Bearings</a> > 
    <span>[MODEL] Bearing</span>
</div>
```

### 2. Flip Card Explanations (CRITICAL)

**Must generate all 6 explanations dynamically**:

#### Explanation Philosophy
Flip card explanations must be **practical and informative** rather than vague analogies. Users need to understand:
- **Specific numbers and calculations** relevant to their applications
- **Consequences of exceeding limits** and failure modes
- **How to measure/calculate their specific requirements**
- **Safety factors and best practices** for optimal bearing life
- **Technical reasons** behind the specifications (physics, materials, etc.)

**Avoid vague comparisons** like "equivalent to 3 people standing on it" or "faster than most power tools". Instead, provide **actionable engineering guidance** with specific numbers, failure modes, and practical calculations.

#### Load Ratings Card Explanations
```html
<div class="explanation-item">
    <strong>Dynamic Load ([Cr]kN = [calc: kN*102]kg):</strong> Maximum force while rotating. Exceeding this causes rapid wear and failure within hours.
</div>
<div class="explanation-item">
    <strong>Static Load ([Cor]kN = [calc: kN*102]kg):</strong> Maximum force when stationary. Use 80% for safety ([calc: kN*102*0.8]kg max recommended).
</div>
<div class="explanation-item">
    <strong>Calculate Your Load:</strong> Measure shaft forces, belt tensions, or gear loads. Include shock/vibration factors.
</div>
<div class="explanation-item">
    <strong>Failure Warning:</strong> Overloading causes bearing raceways to crack and balls to flatten permanently.
</div>
```

**Key Guidelines for Load Rating Explanations:**
- **Include actual numbers**: Always convert kN to kg (multiply by 102)
- **Explain consequences**: What happens when limits are exceeded
- **Provide safety factors**: 80% of static load for safety margin
- **Give practical guidance**: How to calculate their specific loads
- **Mention failure modes**: Specific damage that occurs from overloading

#### Speed Limits Card Explanations
```html
<div class="explanation-item">
    <strong>Grease Limit ([grease_rpm] RPM):</strong> Heat generation increases exponentially above this. Grease breaks down, causing seizure.
</div>
<div class="explanation-item">
    <strong>Oil Advantage ([oil_rpm] RPM):</strong> Better heat dissipation allows [calc: oil_rpm/grease_rpm*100-100]% higher speed. Required for high-speed spindles.
</div>
<div class="explanation-item">
    <strong>Safe Operating Speed:</strong> Use 90% of limit ([calc: grease_rpm*0.9] RPM) for maximum L10 life of 10,000+ hours.
</div>
<div class="explanation-item">
    <strong>Failure Mode:</strong> Exceeding speed causes cage failure, ball skidding, and catastrophic overheating within minutes.
</div>
```

**Key Guidelines for Speed Limit Explanations:**
- **Explain the physics**: Why limits exist (heat generation, lubrication breakdown)
- **Differentiate lubrication types**: Why oil allows higher speeds than grease
- **Quantify safety margins**: 90% of max for optimal bearing life
- **Mention L10 life**: Industry standard bearing life rating (10,000+ hours)
- **Describe failure modes**: Specific damage that occurs at excessive speeds
- **Time urgency**: Failure happens within minutes, not hours

#### Material & Quality Card Explanations
```html
<div class="explanation-item">
    <strong>Gcr15 Steel:</strong> Premium bearing steel - harder than tool steel
</div>
<div class="explanation-item">
    <strong>High Carbon:</strong> Superior hardness and wear resistance
</div>
<div class="explanation-item">
    <strong>Chromium:</strong> Adds corrosion resistance and toughness
</div>
<div class="explanation-item">
    <strong>Silicon:</strong> Improves strength and deoxidizes the steel
</div>
<div class="explanation-item">
    <strong>ISO Standard:</strong> Fits any [MODEL] application worldwide
</div>
```

#### Vibration Classes Card Explanations
```html
<div class="explanation-item">
    <strong>V2 Grade:</strong> Standard grade - good for general applications
</div>
<div class="explanation-item">
    <strong>V3 Grade:</strong> Low vibration - like a smooth car engine
</div>
<div class="explanation-item">
    <strong>V4 Grade:</strong> Ultra-smooth - for precision instruments
</div>
<div class="explanation-item">
    <strong>Frequency Bands:</strong> Measured across different rotation speeds
</div>
```

#### Noise Levels Card Explanations
```html
<div class="explanation-item">
    <strong>Z2 Grade:</strong> Quiet as a library - good for most applications
</div>
<div class="explanation-item">
    <strong>Z3 Grade:</strong> Very quiet - like a whisper (40 dB = normal whisper)
</div>
<div class="explanation-item">
    <strong>Z4 Grade:</strong> Ultra-quiet - perfect for [model-specific quiet applications]
</div>
<div class="explanation-item">
    <strong>Application:</strong> Ideal for sensitive environments
</div>
```

#### Internal Clearance Card Explanations
```html
<div class="explanation-item">
    <strong>C2 (Tight):</strong> Precision applications - less play, more accurate
</div>
<div class="explanation-item">
    <strong>C0 (Normal):</strong> Standard choice - works for most applications
</div>
<div class="explanation-item">
    <strong>C3 (Loose):</strong> Better for hot environments - allows thermal expansion
</div>
<div class="explanation-item">
    <strong>C4/C5:</strong> For temperatures above 100°C and 150°C respectively
</div>
```

### 3. Dynamic Calculations Required

#### Load Capacity Conversions
- **kN to kg**: `kN × 102 = kg` (e.g., 3.32kN = 338kg)
- **Real-world examples**: Based on model size and typical applications

#### Speed Conversions
- **RPM to rotations/second**: `RPM ÷ 60`
- **Comparison examples**: Power tools, motors, fans, etc.

#### Recommended Operating Speed
- **90% of max speed**: `grease_rpm × 0.9`

### 4. Dynamic FAQ Generation

### Process Overview
1. **Extract bearing specifications** from JSON
2. **Use FAQ generation guide** (`docs/faq_generation_guide.md`) as framework
3. **Generate model-specific FAQs** using AI/LLM
4. **Ensure 4 questions per category** (16 total)
5. **Follow structured format** for each FAQ

### FAQ Structure Template
```markdown
## Question: [Model-specific practical question]

### Direct Answer (20-30 words)
Quick solution specific to this bearing model

### Why This Matters (60-100 words)
- Model-specific technical reasoning
- Real-world consequences for this bearing size/application
- Practical implications

### How To Handle It (50-80 words)
- Step-by-step guidance for this model
- Specific load/speed/temperature limits
- When to seek professional help

### Pro Tip (15-25 words)
Model-specific insider knowledge
```

### Categories & Focus Areas

#### 1. Selection & Replacement
- Focus on **608-specific applications** (skateboards, motors, fans)
- **Interchange compatibility** with other models
- **Load capacity considerations** (3.32kN specific guidance)
- **Speed requirements** (26,000 RPM considerations)

#### 2. Installation & Maintenance
- **8mm bore-specific** installation challenges
- **Lubrication requirements** for this size
- **Common failure modes** in 608 applications
- **Maintenance intervals** based on typical usage

#### 3. Troubleshooting
- **Noise issues** specific to small bearings
- **Overheating causes** in high-speed applications
- **Wear patterns** common to 608 bearings
- **Diagnostic techniques** for this size

#### 4. Cost & Performance Optimization
- **Premium vs standard** 608 bearings
- **Lifecycle cost analysis** for common applications
- **Performance upgrades** (sealed vs open)
- **Bulk purchasing considerations**

## Reusable Components

### 1. Navbar Component
- **Files**: `webpages/shared/navbar.html`, `webpages/shared/navbar.css`
- **Implementation**: Direct HTML inclusion via JavaScript
- **Usage**: Load dynamically in all pages

### 2. Footer Component
- **Files**: `webpages/shared/footer.html`, `webpages/shared/footer.css`
- **Implementation**: Direct HTML embedding (not JavaScript due to CORS)
- **Styling**: Light background, modern contained design

### 3. CTA Component (Model-Specific)
- **Files**: `webpages/shared/cta-model.html`, `webpages/shared/cta-model.css`, `webpages/shared/cta-model.js`
- **Implementation**: Template with `[MODEL]` placeholders
- **Usage**: `loadModelCTA('608', 'cta-container')`
- **Features**: Dynamic model number replacement

### 4. Watermark Component
- **Files**: `webpages/shared/watermark.html`, `webpages/shared/watermark.css`
- **Implementation**: Direct HTML embedding
- **Design**: Dark to light grey gradient, bottom-positioned

### Component Integration Rules
1. **Direct HTML embedding** for static components (footer, watermark)
2. **JavaScript templates** for dynamic components (CTA)
3. **Consistent file paths** relative to model page location
4. **CORS-safe implementation** (avoid fetch() for local files)

### Critical File Paths for Model Pages
```
For model in: webpages/internalwebpages/specs/miniature-series/[MODEL]/

CSS Links:
- ../../../../shared/navbar.css
- ../../../../shared/footer.css  
- ../../../../shared/cta-model.css
- ../../../../shared/watermark.css
- styles.css (local)

JavaScript:
- ../../../../shared/cta-model.js

Fetch URLs:
- ../../../../shared/navbar.html
```

## UI/UX Standards

### Design Principles
1. **608 page as reference**: All model pages must match 608 exactly
2. **Consistent spacing**: Use CSS variables for section gaps
3. **Responsive design**: Mobile-first approach
4. **Accessibility**: Proper contrast ratios and keyboard navigation

### Color Scheme
- **Primary**: Black text (`#000000`)
- **Secondary**: Grey text (`#666666`, `#6B7280`)
- **Accent**: Neon green (`var(--accent-neon)`)
- **Backgrounds**: White (`#ffffff`), light grey (`#f8fafc`)
- **Flip card backs**: Neon green background with black text

### Typography
- **Font**: Bai Jamjuree (as per user preference)
- **Headings**: Bold, hierarchical sizing
- **Body text**: Clear, readable line heights
- **Technical specs**: Monospace for numerical values

### Spacing System
```css
:root {
  --space-section-1: 32px;  /* Reduced from 48px */
  --space-section-2: 48px;  /* Reduced from 64px */
}
```

### Interactive Elements
- **Specs flip cards**: 520px height (desktop), 450px (mobile) - increased to eliminate scrollers
- **Seal flip cards**: 360px height (desktop), 320px (mobile) - shorter for simpler content
- **Hover states**: Smooth transitions (0.3s)
- **Touch targets**: Minimum 44px for mobile
- **Focus indicators**: Visible keyboard navigation

### Responsive Breakpoints
- **Mobile**: ≤ 768px
- **Tablet**: 769px - 1024px
- **Desktop**: ≥ 1025px

## Technical Implementation

### File Structure
```
webpages/internalwebpages/specs/miniature-series/[MODEL]/
├── index.html
└── styles.css
```

### HTML Template Structure
```html
<!DOCTYPE html>
<html lang="en" data-model="[MODEL]">
<head>
    <!-- SEO metadata from JSON -->
    <title>[seo_metadata.title]</title>
    <meta name="description" content="[seo_metadata.meta_description]">
    <meta name="keywords" content="[seo_metadata.keywords.join(', ')]">
    <link rel="canonical" href="[seo_metadata.canonical_url]">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="[seo_metadata.og_data.title]">
    <meta property="og:description" content="[seo_metadata.og_data.description]">
    <!-- ... other OG tags -->
    
    <!-- Twitter Meta Tags -->
    <!-- ... twitter tags -->
    
    <!-- Structured Data (Schema.org JSON-LD) -->
    <script type="application/ld+json">[seo_metadata.schema_markup]</script>
    
    <!-- External fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- CSS files (EXACT PATHS) -->
    <link rel="stylesheet" href="../../../../shared/navbar.css">
    <link rel="stylesheet" href="../../../../shared/footer.css">
    <link rel="stylesheet" href="../../../../shared/cta-model.css">
    <link rel="stylesheet" href="../../../../shared/watermark.css">
    <link rel="stylesheet" href="styles.css">
</head>
<body data-page="miniature" data-model="[MODEL]">
    <!-- 1. Navigation Header -->
    <div id="navbar-container"></div>

    <!-- 2. Hero Section -->
    <section class="hero"><!-- Hero content --></section>

    <!-- 3. Specifications Section -->
    <section class="section" id="specifications"><!-- Specs + flip cards --></section>

    <!-- 4. Seal Options -->
    <section class="section bg-light"><!-- Seal types with popular badges --></section>

    <!-- 5. Applications -->
    <section class="section" id="applications"><!-- Application cards --></section>

    <!-- 6. FAQs -->
    <section class="section bg-light"><!-- FAQ accordion --></section>

    <!-- 7. Cross References & Alternatives -->
    <section class="section bg-light"><!-- Related models --></section>

    <!-- 8. Expertise Signals -->
    <section class="section"><!-- Professional insights --></section>

    <!-- 9. CTA Container (Dynamic) -->
    <div id="cta-container"></div>

    <!-- 10. Footer (Direct HTML embedding) -->
    <footer class="footer">[embed footer.html directly]</footer>

    <!-- 11. Watermark Section (Direct HTML embedding) -->
    <section class="watermark-section">[embed watermark.html directly]</section>

    <!-- Scripts -->
    <script src="../../../../shared/cta-model.js"></script>
    <script>
        <!-- All JavaScript implementation -->
    </script>
</body>
</html>
```

### CSS Architecture
```css
/* Base styles */
/* Layout components */
/* Flip card system */
/* Responsive adjustments */
/* Component overrides */
```

### JavaScript Features
```javascript
// Navbar loading
fetch('../../../../shared/navbar.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('navbar-container').innerHTML = data;
    });

// Mobile flip card support
document.addEventListener('DOMContentLoaded', function() {
    const flipCards = document.querySelectorAll('.flip-card');
    flipCards.forEach(card => {
        card.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                this.classList.toggle('flipped');
            }
        });
    });
});

// FAQ toggle functionality
function toggleFaqCategory(header) {
    const category = header.parentElement;
    const isActive = category.classList.contains('active');
    
    // Close all categories
    document.querySelectorAll('.faq-category').forEach(cat => {
        cat.classList.remove('active');
    });
    
    // Open clicked category if it wasn't active
    if (!isActive) {
        category.classList.add('active');
    }
}

// CTA dynamic loading
document.addEventListener('DOMContentLoaded', function() {
    loadModelCTA('[MODEL]', 'cta-container');
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
```

### Required HTML Structure Elements
```html
<!-- Essential containers -->
<div id="navbar-container"></div>
<div id="cta-container"></div>

<!-- Essential data attributes -->
<html lang="en" data-model="[MODEL]">
<body data-page="miniature" data-model="[MODEL]">

<!-- FAQ category structure -->
<div class="faq-category">
    <div class="faq-category-header" onclick="toggleFaqCategory(this)">
        <span>[Category Icon] [Category Name]</span>
        <span class="faq-chevron">▼</span>
    </div>
    <div class="faq-questions">
        <!-- FAQ content -->
    </div>
</div>
```

### Flip Card Implementation
```css
.flip-card {
    perspective: 1000px;
    min-height: 420px;
}

.flip-card-inner {
    transform-style: preserve-3d;
    transition: transform 0.6s;
}

.flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
}

/* Mobile touch support */
@media (max-width: 768px) {
    .flip-card.flipped .flip-card-inner {
        transform: rotateY(180deg);
    }
}
```

## Deployment Process

### 1. Local Development
- **Directory**: Create in `webpages/internalwebpages/specs/miniature-series/[MODEL]/`
- **Files**: Generate `index.html` and `styles.css`
- **Testing**: Verify all components load correctly

### 2. Production Deployment
- **Script**: `deployment/create_separate_page.py --page [MODEL]`
- **Output**: Standalone HTML files in `deployment/specs/miniature-series/[MODEL]/`
- **Upload**: `deployment/curl_upload.py --page [MODEL]`

### 3. URL Structure
- **Live URL**: `https://rhdbearings.com/specs/miniature-series/[MODEL]`
- **Clean URLs**: No `.html` extension required
- **SEO-friendly**: Hierarchical structure

### 4. Deployment Scripts Configuration

#### create_separate_page.py
```python
def is_model_page(page_type):
    return page_type in ['608', '604', '605', ...]  # Add new models here

def get_model_info(page_type):
    return {
        'page_dir': f'internalwebpages/specs/miniature-series/{page_type}',
        'output_dir': f'specs/miniature-series/{page_type}',
        'page_title': f'{page_type} Bearing Specifications',
        'clean_url': f'/specs/miniature-series/{page_type}'
    }
```

#### curl_upload.py
```python
def get_model_upload_info(page_type):
    return {
        'local_file': f'./specs/miniature-series/{page_type}/index.html',
        'remote_file': f'specs/miniature-series/{page_type}/index.html',
        'clean_url': f'https://rhdbearings.com/specs/miniature-series/{page_type}'
    }
```

## Critical Implementation Requirements

### Exact CSS Structure (Copy from 608)
**Must copy these exact CSS sections from 608 styles.css**:
1. **Flip card system** (lines 1237-1366)
2. **Specifications section** (dimensions table + image layout)
3. **Applications section** (compressed cards with sticky requirements) 
4. **FAQ accordion styling**
5. **Cross-reference cards styling**
6. **Expertise signals styling**

### Essential CSS Variables
```css
:root {
  --space-section-1: 32px;  /* Reduced spacing */
  --space-section-2: 48px;  /* Reduced spacing */
  --accent-neon: #34d399;   /* Brand neon green */
}
```

### Required Font Import
```html
<link href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Flip Card CSS (CRITICAL - Must be exact)
```css
.flip-card {
    background-color: transparent;
    perspective: 1000px;
    position: relative;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: left;
    transition: transform 0.6s;
    transform-style: preserve-3d;
    min-height: 520px;
}

.flip-card:hover .flip-card-inner {
    transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    -webkit-backface-visibility: hidden;
    backface-visibility: hidden;
    border-radius: 12px;
    padding: 28px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
}

.flip-card-front {
    background: #ffffff;
    color: var(--text-primary);
    border: 1px solid rgba(0, 0, 0, 0.08);
}

.flip-card-back {
    background: var(--accent-neon);
    color: #000000;
    transform: rotateY(180deg);
    border: 1px solid rgba(52, 211, 153, 0.3);
}

/* Mobile support */
@media (max-width: 768px) {
    .flip-card:hover .flip-card-inner {
        transform: none;
    }
    
    .flip-card.flipped .flip-card-inner {
        transform: rotateY(180deg);
    }
    
    .flip-card-inner {
        min-height: 450px;
    }
    
    .seal-card.flip-card .flip-card-inner {
        min-height: 280px;
    }
}
```

### Seal Card Height CSS (CRITICAL - Different from Specs Cards)
```css
/* Seal-specific flip cards (shorter than specs cards) */
.seal-card.flip-card .flip-card-inner {
    min-height: 360px;
}

@media (max-width: 768px) {
    .seal-card.flip-card .flip-card-inner {
        min-height: 320px;
    }
}
```

## Quality Checklist

### Pre-Deployment Checklist
- [ ] **Data accuracy**: All JSON data correctly extracted and displayed
- [ ] **FAQ generation**: 16 model-specific FAQs generated using guide
- [ ] **Flip cards**: All 6 cards flip correctly with proper content
- [ ] **Responsive design**: Tests on mobile, tablet, desktop
- [ ] **Component loading**: Navbar, footer, CTA, watermark all load
- [ ] **SEO metadata**: Title, description, keywords, schema markup
- [ ] **Cross-references**: Links to related models work
- [ ] **Images**: Technical drawing loads correctly
- [ ] **Performance**: Page loads under 3 seconds
- [ ] **Accessibility**: Keyboard navigation and screen readers

### Content Quality Standards
- [ ] **Technical accuracy**: All specifications match JSON data
- [ ] **Plain English explanations**: Flip card backs are user-friendly
- [ ] **Complete material data**: Carbon, Chromium, Silicon percentages
- [ ] **Consistent formatting**: Numbers, units, and styling
- [ ] **Brand consistency**: Neon green accents throughout
- [ ] **Error-free text**: No typos or duplicated content

### UI/UX Validation
- [ ] **608 page consistency**: Visual comparison passes
- [ ] **Interactive elements**: Hover and touch states work
- [ ] **Loading states**: No broken images or missing content
- [ ] **Typography**: Bai Jamjuree font loads correctly
- [ ] **Spacing**: Sections have consistent gaps
- [ ] **Color scheme**: Matches brand guidelines

## Troubleshooting

### Common Issues & Solutions

#### 1. Component Loading Failures
**Problem**: Navbar, footer, or CTA not loading
**Solution**: 
- Check file paths relative to model directory
- Use direct HTML embedding for static components
- Verify JavaScript template strings for dynamic components

#### 2. Flip Card Content Overflow
**Problem**: Text exceeds card boundaries
**Solution**:
- **Specs cards**: Increase `min-height` to 520px (desktop) / 450px (mobile)
- **Seal cards**: Use shorter `min-height` 360px (desktop) / 320px (mobile)
- Content should fit without scrollers (overflow-y: visible)
- Optimize explanation text length for card type

#### 3. Duplicate Hover Text
**Problem**: "Hover for explanationHover for explanation"
**Solution**:
- Remove HTML text content from `.flip-hint` divs
- Let CSS `::before` pseudo-elements handle the text

#### 4. Mobile Flip Functionality
**Problem**: Cards don't flip on mobile devices
**Solution**:
- Implement JavaScript click handlers for mobile
- Use `.flipped` class toggle on touch devices
- Disable hover effects on mobile

#### 5. SEO Metadata Issues
**Problem**: Missing or incorrect meta tags
**Solution**:
- Extract complete `seo_metadata` object from JSON
- Include all required fields: title, description, keywords
- Add Open Graph and Twitter Card data
- Implement Schema.org JSON-LD markup

#### 6. Performance Issues
**Problem**: Slow page loading
**Solution**:
- Optimize image sizes (use SVG for technical drawings)
- Minimize CSS and JavaScript
- Use efficient CSS selectors
- Implement proper caching headers

### Debugging Tools
1. **Browser DevTools**: Check console for JavaScript errors
2. **Responsive Design Mode**: Test various screen sizes
3. **Network Tab**: Monitor resource loading times
4. **Lighthouse**: Performance and accessibility audits
5. **HTML Validator**: Ensure markup validity

## Advanced Considerations

### Future Enhancements
1. **Lazy loading**: Implement for images and non-critical content
2. **Progressive Web App**: Add service worker and manifest
3. **Schema markup**: Enhance with Product schema
4. **Internationalization**: Support multiple languages
5. **A/B testing**: Test different FAQ formats or layouts

### Maintenance Guidelines
1. **Regular updates**: Keep JSON data current
2. **Performance monitoring**: Track page load times
3. **User feedback**: Monitor FAQ engagement
4. **Component updates**: Maintain shared components
5. **SEO optimization**: Update keywords and meta descriptions

### Scalability Considerations
1. **Template system**: Consider templating engine for large-scale generation
2. **Data management**: Centralized JSON schema validation
3. **Build automation**: Automated deployment pipeline
4. **Content management**: CMS integration for non-technical updates
5. **Version control**: Track changes to component library

## Conclusion

This guide provides a comprehensive framework for generating consistent, high-quality model pages based on the 608 bearing page template. By following these guidelines, you can create professional, user-friendly, and SEO-optimized pages for any bearing model while maintaining design consistency and technical accuracy.

The key to success is treating the 608 page as the definitive template and ensuring every new model page matches its structure, styling, and functionality exactly while only changing the model-specific data and FAQs.
