// Footer JavaScript
// This file loads the footer content dynamically

document.addEventListener('DOMContentLoaded', function() {
    const footerContainer = document.getElementById('footer-container');
    if (footerContainer) {
        // Load footer HTML content
        fetch('../shared/footer.html')
            .then(response => response.text())
            .then(html => {
                footerContainer.innerHTML = html;
            })
            .catch(error => {
                console.error('Error loading footer:', error);
            });
    }
});
