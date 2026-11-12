#!/usr/bin/env python3
"""Measure phrase onsets from audio ENERGY in the reference voice (the one the picture was timed to) and in a new voice,
match them, and print how far each new phrase is from its picture beat. Optionally writes a shift table for
phrase_sync.py. STT timestamps have different biases per voice; energy onsets do not.

Examples:
  python onsets.py --ref scratch_placed.wav --new final_placed.wav
  python onsets.py --ref scratch_placed.wav --new final_placed.wav --ref-words words/scratch.json \
      --new-words words/final.json --emit-shifts shifts.json

Matching: with both words files, phrases are matched by their first two words (most reliable); otherwise by order,
nearest onset within --window seconds. Needs: ffmpeg, numpy.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _audio as A  # noqa: E402


def label(words, R):
    out = []
    for a, b in R:
        ws = [w["w"] for w in (words or []) if a - 0.12 <= (w["s"] + w["e"]) / 2 <= b + 0.05]
        out.append((a, b, " ".join(ws)))
    return out


def main():
    ap = argparse.ArgumentParser(description="Energy-based phrase onsets: reference voice vs new voice.")
    ap.add_argument("--ref", required=True, help="voice the picture was timed to (e.g. the placed scratch voice)")
    ap.add_argument("--new", required=True, help="new voice, already placed (place_lines.py)")
    ap.add_argument("--ref-words", help="word timings JSON of --ref (optional, improves matching + labels)")
    ap.add_argument("--new-words", help="word timings JSON of --new (optional)")
    ap.add_argument("--window", type=float, default=1.2, help="max distance for a match (s, default 1.2)")
    ap.add_argument("--tolerance", type=float, default=0.12, help="flag phrases further than this (s, default 0.12)")
    ap.add_argument("--min-gap", type=float, default=0.06, help="pauses shorter than this do not split a phrase (s)")
    ap.add_argument("--emit-shifts", help="write {new_onset: shift_s} for flagged phrases (input for phrase_sync.py)")
    ap.add_argument("--aliases", help="JSON token map for word matching")
    a = ap.parse_args()

    A.need_ffmpeg()
    A.np()
    aliases = A.load_aliases(a.aliases)
    rw = json.load(open(a.ref_words, encoding="utf-8")) if a.ref_words else None
    nw = json.load(open(a.new_words, encoding="utf-8")) if a.new_words else None
    RJ = label(rw, A.regions(A.load(a.ref), min_gap=a.min_gap))
    RN = label(nw, A.regions(A.load(a.new), min_gap=a.min_gap))
    by_words = rw is not None and nw is not None
    fj = [A.tokens(t, aliases)[:2] for _, _, t in RJ]
    fn = [A.tokens(t, aliases)[:2] for _, _, t in RN]
    used, shifts, last = set(), {}, -1
    print(f"{'new':>7} {'ref':>7} {'diff':>6}   phrase")
    for i, (s, e, t) in enumerate(RN):
        best = None
        for k, (js, je, jt) in enumerate(RJ):
            if k in used or abs(js - s) > a.window:
                continue
            if by_words:
                if fn[i] and fj[k] == fn[i]:
                    best = k; break
            elif k > last and (best is None or abs(js - s) < abs(RJ[best][0] - s)):
                best = k
        if best is None:
            print(f"{s:7.2f} {'-':>7} {'':>6}   {t}")
            continue
        used.add(best); last = max(last, best)
        js = RJ[best][0]; d = s - js
        flag = "<<" if abs(d) > a.tolerance else "  "
        print(f"{s:7.2f} {js:7.2f} {d:+6.2f} {flag} {t}")
        if abs(d) > a.tolerance:
            shifts[f"{s:.3f}"] = round(js - s, 3)
    print(f"\n{len(shifts)} phrase(s) outside +/-{a.tolerance}s of their picture beat")
    if a.emit_shifts:
        with open(a.emit_shifts, "w", encoding="utf-8") as f:
            json.dump(shifts, f, indent=1)
        print(f"shift table -> {a.emit_shifts} (review it, then run phrase_sync.py)")


if __name__ == "__main__":
    main()
