@echo off
REM FFmpeg GUI - Windows Run Script
REM Quick launcher for the application

echo ===========================================
echo FFmpeg GUI - Starting Application
echo ===========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found!
    echo Please run setup_windows.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if GUI file exists
if not exist "GUI_pyqt6_WINFF.py" (
    echo GUI_pyqt6_WINFF.py not found!
    echo Make sure you are in the correct directory.
    echo.
    pause
    exit /b 1
)

REM Run the PyQt6 version
echo Starting FFmpeg GUI (PyQt6 version)...
echo.
python GUI_pyqt6_WINFF.py

REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)