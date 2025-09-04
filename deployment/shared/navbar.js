// Navbar JavaScript
// This file loads the navbar content dynamically

document.addEventListener('DOMContentLoaded', function() {
    const navbarContainer = document.getElementById('navbar-container');
    if (navbarContainer) {
        // Load navbar HTML content
        fetch('../shared/navbar.html')
            .then(response => response.text())
            .then(html => {
                navbarContainer.innerHTML = html;
            })
            .catch(error => {
                console.error('Error loading navbar:', error);
            });
    }
});
