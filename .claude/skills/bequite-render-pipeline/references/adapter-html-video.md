# Adapter: HTML / React to video (Remotion, HyperFrames, frame capture)

Most important first: **a code renderer can look premium — the failures in practice were design decisions (portrait framing, one entrance for every line, 30 fps without real blur), not the engine.** Build at 60 fps, deterministic per frame, with real motion blur, and the treatments from `.claude/skills/bequite-kinetic-type/assets/kinetic.js` or their framework equivalents.

## Options

| Option | Best for | How an agent drives it | Install / licence | Honest limits |
|---|---|---|---|---|
| **Remotion** | React developers; templated films; language/customer variants; CI renders | write compositions; preview in Remotion Studio; `npx remotion render <id> out.mp4`; official AI docs + agent skills (2026) | Node; free for individuals/small teams; a **company licence** applies above a team-size threshold (read remotion.dev/license before client work) | you build the motion vocabulary; motion blur via its blur components or sub-frame accumulation; WebGL/3D heavier |
| **HyperFrames** | agent-first HTML scenes → MP4 | `npx hyperframes@latest doctor`, `init <name> --example=blank`, `render`; ships its own agent skills (`skills update`); imports a word-timing transcript for subtitles (per a community setup guide) | Node (guide says ≥ 22); first render downloads a headless browser (~150 MB); **licence, maintainer and stability UNVERIFIED** — read the repo before use | young tool; not tested in this pack |
| **Frame capture (DIY)** | full control with any HTML/canvas/WebGL; no framework | expose `renderAt(t)`; a headless browser screenshots each frame (or N sub-frames for blur); ffmpeg encodes | Node + a headless browser (e.g. via Puppeteer or Playwright — install only with a recorded decision) | slowest; you own colour, timing and blur |

## Rules that make it look good

- **60 fps**, deterministic: everything is a function of the frame number (no `setTimeout`/real-time clocks during render). In `kinetic.js`, create animations with `{paused: true}` and set `currentTime` per frame (`Kinetic.seek`).
- **Real motion blur:** accumulate 4–16 sub-frames per output frame (shutter ~180°) for fast moves, or use the framework's blur; a 3-sample blur looked "not smooth".
- **Easing** from `.claude/skills/bequite-motion-director/references/motion-grammar.md`; springs only on landings.
- **Fonts:** load local font files (`@font-face`) and wait for `document.fonts.ready` before the first frame; Arabic needs an Arabic-capable font and word-level animation (`.claude/skills/bequite-kinetic-type/references/arabic-rtl.md`).
- **Resolution:** render at the master size (e.g. 2560×1440) or set `deviceScaleFactor` 2 on a 1280×720 layout; UI screenshots at native resolution.
- **Colour:** sRGB in, `yuv420p` out with `-color_primaries bt709 -color_trc bt709 -colorspace bt709` to avoid shifts.
- **Audio:** render silent, mux the mastered mix with ffmpeg (`adapter-ffmpeg.md`).
- **Recuts:** build compositions from layout tokens so a 9:16 version is a second composition with re-placed type, not a crop.

## Minimal frame-capture contract (DIY)

1. Page exposes `window.renderAt = (seconds) => { /* set every animation's state */ }` and `window.ready` (fonts + images loaded).
2. Capture loop: for frame `f` in `0..N-1`, for sub-sample `s` in `0..S-1`: `renderAt((f + s/S * shutter) / fps)` → screenshot; average sub-samples (or let ffmpeg `tmix` do it).
3. Encode PNG sequence with ffmpeg (`-framerate 60 -i f_%05d.png -c:v libx264 -crf 15 -pix_fmt yuv420p`).
4. Stills + contact sheet for review before the full sequence.

Evidence: log the render command, frame count, elapsed time and the `qc_report.py` block in `evidence.md`.
