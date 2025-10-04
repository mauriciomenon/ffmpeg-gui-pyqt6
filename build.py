#!/usr/bin/env python3
"""
Universal build script for FFmpeg GUI
Supports macOS ARM64 and Windows AMD64 builds
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Build FFmpeg GUI executables')
    parser.add_argument('platform', choices=['macos', 'windows', 'both'], 
                       help='Target platform to build for')
    parser.add_argument('--clean', action='store_true', 
                       help='Clean build artifacts before building')
    
    args = parser.parse_args()
    
    # Check virtual environment
    if not os.environ.get('VIRTUAL_ENV'):
        print("Error: Virtual environment not active")
        print("Activate with: source .venv/bin/activate")
        sys.exit(1)
    
    # Clean if requested
    if args.clean:
        print("Cleaning build artifacts...")
        subprocess.run(['python', '-c', '''
import os, shutil
dirs = ["build", "dist", "__pycache__"]
files = ["*.spec", "*.dmg", "*.zip", "version_info.txt"]
for d in dirs:
    if os.path.exists(d): shutil.rmtree(d)
import glob
for pattern in files:
    for f in glob.glob(pattern): os.remove(f)
print("Cleaned.")
        '''])
    
    # Install PyInstaller if not present
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller>=6.0.0'])
    
    # Build based on platform
    if args.platform in ['macos', 'both']:
        if sys.platform == 'darwin':
            print("Building macOS ARM64 version...")
            result = subprocess.run([sys.executable, 'build_macos.py'])
            if result.returncode != 0:
                print("macOS build failed")
                sys.exit(1)
        else:
            print("Warning: macOS build requires macOS system")
    
    if args.platform in ['windows', 'both']:
        print("Building Windows AMD64 version...")
        result = subprocess.run([sys.executable, 'build_windows.py'])
        if result.returncode != 0:
            print("Windows build failed")
            sys.exit(1)
    
    print("Build completed successfully!")

if __name__ == '__main__':
    main()