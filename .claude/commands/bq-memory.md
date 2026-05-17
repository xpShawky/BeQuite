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

## Standardized command fields (alpha.6)

**Phase:** P5 — Memory and Handoff (or anytime)
**When NOT to use:** mid-implementation when state is in flux (snapshot first, then continue); use `/bq-recover` to read snapshots, not `/bq-memory`.
**Preconditions:** `BEQUITE_INITIALIZED`
**Required previous gates:** `BEQUITE_INITIALIZED`
**Subcommands:** `show`, `snapshot`, `refresh`
**Quality gate:**
- For `snapshot`: `MEMORY_SNAPSHOT_<date>.md` written; rolled-up state captured; marks `MEMORY_SNAPSHOT ✅`
- For `show`: human-readable output of requested section
- For `refresh`: state files re-read; agent context updated
**Failure behavior:**
- State file unreadable → log to `ERROR_LOG.md`; write partial snapshot with what is readable; flag the missing pieces
- No state to snapshot (fresh repo) → suggest `/bq-init` first
**Memory updates:** Writes new snapshot file (on `snapshot` subcommand). No mutation otherwise.
**Log updates:** `AGENT_LOG.md`.

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

---

## Gate check + memory preflight (alpha.15)

Before doing any work:

1. **Gate check.** Read `.bequite/state/WORKFLOW_GATES.md`. If this command's required gates aren't `✅`, refuse:
   > "You're trying to run this command, but `<required-gate>` is pending. Run `<prerequisite-command>` first."

   Don't proceed when a required gate is missing. Recommend the prerequisite + how to resume.

2. **Memory preflight.** Read these files first (per `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`):

   - `.bequite/state/PROJECT_STATE.md`
   - `.bequite/state/CURRENT_MODE.md`
   - `.bequite/state/CURRENT_PHASE.md`
   - `.bequite/state/LAST_RUN.md`
   - `.bequite/state/MISTAKE_MEMORY.md` — top 10–20 entries (skip mistakes already learned)
   - Other state files only when relevant to this command's scope (`DECISIONS.md` for architectural questions, `OPEN_QUESTIONS.md` for phase transitions, `MODE_HISTORY.md` when invoked via `/bq-auto`-style flows)

   **Use focused reads.** Don't load all of `.bequite/` every command.

## Memory writeback (alpha.15)

After successful completion:

- `.bequite/state/LAST_RUN.md` — this command + outcome
- `.bequite/state/WORKFLOW_GATES.md` — set this command's gate to `✅` if applicable
- `.bequite/state/CURRENT_PHASE.md` — advance if phase transitioned
- `.bequite/logs/AGENT_LOG.md` — append entry
- `.bequite/logs/CHANGELOG.md` `[Unreleased]` — only when material files changed (skip for read-only commands)
- `.bequite/state/MISTAKE_MEMORY.md` — append when a project-specific lesson surfaced
- `.bequite/state/MODE_HISTORY.md` — append mode + outcome (when invoked via `/bq-auto`-style mode)

**Failure behavior:** don't claim `✅ done` if any of the above wasn't completed. Report PARTIAL with the specific gap.
