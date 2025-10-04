# Setup Scripts Documentation

## Automated Setup Scripts

The repository includes automated setup scripts for easy installation on different platforms.

### Windows Scripts

#### `setup_windows.bat`
**Purpose:** Automated setup for Windows systems
**Usage:** Double-click or run `setup_windows.bat` in Command Prompt

**What it does:**
1. Checks if Python is installed and accessible
2. Creates virtual environment (`.venv`) if not exists
3. Activates virtual environment
4. Upgrades pip to latest version
5. Installs all dependencies from `requirements.txt`
6. Displays usage instructions

**Error handling:**
- Verifies Python installation
- Checks virtual environment creation
- Validates dependency installation
- Provides helpful error messages

#### `run_windows.bat`
**Purpose:** Quick launcher for the application
**Usage:** Double-click or run `run_windows.bat`

**What it does:**
1. Checks if virtual environment exists
2. Activates virtual environment
3. Launches PyQt6 GUI application
4. Keeps window open if errors occur

### macOS/Linux Scripts

#### `setup_macos.sh`
**Purpose:** Automated setup for macOS and Linux systems
**Usage:** `chmod +x setup_macos.sh && ./setup_macos.sh`

**What it does:**
1. Checks if Python 3 is installed
2. Creates virtual environment using `python3 -m venv`
3. Activates virtual environment
4. Upgrades pip to latest version
5. Installs all dependencies from `requirements.txt`
6. Provides usage instructions including Makefile options

**Error handling:**
- Exits on any error (`set -e`)
- Verifies Python 3 availability
- Checks requirements.txt existence
- Clear error messages with installation hints

#### `run_macos.sh`
**Purpose:** Quick launcher for the application
**Usage:** `./run_macos.sh`

**What it does:**
1. Checks if virtual environment exists
2. Activates virtual environment
3. Launches PyQt6 GUI application

## Usage Examples

### First-time Setup

**Windows:**
```cmd
# Download/clone repository
cd ffmpeg-gui-pyqt6

# Run setup (creates venv and installs dependencies)
setup_windows.bat

# Run application
run_windows.bat
```

**macOS/Linux:**
```bash
# Download/clone repository
cd ffmpeg-gui-pyqt6

# Make scripts executable and run setup
chmod +x setup_macos.sh run_macos.sh
./setup_macos.sh

# Run application
./run_macos.sh
```

### Daily Usage

After initial setup, just use the run scripts:

**Windows:** Double-click `run_windows.bat`
**macOS/Linux:** `./run_macos.sh`

## Troubleshooting

### Windows Issues

**"Python is not recognized"**
- Install Python from [python.org](https://www.python.org/downloads/)
- **IMPORTANT:** Check "Add Python to PATH" during installation
- Restart Command Prompt after installation

**"Access is denied" on .bat files**
- Right-click → "Run as administrator"
- Or adjust execution policies in PowerShell

**Antivirus blocks scripts**
- Add repository folder to antivirus exceptions
- Some antivirus software blocks .bat files by default

### macOS/Linux Issues

**"Permission denied"**
- Make scripts executable: `chmod +x *.sh`
- Check file permissions: `ls -la *.sh`

**"python3: command not found"**
- Install Python 3: `brew install python` (macOS) or `sudo apt install python3` (Linux)
- Use full path: `/usr/bin/python3` instead of `python3`

**Virtual environment creation fails**
- Install venv module: `sudo apt install python3-venv` (Linux)
- Use alternative: `python3 -m pip install virtualenv`

## Manual Alternative

If scripts don't work, you can always use manual installation:

```bash
# Create virtual environment
python -m venv .venv              # Windows
python3 -m venv .venv             # macOS/Linux

# Activate virtual environment  
.venv\Scripts\activate.bat        # Windows
source .venv/bin/activate         # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run application
python GUI_pyqt6_WINFF.py
```

## Integration with Build System

The scripts complement the existing build system:

**Development workflow:**
1. `setup_windows.bat` or `./setup_macos.sh` - Initial setup
2. `run_windows.bat` or `./run_macos.sh` - Daily usage
3. `make build-macos` or build process - Create executables

**Alternative Makefile usage (macOS/Linux):**
```bash
make venv install    # Equivalent to setup script
make run-pyqt        # Equivalent to run script
make build-macos     # Additional build functionality
```