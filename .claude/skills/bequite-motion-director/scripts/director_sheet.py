#!/usr/bin/env python3
"""Join picture, cuts, sound and voice of a studied film into one director's timeline.

Run after film_study.py (metrics.json) and transcribe.py (transcript.md) wrote into the same folder:
  python director_sheet.py VIDEO STUDYDIR

Writes STUDYDIR/director.md:
  - Voice: words per minute while speaking, pauses, how much of the film has voice, pitch estimate
    (low / high voice; an estimate from the mixed track, music under the voice skews it), and how
    the voice sits against the cuts (cuts in pauses, lines that start just before a cut = the sound
    leads the picture, a J-cut feel).
  - One row per shot: time, length, camera, how we cut into it (picture tags + sound tags), the
    voice line under it, and the loudest moment in it.
Needs numpy (optional dependency, checked at run time) and ffmpeg.
"""
import json
import os
import re
import subprocess
import sys


def need():
    try:
        import numpy as np
        return np
    except ImportError:
        sys.exit("Missing optional dependency 'numpy'.")


np = need()
LINE = re.compile(r"^\[(\d+):([\d.]+)-(\d+):([\d.]+)\]\s*(.*)$")


def read_transcript(path):
    segs = []
    if not os.path.exists(path):
        return segs
    for ln in open(path, encoding="utf-8"):
        m = LINE.match(ln.strip())
        if m:
            s = int(m.group(1)) * 60 + float(m.group(2))
            e = int(m.group(3)) * 60 + float(m.group(4))
            txt = m.group(5).replace(" (low confidence)", "")
            segs.append({"s": s, "e": e, "text": txt, "low": "(low confidence)" in ln})
    return segs


def pitch(video, segs, start=0.0, sr=16000):
    """Median F0 of voiced frames inside speech segments (normalised autocorrelation, 70-400 Hz)."""
    if not segs:
        return None
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    f0s = []
    n, hop = 640, 320
    lo, hi = sr // 400, sr // 70
    for sg in segs:
        if sg["low"]:
            continue
        a, b = int(sg["s"] * sr), int(sg["e"] * sr)
        for i in range(a, min(b, len(x) - n), hop):
            fr = x[i:i + n] - x[i:i + n].mean()
            en = float((fr * fr).sum())
            if en < 1e-4:
                continue
            ac = np.correlate(fr, fr, "full")[n - 1:]
            ac /= ac[0] + 1e-12
            k = lo + int(np.argmax(ac[lo:hi]))
            if ac[k] > 0.55:
                f0s.append(sr / k)
            if len(f0s) > 6000:
                break
    if len(f0s) < 30:
        return None
    return float(np.median(f0s))


def fmt(t):
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    video, d = sys.argv[1], sys.argv[2]
    m = json.load(open(os.path.join(d, "metrics.json"), encoding="utf-8"))
    start, end = m["window"]
    dur = end - start
    segs = [s for s in read_transcript(os.path.join(d, "transcript.md")) if start <= s["s"] < end]
    for s in segs:
        s["s"] -= start
        s["e"] -= start
    cuts = m["cuts"]
    cut_t = np.array([c["t"] for c in cuts]) if cuts else np.array([])

    L = [f"# Director sheet: {m['file']}", ""]
    good = [s for s in segs if not s["low"] and s["text"]]
    if good:
        words = sum(len(s["text"].split()) for s in good)
        talk = sum(s["e"] - s["s"] for s in good)
        gaps = [good[k + 1]["s"] - good[k]["e"] for k in range(len(good) - 1)]
        f0 = pitch(video, [dict(s, s=s["s"] + start, e=s["e"] + start) for s in good])
        if f0 is None:
            vlab = "pitch not measurable (music too loud under the voice, or too little speech)"
        elif f0 < 150:
            vlab = f"low voice, median F0 ≈ {f0:.0f} Hz (typical of a male voice)"
        elif f0 < 185:
            vlab = f"mid voice, median F0 ≈ {f0:.0f} Hz (could be either; listen)"
        else:
            vlab = f"high voice, median F0 ≈ {f0:.0f} Hz (typical of a female voice or a child)"
        in_pause = 0
        mid_line = 0
        for t in cut_t:
            inside = any(s["s"] + 0.15 < t < s["e"] - 0.15 for s in good)
            mid_line += inside
            in_pause += not inside
        leads = sum(1 for s in good if len(cut_t) and np.any((cut_t > s["s"] + 0.05) & (cut_t < s["s"] + 0.8)))
        L += ["## Voice", "",
              f"- {len(good)} lines, {words} words; voice present {talk:.1f} s of {dur:.1f} s ({talk / dur * 100:.0f}%)",
              f"- Pace: {words / talk * 60:.0f} words per minute while speaking (calm narration ≈ 130-150, ad read ≈ 160-180, hype ≈ 190+)",
              f"- Pauses between lines: median {np.median(gaps) if gaps else 0:.2f} s, longest {max(gaps) if gaps else 0:.2f} s",
              f"- {vlab}",
              f"- Cuts during a pause: {in_pause}, cuts in the middle of a line: {mid_line}; lines that start up to 0.8 s before a cut (sound leads picture): {leads}",
              ""]
    else:
        L += ["## Voice", "", "- No reliable speech: music and sound design carry this film.", ""]

    s = m.get("sound", {})
    if s.get("has_audio"):
        L += ["## Sound in one glance", "",
              f"- {s['loudness']['integrated_lufs']} LUFS, LRA {s['loudness']['lra_lu']} LU; tempo ≈ {s['tempo_bpm']} BPM (confidence {s['tempo_confidence']})",
              f"- Cuts on strong onsets {int(s['cuts_on_onset_frac'] * 100)}% vs chance {int(s['chance_frac'] * 100)}% (lift ×{s['sync_lift']}); harmonic share {s.get('harmonic_share_when_audible')}",
              f"- Sound at cuts: {s.get('sound_at_cuts') or 'nothing marked'}; silences: {s['silences'][:8]}", ""]

    db = s.get("peak_db_per_second") or []
    L += ["## Shot by shot", "", "| # | Start | Len | Camera | Cut in (picture · sound) | Voice under it | Peak dB |", "|---|---|---|---|---|---|---|"]
    cut_by_t = {round(c["t"], 3): c for c in cuts}
    for sh in m["shots"]:
        t0, t1 = sh["t"], sh["t"] + sh["len"]
        c = cut_by_t.get(round(t0, 3))
        cut_in = "start" if c is None else (" ".join(c["tags"]) or "cut") + (" · " + " ".join(c.get("sound", [])) if c.get("sound") else "")
        vo = " ".join(x["text"] for x in good if x["s"] < t1 and x["e"] > t0)
        vo = (vo[:90] + "…") if len(vo) > 90 else vo
        pk = max([v for v in db[int(t0):int(t1) + 1] if v is not None], default=None) if db else None
        L.append(f"| {sh['i']} | {fmt(start + t0)} | {sh['len']:.2f} | {sh['camera']}{' (dies)' if sh['move_dies_before_cut'] else ''} | {cut_in} | {vo} | {pk if pk is not None else ''} |")
        if len(L) > 420:
            L.append("| … | | | | | (truncated) | |")
            break
    with open(os.path.join(d, "director.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"ok director sheet -> {os.path.join(d, 'director.md')}")


if __name__ == "__main__":
    main()
