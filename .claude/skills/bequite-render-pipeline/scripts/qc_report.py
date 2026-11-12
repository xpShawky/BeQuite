#!/usr/bin/env python3
"""Delivery QC for a rendered video: format, black frames, frozen frames, loudness, true peak.
Prints (and optionally appends to evidence.md) a Markdown block with every command, its exit code and the key output
lines, plus PASS / FAIL per check. Python standard library only; needs ffmpeg + ffprobe on PATH.

Examples:
  python qc_report.py final_2k.mp4 --expect-size 2560x1440 --expect-fps 60
  python qc_report.py reel_9x16.mp4 --expect-size 1080x1920 --allow-black-tail 1.0 --evidence .bequite/work/0007-film/evidence.md
  python qc_report.py silent_preview.mp4 --no-audio

Loudness targets default to -14 LUFS integrated (+/- 1 LU) and <= -1.0 dBTP (bequite-sound-voice owns the target).
"""
import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout, r.stderr


def q(cmd):
    return " ".join(f'"{c}"' if any(ch in c for ch in " ;,:=") else c for c in cmd)


def main():
    ap = argparse.ArgumentParser(description="Delivery QC report (ffmpeg/ffprobe) with command + output evidence.")
    ap.add_argument("video")
    ap.add_argument("--expect-size", help="WxH, e.g. 2560x1440")
    ap.add_argument("--expect-fps", type=float, help="e.g. 60")
    ap.add_argument("--lufs", type=float, default=-14.0, help="integrated loudness target (default -14)")
    ap.add_argument("--lufs-tol", type=float, default=1.0, help="allowed +/- LU (default 1.0)")
    ap.add_argument("--tp", type=float, default=-1.0, help="max true peak dBTP (default -1.0)")
    ap.add_argument("--black-min", type=float, default=0.2, help="min black run to report, s (default 0.2)")
    ap.add_argument("--black-pix", type=float, default=0.05, help="blackdetect pix_th (default 0.05)")
    ap.add_argument("--allow-black-head", type=float, default=0.0, help="black allowed at the very start, s")
    ap.add_argument("--allow-black-tail", type=float, default=0.0, help="black allowed at the very end (fade out), s")
    ap.add_argument("--freeze", type=float, default=0.0, help="report frozen runs longer than N s (0 = skip; holds are often intended)")
    ap.add_argument("--no-audio", action="store_true", help="skip loudness checks (silent previews)")
    ap.add_argument("--evidence", help="append the Markdown block to this file (e.g. the work folder's evidence.md)")
    a = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found on PATH. Install ffmpeg (https://ffmpeg.org/download.html) and retry.")

    lines = [f"### QC: `{a.video}`", f"_{datetime.datetime.now().isoformat(timespec='seconds')}_", ""]
    results = []

    def check(name, ok, detail):
        results.append((name, ok, detail))

    # 1) format
    cmd = ["ffprobe", "-v", "error", "-show_entries",
           "format=duration,bit_rate:stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
           "-of", "json", a.video]
    rc, out, err = run(cmd)
    lines += ["```", f"$ {q(cmd)}", f"exit {rc}"]
    if rc != 0:
        lines += [err.strip(), "```"]
        print("\n".join(lines)); sys.exit(2)
    info = json.loads(out)
    dur = float(info.get("format", {}).get("duration", 0) or 0)
    v = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    au = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)
    if v:
        num, den = (v.get("r_frame_rate", "0/1").split("/") + ["1"])[:2]
        fps = float(num) / float(den or 1) if float(den or 1) else 0.0
        lines.append(f"video {v.get('codec_name')} {v.get('width')}x{v.get('height')} {fps:.3f} fps {v.get('pix_fmt')}")
    if au:
        lines.append(f"audio {au.get('codec_name')} {au.get('sample_rate')} Hz {au.get('channels')} ch")
    lines += [f"duration {dur:.3f} s", "```"]
    if not v:
        check("video stream", False, "no video stream")
    else:
        if a.expect_size:
            ok = f"{v.get('width')}x{v.get('height')}" == a.expect_size
            check("size", ok, f"{v.get('width')}x{v.get('height')} (expected {a.expect_size})")
        if a.expect_fps:
            ok = abs(fps - a.expect_fps) < 0.01
            check("fps", ok, f"{fps:.3f} (expected {a.expect_fps})")
        if v.get("pix_fmt") not in ("yuv420p", "yuvj420p"):
            check("pix_fmt", False, f"{v.get('pix_fmt')} (social players expect yuv420p)")
        else:
            check("pix_fmt", True, "yuv420p")

    # 2) black frames
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", a.video, "-vf",
           f"blackdetect=d={a.black_min}:pix_th={a.black_pix}", "-an", "-f", "null", "-"]
    rc, out, err = run(cmd)
    runs = [(float(m.group(1)), float(m.group(2))) for m in re.finditer(r"black_start:([\d.]+)\s+black_end:([\d.]+)", err)]
    bad = [(s, e) for s, e in runs
           if not (s <= 0.01 and e <= a.allow_black_head + 0.01) and not (e >= dur - 0.05 and s >= dur - a.allow_black_tail - 0.01)]
    lines += ["```", f"$ {q(cmd)}", f"exit {rc}"] + [f"black {s:.2f}-{e:.2f} s" for s, e in runs] + (["no black runs"] if not runs else []) + ["```"]
    check("black frames", rc == 0 and not bad, "none outside allowed head/tail" if not bad else f"unexpected black: {bad}")

    # 3) frozen frames (optional)
    if a.freeze > 0:
        cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", a.video, "-vf", f"freezedetect=n=0.001:d={a.freeze}", "-an", "-f", "null", "-"]
        rc, out, err = run(cmd)
        fr = re.findall(r"freeze_start: ([\d.]+).*?freeze_end: ([\d.]+)", err, re.S)
        lines += ["```", f"$ {q(cmd)}", f"exit {rc}"] + [f"frozen {s}-{e} s" for s, e in fr] + (["no frozen runs"] if not fr else []) + ["```"]
        check(f"frozen > {a.freeze}s", rc == 0 and not fr, "none" if not fr else f"{len(fr)} run(s): review if unintended")

    # 4) loudness
    if not a.no_audio:
        if not au:
            check("audio stream", False, "no audio stream (use --no-audio for silent previews)")
        else:
            cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", a.video, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]
            rc, out, err = run(cmd)
            summary = err[err.rfind("Summary:"):] if "Summary:" in err else ""
            mI = re.search(r"I:\s+(-?[\d.]+) LUFS", summary)
            mL = re.search(r"LRA:\s+(-?[\d.]+) LU", summary)
            mP = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf) dBFS", summary)
            lines += ["```", f"$ {q(cmd)}", f"exit {rc}"] + [l.strip() for l in summary.splitlines() if l.strip() and not l.strip().startswith("[")][:12] + ["```"]
            if mI:
                I = float(mI.group(1))
                check("integrated loudness", abs(I - a.lufs) <= a.lufs_tol, f"{I:.1f} LUFS (target {a.lufs} +/- {a.lufs_tol})")
            else:
                check("integrated loudness", False, "could not parse ebur128 summary")
            if mP and mP.group(1) != "-inf":
                P = float(mP.group(1))
                check("true peak", P <= a.tp, f"{P:.1f} dBTP (max {a.tp})")
            elif mP:
                check("true peak", True, "-inf (silent)")
            if mL:
                lines.append(f"LRA {mL.group(1)} LU")

    # summary
    lines += ["", "| Check | Result | Detail |", "|---|---|---|"]
    for name, ok, detail in results:
        lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {detail} |")
    overall = all(ok for _, ok, _ in results) and bool(results)
    lines += ["", f"**QC overall: {'PASS' if overall else 'FAIL'}** (automated checks only; phone readability, "
              "banding and honesty checks are visual and listed in qc-checklist.md)", ""]
    text = "\n".join(lines)
    print(text)
    if a.evidence:
        with open(a.evidence, "a", encoding="utf-8") as f:
            f.write("\n" + text + "\n")
        print(f"(appended to {a.evidence})")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()
