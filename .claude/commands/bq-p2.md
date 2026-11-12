---
description: 'Phase 2 orchestrator — Planning and Build. Walks /bq-assign → /bq-implement (looping) OR /bq-feature OR /bq-fix per the active mode. Goal: build the thing.'
---

# /bq-p2 — Phase 2 orchestrator: Planning and Build

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

Run Phase 2 commands. P2's job is to **build**. The exact command sequence depends on the active mode.

## When to use it

- P1 complete (or mode = Add Feature / Fix Problem, which skip P1)
- You want to execute the plan / feature / fix

## Preconditions

- `BEQUITE_INITIALIZED ✅`
- `MODE_SELECTED ✅`
- Mode is one of: New Project, Existing Audit (writes audit only), Add Feature, Fix Problem
- For New Project mode: `PLAN_APPROVED ✅` required

## Required previous gates

Per mode:

| Mode | Required gates |
|---|---|
| New Project | `PLAN_APPROVED ✅` |
| Add Feature | `MODE_SELECTED ✅` only |
| Fix Problem | `MODE_SELECTED ✅` only |
| Existing Audit | (P2 is skipped — no build) |
| Research Only | (P2 is skipped — no build) |
| Release Readiness | (P2 is skipped — no new code) |

## Files to read

- `.bequite/state/CURRENT_MODE.md`
- `.bequite/work/<id>/plan.md` (New Project mode)
- `.bequite/work/<id>/tasks.md` (New Project mode, after /bq-assign)
- `.bequite/work/<id>/spec.md` (Add Feature mode)

## Files to write

- `.bequite/work/<id>/tasks.md` (via `/bq-assign`)
- `.bequite/work/<id>/tasks.md` (the active task)
- `.bequite/work/<id>/spec.md` (Add Feature mode)
- `.bequite/audits/FIX_<slug>.md` (Fix Problem mode)
- `.bequite/work/<id>/log.md` (Fix Problem mode)
- `.bequite/state/WORKFLOW_GATES.md` (gates ticked)
- `.bequite/state/CURRENT_PHASE.md` (advances to P3)
- `CHANGELOG.md` (`[Unreleased]` entry per task)
- `.bequite/logs/AGENT_LOG.md`
- All source files the build touches

## Steps

### Mode = New Project

1. **/bq-assign** — Read IMPLEMENTATION_PLAN.md, write TASK_LIST.md (atomic ≤5min tasks with one acceptance criterion each)
2. **/bq-implement loop** — Pick next `[ ] pending` task, read files, make minimal change, run test, verify acceptance, mark `[x]`. Repeat until TASK_LIST is empty or blocker hit.
3. Per task → CHANGELOG `[Unreleased]` entry.

Mark `TASKS_ASSIGNED ✅`, `IMPLEMENT_DONE ✅`.

### Mode = Add Feature

1. **/bq-feature "<title>"** — Get title, classify type (1 of 12), activate matching skills, write mini-spec, confirm with user, implement, test, log.

Mark `FEATURE_DONE ✅`.

### Mode = Fix Problem

1. **/bq-fix** — Get symptom + reproduction, classify problem type (1 of 15), activate matching skills, reproduce, root cause (5-whys), smallest safe patch, add regression test, verify symptom gone.

Mark `FIX_DONE ✅`.

### Mode = Existing Audit / Research Only / Release Readiness

P2 is skipped. Print: "P2 is not used for this mode. Proceed to P3 with /bq-p3."

### Final: Mark phase complete

If the mode's required gate is `✅`:
- Set `.bequite/state/CURRENT_PHASE.md` → `P3 — Quality and Review`

### Print summary

```
✓ Phase 2 complete — Planning and Build

Mode:           <mode>
Tasks done:     <count> / <total>          (New Project)
Feature:        <title>                     (Add Feature)
Fix:            <symptom>                   (Fix Problem)
Files touched:  <count>
Tests:          <pass> / <total>

Next phase: P3 — run /bq-p3 or /bq-test
```

## Output format

Narrate per command. For /bq-implement loop, narrate per task (`[T-1.3] starting...`, `[T-1.3] done ✓`).

## Quality gate

Per mode:

| Mode | Required for `✅` |
|---|---|
| New Project | All tasks in TASK_LIST `[x]` complete; all touched tests pass |
| Add Feature | Mini-spec complete; feature implemented; new test passes |
| Fix Problem | Symptom reproduced; root cause identified; patch in place; regression test passes |

Plus across all modes:
- No banned weasel words
- CHANGELOG `[Unreleased]` updated
- AGENT_LOG entry per task/feature/fix

## Failure behavior

- 3 consecutive task failures on same task → mark `[!]` blocked, log, **pause for user**
- Test red after implementation → roll back via `git stash`, log to `ERROR_LOG.md`, exit
- Destructive op requested → pause for user OK (never auto-execute)
- Out-of-scope change requested → flag, pause, ask user to update SCOPE.md if intentional

## Usual next command

- `/bq-p3` — run Phase 3 (Quality and Review)
- Or `/bq-test` directly
