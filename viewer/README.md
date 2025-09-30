# 🎵 Audio Processing Pipeline - Web Interface

A modern, professional web interface for AI-powered audio transcription and sentence segmentation. Upload audio files and get instant transcription with intelligent sentence splitting and individual audio segments.

## ✨ Key Features

### 🎤 **Smart Audio Upload**
- **Drag & Drop Interface**: Modern file upload with visual feedback
- **Multi-format Support**: MP3, WAV, M4A, OGG, FLAC
- **File Validation**: Automatic format and size checking (max 100MB)
- **Progress Indicators**: Real-time upload and processing status

### 🤖 **AI-Powered Transcription**
- **faster-whisper Integration**: OpenAI Whisper implementation with word-level timestamps
- **Multi-language Support**: Auto-detect or specify language (Japanese, English, Chinese, etc.)
- **Model Selection**: Choose between speed and accuracy (tiny to large-v3)
- **Processing Time Display**: Real-time feedback on processing duration

### 📝 **Intelligent Sentence Segmentation**
- **Smart Algorithm**: Combines punctuation detection and timing gaps
- **Automatic Splitting**: Breaks long transcripts into natural sentences
- **Timestamp Accuracy**: Precise start/end times for each segment
- **Configurable Thresholds**: Adjustable gap detection for different languages

### ✂️ **Audio Processing**
- **Individual Segments**: Separate MP3 files for each sentence
- **FFmpeg Integration**: High-quality audio cutting with precise timing
- **SRT Generation**: Subtitle files for video editing
- **JSON Export**: Complete metadata with timestamps and file paths

### 🎧 **Interactive Playback**
- **Individual Controls**: Play each segment separately
- **Auto-Next**: Seamless playback through all segments
- **Auto-Scroll**: Automatic navigation to current segment
- **Visual Highlighting**: Current segment highlighting
- **Play All**: Continuous playback of all segments

### 🎨 **Professional UX**
- **Responsive Design**: Works perfectly on desktop and mobile
- **Disabled States**: UI locks during processing to prevent conflicts
- **Loading States**: Clear visual feedback during processing
- **Error Handling**: Comprehensive error messages and recovery

## 🚀 Quick Start

### 1. **Prerequisites**
```bash
# Install FFmpeg (required for audio processing)
# Windows:
winget install ffmpeg

# macOS:
brew install ffmpeg

# Linux:
sudo apt install ffmpeg
```

### 2. **Install Dependencies**
```bash
# Navigate to viewer directory
cd viewer

# Install Python packages
pip install -r requirements.txt
```

### 3. **Run the Application**
```bash
# Option 1: Use launcher (recommended)
python run.py

# Option 2: Direct Flask
python app.py

# Option 3: Windows batch file
start_server.bat
```

### 4. **Access Web Interface**
Open your browser and navigate to: **http://localhost:5000**

## 📁 Project Structure

```
viewer/
├── app.py                    # Main Flask application
├── run.py                    # Application launcher
├── start_server.bat          # Windows batch launcher
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation
├── templates/
│   └── index.html           # Web interface (HTML/CSS/JS)
├── uploads/                 # Temporary upload storage
└── output/                  # Processed results
    └── segments/            # Individual audio files
```

## 🎯 How to Use

### **Step 1: Upload Audio**
1. **Drag & Drop**: Drag your audio file onto the upload area
2. **Or Click**: Click the upload area to browse and select a file
3. **Supported Formats**: MP3, WAV, M4A, OGG, FLAC (max 100MB)

### **Step 2: Configure Settings**
1. **Language**: Choose specific language or leave auto-detect
2. **Model Size**: Select AI model size based on your needs:
   - **Tiny**: Fastest processing, basic accuracy
   - **Small**: Recommended balance (default)
   - **Medium**: Higher accuracy, slower processing
   - **Large**: Maximum accuracy, slowest processing

### **Step 3: Process Audio**
1. **Click "🚀 Process Audio"**
2. **Wait for Processing**: UI will be disabled during processing
3. **Monitor Progress**: Real-time feedback in terminal and browser
4. **Processing Time**: Displayed in results header

### **Step 4: Review Results**
1. **View Segments**: Each sentence with individual audio controls
2. **Play Individual**: Click play on any segment
3. **Use Controls**: Auto-Next, Auto-Scroll, Play All
4. **Download Files**: Access individual audio segments

## 🔧 Configuration Options

### **Model Sizes & Performance**
| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| Tiny | ⚡⚡⚡ | ⭐⭐ | Quick testing |
| Base | ⚡⚡ | ⭐⭐⭐ | Balanced |
| Small | ⚡ | ⭐⭐⭐⭐ | **Recommended** |
| Medium | 🐌 | ⭐⭐⭐⭐⭐ | High accuracy |
| Large | 🐌🐌 | ⭐⭐⭐⭐⭐ | Maximum quality |

### **Supported Languages**
- **Auto-detect** (recommended for mixed content)
- **Japanese** (ja) - Optimized for Japanese audio
- **English** (en) - High accuracy for English
- **Chinese** (zh) - Mandarin and Cantonese support
- **Korean** (ko) - Korean language processing
- **Spanish** (es) - Spanish language support
- **French** (fr) - French language support
- **German** (de) - German language support

### **Audio Format Support**
| Format | Quality | Processing Speed | Recommended |
|--------|---------|------------------|-------------|
| MP3 | ⭐⭐⭐ | ⚡⚡⚡ | ✅ **Best** |
| WAV | ⭐⭐⭐⭐⭐ | ⚡⚡ | ✅ High quality |
| M4A | ⭐⭐⭐⭐ | ⚡⚡ | ✅ Good |
| OGG | ⭐⭐⭐ | ⚡⚡ | ✅ Open source |
| FLAC | ⭐⭐⭐⭐⭐ | ⚡ | ✅ Lossless |

## 📊 Output Information

### **Generated Files**
- **`segments.json`**: Complete metadata with timestamps and file paths
- **`segments/`**: Individual MP3 files for each sentence
- **`segments.srt`**: Subtitle file for video editing
- **Processing Stats**: Time taken, number of segments, model used

### **JSON Structure**
```json
[
  {
    "text": "みなさん、こんにちは、キンスです。",
    "start_time": 0.0,
    "end_time": 2.06,
    "path": "segments/segment_001.mp3",
    "url": "/output/session_id/segments/segment_001.mp3"
  }
]
```

## 🛠️ Technical Architecture

### **Backend (Flask)**
- **Framework**: Flask 2.3+ with Werkzeug
- **AI Engine**: faster-whisper (OpenAI Whisper implementation)
- **Audio Processing**: FFmpeg via pydub
- **File Management**: Session-based organization
- **Error Handling**: Comprehensive error recovery

### **Frontend (HTML5/CSS3/JavaScript)**
- **Responsive Design**: Mobile-first approach
- **Modern UI**: Gradient backgrounds, smooth animations
- **Audio Controls**: HTML5 audio with custom controls
- **Real-time Updates**: Dynamic content loading
- **Accessibility**: Keyboard navigation and screen reader support

### **Processing Pipeline**
1. **Upload Validation**: File type and size checking
2. **AI Transcription**: faster-whisper with word-level timestamps
3. **Sentence Segmentation**: Smart algorithm with punctuation detection
4. **Audio Cutting**: FFmpeg-based precise audio segmentation
5. **File Organization**: Session-based file management
6. **Result Delivery**: JSON metadata and audio file serving

## 🔍 Troubleshooting

### **Common Issues & Solutions**

#### **1. FFmpeg Not Found**
```bash
# Windows
winget install ffmpeg
# Restart terminal after installation

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

#### **2. Model Download Slow**
- **First Run**: Downloads AI model (100-500MB)
- **Subsequent Runs**: Much faster (cached)
- **Network**: Ensure stable internet connection

#### **3. Processing Takes Long**
- **File Size**: Keep under 100MB for best performance
- **Model Size**: Use "small" model for faster processing
- **Language**: Specify language if known for better accuracy

#### **4. Audio Not Playing**
- **Browser Permissions**: Check audio permissions in browser
- **File Generation**: Verify audio files were created successfully
- **Network**: Check browser network tab for 404 errors

#### **5. Unicode Errors**
- **Fixed**: All Unicode issues have been resolved
- **Encoding**: System uses UTF-8 encoding throughout

### **Performance Optimization**

#### **For Speed**
- Use **"small"** model size
- Specify **language** if known
- Use **MP3** format for faster processing
- Keep files under **50MB**

#### **For Accuracy**
- Use **"medium"** or **"large"** model size
- Use **WAV** or **FLAC** format
- Specify **language** for better detection
- Allow longer processing time

## 🌟 Advanced Usage

### **Command Line Processing**
```bash
# Direct pipeline usage
python ../scripts/pipeline.py \
  --audio_path "path/to/audio.mp3" \
  --out_dir "output" \
  --language "ja" \
  --model_size "small" \
  --gap_threshold 0.8 \
  --export_srt
```

### **API Endpoints**
```bash
# Upload and process
POST /upload
Content-Type: multipart/form-data

# Download processed files
GET /output/<session_id>/<filename>

# Check processing status
GET /status/<session_id>
```

### **Batch Processing**
```bash
# Process multiple files
for file in *.mp3; do
  python ../scripts/pipeline.py --audio_path "$file" --out_dir "output_$file"
done
```

## 📈 Performance Metrics

### **Typical Processing Times**
| File Duration | Model Size | Processing Time | Segments Generated |
|---------------|------------|-----------------|-------------------|
| 30 seconds | Small | 15-30 seconds | 5-10 segments |
| 2 minutes | Small | 1-2 minutes | 15-25 segments |
| 5 minutes | Small | 3-5 minutes | 40-60 segments |
| 10 minutes | Medium | 8-15 minutes | 80-120 segments |

### **System Requirements**
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB for models and dependencies
- **CPU**: Multi-core recommended for faster processing
- **Network**: Stable connection for model downloads

## 🔒 Security & Privacy

### **Data Handling**
- **Local Processing**: All processing happens locally
- **No Cloud**: No data sent to external services
- **Temporary Files**: Uploaded files are stored temporarily
- **Session Cleanup**: Files are organized by session ID

### **File Management**
- **Upload Directory**: `uploads/<session_id>/`
- **Output Directory**: `output/<session_id>/`
- **Cleanup**: Manual cleanup of old sessions recommended

## 📝 License & Credits

### **Open Source Components**
- **faster-whisper**: OpenAI Whisper implementation
- **Flask**: Python web framework
- **FFmpeg**: Audio/video processing
- **pydub**: Python audio manipulation

### **Project License**
This project is part of the Audio Processing Pipeline system.

## 🤝 Contributing

### **Bug Reports**
- Check existing issues first
- Provide detailed error messages
- Include system information (OS, Python version)

### **Feature Requests**
- Describe the use case
- Explain the expected behavior
- Consider implementation complexity

### **Development**
- Fork the repository
- Create feature branches
- Test thoroughly before submitting
- Follow existing code style

## 📞 Support

### **Documentation**
- This README file
- Inline code comments
- Terminal help messages

### **Community**
- GitHub Issues for bug reports
- Feature requests welcome
- Pull requests accepted

---

**🎉 Enjoy using the Audio Processing Pipeline Web Interface!**

*For the best experience, use modern browsers (Chrome, Firefox, Safari, Edge) and ensure FFmpeg is properly installed.*
