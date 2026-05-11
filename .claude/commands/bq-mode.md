---
description: Select or display the current BeQuite mode. Six modes — New / Existing Audit / Add Feature / Fix Problem / Research Only / Release Readiness. Determines workflow + which gates apply.
---

# /bq-mode — select the working mode

## Purpose

Set the operating mode for the current BeQuite session. Mode determines which gates are required, which are skipped, and which commands the next-3 menu recommends.

## When to use it

- Just after `/bq-init` on a fresh BeQuite install
- When pivoting from one kind of work to another (e.g. you finished a fix; now you want to add a feature)

## Preconditions

- `BEQUITE_INITIALIZED` gate done (i.e., `.bequite/state/PROJECT_STATE.md` exists)

## Required previous gates

- `BEQUITE_INITIALIZED`

## Files to read

- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/WORKFLOW_GATES.md`

## Files to write

- `.bequite/state/CURRENT_MODE.md` (mode written)
- `.bequite/state/WORKFLOW_GATES.md` (`MODE_SELECTED` gate set to `✅ done`)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Steps

1. Read current mode from `.bequite/state/CURRENT_MODE.md`. If a mode is already selected, ask: "Current mode: `<X>`. Change it? (y/N)" — exit on N.
2. Present the six modes:

   ```
   Select a BeQuite mode:

     1. New Project              — starting from scratch in an empty folder
     2. Existing Project Audit   — work with an existing repo
     3. Add Feature              — existing repo; add one feature
     4. Fix Problem              — something is broken
     5. Research Only            — pre-planning; no implementation
     6. Release Readiness        — built; verify + ship

   Pick a number (1-6) or describe in one sentence.
   ```
3. Wait for user input. Accept number, name, or sentence.
4. If ambiguous, ask one clarifying question.
5. Write the mode to `.bequite/state/CURRENT_MODE.md` with a one-line rationale.
6. Update `WORKFLOW_GATES.md` — set `MODE_SELECTED = ✅ done` + add a mode-specific gate-override note.
7. Append a Decision entry to `.bequite/state/DECISIONS.md`.
8. Update `LAST_RUN.md` + `AGENT_LOG.md`.

## Output format

Print to chat:

```
✓ Mode set: <Mode Name>

What this mode does:
  <one-line description of the workflow>

Recommended next 3 commands:
  1. /<command>
  2. /<command>
  3. /<command>
```

## Quality gate

- `.bequite/state/CURRENT_MODE.md` contains exactly one of the six allowed modes
- `WORKFLOW_GATES.md::MODE_SELECTED` is `✅ done`

## Failure behavior

- If the user picks something not in the six modes → ask again, listing the six options
- If `BEQUITE_INITIALIZED` is not done → refuse + suggest `/bq-init` first
- If the user wants to change mode mid-work → allow it, warn that some artifacts may not apply to the new mode, log the change

## Usual next command

| Mode picked | Next |
|---|---|
| New Project | `/bq-new` |
| Existing Project Audit | `/bq-existing` |
| Add Feature | `/bq-feature` (with feature title argument) |
| Fix Problem | `/bq-fix` (with symptom argument) |
| Research Only | `/bq-discover` (then `/bq-research`) |
| Release Readiness | `/bq-verify` |
