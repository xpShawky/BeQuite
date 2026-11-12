# Workflow gates

The gate system. Every BeQuite command checks gates on entry; if a required gate is not done, the command stops, names the missing gate, and recommends the command that satisfies it.

Gates live in two places (v4):
- **Project gates** - this file. Things true for the whole project.
- **Work gates** - `.bequite/work/<id>/gates.md` for the active work (see `.bequite/ACTIVE.md`). Everything from clarify to verify, plus fix / feature / web / motion gates. Each new piece of work starts with fresh gates.

Commands update gates only after their own checks pass, and record the evidence. Never mark a gate done without evidence.

---

## Current state

**Mode:** (none yet - run /bq-mode)
**Phase:** P0 - Setup and Discovery
**Active work:** see `.bequite/ACTIVE.md`
**Last completed command:** `/bq-init` (scaffold)
**Last completed timestamp:** (not yet - fresh install)

---

## Project gates

| Gate | State | Evidence required |
|---|---|---|
| `BEQUITE_INITIALIZED` | done | `.bequite/state/PROJECT_STATE.md` exists |
| `MODE_SELECTED` | pending | `.bequite/state/CURRENT_MODE.md` has a valid mode |
| `DISCOVERY_COMPLETE` | pending | `.bequite/audits/DISCOVERY_REPORT.md` exists with sections 1-13 filled |
| `DOCTOR_COMPLETE` | pending | `.bequite/audits/DOCTOR_REPORT.md` exists; no BLOCKER findings |
| `DESIGN_DNA_LOCKED` | conditional (frontend) | `.bequite/design/DESIGN_DNA.md` filled and `Status: locked` before the first UI code |
| `AUDIT_COMPLETE` | optional | `.bequite/audits/FULL_PROJECT_AUDIT.md` exists; no BLOCKER findings |
| `RELEASE_PREPPED` | pending | version bumped; CHANGELOG `[Unreleased]` moved to a versioned section |
| `CHANGELOG_UPDATED` | pending | `CHANGELOG.md` has entries for this release |
| `MEMORY_SNAPSHOT` | optional | `.bequite/state/SNAPSHOT-<timestamp>.md` exists if requested |
| `HANDOFF_GENERATED` | optional | `.bequite/handoff/HANDOFF.md` or repo-root `HANDOFF.md` exists if requested |

## Work gates (in `work/<id>/gates.md`)

Core: `CLARIFY_ANSWERED` · `RESEARCH_COMPLETE` · `SCOPE_LOCKED` · `PLAN_APPROVED` · `MULTI_PLAN_DECISION` (optional) · `TASKS_ASSIGNED` · `IMPLEMENTATION_STARTED` · `IMPLEMENTATION_DONE` · `TESTS_PASS` · `REVIEW_APPROVED` · `RED_TEAM_RESOLVED` (optional) · `VERIFY_PASSED` · `CONVERGED`
Fix: `BUG_REPRODUCED` · `ROOT_CAUSE_IDENTIFIED` · `FIX_APPLIED` · `FIX_VERIFIED`
Feature: `FEATURE_TYPE_IDENTIFIED` · `FEATURE_SPEC_APPROVED` · `FEATURE_IMPLEMENTED` · `FEATURE_TESTED`
Web / UI: `DESIGN_CONTINUITY_PASS` (alias `DESIGN_CONTINUITY_OK`) · `VISUAL_QA_DONE` · `PERF_BUDGET_PASS`
Motion: `SCRIPT_APPROVED` · `STYLE_LOCKED` · `RENDER_PLAN_APPROVED` · `PICTURE_LOCKED` · `AUDIO_APPROVED` · `FINAL_QC_PASS` · `DELIVERY_APPROVED`

---

## Required gates by command

`(work)` = checked in the active work's `gates.md`. A command that starts new work creates the work folder first.

| Command | Required gates |
|---|---|
| `/bequite`, `/bq-help`, `/bq-now`, `/bq-explain`, `/bq-init` | none |
| `/bq-mode`, `/bq-discover`, `/bq-doctor`, `/bq-memory`, `/bq-recover`, `/bq-work` | `BEQUITE_INITIALIZED` |
| `/bq-new` | `BEQUITE_INITIALIZED` + `MODE_SELECTED = New Project` |
| `/bq-existing` | `BEQUITE_INITIALIZED` + `MODE_SELECTED = Existing Project Audit` |
| `/bq-clarify`, `/bq-research` | `DISCOVERY_COMPLETE` (starts or uses the active work) |
| `/bq-scope` | `RESEARCH_COMPLETE` (work) |
| `/bq-plan` | `SCOPE_LOCKED` (work); fast mode: `RESEARCH_COMPLETE` (work) |
| `/bq-multi-plan` | `PLAN_APPROVED` (work) |
| `/bq-assign` | `PLAN_APPROVED` (work), or `MULTI_PLAN_DECISION` (work) |
| `/bq-implement` | `TASKS_ASSIGNED` (work) |
| `/bq-feature`, `/bq-fix`, `/bq-spec` | `BEQUITE_INITIALIZED` (self-contained; create their own work) |
| `/bq-motion` | `BEQUITE_INITIALIZED` (creates a `motion` work; its phases are gated by the motion work gates) |
| `/bq-test` | `IMPLEMENTATION_STARTED` (work) |
| `/bq-review`, `/bq-red-team` | `IMPLEMENTATION_DONE` (work) |
| `/bq-audit` | `BEQUITE_INITIALIZED` (project audit; anytime) |
| `/bq-verify` | `TESTS_PASS` + `REVIEW_APPROVED` (work) |
| `/bq-release` | `VERIFY_PASSED` + `CONVERGED` (work) |
| `/bq-handoff` | `VERIFY_PASSED` (work) |
| `/bq-changelog` | none |
| `/bq-auto` | `BEQUITE_INITIALIZED` + `MODE_SELECTED` |
| `/bq-p0` ... `/bq-p5` | the previous phase's gates |
| Capability commands (`/bq-presentation`, `/bq-course`, `/bq-offer`, ...) | `BEQUITE_INITIALIZED` (each creates its own work item) |

### Frontend design continuity (when a frontend exists)

| Command | Behaviour |
|---|---|
| `/bq-feature` (UI types) | requires `DESIGN_DNA_LOCKED`; runs continuity on every section before "done" |
| `/bq-fix` (visual) | re-runs continuity on the touched page |
| `/bq-auto` (uiux / frontend / live-edit / variants) | completion requires `DESIGN_CONTINUITY_PASS` + `VISUAL_QA_DONE` + `PERF_BUDGET_PASS` (work) |
| `/bq-uiux-variants`, `/bq-live-edit` | continuity-check each variant / edited section |
| `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify` | include the design-continuity and performance dimensions |

---

## Mode-specific overrides

- **Fix Problem** skips `MODE_SELECTED`, `RESEARCH_COMPLETE`, `SCOPE_LOCKED`, `PLAN_APPROVED`; requires the fix gates in the work.
- **Add Feature** requires the feature gates in the work.
- **Research Only** stops after `RESEARCH_COMPLETE` (work).
- **Release Readiness** requires `IMPLEMENTATION_DONE` (work), then runs quality + release only.

## How commands update gates

1. Set their gate(s) to done with the evidence (file or command), in this file or the work's `gates.md`.
2. Update "Last completed command" and timestamp above.
3. Never mark a gate done when its own check failed.
