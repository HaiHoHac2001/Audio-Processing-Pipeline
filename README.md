# 🎵 Audio Processing Pipeline - Web Interface

A complete **AI-powered audio processing pipeline** with modern web interface for Japanese language learning and audio analysis.

## ✨ Features

### 🎯 **Core Pipeline:**
1) **Input**: Audio file ≤ 30s (`.mp3/.wav/.m4a/.ogg/.flac`)
2) **AI Transcription**: Word-level timestamps using `faster-whisper`
3) **Smart Segmentation**: Punctuation-based + pause detection
4) **Audio Cutting**: Individual MP3 files per sentence
5) **JSON Export**: Complete metadata with timestamps
6) **Web Interface**: Modern drag & drop UI with interactive playback

### 🌟 **Web Interface Features:**
- **Drag & Drop** upload with real-time feedback
- **Multi-language** support (Japanese, English, Chinese, Vietnamese)
- **Interactive playback** with Auto-Next functionality
- **Responsive design** (desktop & mobile)
- **Processing time** display
- **Error handling** with user-friendly messages

---

## 🚀 Quick Start

### **Option 1: Web Interface (Recommended)**
```bash
# 1. Clone repository
git clone https://github.com/HaiHoHac2001/Audio-Processing-Pipeline.git
cd Audio-Processing-Pipeline

# 2. Install FFmpeg (Windows)
winget install ffmpeg

# 3. Setup Python environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate  # macOS/Linux

# 4. Install dependencies
pip install -r requirements.txt
pip install audioop-lts  # Fix for Python 3.13

# 5. Run web interface
cd viewer
python run.py

# 6. Open browser: http://localhost:5000
```

### **Option 2: Command Line**
```bash
python scripts/pipeline.py --audio_path "your_audio.mp3" --out_dir "output" --language "ja" --model_size "small"
```

## 📋 Prerequisites

### **Required:**
- **FFmpeg** (for audio processing)
- **Python 3.9+** (3.13 supported with fixes)
- **Virtual Environment** (recommended)

### **FFmpeg Installation:**
- **Windows**: `winget install ffmpeg` or `choco install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`

### **Python 3.13 Compatibility:**
This project includes fixes for Python 3.13 compatibility issues with `audioop` module.

---

## 🎯 Usage

### **Web Interface (Recommended)**

1. **Start the web server:**
   ```bash
   cd viewer
   python run.py
   ```

2. **Open browser:** http://localhost:5000

3. **Upload audio file** (≤30s, mp3/wav/m4a/ogg/flac)

4. **Select options:**
   - Language: Japanese, English, Chinese, Vietnamese, or Auto-detect
   - Model size: tiny, base, small, medium, large-v3

5. **Click "Process Audio"** and wait for results

6. **Interactive playback:**
   - Play individual sentences
   - Auto-Next functionality
   - Auto-Scroll following
   - Play All feature

### **Command Line Interface**

```bash
python scripts/pipeline.py \
  --audio_path "your_audio.mp3" \
  --out_dir "output" \
  --language "ja" \
  --model_size "small" \
  --gap_threshold 0.8 \
  --export_srt
```

**Output files:**
- `output/segments/segment_001.mp3` - Individual audio clips
- `output/segments.json` - Metadata with timestamps
- `output/segments.srt` - Subtitle file (if --export_srt used)

---

## 🔧 Configuration & Troubleshooting

### **Model Selection:**
- **tiny**: Fastest, lowest accuracy
- **base**: Good balance
- **small**: Recommended (good accuracy/speed)
- **medium**: Higher accuracy, slower
- **large-v3**: Best accuracy, slowest

### **Language Support:**
- **Japanese**: `ja` (optimized for JLPT)
- **English**: `en`
- **Chinese**: `zh`
- **Vietnamese**: `vi`
- **Auto-detect**: Leave language field empty

### **Troubleshooting:**

#### **Python 3.13 Issues:**
```bash
# If you get "No module named 'audioop'" error:
pip install audioop-lts
```

#### **FFmpeg Not Found:**
```bash
# Windows
winget install ffmpeg
# or
choco install ffmpeg

# Verify installation
ffmpeg -version
```

#### **Virtual Environment Issues:**
```bash
# Create fresh environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
pip install audioop-lts
```

### **Performance Tips:**
- Use **GPU acceleration** if available: `--device cuda --compute_type float16`
- **Smaller model sizes** for faster processing
- **Shorter audio files** (≤30s) for best results
- **SSD storage** for faster I/O operations

## 📁 Project Structure

```
Audio-Processing-Pipeline/
├── scripts/
│   └── pipeline.py          # Core processing script
├── viewer/                  # Flask Web Application
│   ├── app.py              # Main Flask app
│   ├── run.py              # Application launcher
│   ├── templates/
│   │   └── index.html      # Web interface
│   └── requirements.txt    # Flask dependencies
├── requirements.txt        # Main dependencies
└── README.md              # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **faster-whisper** for AI transcription
- **Flask** for web framework
- **FFmpeg** for audio processing
- **pydub** for audio manipulation
