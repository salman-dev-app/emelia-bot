// Main JavaScript for Emelia Bot Dashboard

document.addEventListener('DOMContentLoaded', function() {
    console.log('Emelia Bot Dashboard Loaded');
    
    // Initialize all features
    initDashboard();
    initForms();
    initTables();
    initNotifications();
});

// Dashboard Initialization
function initDashboard() {
    // Auto-refresh stats every 30 seconds
    setInterval(refreshStats, 30000);
    
    // Animate numbers on page load
    animateNumbers();
}

// Animate number counters
function animateNumbers() {
    const numbers = document.querySelectorAll('.number');
    
    numbers.forEach(num => {
        const target = parseInt(num.innerText);
        const duration = 1000;
        const step = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                num.innerText = target;
                clearInterval(timer);
            } else {
                num.innerText = Math.floor(current);
            }
        }, 16);
    });
}

// Refresh dashboard statistics
async function refreshStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        // Update stats on the page
        if (data.success) {
            updateDashboardStats(data.stats);
        }
    } catch (error) {
        console.error('Error refreshing stats:', error);
    }
}

// Update dashboard statistics
function updateDashboardStats(stats) {
    // Update total users
    const usersEl = document.querySelector('#total-users .number');
    if (usersEl) usersEl.innerText = stats.total_users || 0;
    
    // Update total messages
    const messagesEl = document.querySelector('#total-messages .number');
    if (messagesEl) messagesEl.innerText = stats.total_messages || 0;
    
    // Update active channels
    const channelsEl = document.querySelector('#active-channels .number');
    if (channelsEl) channelsEl.innerText = stats.active_channels || 0;
}

// Form handling
function initForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerText;
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerText = 'Processing...';
            
            try {
                const formData = new FormData(form);
                const response = await fetch(form.action, {
                    method: form.method,
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showNotification('Success!', 'success');
                    form.reset();
                } else {
                    showNotification(result.message || 'Error occurred', 'error');
                }
            } catch (error) {
                showNotification('Network error occurred', 'error');
                console.error('Form submission error:', error);
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = originalText;
            }
        });
    });
}

// Table features
function initTables() {
    // Add search functionality to tables
    const searchInputs = document.querySelectorAll('.table-search');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const tableId = this.dataset.table;
            const table = document.getElementById(tableId);
            const rows = table.querySelectorAll('tbody tr');
            const searchTerm = this.value.toLowerCase();
            
            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    });
    
    // Add sorting functionality
    const headers = document.querySelectorAll('th.sortable');
    
    headers.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            sortTable(this);
        });
    });
}

// Sort table by column
function sortTable(header) {
    const table = header.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(header.parentElement.children).indexOf(header);
    const isAscending = header.classList.contains('asc');
    
    rows.sort((a, b) => {
        const aValue = a.children[columnIndex].innerText;
        const bValue = b.children[columnIndex].innerText;
        
        if (isAscending) {
            return bValue.localeCompare(aValue);
        } else {
            return aValue.localeCompare(bValue);
        }
    });
    
    // Remove all sorting classes
    header.parentElement.querySelectorAll('th').forEach(th => {
        th.classList.remove('asc', 'desc');
    });
    
    // Add appropriate class
    header.classList.add(isAscending ? 'desc' : 'asc');
    
    // Re-append sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

// Notification system
function initNotifications() {
    // Create notification container if it doesn't exist
    if (!document.querySelector('.notifications-container')) {
        const container = document.createElement('div');
        container.className = 'notifications-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
        `;
        document.body.appendChild(container);
    }
}

// Show notification
function showNotification(message, type = 'info', duration = 3000) {
    const container = document.querySelector('.notifications-container');
    const notification = document.createElement('div');
    
    notification.className = `alert alert-${type}`;
    notification.style.cssText = `
        margin-bottom: 10px;
        min-width: 300px;
        animation: slideIn 0.3s ease;
    `;
    notification.innerText = message;
    
    container.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Utility functions
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Export functions for use in other scripts
window.EmeliaBot = {
    showNotification,
    refreshStats,
    formatNumber,
    formatDate
};
