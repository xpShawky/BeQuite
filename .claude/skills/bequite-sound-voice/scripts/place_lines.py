#!/usr/bin/env python3
"""Place a full voice read onto the picture's line starts, without a robotic texture.

- splits the read into the script's lines at REAL silences (energy), never inside a word
  (STT word edges are approximate; cutting at them once clipped the start of a word)
- shortens long pauses inside a line, only inside silence (keeps --keep-pause seconds)
- speeds a line up only when it would not fit its slot, only with ffmpeg atempo (WSOLA), at most --max-tempo
- places each line at its start time; a line that still runs long pushes the next one later (reported as "late")
- applies one light chain at the end (default "minimal": low cut + slightly softer highs + a touch of body,
  NO compressor - a fast compressor and phase-vocoder stretching were measured to add the robotic texture)

Example:
  python place_lines.py --take voice_a_full.wav --script script.txt --words words/voice_a_full.json \
      --starts starts.json --duration 57.35 --out placed/voice_a.wav --report placed/voice_a.json

Inputs:
  --script  one VO line per text line ([tags] ignored). The number of lines is read from this file.
  --words   word timings of THIS take from check_take.py --words-dir (any STT with the same JSON shape works)
  --starts  JSON list with one start time (s) per script line, e.g. [0.34, 3.25, 8.23] or [{"start": 0.34}, ...]
Needs: ffmpeg, numpy.
"""
import argparse
import difflib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _audio as A  # noqa: E402

CHAINS = {
    "minimal": "highpass=f=70,equalizer=f=5800:t=q:w=1.4:g=-1.5,equalizer=f=170:t=q:w=0.9:g=1.5",
    "none": None,
}


def main():
    ap = argparse.ArgumentParser(description="Split a full read into script lines at silences and place them on the picture's line starts.")
    ap.add_argument("--take", required=True, help="full voice read (any format ffmpeg reads)")
    ap.add_argument("--script", required=True, help="script text, one VO line per text line")
    ap.add_argument("--words", required=True, help="word timings JSON for this take (from check_take.py)")
    ap.add_argument("--starts", required=True, help="JSON list: one start time per script line")
    ap.add_argument("--duration", required=True, type=float, help="film length in seconds")
    ap.add_argument("--out", required=True, help="output WAV")
    ap.add_argument("--chain", default="minimal", help='"minimal" (default), "none", or a custom ffmpeg -af chain')
    ap.add_argument("--max-tempo", type=float, default=1.15, help="max WSOLA speed-up per line (default 1.15)")
    ap.add_argument("--last-resort-tempo", type=float, default=None, help="optional second ceiling (e.g. 1.2) tried only if the film still overruns")
    ap.add_argument("--keep-pause", type=float, default=0.22, help="pauses inside a line are shortened to this (s)")
    ap.add_argument("--silence-db", type=float, default=38.0, help="silence = quieter than (95th pct - N dB) (default 38)")
    ap.add_argument("--aliases", help='JSON token map, e.g. {"acme cloud": "acmecloud"}')
    ap.add_argument("--report", help="write a JSON report (per line: start, late by, tempo, pauses cut)")
    a = ap.parse_args()

    A.need_ffmpeg()
    np = A.np()
    SR, HOP = A.SR, 0.01
    aliases = A.load_aliases(a.aliases)
    lines = [A.tokens(l, aliases) for l in A.script_lines(a.script)]
    L = len(lines)
    with open(a.starts, encoding="utf-8") as f:
        st = json.load(f)
    starts = [float(s["start"] if isinstance(s, dict) else s) for s in st]
    if len(starts) != L:
        sys.exit(f"--starts has {len(starts)} entries but the script has {L} lines; they must match")
    with open(a.words, encoding="utf-8") as f:
        W = json.load(f)
    if not W:
        sys.exit("the words file is empty")

    x = A.load(a.take, SR, 1)
    ref = [t for l in lines for t in l]
    first = np.cumsum([0] + [len(l) for l in lines]).tolist()
    hyp, own = [], []
    for i, w in enumerate(W):
        for t in A.tokens(w["w"], aliases):
            hyp.append(t); own.append(i)
    m = {}
    for blk in difflib.SequenceMatcher(None, ref, hyp, autojunk=False).get_matching_blocks():
        for d in range(blk.size):
            m[blk.a + d] = own[blk.b + d]
    if not m:
        sys.exit("no script words were found in the transcript - wrong take, wrong language or wrong script?")

    def word_at(ri):
        for k in list(range(ri, len(ref))) + list(range(ri - 1, -1, -1)):
            if k in m:
                return m[k]
        return 0

    env = A.energy_db(x, SR, HOP)
    thr = np.percentile(env, 95) - a.silence_db
    ws = [W[word_at(first[k])]["s"] for k in range(L)]
    we = [W[max(word_at(first[k]), word_at(first[k + 1]) - 1)]["e"] for k in range(L - 1)] + [W[-1]["e"]]
    onset = int(np.argmax(env > thr)) * HOP

    def quiet_runs(q):
        runs, i = [], 0
        while i < len(q):
            if q[i]:
                j = i
                while j < len(q) and q[j]:
                    j += 1
                runs.append((i, j)); i = j
            else:
                i += 1
        return runs

    a_, b_ = [max(0.0, onset - 0.06)], []
    for k in range(L - 1):
        lo, hi = max(0, int((we[k] - 0.15) / HOP)), min(len(env), int((ws[k + 1] + 0.15) / HOP))
        if hi <= lo:
            c = we[k]; b_.append(c); a_.append(c); continue
        runs = quiet_runs(env[lo:hi] < thr)
        if runs:
            r0, r1 = max(runs, key=lambda r: r[1] - r[0]); r0 += lo; r1 += lo
            b_.append(min(r1, r0 + 8) * HOP)   # a line ends at most 80 ms into the silence
            a_.append(max(r0, r1 - 6) * HOP)   # the next line starts at most 60 ms before its sound
        else:
            c = (lo + int(np.argmin(env[lo:hi]))) * HOP; b_.append(c); a_.append(c)
    q = np.where(env[int(we[-1] / HOP):] < thr)[0]
    b_.append(min(len(x) / SR, we[-1] + (q[0] + 8) * HOP if len(q) else len(x) / SR))

    def xfade(p, r, ms=10):
        f = int(ms / 1000 * SR)
        if len(p) < f or len(r) < f:
            return np.concatenate([p, r])
        ramp = np.linspace(0, 1, f, dtype=np.float32)
        return np.concatenate([p[:-f], p[-f:] * (1 - ramp) + r[:f] * ramp, r[f:]])

    ladder = [a.max_tempo] + ([a.last_resort_tempo] if a.last_resort_tempo and a.last_resort_tempo > a.max_tempo else [])
    D = a.duration
    for TMAX in ladder:
        out = np.zeros(int(D * SR) + 4 * SR, np.float32)
        cur_end, rep = 0.0, []
        for k in range(L):
            s0, s1 = a_[k], b_[k]
            e = env[int(s0 / HOP):int(s1 / HOP)]
            runs = [(i, j) for i, j in quiet_runs(e < thr) if (j - i) * HOP > a.keep_pause + 0.05 and i > 0 and j < len(e)]
            cuts = []
            for i, j in runs:
                c0 = s0 + i * HOP + a.keep_pause / 2
                cuts.append((c0, c0 + (j - i) * HOP - a.keep_pause))
            y, cur = np.zeros(0, np.float32), s0
            for c0, c1 in cuts:
                p = x[int(cur * SR):int(c0 * SR)]; y = xfade(y, p) if len(y) else p; cur = c1
            p = x[int(cur * SR):int(s1 * SR)]; y = xfade(y, p) if len(y) else p.copy()
            if len(y) < int(0.06 * SR):
                print(f"warning: line {k + 1} is almost empty ({len(y) / SR:.2f} s) - check the words file", file=sys.stderr)
            fi, fo = min(len(y), int(0.01 * SR)), min(len(y), int(0.05 * SR))
            if fi: y[:fi] *= np.linspace(0, 1, fi)
            if fo: y[-fo:] *= np.linspace(1, 0, fo)
            start = max(starts[k], cur_end + 0.08)
            nxt = starts[k + 1] if k < L - 1 else D - 0.4
            d = len(y) / SR
            tempo = min(TMAX, max(1.0, d / max(0.3, nxt - start - 0.08)))
            if tempo > 1.005:
                y = A.ffilter(y, f"atempo={tempo:.4f}", SR)
            i0 = int(start * SR); n = max(0, min(len(y), len(out) - i0)); out[i0:i0 + n] += y[:n]
            cur_end = start + len(y) / SR
            rep.append({"line": k + 1, "start": round(start, 3), "late_by": round(start - starts[k], 3),
                        "tempo": round(tempo, 3), "pauses_cut": len(cuts), "dur": round(len(y) / SR, 3)})
        if cur_end <= D - 0.45:
            break
    chain = CHAINS.get(a.chain, a.chain)
    A.write(a.out, out[:int(D * SR)], SR, af=chain)
    late = [(r["line"], r["late_by"]) for r in rep if r["late_by"] > 0.01]
    print(f"{a.out}: ends {cur_end:.2f} s of {D:.2f}; tempo {min(r['tempo'] for r in rep):.2f}-{max(r['tempo'] for r in rep):.2f}; "
          f"late lines {late or 'none'}; chain {a.chain}")
    if cur_end > D - 0.45:
        print("WARNING: the read does not fit the film even at the tempo ceiling. Do not push tempo further; "
              "re-time the picture or ask for a faster take.", file=sys.stderr)
    if a.report:
        with open(a.report, "w", encoding="utf-8") as f:
            json.dump({"take": a.take, "end": round(cur_end, 3), "tempo_ceiling": TMAX, "lines": rep}, f, indent=1)


if __name__ == "__main__":
    main()
