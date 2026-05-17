---
description: Final release prep after /bq-verify passed. Updates CHANGELOG, suggests tag, shows the push command. Never auto-pushes; the user confirms.
---

# /bq-release — release prep

You are preparing the **ship** step. Verify has passed. Now: update CHANGELOG, propose a tag, hand the user the exact commands to push.

## Step 1 — Read context

- `.bequite/audits/VERIFY_REPORT.md` (must exist + must say PASS)
- `.bequite/logs/CHANGELOG.md` (this project's changelog)
- `.bequite/plans/SCOPE.md`
- `.bequite/tasks/TASK_LIST.md` (every task `[x] done`?)
- `package.json` / `pyproject.toml` / `Cargo.toml` (current version)

## Step 2 — Block if not ready

Don't proceed unless:
- `VERIFY_REPORT.md` exists AND says PASS
- No `[!] blocked` tasks
- No `[~] in-progress` tasks

If any block: print why + suggest the right next command. Exit.

## Step 3 — Propose the version bump

Based on the kind of changes (read recent commit messages):

- Bug fixes only → patch bump (`v1.2.3` → `v1.2.4`)
- New features, backwards-compatible → minor bump (`v1.2.3` → `v1.3.0`)
- Breaking changes → major bump (`v1.2.3` → `v2.0.0`)
- Pre-1.0 → looser; suggest patch unless a major change happened

Ask the user:
> "Propose `v1.3.0` (minor — new features, backwards-compat). OK? (y/n/custom)"

## Step 4 — Update CHANGELOG.md

Run `/bq-changelog` internally (or invoke the same logic):

- Read all `[Unreleased]` section
- Move it under `## [<new-version>] — <today>` heading
- Re-create an empty `## [Unreleased]` at top

For each entry, ensure:
- It has Added / Changed / Fixed / Deprecated / Removed / Security section
- It cites the spec file or commit if relevant

## Step 5 — Update version in manifests

Bump:
- `package.json::version` (Node)
- `pyproject.toml::version` (Python)
- `Cargo.toml::version` (Rust)
- Per-app manifests if monorepo

Show the diff. Don't commit yet — the user confirms.

## Step 6 — Print the release commands

Don't run these. Print them for the user to copy:

```
✓ Release prep ready

Version:  v<new>
Changes:  <summary> (see .bequite/logs/CHANGELOG.md)

To finish the release:

  git add -A
  git commit -m "release(v<new>): <summary line>"
  git tag -a v<new> -m "<short tag message>"
  git push origin main
  git push origin v<new>

To publish to PyPI / npm (if applicable):

  npm publish                  # or
  python -m build && twine upload dist/*

(Don't auto-publish — these are one-way doors. The user runs them.)
```

## Step 7 — Update state + log

- `.bequite/state/CURRENT_PHASE.md` → "Phase 4 — Ship → release prep"
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md` appended

## Step 8 — Report back (above)

## Rules

- **Never auto-push or auto-publish.** Tags and publishes are one-way doors. The user does them.
- **CHANGELOG must be sharp.** No "(no changes yet)". If you don't know what changed, read the commit log.
- **Verify must have passed.** Don't release if VERIFY_REPORT.md is FAIL or stale (>7 days old).
- **No "should be ready" claims.** Either verify passed or it didn't.

See `.claude/skills/bequite-release-gate/SKILL.md` for the deeper procedure (CI parity, signing, npm 2FA, etc.).

## Standardized command fields (alpha.6)

**Phase:** P4 — Release
**When NOT to use:** verify hasn't passed yet (run `/bq-verify` first); CHANGELOG `[Unreleased]` is empty (nothing to release).
**Preconditions:** `BEQUITE_INITIALIZED`, `VERIFY_PASS`, `CHANGELOG_READY`
**Required previous gates:** `BEQUITE_INITIALIZED`, `VERIFY_PASS`, `CHANGELOG_READY`
**Quality gate:**
- Version bumped in manifest (per semver: patch / minor / major matches CHANGELOG content)
- CHANGELOG `[Unreleased]` moved to `[vX.Y.Z]` with date
- Release commands printed (NOT executed — user runs `git push` + `git tag`)
- Marks `RELEASE_READY ✅` after user confirms they ran the commands
**Failure behavior:**
- Verify > 24h old → recommend re-running `/bq-verify` first (stale verify is a risk)
- Manifest unreadable → ask user which file holds the version
- Pre-1.0 with breaking change → require explicit user OK before bumping minor (per release-gate skill)
**Memory updates:** Bumps version in manifest(s). Moves CHANGELOG entry. Sets `RELEASE_READY ✅` after user confirmation.
**Log updates:** `AGENT_LOG.md`. CHANGELOG section header updated.

**Hard human gate (#17):** the actual `git push origin main`, `git tag -a vX.Y.Z`, and `git push origin vX.Y.Z` commands are user-run. Auto-mode prints them; never executes them.

## Memory files this command reads

- `.bequite/audits/VERIFY_REPORT.md`
- `.bequite/logs/CHANGELOG.md`
- `.bequite/plans/SCOPE.md`
- `.bequite/tasks/TASK_LIST.md`
- All version manifests

## Memory files this command writes

- `.bequite/logs/CHANGELOG.md` (Unreleased section moved into a versioned section)
- Version manifests (bumped)
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

- (Manual git commands, then) `/bq-handoff` (if handing off) or `/bequite` (back to the menu)

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
