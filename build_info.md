# Build Instructions

## Requirements

### macOS ARM64 (.app)
- macOS 11.0 or later (Apple Silicon)
- Python 3.8+
- Virtual environment with dependencies installed

### Windows AMD64 (.exe)
- Python 3.8+ (any platform for cross-compilation)
- PyInstaller 6.0+
- Virtual environment with dependencies installed

## Build Commands

### Quick Build
```bash
# Setup environment
make venv install

# Build for current platform
make build-macos    # macOS only
make build-windows  # Any platform

# Universal build script
python build.py macos     # macOS .app
python build.py windows   # Windows .exe
python build.py both      # Both platforms
```

### Manual Build Process

#### macOS ARM64
```bash
source .venv/bin/activate
python build_macos.py
```

Output files:
- `dist/FFmpeg_GUI.app` - Application bundle
- `FFmpeg_GUI_macOS_ARM64.dmg` - Installer (optional)

#### Windows AMD64
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
python build_windows.py
```

Output files:
- `dist/windows/FFmpeg_GUI_Windows_AMD64.exe` - Executable
- `FFmpeg_GUI_Windows_AMD64.zip` - Distribution package

## Build Configuration

### Dependencies
All required dependencies are automatically bundled:
- PyQt6 runtime libraries
- FFmpeg-python bindings
- SSL certificates
- Safe extraction utilities

### Architecture Targets
- **macOS**: ARM64 (Apple Silicon M1/M2/M3)
- **Windows**: AMD64 (x86_64)

### File Structure
```
dist/
├── FFmpeg_GUI.app/                    # macOS bundle
│   └── Contents/
│       ├── MacOS/FFmpeg_GUI           # Executable
│       ├── Resources/                 # Resources
│       └── Info.plist                 # App metadata
└── windows/
    └── FFmpeg_GUI_Windows_AMD64.exe   # Windows executable
```

## Testing Built Applications

### macOS
```bash
# Test the app bundle
open dist/FFmpeg_GUI.app

# Or run directly
dist/FFmpeg_GUI.app/Contents/MacOS/FFmpeg_GUI
```

### Windows
```bash
# Test executable (if on Windows)
dist/windows/FFmpeg_GUI_Windows_AMD64.exe

# Or test via Wine on macOS/Linux
wine dist/windows/FFmpeg_GUI_Windows_AMD64.exe
```

## Distribution

### macOS
- Distribute the `.app` bundle or `.dmg` installer
- Users can drag to Applications folder
- No additional installation required

### Windows
- Distribute the `.zip` package or standalone `.exe`
- No installation required (portable executable)
- All dependencies are bundled

## Troubleshooting

### Common Issues

**"Module not found" errors**
- Ensure all dependencies are installed in virtual environment
- Check that virtual environment is activated before building

**Build fails on macOS**
- Verify you're running on Apple Silicon Mac
- Check Xcode Command Line Tools are installed: `xcode-select --install`

**Windows build missing dependencies**
- Install PyInstaller: `pip install pyinstaller>=6.0.0`
- Ensure all hidden imports are specified in build script

**Large executable size**
- Normal for bundled applications (50-150MB)
- PyQt6 and Python runtime add significant size
- Use `--onefile` for single executable vs `--onedir` for faster startup

### Build Optimization

**Reduce Size**
- Remove unused imports from source code
- Use `--exclude-module` for unneeded packages
- Consider UPX compression (advanced)

**Faster Builds**
- Use `--onedir` instead of `--onefile`
- Keep build cache between builds
- Build incrementally when possible