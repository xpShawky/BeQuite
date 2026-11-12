---
name: bequite-sound-voice
description: 'Sound for promo, product and explainer films: voice-over choice and direction, scratch voice first and paid voice only after picture lock, auditions inside the mix, the de-robot fix (gentle WSOLA time-stretch up to 1.15x, light EQ, no heavy compressor), splitting / placing / phrase-syncing a read to an approved picture, music edited to picture with the drop on the logo hit, sparse tuned SFX, mixing and mastering to -14 LUFS and <= -1 dBTP, captions from word timings, and licence checks. Ships parameterised Python scripts (ffmpeg + numpy). Use whenever a film needs a voice-over, music, sound effects, a mix or captions, or when someone says the voice sounds robotic, slow, too emotional or out of sync, wants to compare voices, or asks which TTS or music is safe to use.'
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, WebFetch, WebSearch
---

# bequite-sound-voice — sound that serves the picture

Order matters: **scratch voice → picture approved (`PICTURE_LOCKED`) → paid voice → music + SFX → mix → master (`AUDIO_APPROVED`).** No paid credit, subscription or licence purchase without a priced yes from the user (a BeQuite hard stop). Present every choice as numbered, equal-loudness, audio-only options **inside the full mix**, and let the user choose by ear on a phone.

## When to use / when not to use

**Use:** voice-over (TTS or human), voice processing and sync, music choice and edit, SFX, mix, master, captions from speech, licence questions for audio, "the voice sounds robotic / slow / too emotional / out of sync".

**Do not use:** picture timing and story (that is `bequite-motion-director`); video encodes and QC of the final file (`bequite-render-pipeline`, which re-measures loudness after encoding); podcast or meeting audio cleanup with no film.

## Voice in five rules (detail: `references/voice.md`)

1. **Scratch first:** a free voice (OS text-to-speech or any free TTS) with the final script times the animatic. Paid voice only after `PICTURE_LOCKED`.
2. **Audition properly:** shortlist 3–5 voices from several providers (check today's commercial terms), read the **whole script**, then hear each **inside the full mix**, same loudness, numbered. Reset provider settings per voice.
3. **Direct the delivery, not the emotion:** a one-line character ("calm senior expert showing a colleague a tool that saved her a week; warm, steady, never salesy"), pace as a number (≈ 2.3–2.6 words/s), stress 1–2 words per line, short tags; over-expressive settings produce laughs and sighs. Spell names phonetically and verify with speech-to-text.
4. **De-robot fix:** speed changes only with WSOLA (`atempo`), only where a line doesn't fit, **≤ 1.15×** (1.2× last resort); light EQ only (`highpass 70 Hz · −1.5 dB @ 5.8 kHz · +1.5 dB @ 170 Hz`); **no fast/heavy compressor**, no parallel presence band, no phase-vocoder stretching. When in doubt, measure (`voice_chain_compare.py`) and let the user choose by ear.
5. **Move the voice to the picture, not the picture to the voice:** split at energy silences, place on line starts, then move whole phrases inside silence onto the picture beats (±0.12 s), no stretching.

## Music, SFX, mix (detail: `references/music-sfx-mix.md`)

- Pick music for **structure** (intro → build → drop → resolve), then mood; 4–6 commercial-safe candidates, 2–3 offered in context.
- Edit to picture on a beat grid: quiet intro, darker bed under the problem, a near-silent breath (~0.5 s) before the reveal, **the drop on the logo hit**, open groove under the demo, outro on the end card. Cut on bars.
- SFX: **one sound per gesture**, not per element; vary repeats (±1–3 semitones, ±3 dB); tune tonal hits to the music's key; SFX 1–3 frames before the visual hit; leave 2–3 silences.
- Levels: music ≈ 10 dB under the voice and ducked ~5.5 dB under each phrase (attack 60 ms, release 350 ms); SFX ~4 dB ducked, only hero hits punch through.
- **Master: −14 LUFS integrated, ≤ −1 dBTP** (two-pass loudnorm + limiter); re-measure after the AAC encode. Listen on a phone and earphones, not only PC speakers.
- Captions: an `.srt` from the voice's word timings — feeds autoplay muted.

## Licences (detail: `references/licences.md`)

Save proof for every asset (track page, plan, date) in the licence ledger. Free tiers of many TTS and AI-music tools are non-commercial; stock-music "free for commercial use" can still trigger Content ID claims; subscriptions usually license the subscriber, not a client's paid ads; some TTS providers require telling listeners the voice is AI.

## Scripts (`scripts/`, run with `--help`)

| Script | Does | Needs |
|---|---|---|
| `check_take.py` | speech-to-text vs script: missing/extra words, tags read aloud, long gaps; saves word timings JSON + `.srt` | ffmpeg, numpy, faster-whisper (optional dep) |
| `place_lines.py` | split a full read into the script's lines at silences, shorten pauses, WSOLA ≤ 1.15× only if needed, place on line starts, light chain | ffmpeg, numpy |
| `onsets.py` | energy phrase onsets: reference voice vs new voice; emits a shift table | ffmpeg, numpy |
| `phrase_sync.py` | move whole phrases onto picture beats (cut in silence, no stretch) | ffmpeg, numpy |
| `voice_chain_compare.py` | numbered chain options + clarity score (CPP) to find a robotic texture | ffmpeg, numpy |
| `mix_cues.py` | JSON cue sheet → voice/music/SFX stems + mastered mix (example: `references/example_cue_sheet.json`) | ffmpeg, numpy |
| `master.py` | two-pass loudness master, or `--measure-only` | ffmpeg (stdlib only) |

Every script prints a helpful install line if an optional dependency is missing. Usage notes: `.claude/skills/bequite-sound-voice/scripts/README.md`.

## Files this skill writes

Into the active work folder `.bequite/work/<id>/outputs/audio/`: `scratch/` (scratch voice + word timings), `takes/` (raw paid takes), `words/` (timings, `.srt`), `placed/` and `synced/` voice, `auditions/` (numbered in-mix options), `cues.json`, `stems/`, `mix_raw.wav`, `mix.wav`. Licence ledger rows in `plan.md`; voice/music picks and the user's verdicts in `review.md`; one entry per step in `log.md`.

## Evidence rule

Every check and master goes to `evidence.md` as command + exit code + key output (match ratio and diffs from `check_take.py`; late lines and tempo range from `place_lines.py`; phrases outside tolerance from `onsets.py`; integrated LUFS / true peak / LRA from `master.py` or `mix_cues.py`). "Not robotic" and "in sync" are the user's verdict on a phone, recorded in `review.md`; the agent reports measurements, not impressions.
