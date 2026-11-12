#!/usr/bin/env python3
"""Cue-sheet mixer: voice + music edited to picture + sparse SFX + optional tuned tones -> stems + mastered mix.
Everything the film needs is data in one JSON cue sheet, so a new cut or a new voice is a JSON edit, not new code.

Example:
  python mix_cues.py cues.json --out audio/mix.wav --stems audio/stems/
  voice audition inside the same mix:   python mix_cues.py cues.json --voice vo/option_3.wav --out audition/03.wav

Cue sheet (paths are relative to the cue sheet's folder; see ../references/example_cue_sheet.json):
{
  "duration": 30.0,
  "voice":  {"file": "vo/voice.wav", "gain_db": 0},
  "music":  {"gain_db": -7, "duck_db": -5.5, "attack": 0.06, "release": 0.35,
             "segments": [{"file": "music/track.mp3", "film_start": 0, "film_end": 12, "track_start": 1.6,
                           "fade_in": 1.2, "fade_out": 0.3, "lowpass": 4200}],
             "automation": [[0, -6], [11.4, -6], [11.5, -60], [12.0, 0], [29.5, -40]]},
  "sfx":    {"duck_db": -4, "cues": [{"file": "sfx/whoosh.wav", "at": 11.8, "gain_db": -24, "peak": 0.41,
             "semis": 0, "lowpass": null, "highpass": null, "trim_start": 0, "trim_len": null, "fade_out": 0.04}]},
  "tones":  [{"freq": 523.25, "at": 12.0, "gain_db": -24, "dur": 0.9, "bright": 0.35}],
  "master": {"lufs": -14, "true_peak": -1.2, "lra": 11}
}
"peak" = the moment inside the (trimmed) sample that must land exactly on "at" (e.g. the impact of a whoosh).
"automation" = music level in dB at film times (linear interpolation), applied on top of gain_db and ducking.
Needs: ffmpeg, numpy.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _audio as A  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="JSON cue sheet -> voice/music/SFX stems + mastered mix.")
    ap.add_argument("cues", help="cue sheet JSON")
    ap.add_argument("--out", required=True, help="mastered mix WAV")
    ap.add_argument("--voice", help="override the voice file (audition other voices inside the same mix)")
    ap.add_argument("--stems", help="folder for vo/music/sfx stem WAVs (keep them for re-cuts)")
    ap.add_argument("--no-master", action="store_true", help="write the raw sum only")
    ap.add_argument("--seed", type=int, default=7, help="random seed for any jitter (default 7)")
    a = ap.parse_args()

    A.need_ffmpeg()
    np = A.np()
    SR = A.SR
    with open(a.cues, encoding="utf-8") as f:
        C = json.load(f)
    base = os.path.dirname(os.path.abspath(a.cues))
    P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    D = float(C["duration"]); N = int(D * SR)
    db = lambda x: 10 ** (np.asarray(x, dtype=np.float64) / 20)

    def place(bus, y, t, gain=0.0):
        i = int(round(t * SR)); j = 0
        if i < 0:
            j = -i; i = 0
        n = min(len(y) - j, len(bus) - i)
        if n > 0:
            bus[i:i + n] += y[j:j + n] * float(db(gain))

    def fades(y, fi, fo):
        a_, b_ = min(len(y), int(fi * SR)), min(len(y), int(fo * SR))
        if a_: y[:a_] *= np.linspace(0, 1, a_)[:, None]
        if b_: y[-b_:] *= np.linspace(1, 0, b_)[:, None]
        return y

    def pitch(y, semis):
        if abs(semis) < 0.01:
            return y
        r = 2 ** (semis / 12); idx = np.arange(0, len(y) - 1, r)
        return np.stack([np.interp(idx, np.arange(len(y)), y[:, c]) for c in range(y.shape[1])], 1).astype(np.float32)

    def filt(lp=None, hp=None):
        parts = []
        if hp: parts.append(f"highpass=f={hp}")
        if lp: parts.append(f"lowpass=f={lp}")
        return ",".join(parts) or None

    # ---- voice ----
    vfile = a.voice or (C.get("voice") or {}).get("file")
    if vfile:
        vo = A.load(P(vfile) if not a.voice else a.voice, SR, 1)[:N]
        vo = np.pad(vo, (0, max(0, N - len(vo))))
        VO = np.repeat(vo[:, None], 2, axis=1) * float(db((C.get("voice") or {}).get("gain_db", 0)))
        act = (np.convolve(np.abs(vo), np.ones(2400) / 2400, "same") > 0.01).astype(np.float32)
    else:
        VO = np.zeros((N, 2), np.float32); act = np.zeros(N, np.float32)
    M = C.get("music") or {}
    att, rel = float(M.get("attack", 0.06)), float(M.get("release", 0.35))
    duck = np.zeros(N, np.float32); d = 0.0; step = 48
    up, dn = step / (att * SR), step / (rel * SR)
    for i in range(0, N, step):
        d = min(1.0, d + up) if act[i] > d else max(0.0, d - dn)
        duck[i:i + step] = d

    # ---- music ----
    mus = np.zeros((N, 2), np.float32)
    for s in M.get("segments", []):
        f0, f1, t0 = float(s["film_start"]), float(s["film_end"]), float(s.get("track_start", 0))
        xin, xout = float(s.get("fade_in", 0)), float(s.get("fade_out", 0))
        y = A.load(P(s["file"]), SR, 2, ss=t0, t=f1 - f0 + xout, af=filt(s.get("lowpass"), s.get("highpass")))
        place(mus, fades(y, xin, xout), f0, float(s.get("gain_db", 0)))
    t = np.arange(N) / SR
    auto = M.get("automation")
    lvl = np.interp(t, [p[0] for p in auto], [p[1] for p in auto]) if auto else np.zeros(N)
    mus = mus * db(lvl + float(M.get("gain_db", -7)) + float(M.get("duck_db", -5.5)) * duck)[:, None].astype(np.float32)

    # ---- SFX + tones ----
    bus = np.zeros((N, 2), np.float32)
    cache = {}
    S = C.get("sfx") or {}
    for c in S.get("cues", []):
        key = (c["file"], c.get("trim_start", 0), c.get("trim_len"), c.get("lowpass"), c.get("highpass"))
        if key not in cache:
            cache[key] = A.load(P(c["file"]), SR, 2, ss=c.get("trim_start", 0) or None, t=c.get("trim_len"),
                                af=filt(c.get("lowpass"), c.get("highpass")))
        y = fades(pitch(cache[key].copy(), float(c.get("semis", 0))), 0.003, float(c.get("fade_out", 0.04)))
        place(bus, y, float(c["at"]) - float(c.get("peak", 0)), float(c.get("gain_db", -24)))
    for tone in C.get("tones", []):
        fq, dur, br = float(tone["freq"]), float(tone.get("dur", 0.9)), float(tone.get("bright", 0.35))
        n = int(dur * SR); tt = np.arange(n) / SR
        y = (np.sin(2 * np.pi * fq * tt) + br * np.sin(4 * np.pi * fq * tt) * np.exp(-tt * 9)
             + 0.12 * np.sin(6 * np.pi * fq * tt) * np.exp(-tt * 14)) * np.exp(-tt * 4.2) * np.minimum(1, tt / 0.004)
        y = np.stack([y, y], 1).astype(np.float32)
        for dl, g in [(0.071, 0.22), (0.113, 0.14)]:   # tiny room: two short echoes, slightly different per side
            k = int(dl * SR); k2 = int(k * 1.07)
            y[k:, 0] += y[:-k, 0] * g; y[k2:, 1] += y[:-k2, 1] * g
        place(bus, y / (np.abs(y).max() + 1e-9), float(tone["at"]), float(tone.get("gain_db", -24)))
    bus = bus * db(float(S.get("duck_db", -4)) * duck)[:, None].astype(np.float32)

    # ---- sum, stems, master ----
    mix = VO + mus + bus
    mix = A.ffilter(mix, "highpass=f=30", SR)
    if a.stems:
        os.makedirs(a.stems, exist_ok=True)
        for name, y in (("vo", VO), ("music", mus), ("sfx", bus)):
            A.write(os.path.join(a.stems, f"{name}.wav"), y, SR)
        print(f"stems -> {a.stems}")
    peak = float(np.abs(mix).max())
    if a.no_master:
        A.write(a.out, mix, SR)
        print(f"{a.out}: raw mix, sample peak {20 * np.log10(peak + 1e-9):.1f} dBFS (not mastered)")
        return
    raw = os.path.splitext(a.out)[0] + "_raw.wav"
    A.write(raw, mix, SR)
    m = C.get("master") or {}
    I, TP, L = A.master(raw, a.out, float(m.get("lufs", -14)), float(m.get("true_peak", -1.2)), float(m.get("lra", 11)), SR)
    print(f"{a.out}: integrated {I} LUFS | true peak {TP} dBTP | LRA {L} LU  (raw kept at {raw})")


if __name__ == "__main__":
    main()
