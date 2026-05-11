# Workflow gates

This file is **the gate system**. Every BeQuite command reads it on entry. If a precondition is not met, the command stops with a clear error + next-valid-command hint.

**Don't edit this file by hand.** It's machine-tracked. Commands update it after they complete.

---

## Current state

**Mode:** `(none yet — run /bq-mode)`
**Phase:** P0 — Setup and Discovery
**Last completed command:** `/bq-init` (this scaffold)
**Last completed timestamp:** 2026-05-11 (fresh BeQuite install)

---

## Gate ledger

Format: `GATE_NAME` — `state` — `evidence`

### Phase 0 — Setup and Discovery

| Gate | State | Evidence required |
|---|---|---|
| `MODE_SELECTED` | ❌ pending | `.bequite/state/CURRENT_MODE.md` has a valid mode |
| `BEQUITE_INITIALIZED` | ✅ done | `.bequite/state/PROJECT_STATE.md` exists |
| `DISCOVERY_COMPLETE` | ❌ pending | `.bequite/audits/DISCOVERY_REPORT.md` exists with sections 1-13 filled |
| `DOCTOR_COMPLETE` | ❌ pending | `.bequite/audits/DOCTOR_REPORT.md` exists; no BLOCKER findings |

### Phase 1 — Product Framing and Research

| Gate | State | Evidence required |
|---|---|---|
| `CLARIFY_ANSWERED` | ❌ pending | `.bequite/state/OPEN_QUESTIONS.md` has 3-5 questions with answers |
| `RESEARCH_COMPLETE` | ❌ pending | `.bequite/research/RESEARCH_REPORT.md` exists with all 11 dimensions |
| `SCOPE_LOCKED` | ❌ pending | `.bequite/plans/SCOPE.md` exists; user approved |
| `PLAN_APPROVED` | ❌ pending | `.bequite/plans/IMPLEMENTATION_PLAN.md` exists; user approved |
| `MULTI_PLAN_DECISION` | ⚪ optional | If user invoked `/bq-multi-plan`, `.bequite/plans/MERGED_IMPLEMENTATION_PLAN.md` exists + user approved |

### Phase 2 — Build

| Gate | State | Evidence required |
|---|---|---|
| `TASKS_ASSIGNED` | ❌ pending | `.bequite/tasks/TASKS.md` exists with atomic tasks |
| `IMPLEMENTATION_STARTED` | ❌ pending | At least one task marked `[~]` or `[x]` |
| `IMPLEMENTATION_DONE` | ❌ pending | All required tasks marked `[x]`; no `[!]` blocked |

### Phase 3 — Quality

| Gate | State | Evidence required |
|---|---|---|
| `TESTS_PASS` | ❌ pending | `/bq-test` reports green; no failing tests |
| `AUDIT_COMPLETE` | ❌ pending | `.bequite/audits/FULL_PROJECT_AUDIT.md` exists; no BLOCKER findings |
| `REVIEW_APPROVED` | ❌ pending | Latest `.bequite/audits/REVIEW-*.md` verdict = Approved or Approved-with-comments |
| `RED_TEAM_RESOLVED` | ⚪ optional | Latest `.bequite/audits/RED_TEAM-*.md` blockers resolved |

### Phase 4 — Ship

| Gate | State | Evidence required |
|---|---|---|
| `VERIFY_PASSED` | ❌ pending | `.bequite/audits/VERIFY_REPORT.md` verdict = PASS within last 24h |
| `RELEASE_PREPPED` | ❌ pending | Version bumped; CHANGELOG `[Unreleased]` moved to versioned section |
| `CHANGELOG_UPDATED` | ❌ pending | `CHANGELOG.md` has entries for this release |

### Phase 5 — Continue Later

| Gate | State | Evidence required |
|---|---|---|
| `MEMORY_SNAPSHOT` | ⚪ optional | `.bequite/state/SNAPSHOT-<timestamp>.md` exists if requested |
| `HANDOFF_GENERATED` | ⚪ optional | `.bequite/handoff/HANDOFF.md` or repo-root `HANDOFF.md` exists if requested |

---

## Required gates by command

Each command has a list of gates that MUST be in state `✅ done` before the command runs. If any required gate is `❌ pending`, the command refuses to run and tells you what to do first.

| Command | Required gates |
|---|---|
| `/bequite` | (none — always runs; it's the menu) |
| `/bq-help` | (none) |
| `/bq-init` | (none) |
| `/bq-mode` | `BEQUITE_INITIALIZED` |
| `/bq-new` | `BEQUITE_INITIALIZED` + `MODE_SELECTED = New Project` |
| `/bq-existing` | `BEQUITE_INITIALIZED` + `MODE_SELECTED = Existing Project Audit` |
| `/bq-discover` | `BEQUITE_INITIALIZED` |
| `/bq-doctor` | `BEQUITE_INITIALIZED` |
| `/bq-clarify` | `DISCOVERY_COMPLETE` |
| `/bq-research` | `DISCOVERY_COMPLETE` |
| `/bq-scope` | `RESEARCH_COMPLETE` |
| `/bq-plan` | `SCOPE_LOCKED` (or for fast mode, `RESEARCH_COMPLETE`) |
| `/bq-multi-plan` | `PLAN_APPROVED` (multi-plan is post-plan validation) |
| `/bq-assign` | `PLAN_APPROVED` (or `MULTI_PLAN_DECISION` if multi-plan was run) |
| `/bq-implement` | `TASKS_ASSIGNED` |
| `/bq-feature` | `BEQUITE_INITIALIZED` (feature mode self-contained) |
| `/bq-fix` | `BEQUITE_INITIALIZED` (fix mode self-contained) |
| `/bq-test` | `IMPLEMENTATION_STARTED` |
| `/bq-audit` | `IMPLEMENTATION_DONE` (or anytime for an audit-only mode) |
| `/bq-review` | `IMPLEMENTATION_DONE` |
| `/bq-red-team` | `IMPLEMENTATION_DONE` |
| `/bq-verify` | `TESTS_PASS` + `REVIEW_APPROVED` |
| `/bq-release` | `VERIFY_PASSED` |
| `/bq-changelog` | (none — can be run anytime) |
| `/bq-memory` | `BEQUITE_INITIALIZED` |
| `/bq-recover` | `BEQUITE_INITIALIZED` |
| `/bq-handoff` | `VERIFY_PASSED` (handoff implies ship-ready) |
| `/bq-auto` | `BEQUITE_INITIALIZED` + `MODE_SELECTED` |
| `/bq-p0` | (none — orchestrates Phase 0) |
| `/bq-p1` | All P0 gates done |
| `/bq-p2` | All P1 gates done |
| `/bq-p3` | All P2 gates done |
| `/bq-p4` | All P3 gates done |
| `/bq-p5` | All P4 gates done |

---

## Next valid commands

Based on current state above, the commands you can run RIGHT NOW are:

1. `/bequite` (always)
2. `/bq-help`
3. `/bq-init` (already done; safe to re-run)
4. `/bq-mode` — select your mode
5. `/bq-discover` — inspect the repo
6. `/bq-doctor` — environment health
7. `/bq-p0` — orchestrate all of Phase 0

Run `/bequite` for an interactive menu that reads this state.

---

## How commands update this file

Each command, after successfully completing, does:

1. Set its gate(s) to `✅ done`
2. Update "Last completed command" + timestamp
3. Recompute "Next valid commands"
4. Commit the change (atomic — same operation as the command's main output)

Commands NEVER mark a gate `✅ done` if their quality-gate check failed.

---

## Mode-specific gate overrides

Some modes skip gates that don't apply.

### Mode: Fix Problem (`/bq-fix`)

Skips:
- `MODE_SELECTED` (implicit from `/bq-fix` invocation)
- `RESEARCH_COMPLETE` (fix doesn't usually need 11-dim research)
- `SCOPE_LOCKED` (fix scope is "make the bug stop")
- `PLAN_APPROVED` (the fix is itself a mini-plan)

Requires:
- `BEQUITE_INITIALIZED`
- Fix-specific gates: `BUG_REPRODUCED`, `ROOT_CAUSE_IDENTIFIED`, `FIX_APPLIED`, `FIX_VERIFIED`

### Mode: Add Feature (`/bq-feature`)

Skips:
- `MODE_SELECTED = New Project | Existing Audit` (this is a different mode)

Requires:
- `BEQUITE_INITIALIZED`
- Feature-specific gates: `FEATURE_TYPE_IDENTIFIED`, `FEATURE_SPEC_APPROVED`, `FEATURE_IMPLEMENTED`, `FEATURE_TESTED`

### Mode: Research Only

Requires:
- `BEQUITE_INITIALIZED`
- `DISCOVERY_COMPLETE`
- `RESEARCH_COMPLETE`

Stops there. Doesn't proceed to scope/plan/build.

### Mode: Release Readiness

Requires:
- `BEQUITE_INITIALIZED`
- `IMPLEMENTATION_DONE` (must already be built)

Then runs P3 + P4 only.
