# WORKED EXAMPLE — the PlateMaker launch film (one real project)

> **This is a labelled worked example, not a rule set.** It records one film made by an agent-plus-client pair in 2026, so later films can learn from real verdicts. The rules it produced live in the skills' main files; the client is called "the client" here and collaborators are not named. Measurements come from a later study of the delivered files; motion smoothness and audio feel were judged by the client, not re-verified.

## The job

- **Product:** PlateMaker, a Photoshop (UXP) plugin that builds scientific figure plates (microscopy photos + scale bars + insets + labels).
- **Film:** 57 s, 16:9, 60 fps, 2560×1440 master; 720p phone preview; a 9:16 reel; a 14-page 4:5 making-of PDF; posts for four platforms.
- **Built with:** After Effects driven 100 % by ExtendScript from the agent (zero hand-set keyframes), ffmpeg + Python/numpy for all audio, speech-to-text for timing.
- **Effort:** 14 versions in about 2.5 days, made possible by cheap previews (stills → contact sheet → ~6 MB 720p preview on the client's phone).
- **Measured on the master:** −14.0 LUFS integrated; black only in the intended final fade; scene detect found 3 hard changes in 57 s — the film is almost entirely continuous (whips, blurs, in-scene moves).

## Version table (client verdicts, summarised)

| v | What it was | Verdict | Lesson (now in the skills) |
|---|---|---|---|
| 1 | HTML/JS frame renderer, 9:16 portrait, 30 fps, ~80 SFX, synth music, no voice | rejected: wrong format, cheap type, bounces not smooth, annoying sound, no voice | deliver the screen output in the agreed format; text needs treatments; 60 fps + real blur; one sound per gesture; a voice carries the story |
| 2 | first scripted AE build; one "marching ants" guide element | liked a lot | one guide element ties a film together; scripted AE works end to end |
| 4 | two external-AI critiques merged; blue/purple blobs; colour wash over the photos | look rejected; demo rushed | neutral + one accent; never colour-wash real images; honest demo order |
| 5 | client's own story in real sentences; neutral greys + one light blue | "not smooth": every line rose word by word; tour too fast; plate blurry on zoom | vary the treatment per line; demo pacing; native-resolution pixels |
| 6 | kinetic-type toolkit; 3D camera; full-res plate | much better | collapsed precomps ignore 3D cameras; the hold-key ease bug |
| 7 | faster writing (0.5–0.65 s per sentence) | a wait still too long; **banding** in dark gradients | follow speech rhythm; 16 bpc + 2K export |
| 8 | comment-style quote written on the voice rhythm | **picture approved** | lock picture before any paid credits |
| 9–10 | final voice + two music edits; a name mispronounced, then spelled phonetically | music chosen; name fixed | generate several pronunciations; judge in the mix |
| 11–13 | a second, more energetic AI voice | "robotic texture" heard on the phone | measured: phase-vocoder stretch + fast compressor caused it (see `bequite-sound-voice`) |
| 14 | 10-voice audition, full script, each inside the full mix | final: calm voice, light EQ, **no compressor** | calm keynote delivery beats energetic; audition inside the mix |

The HTML engine was not the real reason v1 failed: a code renderer can look premium. AE was the faster route for this client to text animators, a 3D camera and real motion blur. The engine is a recorded decision, never a default.

## What the client accepted / rejected

**Accepted:** character write-on (blur → sharp, small rise, soft bounce) for the turning line; a different treatment on every line serving the meaning (a word swap in one slot, "stretched" stretched, "square" boxed, letters of "nothing lines up" falling out of line, a typed AI prompt with a caret, a key word recoloured, "rejected" turning red with a punch); a full stop that grows into the app icon (match cut); an underline drawn as a product name is written; pills that swap labels; a slow 3D camera over the result; a constant 0.5–1 % drift.

**Rejected:** portrait/POV framing; every line rising word by word; a camera tour at 0.16 s per stop ("nothing visible"; ~0.55 s worked); downsampled images (blurry on zoom); AI-generic blobs; coloured overlays on scientific images; mixed fonts on a word that must read normally; empty waits; fragment copy.

## What a later frame study found (honest critique)

About 6.5/10 on an Apple-launch scale, 8/10 for a solo, script-built explainer: it has the *grammar* of premium motion (one family, one accent, restraint, motivated whips, a pause before the reveal, a match cut, 60 fps + blur, banding-free 2K) but not the production value (no real light, materials, depth of field or 3D space).

Weaknesses to avoid next time:
1. **Middle monotony** — the same imagery carried ~35 s; change scale, texture or subject about every 10 s.
2. **Small type on a phone** — cards filling 25–40 % of the frame looked elegant at 2K and small on a phone.
3. **The 9:16 was a letterbox** — the film used only ~32 % of the vertical height, and the call-to-action box used a different accent colour and square corners than the film. → real recuts; delivery assets use the film's system.
4. **Demo honesty drift** — the film showed annotation features the first shipped build only partly had. → honesty table at M2, re-checked at M8.
5. **Delivery hygiene** — two files named FINAL (one stale); the phone preview at 30 fps while the master was 60.

## Process that worked

Picture first with a free scratch voice → client approves → voice → music + SFX → mix → masters. A plan file per version with a resume checklist (sessions stopped several times). External AIs used for critique, never obeyed. Keys in `.env`, never printed. Privacy list enforced throughout (only images the client was allowed to publish).
