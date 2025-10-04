@echo off
REM FFmpeg GUI - Windows Setup Script
REM This script sets up the virtual environment and installs dependencies

echo ===========================================
echo FFmpeg GUI - Windows Setup
echo ===========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo.
    echo Make sure requirements.txt exists and contains valid packages
    pause
    exit /b 1
)

echo.
echo ===========================================
echo Setup completed successfully!
echo ===========================================
echo.
echo To run the application:
echo 1. Activate virtual environment: .venv\Scripts\activate.bat
echo 2. Run PyQt6 version: python GUI_pyqt6_WINFF.py
echo 3. Or run Tkinter version: python GUI_tkinter_WINFF.py
echo.
echo To build Windows executable:
echo 1. Activate virtual environment: .venv\Scripts\activate.bat  
echo 2. Run: pyinstaller FFmpeg_GUI_Windows.spec
echo.

pause