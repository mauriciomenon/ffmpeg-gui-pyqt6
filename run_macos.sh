#!/bin/bash
# FFmpeg GUI - macOS/Linux Run Script
# Quick launcher for the application

echo "==========================================="
echo "FFmpeg GUI - Starting Application"
echo "==========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run ./setup_macos.sh first to set up the environment."
    echo ""
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if GUI file exists
if [ ! -f "GUI_pyqt6_WINFF.py" ]; then
    echo "GUI_pyqt6_WINFF.py not found!"
    echo "Make sure you are in the correct directory."
    echo ""
    exit 1
fi

# Run the PyQt6 version
echo "Starting FFmpeg GUI (PyQt6 version)..."
echo ""
python GUI_pyqt6_WINFF.py