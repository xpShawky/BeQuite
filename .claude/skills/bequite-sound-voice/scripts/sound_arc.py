# Plot the sound arc of several films: total loudness, kick band (35-130 Hz) and hats band (5-12 kHz), 0.1 s windows.
#   python sound_arc.py out.png film1.mp4 label1 film2.mp4 label2 ...
import sys, subprocess, numpy as np
from scipy.signal import butter, sosfiltfilt
from PIL import Image, ImageDraw, ImageFont
SR = 22050
def dec(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)
def rms(x, w): n = len(x) // w; return np.sqrt(np.mean(x[:n*w].reshape(n, w) ** 2, axis=1) + 1e-12)
def bp(x, lo, hi):
    sos = butter(4, [lo, hi], btype="band", fs=SR, output="sos"); return sosfiltfilt(sos, x)
out, items = sys.argv[1], list(zip(sys.argv[2::2], sys.argv[3::2]))
W, RH = 1800, 230; img = Image.new("RGB", (W, RH * len(items)), (12, 12, 14)); d = ImageDraw.Draw(img)
try:
    f = ImageFont.truetype("arial.ttf", 20)
except OSError:
    f = ImageFont.load_default()
for k, (p, lab) in enumerate(items):
    x = dec(p); w = int(SR * 0.1); dur = len(x) / SR
    tot, kick, hat = [20 * np.log10(rms(s, w)) for s in (x, bp(x, 35, 130), bp(x, 5000, 11000))]
    y0 = k * RH; sx = (W - 80) / dur
    for t in range(0, int(dur) + 1, 5):
        X = 60 + t * sx; d.line([(X, y0 + 30), (X, y0 + RH - 10)], fill=(40, 40, 46)); d.text((X + 2, y0 + RH - 30), f"{t}s", font=f, fill=(110, 110, 120))
    for arr, col in ((tot, (230, 230, 235)), (kick, (255, 170, 40)), (hat, (90, 200, 255))):
        pts = [(60 + i * 0.1 * sx, y0 + RH - 15 - max(0, (v + 70)) / 70 * (RH - 50)) for i, v in enumerate(arr)]
        d.line(pts, fill=col, width=2)
    d.text((10, y0 + 6), f"{lab}   (white = loudness, orange = kick/low drums, blue = hats/cymbals)", font=f, fill=(255, 220, 120))
img.save(out); print("ok")
