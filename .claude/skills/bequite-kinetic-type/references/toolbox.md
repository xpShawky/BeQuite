# The kinetic-type toolbox

Most important first: **pick from this list by meaning, give each line one entrance + at most one emphasis + one exit, and keep one treatment consistent within a scene.** Numbers are starting values from real reviews; tune by eye on a phone. "AE" = function in `.claude/skills/bequite-render-pipeline/assets/ae/lib/type.jsx` (+ `core.jsx`); "Web" = function in `../assets/kinetic.js`.

## 1. Blur-in write-on (headline, turning point)
- **Look:** units arrive in reading order out of a soft blur, rising a little (≈0.26 em), scale 82 → 100 %, with a soft trailing bounce (≈+7 % then settle). Reads as "keynote".
- **Params:** sentence sweep 0.5–0.65 s; blur 12–14 px; unit = character (Latin) / word (connected scripts).
- **AE:** `K.say(comp, segs, cx, y, t0, t1, o)` (lays out + writes; `o.by: "word"` for Arabic). **Web:** `Kinetic.writeOn(el, {dur:0.6})`.

## 2. Mask slide-up (calm, editorial)
- **Look:** each word rises from behind its own baseline mask; 0.35–0.5 s, strong ease-out, 40 ms stagger.
- **Watch:** pad the mask for ascenders, descenders and Arabic marks, or they clip.
- **AE:** `K.maskRise(comp, segs, cx, y, {tIn, per})`. **Web:** `Kinetic.maskRise(el)`.

## 3. Directional smear (energetic)
- **Look:** a word travels 150–300 px in 4–6 frames with heavy horizontal motion blur, lands with 2–4 % overshoot. Per-character horizontal smear with a wave = louder variant.
- **AE:** `K.reveal(layer, t0, dur, "smear", {dx})`. **Web:** `Kinetic.smear(el)` (CSS has no directional blur; it approximates with scaleX stretch + blur).

## 4. Scale punch (one emphasis word)
- **Look:** the word scales 1.25 → 1 with a short hold, often with a colour change on the beat; failure words add red + a tiny card shake (≤ 10 px).
- **AE:** `K.punch(layer, t, 125, 0.35)`. **Web:** `Kinetic.punch(el)`.

## 5. Word → icon swap
- **Look:** a word collapses into a glowing pill/rectangle that morphs into an icon (or the reverse); the rest of the sentence re-flows smoothly.
- **Build:** text unwrite + a rounded-rect whose size/roundness animates + the icon popping in at the rectangle's centre; swap on the fastest frame.
- **AE:** `K.rect` size/round keys + `K.pop` / `K.ICON.*`. **Web:** two spans + `Kinetic.growIn` on the icon.

## 6. Letter pop (brand moment)
- **Look:** letters pop in ~35 ms apart (scale 0 → ~128 % → 100 %), last glyph may wobble; optional light shine sweep after.
- **Latin only** — connected scripts pop by word.
- **AE:** `K.pop(layer, t0, dur)` + `K.shine(...)`. **Web:** `Kinetic.letterPop(el)`.

## 7. Swap in place (lists, alternatives)
- **Look:** a prefix stays; one slot swaps its word (old rises out, new rises in from below inside the same mask); the line re-centres and the new word rides the same glide; optionally the final word changes colour.
- **Params:** glide 0.3–0.35 s; keep the voice's pause between swaps visible.
- **AE:** `K.swapLine(comp, prefix, words, cx, y, tIn, times)`. **Web:** `Kinetic.swapInPlace(slot, words, {every})`.

## 8. Recolour sweep (one key word)
- **Look:** after the word is written, its colour sweeps to the accent in reading order (permanent).
- **AE:** `K.recolor(layer, t0, dur, hex)`. **Web:** `Kinetic.recolour(el, {to})` — a gradient clipped to the text, so no letter splitting (safe for Arabic).

## 9. Inline icon
- **Look:** an icon grows inside the sentence ("Made for 🔊 calm"), its details build one by one; later the icon and the next word swap together ("🎙 talk").
- **AE:** shape layers placed with the layout widths from `K.lay` + `K.pop`. **Web:** `Kinetic.growIn(iconEl)` (animates width so the line re-flows).

## 10. Typing with a caret (chat, search, command)
- **Look:** characters appear one by one at a human rhythm (pauses after spaces and punctuation), caret follows and blinks after.
- **AE:** `K.typeOn(comp, str, x, y, t0, t1, {rtl})` (Source Text expression + caret on `sourceRectAtTime`). **Web:** `Kinetic.typeOn(el, text, {cps})`.

## Also in the kit
- **Underline/outline drawn while the word writes** — a trim-path line (`K.line(...).end` keys) or a CSS `background-size` underline.
- **Do it to the word** — stretch (scaleX 150 %), box (outline rect), misalign (`K.misalign`, Latin only), wrong font (only when the meaning is "wrong fonts").
- **Pills with swapping labels** — `K.pillSwap(comp, cx, cy, items)`.
- **Exit / unwrite** — `K.unwrite(lay, t)` / `Kinetic.unwrite(el)`.
- **Living hold** — `K.push(...)`, `K.drift(...)` / `Kinetic.drift(el)`.

## Rejected patterns (from real reviews)
- every line rising bottom → top word by word ("not smooth", monotone)
- slide/fade only on every line ("cheap")
- 30 fps stepped CSS with per-scene easing and no blur ("bounces not smooth")
- text appearing before the voice says it, or an empty card waiting for text
- mixed fonts on a word that must be read normally
- springs on text that must be read immediately

## Studying type in a reference
At 4 fps contact sheets, per line write: entrance (type + duration), emphasis, exit, hold, words on screen, alignment, colour change. Steal the idea, not the look.
