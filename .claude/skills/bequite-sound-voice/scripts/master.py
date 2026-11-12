#!/usr/bin/env python3
"""Master a mix to a loudness target with two-pass loudnorm (linear) + a safety limiter, then measure the result.
Or only measure (--measure-only). Python standard library only; needs ffmpeg.

Examples:
  python master.py mix_raw.wav mix_master.wav                 # -14 LUFS, true peak aimed at -1.2 dBTP
  python master.py mix_raw.wav mix_master.wav --lufs -16 --tp -1.5
  python master.py --measure-only final_film.mp4              # re-measure AFTER the AAC encode, always

The target (-14 LUFS integrated, <= -1 dBTP) is owned by bequite-sound-voice (references/music-sfx-mix.md).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _audio as A  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Two-pass loudness master + measurement (ffmpeg).")
    ap.add_argument("inp", help="input audio or video")
    ap.add_argument("out", nargs="?", help="output WAV (omit with --measure-only)")
    ap.add_argument("--lufs", type=float, default=-14.0, help="integrated target (default -14)")
    ap.add_argument("--tp", type=float, default=-1.2, help="true-peak target dBTP (default -1.2, for <= -1 after encoding)")
    ap.add_argument("--lra", type=float, default=11.0, help="loudness range target (default 11)")
    ap.add_argument("--measure-only", action="store_true")
    a = ap.parse_args()

    A.need_ffmpeg()
    if a.measure_only:
        I, P, L = A.ebur128(a.inp)
        print(f"{a.inp}: integrated {I} LUFS | true peak {P} dBTP | LRA {L} LU")
        return
    if not a.out:
        sys.exit("give an output file, or use --measure-only")
    I, P, L = A.master(a.inp, a.out, a.lufs, a.tp, a.lra)
    ok = I is not None and abs(I - a.lufs) <= 1.0 and (P is None or P <= -1.0)
    print(f"{a.out}: integrated {I} LUFS | true peak {P} dBTP | LRA {L} LU -> {'OK' if ok else 'CHECK'} "
          f"(target {a.lufs} LUFS, <= -1 dBTP)")
    print("Re-measure the final video after the AAC encode (this script with --measure-only, or render-pipeline qc_report.py).")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
