#!/usr/bin/env python3
"""Format DNA: measure the form of the top videos in a niche and aggregate it into numbers.

For each URL it runs the video ladder (bequite-video-intel/scripts/watch.py): L0 metadata,
L1 captions in the given language (falls back to nothing, never a wildcard), L3 full at low
resolution + film_study.py. Then it measures what a producer needs:

  hook      words spoken in the first 3 s, first caption line, first-3-s frame strip (0-3 s, 0.5 s step)
  pace      speaking rate (words per second over the spoken span), cuts per minute, mean / median shot,
            pacing by quarter, longest hold
  sound     loudness (LUFS, LRA), music vs voice share, silences, what sound sits on the cuts
  shape     length, aspect, ending (last caption line), CTA words in the last 15% of the transcript

  python dna.py measure OUT URL [URL ...] --lang ar-orig [--height 360] [--py PYTHON]
  python dna.py sheet OUT              # aggregate OUT/*/dna.json into OUT/format-sheet-data.md

Visual style (caption position, words per caption, colours) is read by eye from each
video's first3s.jpg and study/shots.jpg and written into the sheet by hand; this script
puts the frames in front of you, it does not guess them.
"""
import argparse
import json
import re
import statistics as st
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
WATCH = HERE.parents[1] / "bequite-video-intel" / "scripts" / "watch.py"
CTA = ["تابع", "اشترك", "لايك", "كومنت", "اكتب", "احفظ", "شير", "follow", "subscribe", "comment", "link", "اللينك", "الرابط", "الوصف"]


def run(cmd, timeout=1800):
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def vid_id(url):
    m = re.search(r"(?:v=|shorts/|youtu\.be/|video/)([\w-]{6,})", url)
    return m.group(1) if m else re.sub(r"\W+", "_", url)[-20:]


def parse_transcript(path):
    lines = []
    if not path.exists():
        return lines
    for l in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\[(\d+):(\d+(?:\.\d+)?)(?:-[\d:.]+)?\]\s*(.*)", l)
        if m:
            lines.append((int(m[1]) * 60 + float(m[2]), m[3].replace("(low confidence)", "").strip()))
    return lines


def measure_one(a, url, out):
    d = out / vid_id(url)
    d.mkdir(parents=True, exist_ok=True)
    py = [a.py, "-P", "-E", str(Path(a.watch) if a.watch else WATCH)]
    run(py + ["meta", url, str(d)])
    run(py + ["captions", url, str(d), "--lang", a.lang])
    time.sleep(a.pause)
    run(py + ["full", url, str(d), "--height", str(a.height), "--study", "--py", a.py])
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else {}
    study = json.loads((d / "study" / "metrics.json").read_text(encoding="utf-8")) if (d / "study" / "metrics.json").exists() else {}
    tr = parse_transcript(d / "transcript.md")
    pic, snd = study.get("picture") or {}, study.get("sound") or {}
    dur = float(meta.get("duration") or (study.get("meta") or {}).get("duration") or 0)
    words = [(t, w) for t, line in tr for w in line.split()]
    spoken = (tr[-1][0] - tr[0][0]) if len(tr) > 1 else 0
    hook = " ".join(line for t, line in tr if t < 3.0)
    tail_from = dur * 0.85 if dur else 0
    tail = " ".join(line for t, line in tr if t >= tail_from)
    vid = next(iter(sorted(d.glob("full.*"))), None)
    if vid:
        run(["ffmpeg", "-v", "error", "-y", "-i", str(vid), "-vf",
             "select='lte(t\\,3)',fps=2,scale=240:-2,tile=7x1", "-frames:v", "1", str(d / "first3s.jpg")])
    shots = study.get("shots") or []
    lens = [s.get("len") or 0 for s in shots]
    res = {
        "url": url, "title": meta.get("title"), "channel": meta.get("channel"), "upload_date": meta.get("upload_date"),
        "views": meta.get("view_count"), "likes": meta.get("like_count"), "comments": meta.get("comment_count"),
        "duration_s": dur, "vertical": meta.get("vertical"),
        "hook_words_first3s": len(hook.split()), "hook_text_first3s": hook,
        "first_caption": tr[0][1] if tr else None, "first_caption_at": tr[0][0] if tr else None,
        "speech_words": len(words), "words_per_second": round(len(words) / spoken, 2) if spoken else None,
        "cuts_per_min": pic.get("cuts_per_min"), "shots": pic.get("shots"),
        "pacing_by_quarter": pic.get("avg_shot_by_quarter"), "camera_time_pct": pic.get("camera_time_pct"),
        "shot_mean_s": round(st.mean(lens), 2) if lens else None, "shot_median_s": round(st.median(lens), 2) if lens else None,
        "longest_hold_s": round(max(lens), 2) if lens else None,
        "lufs": (snd.get("loudness") or {}).get("integrated_lufs"), "lra": (snd.get("loudness") or {}).get("lra_lu"),
        "harmonic_share": snd.get("harmonic_share_when_audible"), "percussive_hits_per_s": snd.get("percussive_hits_per_sec"),
        "cuts_on_onset_frac": snd.get("cuts_on_onset_frac"), "sound_at_cuts": snd.get("sound_at_cuts"),
        "silences": snd.get("silences"),
        "cta_in_last_15pct": [w for w in CTA if w in tail.lower()], "last_line": tr[-1][1] if tr else None,
    }
    (d / "dna.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("title", "duration_s", "hook_words_first3s", "words_per_second", "cuts_per_min", "shot_median_s", "lufs")}, ensure_ascii=False))


def cmd_sheet(a, out):
    rows = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(out.glob("*/dna.json"))]
    keys = ["duration_s", "views", "hook_words_first3s", "first_caption_at", "words_per_second", "cuts_per_min", "shots",
            "shot_mean_s", "shot_median_s", "longest_hold_s", "lufs", "lra", "harmonic_share", "percussive_hits_per_s",
            "cuts_on_onset_frac"]
    lines = [f"# Format data: {len(rows)} videos", "", "| measure | " + " | ".join((r.get('channel') or '?')[:18] for r in rows) + " | median |",
             "|---|" + "---|" * (len(rows) + 1)]
    for k in keys:
        vals = [r.get(k) for r in rows]
        nums = [v for v in vals if isinstance(v, (int, float))]
        lines.append(f"| {k} | " + " | ".join("" if v is None else str(v) for v in vals) + f" | {round(st.median(nums), 2) if nums else ''} |")
    lines += ["", "## Hooks (first 3 s, as spoken)", ""] + [f"- {r.get('channel')}: \"{r.get('hook_text_first3s')}\"" for r in rows]
    lines += ["", "## Endings (last line; CTA words in the last 15%)", ""] + [f"- {r.get('channel')}: \"{r.get('last_line')}\" {r.get('cta_in_last_15pct')}" for r in rows]
    (out / "format-sheet-data.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("measure")
    m.add_argument("out")
    m.add_argument("urls", nargs="+")
    m.add_argument("--lang", default="en")
    m.add_argument("--height", type=int, default=360)
    m.add_argument("--py", default=sys.executable)
    m.add_argument("--watch")
    m.add_argument("--pause", type=float, default=8.0, help="seconds between videos (caption rate limit)")
    s = sub.add_parser("sheet")
    s.add_argument("out")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.cmd == "measure":
        for u in a.urls:
            measure_one(a, u, out)
    else:
        cmd_sheet(a, out)


if __name__ == "__main__":
    main()
