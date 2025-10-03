#!/bin/bash

echo "🎵 Audio Processing Pipeline - Installation Script"
echo "================================================"

echo ""
echo "📋 Checking prerequisites..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.9+ from https://python.org"
    exit 1
fi

echo "✅ Python found"
python3 --version

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg is not installed"
    echo "Installing FFmpeg..."
    
    # Detect OS and install FFmpeg
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo "Please install Homebrew first: https://brew.sh"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y ffmpeg
        elif command -v yum &> /dev/null; then
            sudo yum install ffmpeg
        else
            echo "Please install FFmpeg manually from https://ffmpeg.org"
            exit 1
        fi
    else
        echo "Please install FFmpeg manually from https://ffmpeg.org"
        exit 1
    fi
fi

echo "✅ FFmpeg found"

echo ""
echo "🐍 Setting up Python virtual environment..."

# Create virtual environment
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip wheel

# Install requirements
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install requirements"
    exit 1
fi

# Install Flask dependencies
cd viewer
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Flask requirements"
    exit 1
fi

cd ..

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "🚀 To start the web interface:"
echo "   1. cd viewer"
echo "   2. python run.py"
echo "   3. Open http://localhost:5000 in your browser"
echo ""
echo "🎯 To run command line:"
echo "   python scripts/pipeline.py --audio_path \"your_audio.mp3\" --language \"ja\""
echo ""
