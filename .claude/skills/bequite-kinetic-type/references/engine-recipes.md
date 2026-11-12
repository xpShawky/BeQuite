# Engine recipes for kinetic type

Most important first: **the treatment is chosen by meaning (`toolbox.md`); the engine is chosen per project (`bequite-render-pipeline`).** These recipes show how each treatment maps onto each engine. Easing values come from `.claude/skills/bequite-motion-director/references/motion-grammar.md`.

## After Effects (scripted)

Library: `.claude/skills/bequite-render-pipeline/assets/ae/lib/type.jsx` (needs `core.jsx`). Segments are `[text, kind, font?, color?]` with kind 0 plain · 1 accent · 2 failure red.

| Treatment | Function | Notes |
|---|---|---|
| layout only | `K.lay(c, segs, cx, y, o)` | centred, or start at `cx` with `o.just = "left"` |
| blur-in write-on | `K.say(c, segs, cx, y, t0, t1, o)` / `K.write` / `K.writeLay` | first unit starts at t0, last at t1; `o.by = "word"` for Arabic |
| mask slide-up | `K.maskRise(c, segs, cx, y, {tIn, per})` | |
| smear / pop / blur reveal | `K.reveal(layer, t0, dur, "smear" \| "pop" \| "blur" \| "rise", o)` | |
| exit | `lay.out(t)` / `K.unwrite(lay, t)` / `K.hide(...)` | |
| scale punch | `K.punch(layer, t, 125, 0.35)` | |
| letter pop + shine | `K.pop(layer, t0, dur)`, `K.shine(layer, t0, dur, hex)` | Latin only |
| swap in place | `K.swapLine(c, prefix, words, cx, y, tIn, times, o)` | `o.wMul[i]` for a stretched word |
| recolour sweep | `K.recolor(layer, t0, dur, hex)` | |
| typing + caret | `K.typeOn(c, str, x, y, t0, t1, {rtl})` | Source Text expression |
| misalign | `K.misalign(layer, t, amt, rot)` | Latin only |
| pills | `K.pillSwap(c, cx, cy, items, o)` + `K.ICON.*` | |
| living hold | `K.push(c, layers, cx, cy, t0, t1, amt)`, `K.drift(layer)` | |

How it works: one text animator per effect (opacity, blur, position, scale) with a range selector "ramp up" whose offset is keyed from −width to 100 %; a second "bounce" animator trails the first. Units: characters excluding spaces (default) or words. Starter build: `.claude/skills/bequite-render-pipeline/assets/ae/examples/hello_film.jsx`.

## Browser: HTML / CSS / JS (also the source for HTML-to-video renderers)

`../assets/kinetic.js` — no dependencies, Web Animations API, `prefers-reduced-motion` aware, word units for connected scripts, direction-aware sweeps. Open `../assets/kinetic-demo.html` through any local static server to see every treatment in English and Arabic.

For frame-accurate video renders, create animations paused and set `currentTime` from the renderer's frame clock (`Kinetic.seek(anims, ms)`), so each captured frame is deterministic.

**CSS-only blur-in by character** (when no JS is wanted; Latin only):

```css
.w span { display:inline-block; opacity:0; filter:blur(12px); transform:translateY(.26em) scale(.82);
          animation:k-in .42s cubic-bezier(.16,1,.3,1) forwards; animation-delay:calc(var(--i) * 28ms); }
@keyframes k-in { 75% { opacity:1; filter:blur(0); transform:translateY(-.02em) scale(1.03); }
                  to  { opacity:1; filter:blur(0); transform:none; } }
@media (prefers-reduced-motion: reduce) { .w span { animation:none; opacity:1; filter:none; transform:none; } }
```

**GSAP** (free since 2025 incl. SplitText — verify the current licence): `SplitText.create(el, {type: "words"})` for Arabic, `"chars"` for Latin; `gsap.from(split.chars, {opacity:0, filter:"blur(12px)", y:"0.26em", scale:0.82, stagger:0.028, duration:0.42, ease:"expo.out"})`. Install only after the decision is recorded (no auto-install).

## Remotion (React → MP4)

Everything is a function of the frame number: `const f = useCurrentFrame(); const {fps} = useVideoConfig();`. Per unit `i`: `const p = interpolate(f - start - i * staggerFrames, [0, durFrames], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.bezier(0.16, 1, 0.3, 1)})` → opacity `p`, blur `(1 - p) * 12px`, translateY `(1 - p) * 0.26em`. Use `spring({frame, fps, config: {damping: 14}})` only for things that land. Split Arabic by words (`text.split(/(\s+)/)`), Latin by graphemes (`Intl.Segmenter`). Remotion's licence terms apply to companies (`bequite-render-pipeline` adapter).

## Other engines

- **Blender:** text objects need an Arabic shaping workaround (Blender's text object historically did not shape Arabic — **UNVERIFIED** for current versions); prefer compositing type from AE/web over the 3D render.
- **DaVinci Resolve / Fusion:** Text+ with Follower modifier for per-character offsets (Latin); words for Arabic. Treat as an option, not a default.
- **Rive / Lottie:** good for interactive web type; check per-character support and RTL shaping in the target runtime before choosing.

Whatever the engine: check the result on stills at each beat and on a phone-size preview; Arabic lines get the `arabic-rtl.md` checklist.
