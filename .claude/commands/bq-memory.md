---
description: Read or write BeQuite memory snapshots. Use to inspect what BeQuite remembers, refresh context after a long pause, or save a checkpoint before risky work.
---

# /bq-memory — memory operations

You are managing BeQuite's **persistent memory** at `.bequite/`. Read it, refresh it, snapshot it.

## Modes

The user may invoke this with an argument:

- `/bq-memory` (no arg) — show a summary of what's in memory
- `/bq-memory show <topic>` — show one specific area (state, logs, plans, tasks, audits)
- `/bq-memory snapshot` — write a versioned snapshot of current state
- `/bq-memory refresh` — re-read everything (useful at start of new session)

## Default — show summary

Read all `.bequite/state/*.md` and summarize:

```
BeQuite memory summary

State:
  Project type:    <from PROJECT_STATE.md>
  Current phase:   <from CURRENT_PHASE.md>
  Last run:        <from LAST_RUN.md>
  Open questions:  <count, with titles> (see OPEN_QUESTIONS.md)
  Decisions:       <count> recorded (see DECISIONS.md)

Plans:
  Implementation:  <yes / no>
  Multi-model:     <yes / no>
  Scope:           <yes / no>
  Feature specs:   <count> files

Tasks:
  Total:           <count>
  Done:            <count>
  In progress:     <count>
  Blocked:         <count>
  Pending:         <count>

Audits:
  Discovery:       <yes / no>
  Doctor:          <yes / no>
  Research:        <yes / no>
  Full project:    <yes / no>
  Verify:          <yes / no>
  Review reports:  <count>
  Red-team:        <count>

Logs:
  AGENT_LOG.md:    <count> entries
  CHANGELOG.md:    <count> versioned sections + [Unreleased]
  ERROR_LOG.md:    <count> resolved bugs + <count> open
```

## `/bq-memory show <topic>`

Show the requested area, formatted. Topics:

- `state` → contents of all `.bequite/state/*.md`
- `state.questions` → just OPEN_QUESTIONS.md
- `state.decisions` → just DECISIONS.md
- `state.phase` → just CURRENT_PHASE.md
- `logs` → AGENT_LOG + CHANGELOG + ERROR_LOG (truncated to recent entries)
- `logs.errors` → just ERROR_LOG.md
- `logs.agent` → just AGENT_LOG.md (last 20 entries)
- `plans` → IMPLEMENTATION_PLAN.md + SCOPE.md
- `tasks` → TASK_LIST.md (formatted with progress bar)
- `audits` → list each audit file by date + size
- `audits.discovery` → DISCOVERY_REPORT.md
- `audits.doctor` → DOCTOR_REPORT.md
- `audits.full` → FULL_PROJECT_AUDIT.md
- `audits.verify` → VERIFY_REPORT.md

## `/bq-memory snapshot`

Capture the entire state at this moment for future recovery. Write:

`.bequite/state/SNAPSHOT-<YYYYMMDD-HHMMSS>.md`:

```markdown
# Memory snapshot

**Taken:** <ISO 8601 UTC>
**Reason:** <user provided or "manual checkpoint">

## State summary

(copy of the default summary output)

## Inline copies

(short copy of the most important files)

### CURRENT_PHASE.md
<content>

### LAST_RUN.md
<content>

### OPEN_QUESTIONS.md (resolved only)
<content>

### TASK_LIST.md status overview
<count by status>
```

The user may want to revert to this snapshot later via `/bq-recover SNAPSHOT-<timestamp>`.

## `/bq-memory refresh`

For when the user starts a new Claude Code session and wants a fresh context dump:

1. Re-read every `.bequite/state/*.md`
2. Re-read the last 5 entries of `AGENT_LOG.md`
3. Re-read the most recent audit / plan / task list
4. Produce a "ready to resume" summary

This is exactly what `/bq-recover` does for a new session — `refresh` is the read-only version of that.

## Step — Update state + log

- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md` appended

## Report back

```
✓ /bq-memory <mode> done

<summary or path-to-snapshot>

Next: <command-suggestion based on what's in memory>
```

## Rules

- **Read-only by default.** Only `snapshot` writes.
- **Don't truncate the user's view.** If they say `show state.decisions`, print all of it.
- **Snapshot files are timestamped + immutable.** Never overwrite a SNAPSHOT-*.md.

## Memory files this command reads

- All `.bequite/state/*.md`
- All `.bequite/logs/*.md`
- All `.bequite/plans/*.md`
- All `.bequite/tasks/*.md`
- All `.bequite/audits/*.md`

## Memory files this command writes

- `.bequite/state/SNAPSHOT-<timestamp>.md` (snapshot mode only)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

Depends on what the memory shows — `/bequite` for the menu, or the specific command relevant to what's open.
