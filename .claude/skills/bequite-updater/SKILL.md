---
name: bequite-updater
description: Safe BeQuite-self-update discipline. Detects version + source + local edits, backs up before changes, merges updates non-destructively, NEVER overwrites project memory, surfaces conflicts as .bequite-update.md sibling files. Invoked by /bq-update.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

# bequite-updater — safe self-update discipline

## Purpose

Encode the safety + diff + merge + conflict + backup discipline that `/bq-update` uses to refresh BeQuite **inside an existing project** without breaking the user's memory, customization, or workflow.

Invoked by `/bq-update`.

---

## When to use this skill

- BeQuite itself is being updated (via `/bq-update`)
- A new alpha is released and the user wants the new commands/skills
- A user is testing a local BeQuite dev branch against an installed project

## When NOT to use this skill

- First-time install (use `scripts/install-bequite.{ps1,sh}`)
- Updating user project code (this skill only updates BeQuite's own files)
- Major version migration (alpha → 1.0) — out of scope until 1.0 ships

---

## Version detection

Source-of-truth order:

1. `.bequite/state/BEQUITE_VERSION.md` (created on first `/bq-update`; carries `**Version:** v3.0.0-alpha.X`)
2. `CLAUDE.md` BeQuite section (created by installer; carries the version in the heading)
3. Falling back to "v3.0.0-alpha.unknown" if neither is parseable

For the remote version:
- **GitHub:** read `package.json` (if present) → `version` field; OR fetch `docs/changelogs/CHANGELOG.md` → most recent `## [v...]` heading
- **Local clone:** same files, local filesystem

## Source detection

`.bequite/state/UPDATE_SOURCE.md` carries the configured source. If missing, default to GitHub `xpShawky/BeQuite` main.

Modes:
- `source=local path=X` (overrides config for this run)
- `source=github repo=X branch=Y` or `tag=Y`

## Backup strategy

**Always run before changing files** (unless `force` mode + user accepts risk).

```
.bequite/backups/<ISO-8601-timestamp>/
├── claude-commands/        # full copy of .claude/commands/ pre-update
├── claude-skills/          # full copy of .claude/skills/ pre-update
├── commands.md             # if present at root
├── claude-md.md            # CLAUDE.md before edit
└── version-pre-update.md   # BEQUITE_VERSION.md before edit
```

Verify backup integrity (file count matches; spot-check 2-3 files for content) before proceeding.

## Diff strategy

For each file the update wants to change:

1. Compute SHA-256 of local file
2. Compute SHA-256 of remote/source file
3. If equal → no change needed
4. If different → look for "local edit" signals:
   - File mtime newer than "shipped baseline" (we don't have a baseline registry in v1 — proxy: file modified after the last `/bq-update` timestamp from `UPDATE_LOG.md`, OR the file's first line doesn't match the standard alpha.X frontmatter pattern)
   - Custom markdown sections not present in the shipped version
   - User added their own command-level content

5. If "modified, no local edits" → safe to overwrite
6. If "modified, local edits detected" → conflict; write to `.bequite-update.md` sibling; don't overwrite the local file

## Merge strategy

| Case | Action |
|---|---|
| File in remote, missing locally | Copy from remote (new file) |
| File in local, missing from remote | Skip (don't delete; user might be on an old version that has files removed; let them reconcile) |
| File modified, no local edits | Overwrite from remote |
| File modified, local edits detected | Conflict — write `.bequite-update.md` sibling |
| File only differs in trailing whitespace / line endings | Normalize to remote and overwrite |

## Conflict handling

When a conflict surfaces:

1. **Default behavior (safe mode):** write new version to `<file>.bequite-update.md`. Don't touch local file. Log in `UPDATE_LOG.md`.
2. **Force mode:** overwrite anyway. Backup is still made. Full diff written to `UPDATE_LOG.md` so user can see exactly what was lost.

Example sibling file naming:

```
.claude/commands/bq-fix.md                 ← your local edited version
.claude/commands/bq-fix.md.bequite-update.md  ← new shipped version (sibling)
```

User reviews both, merges manually, then deletes the `.bequite-update.md` sibling.

## Files SAFE to update

- `.claude/commands/*.md` (with conflict handling)
- `.claude/skills/bequite-*/SKILL.md` (with conflict handling)
- `.claude/skills/bequite-*/references/*.md` (if shipped)
- `commands.md` (project root) — reference doc, overwrite OK
- `CLAUDE.md` — only the BeQuite section between `<!-- BEQUITE -->` markers
- `.bequite/principles/*.md` — only if missing (don't overwrite once installed)
- `.bequite/uiux/*.md` (templates) — only if missing
- `.bequite/jobs/*.md` (templates) — only if missing
- `.bequite/money/*.md` (templates) — only if missing
- `.bequite/decisions/` — only template additions; never overwrite user ADRs

## Files NEVER to overwrite

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
- `.bequite/audits/` (real audit reports)
- `.bequite/plans/` (real plans + features — except templates if user confirms)
- `.bequite/tasks/` (real TASK_LIST + CURRENT_TASK)
- `.bequite/prompts/` (real prompt exchanges)
- `.bequite/research/` (if exists)
- `.bequite/jobs/` content (user search results)
- `.bequite/money/` content (user search results + action plan)
- User code outside BeQuite paths

## Logging

Per-update entry in `.bequite/logs/UPDATE_LOG.md`:

```markdown
## <ISO 8601 UTC> — update from <source>

**Mode:** safe | check | force | local-source | github-source
**Version:** v3.0.0-alpha.X → v3.0.0-alpha.Y
**Source:** <repo / path>

**Files added:** <count>
  - <list>

**Files updated (no conflict):** <count>
  - <list with line-change summaries>

**Files skipped (conflict):** <count>
  - <file> — review .bequite-update.md sibling

**Files NOT changed (in never-overwrite list):** <count>

**Backup:** .bequite/backups/<timestamp>/

**Result:** success | partial | failed
**Notes:** <free-form>
```

Per-update entry in `AGENT_LOG.md` (summary):

```markdown
## <timestamp> — /bq-update <mode>
Updated BeQuite to v3.0.0-alpha.Y. <N> files changed, <M> conflicts.
Backup: .bequite/backups/<timestamp>/
```

## Rollback

If user wants to undo an update:

1. Open `.bequite/backups/<latest-timestamp>/`
2. Run: `cp -r .bequite/backups/<timestamp>/claude-commands/* .claude/commands/`
3. Same for `claude-skills/`
4. Restore `commands.md` and `CLAUDE.md` from backup
5. Restore `BEQUITE_VERSION.md` to the pre-update content

A future `/bq-update rollback` command can automate this. For now, document the manual path in the report.

## Test after update

After a successful update:

1. Check `.claude/commands/bequite.md` parses (YAML frontmatter intact)
2. Check `.claude/skills/bequite-*/SKILL.md` files all have valid frontmatter
3. Check `BEQUITE_VERSION.md` reflects the new version
4. Print a summary; suggest `/bq-now` to verify state

If anything looks corrupted → recommend rollback path.

## Common mistakes to avoid

- ❌ Overwriting `.bequite/state/MISTAKE_MEMORY.md` (user's project-specific lessons — never touch)
- ❌ Skipping backup in safe mode
- ❌ Auto-resolving conflicts on local-edited files (user's customizations would be silently lost)
- ❌ Updating without checking git remote is reachable (partial updates corrupt state)
- ❌ Forgetting to refresh `BEQUITE_VERSION.md` (next update can't detect what changed)

## Failure handling

| Failure | Recovery |
|---|---|
| GitHub unreachable | Log + exit; suggest local clone source |
| `git clone` fails | Log + exit; check user's network + git auth |
| Backup directory unwritable (permissions) | Log + exit; **do not proceed without backup** unless `force` |
| Update transferred partial files (network drop) | Roll back from in-progress backup; mark update as failed |
| File hash mismatch after copy (file system error) | Roll back; retry once; if persistent, exit |

## What this skill does NOT do

- Update user project code (out of scope)
- Migrate user data between BeQuite major versions (different problem; future)
- Auto-resolve conflicts on local-edited files (always surfaces; user decides)
- Push changes to git (read-only on the source side)
- Install new dependencies (per tool neutrality)

## See also

- `.claude/commands/bq-update.md` — the command spec
- `.bequite/state/BEQUITE_VERSION.md` — version source-of-truth
- `.bequite/state/UPDATE_SOURCE.md` — source configuration
- `.bequite/logs/UPDATE_LOG.md` — detailed update history
- `scripts/install-bequite.{ps1,sh}` — first-time installer (different concern)
