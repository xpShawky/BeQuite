---
name: bequite-updater
description: Use for /bq-update, when the automatic update check reports a new version it will not install by itself (Auto update off, a fork, a branch, a local clone), when an update failed, or when the user asks how BeQuite updates itself. Fetches one commit, backs up, merges around local edits, never touches project memory, and rolls back on failure.
last_verified: 2026-11-22
sources:
  - https://docs.github.com/en/rest/releases/releases  # "latest release" = most recent non-prerelease, non-draft release
  - https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api  # 60 unauthenticated requests per hour per address
  - https://git-scm.com/docs/git-clone  # --depth 1 --branch <tag> (a tag detaches HEAD at that commit)
  - https://git-scm.com/docs/git-archive  # exports the tree of a named commit, not the working tree
  - https://semver.org/  # MAJOR, MINOR, PATCH
  - https://keepachangelog.com/en/1.1.0/  # Added, Changed, Deprecated, Removed, Fixed, Security
  - https://code.claude.com/docs/en/plugins-reference  # plugin installs are versioned and updated by the harness
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

# bequite-updater

Two paths update BeQuite. The **automatic** one is a script and needs no judgement; this skill is the **manual** one, for everything the script refuses to do by itself.

## When to use

- `/bq-update`, in any mode.
- The update line says "available" (Auto update is off, the source is a fork, a branch or a path the script will not run).
- The update line says "failed", or files look half-updated.
- The user edited BeQuite's own commands or skills and wants to keep those edits through an update.

Not for: a first install (the installers in the README); plugin installs (the harness updates them through `/plugin`); the user's own project code.

## What the automatic path does (so you can explain and debug it)

`.claude/bequite/bin/bq-update.sh` runs as step 1 of every command, at most once an hour (a failed install waits a day).

| It installs by itself | It only reports |
|---|---|
| the latest published GitHub Release of the official repo (prereleases and drafts do not count) | any other repo |
| the tag in "Pinned tag" | a branch (unreleased commits) |
| the last commit of a local BeQuite clone at an absolute path outside the project | a path inside the project, a relative path, a value that fails validation |

It clones or archives **one commit**, checks that commit's `VERSION`, backs up, runs that commit's installer, checks the result, and copies the backup back if anything failed. A lock stops two sessions updating at once. Results and the reason for a skip are in `.bequite/state/UPDATE_CHECK.md`; every install is in `.bequite/logs/UPDATE_LOG.md`. In the BeQuite source repo itself it always skips.

## Procedure (manual update)

1. **Read** `.bequite/state/BEQUITE_VERSION.md`, `UPDATE_SOURCE.md`, `PACKS.md`, and the last entries of `UPDATE_LOG.md`.
2. **Name the source and get a yes when it is not an official release.** A fork, a branch or a local clone means running code nobody released: say which repo and which commit, and wait.
3. **Fetch one commit into a temp folder:** `git clone --depth 1 --branch <tag or branch> <url>` or, for a local clone, `git -C <path> archive HEAD | tar -x -C <tmp>` (committed files only). Read its `VERSION`.
4. **`check` mode:** list files that would be added, changed and removed (the source's `.claude/bequite/REMOVED.txt`), and which changed files the user edited (compare with the backup of the last update, or ask). Stop there.
5. **Back up** to `.bequite/backups/<time>-v<old>/`: `.claude/commands`, the `bequite-*` skills, `.claude/bequite`, `.claude/hooks`, `.claude/agents`, `CLAUDE.md`, `commands.md`, `BEQUITE_VERSION.md`. No backup, no update.
6. **Merge:**
   - not edited locally: replace;
   - edited locally: keep the user's file and write the new one beside it as `<file>.bequite-update.md`; list these for the user (`force` replaces, the backup keeps their copy);
   - removed upstream: move to `.bequite/backups/<time>-removed/`; a hook the user's settings still run stays where it is;
   - missing `.bequite/` templates: add; packs: follow `PACKS.md`.
7. **Never touch:** anything the user or the agent wrote in `.bequite/` (state, logs, work folders, audits, plans, research, DNA files), `CHANGELOG.md`, and `CLAUDE.md` outside the `<!-- BEQUITE -->` block. The block is replaced only when both markers exist.
8. **Check and record:** `.claude/commands/bequite.md` and `.claude/bequite/bin/bq-update.sh` exist and the version file matches the source's `VERSION`. Then write `UPDATE_LOG.md` (from, to, source and commit, counts, files kept with a sibling, the backup path). If the check fails, copy the backup back and report a failed update.

## Worked example (real runs, 2026-11-22)

- **A v4 project moved to v1 by hand:** the project had `**Version:** v4.0.0` and GitHub as its source; v4 has no update script, so it cannot update itself. One forced install from a local clone: exit 0, "55 commands, 38 skills, 4 subagents", 17 files that v1 removed moved to `.bequite/backups/<time>-removed/`, version line `v4.0.0 -> v1.0.0`, memory and the user's own folders untouched. The next check printed "no release found" (nothing was released yet), exit 0.
- **The automatic path under test** (`scripts/test_update.sh`, 21 checks, exit 0): an old version line containing `/` is rewritten correctly; uncommitted files in the source are not installed; a held lock stops a second install; a failing installer ends with the previous files put back and no retry the same day; a source inside the project, a relative path, another repo and a malformed repo are all refused.

## Quality gate

- A backup existed before the first changed file.
- No memory file changed; every local edit survived as the file or in the backup.
- The installed version equals the fetched commit's `VERSION`, and that commit is named in the log.
- A failed update was rolled back and reported as failed, never as done.

## Boundaries

No install from a source the user did not approve when it is not an official release. No deletion: removed files are moved. No change to `.gitignore`, hooks settings or anything outside BeQuite's own files without a yes. Backups are never pruned automatically: they may hold the user's edits.
