#!/usr/bin/env python3
"""
Simple launcher for the audio processing web application
"""
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import the pipeline
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

if __name__ == '__main__':
    from app import app
    print("🎵 Starting Audio Processing Pipeline Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)
