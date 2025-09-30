# JLPT Audio Pipeline (30s clip → transcript → sentence segments → per-sentence audio → JSON → simple UI)

This mini project gives you an end‑to‑end pipeline that follows the exact flow in your diagram:

1) **Input**: an audio file ≤ 30s (`.mp3/.wav/.m4a`).
2) **Transcribe** with word‑level timestamps using `faster-whisper` (fast, accurate, supports Japanese/Chinese/Vietnamese/English…).
3) **Sentence segmentation** in Python:
   - Prefer punctuation (`。！？!?…` etc.).
   - Fallback: split by long pauses (gap ≥ 0.8s) or length guard.
4) **Cut audio** per sentence using `pydub` (FFmpeg under the hood).
5) **Write JSON** with `{ text, start_time, end_time, path }`.
6) **Render** a simple web page that lists sentences and lets you play each clipped audio. There’s an **Auto‑Next** button to play through all.

---

## 0) Prerequisites (one-time)

- Install **FFmpeg**
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt-get update && sudo apt-get install -y ffmpeg`
  - Windows (winget): `winget install Gyan.FFmpeg` (or download from ffmpeg.org)
- Python 3.9+ recommended

Create a virtual env and install deps:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -U pip wheel
pip install -r requirements.txt
```

> If you have **NVIDIA GPU**, you can set `--device cuda --compute_type float16` for big speedups.

---

## 1) Run the pipeline

```bash
python scripts/pipeline.py   --audio_path /absolute/path/to/your_30s_audio.mp3   --out_dir output   --language ja              # or 'zh','vi','en', or omit to auto-detect
  --model_size small         # tiny|base|small|medium|large-v3 (large is slowest)
  --gap_threshold 0.8        # seconds: used when punctuation is missing
```

What you get:
- `output/segments/segment_001.mp3` … per-sentence audio clips
- `output/segments.json` … an array of objects: `{"text","start_time","end_time","path"}`
- Open `viewer/index.html` in a browser (or serve the folder) to test playback.

---

## 2) Open the viewer

Simplest: open `viewer/index.html` directly in a browser and select the generated `segments.json` from the **Load JSON** button.  
Or start a quick static server from the project root:

```bash
python -m http.server 8888
# then visit http://localhost:8888/viewer/
# click "Load JSON" and pick /output/segments.json
```

---

## Notes & Tweaks

- If the transcript has no punctuation, the script falls back to **pause-based** splitting (default gap 0.8s). Tune with `--gap_threshold`.
- For Japanese/Chinese, we treat `。！？` as sentence end. You can extend the set in code.
- Want SRT/VTT? Add `--export_srt` and we’ll write `/output/segments.srt`.
- File names & paths are **relative** inside `segments.json`, so you can move the whole `output` folder around easily.
- For accuracy on long audios, switch to **whisperX** alignment later; for ≤30s, `faster-whisper` with word timestamps is usually enough.
