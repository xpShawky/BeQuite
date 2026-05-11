---
description: Phase 3 orchestrator — Quality and Review. Walks /bq-test → /bq-audit (if requested) → /bq-review → optional /bq-red-team. Goal: confirm the build works before shipping.
---

# /bq-p3 — Phase 3 orchestrator: Quality and Review

## Purpose

Run Phase 3 commands. P3's job is to **confirm it works**. Tests run, code reviewed, optional adversarial red-team. No release yet.

## When to use it

- P2 complete (you have code to review) OR
- Mode = Existing Audit (audit is the goal, not build)
- You want full quality coverage before `/bq-verify`

## Preconditions

- `BEQUITE_INITIALIZED ✅`
- `MODE_SELECTED ✅`
- Code exists to test/review (or mode = Existing Audit)

## Required previous gates

Per mode:

| Mode | Required |
|---|---|
| New Project | `IMPLEMENT_DONE ✅` |
| Existing Audit | `DISCOVERY_DONE ✅` |
| Add Feature | `FEATURE_DONE ✅` |
| Fix Problem | `FIX_DONE ✅` |
| Release Readiness | (no required predecessor; full audit happens here) |
| Research Only | (skip; no code to review) |

## Files to read

- `.bequite/state/CURRENT_MODE.md`
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (acceptance criteria reference)
- `.bequite/audits/DISCOVERY_REPORT.md`
- Source code (touched files + recent commits)

## Files to write

- Test files (when /bq-test writes missing tests)
- `.bequite/audits/FULL_PROJECT_AUDIT.md` (via `/bq-audit`)
- `.bequite/audits/REVIEW_<date>.md` (via `/bq-review`)
- `.bequite/audits/RED_TEAM_<date>.md` (via `/bq-red-team`, optional)
- `.bequite/state/WORKFLOW_GATES.md` (gates ticked)
- `.bequite/state/CURRENT_PHASE.md` (advances to P4)
- `.bequite/logs/AGENT_LOG.md`

## Steps

### 1. /bq-test

Detect framework (vitest / jest / pytest / cargo test). Run them. Identify coverage gaps in recently-changed source files. Offer to write missing tests.

Mark `TEST_DONE ✅` once all tests pass.

### 2. /bq-audit (conditional)

Run if:
- Mode = Existing Audit (the audit IS the goal)
- Mode = Release Readiness
- User explicitly requested it

10-area audit: install / run / frontend / API / CLI / tests / docs / UX / security / release. Severity-tagged findings.

Mark `AUDIT_DONE ✅` if ran.

### 3. /bq-review

Per-file commentary on uncommitted diff + recent commits. Verdict per change: Approved / Approved-with-comments / Blocked.

Mark `REVIEW_DONE ✅`.

### 4. (Optional) /bq-red-team

Ask the user: "Run adversarial Skeptic? (y/N)"

If yes → 8 attack angles, severity-tagged findings, kill-shot questions. Mark `RED_TEAM_DONE ⚪ optional ✅`.

If no → skip.

### 5. Resolve blockers

If `/bq-review` or `/bq-red-team` produced **Blocker** findings:
- **Pause for user.**
- Print the blockers + suggested fixes.
- User chooses: fix now (loop back to P2), defer to backlog, or accept-with-justification.

### 6. Mark phase complete

If `TEST_DONE ✅` + `REVIEW_DONE ✅` (+ `AUDIT_DONE ✅` if applicable) + no unresolved blockers:
- Set `.bequite/state/CURRENT_PHASE.md` → `P4 — Release`

### 7. Print summary

```
✓ Phase 3 complete — Quality and Review

Mode:            <mode>
Tests:           <pass> / <total>          ✓
Coverage gaps:   <count>                    (filled / outstanding)
Audit findings:  Blocker: <n>  High: <n>  Med: <n>  Low: <n>
Review verdict:  <Approved / Approved-with-comments>
Red-team:        <ran / skipped>

Next phase: P4 — run /bq-p4 or /bq-verify
```

## Output format

Narrate each step. At the end, print summary.

## Quality gate

- All tests pass (`TEST_DONE ✅`)
- Review complete (`REVIEW_DONE ✅`)
- No unresolved Blocker findings
- Audit done (if mode requires it)

## Failure behavior

- Test red → log, pause for fix; do NOT advance to P4
- Audit finds Blocker → pause for user, surface concrete fix path
- Review verdict = Blocked → pause; loop back to P2 to address
- /bq-red-team finds critical kill-shot → pause for user discussion

## Usual next command

- `/bq-p4` — run Phase 4 (Release)
- Or `/bq-verify` directly (full gate matrix)
- Or `/bq-fix` (if a Blocker needs fixing first)
