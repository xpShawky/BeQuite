#!/usr/bin/env python3
"""Measure a reference film so its study rests on numbers, not impressions.

Finds every hard cut, then measures per shot (length, camera move, whether the move dies before
the cut), per cut (graphic / position-locked match, motion carried across the cut, flash or black),
and the sound (loudness, tempo, onsets, silences, sudden drops) and how the cuts sit on the sound.

Examples:
  python film_study.py film.mp4 out/
  python film_study.py event.mp4 out/ --start 0 --end 600      # study only the opening
  python film_study.py film.mp4 out/ --scene 0.25 --sheet-max 80

Writes into OUTDIR:
  summary.md    the numbers in a readable page (start here)
  metrics.json  everything, machine-readable
  shots.jpg     one labelled tile per shot (sampled when there are more than --sheet-max)
  matches.jpg   before|after pairs for the strongest match cuts (the "same place, new world" cuts)
  timeline.png  loudness, onsets and cuts on one time axis (see how picture sits on sound)

Needs: numpy, opencv-python, Pillow (optional dependencies, checked at run time) and ffmpeg/ffprobe.
Limits: dissolves, whip-pans and morphs are soft transitions; the detector catches hard cuts (and
very fast whips). Tempo is one global estimate. Treat every label as a pointer to look at, not a verdict.
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys

W, H = 160, 90          # analysis resolution
SR = 11025              # analysis sample rate
HOP = 256               # ~23 ms audio hop


def need():
    try:
        import numpy as np
        import cv2
        from PIL import Image, ImageDraw
        return np, cv2, Image, ImageDraw
    except ImportError as e:
        sys.exit(f"Missing optional dependency ({e.name}). Install numpy, opencv-python and Pillow first.")


np, cv2, Image, ImageDraw = need()


def probe(video):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate:format=duration", "-of", "json", video],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    j = json.loads(r.stdout or "{}")
    st = (j.get("streams") or [{}])[0]
    num, den = (st.get("r_frame_rate", "30/1").split("/") + ["1"])[:2]
    fps = float(num) / float(den or 1)
    return {"width": st.get("width"), "height": st.get("height"), "fps": round(fps, 3),
            "duration": float(j.get("format", {}).get("duration", 0))}


def ffin(video, start, end):
    cmd = ["ffmpeg", "-v", "error"]
    if start:
        cmd += ["-ss", f"{start}"]
    cmd += ["-i", video]
    if end:
        cmd += ["-t", f"{end - start}"]
    return cmd


# ---------------------------------------------------------------- picture

def edge_map(g):
    e = cv2.Canny(g, 60, 160).astype(np.float32)
    return cv2.GaussianBlur(e, (0, 0), 2.0)


def corr(a, b):
    a = a.ravel() - a.mean()
    b = b.ravel() - b.mean()
    d = math.sqrt(float((a * a).sum()) * float((b * b).sum()))
    return float((a * b).sum() / d) if d > 1e-6 else 0.0


def hsv_hist(rgb):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h = cv2.calcHist([hsv], [0, 1, 2], None, [8, 4, 4], [0, 180, 0, 256, 0, 256])
    return cv2.normalize(h, h).flatten()


def flow_stats(pg, g):
    f = cv2.calcOpticalFlowFarneback(pg, g, None, 0.5, 2, 9, 2, 5, 1.1, 0)
    fx, fy = f[..., 0], f[..., 1]
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    xs -= W / 2
    ys -= H / 2
    r2 = (xs * xs + ys * ys).mean()
    zoom = float((fx * xs + fy * ys).mean() / r2) * 100.0   # % scale change per frame (approx)
    return float(fx.mean()), float(fy.mean()), float(np.sqrt(fx * fx + fy * fy).mean()), zoom


def scan_picture(video, start, end, fps, thr):
    p = subprocess.Popen(ffin(video, start, end) + ["-an", "-vf", f"scale={W}:{H}:flags=area",
                         "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    size = W * H * 3
    prev = prev_g = prev_h = None
    prev_mafd = 0.0
    prev_hd = 0.0
    frames = []          # per frame: [score, dx, dy, mag, zoom, luma]
    cuts = []            # per cut: dict with frame index and the frames around it
    keep_before = []     # last few frames (rgb) for cut analysis
    pending = []         # cuts waiting for frames after them
    i = 0
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        rgb = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        hcur = hsv_hist(rgb)
        hd = float(cv2.compareHist(prev_h, hcur, cv2.HISTCMP_BHATTACHARYYA)) if prev_h is not None else 0.0
        score = 0.0
        dx = dy = mag = zoom = 0.0
        if prev is not None:
            mafd = float(np.abs(rgb.astype(np.int16) - prev.astype(np.int16)).mean())
            score = min(mafd, abs(mafd - prev_mafd)) / 100.0
            prev_mafd = mafd
            dx, dy, mag, zoom = flow_stats(prev_g, g)
        # second path: a colour swap at similar brightness (same layout, new colour) barely moves the pixel
        # score but jumps the colour histogram; skip very dark frames, where flicker would look the same
        hist_cut = hd >= 0.30 and abs(hd - prev_hd) >= 0.25 and float(g.mean()) > 25
        is_cut = prev is not None and (score >= thr or hist_cut) and (not cuts or i - cuts[-1]["f"] >= 2)
        if is_cut and score < thr:
            score = max(score, hd)
        prev_hd, prev_h = hd, hcur
        frames.append([score, dx, dy, mag, zoom, float(g.mean())])
        if is_cut:
            c = {"f": i, "score": score, "before": keep_before[-1].copy(), "after": None}
            cuts.append(c)
            pending.append(c)
        for c in pending:
            if c["after"] is None and i >= c["f"] + 1:   # one frame in, past any blend frame
                c["after"] = rgb.copy()
        pending = [c for c in pending if c["after"] is None]
        keep_before = (keep_before + [rgb.copy()])[-3:]
        prev, prev_g = rgb, g
        i += 1
    p.wait()
    for c in cuts:
        if c["after"] is None:
            c["after"] = prev
    return np.array(frames, dtype=np.float32) if frames else np.zeros((0, 6), np.float32), cuts


def classify_cut(c, fr):
    b, a = c["before"], c["after"]
    gb, ga = cv2.cvtColor(b, cv2.COLOR_RGB2GRAY), cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    edge = corr(edge_map(gb), edge_map(ga))
    tone = corr(cv2.GaussianBlur(gb, (0, 0), 3).astype(np.float32), cv2.GaussianBlur(ga, (0, 0), 3).astype(np.float32))
    colour = float(cv2.compareHist(hsv_hist(b), hsv_hist(a), cv2.HISTCMP_BHATTACHARYYA))
    f = c["f"]
    pre = fr[max(1, f - 4):f, 1:3]
    post = fr[f + 2:f + 5, 1:3]
    motion_cos = None
    if len(pre) and len(post):
        u, v = pre.mean(0), post.mean(0)
        nu, nv = np.linalg.norm(u), np.linalg.norm(v)
        if nu > 0.3 and nv > 0.3:
            motion_cos = float(u @ v / (nu * nv))
    lb, la = float(gb.mean()), float(ga.mean())
    tags = []
    match = max(edge, abs(tone))
    if colour >= 0.35 and match >= 0.45:
        tags.append("graphic-match")          # different world, same layout
    elif colour < 0.35 and edge >= 0.6:
        tags.append("same-setup")             # same scene re-cut (jump / punch-in)
    if abs(tone) >= 0.55 and colour >= 0.35:
        tags.append("position-locked")        # big shapes sit in the same place
    if motion_cos is not None and motion_cos > 0.8:
        tags.append("motion-carried")
    if la < 12 or lb < 12:
        tags.append("black")
    if la > 235 or lb > 235:
        tags.append("white-flash")
    return {"edge_sim": round(edge, 3), "tone_sim": round(tone, 3), "colour_change": round(colour, 3),
            "motion_cos": None if motion_cos is None else round(motion_cos, 2), "match_score": round(match * min(1.0, colour / 0.35), 3),
            "tags": tags}


def camera_label(seg):
    if len(seg) < 3:
        return "flash", 0.0, False
    dx, dy, mag, zoom = seg[:, 1].mean(), seg[:, 2].mean(), seg[:, 3].mean(), seg[:, 4].mean()
    n = len(seg)
    q = max(1, n // 5)
    mid = seg[q:n - q, 3].mean() if n > 2 * q else mag
    tail = seg[n - q:, 3].mean()
    dies = bool(mid > 0.35 and tail < 0.35 * mid)
    if mag < 0.12:
        lab = "locked-off"
    elif abs(zoom) > 0.25 and abs(zoom) * 2 > math.hypot(dx, dy):
        lab = "push-in" if zoom > 0 else "pull-out"
    elif math.hypot(dx, dy) > 0.25:
        lab = ("move-left" if dx > 0 else "move-right") if abs(dx) >= abs(dy) else ("move-up" if dy > 0 else "move-down")
    else:
        lab = "inner-motion"   # things move inside a roughly still frame
    return lab, float(mag), dies


# ---------------------------------------------------------------- sound

def scan_audio(video, start, end):
    raw = subprocess.run(ffin(video, start, end) + ["-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    if x.size < SR:
        return None
    n = 1 + (x.size - 1024) // HOP
    win = np.hanning(1024).astype(np.float32)
    rms, flux, low, high, bands = [], [], [], [], []
    prevmag = None
    freqs = np.fft.rfftfreq(1024, 1 / SR)
    lowb, highb = freqs < 150, freqs > 3000
    edges = np.geomspace(40, SR / 2, 49)                 # 48 log bands for the music/SFX split
    band_of = np.clip(np.searchsorted(edges, freqs) - 1, 0, 47)
    for s in range(0, n, 4096):                          # chunked STFT
        idx = np.arange(s, min(n, s + 4096))[:, None] * HOP + np.arange(1024)[None, :]
        fr = x[idx]
        rms.append(np.sqrt((fr * fr).mean(1) + 1e-12))
        spec = np.abs(np.fft.rfft(fr * win, axis=1))
        pw = spec * spec
        bp = np.zeros((pw.shape[0], 48), np.float32)
        for b in range(48):
            sel = band_of == b
            if sel.any():
                bp[:, b] = pw[:, sel].sum(1)
        bands.append(bp)
        mag = np.log1p(100 * spec)
        if prevmag is not None:
            d0 = mag[0] - prevmag
            d = np.vstack([d0[None], np.diff(mag, axis=0)])
        else:
            d = np.vstack([np.zeros((1, mag.shape[1])), np.diff(mag, axis=0)])
        d = np.maximum(d, 0)
        flux.append(d.mean(1))
        low.append(d[:, lowb].mean(1))
        high.append(d[:, highb].mean(1))
        prevmag = mag[-1]
    rms = np.concatenate(rms)
    bands = np.concatenate(bands)
    # Harmonic / percussive split (median filtering, Fitzgerald 2010): sustained energy along time is
    # music beds, pads and voice; energy spread across frequency in one instant is drums, hits, clicks.
    try:
        from scipy.ndimage import median_filter
        harm = median_filter(bands, size=(17, 1))
        perc = median_filter(bands, size=(1, 7))
        mask = perc / (perc + harm + 1e-12)
        perc_env = (bands * mask).sum(1)
        harm_env = (bands * (1 - mask)).sum(1)
    except ImportError:
        perc_env = harm_env = None
    return {"db": 20 * np.log10(rms), "flux": np.concatenate(flux), "low": np.concatenate(low),
            "high": np.concatenate(high), "dt": HOP / SR, "t0": 512 / SR, "perc": perc_env, "harm": harm_env}


def cut_sound(au, t, ref, booms, perc_pk):
    """What the sound does at one cut: boom, hit, whoosh into it, riser into it, cut to silence."""
    dt, db, hi = au["dt"], au["db"], au["high"]
    i = int(t / dt)
    if i <= 2 or i >= len(db) - 2:
        return []
    tags = []
    if len(booms) and np.min(np.abs(np.asarray(booms) - t)) <= 0.08:
        tags.append("boom")
    if len(perc_pk) and np.min(np.abs(perc_pk - t)) <= 0.07:
        tags.append("hit")
    w = int(0.35 / dt)
    pre = hi[max(0, i - w):i]
    if len(pre) > 4:
        base = np.median(hi[max(0, i - 6 * w):max(1, i - w)]) + 1e-9
        if pre[-len(pre) // 3:].mean() > 2.0 * base and pre[-len(pre) // 3:].mean() > pre[:len(pre) // 3].mean() * 1.5:
            tags.append("whoosh-in")
    r = int(2.5 / dt)
    if i - r > 0:
        seg = np.convolve(db[i - r:i], np.ones(9) / 9, mode="valid")
        if len(seg) > 10 and seg[-1] - seg[0] >= 6 and np.corrcoef(np.arange(len(seg)), seg)[0, 1] > 0.8:
            tags.append("riser-in")
    after = db[i:i + int(0.3 / dt)]
    before = db[max(0, i - int(0.3 / dt)):i]
    if len(after) and after.mean() < ref - 25 and before.mean() > ref - 15:
        tags.append("cut-to-silence")
    elif len(after) and len(before) and after.mean() - before.mean() > 10:
        tags.append("sound-slam")
    return tags


def peaks(env, dt, k=1.0, gap=0.07):
    w = max(3, int(1.0 / dt))
    kern = np.ones(w) / w
    base = np.convolve(env, kern, mode="same")
    thr = base + k * env.std()
    g = max(1, int(gap / dt))
    out = []
    for i in range(1, len(env) - 1):
        if env[i] > thr[i] and env[i] >= env[max(0, i - g):i + g + 1].max():
            if not out or i - out[-1] >= g:
                out.append(i)
    return np.array(out, dtype=int)


def tempo(env, dt):
    e = env - env.mean()
    lags = np.arange(int(60 / 200 / dt), int(60 / 60 / dt) + 1)
    if len(e) < lags[-1] * 3:
        return None, 0.0, None
    ac = np.array([float((e[:-l] * e[l:]).mean()) for l in lags])
    bpm = 60 / (lags * dt)
    weight = np.exp(-0.5 * (np.log2(bpm / 120) / 0.9) ** 2)
    score = ac * weight
    j = int(score.argmax())
    conf = float(ac[j] / (np.abs(ac).mean() + 1e-9))
    period = lags[j]
    phase = int(np.argmax([env[p::period].sum() for p in range(period)]))
    beats = np.arange(phase, len(env), period) * dt + 512 / SR
    return round(float(bpm[j]), 1), round(conf, 2), beats


def loudness(video, start, end):
    cmd = ffin(video, start, end)
    cmd[2] = "info"                                    # the ebur128 summary is printed at info level
    r = subprocess.run(cmd + ["-nostats", "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    t = r.stderr.split("Summary:")[-1]
    def grab(key):
        m = re.search(key + r":\s*(-?[\d.]+)", t)
        return float(m.group(1)) if m else None
    return {"integrated_lufs": grab("I"), "lra_lu": grab("LRA"), "true_peak_dbfs": grab("Peak")}


# ---------------------------------------------------------------- sheets

def grab_tile(video, t, w=256):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t):.3f}", "-i", video, "-frames:v", "1",
                        "-vf", f"scale={w}:-2", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    if not r.stdout:
        return None
    import io
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")


def sheet(tiles, cols, out, quality=72):
    tiles = [t for t in tiles if t[0] is not None]
    if not tiles:
        return
    tw, th = tiles[0][0].size
    rows = math.ceil(len(tiles) / cols)
    img = Image.new("RGB", (cols * tw, rows * (th + 16)), (18, 18, 18))
    d = ImageDraw.Draw(img)
    for k, (im, label) in enumerate(tiles):
        x, y = (k % cols) * tw, (k // cols) * (th + 16)
        img.paste(im.resize((tw, th)), (x, y + 16))
        d.text((x + 3, y + 2), label, fill=(235, 235, 235))
    img.save(out, quality=quality)


def timeline(out, dur, au, cuts_t, match_t, onsets_t, silences):
    Wd, Hd = 1800, 260
    img = Image.new("RGB", (Wd, Hd), (250, 250, 250))
    d = ImageDraw.Draw(img)
    X = lambda t: int(t / max(dur, 1e-6) * (Wd - 20)) + 10
    for s, e in silences:
        d.rectangle([X(s), 10, X(e), Hd - 10], fill=(225, 225, 225))
    if au is not None:
        db = au["db"]
        step = max(1, len(db) // (Wd - 20))
        pts = []
        for i in range(0, len(db), step):
            v = max(-60.0, float(db[i:i + step].max()))
            pts.append((X(i * au["dt"]), int(120 - (v + 60) / 60 * 100)))
        d.line(pts, fill=(40, 90, 200), width=1)
        fl = au["flux"]
        m = fl.max() + 1e-9
        pts = [(X(i * au["dt"]), int(240 - float(fl[i:i + step].max()) / m * 100)) for i in range(0, len(fl), step)]
        d.line(pts, fill=(120, 120, 120), width=1)
    for t in onsets_t:
        d.line([X(t), 236, X(t), 250], fill=(0, 0, 0))
    for t in cuts_t:
        d.line([X(t), 10, X(t), 130], fill=(220, 40, 40))
    for t in match_t:
        d.line([X(t), 10, X(t), 130], fill=(20, 170, 60), width=3)
    step = 1 if dur <= 40 else 5 if dur <= 200 else 30 if dur <= 1200 else 120
    for s in range(0, int(dur) + 1, step):
        d.text((X(s) + 1, 126), f"{s}", fill=(90, 90, 90))
    d.text((12, 12), "blue: loudness dB   red: cuts   green: match cuts   grey: onsets   shaded: silence", fill=(0, 0, 0))
    img.save(out)


# ---------------------------------------------------------------- main

def fmt(t):
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("outdir")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--scene", type=float, default=0.30, help="hard-cut threshold (ffmpeg scene score scale)")
    ap.add_argument("--sheet-max", type=int, default=60)
    ap.add_argument("--no-sheets", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    meta = probe(a.video)
    end = a.end if a.end else meta["duration"]
    end = min(end, meta["duration"])
    dur = end - a.start
    fr, cuts = scan_picture(a.video, a.start, end, meta["fps"], a.scene)
    fps = len(fr) / dur if dur > 0 and len(fr) else meta["fps"]
    nfr = len(fr)

    cut_rows = []
    for c in cuts:
        row = {"t": round(c["f"] / fps, 3), "frame": c["f"], "scene": round(c["score"], 3)}
        row.update(classify_cut(c, fr))
        cut_rows.append(row)
    bounds = [0] + [c["f"] for c in cuts] + [nfr]
    shots = []
    for k in range(len(bounds) - 1):
        s, e = bounds[k], bounds[k + 1]
        if e <= s:
            continue
        seg = fr[s + 1:e] if e - s > 2 else fr[s:e]
        lab, mag, dies = camera_label(seg)
        shots.append({"i": len(shots) + 1, "t": round(s / fps, 3), "len": round((e - s) / fps, 3),
                      "camera": lab, "motion": round(mag, 2), "move_dies_before_cut": dies,
                      "luma": round(float(fr[s:e, 5].mean()), 1)})

    au = scan_audio(a.video, a.start, end)
    sound = {"has_audio": au is not None}
    onsets_t, silences, drops, cuts_t = [], [], [], [c["t"] for c in cut_rows]
    if au is not None:
        dt = au["dt"]
        pk = peaks(au["flux"], dt)
        if len(pk):
            h = au["flux"][pk]
            strong = pk[h >= np.percentile(h, 60)]
        else:
            strong = pk
        T0 = au["t0"]                                   # frame centre offset (~46 ms)
        onsets_t = (strong * dt + T0).round(3).tolist()
        bpm, conf, beats = tempo(au["flux"], dt)
        db = au["db"]
        ref = float(np.percentile(db, 90))
        quiet = db < ref - 28
        i = 0
        while i < len(quiet):
            if quiet[i]:
                j = i
                while j < len(quiet) and quiet[j]:
                    j += 1
                if (j - i) * dt >= 0.25:
                    silences.append((round(i * dt, 2), round(j * dt, 2)))
                i = j
            else:
                i += 1
        sm = np.convolve(db, np.ones(5) / 5, mode="same")
        lag = int(0.3 / dt)
        for i in range(lag, len(sm) - lag, lag // 2 or 1):
            if sm[i - lag] - sm[i + lag] > 15 and sm[i - lag] > ref - 12:
                if not drops or i * dt - drops[-1] > 1.0:
                    drops.append(round(i * dt, 2))
        lp = peaks(au["low"], dt, k=2.0, gap=0.25)
        booms = (lp * dt + T0).round(2).tolist()
        def near(ts, pts, tol=0.07):
            if not len(pts) or not ts:
                return 0.0
            pts = np.asarray(pts)
            return float(np.mean([np.min(np.abs(pts - t)) <= tol for t in ts]))
        rate = len(onsets_t) / max(dur, 1e-6)
        chance = 1 - math.exp(-rate * 0.14)
        hit = near(cuts_t, onsets_t)
        beat_hit = near(cuts_t, beats.tolist() if beats is not None else [])
        perc_pk = np.array([])
        music_share = None
        if au["perc"] is not None:
            pe = np.log1p(au["perc"] / (np.median(au["perc"]) + 1e-12))
            pp = peaks(pe, dt, k=1.5, gap=0.1)
            perc_pk = pp * dt + T0
            hshare = au["harm"] / (au["harm"] + au["perc"] + 1e-12)
            loud = db > ref - 30
            music_share = round(float(hshare[loud].mean()), 2) if loud.any() else None
        cut_sfx = {}
        for c in cut_rows:
            c["sound"] = cut_sound(au, c["t"], ref, booms, perc_pk)
            for tg in c["sound"]:
                cut_sfx[tg] = cut_sfx.get(tg, 0) + 1
        sec = max(1, int(dur))
        per_sec = [round(float(db[int(s / dt):int((s + 1) / dt)].max()), 1) if int(s / dt) < len(db) else None for s in range(sec)]
        sound.update({
            "loudness": loudness(a.video, a.start, end),
            "tempo_bpm": bpm, "tempo_confidence": conf,
            "strong_onsets_per_sec": round(rate, 2),
            "cuts_on_onset_frac": round(hit, 2), "chance_frac": round(chance, 2),
            "sync_lift": round(hit / chance, 2) if chance > 0 else None,
            "cuts_on_beat_grid_frac": round(beat_hit, 2),
            "silences": silences, "sudden_drops_t": drops, "low_booms_t": booms[:80],
            "percussive_hits_per_sec": round(len(perc_pk) / max(dur, 1e-6), 2),
            "harmonic_share_when_audible": music_share, "sound_at_cuts": cut_sfx,
            "peak_db_per_second": per_sec if sec <= 400 else None,
        })

    lens = np.array([s["len"] for s in shots]) if shots else np.array([dur])
    quarters = []
    for q in range(4):
        lo, hi = dur * q / 4, dur * (q + 1) / 4
        n = sum(1 for t in cuts_t if lo <= t < hi)
        quarters.append(round((hi - lo) / (n + 1), 2))
    cams = {}
    for s in shots:
        cams[s["camera"]] = round(cams.get(s["camera"], 0) + s["len"] / dur * 100, 1)
    tagcount = {}
    for c in cut_rows:
        for t in c["tags"]:
            tagcount[t] = tagcount.get(t, 0) + 1
    picture = {"shots": len(shots), "cuts": len(cut_rows), "cuts_per_min": round(len(cut_rows) / dur * 60, 1),
               "asl_mean": round(float(lens.mean()), 2), "asl_median": round(float(np.median(lens)), 2),
               "shortest": round(float(lens.min()), 2), "longest": round(float(lens.max()), 2),
               "avg_shot_by_quarter": quarters, "camera_time_pct": cams, "cut_tags": tagcount,
               "moves_dying_before_cut": sum(1 for s in shots if s["move_dies_before_cut"])}
    out = {"file": os.path.basename(a.video), "meta": meta, "window": [a.start, end],
           "picture": picture, "sound": sound, "shots": shots, "cuts": cut_rows}
    with open(os.path.join(a.outdir, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    matches = sorted([c for c in cut_rows if {"graphic-match", "position-locked", "motion-carried"} & set(c["tags"])],
                     key=lambda c: -c["match_score"])
    match_t = [c["t"] for c in matches if "graphic-match" in c["tags"] or "position-locked" in c["tags"]]
    if not a.no_sheets:
        pick = shots
        if len(shots) > a.sheet_max:
            idx = np.linspace(0, len(shots) - 1, a.sheet_max).round().astype(int)
            pick = [shots[i] for i in sorted(set(idx.tolist()))]
        tiles = [(grab_tile(a.video, a.start + s["t"] + s["len"] / 2, 224),
                  f"#{s['i']} {fmt(a.start + s['t'])} {s['len']:.1f}s") for s in pick]
        sheet(tiles, 8 if len(tiles) > 24 else 6, os.path.join(a.outdir, "shots.jpg"))
        pairs = []
        for c in matches[:16]:
            t = a.start + c["t"]
            pairs.append((grab_tile(a.video, t - 1.5 / fps, 224), f"{fmt(t)} before"))
            pairs.append((grab_tile(a.video, t + 1.5 / fps, 224), f"after {'+'.join(c['tags'])[:26]}"))
        if pairs:
            sheet(pairs, 4, os.path.join(a.outdir, "matches.jpg"))
        timeline(os.path.join(a.outdir, "timeline.png"), dur, au, cuts_t, match_t, onsets_t, silences)

    L = [f"# Film study: {out['file']}", "",
         f"{meta['width']}x{meta['height']} · {meta['fps']} fps · window {fmt(a.start)}–{fmt(end)} ({dur:.1f} s)", "",
         "## Picture", "",
         f"- {picture['shots']} shots, {picture['cuts']} hard cuts ({picture['cuts_per_min']}/min); shot length mean {picture['asl_mean']} s, median {picture['asl_median']} s, range {picture['shortest']}–{picture['longest']} s",
         f"- Average shot length by quarter (pacing curve): {picture['avg_shot_by_quarter']}",
         f"- Camera (share of running time): {picture['camera_time_pct']}",
         f"- Cut tags: {picture['cut_tags'] or 'none'}; shots whose move dies before the cut: {picture['moves_dying_before_cut']}"]
    dark = float((fr[:, 5] < 25).mean()) if nfr else 0.0
    picture["dark_share"] = round(dark, 2)
    if dark > 0.10:
        L.append(f"- WARNING: {dark * 100:.0f}% of frames are very dark (luma < 25): hard cuts there can be missed and flicker can look like cuts; check those stretches by eye")
    L.append("")
    if sound["has_audio"]:
        s = sound
        L += ["## Sound", "",
              f"- Loudness: {s['loudness']['integrated_lufs']} LUFS integrated, LRA {s['loudness']['lra_lu']} LU, true peak {s['loudness']['true_peak_dbfs']} dBFS",
              f"- Tempo estimate: {s['tempo_bpm']} BPM (confidence {s['tempo_confidence']}; above ~3 means a steady beat)",
              f"- Cuts landing within ±70 ms of a strong onset: {int(s['cuts_on_onset_frac'] * 100)}% (chance {int(s['chance_frac'] * 100)}%, lift ×{s['sync_lift']}); on the beat grid: {int(s['cuts_on_beat_grid_frac'] * 100)}%",
              f"- Silences ≥0.25 s: {s['silences'][:20]}",
              f"- Sudden drops (−15 dB within 0.6 s): {s['sudden_drops_t'][:20]}",
              f"- Low booms / hits: {s['low_booms_t'][:30]}",
              f"- Music vs hits: harmonic share {s['harmonic_share_when_audible']} (near 1 = sustained music/voice bed, low = percussive / SFX-driven); percussive hits {s['percussive_hits_per_sec']}/s",
              f"- What the sound does at cuts (count of {picture['cuts']}): {s['sound_at_cuts'] or 'nothing marked'}", ""]
        if s.get("peak_db_per_second"):
            L += [f"- Peak dB per second: {s['peak_db_per_second']}", ""]
    else:
        L += ["## Sound", "", "- No audio track.", ""]
    if matches:
        L += ["## Strongest match cuts (see matches.jpg)", "", "| Time | Tags | edge | tone | colour change | motion cos |", "|---|---|---|---|---|---|"]
        for c in matches[:16]:
            L.append(f"| {fmt(a.start + c['t'])} | {', '.join(c['tags'])} | {c['edge_sim']} | {c['tone_sim']} | {c['colour_change']} | {c['motion_cos']} |")
        L.append("")
    if len(shots) <= 150:
        L += ["## Shots", "", "| # | Start | Len s | Camera | Motion | Dies before cut |", "|---|---|---|---|---|---|"]
        for s in shots:
            L.append(f"| {s['i']} | {fmt(a.start + s['t'])} | {s['len']} | {s['camera']} | {s['motion']} | {'yes' if s['move_dies_before_cut'] else ''} |")
    with open(os.path.join(a.outdir, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"ok {out['file']}: {picture['shots']} shots, {picture['cuts']} cuts -> {a.outdir}")


if __name__ == "__main__":
    main()
