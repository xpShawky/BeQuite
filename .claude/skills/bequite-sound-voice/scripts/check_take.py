#!/usr/bin/env python3
"""Check voice takes against the script with speech-to-text: missing / repeated / extra words (e.g. a direction tag read
aloud), long gaps, duration. Optionally saves word timings (JSON) and captions (SRT) for each take.

Examples:
  python check_take.py --script script.txt takes/                      # every audio file in the folder
  python check_take.py --script script.txt take_a.wav take_b.wav --words-dir words/ --srt
  python check_take.py --script script.txt take.wav --prompt "BrandName, ProductName" --aliases aliases.json

Needs: ffmpeg; numpy; faster-whisper (optional dependency, only this script: python -m pip install faster-whisper).
Any word-timestamp STT can replace faster-whisper; the rest of the pipeline only reads the words JSON
([{"w": word, "s": start_s, "e": end_s}, ...]).
Run it on raw takes, and again after placement (placed audio must still say every word).
"""
import argparse
import difflib
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _audio as A  # noqa: E402

AUDIO_EXT = (".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac", ".aiff", ".aif")


def collect(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for f in sorted(glob.glob(os.path.join(p, "*"))):
                if f.lower().endswith(AUDIO_EXT) and not os.path.basename(f).startswith("_"):
                    out.append(f)
        elif os.path.exists(p):
            out.append(p)
        else:
            print(f"warning: not found: {p}", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser(description="Speech-to-text check of voice takes against the script.")
    ap.add_argument("takes", nargs="+", help="audio files and/or folders")
    ap.add_argument("--script", required=True, help="script text, one line per VO line ([tags] are ignored)")
    ap.add_argument("--model", default="small", help="faster-whisper model (default small)")
    ap.add_argument("--language", default="en", help="language code (default en; e.g. ar)")
    ap.add_argument("--prompt", default=None, help="names to spell right (initial prompt). Omit to hear what was really said")
    ap.add_argument("--aliases", help='JSON map for token matching, e.g. {"acme cloud": "acmecloud", "2": "two"}')
    ap.add_argument("--gap", type=float, default=0.9, help="report pauses longer than N s (default 0.9)")
    ap.add_argument("--words-dir", help="save <take>.json word timings here")
    ap.add_argument("--srt", action="store_true", help="also save <take>.srt captions (needs --words-dir)")
    ap.add_argument("--report", help="write a JSON report here")
    a = ap.parse_args()

    A.need_ffmpeg()
    A.np()  # numpy is needed by A.load()
    fw = A.need("faster_whisper", "faster-whisper", "speech-to-text")
    aliases = A.load_aliases(a.aliases)
    ref = A.tokens(" ".join(A.script_lines(a.script)), aliases)
    files = collect(a.takes)
    if not files:
        sys.exit("no audio takes found")
    if a.srt and not a.words_dir:
        sys.exit("--srt needs --words-dir")
    if a.words_dir:
        os.makedirs(a.words_dir, exist_ok=True)

    model = fw.WhisperModel(a.model, device="cpu", compute_type="int8")
    rep = {}
    for f in files:
        x = A.load(f, sr=16000, ch=1)
        segs, _ = model.transcribe(x, word_timestamps=True, language=a.language, initial_prompt=a.prompt)
        ws = [w for s in segs for w in s.words]
        words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for w in ws]
        hyp = A.tokens(" ".join(w["w"] for w in words), aliases)
        sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
        diffs = [{"op": op, "script": " ".join(ref[i1:i2]), "heard": " ".join(hyp[j1:j2])}
                 for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
        gaps = [(round(words[i]["e"], 2), round(words[i + 1]["s"] - words[i]["e"], 2))
                for i in range(len(words) - 1) if words[i + 1]["s"] - words[i]["e"] > a.gap]
        k = os.path.splitext(os.path.basename(f))[0]
        rep[k] = {"file": f, "dur": round(len(x) / 16000, 2), "match": round(sm.ratio(), 3), "diffs": diffs, "gaps": gaps}
        print(f"\n{k}: {rep[k]['dur']} s  match {rep[k]['match']}")
        for d in diffs:
            print(f"  {d['op']:8s} script: '{d['script']}'  heard: '{d['heard']}'")
        if gaps:
            print(f"  pauses > {a.gap}s at: {gaps}")
        if a.words_dir:
            wj = os.path.join(a.words_dir, k + ".json")
            with open(wj, "w", encoding="utf-8") as fh:
                json.dump(words, fh, ensure_ascii=False, indent=0)
            print(f"  words -> {wj}")
            if a.srt:
                sp = os.path.join(a.words_dir, k + ".srt")
                with open(sp, "w", encoding="utf-8") as fh:
                    fh.write(A.words_to_srt(words))
                print(f"  captions -> {sp}")
    if a.report:
        with open(a.report, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, ensure_ascii=False, indent=1)
        print(f"\nreport -> {a.report}")


if __name__ == "__main__":
    main()
