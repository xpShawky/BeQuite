#!/usr/bin/env python3
"""Find where a "robotic" voice texture comes from, and make listening options.

make mode: render the same voice through several processing chains, loudness-matched (-16 LUFS), as numbered
           audio-only files (optionally only excerpts), and print a clarity score for each.
measure mode: print the clarity score of existing files.

Clarity = median cepstral peak prominence (CPP) over voiced frames. Lower = rougher / more artificial.
It is a pointer, not a verdict: the user's ears on a PHONE / earphones decide (the texture was not obvious on PC
speakers in the field case).

Examples:
  python voice_chain_compare.py make --input placed_wsola.wav --outdir chains/ --excerpt 11.3-21.2 --excerpt 29-32.3
  python voice_chain_compare.py make --input placed.wav --outdir chains/ --presets minimal,none,comp_fast
  python voice_chain_compare.py measure chains/*.wav source_take.wav

Presets (ffmpeg -af): minimal (recommended) · none · comp_gentle · comp_fast (reproduces the warble cause) ·
custom chains via --chain NAME="filter,chain". Needs: ffmpeg, numpy.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _audio as A  # noqa: E402

PRESETS = {
    "minimal": "highpass=f=70,equalizer=f=5800:t=q:w=1.4:g=-1.5,equalizer=f=170:t=q:w=0.9:g=1.5",
    "none": "anull",
    "comp_gentle": "highpass=f=80,acompressor=threshold=0.1:ratio=2:attack=20:release=250:knee=6,equalizer=f=5800:t=q:w=1.4:g=-1.5",
    "comp_fast": "highpass=f=85,acompressor=threshold=0.1:ratio=3:attack=5:release=80:makeup=2,equalizer=f=3500:t=q:w=1:g=1.5",
}


def cpp(y, sr):
    np = A.np()
    n, hop = 2048, 512
    win = np.hanning(n)
    vals = []
    for i in range(0, len(y) - n, hop):
        fr = y[i:i + n] * win
        if np.sqrt((fr ** 2).mean()) < 0.02:
            continue
        spec = 20 * np.log10(np.abs(np.fft.rfft(fr)) + 1e-9)
        cep = np.abs(np.fft.irfft(spec))
        qf = np.arange(len(cep)) / sr
        m = (qf > 1 / 400) & (qf < 1 / 70)   # 70-400 Hz pitch range
        idx = np.arange(len(cep))[m]
        fit = np.polyfit(idx, cep[m], 1)
        vals.append(cep[m].max() - np.polyval(fit, idx[np.argmax(cep[m])]))
    return float(np.median(vals)) if vals else float("nan")


def parse_span(s):
    a, b = s.split("-")
    return float(a), float(b)


def main():
    ap = argparse.ArgumentParser(description="Voice-chain options + clarity (CPP) measurement.")
    sub = ap.add_subparsers(dest="mode", required=True)
    mk = sub.add_parser("make", help="render chain options")
    mk.add_argument("--input", required=True, help="voice already placed/sped with WSOLA only, no other processing")
    mk.add_argument("--outdir", required=True)
    mk.add_argument("--presets", default="minimal,none,comp_gentle,comp_fast", help="comma list of preset names")
    mk.add_argument("--chain", action="append", default=[], help='extra option NAME="ffmpeg,af,chain" (repeatable)')
    mk.add_argument("--excerpt", action="append", default=[], help="START-END seconds to keep (repeatable); default whole file")
    ms = sub.add_parser("measure", help="measure clarity of existing files")
    ms.add_argument("files", nargs="+")
    a = ap.parse_args()

    A.need_ffmpeg()
    np = A.np()
    SR = A.SR
    if a.mode == "measure":
        for f in a.files:
            print(f"{os.path.basename(f):40s} clarity (CPP) {cpp(A.load(f, SR, 1), SR):6.2f}")
        return

    chains = {}
    for name in [p.strip() for p in a.presets.split(",") if p.strip()]:
        if name not in PRESETS:
            sys.exit(f"unknown preset '{name}'. Known: {', '.join(PRESETS)}")
        chains[name] = PRESETS[name]
    for c in a.chain:
        if "=" not in c:
            sys.exit('--chain must look like NAME="filter,chain"')
        k, v = c.split("=", 1); chains[k.strip()] = v.strip().strip('"')
    os.makedirs(a.outdir, exist_ok=True)
    x = A.load(a.input, SR, 1)
    spans = [parse_span(s) for s in a.excerpt]

    def excerpt(y):
        if not spans:
            return y
        parts = []
        for s, e in spans:
            seg = y[int(s * SR):int(e * SR)].copy(); f = min(len(seg) // 2, int(0.05 * SR))
            if f:
                seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
            parts += [seg, np.zeros(int(0.6 * SR), np.float32)]
        return np.concatenate(parts)

    for n, (name, af) in enumerate(chains.items(), 1):
        y = excerpt(A.ffilter(x, af, SR))
        tmp = os.path.join(a.outdir, f"_tmp_{name}.wav")
        out = os.path.join(a.outdir, f"{n:02d}_{name}.wav")
        A.write(tmp, y, SR)
        A.write(out, A.load(tmp, SR, 1, af="loudnorm=I=-16:TP=-1.5:LRA=11"), SR)
        os.remove(tmp)
        print(f"{os.path.basename(out):32s} clarity (CPP) {cpp(A.load(out, SR, 1), SR):6.2f}   chain: {af}")
    print("\nListen to the numbered files on a phone and on earphones, same loudness, then let the user choose by ear.")


if __name__ == "__main__":
    main()
