#!/usr/bin/env python3
"""Labelled contact sheet from stills, or from frames pulled out of a video at chosen times.

Examples:
  python contact_sheet.py sheet.png stills/*.png --cols 4
  python contact_sheet.py sheet.png --video preview.mp4 --every 1.0 --cols 6
  python contact_sheet.py sheet.png --video preview.mp4 --times 0.5,2.25,4.0

Needs: Pillow (optional dependency, checked at run time); ffmpeg on PATH for --video.
Each tile is labelled with its file name or its timestamp, so notes can point at an exact frame.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile


def need_pillow():
    try:
        from PIL import Image, ImageDraw  # noqa: F401
        return Image, ImageDraw
    except ImportError:
        sys.exit("Missing optional dependency 'Pillow' (used to draw the sheet). Install: python -m pip install Pillow")


def duration_of(video):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", video],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        sys.exit(f"ffprobe could not read the duration of {video}: {r.stderr.strip()}")


def grab_frames(video, times, outdir):
    files = []
    for t in times:
        f = os.path.join(outdir, f"t{t:09.3f}.png")
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", f],
                           capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(f):
            print(f"warning: no frame at {t:.3f}s ({r.stderr.strip()})", file=sys.stderr)
            continue
        files.append((f, f"{t:.2f}s"))
    return files


def main():
    ap = argparse.ArgumentParser(description="Labelled contact sheet from stills or video frames.")
    ap.add_argument("out", help="output image (png/jpg)")
    ap.add_argument("images", nargs="*", help="input stills (ignored with --video)")
    ap.add_argument("--video", help="pull frames from this video instead of using stills")
    ap.add_argument("--every", type=float, help="with --video: one frame every N seconds")
    ap.add_argument("--times", help="with --video: comma-separated seconds, e.g. 0.5,2.25,4")
    ap.add_argument("--cols", type=int, default=4, help="tiles per row (default 4)")
    ap.add_argument("--width", type=int, default=640, help="tile width in px (default 640)")
    a = ap.parse_args()

    Image, ImageDraw = need_pillow()
    tmp = None
    if a.video:
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            sys.exit("ffmpeg/ffprobe not found on PATH (needed for --video).")
        if a.times:
            times = [float(x) for x in a.times.split(",") if x.strip()]
        else:
            step = a.every or 1.0
            d = duration_of(a.video)
            times, t = [], step / 2
            while t < d:
                times.append(round(t, 3)); t += step
        tmp = tempfile.mkdtemp(prefix="sheet_")
        items = grab_frames(a.video, times, tmp)
    else:
        items = [(f, os.path.basename(f)) for f in a.images]
    if not items:
        sys.exit("no images to place on the sheet")

    tiles = []
    for f, label in items:
        im = Image.open(f).convert("RGB")
        im = im.resize((a.width, max(1, int(im.height * a.width / im.width))), Image.LANCZOS)
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 8 + 7 * len(label), 22], fill=(0, 0, 0))
        d.text((6, 5), label, fill=(255, 255, 255))
        tiles.append(im)
    H = max(t.height for t in tiles)
    rows = (len(tiles) + a.cols - 1) // a.cols
    pad = 6
    sheet = Image.new("RGB", (a.cols * a.width + (a.cols + 1) * pad, rows * H + (rows + 1) * pad), (128, 128, 128))
    for i, t in enumerate(tiles):
        sheet.paste(t, (pad + (i % a.cols) * (a.width + pad), pad + (i // a.cols) * (H + pad)))
    sheet.save(a.out)
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"{a.out} {sheet.size[0]}x{sheet.size[1]} tiles={len(tiles)}")


if __name__ == "__main__":
    main()
