@echo off
REM Full-stack development server launcher for Windows

echo 🔧 PPT Report Generator - Development Server
echo ==============================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is required but not installed
    pause
    exit /b 1
)

REM Install Python dependencies if needed
if not exist "venv" (
    echo 📦 Setting up Python virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Run the development server
python start_dev.py
pause