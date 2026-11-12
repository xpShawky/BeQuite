#!/usr/bin/env python3
"""Timestamped transcript of a film's voice-over / dialogue / lyrics, for studying references.

Examples:
  python transcribe.py film.mp4 out/transcript.md
  python transcribe.py film.mp4 out/transcript.md --model large-v3-turbo --device cuda --start 0 --end 600
  python transcribe.py --batch list.txt          # each line: <video>|<output.md>[|start|end]

Needs: faster-whisper (optional dependency, checked at run time; use an existing install, do not
pip-install it blindly), ffmpeg on PATH. On Windows with pip-installed nvidia-cublas/cudnn wheels,
their DLL folders are added to PATH automatically so --device cuda works.
Writes one line per segment: `[mm:ss.s-mm:ss.s] text`, plus the detected language. Music-only
films come back empty or with hallucinated filler: treat lines with low confidence as UNVERIFIED.
"""
import argparse
import os
import site
import subprocess
import sys
from pathlib import Path


def add_cuda_dlls():
    dirs = []
    for sp in site.getsitepackages() + [site.getusersitepackages()]:
        nv = Path(sp) / "nvidia"
        if nv.is_dir():
            dirs += [p for p in nv.glob("*/bin") if p.is_dir()]
    for d in dirs:
        os.environ["PATH"] = str(d) + os.pathsep + os.environ.get("PATH", "")
        if hasattr(os, "add_dll_directory"):
            try:
                os.add_dll_directory(str(d))
            except OSError:
                pass


def ts(s):
    return f"{int(s // 60):02d}:{s % 60:04.1f}"


def load_model(name, device):
    add_cuda_dlls()
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Missing optional dependency 'faster-whisper'. Point this script at a Python that already has it.")
    root = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~/.cache")), "faster-whisper")
    ctype = "float16" if device == "cuda" else "int8"
    return WhisperModel(name, device=device, compute_type=ctype, download_root=root)


def audio_slice(video, start, end):
    """Decode to 16 kHz mono float32 with ffmpeg (handles any container, honours start/end)."""
    import numpy as np
    cmd = ["ffmpeg", "-v", "error"]
    if start:
        cmd += ["-ss", str(start)]
    cmd += ["-i", video]
    if end:
        cmd += ["-t", str(end - (start or 0))]
    cmd += ["-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def run_one(model, video, out, start=0.0, end=None, lang=None):
    audio = audio_slice(video, start, end)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    if audio.size < 16000:
        Path(out).write_text(f"# Transcript: {Path(video).name}\n\n(no audio)\n", encoding="utf-8")
        return 0
    segs, info = model.transcribe(audio, language=lang, vad_filter=True, beam_size=5,
                                  condition_on_previous_text=False)
    lines = [f"# Transcript: {Path(video).name}", "",
             f"Language: {info.language} ({info.language_probability:.2f}) · offset {start:.1f} s · model output, check names and numbers", ""]
    n = 0
    for s in segs:
        flag = " (low confidence)" if s.avg_logprob < -1.0 or s.no_speech_prob > 0.6 else ""
        lines.append(f"[{ts(s.start + start)}-{ts(s.end + start)}] {s.text.strip()}{flag}")
        n += 1
    if n == 0:
        lines.append("(no speech detected: music / SFX only)")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", nargs="?")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--batch")
    ap.add_argument("--model", default="large-v3-turbo")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--lang", default=None)
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    a = ap.parse_args()
    model = load_model(a.model, a.device)
    jobs = []
    if a.batch:
        for line in Path(a.batch).read_text(encoding="utf-8").splitlines():
            if line.strip():
                p = line.split("|")
                jobs.append((p[0], p[1], float(p[2]) if len(p) > 2 and p[2] else 0.0,
                             float(p[3]) if len(p) > 3 and p[3] else None))
    else:
        if not (a.video and a.out):
            ap.error("give VIDEO OUT or --batch")
        jobs.append((a.video, a.out, a.start, a.end))
    for v, o, s, e in jobs:
        try:
            n = run_one(model, v, o, s, e, a.lang)
            print(f"ok {n:4d} segments  {o}", flush=True)
        except Exception as ex:  # keep the batch going; report the failure
            print(f"FAIL {v}: {ex}", flush=True)


if __name__ == "__main__":
    main()
