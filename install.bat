@echo off
echo 🎵 Audio Processing Pipeline - Installation Script
echo ================================================

echo.
echo 📋 Checking prerequisites...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

:: Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ FFmpeg is not installed
    echo Installing FFmpeg using winget...
    winget install ffmpeg
    if %errorlevel% neq 0 (
        echo ❌ Failed to install FFmpeg
        echo Please install FFmpeg manually from https://ffmpeg.org
        pause
        exit /b 1
    )
)

echo ✅ FFmpeg found

echo.
echo 🐍 Setting up Python virtual environment...

:: Create virtual environment
python -m venv .venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

:: Activate virtual environment
call .venv\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip wheel

:: Install requirements
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

:: Install Flask dependencies
cd viewer
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Flask requirements
    pause
    exit /b 1
)

cd ..

echo.
echo ✅ Installation completed successfully!
echo.
echo 🚀 To start the web interface:
echo    1. cd viewer
echo    2. python run.py
echo    3. Open http://localhost:5000 in your browser
echo.
echo 🎯 To run command line:
echo    python scripts/pipeline.py --audio_path "your_audio.mp3" --language "ja"
echo.
pause
