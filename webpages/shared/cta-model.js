/**
 * CTA component template - embedded to avoid CORS issues with local files
 */
const CTA_TEMPLATE = `
<!-- Contact CTA -->
<section class="section cta-section">
    <div class="container">
        <div class="cta-content">
            <div class="cta-header">
                <div class="cta-badge">🔥 FAST DELIVERY</div>
                <h2>Need <span class="model-number">[MODEL]</span> Bearings Today?</h2>
                <p class="cta-subtitle">Get instant pricing and availability for premium <span class="model-number">[MODEL]</span> bearings. Same-day dispatch available for orders before 2 PM.</p>
            </div>
            
            <div class="cta-main">
                <div class="cta-features">
                    <div class="feature-item">
                        <div class="feature-icon">⚡</div>
                        <div class="feature-content">
                            <h4>Instant Quote</h4>
                            <p>Real-time pricing & availability</p>
                        </div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🚀</div>
                        <div class="feature-content">
                            <h4>Same Day Dispatch</h4>
                            <p>Orders before 2 PM ship today</p>
                        </div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🏆</div>
                        <div class="feature-content">
                            <h4>Premium Quality</h4>
                            <p>ISO certified, 20+ years expertise</p>
                        </div>
                    </div>
                </div>
                
                <div class="cta-actions">
                    <a href="tel:+91-9702081858" class="btn btn-primary">
                        <span class="btn-icon">📞</span>
                        <span class="btn-text">
                            <strong>Call Now</strong>
                            <small>+91-9702081858</small>
                        </span>
                    </a>
                    <a href="mailto:sales@rhdenterprise.in" class="btn btn-secondary">
                        <span class="btn-icon">📧</span>
                        <span class="btn-text">
                            <strong>Email Quote</strong>
                            <small>Instant Response</small>
                        </span>
                    </a>
                </div>
            </div>
            
            <div class="cta-footer">
                <div class="company-info">
                    <div class="company-brand">
                        <strong>RHD Bearings</strong>
                        <span class="company-tagline">Your Trusted Bearing Partner</span>
                    </div>
                    <div class="company-location">
                        📍 203 Vihar Estate, Sakinaka, Andheri East, Mumbai 400072
                    </div>
                </div>
                <div class="business-info">
                    <div class="business-item">
                        <span class="business-label">OEM Sales:</span>
                        <span class="business-value">oemsales@rhdenterprise.in</span>
                    </div>
                    <div class="business-item">
                        <span class="business-label">Bulk Orders:</span>
                        <span class="business-value">Significant discounts available</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
`;

/**
 * Load and initialize the model CTA component
 * @param {string} modelNumber - The bearing model number (e.g., "608", "6001", etc.)
 * @param {string} containerId - The ID of the container element where CTA will be loaded
 */
function loadModelCTA(modelNumber, containerId = 'cta-container') {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`CTA container with ID '${containerId}' not found`);
        return;
    }

    try {
        // Replace all instances of [MODEL] with the actual model number
        const processedHTML = CTA_TEMPLATE.replace(/\[MODEL\]/g, modelNumber);
        container.innerHTML = processedHTML;
        console.log(`CTA component loaded successfully for model: ${modelNumber}`);
    } catch (error) {
        console.error('Error loading CTA component:', error);
        // Fallback: show a simple CTA
        container.innerHTML = `
            <section class="section" style="background: #000; color: #fff; text-align: center; padding: 60px 0;">
                <div class="container">
                    <h2>Need ${modelNumber} Bearings Today?</h2>
                    <p>Contact us for instant pricing and availability</p>
                    <a href="tel:+91-9702081858" style="background: #D2FF37; color: #000; padding: 12px 24px; border-radius: 8px; text-decoration: none; display: inline-block; margin: 10px;">📞 Call +91-9702081858</a>
                </div>
            </section>
        `;
    }
}

/**
 * Initialize CTA when DOM is ready
 * This function should be called after the page loads
 */
function initializeCTA() {
    // Auto-detect model number from page data attribute or URL
    const modelNumber = detectModelNumber();
    if (modelNumber) {
        loadModelCTA(modelNumber);
    }
}

/**
 * Auto-detect model number from various sources
 * @returns {string|null} - The detected model number or null if not found
 */
function detectModelNumber() {
    // Try to get from body data attribute
    const bodyElement = document.body;
    if (bodyElement.dataset.model) {
        return bodyElement.dataset.model;
    }
    
    // Try to get from URL path
    const pathMatch = window.location.pathname.match(/\/([0-9]+[A-Z]*)\//);
    if (pathMatch) {
        return pathMatch[1];
    }
    
    // Try to get from page title
    const titleMatch = document.title.match(/([0-9]+[A-Z]*)/);
    if (titleMatch) {
        return titleMatch[1];
    }
    
    return null;
}
