---
description: Lightweight section-by-section frontend live edit. Maps visible sections to source files (SECTION_MAP.md), applies targeted code edits, verifies via build + screenshots (if browser automation available). Not a heavy Studio. Browser automation used only if frontend exists and tool is already available.
---

# /bq-live-edit: change one section, measure before and after

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

For small visible changes to an existing frontend: text, spacing, type, colour, a crowded card, a broken phone layout, an empty state. The procedure is `bequite-live-edit` (which eyes to use, the eight steps, the edit recipes); design values come from `.bequite/design/DESIGN_DNA.md` through `bequite-frontend-design-system`.

## Syntax

```
/bq-live-edit                        ask what to edit
/bq-live-edit "<what to change>"     e.g. "make the pricing cards less crowded"
```

Not for a new page or feature (`/bq-feature`), several design directions (`/bq-uiux-variants`), a redesign (`/bq-auto uiux`), or a logic bug (`/bq-fix`).

## Gates

Needs `BEQUITE_INITIALIZED` and a frontend in the project. An edit that touches more than one section re-runs the Design Continuity Gate on those sections (`DESIGN_CONTINUITY_PASS`). No browser tool is installed for this command: it uses the best one this session already has and says which.

## Steps

1. **Detect** the stack and the dev command from the manifest; start the dev server only if the project has one and it needs no secrets the agent lacks.
2. **Locate the section** on the page and in source (visible text, component name, class). Record it in `.bequite/uiux/SECTION_MAP.md`. Several matches: ask one question.
3. **Before:** a screenshot at desktop and phone width, the measured values the request is about (sizes, weights, colours, overflow), console errors.
4. **Target:** the value comes from the Design DNA or a measured reference, not from taste, and is written down.
5. **Smallest edit** in the file that owns the section; a token changes only when the issue is system-wide. The old snippet goes into `.bequite/uiux/LIVE_EDIT_LOG.md` first.
6. **After:** repeat step 3 exactly and compare numbers, not impressions.
7. **Guard:** build, run the existing tests, check the neighbouring sections did not move.
8. **Log** the entry: request, `file:line`, before and after values, screenshots, commands and exit codes. Undo is restoring the logged snippet.

## Output

```
Live edit: <section> in <file:line>    <property>: <before> -> <after>
Checked: <browser tier used, or "code only: UNVERIFIED visually">   build: exit <n>   tests: <pass>/<total>
Log: .bequite/uiux/LIVE_EDIT_LOG.md
```

## Quality gate

One section, one cause; before and after were measured the same way; neighbours unchanged; the build is green; a visual claim without a browser is marked `UNVERIFIED:`.

## Next Command Recommendations (typical)

`/bq-live-edit "<next section>"` · `/bq-review` for a larger batch · `/bq-verify` before shipping.
