---
description: 'Phase 4 orchestrator — Release. Walks /bq-verify → /bq-changelog → /bq-release (instructions only, never auto-pushes). Goal: ship the change with a clean trail.'
---

# /bq-p4 — Phase 4 orchestrator: Release

## Purpose

Run Phase 4 commands. P4's job is to **ship**. Full gate matrix verifies, CHANGELOG sharpened, release commands printed. **Nothing is auto-pushed** — the user runs the git commands themselves.

## When to use it

- P3 complete (tests pass, review approved, no blockers)
- You're ready to tag + release
- You want one command instead of three

## Preconditions

- `BEQUITE_INITIALIZED ✅`
- `MODE_SELECTED ✅`
- P3 complete OR mode = Release Readiness

## Required previous gates

| Mode | Required |
|---|---|
| New Project | `TEST_DONE ✅`, `REVIEW_DONE ✅` |
| Add Feature | `TEST_DONE ✅`, `REVIEW_DONE ✅` |
| Fix Problem | `TEST_DONE ✅`, `REVIEW_DONE ✅` |
| Release Readiness | `TEST_DONE ✅`, `AUDIT_DONE ✅`, `REVIEW_DONE ✅` |
| Existing Audit | (P4 skipped — no release) |
| Research Only | (P4 skipped) |

## Files to read

- `.bequite/plans/IMPLEMENTATION_PLAN.md` (acceptance criteria)
- `.bequite/audits/FULL_PROJECT_AUDIT.md` (if exists)
- `package.json` / `pyproject.toml` / `Cargo.toml` (current version)
- `.bequite/logs/CHANGELOG.md` (`[Unreleased]` section)
- `git log` (commits since last tag)

## Files to write

- `.bequite/audits/VERIFY_REPORT.md` (via `/bq-verify`)
- `.bequite/logs/CHANGELOG.md` (via `/bq-changelog` — moves `[Unreleased]` to `[vX.Y.Z]`)
- `.bequite/state/WORKFLOW_GATES.md` (gates ticked)
- `.bequite/state/CURRENT_PHASE.md` (advances to P5)
- Version bumped in `package.json` / `pyproject.toml` etc. (via `/bq-release`)
- `.bequite/logs/AGENT_LOG.md`

## Steps

### 1. /bq-verify

Run every applicable gate: install / lint / typecheck / unit / integration / build / smoke / e2e. Write VERIFY_REPORT.md.

If FAIL → **stop here**. Print the failures. Loop back to P2/P3.

If PASS → mark `VERIFY_PASS ✅`.

### 2. /bq-changelog

Categorize commits since last tag into Added / Changed / Fixed / Deprecated / Removed / Security per Keep a Changelog v1.1. Sharpen wording (no weasel).

Mark `CHANGELOG_READY ✅`.

### 3. /bq-release

Compute the version bump (patch / minor / major based on changelog content + user confirmation).

Move `[Unreleased]` → `[vX.Y.Z]` in CHANGELOG with today's date.

Bump version in manifest files.

**Print the git commands.** Do NOT execute them. User runs:

```bash
git add -A
git commit -m "release: vX.Y.Z"
git tag vX.Y.Z
git push origin main
git push origin vX.Y.Z
```

**Hard human gate.** Wait for user to confirm they ran the commands (or said "skip — local only").

Mark `RELEASE_READY ✅`.

### 4. Mark phase complete

If `VERIFY_PASS ✅` + `CHANGELOG_READY ✅` + `RELEASE_READY ✅`:
- Set `.bequite/state/CURRENT_PHASE.md` → `P5 — Memory and Handoff`

### 5. Print summary

```
✓ Phase 4 complete — Release

Mode:           <mode>
Verify:         PASS ✓
Version:        <old> → <new>
CHANGELOG:      vX.Y.Z entry written
Git commands:   printed (user runs them)

Next phase: P5 — run /bq-p5 or /bq-memory snapshot
```

## Output format

Narrate each step. Highlight git commands clearly. At end, print summary.

## Quality gate

- `VERIFY_PASS ✅`
- `CHANGELOG_READY ✅`
- `RELEASE_READY ✅`
- Version bump matches changelog content (no patch bump for breaking changes)
- All git commands shown (none auto-executed)

## Failure behavior

- `/bq-verify` FAIL → pause; loop back to P2/P3
- User refuses to bump version → keep version unchanged; release stays `[Unreleased]`; mark `RELEASE_READY ⚪ deferred`
- Manifest file unreadable → log error; ask user for which file holds the version

## Usual next command

- `/bq-p5` — run Phase 5 (Memory and Handoff)
- Or `/bq-handoff` directly (if shipping to a second engineer)
- Or done (if this was a solo release)
