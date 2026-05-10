---
name: bequite.impeccable-craft
description: Invoke a specific Impeccable command (craft / teach / document / extract / shape / critique / audit / polish / bolder / quieter / distill / harden / onboard / animate / colorize / typeset / layout / delight / overdrive / clarify / adapt / optimize / live). Loaded skill at skill/skills-bundled/impeccable/. Saves before/after screenshots as evidence.
phase: P5 | P6
persona: frontend-designer
loaded_skill: skill/skills-bundled/impeccable/
---

# /bequite.impeccable-craft <impeccable-command> [args]

When invoked (or `bequite design craft|polish|...`):

## Step 1 — Validate

Frontend Doctrine must be loaded. Argument must be one of the 23 Impeccable commands:

`craft, teach, document, extract, shape, critique, audit, polish, bolder, quieter, distill, harden, onboard, animate, colorize, typeset, layout, delight, overdrive, clarify, adapt, optimize, live`

If not, refuse — list valid commands.

## Step 2 — Snapshot before

Save before-screenshots to `evidence/<phase>/<task>/screenshots/before/`. Capture viewport 360 + 1440. For mena-bilingual: also locale `ar-*` (RTL).

## Step 3 — Invoke Impeccable

Load `skill/skills-bundled/impeccable/` and dispatch to the named command. The command operates on the file(s) the user specifies (or the active feature's frontend by default).

## Step 4 — Snapshot after

Save after-screenshots same locations under `screenshots/after/`. Visual diff (manually-reviewed; automated diff in v0.6.0+).

## Step 5 — Run `/bequite.design-audit`

Confirm the change moved metrics in the right direction:

- Anti-patterns reduced.
- axe-core findings reduced.
- Tokens-only adherence improved.

## Step 6 — Per-task commit + receipt

Conventional Commits: `style(<task_id>): impeccable <command> on <component>`. Receipt records before/after screenshot paths + the Impeccable command applied.

## Step 7 — Update state

`state/recovery.md`, `.bequite/memory/activeContext.md`. The `progress.md::Evolution log` notes the design pass.

## Stop condition

- Before + after screenshots saved.
- `/bequite.design-audit` shows improvement (or doesn't worsen).
- Per-task commit landed.
- Receipt emitted.

## Anti-patterns

- Skipping before-snapshots (no proof of improvement).
- Running multiple Impeccable commands in one invocation (do one at a time so the diff is attributable).
- Auto-committing without user confirmation (UI changes are visible — user sees them).

## The 23 Impeccable commands (brief)

- `craft` — apply Impeccable's design language to a section.
- `teach` — explain why the current state is or isn't good.
- `document` — produce design notes for a component.
- `extract` — pull a pattern out of one component into a reusable token / variant.
- `shape` — adjust shape language (border radius, corner profiles).
- `critique` — point out issues without fixing.
- `audit` — comprehensive scan.
- `polish` — small refinements (contrast, spacing, alignment).
- `bolder` — increase visual weight.
- `quieter` — reduce visual weight.
- `distill` — simplify a noisy component.
- `harden` — add edge-case states (loading, error, empty, disabled).
- `onboard` — first-time-user / onboarding flow refinement.
- `animate` — motion design (eased, never bounce/elastic).
- `colorize` — colour palette pass.
- `typeset` — typography pass.
- `layout` — grid / flex / responsive pass.
- `delight` — small interactive flourishes.
- `overdrive` — push a component to its emphasised extreme.
- `clarify` — wording / labels / microcopy.
- `adapt` — responsive variants (mobile / tablet / desktop).
- `optimize` — performance (bundle size, render).
- `live` — interactive preview / playground for a component.

## Related

- `/bequite.design-audit` — find issues to remediate.
- `/bequite.validate` — Phase 6 validation including frontend gates.
