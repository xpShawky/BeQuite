---
description: 'Phase 0 orchestrator — Setup and Discovery. Walks /bq-init → /bq-mode → /bq-discover → /bq-doctor in order, pausing only at the mode-selection gate. Goal: learn what''s there before deciding anything.'
---

# /bq-p0 — Phase 0 orchestrator: Setup and Discovery

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

## Purpose

Run all Phase 0 commands in the right order, in one pass. P0's job is to **learn**: what's in this repo, what mode are we in, what's the environment, what risks exist. No decisions about what to build yet.

## When to use it

- First time touching a project with BeQuite
- After a long break (re-orient before resuming)
- You're tired of running `/bq-init`, `/bq-discover`, `/bq-doctor` separately

## Preconditions

- The repo has either:
  - An existing project (manifests like `package.json`, `pyproject.toml`, `Cargo.toml`, etc.), OR
  - An empty folder that the user wants to start fresh in

## Required previous gates

- None (P0 is the entry phase)

## Files to read

- (At start) whatever exists in the working directory
- After `/bq-init`: `.bequite/state/PROJECT_STATE.md`

## Files to write

- `.bequite/state/PROJECT_STATE.md` (via `/bq-init`)
- `.bequite/state/CURRENT_PHASE.md` (set to `P0 — Setup and Discovery`)
- `.bequite/state/CURRENT_MODE.md` (via `/bq-mode`)
- `.bequite/state/WORKFLOW_GATES.md` (gates ticked)
- `.bequite/audits/DISCOVERY_REPORT.md` (via `/bq-discover`)
- `.bequite/audits/DOCTOR_REPORT.md` (via `/bq-doctor`)
- `.bequite/logs/AGENT_LOG.md`

## Steps

### 1. /bq-init

Initialize the `.bequite/` tree if not present. Mark gate `BEQUITE_INITIALIZED ✅`.

If already initialized → no-op (skip).

### 2. /bq-mode

Pause for user to pick one of 6 modes (or accept the recommended default). Mark gate `MODE_SELECTED ✅`.

**This is the only hard human gate in P0.**

### 3. /bq-discover

Read the codebase (stack detection, entry points, ports, tests, CI, docs, smells). Write `DISCOVERY_REPORT.md`.

For **New Project** mode in an empty folder: skip discover (nothing to discover).

Mark gate `DISCOVERY_COMPLETE ✅`.

### 4. /bq-doctor

Probe environment (Node, Python, Docker, ports, PATH). Write `DOCTOR_REPORT.md`.

Mark gate `DOCTOR_COMPLETE ✅`.

### 5. Mark phase complete

If `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `DISCOVERY_COMPLETE` (or N/A for empty new project), `DOCTOR_COMPLETE` are all `✅`:
- Set `.bequite/state/CURRENT_PHASE.md` → `P1 — Product Framing and Research` (advance)

### 6. Print summary

```
✓ Phase 0 complete — Setup and Discovery

Mode:            <mode>
Stack detected:  <list> (or "fresh project")
Env health:      <green/yellow/red>
Risks surfaced:  <count>

Reports:
  .bequite/audits/DISCOVERY_REPORT.md
  .bequite/audits/DOCTOR_REPORT.md

Next phase: P1 — run /bq-p1
```

## Output format

Narrate each step ("Running /bq-init...", "Running /bq-discover...") so the user can see progress. At the end, print the summary above.

## Quality gate

- `BEQUITE_INITIALIZED ✅`
- `MODE_SELECTED ✅`
- `DISCOVERY_COMPLETE ✅` (or N/A)
- `DOCTOR_COMPLETE ✅`
- `CURRENT_PHASE.md` advanced to P1

## Failure behavior

- `/bq-init` fails → log + exit; investigate before retry
- User refuses to pick a mode → exit gracefully; nothing else can proceed
- `/bq-discover` finds nothing readable → still write a minimal `DISCOVERY_REPORT.md` with a "fresh project" verdict
- `/bq-doctor` finds critical missing tools → write the report, advance anyway; the user fixes env issues separately

## Usual next command

- `/bq-p1` — run Phase 1 (Product Framing and Research)
- Or run individual P1 commands: `/bq-clarify`, `/bq-research`, `/bq-scope`, `/bq-plan`
