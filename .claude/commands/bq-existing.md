---
description: Begin an Existing Project Audit workflow. Sets the mode, recommends discover → doctor → audit sequence. Use when working with a repo that already has source code.
---

# /bq-existing — Existing Project Audit workflow entry

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

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

Or run /bq-auto phase=P0 to walk Phase 0 automatically.
```

## Quality gate

- `PROJECT_STATE.md` reflects existing-repo type
- 3 questions queued

## Failure behavior

- Folder looks empty → suggest `/bq-new`
- Mode is wrong → suggest `/bq-mode`

## Usual next command

`/bq-discover` (or `/bq-auto phase=P0`)
