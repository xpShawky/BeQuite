---
name: bequite-render-pipeline
description: 'Choose and drive the engine that builds and renders a motion film, then QC and deliver it. Tool-neutral engine decision (10 questions) with adapters for After Effects (ExtendScript bridge + aerender, AE path from BEQUITE_AE_PATH or auto-detected), Remotion and HyperFrames (HTML/React to MP4), Blender (3D, render passes, headless), DaVinci Resolve (edit, grade, deliver; Studio scripting/MCP), ffmpeg (frame studies, previews, reframes, captions, mux) and AI video as plates. Owns the render plan, cache/GPU/disk safety, and the delivery QC checklist with commands (black frames, loudness, size/fps, banding, phone readability). Use whenever a film or animation must be built, rendered, previewed, reframed to 9:16 / 1:1 / 4:5, encoded or checked, or when a render shows banding, black frames, blurry zooms or a 3D camera that does nothing.'
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

# bequite-render-pipeline — the right engine, a planned render, a checked file

The director decides *what* each shot needs (`bequite-motion-director`); this skill decides *which engine builds it*, writes the render plan, drives the engine, and proves the output with QC evidence. Named tools are adapters, never defaults: pick per project with written reasons, and re-check versions, licences and availability every run.

## When to use / when not to use

**Use:** M4 tool decision + render plan, M5–M6 builds and previews, M8 master render + QC, M9 reframes/encodes; engine problems (banding, black frames, blurry zooms, a 3D camera ignored, disk filling, aerender failing); "can this be done without After Effects?".

**Do not use:** story, style and pacing decisions (director); text-treatment choice (`bequite-kinetic-type`); audio processing and mastering (`bequite-sound-voice` — this skill only muxes and re-measures); web pages with scroll motion (`bequite-frontend-design-system`).

## Engine choice (detail + decision record: `references/engine-choice.md`)

| Capability needed | Candidate adapters | Adapter doc |
|---|---|---|
| scripted 2D/2.5D motion graphics, text animators, 3D camera, real motion blur, 16-bit | After Effects (ExtendScript + aerender) | `references/adapter-after-effects.md` |
| code-as-video, no paid app, React/HTML skills, versionable, CI-renderable | Remotion · HyperFrames · headless-browser frame capture | `references/adapter-html-video.md` |
| real 3D: products, devices, ribbons, materials, light, depth of field | Blender (bpy, headless, MCP) | `references/adapter-blender.md` |
| editing footage, colour grade, finishing, delivery presets | DaVinci Resolve (Studio scripting / MCP; free has limits) | `references/adapter-davinci-resolve.md` |
| study, previews, contact sheets, reframes, captions, mux, QC | ffmpeg (always) | `references/adapter-ffmpeg.md` |
| organic in-between shots, plates | AI video (plates only) | `.claude/skills/bequite-motion-director/references/ai-generation.md` |

Hybrids are normal (3D in Blender → assembly with real type in AE or code → grade/deliver in Resolve or ffmpeg). Decide per shot, record why the others were rejected, and never install anything without the user's yes.

## Render plan (✋ `RENDER_PLAN_APPROVED`)

Write `plan.md` from `references/render-plan-template.md` before any full render: engine per shot, comps/scenes, resolution, fps, bit depth, codec, expected time, disk + GPU budget, cache policy, paid credits with prices, fallback. The full-quality master render needs a separate yes at M8. Previews stay cheap: stills → contact sheet → 720p preview at the master's fps.

## Safety rules for every engine

- **Plan first; previews before masters.** A full render without an approved plan is a contract violation.
- **Never change the user's app preferences or security settings.** If an engine needs a setting ticked (AE scripting file/network access, Resolve external scripting), tell the user exactly where; they tick it.
- **Disk and GPU:** cap caches, purge before and after renders, check free disk before a master, watch for black frames from GPU out-of-memory.
- **No hardcoded paths:** AE via `BEQUITE_AE_PATH` or auto-detect (`assets/ae/aepath.js`); every other tool from PATH or a config value in `plan.md`.
- **Native resolution:** never downsample UI or product images for convenience; zooms expose it.
- **Licences:** paid apps (AE, Resolve Studio), company licences (Remotion), and AI credits are listed with prices in the plan.

## Assets and scripts

| Path | What |
|---|---|
| `assets/ae/runae.js`, `assets/ae/aerender.js`, `assets/ae/aepath.js` | Node bridge: run a .jsx in the open AE, render with aerender (+ purge), find AE without hardcoded paths (Windows; macOS via `osascript` — UNVERIFIED here) |
| `assets/ae/lib/core.jsx`, `assets/ae/lib/type.jsx`, `assets/ae/lib/json2.jsx` | ES3 library: tokens from Motion DNA, fixed easing, safe new-project guard, shapes, backgrounds, stills; kinetic-type toolkit |
| `assets/ae/build/purge.jsx`, `assets/ae/examples/hello_film.jsx` | cache purge; a minimal starter build |
| `.claude/skills/bequite-render-pipeline/scripts/qc_report.py` | delivery QC (format, black frames, freeze, loudness, true peak) → Markdown evidence block, PASS/FAIL |
| `.claude/skills/bequite-render-pipeline/scripts/contact_sheet.py` | labelled contact sheets from stills or from a video at chosen times |

## QC (✋ `FINAL_QC_PASS` requires all of it)

Checklist with commands: `references/qc-checklist.md` — automated (format, black, loudness after encode, fps/size) via `qc_report.py`, plus visual checks (banding, Motion DNA continuity on every section, phone readability, safe zones, honesty table, privacy list, licence ledger).

## Files this skill writes

In the active work folder `.bequite/work/<id>/`: `plan.md` (engine decision + render plan), `tasks.md` (per-scene build tasks), engine project files under `assets/` (e.g. `assets/ae/`, `assets/blender/`, `assets/remotion/`), `outputs/animatic/`, `outputs/previews/` (stills, contact sheets, 720p), `outputs/final/` (masters), `outputs/delivery/` (recuts, captions burned/side-car, covers), and `evidence.md` blocks for every render and check; one entry per run in `log.md`.

## Evidence rule

Every render and check is logged in `evidence.md` as **command + exit code + key output** (render time, frame count, ffprobe format line, black runs, LUFS/true peak). `qc_report.py --evidence <work>/evidence.md` writes this block. An engine feature you did not run in this session is reported as `UNVERIFIED:`; a version-specific claim cites the docs URL and date.
