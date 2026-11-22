---
description: Fix a broken behaviour, reproduce first. Classifies it with the 15-type router, loads the matching specialists, captures the exact error, finds the root cause, makes the smallest patch, adds a regression test that fails before and passes after, verifies the symptom is gone and logs it to ERROR_LOG.md.
---

# /bq-fix: reproduce, root cause, smallest patch, proof

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

A route into `PIPELINE.md` stages 0, 1, reproduce, 5 (root cause and patch plan), 7, 8, 9, 10. The type router: `.claude/bequite/docs/architecture/FEATURE_AND_FIX_WORKFLOWS.md` (section "/bq-fix: 15-type router"). Procedure: `bequite-problem-solver`.

## Syntax

```
/bq-fix "<symptom in the user's words>" [type=<1-15 or name>] [mode]
```

## Gates

`BEQUITE_INITIALIZED`. Visual or cross-browser fixes (types 1 and 15) re-run the Design Continuity Gate on the touched sections. A fix that changes auth, a migration on a shared database or production config is a hard human gate.

## Steps

1. **Get the bug:** the symptom, where, since when, what changed. Small fix inside the active work, or a new work (`/bq-work new "<symptom>" type=fix`).
2. **Classify** with the 15-type router (frontend, backend, database, auth, build, test failure, deployment/CI, performance, security, dependency, configuration, network/integration, memory/resource, race/async, cross-platform); load its skills plus `bequite-testing-gate`.
3. **Reproduce** before touching code: the exact steps or a failing test. No reproduction: say so, collect more (logs, versions, inputs) and stop rather than guess.
4. **Capture the exact error** (message, stack, request, environment) in `.bequite/logs/ERROR_LOG.md` with a UTC time and the one-line symptom.
5. **Mini-spec** in the work: symptom, reproduction, hypothesis, files the fix will touch, test plan, rollback.
6. **Root cause** with evidence: narrow by logs, `git bisect`, `git log -S` (pickaxe), a minimal input. Name the cause in one sentence; a fix for a symptom without a cause is not done.
7. **Fix the smallest cause.** No refactor riding along.
8. **Regression test** that fails on the old code and passes on the new; paste both runs.
9. **Verify** the original symptom is gone the way the user saw it (the browser, the command, the endpoint) and the suite is green.
10. **Write back:** `ERROR_LOG.md` (cause and fix), the work log, `CHANGELOG.md` `### Fixed` when users saw the bug, `MISTAKE_MEMORY.md` when the cause is a pattern that can recur, the regression ledger.

## Output

```
✓ /bq-fix "<symptom>" (type <n>: <name>)
Cause: <one sentence>   Patch: <files, lines>
Regression test: <name> failed before, passes after
Verified: <how>   Suite: <pass>/<total>
Next: /bq-review or /bq-verify
```

## Quality gate

Reproduced before fixing; a named root cause; a regression test proven to fail first; the symptom checked the way the user saw it; three failed attempts in a row stop and ask.

## Next Command Recommendations (typical)

`/bq-review` · `/bq-verify` · `/bq-test` if the area had no tests.
