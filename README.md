# FFmpeg GUI - PyQt6 & Tkinter

A graphical user interface for FFmpeg video conversion with both PyQt6 and Tkinter implementations.

## Features

- **Dual GUI Options**: Choose between PyQt6 or Tkinter interface
- **Video Conversion**: Support for various codecs, bitrates, and resolutions
- **FFmpeg Integration**: Built-in FFmpeg download and installation assistance
- **Video Analysis**: Display video information using ffprobe
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Non-blocking Operations**: Responsive UI during video processing

## Contents

- `GUI_pyqt6_WINFF.py` — PyQt6 interface with additional features
- `GUI_tkinter_WINFF.py` — Lightweight Tkinter interface
- `utils_safe_extract.py` — Safe archive extraction utilities
- `requirements.txt` — Project dependencies
- `Makefile` — Development automation scripts

## Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (can be downloaded through the application)

### From Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ffmpeg-gui-pyqt6.git
   cd ffmpeg-gui-pyqt6
   ```

2. **Set up virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   # PyQt6 version
   python GUI_pyqt6_WINFF.py
   
   # Or Tkinter version
   python GUI_tkinter_WINFF.py
   ```

### Binary Downloads

Pre-built executables are available for:

- **macOS ARM64**: `FFmpeg_GUI_macOS_ARM64.dmg` - Native .app bundle in DMG installer
- **Windows AMD64**: Native build required (see `BUILD_WINDOWS_NATIVE.md`)

Note: Cross-compilation from macOS to Windows is not supported by PyInstaller. 
For Windows .exe, build on Windows system using provided spec files.

## Building Executables

### Build Requirements
- Virtual environment with dependencies installed
- PyInstaller 6.0+ (included in requirements.txt)

### Build Commands

```bash
# macOS ARM64 .app bundle
make build-macos

# Windows AMD64 executable (cross-platform)
make build-windows

# Clean build artifacts
make clean-build

# Universal build script
python build.py macos     # macOS only
python build.py windows   # Any platform  
python build.py both      # Both platforms
```

### Build Outputs

**macOS ARM64:**
- `dist/FFmpeg_GUI.app` - Application bundle
- Optional: DMG installer

**Windows AMD64:**
- `dist/windows/FFmpeg_GUI_Windows_AMD64.exe` - Executable
- `FFmpeg_GUI_Windows_AMD64.zip` - Distribution package

See `build_info.md` for detailed build instructions and troubleshooting.

## Usage

1. **Select Input File**: Click "Browse" to choose your video file
2. **Set Output Directory**: Choose where to save the converted video
3. **Configure Settings**: 
   - Select video codec (H.264, H.265, VP9, etc.)
   - Choose audio codec (AAC, MP3, etc.)
   - Set bitrate and resolution
4. **Preview Command**: Review the FFmpeg command before conversion
5. **Convert**: Click "Convert" to start processing

### FFmpeg Installation

If FFmpeg is not installed:
- Use "Baixar FFmpeg" to download FFmpeg binaries
- On Windows, use "Instalar FFmpeg (winget)" for automatic installation
- The app provides guided installation assistance

## Development

### Environment Setup

Using direnv (optional):
```bash
cp .envrc.example .envrc
direnv allow
```

### Running Tests

```bash
# Run all tests
make test

# Or manually with pytest
pytest -v
```

### Code Quality

```bash
# Install git hooks for pre-commit checks
make hooks

# The pre-commit hook will run:
# - File size limits check
# - pytest test suite
```

### Project Structure

```
ffmpeg-gui-pyqt6/
├── GUI_pyqt6_WINFF.py      # Main PyQt6 application
├── GUI_tkinter_WINFF.py    # Tkinter alternative
├── utils_safe_extract.py   # Security utilities
├── requirements.txt        # Dependencies
├── Makefile               # Development tasks
├── tests/                 # Test suite
│   ├── test_command_build.py
│   └── test_safe_extract.py
├── .github/               # CI/CD workflows
└── .githooks/             # Git hooks
```

## Contributing

We accept contributions. Please follow these guidelines:

### Getting Started
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Install development dependencies: `make install`
4. Set up git hooks: `make hooks`

### Development Workflow
1. Make your changes
2. Run tests: `make test`
3. Commit your changes with clear messages
4. Push to your fork and submit a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Keep commits focused and atomic
- Write clear commit messages

### Security Considerations
- All file extractions use safe extraction utilities
- FFmpeg downloads are verified and secured
- Input validation prevents command injection

## Security

This project implements several security measures:
- **Safe Archive Extraction**: Prevents directory traversal attacks
- **Input Sanitization**: Validates all user inputs
- **Secure Downloads**: HTTPS-only with certificate verification
- **Command Injection Prevention**: Proper escaping of shell commands

Report security vulnerabilities privately to the maintainers.

## Platform Support

- **Windows**: Support with winget integration
- **macOS**: Native support with Homebrew compatibility  
- **Linux**: Support across distributions

## Troubleshooting

### Common Issues

**"FFmpeg not found"**
- Use the built-in download feature
- Install via package manager: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Ubuntu)

**"Qt platform plugin not found"**
- Install system Qt libraries or use the Tkinter version
- Set `QT_QPA_PLATFORM=offscreen` for headless environments

**Permission errors on extracted files**
- Ensure write permissions to output directory
- On macOS/Linux, check directory ownership

### Getting Help

1. Check the [Issues](https://github.com/yourusername/ffmpeg-gui-pyqt6/issues) page
2. Review existing discussions and solutions
3. Create a new issue with detailed information:
   - OS and Python version
   - Error messages
   - Steps to reproduce

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original Tkinter implementation by Mauricio Menon
- FFmpeg team for the media processing framework
- PyQt6 and Tkinter communities for GUI frameworks

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and updates.

---

This repository follows strict technical documentation standards. See CONTRIBUTING_RULES.md for details.
