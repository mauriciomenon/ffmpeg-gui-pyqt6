# Building Native Windows Executable

## Requirements
- Windows 10/11 (AMD64/x86_64)
- Python 3.8+ installed from [python.org](https://www.python.org/downloads/)
- Git for Windows (optional) from [git-scm.com](https://git-scm.com/)

## Setup on Windows

### Method 1: Using Git
1. **Clone repository:**
   ```cmd
   git clone https://github.com/yourusername/ffmpeg-gui-pyqt6.git
   cd ffmpeg-gui-pyqt6
   ```

### Method 2: Download ZIP
1. **Download repository:**
   - Go to GitHub repository page
   - Click "Code" > "Download ZIP"
   - Extract to desired folder
   - Open Command Prompt in extracted folder

### Setup Virtual Environment
2. **Create and activate virtual environment:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```
   
   **Note:** If you see `(.venv)` at the start of your command prompt, the virtual environment is active.

3. **Install dependencies:**
   ```cmd
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Test Installation
4. **Test the application:**
   ```cmd
   python GUI_pyqt6_WINFF.py
   ```

## Build Native Windows .exe

### Method 1: Using spec file (recommended)
```cmd
.venv\Scripts\activate.bat
pyinstaller FFmpeg_GUI_Windows.spec
```

### Method 2: Direct command
```cmd
.venv\Scripts\activate.bat
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
- **Executable**: `dist\FFmpeg_GUI_Windows_AMD64.exe`
- **Size**: ~40-60MB (native Windows)
- **Format**: PE32+ executable (Windows .exe)

## Testing
```cmd
dist\FFmpeg_GUI_Windows_AMD64.exe
```

## Troubleshooting

### "python is not recognized"
- Install Python from [python.org](https://www.python.org/downloads/)
- Check "Add Python to PATH" during installation
- Restart Command Prompt after installation

### "No module named PyQt6"
- Ensure virtual environment is activated: `.venv\Scripts\activate.bat`
- Install requirements: `pip install -r requirements.txt`

### "Permission denied" errors
- Run Command Prompt as Administrator
- Check antivirus software (may block PyInstaller)

### Build fails with missing modules
- Add missing modules to `hidden-import` list in spec file
- Check PyInstaller warnings in build output

## Notes
- Creates a true Windows .exe file (PE32+ format)
- No Wine or compatibility layer needed
- Smaller size than cross-compiled version  
- Better Windows integration (file associations, etc.)
- Works on Windows 10/11 AMD64 systems
