"""Shared helpers for the bequite-sound-voice scripts.

Standard library at import time. numpy is imported lazily (np()) so every script's --help works without it.
External tool: ffmpeg + ffprobe on PATH (all audio I/O goes through ffmpeg, so any format ffmpeg reads works).
"""
import json
import re
import shutil
import subprocess
import sys

SR = 48000


# ---------- dependency checks ----------
def need_ffmpeg():
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found on PATH. Install ffmpeg (https://ffmpeg.org/download.html) and retry.")


def need(module, pip_name=None, why=""):
    """Import an optional dependency or exit with a helpful install hint."""
    try:
        return __import__(module)
    except ImportError:
        hint = f" ({why})" if why else ""
        sys.exit(f"Missing optional dependency '{module}'{hint}. Install: python -m pip install {pip_name or module}")


def np():
    return need("numpy", why="audio maths")


# ---------- audio I/O ----------
def load(path, sr=SR, ch=1, ss=None, t=None, af=None):
    """Decode any file with ffmpeg to float32. Returns shape (n,) for mono, (n, ch) otherwise.
    Decodes from the start and slices when ss is given: some TTS WAVs (e.g. 24 kHz downloads) mis-seek with -ss."""
    n_ = np()
    cmd = ["ffmpeg", "-v", "error", "-i", path]
    if af:
        cmd += ["-af", af]
    cmd += ["-ac", str(ch), "-ar", str(sr), "-f", "f32le", "-"]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg could not decode {path}: {r.stderr.decode(errors='replace').strip()}")
    y = n_.frombuffer(r.stdout, n_.float32).copy()
    if ch > 1:
        y = y.reshape(-1, ch)
    if ss is not None or t is not None:
        a = int(round((ss or 0) * sr))
        b = None if t is None else a + int(round(t * sr))
        y = y[a:b].copy()
    return y


def write(path, y, sr=SR, af=None):
    n_ = np()
    y = n_.asarray(y, dtype=n_.float32)
    ch = 1 if y.ndim == 1 else y.shape[1]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(sr), "-ac", str(ch), "-i", "-"]
    if af:
        cmd += ["-af", af]
    cmd += ["-ar", str(sr), path]
    subprocess.run(cmd, input=y.tobytes(), check=True)


def ffilter(y, af, sr=SR):
    """Run a mono/stereo float32 buffer through an ffmpeg audio filter chain and return the result."""
    n_ = np()
    ch = 1 if y.ndim == 1 else y.shape[1]
    r = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(sr), "-ac", str(ch), "-i", "-", "-af", af,
                        "-f", "f32le", "-ar", str(sr), "-ac", str(ch), "-"], input=n_.asarray(y, n_.float32).tobytes(),
                       capture_output=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg filter failed ({af}): {r.stderr.decode(errors='replace').strip()}")
    out = n_.frombuffer(r.stdout, n_.float32).copy()
    return out.reshape(-1, ch) if ch > 1 else out


# ---------- analysis ----------
def energy_db(x, sr=SR, hop_s=0.005):
    n_ = np()
    hop = max(1, int(hop_s * sr))
    m = x if x.ndim == 1 else x.mean(1)
    m = m[:len(m) // hop * hop]
    return 20 * n_.log10(n_.sqrt((m.reshape(-1, hop) ** 2).mean(1)) + 1e-9)


def regions(x, sr=SR, drop=32.0, min_gap=0.06, min_len=0.05, hop_s=0.005):
    """Sound regions from energy: frames louder than (95th percentile - drop dB); gaps shorter than min_gap are merged.
    Returns [(start_s, end_s), ...]. Energy edges are more reliable cut points than STT word edges."""
    n_ = np()
    e = energy_db(x, sr, hop_s)
    if not len(e):
        return []
    thr = n_.percentile(e, 95) - drop
    on = e > thr
    R, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]:
                j += 1
            if R and (i - R[-1][1]) * hop_s < min_gap:
                R[-1][1] = j
            else:
                R.append([i, j])
            i = j
        else:
            i += 1
    return [(a * hop_s, b * hop_s) for a, b in R if (b - a) * hop_s > min_len]


def tokens(s, aliases=None):
    """Lower-case word tokens for script <-> transcript alignment. aliases: {"acme cloud": "acmecloud", "2": "two"}."""
    s = s.lower().replace("-", " ").replace("\u2019", "'")
    for k, v in (aliases or {}).items():
        s = s.replace(k.lower(), v.lower())
    out = re.sub(r"[^\w' ]", " ", s, flags=re.UNICODE).replace("'", "").split()
    return [(aliases or {}).get(t, t) for t in out]


def script_lines(path):
    """Non-empty script lines. Text in [square brackets] (voice-direction tags) is removed for alignment."""
    with open(path, encoding="utf-8") as f:
        raw = [l.strip() for l in f.read().splitlines()]
    return [re.sub(r"\[[^\]]*\]", " ", l).strip() for l in raw if l.strip()]


def load_aliases(path):
    if not path:
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------- loudness ----------
def loudnorm_measure(path, I=-14.0, TP=-1.2, LRA=11.0):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
                        f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    err = r.stderr
    try:
        return json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    except ValueError:
        sys.exit(f"loudnorm measurement failed for {path}:\n{err[-800:]}")


def ebur128(path):
    """Return (integrated LUFS, true peak dBTP, LRA) from ffmpeg's ebur128 summary."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    s = r.stderr[r.stderr.rfind("Summary:"):]
    f = lambda pat: (lambda m: float(m.group(1)) if m and m.group(1) != "-inf" else None)(re.search(pat, s))
    return f(r"I:\s+(-?[\d.]+|-inf) LUFS"), f(r"Peak:\s+(-?[\d.]+|-inf) dBFS"), f(r"LRA:\s+(-?[\d.]+) LU")


def master(raw, out, I=-14.0, TP=-1.2, LRA=11.0, sr=SR):
    """Two-pass loudnorm (linear) + a safety limiter. Returns the measured (I, TP, LRA) of the result."""
    js = loudnorm_measure(raw, I, TP, LRA)
    limit = 10 ** ((TP - 0.3) / 20)  # sample-peak ceiling a little under the true-peak target
    af = (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true,"
          f"alimiter=limit={limit:.4f}:attack=3:release=80:level=disabled")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ar", str(sr), out], check=True)
    return ebur128(out)


# ---------- captions ----------
def srt_time(t):
    t = max(0.0, t)
    h, rem = divmod(int(round(t * 1000)), 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def words_to_srt(words, max_chars=42, max_dur=3.5, pause=0.45, min_dur=0.8):
    """words: [{"w","s","e"}]. Breaks a caption on punctuation, a pause, the char limit or the duration limit."""
    cues, cur = [], []

    def flush():
        if cur:
            s, e = cur[0]["s"], max(cur[-1]["e"], cur[0]["s"] + min_dur)
            cues.append((s, e, " ".join(w["w"].strip() for w in cur).strip()))
            cur.clear()

    for i, w in enumerate(words):
        if cur:
            text = " ".join(x["w"].strip() for x in cur + [w])
            if (len(text) > max_chars or w["e"] - cur[0]["s"] > max_dur or w["s"] - cur[-1]["e"] > pause):
                flush()
        cur.append(w)
        if re.search(r"[.!?\u061F\u06D4]$", w["w"].strip()):
            flush()
    flush()
    for k in range(len(cues) - 1):  # no overlaps
        s, e, t = cues[k]
        if e > cues[k + 1][0]:
            cues[k] = (s, cues[k + 1][0] - 0.01, t)
    return "\n".join(f"{k + 1}\n{srt_time(s)} --> {srt_time(e)}\n{t}\n" for k, (s, e, t) in enumerate(cues))
