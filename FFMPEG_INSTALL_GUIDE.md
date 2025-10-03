# FFmpeg Installation Guide for Windows

To complete the audio processing pipeline, you need to install FFmpeg. Here are several methods:

## Method 1: Using Chocolatey (Recommended)
1. Open PowerShell as Administrator
2. Install Chocolatey if you don't have it:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
3. Install FFmpeg:
   ```powershell
   choco install ffmpeg
   ```

## Method 2: Manual Installation
1. Download FFmpeg from: https://ffmpeg.org/download.html#build-windows
2. Extract the zip file to a folder (e.g., `C:\ffmpeg`)
3. Add `C:\ffmpeg\bin` to your system PATH:
   - Open System Properties → Environment Variables
   - Edit the PATH variable and add `C:\ffmpeg\bin`
   - Restart your command prompt/PowerShell

## Method 3: Using winget
```powershell
winget install ffmpeg
```

## Verify Installation
After installation, verify FFmpeg is working:
```powershell
ffmpeg -version
```

## Run the Complete Pipeline
Once FFmpeg is installed, you can run the complete pipeline:

```powershell
python scripts/pipeline.py --audio_path "audio/testAudio.mp3" --out_dir "output" --language "ja" --model_size "small" --device "cpu" --compute_type "int8" --gap_threshold 0.8 --export_srt
```

Or use the batch script that was generated:
```powershell
output\cut_audio_segments.bat
```
