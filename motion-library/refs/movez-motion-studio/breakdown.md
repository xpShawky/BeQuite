# "motion study 02 / every frame is code" by Movez: breakdown

**File:** `inbox/old/Movez on X_ How to build motion design studio with Opus 5.5 ….mp4` · **Source:** creator post on X (part of a course pitch) · **Length / format:** 14.06 s, 1440x1440 (1:1), **60 fps** · **Studied from:** contact sheet + loudness (no cuts).
**Category:** UI micro-interactions · motion study · loop

## 1. The story in one line
One black "Generate" button morphs through a dozen interface states and comes back to itself: **"every frame is code"**.

## 2. Story shape
A seamless **loop**: start state → a chain of transformations → the start state again. No narrative; the craft is the story.

## 3. Beat sheet
| Time | What we see | Technique |
|---|---|---|
| 0.0–1.5 | "Generate" pill → pressed → spinner → check | state change with squash and settle |
| 1.5–4.0 | the pill stretches into a music-player pill, then expands into a player card (scrubber moves) | **shared-element morph** (the same black shape grows) |
| 4.0–5.5 | the card collapses into a volume slider being dragged | morph to a smaller component |
| 5.5–6.5 | toggle switch flips | |
| 6.5–7.5 | segmented control Day → Week → Month | selection pill slides |
| 7.5–10.0 | it grows into a chart card; numbers **count and roll** (84,320 → 48,353 → 19,204); hover tooltip on the line | number animation, data morph |
| 10.0–12.0 | a command palette: types "fr" → "frame" → selects "Every frame is code" | typing + list filter |
| 12.0–14.0 | the selection becomes a pill "✓ Every frame is code" → shrinks back to "Generate" | **loop closes** |

## 4. Signature techniques
- **Shared-element morphing:** one black shape is the continuity, like the arc in the Claude films, but for UI.
- **60 fps with real cursor movement:** micro-interactions look real, not keyframed.
- **Monochrome on warm off-white**, one gradient accent (the album art). Very restrained.
- **Sound:** steady −13 LUFS bed with soft click SFX on every interaction.

## 5. When to use this style
- **Fits:** app and web product demos, design-system showcases, landing-page hero loops, social loops (1:1 / 4:5), **website micro-interaction motion**.
- **Avoid when:** you need emotion or story; this is pure craft.
- **Cost:** low-medium if built in code (React/Motion, GSAP, Remotion, HTML; it is literally "every frame is code"). It doubles as real website UI.

## 6. What to steal
1. **One element that morphs through every state**: for BeQuite, a command pill that becomes a plan card, a task list, a gate check, a verified badge, and back.
2. **Loop design:** end exactly on the first frame so it can play forever on a landing page or a social feed.
3. **60 fps and a real cursor** for UI motion.
4. **Numbers that roll** to show change (gates passed, files checked).
