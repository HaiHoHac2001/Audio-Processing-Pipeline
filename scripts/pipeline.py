#!/usr/bin/env python3
import argparse, json, os, re, sys
from pathlib import Path
from typing import List, Dict, Any

# Transcription (word-level timestamps)
from faster_whisper import WhisperModel

# Audio slicing
from pydub import AudioSegment

SENTENCE_END_CHARS = set(list(".!?。！？…"))

def load_audio(audio_path: Path) -> AudioSegment:
    return AudioSegment.from_file(audio_path)

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

def export_clips(audio: AudioSegment, sentences: List[Dict[str, Any]], out_dir: Path) -> List[Dict[str, Any]]:
    seg_dir = out_dir / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, sent in enumerate(sentences, start=1):
        start_ms = max(int(sent["start_time"] * 1000), 0)
        end_ms = max(int(sent["end_time"] * 1000), start_ms + 1)
        clip = audio[start_ms:end_ms]
        filename = f"segment_{i:03}.mp3"
        abs_path = seg_dir / filename
        clip.export(abs_path, format="mp3")
        results.append({
            "text": sent["text"],
            "start_time": round(sent["start_time"], 3),
            "end_time": round(sent["end_time"], 3),
            "path": f"segments/{filename}"
        })
    return results

def write_json(items: List[Dict[str, Any]], out_dir: Path):
    with open(out_dir / "segments.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def maybe_write_srt(items: List[Dict[str, Any]], out_dir: Path, export: bool):
    if not export:
        return
    lines = []
    for idx, it in enumerate(items, start=1):
        def fmt(t):
            h = int(t // 3600)
            m = int((t % 3600) // 60)
            s = int(t % 60)
            ms = int((t - int(t)) * 1000)
            return f"{h:02}:{m:02}:{s:02},{ms:03}"

        lines.append(str(idx))
        lines.append(f"{fmt(it['start_time'])} --> {fmt(it['end_time'])}")
        lines.append(it["text"])
        lines.append("")

    with open(out_dir / "segments.srt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    ap = argparse.ArgumentParser(description="30s audio -> sentences -> clips -> JSON")
    ap.add_argument("--audio_path", required=True, help="Path to input audio (<=30s recommended)")
    ap.add_argument("--out_dir", default="output", help="Output directory")
    ap.add_argument("--language", default=None, help="Force language code (e.g., ja, zh, vi, en). Omit to auto-detect.")
    ap.add_argument("--model_size", default="small", help="Whisper model size: tiny|base|small|medium|large-v3")
    ap.add_argument("--device", default="cpu", help="cpu or cuda")
    ap.add_argument("--compute_type", default="int8", help="int8|int8_float16|float16|float32 (choose per hardware)")
    ap.add_argument("--gap_threshold", type=float, default=0.8, help="Seconds of silence to split when punctuation missing")
    ap.add_argument("--export_srt", action="store_true", help="Also write /output/segments.srt")
    args = ap.parse_args()

    audio_path = Path(args.audio_path).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[1/5] Transcribing with faster-whisper (word timestamps)...")
    words, segs, info = transcribe(audio_path, args.model_size, args.device, args.compute_type, language=args.language)
    print(f"   Detected language={getattr(info, 'language', 'n/a')}  |  duration~{getattr(info, 'duration', 'n/a')}s")
    print(f"   Words={len(words)} | Segments={len(segs)}")

    print("[2/5] Grouping into sentences...")
    sentences = words_to_sentences(words, gap_threshold=args.gap_threshold, max_chars=80)
    print(f"   Sentences={len(sentences)}")

    print("[3/5] Loading original audio...")
    audio = load_audio(audio_path)

    print("[4/5] Exporting clips...")
    items = export_clips(audio, sentences, out_dir)

    print("[5/5] Writing JSON...")
    write_json(items, out_dir)
    maybe_write_srt(items, out_dir, export=args.export_srt)

    print(f"Done. See: segments.json and segments folder in output directory")

if __name__ == "__main__":
    main()
