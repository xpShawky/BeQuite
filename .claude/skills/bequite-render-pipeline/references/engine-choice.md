# Engine choice

Most important first: **decide per shot from the capability it needs, then pick the simplest engine that delivers it on this user's machine and budget.** Record the decision in `plan.md` (format below). No engine is the default; After Effects is one optional adapter among several.

## Step 1 — what each shot needs

For every beat in the beat sheet, tick what it needs: per-character text animators · real motion blur · a 3D camera over 2D layers · true 3D objects, materials, light, DOF · photographic footage editing / grading · organic simulation (cloth, liquid, particles) · UI at native resolution · frame-accurate sync to voice/music · Arabic/RTL text shaping · interactivity (web).

## Step 2 — the 10 decision questions (BeQuite tool neutrality)

1. What is the project type (launch film, social reel, explainer, 3D product shot)?
2. What is the actual problem (which capabilities from step 1)?
3. What scale is expected (one film, a series, templated variants per language/customer)?
4. What constraints exist (OS, budget, licences already owned, deadline, no-install policy, GPU, disk)?
5. What stack already exists (the user's apps, a React codebase, a Blender habit)?
6. What viewing experience is required (60 fps, 2K/4K, HDR, vertical recuts)?
7. What failure risks exist (paid licence lapses, GPU OOM, disk cache, vendor churn, non-commercial licence)?
8. What tools are proven for this case?
9. What tools are overkill?
10. What gives the best output with the least complexity?

## Step 3 — adapter profiles

| Adapter | Best for | How an agent drives it | Install / licence | Honest limits |
|---|---|---|---|---|
| **After Effects** | scripted 2D/2.5D motion design, text animators, 3D camera, motion blur, 16-bit, broad plugin ecosystem | ExtendScript (ES3) run inside the open app (`runae.js`), `aerender` CLI for renders; UXP plugins in beta (2026) | paid subscription; Windows/macOS; the user must tick "Allow Scripts to Write Files and Access Network" | needs a running licensed app; ES3 only; ExtendScript end-of-life date unannounced; disk cache and GPU memory hazards; Arabic/RTL control from script UNVERIFIED |
| **Remotion** | code-as-video in React; templated/variant films; CI renders; data-driven | write React components, `npx remotion render`; official agent skills and AI docs exist (2026) | Node; free for individuals and small teams, **company licence above a size threshold** (check remotion.dev/license) | you build the motion system yourself (no text-animator UI); motion blur and 3D need extra work; heavy scenes render slowly on CPU |
| **HyperFrames** | HTML/CSS/JS scenes rendered to MP4 by an agent-oriented CLI | `npx hyperframes@latest init/render` (per its docs; ships its own agent skills); first render downloads a headless browser | Node ≥ 22 per a community setup guide; **licence and maintainer UNVERIFIED** — read the repository licence before client work | young tool; feature set and stability UNVERIFIED in this pack |
| **Headless-browser frame capture** | any HTML/canvas/WebGL scene, full control, no framework | step a `renderAt(t)` function per frame, screenshot with a headless browser, encode with ffmpeg; sub-frame sampling for motion blur | Node + a headless browser | you own timing, blur and colour management; slow; v1 of the worked example failed on design, not on this engine |
| **Blender** | true 3D: devices, products, ribbons, materials, light, DOF, render passes | `bpy` scripts, headless `blender -b -P script.py`, official/community MCP servers | free (GPL); GPU strongly recommended | aesthetic quality is on the director; render time; text shaping for Arabic UNVERIFIED — composite type elsewhere |
| **DaVinci Resolve** | editing footage, colour grading, finishing, delivery presets, audio post (Fairlight) | Python/Lua scripting API; native MCP server in Studio 21.1 (2026) | free version + paid Studio; since 21.1 external scripting is Studio-only (free keeps the console) | not a motion-design tool for kinetic type; destructive ops through MCP have no documented safeguards — dry-run on a copy |
| **ffmpeg** | studying references, previews, contact sheets, reframes, captions burn-in, mux, encode, QC | CLI | free; on PATH | not an animation tool; drawtext shaping of complex scripts depends on the build |
| **AI video** | organic in-betweens, start/end-frame bridges, plates | vendor API or web app | paid credits; terms per plan; lineups change monthly | never UI, text, logos, exact geometry; see `.claude/skills/bequite-motion-director/references/ai-generation.md` |

Version and licence facts above come from research notes dated November 2026; re-verify before writing them into a plan.

## Common decisions

- **The user owns AE and wants keynote-style type fast** → AE + `core.jsx`/`type.jsx`; ffmpeg for QC.
- **No paid apps / must run in CI / many language variants** → Remotion (check licence) or browser frame capture; `kinetic.js` treatments port directly.
- **Hero product in 3D** → Blender passes + assembly in AE or code; UI corner-pinned at native resolution.
- **Footage-led film (interviews, b-roll)** → Resolve for edit/grade; motion graphics from AE/code as overlays.
- **15 s social variant of an existing master** → ffmpeg recut if framing allows; otherwise re-render the scenes at 9:16 in the original engine.

## Decision record (in `plan.md`)

```markdown
### Engine decision: <shot or film>
- Problem: (capabilities needed)
- Options: (2-4 adapters)
- Sources: (docs URLs + date checked)
- Best option: …   Why it fits: …
- Why others rejected: …
- Risk: …   Cost: (licences, credits, render hours)
- Test plan: (a 3-5 s proof render before committing)
- Rollback: (the fallback engine)
```
