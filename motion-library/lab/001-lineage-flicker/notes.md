# Lab 001 — lineage flicker (version cards in one position, accelerating cuts, riser into a hit)

**Date:** 2026-11-12 · **Tool:** After Effects 2026 (26.2) via the BeQuite ExtendScript bridge + aerender; sound in numpy; mux and loudness in ffmpeg · **Time:** about 25 min including two tool fixes · **Credits:** none

## Reference
Apple Event Sep 2026 at 07:10.9-07:11.8 (`refs/apple-event-sep26`): chip generations A15 → A16 → … cut every 3 frames in exactly the same position, accelerating into "the fastest chip ever put in an iPhone". Also the MacBook Neo film 00:08-00:11 (same top-down framing, colour changes per cut).

## Hypothesis
A version history (BeQuite v0.1 → v4 "Titan") told as same-position cards, holds shrinking 18 → 12 → 8 → 6 → 4 → 3 frames, a slow push carried across every cut, a riser that dies on the landing frame and a sub hit on the land, reads as "evolution, accelerating into now".

## Recipe (reproducible)
- `build_lineage.jsx` (run: `node <render-pipeline>/assets/ae/runae.js build_lineage.jsx --root .`): 1920x1080, 30 fps, 5 s; one null "push" scales 100 → 106 % from 0.5 s to the land (2.2 s), then eases back to 100 % in 0.7 s (the settle); each card = rounded-rect shape + version text (Geist Bold 260 px) + a one-word subtitle, parented to the push; layers trimmed per hold.
- `make_sound.py`: riser = exponential sine sweep 180 → 1400 Hz + band noise, gain x^2.2, cut dead at the land; a 25 ms click on each flicker cut; the hit = sub sine falling 100 → 30 Hz with a 0.45 s decay plus a 20 ms noise transient; master with `loudnorm=I=-14:TP=-1`.
- Render: `node <render-pipeline>/assets/ae/aerender.js --project lineage.aep --comp LINEAGE --output render/lineage.mov` (AE 2026's default output module writes H.264 `.mp4`).

## Measured (film_study.py on `render/lineage_final.mp4`)
- 7 cuts found, 6 tagged `graphic-match + position-locked`: the mechanism registers like Apple's.
- Hit measured at 2.18 s (true 2.20 s).
- Only 1 of 7 cuts lands on a detected onset: the cut clicks are masked by the riser.

## Result: PARTLY WORKED
- Worked: the position-locked flicker and the acceleration read clearly; the push across the cuts keeps it alive; the bridge, aerender and the measurement loop all work end to end.
- Did not work: the look. Flat coloured cards read as a template, not as Apple; Apple's flicker works because each frame is a lit, photographed object with texture. The cut clicks disappear under the riser.

## Next attempt
1. Give each card material: a subtle gradient, a specular light sweep that continues across the cuts (the light moves on, the object changes), a soft contact shadow; or render the cards as 3D objects in Blender with one moving key light.
2. Make the cut ticks cut through: brighter (2-6 kHz) and about 6 dB above the riser at that moment, or duck the riser 3 dB on each tick.
3. Try the flicker against a music bed at a known BPM with the holds snapped to beat subdivisions (eighths → sixteenths), then measure the beat-grid hit rate.

## Tool lessons (written back into the pack)
- `aerender` will not create the output folder ("Directory does not exist"): `aerender.js` now creates it.
- `film_study.py` missed colour swaps at similar brightness (it found 2 of 7 cuts): it now also cuts on colour-histogram jumps (skipping very dark frames, where flame flicker looks the same).
- `film_study.py` reported onsets about 46 ms early (frames timed at their start): now timed at the window centre.
- SF Pro is not installed on this machine (and its licence covers Apple-platform design only); Geist is.
