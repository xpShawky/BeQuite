# Introducing Linear Agent (Linear): breakdown

**File:** `inbox/New/Introducing Linear Agent.mp4` · **Source:** owner-provided download (Linear launch film) · **Length / format:** 54.9 s, 1280x640 (2:1), 30 fps · **Studied from:** summary.md + director.md + 2 s contact sheet + extra frames at 2.5–6.5 s, 5–12 s, 20–24 s, 44.5–54.5 s + a re-run of scene detection at threshold 0.04 + per-0.5 s band energy of the audio.
**Category:** product launch · UI demo · software brand film

## 1. The story in one line
You type a request into Linear, Linear finds the issues, writes the plan and builds the document: "Linear. At your command." It feels quiet, expensive and in control.

## 2. Story shape
Prompt → result → second prompt → bigger result (doc, diagram, full app) → confirmation in chat → wordmark + tagline → glyph. One real task told end to end, no problem act, no people, no voice.

## 3. Beat sheet
Cuts below come from a re-run of scene detection at threshold 0.04 (3.1, 11.3, 17.1, 22.0, 29.8, 35.1, 40.7, 45.1 s). The standard pass found **0 cuts** because every shot is dark grey UI on black; all cuts are low-contrast.

| Time | What we see | What we hear | Technique | Why it works |
|---|---|---|---|---|
| 0.0–3.1 | Linear sidebar + "Project spec" page, UI plane tilted in perspective, shallow focus, near-black surround | quiet ambient bed, −38 → −30 dB, rising | perspective UI plane, slow drift | sets the product in one frame without a logo |
| 3.1–11.3 | camera slides down the same plane to the "Ask Linear" box; the prompt is typed live ("Find issues with loading performance", ≈12 characters/s, 7.0–10.0 s) | at the cut a **sub-bass swell**: 3.4–5.3 s, 98–99 % of energy below 150 Hz, peak ≈ −9 dB vs a −30 dB bed, then a sudden drop at 5.29 s back to the bed | live typing with cursor; sound hit one beat after the cut | the swell says "something powerful is about to happen" with no music cliché |
| 11.3–17.1 | answer: "I found 13 bug issues…", a list of ENG-xxxx issues with coloured status dots, rows resolving in | bed only (−29/−30 dB), small high clicks | result appears inside the real UI | the only colour in the film is in the status icons: the eye goes to the data |
| 17.1–22.0 | second prompt typed under the list ("Make a plan to refactor data loading to be optimistic") | bed | prompt → response rhythm repeated | the viewer now knows the grammar, so the second beat is faster |
| 22.0–35.1 | a document "Optimistic loading refactor" builds: title, overview, "At a glance" table, then a flow diagram of boxes draws itself (29.8–35.1) | bed, no hits | build-on of a document, then a diagram | shows the agent's output as an artifact, not a chat bubble |
| 35.1–40.7 | pull back: the whole Linear app with the doc and the side chat panel | bed | context reveal (wide after macro) | proves this is the real product, not a mock |
| 40.7–45.1 | chat close-up: "I created the PRD around the issues you surfaced… What can I help with next?" | second sub-bass swell 40.5–42.4 s (≈ −20 dB, 90–95 % below 150 Hz), drop at 42.5 s | callback to the first swell = sound bookend | marks "task done" |
| 45.1–50.0 | black; "Linear" alone (45.5), then "At your command." fades in grey and brightens to white (47.5–48.5) | a small low pulse at 45.0–45.5 s, then the bed fades | tagline completes the wordmark | the tagline reads as the agent's promise |
| 50.0–54.9 | Linear glyph, centred, small | fade out −35 → −59 dB, silence 53.9–54.8 s | glyph end card | ends in silence: confidence |

## 4. Signature techniques
- **Transitions:** soft, low-contrast cuts and camera slides along one continuous tilted UI plane, so 9 shots read as one move. No flashes, no whooshes.
- **Typography:** the film's only "type" is the product's own UI text plus one end line in a neutral grotesk, white on black, small (≈ 3 % of frame height). The tagline is built as wordmark + full stop + phrase, the phrase arriving in grey and brightening.
- **Camera:** virtual camera over a UI rendered as a flat plane in 3D (≈ 30–40° tilt, estimate), slow constant drift, shallow depth of field so only the active line is sharp. Camera label 100 % "locked-off" in summary.md is wrong for intent: the motion is slow and low-contrast, below the detector's threshold.
- **Colour and background:** near-black world, UI greys, colour only in status icons (yellow, red, green). One light source feel: the screen itself.
- **Pacing:** ASL ≈ 5.6 s over 9 shots (from the 0.04 re-run). Slow, even, no acceleration. The film trusts reading time.
- **Sound:** no voice, no melody to speak of (tempo confidence 1.87 = no steady beat), −28.9 LUFS integrated (very quiet; web embed, not normalised for social), LRA 11.4 LU. Two sub-bass swells (3.4 s and 40.5 s) are the whole sound design; everything else is an ambient bed.

## 5. When to use this style
- Fits: developer tools, AI agents, B2B software, any product whose output is text; launch pages and X posts where people watch on a laptop; 30–60 s.
- Avoid when: the audience does not already want the product (no hook, no human, no emotion), vertical social feeds (small grey text on black dies on a phone), sound-off autoplay with no captions.
- Cost and difficulty: low to medium. Real UI recorded or rebuilt in HTML/Figma, laid on a plane in AE (3D layer + camera + depth of field) or Blender; typing animated as text reveal. The craft is restraint and believable content (real-looking issue IDs, titles).

## 6. What to steal (adapt, never copy)
1. **The tilted UI plane with shallow focus:** BeQuite's terminal / `.bequite/work/` folder on one plane, the camera sliding from prompt to result.
2. **Prompt → artifact, twice:** first beat shows the grammar, second beat shows a bigger output (for BeQuite: `/bq-plan` → a plan file → gates turning green).
3. **Sub-bass swell as the only hit:** one low swell at the first prompt, the same swell when the job is done. A sound bookend instead of music.
4. **Wordmark + full stop + promise:** "BeQuite. <promise>." with the promise fading up grey → white.
5. **Colour only where the data is:** status colours (gates, pass/fail) are the only hue on screen.

## 7. Open questions / UNVERIFIED
- Whether the UI is live product capture or a rebuilt animation: UNVERIFIED (text is crisp at all angles, consistent with a rebuilt vector UI).
- The exact nature of the 3.4 s and 40.5 s sounds (boom, synth swell, or drum) is measured only as low-frequency energy, not listened to.
- Studio or in-house: UNVERIFIED.
