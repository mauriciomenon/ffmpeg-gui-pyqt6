#!/usr/bin/env python3
"""
Build script for native Windows AMD64 executable
This script creates a .spec file that can be used on Windows to build a true .exe
"""

import os
import sys

def create_windows_spec():
    """Create PyInstaller spec file for native Windows build"""
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['GUI_pyqt6_WINFF.py'],
    pathex=[],
    binaries=[],
    datas=[('utils_safe_extract.py', '.')],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'ffmpeg',
        'ssl',
        'urllib3',
        'certifi'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FFmpeg_GUI_Windows_AMD64',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Add this file if available
)
'''
    
    with open('FFmpeg_GUI_Windows.spec', 'w') as f:
        f.write(spec_content)
    
    print("Created FFmpeg_GUI_Windows.spec file")
    return True

def create_build_instructions():
    """Create instructions for building on Windows"""
    
    instructions = """# Building Native Windows Executable

## Requirements
- Windows 10/11 (AMD64)
- Python 3.8+ installed
- Git for Windows (optional)

## Setup on Windows

1. **Clone repository:**
   ```cmd
   git clone https://github.com/yourusername/ffmpeg-gui-pyqt6.git
   cd ffmpeg-gui-pyqt6
   ```

2. **Create virtual environment:**
   ```cmd
   python -m venv .venv
   .venv\\Scripts\\activate
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

## Build Native Windows .exe

### Method 1: Using spec file (recommended)
```cmd
.venv\\Scripts\\activate
pyinstaller FFmpeg_GUI_Windows.spec
```

### Method 2: Direct command
```cmd
.venv\\Scripts\\activate
pyinstaller --onefile --windowed --name=FFmpeg_GUI_Windows_AMD64 ^
    --add-data="utils_safe_extract.py;." ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=ffmpeg ^
    --hidden-import=ssl ^
    --hidden-import=urllib3 ^
    --icon=icon.ico ^
    GUI_pyqt6_WINFF.py
```

## Output
- Executable: `dist\\FFmpeg_GUI_Windows_AMD64.exe`
- Size: ~40-60MB (native Windows)
- Format: PE32+ executable (Windows .exe)

## Testing
```cmd
dist\\FFmpeg_GUI_Windows_AMD64.exe
```

## Notes
- This creates a true Windows .exe file
- No Wine or compatibility layer needed
- Smaller size than cross-compiled version
- Better Windows integration (file associations, etc.)
"""
    
    with open('BUILD_WINDOWS_NATIVE.md', 'w') as f:
        f.write(instructions)
    
    print("Created BUILD_WINDOWS_NATIVE.md instructions")
    return True

def main():
    """Main function"""
    print("Creating native Windows build files...")
    
    create_windows_spec()
    create_build_instructions()
    
    print("\nFiles created:")
    print("- FFmpeg_GUI_Windows.spec (PyInstaller spec file)")  
    print("- BUILD_WINDOWS_NATIVE.md (build instructions)")
    print("\nTo build native Windows .exe:")
    print("1. Copy these files to a Windows machine")
    print("2. Follow instructions in BUILD_WINDOWS_NATIVE.md")

if __name__ == '__main__':
    main()