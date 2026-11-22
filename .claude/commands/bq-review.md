---
description: 'Review the current changes (uncommitted diff or recent commits): spec compliance first, then code quality, with file:line evidence for every finding and a guard pass on generated code. Arguments - a git range, delegate (review a cheaper model''s implementation), persona (a simulated user walks the feature). Verdict: Approved, Approved with comments, or Blocked.'
---

# /bq-review: spec first, then quality

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Stage 8 of `PIPELINE.md`. Procedure: `bequite-guard-pass` (the failure modes generated work shows), `bequite-security-reviewer` on risky paths, `bequite-frontend-quality` on UI diffs. When the review must be independent of the builder, pass 1 goes to a fresh subagent that sees only the diff and the criteria.

## Syntax

```
/bq-review [<git range or branch>] [delegate | persona]
```

Default scope: uncommitted changes plus the last one to three commits. `delegate` reviews the task pack results in `work/<id>/delegate/` task by task (approved, approved with comments, rejected). `persona` walks the feature as a named user and reports friction, not code.

## Gates

Needs `BEQUITE_INITIALIZED` and a diff to review. Sets `REVIEW_APPROVED` on Approved or Approved with comments.

## Steps

1. **Scope the diff** (`git status`, `git diff`, the range given). No diff: stop and say so.
2. **Read what was asked:** `work/<id>/spec.md`, `plan.md`, `tasks.md`, `.bequite/state/DECISIONS.md`, `PROJECT_DNA.md`.
3. **Pass 1, spec compliance.** Is every required item implemented? Are the listed edge cases tested? Did anything outside the task change (a refactor riding along)? Does new code follow the project's conventions and dependency direction? Pass 2 does not start until pass 1 is clean.
4. **Pass 2, quality, per changed file:** correctness, tests, edge cases (null, async errors, off-by-one, races), security (secrets, validation, auth, injection), naming, duplication, performance, reversibility. UI diffs also get design continuity against `.bequite/design/DESIGN_DNA.md` (a polished hero with a generic middle section is not approved).
5. **Guard pass** on generated code: invented APIs, hardcoded success, catch-alls that hide errors, tests that mock the thing under test, docs that no longer match.
6. **Risky domains:** every risk the plan's System Design Risk Check names needs a visible mitigation and a test in the diff. A new dependency without the ten decision questions answered is a blocker.
7. **Write `work/<id>/review.md`** (a dated section): verdict, per-file findings, cross-cutting concerns, action items before merge and after.

## Rules

- Every finding quotes the code at `file:line`. No quote, no finding.
- Flag only what affects correctness or the stated requirements; do not manufacture gaps, and do not fight the project's existing conventions.
- A missing test for a changed branch is a real finding.
- Things unrelated to this diff go to `.bequite/state/OPEN_QUESTIONS.md`, not into the review.
- The review reports; fixes happen in `/bq-implement` or `/bq-fix`.

## Output

```
Review: Approved | Approved with comments | Blocked    files: <n>   findings: <blockers>/<comments>
Report: .bequite/work/<id>/review.md
Next: /bq-verify, or /bq-fix "<blocker>"
```

## Quality gate

Pass 1 ran before pass 2; every finding has a quote; the verdict is explicit; repeat patterns went to `MISTAKE_MEMORY.md`.

## Next Command Recommendations (typical)

Approved: `/bq-verify`. Blocked: `/bq-fix` or `/bq-implement`. High stakes: `/bq-red-team`.
