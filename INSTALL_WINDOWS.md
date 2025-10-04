# Windows Installation Guide

## Quick Start for Windows Users

### Prerequisites
1. **Download Python 3.8+** from [python.org](https://www.python.org/downloads/)
   - ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
   - Choose "Custom Installation" > Check "Add Python to environment variables"

2. **Verify Python Installation:**
   ```cmd
   python --version
   pip --version
   ```

### Option 1: Download Repository as ZIP
1. Go to the [GitHub repository](https://github.com/yourusername/ffmpeg-gui-pyqt6)
2. Click green "Code" button > "Download ZIP"
3. Extract ZIP to a folder (e.g., `C:\ffmpeg-gui`)
4. Open Command Prompt and navigate to the folder:
   ```cmd
   cd C:\ffmpeg-gui
   ```

### Option 2: Using Git (if installed)
```cmd
git clone https://github.com/yourusername/ffmpeg-gui-pyqt6.git
cd ffmpeg-gui-pyqt6
```

## Setup and Run

### 1. Create Virtual Environment
```cmd
python -m venv .venv
```

### 2. Activate Virtual Environment
```cmd
.venv\Scripts\activate.bat
```
**Note:** You should see `(.venv)` at the beginning of your command prompt

### 3. Install Dependencies
```cmd
pip install --upgrade pip
pip install PyQt6 ffmpeg-python pytest pyinstaller
```

**Or use requirements file:**
```cmd
pip install -r requirements.txt
```

### 4. Run the Application
```cmd
python GUI_pyqt6_WINFF.py
```

## Creating Windows Executable

If you want to create a standalone .exe file:

### 1. Install PyInstaller (if not already installed)
```cmd
pip install pyinstaller
```

### 2. Build executable
```cmd
pyinstaller --onefile --windowed --name=FFmpeg_GUI_Windows ^
    --add-data="utils_safe_extract.py;." ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=ffmpeg ^
    GUI_pyqt6_WINFF.py
```

### 3. Find your executable
The .exe file will be created in: `dist\FFmpeg_GUI_Windows.exe`

## Troubleshooting

### "python is not recognized as an internal or external command"
**Solution:** Python is not in your PATH
1. Reinstall Python from [python.org](https://www.python.org/downloads/)
2. **MUST CHECK**: "Add Python to PATH" during installation
3. Restart Command Prompt

### "No module named 'PyQt6'"
**Solution:** Virtual environment not activated or dependencies not installed
1. Activate virtual environment: `.venv\Scripts\activate.bat`
2. Install dependencies: `pip install -r requirements.txt`

### "Access is denied" when running activate.bat
**Solution:** Execution policy restriction
1. Run PowerShell as Administrator
2. Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Try again with Command Prompt

### PyInstaller build fails
**Solution:** Missing modules or antivirus interference
1. Check antivirus software (may block PyInstaller)
2. Add `--debug` to PyInstaller command to see detailed error
3. Add missing modules with `--hidden-import=module_name`

### Application runs but can't find FFmpeg
**Solution:** Use the built-in FFmpeg downloader
1. Run the application
2. Click "Baixar FFmpeg" button
3. Or install FFmpeg separately and add to PATH

## Alternative: PowerShell Commands

If Command Prompt doesn't work, try PowerShell:

```powershell
# Navigate to project folder
cd C:\path\to\ffmpeg-gui-pyqt6

# Create virtual environment
python -m venv .venv

# Activate (PowerShell syntax)
.venv\Scripts\Activate.ps1

# Install and run
pip install -r requirements.txt
python GUI_pyqt6_WINFF.py
```

## System Requirements

- **OS**: Windows 10 or Windows 11
- **Architecture**: x64 (AMD64) - most modern PCs
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for Python + dependencies

## Getting Help

1. Check this troubleshooting section first
2. Ensure Python and pip are working: `python --version` and `pip --version`
3. Make sure virtual environment is activated (look for `(.venv)` in prompt)
4. Try running without virtual environment as a test
5. Check Windows Event Viewer for application errors