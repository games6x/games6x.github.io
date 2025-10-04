#!/usr/bin/env python3
"""
Script to add enhanced fullscreen functionality to all game HTML files
"""

import os
import re
from pathlib import Path

# The complete fullscreen script block to inject (from slope.html lines 790-1041)
FULLSCREEN_SCRIPT_HEADER = """    <script>
        // Set CSS custom property for dynamic viewport height
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

        // Sidebar functionality
        document.addEventListener('DOMContentLoaded', function() {
            setAppHeightLocal(); // Ensure it's set after DOM is loaded"""

FULLSCREEN_FUNCTIONALITY = """

        // Enhanced fullscreen functionality with proper mobile support
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
        });"""

# Directory containing game HTML files
PLAY_DIR = Path('play')

def has_fullscreen_script(content):
    """Check if file already has the enhanced fullscreen script"""
    return ('setAppHeightLocal' in content and 'activateMobileFullscreen' in content)

def update_html_file(filepath):
    """Update a single HTML file with fullscreen functionality"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has the script
        if has_fullscreen_script(content):
            return 'skipped'
        
        # Check if file has the required structure
        if 'id="fullscreenBtn"' not in content or 'id="gameFrame"' not in content or 'id="gameFrame"' not in content:
            return 'missing_elements'
        
        # Pattern 1: Look for existing script tag with DOMContentLoaded
        pattern1 = r'(<script>.*?document\.addEventListener\([\'"]DOMContentLoaded[\'"],[^}]+\}\);)(.*?)(</script>)'
        match1 = re.search(pattern1, content, re.DOTALL)
        
        if match1:
            # Insert fullscreen functionality before the closing script tag
            before_script = match1.group(1)
            middle_content = match1.group(2)
            after_script = match1.group(3)
            
            # Check if there's already fullscreen code
            if 'fullscreenBtn' in middle_content and 'addEventListener' in middle_content:
                # Replace existing fullscreen implementation
                # Remove old fullscreen code
                middle_content = re.sub(
                    r'\s*//\s*(?:Enhanced\s+)?[Ff]ullscreen.*?(?=\n\s*//|\n\s*document\.|</script>)',
                    '',
                    middle_content,
                    flags=re.DOTALL
                )
            
            new_content = before_script + FULLSCREEN_FUNCTIONALITY + middle_content + after_script
            
            # Also update the header if it doesn't have setAppHeightLocal
            if 'setAppHeightLocal' not in content:
                # Replace the opening script + DOMContentLoaded part
                pattern_header = r'<script>\s*document\.addEventListener\([\'"]DOMContentLoaded[\'"],[^{]+\{'
                new_content = re.sub(pattern_header, FULLSCREEN_SCRIPT_HEADER, new_content, count=1)
            
            # Write the updated content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return 'updated'
        else:
            return 'no_pattern_match'
        
    except Exception as e:
        print(f"Error: {e}")
        return 'error'

def main():
    """Main function to update all game files"""
    if not PLAY_DIR.exists():
        print(f"Error: {PLAY_DIR} directory not found!")
        return
    
    html_files = list(PLAY_DIR.glob('*.html'))
    print(f"Found {len(html_files)} HTML files to process\n")
    print("="*70)
    
    results = {
        'updated': [],
        'skipped': [],
        'missing_elements': [],
        'no_pattern_match': [],
        'error': []
    }
    
    for i, filepath in enumerate(sorted(html_files), 1):
        result = update_html_file(filepath)
        results[result].append(filepath.name)
        
        # Print progress
        if result == 'updated':
            print(f"[{i:3d}/{len(html_files)}] [OK] {filepath.name}")
        elif result == 'skipped':
            print(f"[{i:3d}/{len(html_files)}] [-] {filepath.name} (already has script)")
        elif i % 50 == 0:  # Print every 50 files
            print(f"[{i:3d}/{len(html_files)}] Processed...")
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY:")
    print(f"  [OK] Updated:           {len(results['updated']):3d}")
    print(f"  [-]  Skipped:           {len(results['skipped']):3d}")
    print(f"  [!]  Missing Elements:  {len(results['missing_elements']):3d}")
    print(f"  [!]  No Pattern Match:  {len(results['no_pattern_match']):3d}")
    print(f"  [X]  Errors:            {len(results['error']):3d}")
    print(f"  {'-'*34}")
    print(f"  Total:                  {len(html_files):3d}")
    print("="*70)
    
    # Print warnings if any
    if results['missing_elements']:
        print(f"\n[!] Files missing required elements (fullscreenBtn or gameFrame):")
        for name in results['missing_elements'][:10]:  # Show first 10
            print(f"    - {name}")
        if len(results['missing_elements']) > 10:
            print(f"    ... and {len(results['missing_elements']) - 10} more")
    
    if results['no_pattern_match']:
        print(f"\n[!] Files with no matching pattern:")
        for name in results['no_pattern_match'][:10]:  # Show first 10
            print(f"    - {name}")
        if len(results['no_pattern_match']) > 10:
            print(f"    ... and {len(results['no_pattern_match']) - 10} more")

if __name__ == '__main__':
    main()

