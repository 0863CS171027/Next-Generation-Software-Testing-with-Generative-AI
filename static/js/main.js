/* Main JavaScript */

console.log('Next-Generation Software Testing with Generative AI - Application Loaded');

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// API Helper Functions
const API = {
    get: function(endpoint) {
        return fetch(endpoint, { method: 'GET' })
            .then(response => response.json());
    },
    
    post: function(endpoint, data) {
        return fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(response => response.json());
    },
    
    delete: function(endpoint) {
        return fetch(endpoint, { method: 'DELETE' })
            .then(response => response.json());
    }
};

// Utility Functions
const Utils = {
    formatDate: function(dateString) {
        return new Date(dateString).toLocaleDateString();
    },
    
    formatTime: function(dateString) {
        return new Date(dateString).toLocaleTimeString();
    },
    
    formatDateTime: function(dateString) {
        return new Date(dateString).toLocaleString();
    },
    
    showAlert: function(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.main-content');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
};

// Export functions
window.API = API;
window.Utils = Utils;
