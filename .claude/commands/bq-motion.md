---
description: 'Motion film studio (C18). Direct a product launch film, promo, ad, reel, explainer or kinetic-type piece like a motion director: references, script and beats, style lock, tool choice and render plan, animatic, build rounds, voice and sound, render and QC, platform recuts, launch posts and a making-of guide. Plan first; stops before paid credits, the final render and any posting. Tool-neutral (After Effects, Remotion/HyperFrames, Blender, DaVinci Resolve, AI video are adapters).'
---

# /bq-motion - direct a film, not "make an animation" (C18)

<!-- bq:contract -->
> **Every run follows the contract** (`.claude/bequite/docs/architecture/COMMAND_EXECUTION_CONTRACT.md`):
> 1. **Skills first:** announce the `Skill Selection:` block before any plan, edit or tool call for the task.
> 2. **Resolve the work:** read `.bequite/ACTIVE.md`; use `.bequite/work/<id>/`, or create the next work folder if this is new work (`/bq-work`).
> 3. **Gates:** project gates in `.bequite/state/WORKFLOW_GATES.md`, work gates in `work/<id>/gates.md`. Refuse and name the missing gate.
> 4. **Plan first:** non-trivial work gets a plan the user approves before output. Hard human gates always wait for a yes.
> 5. **Evidence:** every check goes to `work/<id>/evidence.md` (command + exit code + output) or is marked `UNVERIFIED:`.
> 6. **Write back:** `work/<id>/log.md`, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, and `.bequite/state/MISTAKE_MEMORY.md` when a lesson surfaced.
> 7. **Finish** with the Next Command Recommendations block.
<!-- /bq:contract -->

The director brain is the skill `bequite-motion-director` (phases M0-M9, hard stops, honesty rules). Craft: `bequite-kinetic-type` (moving text, Arabic/RTL), `bequite-sound-voice` (voice, music, SFX, mix), `bequite-render-pipeline` (engine choice, adapters, render plan, QC). Reference films: `motion-library/` (repo of the user's studied references; `INDEX.md` first).

## Syntax

```
/bq-motion "<idea>" [length=30s] [aspect=16:9,9:16] [lang=en|ar] [refs=<file|folder|url>] [engine=auto|ae|remotion|blender|resolve|ai]
/bq-motion                     continue the active motion work from its next phase
/bq-motion M<n>                jump to a phase of the active motion work (gates still apply)
/bq-motion study <file|folder|url>   study reference films into motion-library (frames + breakdown + INDEX row)
/bq-motion recut <platform>    extra delivery recut (9:16, 1:1, 4:5, a 15 s cut ...)
/bq-motion post                launch posts + comment-to-DM plan + making-of guide (M9)
/bq-motion status              phase, motion gates, open notes, next step
```

Examples: `/bq-motion "Launch film for BeQuite v4, Apple-style, 45s, 16:9 + 9:16"` · `/bq-motion "Reel for our clinic booking app in Arabic" lang=ar` · `/bq-motion study motion-library/inbox/`.

## Steps

1. **Skills first.** Announce `Skill Selection:` (always `bequite-motion-director`; add kinetic-type, sound-voice, render-pipeline, writing-dna, localization-rtl, presentation-builder as the phase needs).
2. **Work.** If the active work is not a `motion` work, create one (`/bq-work new "<idea>" type=motion`), which turns the motion gates on in `gates.md`. Everything this command makes lives under `.bequite/work/<id>/` (`brief.md`, `research.md`, `spec.md`, `plan.md`, `tasks.md`, `review.md`, `evidence.md`, `assets/`, `outputs/`).
3. **Run the next phase** per `bequite-motion-director`:

| Phase | Output | Stops for the user |
|---|---|---|
| M0 Brief | `brief.md`: goal, audience, the one feeling, platforms, length, budget/credit ceiling, assets, what the product really does today, tools on this machine | asks only the questions that change the plan |
| M1 References | 2-3 options from `motion-library/INDEX.md` ("we could do it like X, or like Y, because ...") + any new references studied | - |
| M2 Script + beats | script, story shape, beat sheet (≤ 3 s per beat), per-line type treatment, honesty check | ✋ `SCRIPT_APPROVED` |
| M3 Style lock | 2-3 styleframes of the same key frame → Motion DNA | ✋ `STYLE_LOCKED` |
| M4 Tool + render plan | engine per shot with reasons, render plan, disk/GPU budget, every paid credit priced | ✋ `RENDER_PLAN_APPROVED` |
| M5 Animatic | timing with a free scratch voice; stills + contact sheet | - |
| M6 Build rounds | contact sheet + phone-size preview per round; version table | ✋ `PICTURE_LOCKED` |
| M7 Voice + sound | auditions in the mix, music edit to picture, sparse SFX, master −14 LUFS | ✋ before any paid credit · ✋ `AUDIO_APPROVED` |
| M8 Render + QC | ✋ yes before the full master; QC commands + output in `evidence.md` | `FINAL_QC_PASS` |
| M9 Delivery | real recuts per platform (reframed, not letterboxed), captions, posts (Instagram, TikTok, Facebook, LinkedIn), comment-to-DM plan, making-of guide | ✋ `DELIVERY_APPROVED` · the user does all posting |

4. **Plan first, always.** In auto mode the run may continue through M0-M1 and the M5-M6 build rounds, but it always stops at M2, M3 and M4 so the user approves the plan before anything is built, and at every other ✋.
5. **Before you claim a phase is done**, show the evidence: contact sheet paths, preview paths, QC command + output. A phase without evidence stays open.

## Honesty and safety

- Never show a feature, number or result the product does not have today; official logos are placed from the official files, never redrawn or generated.
- No paid voice, music, stock or AI-video credit without a priced yes. Check licences and record them in `evidence.md`.
- Third-party reference films stay in `motion-library/inbox/` (local only, gitignored); studies describe and analyse, never copy.
- Posting, DMs and uploads are always done by the user.

## Write back

`work/<id>/log.md` per phase · `review.md` version table · `evidence.md` for every render/QC check · lessons (what the user rejected and why) to `.bequite/state/MISTAKE_MEMORY.md` · new reference studies to `motion-library/INDEX.md` · `.bequite/state/LAST_RUN.md` · `.bequite/logs/AGENT_LOG.md`.

## Next Command Recommendations

During the film: `/bq-motion` (next phase). After `DELIVERY_APPROVED`: `/bq-motion post`, then `/bq-work close`. For a website that should carry the same look: `/bq-feature` with the web-motion layer (`bequite-frontend-design-system`). For a slide version: `/bq-presentation`.
