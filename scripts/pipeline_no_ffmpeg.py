#!/usr/bin/env python3
import argparse, json, os, re, sys
from pathlib import Path
from typing import List, Dict, Any

# Transcription (word-level timestamps)
from faster_whisper import WhisperModel

# For audio processing without pydub
import wave
import struct

SENTENCE_END_CHARS = set(list(".!?。！？…"))

def transcribe(audio_path: Path, model_size: str, device: str, compute_type: str, language: str = None):
    """
    Returns (words:list[dict], segments:list[dict], info)
    Each word: {"text": str, "start": float, "end": float}
    """
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    segments, info = model.transcribe(
        str(audio_path),
        language=language,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=200),
        word_timestamps=True,
        beam_size=5,
    )

    words = []
    seg_objs = []
    for seg in segments:
        seg_obj = dict(
            start=float(seg.start) if seg.start is not None else None,
            end=float(seg.end) if seg.end is not None else None,
            text=seg.text.strip()
        )
        seg_objs.append(seg_obj)
        if seg.words:
            for w in seg.words:
                if w.start is None or w.end is None:
                    # Skip tokens without timing (rare)
                    continue
                words.append(dict(text=w.word, start=float(w.start), end=float(w.end)))
        else:
            # Fallback: if words are missing, approximate by splitting the seg text evenly
            chars = list(seg.text.strip())
            if not chars:
                continue
            dur = (seg_obj["end"] - seg_obj["start"]) if seg_obj["start"] is not None and seg_obj["end"] is not None else 0.0
            if dur <= 0 or seg_obj["start"] is None:
                continue
            per_char = dur / max(len(chars), 1)
            t = seg_obj["start"]
            for ch in chars:
                words.append(dict(text=ch, start=t, end=t + per_char))
                t += per_char

    # sort by time just in case
    words.sort(key=lambda w: (w["start"], w["end"]))
    return words, seg_objs, info

def should_close_sentence(accum_text: str, current_word: Dict[str, Any], next_word: Dict[str, Any], gap_threshold: float) -> bool:
    # 1) punctuation-based
    if accum_text and accum_text[-1] in SENTENCE_END_CHARS:
        return True
    # 2) long gap to next word
    if next_word is not None:
        gap = next_word["start"] - current_word["end"]
        if gap >= gap_threshold:
            return True
    return False

def words_to_sentences(words: List[Dict[str, Any]], gap_threshold: float, max_chars: int = 80) -> List[Dict[str, Any]]:
    """
    Greedy grouping into sentences using punctuation as primary signal,
    then long gaps as fallback. Adds a length guard to avoid giant chunks.
    """
    sentences = []
    if not words:
        return sentences

    acc = []
    for i, w in enumerate(words):
        acc.append(w)
        next_w = words[i+1] if i+1 < len(words) else None
        accum_text = "".join(x["text"] for x in acc)

        need_close = False

        # close if we hit punctuation or a long gap
        if should_close_sentence(accum_text, w, next_w, gap_threshold):
            need_close = True
        # length guard if no punctuation shows up for a while
        elif len(accum_text) >= max_chars:
            need_close = True

        if need_close:
            start = acc[0]["start"]
            end   = acc[-1]["end"]
            text  = normalize_spacing(accum_text)
            if text.strip():
                sentences.append(dict(text=text, start_time=float(start), end_time=float(end)))
            acc = []

    # Flush last
    if acc:
        start = acc[0]["start"]
        end   = acc[-1]["end"]
        text  = normalize_spacing("".join(x["text"] for x in acc))
        if text.strip():
            sentences.append(dict(text=text, start_time=float(start), end_time=float(end)))

    return sentences

def normalize_spacing(s: str) -> str:
    # Collapse awkward spaces around CJK and punctuation
    s = re.sub(r"\s+", " ", s).strip()
    # remove spaces before CJK punctuation
    s = re.sub(r"\s+([。！？…])", r"\1", s)
    return s

def create_audio_segments_info(sentences: List[Dict[str, Any]], out_dir: Path) -> List[Dict[str, Any]]:
    """
    Create information about audio segments without actually cutting the audio.
    This creates the JSON structure but notes that FFmpeg is needed for actual audio cutting.
    """
    seg_dir = out_dir / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, sent in enumerate(sentences, start=1):
        filename = f"segment_{i:03}.mp3"
        results.append({
            "text": sent["text"],
            "start_time": round(sent["start_time"], 3),
            "end_time": round(sent["end_time"], 3),
            "path": f"segments/{filename}",
            "note": "Audio segment needs to be created with FFmpeg. Install FFmpeg and run the full pipeline."
        })
    return results

def write_json(items: List[Dict[str, Any]], out_dir: Path):
    with open(out_dir / "segments.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def write_ffmpeg_script(sentences: List[Dict[str, Any]], audio_path: Path, out_dir: Path):
    """Create a batch script to cut audio segments using FFmpeg"""
    script_path = out_dir / "cut_audio_segments.bat"
    seg_dir = out_dir / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)
    
    with open(script_path, "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("echo Cutting audio segments with FFmpeg...\n")
        f.write(f'md "{seg_dir}" 2>nul\n')
        
        for i, sent in enumerate(sentences, start=1):
            start_time = sent["start_time"]
            duration = sent["end_time"] - sent["start_time"]
            filename = f"segment_{i:03}.mp3"
            
            f.write(f'ffmpeg -i "{audio_path}" -ss {start_time:.3f} -t {duration:.3f} -c copy "{seg_dir / filename}"\n')
        
        f.write("echo Done! Audio segments created.\n")
        f.write("pause\n")

def main():
    ap = argparse.ArgumentParser(description="Audio transcription and sentence splitting (without audio cutting)")
    ap.add_argument("--audio_path", required=True, help="Path to input audio")
    ap.add_argument("--out_dir", default="output", help="Output directory")
    ap.add_argument("--language", default=None, help="Force language code (e.g., ja, zh, vi, en). Omit to auto-detect.")
    ap.add_argument("--model_size", default="small", help="Whisper model size: tiny|base|small|medium|large-v3")
    ap.add_argument("--device", default="cpu", help="cpu or cuda")
    ap.add_argument("--compute_type", default="int8", help="int8|int8_float16|float16|float32 (choose per hardware)")
    ap.add_argument("--gap_threshold", type=float, default=0.8, help="Seconds of silence to split when punctuation missing")
    args = ap.parse_args()

    audio_path = Path(args.audio_path).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[1/3] Transcribing with faster-whisper (word timestamps)…")
    words, segs, info = transcribe(audio_path, args.model_size, args.device, args.compute_type, language=args.language)
    print(f"   Detected language={getattr(info, 'language', 'n/a')}  |  duration≈{getattr(info, 'duration', 'n/a')}s")
    print(f"   Words={len(words)} | Segments={len(segs)}")

    print("[2/3] Grouping into sentences…")
    sentences = words_to_sentences(words, gap_threshold=args.gap_threshold, max_chars=80)
    print(f"   Sentences={len(sentences)}")

    print("[3/3] Creating output files…")
    items = create_audio_segments_info(sentences, out_dir)
    write_json(items, out_dir)
    write_ffmpeg_script(sentences, audio_path, out_dir)

    print(f"Done! See: {out_dir / 'segments.json'}")
    print(f"FFmpeg batch script created: {out_dir / 'cut_audio_segments.bat'}")
    print("To cut audio segments, install FFmpeg and run the batch script.")

if __name__ == "__main__":
    main()
