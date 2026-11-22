---
description: Generate multiple UI/UX design directions in isolation. 1-10 variants. Each lives in an isolated route (/uiux/v1) or component (src/uiux-variants/Variant01). Original UI untouched. User picks winner; agent merges. Produces UIUX_VARIANTS_REPORT.md.
---

# /bq-uiux-variants: several real directions, the user picks one

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Each variant is a different direction built from a different set of measured human references, not a colour swap of the same layout. The existing UI is not touched until the user picks. Procedure: `bequite-ux-ui-designer` (the Variants section) under `bequite-frontend-design-system`, with `bequite-frontend-quality` for the checks and `bequite-human-taste` for the reference study.

## Syntax

```
/bq-uiux-variants [count] ["<screen or scope>"] [style=<direction>]
```

Count: the number given (1 to 10); without one, 3 for a small or utility project and 5 for a design-critical one. Ten needs the user's confirmation, and never more. `style=` seeds every variant from one named direction (for example `style=3d`); the variants must still differ in direction within it.

## Gates

Needs `BEQUITE_INITIALIZED` and a frontend (or a new project whose stack is chosen). **Picking the winner is a hard human gate**: the command stops and waits. After the merge the Design DNA is updated and locked (`DESIGN_DNA_LOCKED`) and the merged screen passes `DESIGN_CONTINUITY_PASS`.

## Steps

1. **Read** the Design DNA if one exists, `PROJECT_STATE.md`, the spec, who the users are. State the screen the variants are for (the most-used one: the dashboard home, the landing page).
2. **References first.** For each direction, a different reference set of real products or sites, studied and measured (type scale, spacing, density, colour roles). Propose the directions in one line each, with who each suits, before building.
3. **Isolate** with what the project already has, installing nothing: routed previews (`/uiux/v1`, `/uiux/v2`), isolated components (`src/uiux-variants/Variant01/`), or Storybook stories if Storybook is already there.
4. **Build each variant** as one complete screen with real states (data, empty, loading, error) at phone and desktop width, with its own tokens. Every variant meets the same quality checks and the tell sweep.
5. **Compare** in `.bequite/uiux/UIUX_VARIANTS_REPORT.md`: each direction's references, strengths, weaknesses, screenshots at both widths (`.bequite/uiux/screenshots/`), a side-by-side table, and a recommendation with its reason.
6. **Stop and wait** for the user's pick.
7. **Merge the winner:** its tokens become the project's, the affected pages are rewritten to its patterns, and the choice with its reason goes to `DECISIONS.md` and `.bequite/uiux/selected-variant.md`.
8. **Archive the others** to `.bequite/uiux/archive/<time>/`. Nothing is deleted unless the user asks.
9. **Verify the merged UI:** build, a real browser check of the merged screen and of the existing routes for regressions.

## Output

```
<n> variants: V1 <direction> (/uiux/v1), V2 <direction> (/uiux/v2) ...
Report: .bequite/uiux/UIUX_VARIANTS_REPORT.md    Recommendation: V<n>, because <reason>
Waiting for your pick (reply with the number).
```

## Quality gate

Directions differ in structure, not only in colour; each has its measured references; all states and both widths exist for every variant; the original UI was untouched before the pick; nothing was installed to make previews work.

## Next Command Recommendations (typical)

After the merge: `/bq-live-edit` for adjustments · `/bq-feature` to build the remaining screens in the chosen direction · `/bq-verify`.
