---
description: Update BeQuite (commands + skills + docs + memory templates) from GitHub or a local source. Safe + non-destructive: backups before changing files; never overwrites project memory; preserves local customization. Modes: check / safe / force / local-source / github-source.
---

# /bq-update — update BeQuite itself

## Purpose

Update BeQuite commands, skills, docs templates, and version metadata **inside an existing project** without re-running the full installer.

**Safe by default.** Backs up `.claude/commands/` + `.claude/skills/` before touching anything. Never overwrites your project memory (`PROJECT_STATE.md`, `DECISIONS.md`, `MISTAKE_MEMORY.md`, `.bequite/jobs/`, `.bequite/money/`, `.bequite/research/`).

## When to use it

- BeQuite ships a new alpha (alpha.X+1 released)
- You want the latest commands without manual `git pull` + `cp -r`
- You forked a private mirror and want to sync from there
- You're developing BeQuite itself and want to test local changes against a target project

## When NOT to use it

- First-time install — use `scripts/install-bequite.{ps1,sh}` instead
- You have heavy local customizations in `.claude/commands/` and don't want them touched — read `## Conflict handling` below first
- You're mid-flight on a critical task — wait until you're between phases

## Syntax + modes

```
/bq-update                                  # safe update (default — backup then update)
/bq-update check                            # show what would change; don't touch files
/bq-update force                            # skip backup + interactive prompts (warned)
/bq-update source=local path="C:/dev/BeQuite"   # update from local clone
/bq-update source=github repo="xpShawky/BeQuite" branch=main   # update from GitHub
/bq-update source=github repo="xpShawky/BeQuite" tag=v3.0.0-alpha.9   # pinned tag
```

Examples:
- `/bq-update check` — preview only
- `/bq-update` — backup + update from default source (GitHub `xpShawky/BeQuite` main)
- `/bq-update source=local path="../BeQuite-dev"` — for BeQuite contributors developing locally

## Preconditions

- `BEQUITE_INITIALIZED`

## Required previous gates

- `BEQUITE_INITIALIZED`

## Memory preflight (read at start)

- `.bequite/state/BEQUITE_VERSION.md` — current installed version
- `.bequite/state/UPDATE_SOURCE.md` — configured update source (if any)
- `.claude/commands/` — current command files (count + names)
- `.claude/skills/` — current skill directories

## Files this command writes

- `.bequite/state/BEQUITE_VERSION.md` — updated after successful update
- `.bequite/state/UPDATE_SOURCE.md` — created/updated on first run
- `.bequite/logs/UPDATE_LOG.md` — append-only log per update
- `.bequite/backups/<timestamp>/` — backup of pre-update state
- `.bequite/logs/AGENT_LOG.md`
- `.bequite/logs/CHANGELOG.md` (only if user-facing behavior shifted)

## Steps

### 1. Detect current version

Read `.bequite/state/BEQUITE_VERSION.md`. If it doesn't exist, parse from `CLAUDE.md` BeQuite section (created by installer). If still unknown → mark as "v3.0.0-alpha.unknown".

### 2. Read local BeQuite state

- Count files in `.claude/commands/`
- Count directories in `.claude/skills/bequite-*/`
- Check for local edits: compute hash of each file; compare to "shipped" baseline (we don't have this baseline in v1; for now, log file mtimes that look manually edited)
- Read `UPDATE_SOURCE.md` to know where to fetch from

### 3. Resolve source

| Mode | Behavior |
|---|---|
| (none — default) | Read `UPDATE_SOURCE.md`; if missing, use GitHub `xpShawky/BeQuite` main |
| `source=local path=X` | Use local clone at `X` |
| `source=github repo=X branch=Y` | Use specific GitHub repo + branch |
| `source=github repo=X tag=Y` | Use a pinned tag (recommended for stability) |

If GitHub source unreachable → log + suggest local clone fallback; don't proceed.

### 4. Check for available updates

- Compare local version to source version
- If equal → "Already up to date." Exit without changes (unless `force`).
- If newer remote version → enumerate what changed:
  - New commands (in remote, missing locally)
  - Modified commands (different content)
  - Deleted commands (in local, missing remotely — careful)
  - New skills
  - Modified skills
  - Deleted skills
  - New memory templates (in target project, missing because earlier installer didn't include them)

### 5. `check` mode — preview only

Print:

```
BeQuite update preview

Current version: v3.0.0-alpha.X
Available:       v3.0.0-alpha.Y
Source:          <source>

Commands:
  + bq-newcommand        (new)
  ~ bq-fix               (modified — 14 lines changed)
  ~ bq-plan              (modified — 28 lines changed)

Skills:
  + bequite-newskill     (new)
  ~ bequite-researcher   (modified)

Memory templates (new — would be added):
  + .bequite/jobs/HIDDEN_GEMS.md

Local customization detected (would NOT be overwritten without force):
  ~ .claude/commands/bq-fix.md  (mtime > shipped baseline — likely edited by you)

To apply: /bq-update
To force: /bq-update force
```

Exit. No files changed.

### 6. Backup (always for safe mode; skipped only for `force`)

Create `.bequite/backups/<ISO-8601-timestamp>/` with:
- `.claude/commands/` (full copy)
- `.claude/skills/` (full copy)
- `commands.md` (if present at root)
- Version metadata files

Print backup path. Confirm size + file count.

### 7. Merge updates

For each file class:

| File class | Strategy |
|---|---|
| `.claude/commands/*.md` (new) | Copy from source |
| `.claude/commands/*.md` (modified, no local edits) | Overwrite from source |
| `.claude/commands/*.md` (modified, local edits detected) | Write to `<file>.bequite-update.md`; surface conflict |
| `.claude/skills/bequite-*/` (new) | Copy from source |
| `.claude/skills/bequite-*/` (modified, no local edits) | Overwrite from source |
| `.claude/skills/bequite-*/` (modified, local edits) | Write to `<file>.bequite-update.md`; surface conflict |
| `.bequite/principles/*.md` (template) | Copy if missing; never overwrite if present |
| `.bequite/uiux/*.md` (template) | Copy if missing; never overwrite |
| `.bequite/jobs/*.md` (template) | Copy if missing; never overwrite |
| `.bequite/money/*.md` (template) | Copy if missing; never overwrite |
| `commands.md` (root) | Overwrite (reference doc, not memory) |

### 8. Never overwrite (hard rules)

These files NEVER get touched by `/bq-update`:

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/WORKFLOW_GATES.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/state/DECISIONS.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/ASSUMPTIONS.md`
- `.bequite/state/MISTAKE_MEMORY.md`
- `.bequite/state/MEMORY_SNAPSHOT_*.md`
- `.bequite/logs/AGENT_LOG.md`
- `.bequite/logs/CHANGELOG.md`
- `.bequite/logs/ERROR_LOG.md`
- `.bequite/audits/` (your real audit reports)
- `.bequite/plans/` (your real plans + features — except templates, which prompt)
- `.bequite/tasks/` (your real TASK_LIST + CURRENT_TASK)
- `.bequite/prompts/` (your real prompt exchanges)
- `.bequite/research/` (if exists)
- `.bequite/jobs/` content (templates only added if missing)
- `.bequite/money/` content (same)
- `.bequite/uiux/` content beyond templates
- `CLAUDE.md` body (only the BeQuite section between `<!-- BEQUITE -->` markers may be refreshed; user content untouched)

### 9. Conflict handling

When a local edit is detected on a file that the update wants to change:

1. **Default behavior (safe):** write the new version as `<file>.bequite-update.md` (suffix). The local file stays. User reviews + merges manually.
2. **Force mode:** overwrite anyway. Backup is still made. User gets diff in `UPDATE_LOG.md`.

Print to `.bequite/logs/UPDATE_LOG.md`:

```markdown
## <timestamp> — update from <source>

**Version:** v3.0.0-alpha.X → v3.0.0-alpha.Y
**Files updated:** <count>
**Files added:** <count>
**Files skipped (local edits):** <count>
  - <file path> — review .bequite-update.md sibling
**Files NOT changed (memory):** <count> (per never-overwrite list)

**Backup:** .bequite/backups/<timestamp>/

**Next:**
- /bq-now to verify state intact
- review .bequite-update.md files if any
- /bq-update force to re-run if conflicts resolved
```

### 10. Update version metadata

Write `.bequite/state/BEQUITE_VERSION.md`:

```markdown
# BeQuite installed version

**Version:** v3.0.0-alpha.Y
**Updated:** <ISO 8601 UTC>
**Source:** github / local
**Source path / repo:** <details>
**Previous version:** v3.0.0-alpha.X
**Last check:** <ISO 8601 UTC>
**Update count:** <N>
```

Write `.bequite/state/UPDATE_SOURCE.md` if it didn't exist:

```markdown
# BeQuite update source configuration

**Source type:** github | local
**Repo URL or local path:** <details>
**Default branch:** main
**Default strategy:** safe (backup + merge; no overwrite of local edits)

## Pinned tag (optional)

Leave blank to track latest commits on default branch. Set to a tag (e.g.
v3.0.0-alpha.9) to pin to a stable release.

**Pinned tag:** (blank)

## Last update

- **Last checked:** <ISO 8601 UTC>
- **Last updated:** <ISO 8601 UTC>
- **Result:** success
```

### 11. Update changelog (only if user-facing behavior shifted)

If the update added / removed commands, changed gate behavior, or added a new mode → append to `.bequite/logs/CHANGELOG.md` under `[Unreleased]`:

```markdown
### Updated
- BeQuite updated from v3.0.0-alpha.X to v3.0.0-alpha.Y
- New commands: <list>
- New skills: <list>
- Backup: .bequite/backups/<timestamp>/
```

### 12. Update logs

`.bequite/logs/AGENT_LOG.md` — entry per update.
`.bequite/logs/UPDATE_LOG.md` — detailed update record.

### 13. Final report

```
✓ BeQuite updated to v3.0.0-alpha.Y

Source:           <source>
Commands changed: <count>
Skills changed:   <count>
Templates added:  <count>
Conflicts:        <count — see .bequite-update.md files>
Backup:           .bequite/backups/<timestamp>/

Logs:
  .bequite/state/BEQUITE_VERSION.md
  .bequite/logs/UPDATE_LOG.md

Next:
  /bq-now           verify state intact
  /bq-help          see new commands (if any)
  /bequite          gate-aware menu
```

## Quality gate

- Backup created before any file change (safe mode)
- No file in the never-overwrite list was touched
- All conflict cases produced `.bequite-update.md` sibling files
- `BEQUITE_VERSION.md` reflects the new version
- `UPDATE_LOG.md` has a full record
- No banned weasel words in the report

## Failure behavior

- Source unreachable → log + exit; suggest local clone fallback; don't change any file
- Backup fails (disk full, permissions) → exit; never proceed without backup unless `force`
- Conflict on a critical command file (e.g. `/bequite`) → write `.bequite-update.md`; flag prominently; suggest user reviews before re-running
- User cancels mid-update → roll back from the in-progress backup

## Memory writeback

- `BEQUITE_VERSION.md` ← new version
- `UPDATE_SOURCE.md` ← refreshed last-checked + last-updated
- `UPDATE_LOG.md` ← detailed entry
- `AGENT_LOG.md` ← summary entry
- `CHANGELOG.md` ← only if user-facing behavior shifted

## Tool neutrality (global rule)

`/bq-update` doesn't pick external tools. It uses:
- `git` (already required by BeQuite installer)
- Built-in file ops (Read / Write / Edit / Bash mkdir+cp)

No new dependency added.

See `.bequite/principles/TOOL_NEUTRALITY.md`.

## Skills activated

- `bequite-updater` — full version-detection / diff / merge / conflict / backup procedures

## Standardized command fields (alpha.10)

**Phase:** Maintenance (not part of P0-P5 workflow)
**When NOT to use:** mid-task on a critical phase; first-time install (use installer); no internet + no local source
**Preconditions:** `BEQUITE_INITIALIZED`; git on PATH (for github source)
**Required previous gates:** `BEQUITE_INITIALIZED`
**Quality gate:** backup made; never-overwrite list respected; conflicts surfaced as `.bequite-update.md`; version metadata updated
**Failure behavior:** source unreachable → exit; backup fails → exit; conflicts → surface as sibling files, don't auto-resolve
**Memory updates:** `BEQUITE_VERSION.md`, `UPDATE_SOURCE.md`, `UPDATE_LOG.md`, `backups/<ts>/`
**Log updates:** `AGENT_LOG.md`; `CHANGELOG.md` if behavior shifted

## Usual next command

- `/bq-now` — verify state is intact after update
- `/bq-help` — discover any new commands
- `/bequite` — gate-aware menu reflecting new commands
