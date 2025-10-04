#!/usr/bin/env python3
"""
Script to add fullscreen functionality to all game HTML files
"""

import os
import re
from pathlib import Path

# The fullscreen script to inject
FULLSCREEN_SCRIPT = """
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
            setAppHeightLocal(); // Ensure it's set after DOM is loaded
"""

# Directory containing game HTML files
PLAY_DIR = Path('play')

def has_fullscreen_script(content):
    """Check if file already has the fullscreen script"""
    return 'setAppHeightLocal' in content or 'activateMobileFullscreen' in content

def update_html_file(filepath):
    """Update a single HTML file with fullscreen functionality"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has the script
        if has_fullscreen_script(content):
            print(f"✓ Skipping {filepath.name} - already has fullscreen script")
            return False
        
        # Find the DOMContentLoaded event listener
        pattern = r"(\s*// Sidebar functionality\s*\n\s*document\.addEventListener\('DOMContentLoaded', function\(\) \{)"
        
        if not re.search(pattern, content):
            print(f"⚠ Warning: {filepath.name} - Could not find DOMContentLoaded pattern")
            return False
        
        # Replace the pattern with our enhanced script
        new_content = re.sub(pattern, FULLSCREEN_SCRIPT, content, count=1)
        
        if new_content == content:
            print(f"⚠ Warning: {filepath.name} - No changes made")
            return False
        
        # Write the updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Updated {filepath.name}")
        return True
        
    except Exception as e:
        print(f"✗ Error updating {filepath.name}: {e}")
        return False

def main():
    """Main function to update all game files"""
    if not PLAY_DIR.exists():
        print(f"Error: {PLAY_DIR} directory not found!")
        return
    
    html_files = list(PLAY_DIR.glob('*.html'))
    print(f"Found {len(html_files)} HTML files to process\n")
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for filepath in sorted(html_files):
        result = update_html_file(filepath)
        if result:
            updated_count += 1
        elif has_fullscreen_script(filepath.read_text(encoding='utf-8')):
            skipped_count += 1
        else:
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Errors:  {error_count}")
    print(f"  Total:   {len(html_files)}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

