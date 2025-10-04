#!/bin/bash
# FFmpeg GUI - macOS/Linux Setup Script
# This script sets up the virtual environment and installs dependencies

set -e  # Exit on any error

echo "==========================================="
echo "FFmpeg GUI - macOS/Linux Setup"
echo "==========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found!"
    echo ""
    echo "Please install Python 3.8+ from:"
    echo "- macOS: https://www.python.org/downloads/ or 'brew install python'"
    echo "- Linux: 'sudo apt install python3 python3-venv python3-pip'"
    echo ""
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created successfully!"
else
    echo "Virtual environment already exists."
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Dependencies installed successfully!"
else
    echo "ERROR: requirements.txt not found!"
    exit 1
fi

echo ""
echo "==========================================="
echo "Setup completed successfully!"
echo "==========================================="
echo ""
echo "To run the application:"
echo "1. Activate virtual environment: source .venv/bin/activate"
echo "2. Run PyQt6 version: python GUI_pyqt6_WINFF.py"
echo "3. Or run Tkinter version: python GUI_tkinter_WINFF.py"
echo ""
echo "To build macOS application:"
echo "1. Activate virtual environment: source .venv/bin/activate"
echo "2. Run: python build_macos.py"
echo ""
echo "Alternative: use Makefile commands"
echo "- make venv install"
echo "- make run-pyqt"
echo "- make build-macos"
echo ""