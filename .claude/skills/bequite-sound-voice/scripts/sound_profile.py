# Sound profile of a reference film: tempo, drum hits, loudness arc (build / drop / silence) and cut-to-beat sync.
# numpy + scipy + ffmpeg only.
#   python .claude/skills/bequite-sound-voice/scripts/sound_profile.py <film.mp4> [--label name] [--json out.json]
import argparse, json, subprocess, sys
import numpy as np
from scipy.signal import butter, sosfiltfilt, find_peaks

SR = 22050
def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)

def band(x, lo, hi):
    sos = butter(4, [lo, hi], btype="band", fs=SR, output="sos") if lo else butter(4, hi, btype="low", fs=SR, output="sos")
    return sosfiltfilt(sos, x)

def env(x, hop):
    n = len(x) // hop
    return np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)

def onset_strength(x, hop=256, nfft=1024):
    win = np.hanning(nfft); frames = 1 + (len(x) - nfft) // hop
    idx = np.arange(nfft)[None, :] + hop * np.arange(frames)[:, None]
    S = np.abs(np.fft.rfft(x[idx] * win, axis=1)); S = np.log1p(100 * S)
    flux = np.maximum(0, np.diff(S, axis=0)).sum(axis=1)
    return np.concatenate([[0], flux]), hop / SR

def tempo(oenv, dt, lo=70, hi=180):
    o = oenv - oenv.mean(); ac = np.correlate(o, o, "full")[len(o) - 1:]
    lags = np.arange(len(ac)) * dt; bpm = 60 / np.maximum(lags, 1e-9)
    m = (bpm >= lo) & (bpm <= hi)
    # weight towards 100-130 (where promo music sits) to break octave ties
    w = np.exp(-0.5 * ((np.log2(bpm[m] / 118)) / 0.9) ** 2)
    k = np.argmax(ac[m] * w); return float(bpm[m][k]), float(ac[m][k] / ac[0])

def hits(x, lo, hi, thr_sd=2.2, min_gap=0.09):
    e = env(band(x, lo, hi), 256); dt = 256 / SR
    d = np.maximum(0, np.diff(np.log(e + 1e-6))); d = np.concatenate([[0], d])
    h = d * (e / (e.max() + 1e-9)) ** 0.5
    pk, _ = find_peaks(h, height=h.mean() + thr_sd * h.std(), distance=max(1, int(min_gap / dt)))
    return pk * dt

def cuts(path, thr=0.32):
    out = subprocess.run(["ffmpeg", "-v", "info", "-i", path, "-vf", f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    ts = []
    for line in out.splitlines():
        if "pts_time:" in line:
            try: ts.append(float(line.split("pts_time:")[1].split()[0]))
            except Exception: pass
    return np.array(ts)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("film"); ap.add_argument("--label", default=None); ap.add_argument("--json", default=None)
    a = ap.parse_args()
    x = decode(a.film); dur = len(x) / SR
    oenv, dt = onset_strength(x)
    bpm, conf = tempo(oenv, dt)
    kick, snare = hits(x, 35, 130), hits(x, 1500, 5000, thr_sd=2.6)
    lufs_like = 20 * np.log10(env(x, int(SR * 0.25)) + 1e-9)          # 0.25 s RMS in dBFS
    peak = lufs_like.max()
    quiet = np.nonzero(lufs_like < peak - 30)[0] * 0.25                 # near-silent windows
    # silences = runs of quiet windows >= 0.5 s
    sil = []
    if len(quiet):
        start = prev = quiet[0]
        for t in quiet[1:]:
            if t - prev > 0.26: (sil.append((start, prev + 0.25)) if prev + 0.25 - start >= 0.5 else None); start = t
            prev = t
        if prev + 0.25 - start >= 0.5: sil.append((start, prev + 0.25))
    c = cuts(a.film)
    beat = 60 / bpm
    # beat phase: the offset that puts most kicks on the grid
    best = max(np.linspace(0, beat, 48, endpoint=False), key=lambda ph: np.sum(np.abs(((kick - ph + beat / 2) % beat) - beat / 2) < 0.04))
    def on_grid(ts, tol):
        if len(ts) == 0: return 0.0
        return float(np.mean(np.abs(((ts - best + beat / 2) % beat) - beat / 2) < tol))
    chance = lambda tol: 2 * tol / beat
    thirds = [float(np.mean(lufs_like[int(i * len(lufs_like) / 3): int((i + 1) * len(lufs_like) / 3)])) for i in range(3)]
    res = {
        "label": a.label or a.film.split("/")[-1], "duration": round(dur, 2), "bpm": round(bpm, 1), "tempo_conf": round(conf, 2),
        "kicks_per_s": round(len(kick) / dur, 2), "snares_per_s": round(len(snare) / dur, 2),
        "loudness_thirds_db": [round(v, 1) for v in thirds], "peak_db": round(float(peak), 1),
        "silences": [[round(s, 2), round(e, 2)] for s, e in sil],
        "cuts": len(c), "cuts_per_s": round(len(c) / dur, 2),
        "cuts_on_beat_40ms": round(on_grid(c, 0.04), 2), "chance_40ms": round(chance(0.04), 2),
        "cuts_on_beat_80ms": round(on_grid(c, 0.08), 2), "chance_80ms": round(chance(0.08), 2),
        "first_kick": round(float(kick[0]), 2) if len(kick) else None,
        "loudest_moment": round(float(np.argmax(lufs_like) * 0.25), 2),
    }
    print(json.dumps(res, ensure_ascii=False))
    if a.json: json.dump(res, open(a.json, "w"), indent=1)

if __name__ == "__main__":
    main()
