#!/usr/bin/env python3
"""Check a content package against the platform matrix before it goes to the owner for approval.

A package is a folder:
  package.json   {"id", "title", "platforms": ["telegram","instagram","youtube","tiktok"], "video": "final.mp4" (optional
                  until produced), "duration_s", "captions": "captions.srt", "texts": {"telegram": "...", "instagram": "...",
                  "youtube_title": "...", "youtube_description": "...", "tiktok": "..."}, "synthetic_media": false,
                  "claims": [{"text": "...", "source": "https://..."}]}
  captions.srt   timed captions

  python package_check.py PACKAGE_DIR

Prints one line per check (ok / FAIL / warn) and exits 1 on any FAIL. It never posts anything.
Limits come from references/platform-matrix.md (read 2026-11-21).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

LIMITS = {
    "telegram_caption": 1024, "telegram_video_mb": 50,
    "youtube_title": 100, "shorts_max_s": 180, "reels_max_s": 180,
    "instagram_caption": 2200, "instagram_hashtags": 30,
}


def probe(video):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=width,height:format=duration,size", "-of", "json", str(video)],
                             capture_output=True, text=True, timeout=60).stdout
        j = json.loads(out)
        s = (j.get("streams") or [{}])[0]
        f = j.get("format") or {}
        return float(f.get("duration", 0)), int(f.get("size", 0)), s.get("width"), s.get("height")
    except Exception:
        return None


def srt_ok(path):
    t = path.read_text(encoding="utf-8")
    cues = re.findall(r"(\d\d):(\d\d):(\d\d),(\d{3}) --> (\d\d):(\d\d):(\d\d),(\d{3})", t)
    if not cues:
        return False, "no cues"
    last = 0.0
    for c in cues:
        a = int(c[0]) * 3600 + int(c[1]) * 60 + int(c[2]) + int(c[3]) / 1000
        b = int(c[4]) * 3600 + int(c[5]) * 60 + int(c[6]) + int(c[7]) / 1000
        if b <= a or a < last - 0.001:
            return False, f"cue at {a:.2f}s overlaps or ends before it starts"
        last = b
    return True, f"{len(cues)} cues, ends at {last:.1f}s"


def main():
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if len(sys.argv) == 2 else 2)
    d = Path(sys.argv[1])
    if not (d / "package.json").is_file():
        print(f"FAIL  {d / 'package.json'} not found (a package is a folder with package.json)")
        sys.exit(1)
    p = json.loads((d / "package.json").read_text(encoding="utf-8"))
    res = []

    def check(ok, msg, level="FAIL"):
        res.append(("ok" if ok else level, msg))

    texts = p.get("texts", {})
    plats = p.get("platforms", [])
    dur = p.get("duration_s")
    if "telegram" in plats:
        n = len(texts.get("telegram", ""))
        check(0 < n <= LIMITS["telegram_caption"], f"telegram caption {n} chars (max {LIMITS['telegram_caption']})")
    if "instagram" in plats:
        cap = texts.get("instagram", "")
        check(0 < len(cap) <= LIMITS["instagram_caption"], f"instagram caption {len(cap)} chars (max {LIMITS['instagram_caption']}, UNVERIFIED limit)", "warn")
        tags = len(re.findall(r"#\w+", cap))
        check(tags <= LIMITS["instagram_hashtags"], f"instagram hashtags {tags} (max {LIMITS['instagram_hashtags']}, UNVERIFIED limit)", "warn")
    if "youtube" in plats:
        n = len(texts.get("youtube_title", ""))
        check(0 < n <= LIMITS["youtube_title"], f"youtube title {n} chars (max {LIMITS['youtube_title']})")
        check(bool(texts.get("youtube_description")), "youtube description present")
    if dur is not None:
        check(dur <= LIMITS["shorts_max_s"], f"duration {dur}s fits Shorts/Reels (<= {LIMITS['shorts_max_s']}s)")
    cap = d / p.get("captions", "captions.srt")
    if cap.exists():
        ok, msg = srt_ok(cap)
        check(ok, f"captions: {msg}")
    else:
        check(False, "captions file missing")
    for c in p.get("claims", []):
        check(bool(re.match(r"https?://", c.get("source", ""))), f"claim has a source: {c.get('text', '')[:50]}")
    check("synthetic_media" in p, "synthetic_media declared (YouTube containsSyntheticMedia)")
    vid = p.get("video")
    if vid and (d / vid).exists():
        pr = probe(d / vid)
        if pr:
            vdur, size, w, h = pr
            check(h and w and h >= w, f"video vertical or square ({w}x{h})")
            if "telegram" in plats:
                check(size <= LIMITS["telegram_video_mb"] * 1024 * 1024, f"video {size / 1048576:.1f} MB (telegram max 50)")
            check(vdur <= LIMITS["shorts_max_s"], f"video {vdur:.1f}s (max {LIMITS['shorts_max_s']})")
    else:
        res.append(("warn", "no video yet: package is a pre-production draft"))
    appr = d / "APPROVAL.md"
    check(appr.exists() and "PENDING" in appr.read_text(encoding="utf-8") or appr.exists() and "APPROVED" in appr.read_text(encoding="utf-8"),
          "APPROVAL.md present (PENDING until the owner says yes)")
    for lvl, msg in res:
        print(f"{lvl:4}  {msg}")
    fails = sum(1 for l, _ in res if l == "FAIL")
    print(f"\n{len(res) - fails}/{len(res)} checks not failing")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
