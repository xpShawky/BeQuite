---
description: Begin an Existing Project Audit workflow. Sets the mode, recommends discover → doctor → audit sequence. Use when working with a repo that already has source code.
---

# /bq-existing — Existing Project Audit workflow entry

## Purpose

Mark the working assumption as "this repo already has code; we're understanding + improving it" and recommend the right next commands.

## When to use it

- After `/bq-mode` selected "Existing Project Audit"
- The folder has source code, manifests, README, etc.
- You want to understand the state + propose improvements before changing anything

## Preconditions

- `BEQUITE_INITIALIZED`
- `MODE_SELECTED = Existing Project Audit`

## Required previous gates

- `BEQUITE_INITIALIZED`
- `MODE_SELECTED`

## Files to read

- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/PROJECT_STATE.md`
- The current directory's top-level (Glob)

## Files to write

- `.bequite/state/PROJECT_STATE.md` (updated: "type = existing repo; stack TBD by /bq-discover")
- `.bequite/state/OPEN_QUESTIONS.md` (queues audit-specific questions)
- `.bequite/logs/AGENT_LOG.md`

## Steps

1. Read `.bequite/state/CURRENT_MODE.md`. If not "Existing Project Audit", refuse + suggest `/bq-mode`.
2. Glob the current directory. If it looks like a fresh empty folder (no package.json, no source), warn:
   > "This folder looks empty. Existing Project Audit mode expects existing code. Did you mean `/bq-new`?"
3. Update `PROJECT_STATE.md`:
   - `Project type: existing repo`
   - `Stack: TBD — pending /bq-discover`
4. Queue questions in `OPEN_QUESTIONS.md`:
   - "What's the goal — understand it, fix it, improve quality, or add a feature?"
   - "Is this production today or pre-launch?"
   - "Who owns this repo (you alone / team / external)?"
5. Print next steps.

## Output format

```
✓ Existing Project Audit workflow set

Current state:
  Mode:    Existing Project Audit
  Folder:  <path>
  Stack:   to be detected by /bq-discover
  Phase:   P0 — Setup and Discovery

Pre-queued questions:
  Q1. What's the goal?
  Q2. Production or pre-launch?
  Q3. Who owns this?

Recommended sequence:
  /bq-discover    inspect the repo + write DISCOVERY_REPORT.md
  /bq-doctor      environment health check
  /bq-audit       full project audit (catches install/run/UX/security gaps)
  /bq-clarify     answer the queued questions
  /bq-plan        write a remediation / improvement plan
  /bq-fix         fix the first blocker (if audit finds any)
  /bq-implement   workhorse for planned changes

Or run /bq-p0 to walk Phase 0 automatically.
```

## Quality gate

- `PROJECT_STATE.md` reflects existing-repo type
- 3 questions queued

## Failure behavior

- Folder looks empty → suggest `/bq-new`
- Mode is wrong → suggest `/bq-mode`

## Usual next command

`/bq-discover` (or `/bq-p0`)
