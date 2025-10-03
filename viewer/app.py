#!/usr/bin/env python3
"""
Flask web application for audio processing pipeline
"""
import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_pipeline(audio_path, output_dir, language=None, model_size="small"):
    """Run the audio processing pipeline"""
    try:
        # Get the path to the pipeline script
        script_path = Path(__file__).parent.parent / "scripts" / "pipeline.py"
        
        # Check if script exists
        if not script_path.exists():
            return False, f"Pipeline script not found at: {script_path}"
        
        # Use Python executable from virtual environment
        # Get the parent directory (project root) and find .venv
        project_root = Path(__file__).parent.parent
        venv_python = project_root / ".venv" / "Scripts" / "python.exe"
        
        if venv_python.exists():
            python_exe = str(venv_python)
        else:
            # Fallback to current Python if venv not found
            python_exe = sys.executable
        
        # Convert to absolute paths
        audio_path_abs = Path(audio_path).resolve()
        output_dir_abs = Path(output_dir).resolve()
        
        # Build command
        cmd = [
            python_exe, str(script_path),
            "--audio_path", str(audio_path_abs),
            "--out_dir", str(output_dir_abs),
            "--model_size", model_size,
            "--device", "cpu",
            "--compute_type", "int8",
            "--gap_threshold", "0.8",
            "--export_srt"
        ]
        
        if language:
            cmd.extend(["--language", language])
        
        print(f"Running command: {' '.join(cmd)}")
        
        # Run the pipeline
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        print(f"Return code: {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        
        if result.returncode != 0:
            return False, f"Pipeline failed: {result.stderr}"
        
        return True, "Processing completed successfully"
        
    except Exception as e:
        return False, f"Error running pipeline: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: mp3, wav, m4a, ogg, flac'}), 400
        
        # Get processing parameters
        language = request.form.get('language', '').strip() or None
        model_size = request.form.get('model_size', 'small')
        
        print(f"Processing file: {file.filename}")
        print(f"Language: {language}")
        print(f"Model size: {model_size}")
        
        # Record start time
        import time
        start_time = time.time()
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Create session directories
        session_upload_dir = Path(app.config['UPLOAD_FOLDER']) / session_id
        # Use parent directory for output to match pipeline script
        session_output_dir = Path(__file__).parent.parent / app.config['OUTPUT_FOLDER'] / session_id
        session_upload_dir.mkdir(parents=True, exist_ok=True)
        session_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        audio_path = session_upload_dir / filename
        file.save(audio_path)
        
        print(f"File saved to: {audio_path}")
        print(f"Output directory: {session_output_dir}")
        
        # Run processing pipeline
        success, message = run_pipeline(audio_path, session_output_dir, language, model_size)
        
        if not success:
            print(f"Pipeline failed: {message}")
            return jsonify({'error': message}), 500
        
        # Load the generated segments.json
        segments_path = session_output_dir / 'segments.json'
        if not segments_path.exists():
            return jsonify({'error': 'Processing completed but no segments found'}), 500
        
        with open(segments_path, 'r', encoding='utf-8') as f:
            segments = json.load(f)
        
        # Update paths to be relative to the session
        for segment in segments:
            segment['path'] = f"segments/{Path(segment['path']).name}"
            # Add full URL path for serving
            segment['url'] = f"/output/{session_id}/segments/{Path(segment['path']).name}"
        
        # Calculate processing time
        end_time = time.time()
        processing_time = round(end_time - start_time, 2)
        
        print(f"Successfully processed {len(segments)} segments in {processing_time} seconds")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'segments': segments,
            'message': message,
            'processing_time': processing_time,
            'total_segments': len(segments)
        })
        
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/output/<session_id>/<path:filename>')
def serve_output(session_id, filename):
    """Serve processed files"""
    # Use parent directory for output to match pipeline script
    output_path = Path(__file__).parent.parent / app.config['OUTPUT_FOLDER'] / session_id
    return send_from_directory(str(output_path), filename)

@app.route('/status/<session_id>')
def get_status(session_id):
    """Check processing status"""
    segments_path = Path(app.config['OUTPUT_FOLDER']) / session_id / 'segments.json'
    
    if segments_path.exists():
        with open(segments_path, 'r', encoding='utf-8') as f:
            segments = json.load(f)
        return jsonify({'status': 'completed', 'segments': segments})
    else:
        return jsonify({'status': 'processing'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
