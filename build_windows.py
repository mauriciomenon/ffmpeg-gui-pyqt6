#!/usr/bin/env python3
"""
Build script for Windows AMD64 executable
Can be run on any platform with cross-compilation support
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

def build_windows_exe():
    """Build Windows executable"""
    
    # Check if virtual environment is active
    venv_path = os.environ.get('VIRTUAL_ENV')
    if not venv_path:
        print("Error: Please activate virtual environment first")
        if sys.platform == 'win32':
            print("Run: .venv\\Scripts\\activate")
        else:
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
    
    # PyInstaller command for Windows executable
    pyinstaller_cmd = [
        'pyinstaller',
        '--onefile',  # Single executable file
        '--console',  # Keep console for cross-platform compatibility
        '--name=FFmpeg_GUI_Windows_AMD64',
        '--add-data=utils_safe_extract.py' + (';.' if sys.platform == 'win32' else ':.'),
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=ffmpeg',
        '--hidden-import=ssl',
        '--distpath=dist/windows',
        'GUI_pyqt6_WINFF.py'
    ]
    
    # Add icon if available
    if os.path.exists('icon.ico'):
        pyinstaller_cmd.insert(-1, '--icon=icon.ico')
    else:
        print("Warning: icon.ico not found, using default PyInstaller icon")
    
    # Add Windows-specific options if running on Windows
    if sys.platform == 'win32':
        pyinstaller_cmd.extend([
            '--version-file=version_info.txt'  # Will create if needed
        ])
    
    try:
        # Create version info file for Windows if it doesn't exist
        create_version_info()
        
        # Run PyInstaller
        result = run_command(pyinstaller_cmd)
        
        if result.returncode == 0:
            print("\nBuild successful!")
            print("Executable location: dist/windows/FFmpeg_GUI_Windows_AMD64.exe")
            
            # Create zip package
            create_windows_package()
            return True
        else:
            print("Build failed!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        return False

def create_version_info():
    """Create version info file for Windows executable"""
    
    version_info = """# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,2,0,0),
    prodvers=(1,2,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'FFmpeg GUI'),
        StringStruct(u'FileDescription', u'FFmpeg GUI for Windows'),
        StringStruct(u'FileVersion', u'1.2.0'),
        StringStruct(u'InternalName', u'FFmpeg_GUI'),
        StringStruct(u'LegalCopyright', u'MIT License'),
        StringStruct(u'OriginalFilename', u'FFmpeg_GUI_Windows_AMD64.exe'),
        StringStruct(u'ProductName', u'FFmpeg GUI'),
        StringStruct(u'ProductVersion', u'1.2.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    print("Created version_info.txt")

def create_windows_package():
    """Create ZIP package with executable and documentation"""
    
    import zipfile
    
    zip_name = "FFmpeg_GUI_Windows_AMD64.zip"
    exe_name = "FFmpeg_GUI_Windows_AMD64"
    
    # Look for executable with or without .exe extension
    exe_paths = [
        f"dist/windows/{exe_name}.exe",
        f"dist/windows/{exe_name}",
        f"dist/windows/{exe_name}.app/Contents/MacOS/{exe_name}"
    ]
    
    exe_path = None
    for path in exe_paths:
        if os.path.exists(path):
            exe_path = path
            break
    
    if not exe_path:
        print("Error: Executable not found in expected locations")
        print("Checked paths:", exe_paths)
        return False
    
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add executable with proper name
            exe_filename = "FFmpeg_GUI_Windows_AMD64.exe"
            zipf.write(exe_path, exe_filename)
            
            # Add documentation
            docs = ['README.md', 'LICENSE', 'CHANGELOG.md']
            for doc in docs:
                if os.path.exists(doc):
                    zipf.write(doc, doc)
            
            # Create simple usage instructions
            usage_txt = """FFmpeg GUI for Windows
====================

This is a portable executable for Windows AMD64 systems.

Usage:
1. Double-click FFmpeg_GUI_Windows_AMD64.exe to run
2. If FFmpeg is not installed, use the "Download FFmpeg" button
3. Select your video file and configure conversion settings
4. Click Convert to process your video

Requirements:
- Windows 10 or later (AMD64)
- No additional installation required

For more information, see README.md
"""
            zipf.writestr("USAGE.txt", usage_txt)
        
        print(f"\nPackage created: {zip_name}")
        return True
        
    except Exception as e:
        print(f"Package creation failed: {e}")
        return False

def main():
    """Main build function"""
    print("Building FFmpeg GUI for Windows AMD64...")
    
    if build_windows_exe():
        print("\nWindows build completed successfully!")
        print("Files created:")
        print("- dist/windows/FFmpeg_GUI_Windows_AMD64.exe")
        print("- FFmpeg_GUI_Windows_AMD64.zip")
    else:
        print("Build failed!")

if __name__ == '__main__':
    main()