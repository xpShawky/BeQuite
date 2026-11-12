# bequite-sound-voice scripts

Parameterised tools for voice placement, sync, chain comparison, mixing and mastering. No project paths, no fixed line counts: the number of lines comes from the script file, timings from JSON, everything else from flags. Run any script with `--help`.

## Requirements

| Need | Used by | Install |
|---|---|---|
| Python 3.9+ | all | — |
| ffmpeg + ffprobe on PATH | all (all audio I/O, filters, loudness) | https://ffmpeg.org/download.html |
| numpy | all except `master.py` | `python -m pip install numpy` |
| faster-whisper (optional) | `check_take.py` only | `python -m pip install faster-whisper` (CPU int8 works; any STT producing the same words JSON can replace it) |

Missing optional dependencies produce a one-line install hint, never a traceback. Nothing is installed automatically.

## Data shapes

- **script.txt** — one VO line per text line; `[tags]` are ignored for alignment.
- **words JSON** — `[{"w": "word", "s": 0.34, "e": 0.61}, ...]` (from `check_take.py --words-dir`).
- **starts JSON** — one start time per script line: `[0.34, 3.25, 8.23]` or `[{"start": 0.34}, ...]`.
- **shifts JSON** — `{"<phrase onset s>": <shift s>}` (from `onsets.py --emit-shifts`; hand-editable).
- **cue sheet JSON** — see `../references/example_cue_sheet.json` and the header of `mix_cues.py`.
- **aliases JSON** (optional) — token map for names the STT spells differently: `{"acme cloud": "acmecloud", "2": "two"}`.

## Typical run (outputs into the active work folder)

```bash
W=.bequite/work/0007-launch-film/outputs/audio
python check_take.py --script $W/script.txt $W/takes/ --words-dir $W/words --srt
python place_lines.py --take $W/takes/voice_a.wav --script $W/script.txt --words $W/words/voice_a.json \
    --starts $W/starts.json --duration 57.35 --out $W/placed/voice_a.wav --report $W/placed/voice_a.json
python onsets.py --ref $W/scratch/scratch_placed.wav --new $W/placed/voice_a.wav --emit-shifts $W/placed/shifts_a.json
python phrase_sync.py --voice $W/placed/voice_a.wav --shifts $W/placed/shifts_a.json --out $W/synced/voice_a.wav --duration 57.35
python mix_cues.py $W/cues.json --voice $W/synced/voice_a.wav --out $W/auditions/01_voice_a.wav
python mix_cues.py $W/cues.json --out $W/mix.wav --stems $W/stems
python master.py --measure-only $W/mix.wav
```

Paste each command, its exit code and the key output lines into the work's `evidence.md`.

## Verified in this pack

All scripts pass `python -m py_compile` and `--help`. `place_lines`, `onsets`, `phrase_sync`, `voice_chain_compare`, `mix_cues` and `master` were run end to end on synthetic audio (ffmpeg 8.0.1, numpy 2.4, Python 3.14). `check_take.py` was not run end to end (faster-whisper not installed on the test machine): UNVERIFIED beyond compile and `--help`.
