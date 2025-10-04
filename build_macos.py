#!/usr/bin/env python3
"""
Build script for macOS ARM64 .app bundle
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, check=True):
    """Run shell command and return result"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result

def build_macos_app():
    """Build macOS .app bundle"""
    
    # Check if we're on macOS
    if sys.platform != 'darwin':
        print("Error: macOS build must be run on macOS")
        return False
    
    # Check if virtual environment is active
    if not os.environ.get('VIRTUAL_ENV'):
        print("Error: Please activate virtual environment first")
        print("Run: source .venv/bin/activate")
        return False
    
    # Clean previous builds
    build_dirs = ['build', 'dist', '__pycache__']
    for build_dir in build_dirs:
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
            print(f"Cleaned {build_dir}/")
    
    # Remove .spec files
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"Removed {spec_file}")
    
    # PyInstaller command for macOS app bundle
    pyinstaller_cmd = [
        'pyinstaller',
        '--onedir',  # Create one-directory bundle
        '--windowed',  # No console window
        '--name=FFmpeg_GUI',
        '--icon=icon.icns',  # Will be created if not exists
        '--add-data=utils_safe_extract.py:.',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=ffmpeg',
        '--target-arch=arm64',  # Specific for Apple Silicon
        '--osx-bundle-identifier=com.ffmpegui.app',
        'GUI_pyqt6_WINFF.py'
    ]
    
    try:
        # Create icon if it doesn't exist
        if not os.path.exists('icon.icns'):
            print("Warning: icon.icns not found, using default PyInstaller icon")
            pyinstaller_cmd = [cmd for cmd in pyinstaller_cmd if not cmd.startswith('--icon')]
        
        # Run PyInstaller
        result = run_command(pyinstaller_cmd)
        
        if result.returncode == 0:
            print("\nBuild successful!")
            print("App bundle location: dist/FFmpeg_GUI.app")
            print("\nTo test the app:")
            print("open dist/FFmpeg_GUI.app")
            return True
        else:
            print("Build failed!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        return False

def create_dmg():
    """Create DMG installer for macOS"""
    
    if not os.path.exists('dist/FFmpeg_GUI.app'):
        print("Error: App bundle not found. Build the app first.")
        return False
    
    dmg_name = "FFmpeg_GUI_macOS_ARM64"
    
    # Create DMG using hdiutil
    dmg_cmd = [
        'hdiutil', 'create',
        '-volname', 'FFmpeg GUI',
        '-srcfolder', 'dist/',
        '-ov', '-format', 'UDZO',
        f'{dmg_name}.dmg'
    ]
    
    try:
        run_command(dmg_cmd)
        print(f"\nDMG created: {dmg_name}.dmg")
        return True
    except subprocess.CalledProcessError as e:
        print(f"DMG creation failed: {e}")
        return False

def main():
    """Main build function"""
    print("Building FFmpeg GUI for macOS ARM64...")
    
    if build_macos_app():
        print("\nDo you want to create a DMG installer? (y/N): ", end="")
        create_dmg_choice = input().strip().lower()
        
        if create_dmg_choice in ['y', 'yes']:
            create_dmg()
    
    print("\nBuild process completed.")

if __name__ == '__main__':
    main()