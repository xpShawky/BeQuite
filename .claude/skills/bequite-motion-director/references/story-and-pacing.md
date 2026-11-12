# Story and pacing

Most important first: **a new beat about every 2–3 s, each beat ≤ 3 s of new information, and breathing room before the moment that matters.** Fast is for transitions; slow is for anything the viewer must read or recognise. (Text write and hold times are owned by `bequite-kinetic-type`; this file owns beats, demos, transitions and the overall rhythm.)

## Story shapes

Pick one per film and write it in `spec.md`. Use real sentences, not fragments ("Six images. One plate." read as AI copy to a real audience).

| Shape | Beats | Fits |
|---|---|---|
| **Problem → turn → proof → brand** | pain the audience knows → failed alternatives (1–3) → "there's a better way" → product → real result → call to action → sign-off | tools, B2B, pro software, plugins |
| **Hero reveal** | context → tease (detail, macro) → pause → slow reveal → features ×3–4 → lockup | hardware, premium consumer products |
| **One thread** | one guide element (a light, a line, a shape) travels through every feature and lands in the logo | consumer apps with several features |
| **Before → after** | the messy "before" in real UI → one action → the clean "after", repeated 2–3 times | utilities, editors, automation |
| **Day in the life / POV** | a person's moment → the product appears inside it → the moment gets better | lifestyle, mobile apps |
| **Manifesto** | 5–7 short statements on one rhythm, product at the end | brand films, launches without a demo |

Hook with the proof (the real result, a real number) rather than a logo. Never open on "my first…".

## Beat pacing

- **12–20 beats per 60 s.** Social pace is about one beat every 2.5 s; a launch film can breathe more.
- **Burst, then settle:** a transition peaks for 0.3–0.6 s with motion blur, eases out over ~0.8–1.2 s, then a readable hold of 1–2 s.
- **Nothing fully static:** a 0.5–1 % camera drift or slow push on every hold. The one exception: the end card may be dead still.
- **Tempo variation is the point.** One surprise break mid-film (a sudden stop on a sound, a depth change) keeps a long piece from feeling relentless. Change scale, texture or subject about every 10 s so the middle never goes monotonous (the most common failure: the same imagery carrying 30 s).
- **The pause before the reveal:** 0.5–1 s of near-stillness and near-silence right before the hero moment / logo hit. Hold the key idea a little longer than feels comfortable.
- **End card holds 2.5–4 s** on a launch film (social cuts can go to ~1.6 s). The cheapest seconds in the film.

## Demos and UI

App-usage numbers (UI motion 100–500 ms; enter ≈225 ms, exit ≈195 ms) are for *using* an app. A viewer of a film has never seen the UI, so:

- One action per beat; taps and screen changes at ~1.5–2× app duration (≈0.4–0.6 s).
- Hold each result ≥ 1 s before the next action.
- Camera tours across UI: 0.6–1.0 s per stop, 1–2 s on the stop that carries the message (0.16 s per stop was "nothing visible" in the field case; ~0.55 s worked).
- Configure → press the button → the real result. Never show the result before the action.
- Zoom into the UI instead of shrinking it: a 2× crop of the panel in use beats a whole screen at 30 %. Keep UI at native resolution (`bequite-render-pipeline` adapters say how).

## Fast vs slow

| Fast (0.3–0.6 s, peak blur) | Slow (≥ 1.5 s, drift) |
|---|---|
| transitions, whips (6–10 frames), swaps, object wipes, emphasis punches | product hero, UI state, result, logo reveal, end card, any text that must be read |

Speed hides a cut; stillness lets the eye read. Never swap content on a hold.

## Templates

**60 s launch film**

| Segment | Time | Beats | Notes |
|---|---|---|---|
| Hook | 0–4 s | 1–2 | one striking move or the proof; no logo yet |
| Problem / context | 4–12 s | 3–4 | type-led; holds per the reading rule |
| Reveal | 12–18 s | 2 | the pause right before; slow 1.5–2 s entrance |
| Features ×3–4 | 18–48 s | 3 each | per feature: transform-in 0.5 s · demo 2–4 s · result hold 1–2 s · headline 1.5–2.5 s |
| Tempo break | inside features | 1 | one surprise |
| Wrap / lockup | 48–60 s | 2–3 | slower than the rest; end card 2.5–4 s |

**45 s:** 3 features, shorter problem. **30 s:** hook → one problem line → reveal → 2 features → lockup (65–75 spoken words). **15 s cut-down:** the single best moment (often the reveal or one transform) + lockup + CTA; re-edit, don't speed up.

## Pacing to music

Frames per beat = fps × 60 ÷ BPM (60 fps at 120 BPM = 30 frames). Land picture accents on beats; the logo hit on a downbeat. The music edit itself is `bequite-sound-voice`; decide the hit frame together in M5.
