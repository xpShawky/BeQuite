---
description: 'Phase 5 orchestrator — Memory and Handoff. Walks /bq-memory snapshot → optional /bq-handoff. Goal: persist state for the next session or hand off to a second engineer.'
---

# /bq-p5 — Phase 5 orchestrator: Memory and Handoff

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

Run Phase 5 commands. P5's job is to **continue cleanly later**. Snapshot the BeQuite memory state, optionally generate a handoff package for another engineer (or yourself in two weeks).

## When to use it

- After P4 (or any meaningful milestone)
- Before a long break (vacation, weekend, end-of-day)
- Before handing the project to a teammate or a vibe-coder
- After a release tag

## Preconditions

- `BEQUITE_INITIALIZED ✅`

## Required previous gates

- `BEQUITE_INITIALIZED ✅`
- (None else — P5 is callable at any point after init)

## Files to read

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/state/DECISIONS.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/work/<id>/plan.md` (if exists)
- `.bequite/work/<id>/verify.md` (if exists)
- `CHANGELOG.md`
- `.bequite/logs/AGENT_LOG.md` (last 20 entries)

## Files to write

- `.bequite/state/MEMORY_SNAPSHOT_<date>.md` (via `/bq-memory snapshot`)
- `HANDOFF.md` at repo root (via `/bq-handoff`, optional)
- `.bequite/state/WORKFLOW_GATES.md` (gates ticked)
- `.bequite/logs/AGENT_LOG.md`

## Steps

### 1. /bq-memory snapshot

Roll up the current state (mode, phase, gates, last 20 log entries, open questions, decisions, recent CHANGELOG) into one snapshot file at `.bequite/state/MEMORY_SNAPSHOT_<date>.md`.

This is the file `/bq-recover` reads on session resume.

Mark `MEMORY_SNAPSHOT ✅`.

### 2. (Optional) /bq-handoff

Ask the user: "Generate HANDOFF.md for another engineer or future-you? (y/N)"

If yes → write `HANDOFF.md` at repo root with two sections:
- **Engineer handoff** — full technical context: stack, ports, env vars (template, no secrets), how to boot, what's done, what's pending, known issues
- **Vibe handoff** — non-engineer-readable: what the product does, what's working, what to test, who to ask

Mark `HANDOFF_DONE ⚪ optional ✅`.

If no → skip.

### 3. Mark cycle complete

If `MEMORY_SNAPSHOT ✅`:
- Print final summary
- `CURRENT_PHASE.md` stays at P5 (terminal; next cycle re-enters at P0 if scope expands, or P2 for new features)

### 4. Print summary

```
✓ Phase 5 complete — Memory and Handoff

Mode:            <mode>
Memory snapshot: .bequite/state/MEMORY_SNAPSHOT_<date>.md
Handoff doc:     HANDOFF.md (written / skipped)
Open questions:  <count>
Pending tasks:   <count>

Status: project safe to leave / hand off.

Next session: open the repo + run /bq-recover.
```

## Output format

Narrate each step. At end, print summary + the single most useful next command for the user's situation.

## Quality gate

- `MEMORY_SNAPSHOT ✅`
- Snapshot file is human-readable (no PII; secrets redacted)
- If HANDOFF.md written: receiver checklist included; no secrets

## Failure behavior

- State files unreadable → log error; write partial snapshot with what is readable; flag the missing pieces
- User says no to handoff → that's fine; snapshot alone is enough for solo resume

## Usual next command

- (End of cycle) — close the session
- Or `/bq-recover` next session to resume
- Or start a new cycle: `/bq-mode` → `/bq-p0` again (for a new feature or fix)
