#!/usr/bin/env python3
"""
Simple script to replace old fullscreen functionality with enhanced version
"""

import re
from pathlib import Path

PLAY_DIR = Path('play')

# The enhanced fullscreen script to inject before the fullscreenBtn listener
VIEWPORT_HEIGHT_SCRIPT = """        // Set CSS custom property for dynamic viewport height
        function setAppHeightLocal() {
            const doc = document.documentElement;
            doc.style.setProperty('--app-height', `${window.innerHeight}px`);
        }

        // Prevent touch scrolling when in fullscreen
        function preventTouchMoveLocal(e) {
            e.preventDefault();
        }

        // Update on resize and orientation change
        window.addEventListener('resize', setAppHeightLocal);
        window.addEventListener('orientationchange', setAppHeightLocal);
        setAppHeightLocal(); // Set initial value

"""

# The enhanced fullscreen event listener (lines 856-1041 from slope.html)
FULLSCREEN_LISTENER = """        // Enhanced fullscreen functionality with proper mobile support
        document.getElementById('fullscreenBtn').addEventListener('click', function() {
            const gameFrame = document.getElementById('gameFrame');
            const header = document.querySelector('.header-custom');
            const sidebar = document.getElementById('sidebar');
            const breadcrumb = document.querySelector('.breadcrumb-nav');
            const footer = document.querySelector('.footer-modern');
            const sparkleContainer = document.querySelector('.sparkle-container');
            
            // Check if already in fullscreen
            if (document.fullscreenElement || 
                document.webkitFullscreenElement || 
                document.mozFullScreenElement || 
                document.msFullscreenElement) {
                // Exit fullscreen
                exitFullscreen();
            } else {
                // Enter fullscreen
                enterFullscreen();
            }
            
            function enterFullscreen() {
                // Try native fullscreen API first
                if (gameFrame.requestFullscreen) {
                    gameFrame.requestFullscreen().catch(err => {
                        console.log('Native fullscreen failed:', err);
                        activateMobileFullscreen();
                    });
                } else if (gameFrame.webkitRequestFullscreen) {
                    gameFrame.webkitRequestFullscreen().catch(err => {
                        console.log('Webkit fullscreen failed:', err);
                        activateMobileFullscreen();
                    });
                } else if (gameFrame.mozRequestFullScreen) {
                    gameFrame.mozRequestFullScreen().catch(err => {
                        console.log('Moz fullscreen failed:', err);
                        activateMobileFullscreen();
                    });
                } else if (gameFrame.msRequestFullscreen) {
                    gameFrame.msRequestFullscreen().catch(err => {
                        console.log('MS fullscreen failed:', err);
                        activateMobileFullscreen();
                    });
                } else {
                    // No native fullscreen support, use mobile fallback
                    activateMobileFullscreen();
                }
            }
            
            function exitFullscreen() {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                } else {
                    // Exit mobile fullscreen mode
                    deactivateMobileFullscreen();
                }
            }
            
            function activateMobileFullscreen() {
                // Update app height immediately
                setAppHeightLocal();
                
                // Store the current scroll position
                const scrollY = window.scrollY;
                document.body.style.top = `-${scrollY}px`;
                
                // Set explicit height using window.innerHeight for more reliability
                gameFrame.style.height = `${window.innerHeight}px`;
                gameFrame.style.width = `${window.innerWidth}px`;
                
                // Add mobile fullscreen class to body
                document.body.classList.add('mobile-fullscreen-active');
                
                // Add mobile fullscreen class to game frame
                gameFrame.classList.add('mobile-fullscreen');
                
                // Hide UI elements (but NOT game container elements)
                if (header) header.style.display = 'none';
                if (sidebar) sidebar.style.display = 'none';
                if (breadcrumb) breadcrumb.style.display = 'none';
                if (footer) footer.style.display = 'none';
                if (sparkleContainer) sparkleContainer.style.display = 'none';
                
                // Hide game info bar specifically
                const gameInfoBar = document.querySelector('.game-info-bar');
                if (gameInfoBar) gameInfoBar.style.display = 'none';
                
                // Prevent scrolling on mobile
                document.body.style.overflow = 'hidden';
                document.documentElement.style.overflow = 'hidden';
                
                // Prevent touch scrolling
                document.addEventListener('touchmove', preventTouchMoveLocal, { passive: false });
                
                // Update height on orientation change while in fullscreen
                const updateHeightHandler = () => {
                    setAppHeightLocal();
                    gameFrame.style.height = `${window.innerHeight}px`;
                    gameFrame.style.width = `${window.innerWidth}px`;
                };
                window.addEventListener('resize', updateHeightHandler);
                window.addEventListener('orientationchange', updateHeightHandler);
                
                // Store handler for removal later
                gameFrame.dataset.updateHandler = 'active';
                
                // Add close button
                const closeBtn = document.createElement('button');
                closeBtn.innerHTML = '✕';
                closeBtn.id = 'fullscreenCloseBtn';
                
                // Add hover effect
                closeBtn.addEventListener('mouseenter', function() {
                    this.style.background = 'rgba(220, 38, 38, 0.9)';
                    this.style.transform = 'scale(1.1)';
                });
                
                closeBtn.addEventListener('mouseleave', function() {
                    this.style.background = 'rgba(0,0,0,0.8)';
                    this.style.transform = 'scale(1)';
                });
                
                closeBtn.addEventListener('click', function() {
                    deactivateMobileFullscreen();
                });
                
                document.body.appendChild(closeBtn);
                
                // Update fullscreen button icon
                const fullscreenBtn = document.getElementById('fullscreenBtn');
                const fullscreenIcon = fullscreenBtn.querySelector('svg');
                fullscreenIcon.innerHTML = '<path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"></path>';
            }
            
            function deactivateMobileFullscreen() {
                // Remove mobile fullscreen classes
                document.body.classList.remove('mobile-fullscreen-active');
                gameFrame.classList.remove('mobile-fullscreen');
                
                // Remove touch scroll prevention
                document.removeEventListener('touchmove', preventTouchMoveLocal, { passive: false });
                
                // Reset game frame dimensions
                gameFrame.style.height = '';
                gameFrame.style.width = '';
                
                // Clear update handler flag
                delete gameFrame.dataset.updateHandler;
                
                // Restore scrolling
                document.body.style.overflow = '';
                document.documentElement.style.overflow = '';
                
                // Restore scroll position
                const scrollY = document.body.style.top;
                document.body.style.top = '';
                window.scrollTo(0, parseInt(scrollY || '0') * -1);
                
                // Show all UI elements
                if (header) header.style.display = '';
                if (sidebar) sidebar.style.display = '';
                if (breadcrumb) breadcrumb.style.display = '';
                if (footer) footer.style.display = '';
                if (sparkleContainer) sparkleContainer.style.display = '';
                
                // Restore game info bar
                const gameInfoBar = document.querySelector('.game-info-bar');
                if (gameInfoBar) gameInfoBar.style.display = '';
                
                // Remove close button
                const closeBtn = document.getElementById('fullscreenCloseBtn');
                if (closeBtn) {
                    document.body.removeChild(closeBtn);
                }
                
                // Update fullscreen button icon
                const fullscreenBtn = document.getElementById('fullscreenBtn');
                const fullscreenIcon = fullscreenBtn.querySelector('svg');
                fullscreenIcon.innerHTML = '<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>';
            }
        });
"""

def update_file(filepath):
    """Update a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has setAppHeightLocal
        if 'setAppHeightLocal' in content:
            return 'skipped'
        
        # Find and replace the old fullscreen implementation
        # Pattern: Match from "// Fullscreen functionality" to the end of that addEventListener block
        pattern = r'(\s*//\s*Fullscreen functionality[^\n]*\n\s*document\.getElementById\([\'"]fullscreenBtn[\'"]\)\.addEventListener\([\'"]click[\'"],[^}]+\{(?:[^{}]|\{[^}]*\})*\}\);)'
        
        match = re.search(pattern, content, re.DOTALL)
        if not match:
            return 'no_match'
        
        # Insert viewport script before the fullscreen listener
        # Find the position before the fullscreen comment
        insert_pos = match.start()
        
        # Create the new content
        new_content = (
            content[:insert_pos] + 
            '\n' + VIEWPORT_HEIGHT_SCRIPT + '\n' +
            FULLSCREEN_LISTENER + 
            content[match.end():]
        )
        
        # Write the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return 'updated'
        
    except Exception as e:
        print(f"ERROR in {filepath.name}: {str(e)[:100]}")
        return 'error'

def main():
    files = sorted(PLAY_DIR.glob('*.html'))
    print(f"Processing {len(files)} files...\n")
    
    results = {'updated': 0, 'skipped': 0, 'no_match': 0, 'error': 0}
    
    for i, filepath in enumerate(files, 1):
        result = update_file(filepath)
        results[result] += 1
        
        if result == 'updated':
            print(f"[{i:3d}] [OK] {filepath.name}")
        elif result == 'skipped' and 'slope' in filepath.name:
            print(f"[{i:3d}] [-]  {filepath.name}")
        elif i % 50 == 0:
            print(f"[{i:3d}] Processing...")
    
    print(f"\n{'='*60}")
    print(f"Updated:   {results['updated']:3d}")
    print(f"Skipped:   {results['skipped']:3d}")
    print(f"No Match:  {results['no_match']:3d}")
    print(f"Errors:    {results['error']:3d}")
    print(f"{'-'*60}")
    print(f"Total:     {len(files):3d}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

