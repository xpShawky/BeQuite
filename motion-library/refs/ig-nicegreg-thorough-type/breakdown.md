# "thorough" type study (nicegreg): breakdown

**File:** `inbox/New/Instagram (2).mp4` (original name) · **Source:** Instagram, nicegreg (https://www.instagram.com/p/Dd2Y1U9hjZs/; identified by the word "thorough" broken into three lines) · **Length / format:** 5.12 s, 1080x1350 (4:5), 23.976 fps · **Studied from:** shots.jpg, three fine contact sheets (`frames/c_open.jpg` 15 fps 0–1.2 s, `c_break.jpg` 16 fps 1.75–2.5 s, `c_morph.jpg` 15 fps 3.3–4.1 s), summary.md
**Category:** kinetic type (studio identity sting)

## 1. The story in one line
One word types on, grows, breaks into a stacked logo lockup with studio details, glitches once into a bubble-graffiti version and snaps back: a 5-second identity for a "design & motion studio".

## 2. Story shape
Type-on → grow → break/stack → settle with metadata → one surprise frame-swap → settle. A logo sting.

## 3. Beat sheet (frame by frame where it matters)
| Time | What we see | What we hear | Technique | Why it works |
|---|---|---|---|---|
| 0.00–0.27 | black | silence 0–0.49 s | hold | |
| 0.27–0.60 | "t" → "th" → "thoro" → "thorough" appears in red bold grotesk, small, centre. Four red corner crop marks appear at "th" and **re-hug the text bounds every step** | | **type-on with live bounding-box corners** | the crop marks make it read as "design tool / selection" |
| 0.60–1.0 | word and corners scale up together (ease-out) to full width | first low hit 0.49 | scale-up of the group | |
| 1.0–1.87 | hold full width | hit 1.25 | hold | reading time |
| 1.87–2.0 | in 1-2 frames the word splits into "tho / ro / ugh", each syllable stepped down and right (staircase); corner marks jump outward vertically | hit 1.76 | **syllable split into a staircase** | the word becomes a shape |
| 2.0–3.0 | group shrinks; the syllables close into a tight left-shifted stack; small mono text "DESIGN & MOTION STUDIO" above and "EST. 2024 PORTLAND, OR" below fades in with a flicker, each word placed on its own grid offset; ® dot appears | drop at 0.98 and quiet bed | **logo lockup with scattered mono metadata** | poster grid feel |
| 3.0–3.70 | hold the lockup | drop at 3.07 | hold | |
| 3.70–3.90 | about 5 frames: the wordmark is replaced by an inflated outlined "bubble/graffiti" version of the word, slightly rotated, bigger; metadata gone | | **substitution frames** (alt-logo flash) | a wink; shows range in one blink |
| 3.90–5.12 | snaps back to the clean stacked lockup, metadata gone, corners stay | tail | return | ending on the clean mark |

## 4. Signature techniques
- **Typography:** one red (#FF0000-like) heavy grotesk (Helvetica/Neue Haas-like, UNVERIFIED) on black, a small mono for metadata; the corner marks are the only other graphic.
- **Motion:** stepped, not tweened, at the key moments (type-on per frame, split in 1-2 frames); eased scale in between. Mixed easing = handmade feel.
- **Camera:** none (locked, one shot).
- **Sound:** −19.9 LUFS, true peak +1.7 dBFS (clips: an Instagram re-encode or a hot master), three low hits at 0.49, 1.25, 1.76 s; tempo unreliable (confidence 1.25). Not mixed for delivery.

## 5. When to use this style
- Fits: logo stings, title cards, chapter cards, 3-6 s; studios and dev tools with a one-word name.
- Avoid when: the word is long or needs to be read by a broad audience in under 1 s.
- Cost: low. AE: Text animator (range selector by character, Smooth off), a null-driven rectangle via `sourceRectAtTime()` for the corner marks, keyframed per-syllable layers, hold-keyframe substitution layer. Half a day.

## 6. What to steal
1. **Selection corners that re-hug text** on every type step (`sourceRectAtTime` expression on 4 corner shapes).
2. **Split a word into syllables on a staircase**, then compress into a stacked lockup.
3. **A 5-frame substitution** of an alternate logo before the final settle.
4. Scatter tiny mono metadata on an offset grid around the mark (BeQuite: "AI HARNESS · v4 · EST. 2025").

## 7. Open questions / UNVERIFIED
Typeface names; whether the bubble version is hand-drawn or a plugin; the sound clipping is from the source or the download.
