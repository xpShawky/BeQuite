# Phase playbook and artefact templates (M0–M9)

Most important first: **each phase ends with a file in the active work folder, and the ✋ phases end with the user's explicit yes recorded in `gates.md`.** A session can stop at any moment; the files are the memory. Keep `log.md` current so the next session can resume from the last line.

Studios run the same order every time — brief → script → moodboard → styleframes → storyboard → animatic with scratch voice → lock → rough pass → polish → sound → reviews → delivery (School of Motion project guide; Giant Ant: "client problems are almost always process problems"). M0–M9 is that order with BeQuite gates.

---

## M0 Brief → `brief.md`

Ask only what you cannot infer. One page.

```markdown
# Brief: <film title>
- Product / subject:            (what it is, in one sentence)
- What it really does today:    (features that ship NOW; anything else is off-limits on screen)
- Audience:                     (who, what they already know)
- The one thing to remember:    (single takeaway; if you can't name it, don't start the script)
- The one feeling:              (relief · power · delight · trust · calm · urgency)
- Platforms + formats:          (16:9 master? 9:16 recut? 1:1 / 4:5? cut-downs 15/30 s?)
- Length:                       (target seconds)
- Voice:                        (none / scratch only / final VO: language, gender, register)
- Deadline:
- Budget + credit ceiling:      (money and paid credits allowed; 0 = free tools only)
- Assets supplied:              (logo files, UI captures, footage, fonts, brand guide)
- Privacy list (never show):    (unpublished data, people, client names, keys, internal URLs)
- Must-show / must-say:
- Tools on this machine:        (from bequite-render-pipeline detection: AE/aerender, Blender, Resolve, Node, ffmpeg, Python libs, fonts)
- Assumptions made:             (auto mode: every guess logged here)
```

## M1 References → `research.md`, `assets/refs/`

Method: `studying-references.md`. Output per reference: what to take (named: "this easing", "this word swap"), what to avoid, timestamps. End with **2–3 options** phrased as choices: "We could do it like A (why) or like B (why)."

## M2 Script + beats → `spec.md` · ✋ `SCRIPT_APPROVED`

```markdown
## Script
(real sentences, 5–9 words each; read aloud with a stopwatch)
30 s ≈ 65–75 spoken words · 60 s ≈ 130–150 words at a calm ad pace (≈ 2.3–2.6 words/s)

## Story shape
(problem → failed alternatives → turn → product → proof → call to action → sign-off, or another shape from story-and-pacing.md)

## Beat sheet
| # | Time | Picture (what we see) | VO / on-screen text | Text treatment | Transition out | Sound idea |
|---|---|---|---|---|---|---|
| 1 | 0.0–2.4 | | | (from bequite-kinetic-type) | | |

## Honesty check
| Claim on screen or in VO | True today? | Evidence (doc, build, measurement) |
|---|---|---|
```

Rules: each beat ≤ 3 s of new information; 12–20 beats per 60 s; every claim has a "yes + evidence" row or is cut.

## M3 Style lock → `spec.md` § Motion DNA, `assets/styleframes/` · ✋ `STYLE_LOCKED`

Make 2–3 styleframes of the **same** key frame (a hero line + the product), named and side by side, each with one line of rationale. The user picks one (a BeQuite variant-winner hard gate). Then lock:

```markdown
## Motion DNA
- Stage(s):            (solid neutral by default; a gradient needs a brand reason)  hex:
- Accent (ONE):        hex · what it marks in each shot · ≈5–8 % of the frame
- Semantic colours:    (red = failure only, etc.)
- Type:                one family, ≤ 2 weights, tracking values, size scale at master resolution AND checked at phone size
- Grid:                columns, margins, base unit
- Depth:               one shadow recipe · glass on at most one layer
- Background:          plain / living (what moves, how slowly)
- Look:                graphic / filmed (lens, grain, DOF, grade)
- Easing set:          2–3 named curves + spring rule (motion-grammar.md)
- Camera language:     (drift amount, push-ins on interactions, whip speed)
- Transition grammar:  (which transitions this film uses and why)
- Guide element:       (what it is, where it ends up)
- Banned list:         (e.g. purple→blue gradients, glowing blobs, colour washes over real images, lens flares)
```

## M4 Tool decision + render plan → `plan.md`, `tasks.md` · ✋ `RENDER_PLAN_APPROVED`

Owned by `bequite-render-pipeline` (engine table, adapters, render-plan template at `.claude/skills/bequite-render-pipeline/references/render-plan-template.md`). The director's part: say per shot what the shot needs (text animators? 3D camera? real lens? organic simulation?), then let the engine follow. Price every paid credit and subscription in the plan; nothing paid runs without this gate.

`tasks.md`: one task per scene + one per sound step + QC + delivery, each with the skills it uses and an execution profile.

## M5 Animatic → `outputs/animatic/`

- Free scratch voice (OS TTS or any free TTS) reading the approved script → word timings (`bequite-sound-voice` `check_take.py`) → beat times.
- Block every beat with flat cards and real text at the right times. Timing first; no polish.
- Stills at each beat + one contact sheet; then a small preview (720p, a few MB).

## M6 Build + review rounds → `outputs/previews/`, `review.md` · ✋ `PICTURE_LOCKED`

Loop: build scene → stills → contact sheet (look at it yourself first) → fix → 720p preview → user watches **on a phone** → notes → next version.

```markdown
## Version table
| v | Date | What changed | User verdict (their words) | Lesson |
|---|---|---|---|---|
| 1 | | | | |

## Resume checklist (for the next session)
- Last good version: v_  · file:
- Open notes: 1. … 2. …
- Next action:
```

Translate notes before changing anything: "too fast" = the viewer can't read or see it; "not smooth" = monotone treatment or linear/default easing; "cheap" = generic treatment, AI-look, low resolution; "robotic" (voice) = measure it (`bequite-sound-voice`). Keep picture changes inside the approved Motion DNA; a new direction re-opens `STYLE_LOCKED`.

## M7 Voice + sound → `outputs/audio/` · ✋ paid credits · ✋ `AUDIO_APPROVED`

Run by `bequite-sound-voice`. Director's part: present options as numbered, equal-loudness, audio-only files inside the full mix; record the pick and the licence of every asset.

## M8 Render + QC → `outputs/final/`, `evidence.md` · `FINAL_QC_PASS`

✋ Ask before the full-quality master render (time, disk, GPU). QC checklist and commands: `.claude/skills/bequite-render-pipeline/references/qc-checklist.md`. Add the director checks: every section still meets the Motion DNA (no middle-of-film drift), every claim matches the honesty table, privacy list honoured, text readable on a phone.

## M9 Delivery → `outputs/delivery/` · ✋ `DELIVERY_APPROVED`

`delivery-and-social.md`. The agent prepares files and text; posting, DMs, automation setup and account settings are always done by the user.

## After the film

Add accepted / rejected lessons to `.bequite/state/MISTAKE_MEMORY.md`, add any newly studied reference to `motion-library/`, and close the work (converge: every acceptance criterion in `spec.md` has evidence).

---

## Pre-production checklist

- [ ] One-page brief with privacy list and "true today" features
- [ ] 2–3 reference options offered; the picked one studied from frames
- [ ] Script read aloud and timed; honesty table complete → `SCRIPT_APPROVED`
- [ ] 2–3 styleframes, one picked; Motion DNA written → `STYLE_LOCKED`
- [ ] Engine per shot decided with reasons; render plan + costs → `RENDER_PLAN_APPROVED`
- [ ] Animatic watched at full speed with scratch voice

## Licence ledger (keep in `plan.md` or `outputs/audio/`)

| Asset | Source | Licence / plan | Covers (organic / client / paid ads / broadcast) | Proof saved (file/URL + date) |
|---|---|---|---|---|
