# Voice-over: choose, direct, process, sync

Most important first: **audition the whole script inside the full mix; process with WSOLA speed only (≤ 1.15×) and light EQ, no heavy compressor; move phrases to the picture inside silence.** The pick changed once the candidates were heard in the mix, and the "robotic" texture was only obvious on a phone.

## 1. Human or AI

AI TTS is good enough for many calm, informative product reads. A human still wins for brand hero films, emotional reads, and anything where one mispronounced or robotic word would hurt. A common middle path: animate to a free scratch read, then replace with a paid AI or human read after `PICTURE_LOCKED`.

## 2. Scratch voice (free)

- Any free TTS reading the approved script: OS voices (Windows speech synthesis, macOS `say`), or a free tier used for timing only (check that timing-only use is allowed).
- Get word timings with `check_take.py --words-dir` → line starts for the animatic.
- The picture is timed to the scratch read; the final voice will be moved onto that timing (§6).

## 3. Choosing a voice (paid, after picture lock)

1. Shortlist 3–5 voices across several providers. Research what is current — this market changes quickly. Capability checklist per provider: commercial licence on your plan · language/accent · delivery control (style prompt, tags, stability) · output format and sample rate · API or web app · disclosure requirements.
2. Generate the **whole script** per voice (short lines hide pacing problems and quirks).
3. Put every candidate **inside the full mix** (music + SFX), audio only, same loudness, numbered, back to back + one file each (`mix_cues.py --voice <file>`).
4. The user picks by ear, on a phone and earphones.
5. Reset provider settings per voice; settings carried over from one voice to the next spoiled a round in the field case.

Provider landscape as found in late-2026 research notes (**UNVERIFIED now — re-check pages before paying**): several major TTS APIs offered prompt-directed delivery and inline tags; one provider documented that long "director's notes" blocks can make the voice drift; one required disclosing to listeners that the voice is AI; one long-standing TTS service shut down at the end of 2025; free tiers of popular TTS tools were non-commercial and required attribution. Record the provider, model, plan and terms URL with the date in the licence ledger.

## 4. Directing the read

- **One-line character:** who speaks, to whom, where. "A calm senior engineer showing a colleague a tool that saved her a week. Warm, confident, unhurried, never salesy."
- **Pace as a number:** ≈ 2.3–2.6 words per second for a calm product film.
- **Stress 1–2 words per line**, no more (capitals or the provider's emphasis syntax; underline for humans).
- **Pauses with punctuation or pause tags**, not stage directions.
- **Tags:** one per line at most (e.g. `[warmly]`, `[curious]`, `<short pause>` — syntax per provider). One tag for the whole read sounds flat; dots between every line sound choppy. Tags guide the read but do not control it exactly.
- **Describe delivery, not emotion level.** Stacked adjectives ("excited, passionate, inspiring") and low-stability/expressive settings produced laughs and sighs that killed takes. Words like "flat" or "quiet" can push a model into monotone.
- **Names:** spell phonetically in the script with a pronunciation note ("NY-kee, rhymes with *sky*"), generate 3–5 variants, verify each with speech-to-text, let the user choose.
- **3–5 takes per line or per read;** comp the best phrases.
- Direction tags in `[square brackets]` are ignored by `check_take.py`/`place_lines.py` alignment, and flagged if the voice reads them aloud.

## 5. The de-robot fix (measured, not guessed)

Field case: a voice sounded robotic on a phone and earphones but fine on PC speakers. Measured with cepstral peak prominence (clarity; lower = rougher) and harmonic warble:

| Cause | Effect |
|---|---|
| phase-vocoder time-stretching (e.g. Rubber Band-style) | clarity dropped (≈ 1.37 → 1.22 in that case) |
| a fast compressor (≈ 10 ms) + a parallel presence band | warble increased |
| WSOLA `atempo` at the same speed | clarity kept |

**Rule:** speed with `atempo` (WSOLA) only, only on lines that don't fit, ≤ 1.15× (1.2× last resort); then the light chain `highpass=f=70,equalizer=f=5800:t=q:w=1.4:g=-1.5,equalizer=f=170:t=q:w=0.9:g=1.5`. No heavy/fast compressor, no parallel presence band (heavy compression exposes AI-voice artefacts). If the voice still sounds wrong: `voice_chain_compare.py make` → 4–6 numbered options → the user chooses by ear.

Earlier notes recommending a 3:1 voice compressor are superseded by this rule.

## 6. Splitting, placing, syncing (scripts)

1. `check_take.py --script script.txt takes/ --words-dir words/` — transcript vs script: missing/repeated words, tags read aloud, long gaps. Run on raw takes and again after placement.
2. `place_lines.py --take … --words … --starts starts.json --duration …` — splits at **energy silences** (STT word edges are approximate; cutting at them once clipped the start of a word), shortens long pauses inside silence, WSOLA only when a line overruns its slot, applies the light chain.
3. `onsets.py --ref <voice the picture was timed to> --new <placed voice> --emit-shifts shifts.json` — energy onsets (STT timestamps have different biases per voice).
4. `phrase_sync.py --voice … --shifts shifts.json` — moves whole phrases onto the picture's beats; result within ±0.12 s, no stretching. Prefer this over re-timing an approved picture.
5. Level-match the placed voice to the level the mixer expects before mixing.

If the picture must move instead: one time-warp table (anchor word → film time) applied to scene time-remapping and to the SFX cue times (engine side: `bequite-render-pipeline`).

## 7. Gotchas

- Some TTS downloads (e.g. 24 kHz WAVs) mis-seek with `ffmpeg -ss`; decode the whole file and slice by samples (the scripts do this). This once mislabelled a comparison — verify every audio slice by transcribing it.
- Keep API keys in `.env`, read them in code, never print them.
- Arabic and other languages: pass `--language` to speech-to-text; test the voice's pronunciation of brand names in that language.
