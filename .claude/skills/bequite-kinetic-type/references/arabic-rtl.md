# Arabic and RTL kinetic type

Most important first: **Arabic is a connected script — animate whole words (or whole glyph clusters), never single letters; reveals and sweeps run right → left; and check every Arabic frame on a still, because shaping breaks silently.** General Arabic/MENA localisation (register, digits, dates, icon mirroring) is owned by `bequite-localization-rtl`; this file covers only text that moves. Rules marked UNVERIFIED were not tested in this pack.

## 1. Connected script: the unit is the word

- Arabic letters change shape by position (isolated / initial / medial / final). If each letter becomes its own animated box (per-character spans with transforms, per-character text animators, letters as separate layers), the shaping engine sees isolated letters and the word falls apart into disconnected forms.
- So: write-on, pop, smear and stagger **by word**. In AE use `o.by: "word"` (range selector "Words"); `kinetic.js` switches to words automatically when it detects Arabic-block characters.
- For a "writing" feel inside one word, don't split it — reveal the **unsplit** word with a mask or clip that sweeps right → left (a soft-edged wipe), or use a recolour/gradient sweep. The glyphs stay joined because the text itself is never cut.
- Per-letter treatments that only make sense in Latin (letters falling out of line, letter pop, per-character blur waves) have no Arabic equivalent; choose a word-level treatment that carries the same meaning.
- Diacritics (tashkeel) and dots sit above/below the line: give masks extra padding top and bottom (`kinetic.js` mask-rise pads 0.25 em), and keep line-height ≥ 1.5 on display text.
- Ligatures (e.g. lam-alef) are single glyphs; an emoji or a combined mark is a single grapheme. Never cut inside them.

## 2. Direction

- Reading order starts at the **right**. Stagger in logical order (first word = rightmost) — DOM order / AE text order already is logical order.
- Sweeps, wipes, underline draws and recolour sweeps travel right → left. Text "entering" naturally comes from the right side (it moves toward the reading direction's end).
- Typing grows leftward; the caret sits at the **left** end of the text (`K.typeOn(..., {rtl: true})`, `Kinetic.typeOn` handles it via the text's direction).
- "Forward" in RTL motion grammar is leftward: progress bars fill right → left, step-by-step whips move right → left. Mirror directional motion, never mirror logos, media icons, clocks or check marks.
- Start-align (right-align) quotes and comments in RTL; centred lines stay centred.

## 3. Kashida (tatweel, U+0640)

- Kashida elongates the connection between joined letters. It is a justification/calligraphic device, not a free "stretch" effect.
- Do **not** insert kashida to animate "stretched" meanings or to fill width in display lines — it changes how the word reads, looks amateur when mis-placed, and breaks search/copy of names.
- It is only valid between two letters that connect; never after non-joining letters (ا د ذ ر ز و) and never inside brand names.
- For a "stretch" meaning in Arabic, scale the whole word on X (`scaleX`), exactly as in Latin.
- Fonts differ in how (and whether) they draw kashida; if a designer insists on calligraphic elongation, use a font designed for it and check every frame.

## 4. Mixed-direction lines (Arabic + Latin brand names, numbers)

- Wrap embedded Latin runs (brand names, product names, code) in a bidi isolate: HTML `<bdi>` or `unicode-bidi: isolate` / `dir="ltr"` on the span. Without isolation, punctuation and numbers jump to the wrong side.
- Treat the Latin run as one unit in the stagger (it reads left → right inside the right-to-left line).
- Punctuation at the end of an Arabic sentence sits on the **left**; the Arabic question mark is ؟ and the Arabic comma ، .
- Digits: decide once per project (Arabic-Indic ٠١٢٣ vs Western 0123) — `bequite-localization-rtl` records the decision. Numbers inside Arabic read left → right; count-ups keep that order.
- In After Effects, RTL paragraph direction and the Middle Eastern text engine are set in the UI (Preferences → Type and the Paragraph panel); controlling them from script is **UNVERIFIED** — set them by hand once, then check stills.

## 5. Fonts

- Choose a family that has both Arabic and Latin designed together (consistent weight, x-height and rhythm), and record the pairing in the Motion DNA. Examples to evaluate (open-licence families commonly used for Arabic UI and display — **verify each licence and glyph coverage before use**): IBM Plex Sans Arabic, Noto Sans Arabic / Noto Kufi Arabic, Cairo, Tajawal, Readex Pro, Almarai, Alexandria, Rubik.
- Arabic glyphs look smaller than Latin at the same point size: size Arabic display text ~10–20 % up and test on a phone.
- **Never apply tracking (letter-spacing) to Arabic** — it breaks the joins. Set tracking 0 for Arabic runs even if the Latin style is tightened.
- Avoid ultra-light weights for Arabic on video; thin strokes and dots disappear after compression.
- Kufi-style faces read more geometric/tech; Naskh-style faces read more traditional/editorial — pick by the film's feeling.

## 6. Timing

- Use the same hold formula (max(1 s, 0.35 s × words + 0.5 s), ×1.5 when not spoken). Arabic words are often longer; if a native reader can't read the line twice, hold longer rather than shrinking text.
- The voice-over drives timing: write each word as it is spoken (word timings from `bequite-sound-voice` speech-to-text with the right language).
- Validate with a native reader on a phone before `PICTURE_LOCKED`.

## 7. Captions and burn-in

- `.srt` captions work for Arabic as plain UTF-8 text; the player shapes it.
- Burning in with ffmpeg: prefer the `subtitles`/`ass` filter (libass, which shapes Arabic through its text-shaping stack) with an Arabic-capable font; plain `drawtext` shapes Arabic only in builds with text-shaping support (a build detail — **UNVERIFIED** per machine; test one frame first).

## 8. Checklist (per Arabic/RTL line)

- [ ] unit = word (or cluster); no per-letter split anywhere
- [ ] sweep / wipe / typing direction right → left; caret on the left
- [ ] no kashida added; tracking 0 on Arabic runs
- [ ] Latin runs isolated; punctuation on the correct side; digits per the project decision
- [ ] masks padded for marks; nothing clipped on stills
- [ ] font pairing recorded; size checked on a phone
- [ ] a native reader confirmed readability and joins on a still and on the preview
