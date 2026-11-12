# Music, SFX, mix and master

Most important first: **edit the music to the picture (drop on the logo hit, breath before it), one SFX per gesture, voice is king, master −14 LUFS integrated / ≤ −1 dBTP and re-measure after encoding.** Everything below is driven by one JSON cue sheet (`.claude/skills/bequite-sound-voice/scripts/mix_cues.py`, example `example_cue_sheet.json`), so a new cut or a new voice is a data edit.

## 1. Music

**Choosing**
- After the animatic timing exists. Pick for **structure** first (intro → build → drop → resolve), mood second, genre last.
- 4–6 commercial-safe candidates (licence checked first, `licences.md`); keynote/product films often sit around 90–120 BPM with clear sections. Offer 2–3 to the user in context (over the animatic), at equal loudness.

**Beat grid**
- Find BPM, downbeats and key (any beat tracker, or by ear + a click). Frames per beat = fps × 60 ÷ BPM (60 fps: 120 BPM = 30 frames, 100 BPM = 36; non-integer tempos drift — re-snap every few bars).

**Editing to picture** (edit the music, not the picture)
- quiet intro under the opening
- a darker, low-passed bed under the problem section
- a near-silent **breath** (≈ −60 dB for ~0.3–0.5 s, or a riser into silence) right before the reveal
- **the drop exactly on the logo-hit frame** (trim or loop bars so a downbeat lands there)
- open groove under the demo
- drums out, pad + final hit on the end card
- cut on bar lines, crossfade 10–30 ms on the downbeat so edits are invisible

## 2. SFX

- **One sound per gesture**, not per element: six items landing = one cascade. ~80 cues on a 40 s film was "annoying"; ~60 sparse, varied cues on a 57 s film worked.
- A hero moment gets three layers: **pre** (riser/reverse swell 0.3–1 s before), **hit** (transient), **tail** (reverb/shimmer). Everything else is one layer.
- Vary repeats: ±1–3 semitones, ±3 dB, never the same sample twice in a row.
- Tonal elements (plucks, chimes) tuned to the music's key; a rising pentatonic run across a feature list was a highlight.
- Timing: whooshes start a few frames before the motion peak; SFX 1–3 frames **before** the visual hit (late sound reads as lag); a sample's peak is placed on the cue time (`"peak"` in the cue sheet).
- High-pass whooshes (~150 Hz) so they don't fight the voice or kick; low-pass what sits behind dialogue; trim a sample's second impact if it masks a word.
- Leave 2–3 moments with no SFX so the hits land.
- UI sounds short, soft, ~8–12 dB under the voice.

## 3. Mix levels

| Element | Level |
|---|---|
| voice | reference (king) |
| music under voice | ≈ 10 dB under (10–20 for dense music); ducked ~4–8 dB (default 5.5) under each phrase, attack ~60 ms, release ~300–350 ms |
| music without voice (intro, drop, end card) | back up near voice level |
| SFX | ≈ 8–12 dB under the voice, ducked ~4 dB while speaking; 1–2 hero hits punch through |

Check stems: voice-to-music gap while speaking; no SFX louder than the voice except intended hits. Phones lose low end: give hits some 100–200 Hz, not only sub.

## 4. Master and loudness

**Target: −14 LUFS integrated, ≤ −1 dBTP true peak** (one file safe on every social platform; louder files get turned down and lose punch). `master.py` aims at −1.2 dBTP to keep margin after AAC encoding.

| Platform | Target | Evidence quality |
|---|---|---|
| YouTube | −14 LUFS, −1 dBTP | widely measured (no official help page found) |
| Instagram / Facebook | −14 (some guides −16), −1 dBTP | the platform normalises but publishes no number |
| TikTok | −14 (some −16), −1 dBTP | no published target |
| LinkedIn | −14 to −16, −1 dBTP | no loudness spec; autoplays **muted** |
| Broadcast (only if aired) | −23 LUFS (EBU R128) / −24 LKFS (ATSC A/85) | formal standards |

Method: two-pass `loudnorm` (measure, then apply linear with the measured values) + a limiter with `level=disabled`; then **re-measure the final MP4 after the AAC encode** (`master.py --measure-only` or `qc_report.py` in `bequite-render-pipeline`). Deliver AAC 48 kHz stereo 256–320 kb/s; keep the WAV mix and stems (vo / music / sfx) for re-cuts.

## 5. Listening QA

- Phone speaker, earphones and a laptop — not only studio/PC speakers.
- Muted autoplay check: does the film work with captions only?
- Options always as audio-only files, equal loudness, numbered.

## 6. Sound checklist

- [ ] music licence proof saved and covers the real use (organic / client / paid ads)
- [ ] voice plan commercial; disclosure rule checked
- [ ] drop on the logo downbeat; edits on bars; breath before the reveal
- [ ] one SFX per gesture; hero moments 3 layers; 2–3 silences; SFX 1–3 frames early
- [ ] voice ~10 dB over music, ducked per phrase
- [ ] master −14 LUFS / ≤ −1 dBTP measured, and re-measured after encoding
- [ ] phone + earphones listen; captions `.srt` delivered
- [ ] stems + WAV archived in `outputs/audio/`
