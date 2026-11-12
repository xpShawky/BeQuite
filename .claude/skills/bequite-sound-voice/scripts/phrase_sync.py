#!/usr/bin/env python3
"""Lock a voice to an approved picture by moving WHOLE phrases (cut only inside the silence around them).
No stretching, no new processing. Prefer this over re-timing an approved picture.

Example:
  python onsets.py --ref scratch_placed.wav --new final_placed.wav --emit-shifts shifts.json
  python phrase_sync.py --voice final_placed.wav --shifts shifts.json --out final_synced.wav --duration 57.35

--shifts: JSON {"<phrase onset s>": <shift s>, ...} (onsets as measured by onsets.py on --voice),
          or a list [[onset, shift], ...]. Hand-edit it freely: it is the editor's decision list.
Reports any phrase that would overlap or crowd its neighbour. Needs: ffmpeg, numpy.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _audio as A  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Move whole voice phrases onto picture beats (cut in silence, no stretch).")
    ap.add_argument("--voice", required=True, help="placed voice to adjust")
    ap.add_argument("--shifts", required=True, help="JSON shift table (see --help header)")
    ap.add_argument("--out", required=True, help="output WAV")
    ap.add_argument("--duration", type=float, help="trim/pad the output to this length (s)")
    ap.add_argument("--match", type=float, default=0.03, help="max distance between a table onset and a measured onset (s)")
    ap.add_argument("--min-gap", type=float, default=0.06, help="must match the value used in onsets.py")
    a = ap.parse_args()

    A.need_ffmpeg()
    np = A.np()
    SR = A.SR
    raw = json.load(open(a.shifts, encoding="utf-8"))
    table = {float(k): float(v) for k, v in (raw.items() if isinstance(raw, dict) else raw)}
    x = A.load(a.voice, SR, 1)
    R = A.regions(x, SR, min_gap=a.min_gap)
    if not R:
        sys.exit("no sound found in --voice")

    def shift_of(onset):
        for k, v in table.items():
            if abs(k - onset) <= a.match:
                return k, v
        return None, 0.0

    edges = [0.0] + [(R[i][1] + R[i + 1][0]) / 2 for i in range(len(R) - 1)] + [len(x) / SR]
    out = np.zeros(len(x) + 2 * SR, np.float32)
    placed, used = [], set()
    for i, (s, e) in enumerate(R):
        key, d = shift_of(s)
        if key is not None:
            used.add(key)
        c0 = max(edges[i], s - 0.06); c1 = min(edges[i + 1], e + 0.10)
        seg = x[int(c0 * SR):int(c1 * SR)].copy()
        f = min(len(seg) // 2, int(0.006 * SR))
        if f:
            seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        i0 = max(0, int((c0 + d) * SR))
        n = min(len(seg), len(out) - i0)
        out[i0:i0 + n] += seg[:n]
        placed.append((s + d, e + d, s, d))
    missing = sorted(set(table) - used)
    if missing:
        print(f"NOT FOUND (no measured onset within {a.match}s): {missing}")
    problems = 0
    for k in range(len(placed) - 1):
        gap = placed[k + 1][0] - placed[k][1]
        if placed[k][3] or placed[k + 1][3]:
            flag = "  << OVERLAP" if gap < 0.04 else ("  < tight" if gap < 0.08 else "")
            problems += bool(flag)
            print(f"{placed[k][2]:7.2f}{placed[k][3]:+.2f} -> {placed[k][0]:7.2f}-{placed[k][1]:7.2f} | next {placed[k + 1][0]:7.2f} gap {gap:.2f}{flag}")
    end = int((a.duration if a.duration else len(x) / SR) * SR)
    y = out[:end] if end <= len(out) else np.pad(out, (0, end - len(out)))
    A.write(a.out, y, SR)
    print(f"written {a.out} ({len(used)} phrase(s) moved, {problems} overlap/tight warning(s))")


if __name__ == "__main__":
    main()
