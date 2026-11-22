---
description: 'Update BeQuite by hand (commands, skills, docs, memory templates) from a release, a tag, a branch or a local clone. Backs up first, never overwrites project memory, and keeps local edits as sibling files to merge. Modes: check / safe / force, with source, tag, branch and path arguments.'
---

# /bq-update: the careful, manual update

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

**Usually you do not need it.** Step 1 of every command runs `.claude/bequite/bin/bq-update.sh`, which installs a new **official GitHub Release** (or the pinned tag) by itself when **Auto update** is `on` in `.bequite/state/UPDATE_SOURCE.md`. That automatic path never follows a branch, another repo, or a path inside the project; it only reports those. Use this command when Auto update is `off`, for a fork, a branch or a local clone, to preview, or to merge around your own edits file by file. Plugin installs update through `/plugin` instead. Procedure: `bequite-updater`.

## Syntax

```
/bq-update                                   safe: back up, then merge
/bq-update check                             show what would change; touch nothing
/bq-update force                             replace pack files (still backs up)
/bq-update source=github tag=v5.0.0          a release tag of the official repo
/bq-update source=github repo="owner/name" branch=main    a fork or unreleased commits
/bq-update source=local path="C:/dev/BeQuite"             a local clone (its last commit)
```

Arguments apply to this run only; add `save=true` to write them to `UPDATE_SOURCE.md`. Not for a first install (use the installer) and not in the middle of a critical task.

## Gates

Needs `BEQUITE_INITIALIZED` and git. A source other than the official repo's releases runs someone's unreleased code on this machine: name the source and the commit, and wait for the user's yes before installing.

## Steps

1. **Installed version and source:** `.bequite/state/BEQUITE_VERSION.md`, `UPDATE_SOURCE.md`, `PACKS.md`.
2. **Resolve the source** from the arguments or the file, then fetch it once into a temp folder: `git clone --depth 1 --branch <tag or branch>` for GitHub, `git archive HEAD` for a local clone (committed files only). Read its `VERSION`. `bash .claude/bequite/bin/bq-update.sh --check` answers "is there a new release" without changing anything.
3. **`check` mode:** list what would be added, changed, removed (the source's `.claude/bequite/REMOVED.txt`) and which changed files you edited locally. Stop.
4. **Back up** to `.bequite/backups/<time>-v<old>/`: `.claude/commands`, the `bequite-*` skills, `.claude/bequite`, `.claude/hooks`, `.claude/agents`, `CLAUDE.md`, `commands.md`, the version file. If the backup fails, stop.
5. **Merge:**
   - a pack file you did not edit is replaced;
   - a pack file you edited stays, and the new version is written beside it as `<file>.bequite-update.md` for you to merge (`force` replaces it; the backup has your copy);
   - files the new version removed are moved to `.bequite/backups/<time>-removed/`, never deleted, and a hook your settings still run is kept;
   - missing `.bequite/` templates are added; packs follow `PACKS.md`.
6. **Never touched:** everything you or the agent wrote in `.bequite/` (state, logs, work folders, audits, plans, research, knowledge, jobs, money, DNA files), `CHANGELOG.md`, and `CLAUDE.md` outside the `<!-- BEQUITE -->` block.
7. **Version and log:** rewrite the version lines in `BEQUITE_VERSION.md`, append the run to `.bequite/logs/UPDATE_LOG.md` (from, to, source and commit, counts, files kept with a sibling, the backup path).
8. **Check the result:** `.claude/commands/bequite.md` and `.claude/bequite/bin/bq-update.sh` exist and the version matches. If not, copy the backup back and report the failure.

## Output

```
BeQuite v<old> -> v<new> from <source>@<tag or commit>
Updated <n>, added <n>, moved aside <n>, kept with a sibling to merge <n>
Backup: .bequite/backups/<time>-v<old>/    Log: .bequite/logs/UPDATE_LOG.md
Next: /bequite short
```

## Quality gate

A backup exists before any change; no memory file was touched; every local edit survived as the file itself or in the backup; the version file matches what is installed; a failed update was rolled back and reported as failed.

## Next Command Recommendations (typical)

`/bequite short` to confirm the state is intact · `/bq-help` for new commands · merge any `.bequite-update.md` siblings.
