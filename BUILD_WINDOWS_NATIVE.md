# Building Native Windows Executable

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
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

## Build Native Windows .exe

### Method 1: Using spec file (recommended)
```cmd
.venv\Scripts\activate
pyinstaller FFmpeg_GUI_Windows.spec
```

### Method 2: Direct command
```cmd
.venv\Scripts\activate
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
- Executable: `dist\FFmpeg_GUI_Windows_AMD64.exe`
- Size: ~40-60MB (native Windows)
- Format: PE32+ executable (Windows .exe)

## Testing
```cmd
dist\FFmpeg_GUI_Windows_AMD64.exe
```

## Notes
- This creates a true Windows .exe file
- No Wine or compatibility layer needed
- Smaller size than cross-compiled version
- Better Windows integration (file associations, etc.)
