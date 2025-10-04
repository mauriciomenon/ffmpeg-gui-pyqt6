# Windows Build Fix

## Issue: Icon File Not Found

**Error:**
```
FileNotFoundError: Icon input file C:\Users\annye\git\ffmpeg-gui-pyqt6\icon.ico not found
```

## Solution

The build fails because `icon.ico` is referenced in the spec file but doesn't exist in the repository.

### Quick Fix (Updated Files)

The repository has been updated with:

1. **FFmpeg_GUI_Windows.spec** - Icon line commented out
2. **BUILD_WINDOWS_NATIVE.md** - Updated build instructions without icon

### Build Now (After Pulling Updates)

```cmd
git pull origin master
.venv\Scripts\activate.bat
pyinstaller FFmpeg_GUI_Windows.spec
```

### Alternative: Create Custom Icon

If you want a custom icon:

1. **Create icon file:**
   - Find or create a `.ico` file (Windows icon format)
   - Name it `icon.ico`
   - Place in repository root directory

2. **Edit spec file:**
   ```python
   # In FFmpeg_GUI_Windows.spec, uncomment:
   icon='icon.ico'  # Add this file if available
   ```

3. **Build:**
   ```cmd
   pyinstaller FFmpeg_GUI_Windows.spec
   ```

### Build Without Icon (Current Default)

The spec file now builds without requiring an icon:

```cmd
# This will work without icon.ico file
.venv\Scripts\activate.bat
pyinstaller FFmpeg_GUI_Windows.spec
```

Output: `dist\FFmpeg_GUI_Windows_AMD64.exe` (uses default PyInstaller icon)

### Manual Command (No Spec File)

Alternative command without spec file:

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
    GUI_pyqt6_WINFF.py
```

## Status

**Fixed in repository:**
- Spec file updated (icon commented out)
- Build instructions updated
- No icon file required for build

**Pull the latest changes and the build should work.**