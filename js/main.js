// Main JavaScript for Unblocked Games Website
// Optimized for performance and SEO

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Performance optimization: Debounce function
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

// Initialize Application
function initializeApp() {
    setupTheme();
    setupSearch();
    setupFavorites();
    setupSmoothScrolling();
    setupLazyLoading();
    setupGameCards();
}

// Theme Functionality
function setupTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    
    // Load saved theme or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    console.log('Toggling theme from', currentTheme, 'to', newTheme);
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const themeIcon = document.getElementById('themeIcon');
    if (!themeIcon) return;
    
    if (theme === 'dark') {
        // Moon icon for dark mode
        themeIcon.innerHTML = `
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        `;
    } else {
        // Sun icon for light mode
        themeIcon.innerHTML = `
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        `;
    }
}

// Enhanced Search Functionality
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const searchResults = document.getElementById('searchResults');
    
    if (searchInput && searchBtn) {
        // Real-time search with debouncing
        searchInput.addEventListener('input', debounce(performLiveSearch, 300));
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
        
        // Hide search results when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.search-container')) {
                hideSearchResults();
            }
        });
    }
}

function performLiveSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchTerm = searchInput.value.trim().toLowerCase();
    const searchResults = document.getElementById('searchResults');
    
    if (searchTerm.length < 2) {
        hideSearchResults();
        return;
    }
    
    // Game database for search
    const games = [
        { id: 'slope', title: 'Slope', icon: 'game_icons/slope.png', url: 'play/slope.html' },
        { id: 'vex-6', title: 'Vex 6', icon: 'game_icons/vex-6.png', url: 'play/vex-6.html' },
        { id: 'minecraft-1.8.8', title: 'Minecraft 1.8.8', icon: 'game_icons/minecraft-1.8.8.png', url: 'play/minecraft-1.8.8.html' },
        { id: 'tunnel-rush', title: 'Tunnel Rush', icon: 'game_icons/tunnel-rush.png', url: 'play/tunnel-rush.html' },
        { id: 'geometry-dash', title: 'Geometry Dash', icon: 'game_icons/geometry-dash.png', url: 'play/geometry-dash.html' },
        { id: 'among-us', title: 'Among Us', icon: 'game_icons/among-us.png', url: 'play/among-us.html' },
        { id: '2048', title: '2048', icon: 'game_icons/2048.png', url: 'play/2048.html' },
        { id: 'retro-bowl', title: 'Retro Bowl', icon: 'game_icons/retro-bowl.png', url: 'play/retro-bowl.html' },
        { id: 'subway-surfers', title: 'Subway Surfers', icon: 'game_icons/subway-surfers.png', url: 'play/subway-surfers.html' },
        { id: 'temple-run-2', title: 'Temple Run 2', icon: 'game_icons/temple-run-2.png', url: 'play/temple-run-2.html' },
        { id: 'flappy-bird', title: 'Flappy Bird', icon: 'game_icons/flappy-bird.png', url: 'play/flappy-bird.html' },
        { id: 'cookie-clicker', title: 'Cookie Clicker', icon: 'game_icons/cookie-clicker.png', url: 'play/cookie-clicker.html' },
        { id: 'fortnite', title: 'Fortnite', icon: 'game_icons/fortnite.png', url: 'play/fortnite.html' },
        { id: '1v1-lol', title: '1v1 LOL', icon: 'game_icons/1v1-lol.png', url: 'play/1v1-lol.html' },
        { id: 'basketball-legends', title: 'Basketball Legends', icon: 'game_icons/basketball-legends.png', url: 'play/basketball-legends.html' },
        { id: 'football-legends', title: 'Football Legends', icon: 'game_icons/football-legends.png', url: 'play/football-legends.html' },
        { id: 'smash-karts', title: 'Smash Karts', icon: 'game_icons/smash-karts.png', url: 'play/smash-karts.html' },
        { id: 'bitlife', title: 'BitLife', icon: 'game_icons/bitlife.png', url: 'play/bitlife.html' },
        { id: 'drift-boss', title: 'Drift Boss', icon: 'game_icons/drift-boss.png', url: 'play/drift-boss.html' },
        { id: 'crossy-road', title: 'Crossy Road', icon: 'game_icons/crossy-road.png', url: 'play/crossy-road.html' }
    ];
    
    // Filter games based on search term
    const filteredGames = games.filter(game => 
        game.title.toLowerCase().includes(searchTerm)
    );
    
    if (filteredGames.length === 0) {
        showSearchResults([{ title: 'No games found', isNoResults: true }]);
    } else {
        showSearchResults(filteredGames.slice(0, 8)); // Limit to 8 results
    }
}

function showSearchResults(games) {
    const searchResults = document.getElementById('searchResults');
    if (!searchResults) return;
    
    searchResults.innerHTML = '';
    
    if (games[0] && games[0].isNoResults) {
        searchResults.innerHTML = '<div class="search-no-results">No games found matching your search</div>';
    } else {
        games.forEach(game => {
            const resultItem = document.createElement('div');
            resultItem.className = 'search-result-item';
            resultItem.innerHTML = `
                <img src="${game.icon}" alt="${game.title}" class="search-result-icon" loading="lazy">
                <h4 class="search-result-title">${game.title}</h4>
            `;
            resultItem.addEventListener('click', () => {
                window.location.href = game.url;
            });
            searchResults.appendChild(resultItem);
        });
    }
    
    searchResults.classList.add('show');
}

function hideSearchResults() {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.classList.remove('show');
    }
}

function performSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchTerm = searchInput.value.trim().toLowerCase();
    
    if (searchTerm === '') {
        showNotification('Please enter a game name to search', 'warning');
        return;
    }
    
    // Hide search results
    hideSearchResults();
    
    // Simple search through game cards
    const gameCards = document.querySelectorAll('.game-card');
    let found = false;
    
    gameCards.forEach(card => {
        const gameTitle = card.querySelector('.game-card-title').textContent.toLowerCase();
        if (gameTitle.includes(searchTerm)) {
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            card.style.border = '3px solid var(--primary)';
            card.style.boxShadow = '0 0 20px rgba(220, 38, 38, 0.5)';
            
            // Remove highlight after 3 seconds
            setTimeout(() => {
                card.style.border = '';
                card.style.boxShadow = '';
            }, 3000);
            
            found = true;
        }
    });
    
    if (!found) {
        showNotification('No games found matching your search. Try a different term.', 'warning');
    }
}


// Favorites System
function setupFavorites() {
    // Load favorites from localStorage
    loadFavorites();
    
    // Update favorite buttons
    updateFavoriteButtons();
}

function toggleFavorite(gameId) {
    let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    
    if (favorites.includes(gameId)) {
        // Remove from favorites
        favorites = favorites.filter(id => id !== gameId);
        showNotification('Removed from favorites', 'warning');
    } else {
        // Add to favorites
        favorites.push(gameId);
        showNotification('Added to favorites', 'success');
    }
    
    localStorage.setItem('favorites', JSON.stringify(favorites));
    updateFavoriteButtons();
}

function loadFavorites() {
    return JSON.parse(localStorage.getItem('favorites') || '[]');
}

function updateFavoriteButtons() {
    const favorites = loadFavorites();
    const favoriteButtons = document.querySelectorAll('[onclick*="toggleFavorite"]');
    
    console.log('Current favorites:', favorites); // Debug log
    
    favoriteButtons.forEach(button => {
        const gameId = button.getAttribute('onclick').match(/'([^']+)'/)[1];
        console.log('Checking button for game:', gameId, 'is favorited:', favorites.includes(gameId)); // Debug log
        
        if (favorites.includes(gameId)) {
            button.classList.add('liked');
            // For game page buttons with SVG, add visual feedback
            if (button.querySelector('svg')) {
                button.style.color = 'var(--danger)';
                button.style.transform = 'scale(1.1)';
            } else {
                // For index page buttons with emoji
                button.innerHTML = '❤️';
                button.style.color = 'var(--danger)';
            }
        } else {
            button.classList.remove('liked');
            // For game page buttons with SVG, remove visual feedback
            if (button.querySelector('svg')) {
                button.style.color = 'var(--gray-400)';
                button.style.transform = 'scale(1)';
            } else {
                // For index page buttons with emoji
                button.innerHTML = '🤍';
                button.style.color = 'var(--gray-400)';
            }
        }
    });
}

// Smooth Scrolling
function setupSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Lazy Loading for Images
function setupLazyLoading() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.src || img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
}

// Game Cards Enhancement
function setupGameCards() {
    const gameCards = document.querySelectorAll('.game-card');
    
    gameCards.forEach(card => {
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Add click animation
        card.addEventListener('click', function(e) {
            if (!e.target.closest('.btn-custom')) {
                const playButton = this.querySelector('.btn-primary');
                if (playButton) {
                    playButton.click();
                }
            }
        });
    });
}

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'var(--success)' : type === 'warning' ? 'var(--warning)' : 'var(--primary)'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-lg);
        z-index: 9999;
        animation: slideInRight 0.3s ease;
        max-width: 300px;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, 3000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0;
        line-height: 1;
    }
    
    .notification-close:hover {
        opacity: 0.8;
    }
`;
document.head.appendChild(style);

// Game Frame Fullscreen Functionality
function toggleFullscreen(gameId) {
    const gameFrame = document.getElementById(`game-frame-${gameId}`);
    if (!gameFrame) return;
    
    if (!document.fullscreenElement) {
        gameFrame.requestFullscreen().catch(err => {
            console.log('Error attempting to enable fullscreen:', err);
        });
    } else {
        document.exitFullscreen();
    }
}

// Keyboard Shortcuts
document.addEventListener('keydown', function(e) {
    // Escape key to exit fullscreen
    if (e.key === 'Escape' && document.fullscreenElement) {
        document.exitFullscreen();
    }
    
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.focus();
        }
    }
});

// Performance Optimization
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Scroll to Top Function
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add scroll to top button
function addScrollToTopButton() {
    const scrollButton = document.createElement('button');
    scrollButton.innerHTML = '↑';
    scrollButton.className = 'scroll-to-top';
    scrollButton.onclick = scrollToTop;
    scrollButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--primary);
        color: white;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: var(--shadow-lg);
        z-index: 1000;
        opacity: 0;
        transition: all 0.3s ease;
    `;
    
    document.body.appendChild(scrollButton);
    
    // Show/hide based on scroll position
    window.addEventListener('scroll', debounce(() => {
        if (window.pageYOffset > 300) {
            scrollButton.style.opacity = '1';
        } else {
            scrollButton.style.opacity = '0';
        }
    }, 100));
}

// Initialize scroll to top button
addScrollToTopButton();

// Analytics (placeholder)
function trackEvent(eventName, eventData = {}) {
    // Placeholder for analytics tracking
    console.log('Event tracked:', eventName, eventData);
}

// Track page views
trackEvent('page_view', {
    page: window.location.pathname,
    title: document.title
});


// Export functions for global access
window.toggleFavorite = toggleFavorite;
window.toggleFullscreen = toggleFullscreen;
window.scrollToTop = scrollToTop;
window.toggleTheme = toggleTheme;
