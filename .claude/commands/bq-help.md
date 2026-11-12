---
description: Full BeQuite command reference, grouped by family with catalog IDs. `/bq-help <command>` explains one command (when to use it, gates, what it reads and writes, what comes next). Read-only.
---

# /bq-help - command reference

Read-only. Never edits files.

## `/bq-help` (no argument)

1. Read `commands.md` (project root). It is the single source for the catalog, so this help never drifts from it. If it is missing, read `.bequite/commands/COMMAND_ID_MAP.md` instead and say that `commands.md` is missing (fix: re-run the installer with `--force`).
2. Print it condensed: the contract summary (skills first, work folders, gates, plan first, evidence, write back), the operating modes table, then each family (W0 Setup, W1 Framing, W2 Build, W3 Quality, W4 Release, W5 Memory, N Navigation, O Orchestrator, C Capabilities, M Maintenance) with ID, command and one line.
3. End with three starting points that fit the current state (read `.bequite/state/CURRENT_PHASE.md` and `.bequite/ACTIVE.md`), for example:
   - nothing set up yet → `/bq-init`, then `/bequite`
   - an idea for a film or reel → `/bq-motion "<idea>"`
   - not sure → `/bq-suggest "<what you want>"`

## `/bq-help <command>` (for example `/bq-help bq-motion`)

Read `.claude/commands/<command>.md` and summarise in under 25 lines: what it is for, when not to use it, syntax and arguments, required gates (from `.bequite/state/WORKFLOW_GATES.md` → "Required gates by command"), what it reads and writes (work folder files), the skills it usually selects, and the usual next command. Deprecated redirects (`/bq-p0`…`/bq-p5`, `/bq-now`) are explained as "use `<new command>` instead".

## Related

`/bequite` (menu with live state) · `/bequite short` (one line) · `/bq-suggest` (which route fits my goal) · `/bq-explain` (explain a file or decision).
