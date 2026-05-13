---
description: Initialize BeQuite in this repo. Creates .bequite/ memory dirs, baseline state files, and a BeQuite section in CLAUDE.md. Use `bq-init new` for a brand-new empty folder.
---

# /bq-init — initialize BeQuite

You are establishing BeQuite's footprint inside the user's repo.

## Modes

The user may invoke this as:
- `/bq-init` (default) — assume an existing repo
- `/bq-init new` — brand-new empty folder

## Step 1 — Detect the state

Check these (with the Read or Glob tools, do not run shell):

- `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `composer.json`, `Gemfile` → existing repo signals
- `.git/` → git initialized
- `.bequite/` → already initialized (refuse to overwrite without confirmation)
- `CLAUDE.md` → host instructions

If `.bequite/` exists and isn't empty, ask:
> "BeQuite memory already exists at `.bequite/`. Re-initialize? (y/N)"

Do not touch existing memory without explicit y.

## Step 2 — Create the memory scaffold

Create these directories (use mkdir-equivalent via Write tool):

```
.bequite/state/
.bequite/logs/
.bequite/prompts/user_prompts/
.bequite/prompts/generated_prompts/
.bequite/prompts/model_outputs/
.bequite/audits/
.bequite/plans/
.bequite/tasks/
```

## Step 3 — Write baseline state files

Author with sensible defaults. Each is a markdown file.

### `.bequite/state/PROJECT_STATE.md`

```markdown
# Project state

**Initialized:** <today's date YYYY-MM-DD>
**Project type:** <existing repo | new project>
**Stack detected:** <from manifests — Node/Python/Rust/Go/etc., or "unknown — run /bq-doctor">
**Repository:** <git remote URL, if available>

## Project summary

(Write 2-3 sentences from README.md if present, else "(no summary yet — run /bq-discover)")

## What BeQuite tracks for this project

- `state/CURRENT_PHASE.md` — workflow phase (Phase 0 → Phase 5)
- `state/LAST_RUN.md` — most recent BeQuite command run + result
- `state/DECISIONS.md` — running list of decisions made
- `state/OPEN_QUESTIONS.md` — questions awaiting answers
- `logs/AGENT_LOG.md` — every command, append-only
- `audits/`, `plans/`, `tasks/`, `prompts/` — per-command artifacts
```

### `.bequite/state/CURRENT_PHASE.md`

```markdown
# Current phase

**Phase:** Phase 0 — Setup and Understanding

**Next step:** Run /bq-discover to inspect the repo, then /bq-doctor for environment.

**Phases:**
- Phase 0 — Setup and Understanding (you are here)
- Phase 1 — Problem Framing
- Phase 2 — Build
- Phase 3 — Quality
- Phase 4 — Ship
- Phase 5 — Continue Later
```

### `.bequite/state/LAST_RUN.md`

```markdown
# Last BeQuite command

**Command:** /bq-init
**Timestamp:** <ISO 8601 UTC, today>
**Result:** BeQuite initialized successfully
**Next suggested:** /bq-discover
```

### `.bequite/state/DECISIONS.md`

```markdown
# Decisions log

Append decisions as the project evolves. Newest at top.

## <date> — BeQuite installed
Decision: Use BeQuite skill pack for this project's coding-agent workflow.
Rationale: Improve output quality with fewer errors via spec-driven gates.
```

### `.bequite/state/OPEN_QUESTIONS.md`

```markdown
# Open questions

Tracked questions awaiting answers. Set status to **resolved** when answered.

(none yet — run /bq-clarify when ready to surface high-value questions)
```

### `.bequite/logs/AGENT_LOG.md`

```markdown
# Agent log

Append-only chronicle of every BeQuite command run. Newest at top.

## <ISO 8601 UTC>
**Command:** /bq-init
**Mode:** <existing repo | new project>
**Files touched:** created .bequite/ memory tree + state baselines
**Next:** /bq-discover
```

### `.bequite/logs/CHANGELOG.md`

```markdown
# Project changelog

Tracked by BeQuite. Use `/bq-changelog` to add entries.

## [Unreleased]

(no changes yet)
```

### `.bequite/logs/ERROR_LOG.md`

```markdown
# Error log

Tracked by `/bq-fix`. Each entry: timestamp, error, root cause, fix, verification.

(empty)
```

## Step 4 — Update CLAUDE.md

If `CLAUDE.md` does not exist, create it with this minimal content:

```markdown
# CLAUDE.md

This project uses **BeQuite** — a lightweight Claude Code skill pack.

## How to use BeQuite here

- Run `/bequite` to see the menu and what to do next.
- Run `/bq-help` for the full command reference.
- BeQuite memory lives in `.bequite/`.
- BeQuite commands live in `.claude/commands/bequite.md` + `.claude/commands/bq-*.md`.
- BeQuite skills live in `.claude/skills/bequite-*/`.

## Core operating rules

- Never claim a task is "done" unless `/bq-verify` passes.
- Always update `.bequite/logs/AGENT_LOG.md` when you take a real action.
- Always update `.bequite/state/CURRENT_PHASE.md` when the workflow phase changes.
- Banned weasel words in completion reports: should, probably, seems to, appears to, I think it works, might, hopefully, in theory.
```

If `CLAUDE.md` already exists, APPEND a new section to it (do not overwrite):

```markdown

---

# BeQuite

This project uses **BeQuite** — a lightweight Claude Code skill pack.

Run `/bequite` to see the menu. See `.bequite/` for memory + state.
```

## Step 5 — Report back

Print this to the chat:

```
✓ BeQuite initialized in <current directory>

Created:
  .bequite/state/{PROJECT_STATE,CURRENT_PHASE,LAST_RUN,DECISIONS,OPEN_QUESTIONS}.md
  .bequite/logs/{AGENT_LOG,CHANGELOG,ERROR_LOG}.md
  .bequite/{prompts,audits,plans,tasks}/

CLAUDE.md: <created | section appended | unchanged>

Phase: Phase 0 — Setup and Understanding
Next:  /bq-discover     inspect the repo + write DISCOVERY_REPORT.md
       /bq-doctor       check Node / Python / Docker / etc.
       /bq-clarify      (new projects only) ask the user 3-5 questions
```

## Standardized command fields (alpha.6)

**Phase:** P0 — Setup and Discovery
**When NOT to use:** `.bequite/` is already initialized and has real content — use `/bq-recover` instead to avoid overwriting memory.
**Preconditions:** writable working directory; not running inside `node_modules`/`vendor`/etc.
**Required previous gates:** none (this is the entry point)
**Quality gate:**
- `.bequite/` tree exists with all 8 subdirs
- All 8 baseline state files written
- `CLAUDE.md` has BeQuite section
- Marks `BEQUITE_INITIALIZED ✅` in `WORKFLOW_GATES.md`
**Failure behavior:**
- `.bequite/` exists with content → refuse + ask user before overwriting; suggest `/bq-recover`
- Write fails on any file → log + exit; do NOT partial-init
**Memory updates:** Sets `BEQUITE_INITIALIZED ✅`. Creates all baseline state files.
**Log updates:** First entry in `AGENT_LOG.md`. CHANGELOG `[Unreleased]` initialized.

## Memory files this command reads

- `CLAUDE.md` (if exists)
- `package.json`, `pyproject.toml`, etc. (to detect stack)
- `README.md` (for the project-summary line)

## Memory files this command writes

- `.bequite/state/PROJECT_STATE.md` (new)
- `.bequite/state/CURRENT_PHASE.md` (new)
- `.bequite/state/LAST_RUN.md` (new)
- `.bequite/state/DECISIONS.md` (new)
- `.bequite/state/OPEN_QUESTIONS.md` (new)
- `.bequite/logs/AGENT_LOG.md` (new — first entry)
- `.bequite/logs/CHANGELOG.md` (new — empty Unreleased)
- `.bequite/logs/ERROR_LOG.md` (new — empty)
- `CLAUDE.md` (created or appended)

## Usual next command

- **Existing repo:** `/bq-discover`
- **New project (`bq-init new`):** `/bq-clarify`
