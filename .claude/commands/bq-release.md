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
