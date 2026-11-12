# MacBook Pro with M5 Pro and M5 Max (Apple): breakdown

**File:** `inbox/New/MacBook Pro with M5 Pro and M5 Max.mp4` · **Source:** owner-provided (Apple product film) · **Length / format:** 100.2 s (≈94.2 s of picture + 6 s silent tail), 1280x720, 23.976 fps · **Studied from:** metrics, director sheet, contact sheets at 0.5 s (opening), 0.2 s (type), 0.75 s (ending), `matches.jpg`, second-pass sync test (67 detector cuts → 74 edits). Not played back by ear.
**Category:** product launch · filmed narrative · kinetic type

## 1. The story in one line
A writer stuck on a blank page, surrounded by people doing heavy creative work on the same laptop, finally writes; every spec is *typed* out of the keyboard. It feels warm, human and quietly powerful.

## 2. Story shape
Blank page (problem) → a day in a library → "Introducing" → a montage of pros, one spec each, all typed → render and code crescendo → release (a stretch, a smile) → title over a wide → logo → silence. **A small human arc wrapped around a spec montage.**

## 3. Beat sheet
| Time | What we see | What we hear | Technique | Why it works |
|---|---|---|---|---|
| 00:00.0-02.6 | white page, an orange text cursor blinking | near silence (0.28-0.95), single key clicks | blank page opener | the problem in one image |
| 00:02.6-10.3 | the writer's face (2.63), a finger hesitating over keys (4.17), a high wide of the library (6.38), fingers typing (8.4) | silences 3.62-3.97; key clicks are the only rhythm | ASMR keyboard as score | silence makes the clicks the music |
| 00:10.3-15.0 | "A day u…" typed on the white page (10.5-11.5); back to her; the line deleted to "A da" (14.0) and back to the bare cursor (14.5) | silences 12.68-17.81 broken only by clicks | **typed-and-deleted cursor** | writer's block shown, not told |
| 00:15.0-18.3 | she walks the stacks (motion carried across the cut at 15.48), sits, looks down | | motion carried across the cut | |
| 00:18.3-27.2 | typing hands; "Introducing the new MacBook Pro" floats over the laptop (23.6); then "Now with M5 Pro" **appears letter by letter, each letter popping out of the keyboard on a keystroke**, spread on a rising diagonal (24.2-26.2) | the music bed enters around 18 s (loudness steps up on `timeline.png`); key clicks stay on top | **keystroke type** | the spec is literally typed by the user |
| 00:27.2-60.0 | montage of pros at work: a coder, a pathologist (microscopy on screen), a lab, a designer seen top-down ("Starting at 1TB of storage", 46.9), a robot designer, "Up to 2x faster SSD", "Up to 5x faster graphics", "And M5 Max" (53) | edits every ~1.3 s; 14.64 / 15.47 / 20.94 / 24.19 / 30.36 / 31.32 / 35.24 / 37.79 / 38.37 / 41.42 / 55.81 / 57.46 on top-10 % hits | keystroke type over each world; lateral moves carried across cuts (30.38, 41.44, 41.98) | one spec per person, all from the same gesture |
| 00:60.0-79.0 | a red apple on a desk (59), a film set with a MacBook on a rig, "Up to 128GB of unified memory" (64.5), node graph, "Up to 8x faster AI performance" (74.2); a robot render **steps from dark → wireframe → shaded yellow in the same framing** (76.15 / 76.36 / 76.49, 0.2 s and 0.1 s) | 72.03 on a top-10 % hit; silence pocket 61.18-62.09 | **position-locked ladder** (render-pass ladder) | the render finishing is felt as three ticks |
| 00:79.0-89.7 | code, a progress bar, the writer again (83-84), a man stretching in his studio (84-86), "Our best performance yet" typed over a hand (87.7-89.3) | the bed winds down (silences 89.56-91.77) | release beat | the crescendo resolves into a breath |
| 00:90.0-95.2 | the writer smiles (90); a wide tableau of her in the library with "The new MacBook Pro / with M5 Pro and M5 Max" (91.3-94.5) | sudden drop at 92.93 | title over the story's wide | the product name lands on the resolved story |
| 00:95.2-100.2 | black, a white Apple logo, legal line | silence 94.16-100.08 | silent tail | |

## 4. Signature techniques
- **Transitions:** hard cuts at 44 per minute (the fastest Apple film here), held together by gesture (hands on keys in every world) and by motion carried across cuts (6 tagged, motion cosine 0.94-1.0). Two confirmed position-locked cuts: the render ladder (76.15-76.49) and the top-down designer (46.9).
- **Typography:** the signature. Letters appear one per keystroke, scattered on a diagonal in screen space over the filmed keyboard; "Introducing" in italic beside an upright line. Small (≈3-4 % frame height), white, no boxes. The opening uses a real text-editor cursor in the product's orange.
- **Camera:** filmed, shallow depth of field, warm practicals; mixed moves (push-in 13 %, pull-out 10 %, lateral 11 %, locked 20 %); 9 shots end with the move dying before the cut.
- **Colour and background:** warm amber library and studios, cool blue only on screens.
- **Pacing:** ASL by quarter 1.67 / 1.39 / 1.32 / 1.32 s: fast and even once the music is in; the first 18 s are the slow part.
- **Sound:** −14.0 LUFS, **LRA 10.0 LU** (the silent typing opening against a full bed), true peak −2.0 dBFS. Tempo unclear (152 BPM at confidence 1.9; 112 BPM from a second estimator), UNVERIFIED. Cuts on strong onsets ×1.07 (n.s.), low booms at cuts ×1.40 (p = 0.086). Picture change vs sound onsets: cross-correlation z = 2.8 at +12 ms: the typed letters pop with the key clicks, which is where the sync lives. No voice.

## 5. When to use this style
- Fits: tools people *type* into (editors, terminals, IDEs, AI assistants, BeQuite itself); 60-100 s; a human face makes it suitable for a brand film.
- Avoid when: you cannot film or source convincing people and hands; under 30 s (the blank-page set-up needs ~15 s).
- Cost and difficulty: medium-high for the shoot (hands, several locations); the keystroke type itself is cheap in AE (per-letter reveal keyed to click SFX markers).

## 6. What to steal (adapt, never copy)
1. **Keystroke type:** every claim is typed, one letter per key click, the letters rising from the keyboard. For BeQuite: claims typed into a terminal, each character on a click, the output lines appearing on a soft tick.
2. **Blank page → typed and deleted → silence:** an opener that states the problem in 10 s without words.
3. **Silence first, music at 18 s:** let the product's own sound (keys, a prompt beep) be the score before the bed arrives.
4. **Render-pass ladder:** dark → wireframe → final in the same framing, 0.1-0.2 s per step.
5. **One gesture across all worlds** (hands on the same keyboard) so a 44-cuts-per-minute montage still reads as one film.

## 7. Open questions / UNVERIFIED
- Music tempo and whether the key clicks are production sound or designed SFX: UNVERIFIED.
- The exact typeface of the keystroke type: UNVERIFIED.
