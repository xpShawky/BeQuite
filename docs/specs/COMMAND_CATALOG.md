# BeQuite Command Catalog (v3.0.0-alpha.2)

**Status:** authored 2026-05-11
**Total commands:** 34 (1 root menu + 33 `/bq-*`)
**Total skills:** 14 (7 baseline + 7 specialist)

Single source of truth for every BeQuite command. Each entry lists: when to use, what it reads, what it writes, required previous gates, quality gate, usual next.

---

## The root menu

### `/bequite`
- **Purpose:** gate-aware project router
- **Phase:** any
- **Required gates:** none (read-only)
- **Reads:** all `.bequite/state/*` + `.bequite/logs/AGENT_LOG.md`
- **Writes:** none
- **Next:** the first item in "Recommended next 3"

---

## Phase 0 — Setup and Discovery

### `/bq-help`
- **Purpose:** full command reference grouped by phase
- **Required gates:** none
- **Writes:** none
- **Next:** any command from the list

### `/bq-init`
- **Purpose:** initialize `.bequite/` tree + baseline state files
- **Required gates:** none
- **Writes:** `.bequite/state/*` skeleton, `.bequite/logs/*` skeleton, CLAUDE.md addition
- **Quality gate sets:** `BEQUITE_INITIALIZED ✅`
- **Next:** `/bq-mode`

### `/bq-mode`
- **Purpose:** select / show workflow mode (6 modes)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/state/CURRENT_MODE.md`
- **Quality gate sets:** `MODE_SELECTED ✅`
- **Next:** per mode — `/bq-new`, `/bq-existing`, `/bq-feature`, `/bq-fix`, `/bq-research`, or `/bq-verify`

### `/bq-new`
- **Purpose:** New Project workflow entry; only for empty folders
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `CURRENT_MODE.md` → New Project; pre-queues 3 foundational questions in OPEN_QUESTIONS.md
- **Next:** `/bq-p0` or `/bq-clarify`

### `/bq-existing`
- **Purpose:** Existing Project Audit workflow entry
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `CURRENT_MODE.md` → Existing Audit; pre-queues audit-specific questions
- **Next:** `/bq-discover` then `/bq-doctor`

### `/bq-discover`
- **Purpose:** inspect repo → DISCOVERY_REPORT.md
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/audits/DISCOVERY_REPORT.md`
- **Quality gate sets:** `DISCOVERY_DONE ✅`
- **Next:** `/bq-doctor`

### `/bq-doctor`
- **Purpose:** environment health probe
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/audits/DOCTOR_REPORT.md`
- **Quality gate sets:** `DOCTOR_DONE ✅`
- **Next:** `/bq-clarify` or `/bq-p1`

---

## Phase 1 — Product Framing and Research

### `/bq-clarify`
- **Purpose:** ask 3-5 high-value clarifying questions
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`
- **Writes:** `.bequite/state/OPEN_QUESTIONS.md` (answers)
- **Quality gate sets:** `CLARIFY_DONE ✅`
- **Next:** `/bq-research`

### `/bq-research`
- **Purpose:** 11-dimension verified evidence (stack, product, competitors, failures, success, user journey, UX/UI, security, scalability, deployment, differentiation)
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `CLARIFY_DONE` (recommended)
- **Writes:** `.bequite/audits/RESEARCH_REPORT.md`, DECISIONS.md appended, OPEN_QUESTIONS.md resolved items marked
- **Quality gate sets:** `RESEARCH_DONE ✅`
- **Skills activated:** bequite-researcher, bequite-security-reviewer, bequite-ux-ui-designer (if UI)
- **Next:** `/bq-scope`

### `/bq-scope`
- **Purpose:** lock IN / OUT / NON-GOALS
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `RESEARCH_DONE` (recommended)
- **Writes:** `.bequite/plans/SCOPE.md`
- **Quality gate sets:** `SCOPE_LOCKED ✅`
- **Skills activated:** bequite-product-strategist
- **Next:** `/bq-plan` or `/bq-multi-plan`

### `/bq-plan`
- **Purpose:** write IMPLEMENTATION_PLAN.md (15 sections)
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `SCOPE_LOCKED` (strongly recommended)
- **Writes:** `.bequite/plans/IMPLEMENTATION_PLAN.md`
- **Quality gate sets:** `PLAN_APPROVED ✅` (after user confirms)
- **Skills activated:** bequite-project-architect, bequite-backend-architect, bequite-database-architect, bequite-security-reviewer, bequite-devops-cloud, bequite-ux-ui-designer (if UI), bequite-frontend-quality (if frontend), bequite-testing-gate
- **Next:** `/bq-multi-plan` or `/bq-assign`

### `/bq-multi-plan`
- **Purpose:** unbiased multi-model planning via manual paste
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `CLARIFY_DONE`, `RESEARCH_DONE`, `SCOPE_LOCKED`
- **Writes:** `.bequite/prompts/generated_prompts/*`, `.bequite/prompts/model_outputs/*`, `.bequite/plans/MULTI_MODEL_COMPARISON.md`, `IMPLEMENTATION_PLAN.md` (merged), `IMPLEMENTATION_PLAN_PRE_MERGE.md` (preserved)
- **Quality gate sets:** `MULTI_PLAN_DONE ✅` (optional)
- **Skills activated:** bequite-multi-model-planning, bequite-project-architect
- **Next:** `/bq-assign`

---

## Phase 2 — Planning and Build

### `/bq-assign`
- **Purpose:** break IMPLEMENTATION_PLAN → atomic TASK_LIST.md (≤5min tasks, dep-ordered, one acceptance each)
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `PLAN_APPROVED`
- **Writes:** `.bequite/tasks/TASK_LIST.md`
- **Quality gate sets:** `ASSIGN_DONE ✅`
- **Next:** `/bq-implement`

### `/bq-implement`
- **Purpose:** implement ONE approved task at a time
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `PLAN_APPROVED`, `ASSIGN_DONE`
- **Writes:** source files, `.bequite/tasks/CURRENT_TASK.md`, `.bequite/tasks/TASK_LIST.md` updated `[x]`, CHANGELOG `[Unreleased]`
- **Quality gate sets:** `IMPLEMENT_DONE ✅` when TASK_LIST empty
- **Skills activated:** depends on task type
- **Next:** `/bq-implement` (next task) or `/bq-test`

### `/bq-feature "title"`
- **Purpose:** Add Feature workflow with 12-type router
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`
- **Writes:** `.bequite/plans/feature-<slug>.md`, source files, tests
- **Quality gate sets:** `FEATURE_DONE ✅`
- **Skills activated:** per 12-type router (see bq-feature.md)
- **Next:** `/bq-review`

### `/bq-fix`
- **Purpose:** Fix workflow with 15-type router; reproduce-first
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`
- **Writes:** source fix, regression test, `.bequite/logs/ERROR_LOG.md`, `.bequite/audits/FIX_<slug>.md`, CHANGELOG if user-visible
- **Quality gate sets:** `FIX_DONE ✅`
- **Skills activated:** per 15-type router (see bq-fix.md); always plus bequite-problem-solver
- **Next:** `/bq-test`

### `/bq-add-feature` (legacy alias for `/bq-feature`)
- Kept for backwards compatibility; routes to bq-feature.

---

## Phase 3 — Quality and Review

### `/bq-test`
- **Purpose:** run + write tests; detect framework
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** new test files; nothing in state
- **Quality gate sets:** `TEST_DONE ✅` when all green
- **Skills activated:** bequite-testing-gate
- **Next:** `/bq-review` or `/bq-implement` (continue loop)

### `/bq-audit`
- **Purpose:** 10-area full project audit
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/audits/FULL_PROJECT_AUDIT.md`
- **Quality gate sets:** `AUDIT_DONE ✅` (optional unless Release Readiness mode)
- **Skills activated:** bequite-security-reviewer, bequite-frontend-quality (if UI), bequite-testing-gate, bequite-devops-cloud
- **Next:** `/bq-fix` (per findings) or `/bq-verify`

### `/bq-review`
- **Purpose:** review uncommitted diff + recent commits
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/audits/REVIEW_<date>.md`
- **Quality gate sets:** `REVIEW_DONE ✅`
- **Skills activated:** bequite-security-reviewer, bequite-testing-gate
- **Next:** `/bq-verify` or `/bq-fix` per verdict

### `/bq-red-team`
- **Purpose:** adversarial Skeptic review (8 attack angles)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/audits/RED_TEAM_<date>.md`
- **Quality gate sets:** `RED_TEAM_DONE ⚪ optional ✅`
- **Skills activated:** bequite-security-reviewer, bequite-problem-solver
- **Next:** `/bq-fix` per findings

---

## Phase 4 — Release

### `/bq-verify`
- **Purpose:** full gate matrix — install + lint + typecheck + unit + integration + build + smoke + e2e
- **Required gates:** `TEST_DONE`, `REVIEW_DONE`
- **Writes:** `.bequite/audits/VERIFY_REPORT.md`
- **Quality gate sets:** `VERIFY_PASS ✅`
- **Skills activated:** bequite-release-gate, bequite-testing-gate, bequite-devops-cloud
- **Next:** `/bq-changelog` then `/bq-release`

### `/bq-changelog`
- **Purpose:** categorize commits into Added / Changed / Fixed / Deprecated / Removed / Security (Keep a Changelog v1.1)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/logs/CHANGELOG.md`
- **Quality gate sets:** `CHANGELOG_READY ✅`
- **Skills activated:** bequite-release-gate
- **Next:** `/bq-release`

### `/bq-release`
- **Purpose:** version bump + final CHANGELOG; print git commands (never auto-pushes)
- **Required gates:** `VERIFY_PASS`, `CHANGELOG_READY`
- **Writes:** version files (package.json etc.), CHANGELOG entry
- **Quality gate sets:** `RELEASE_READY ✅` (after user runs git commands)
- **Skills activated:** bequite-release-gate
- **Next:** `/bq-memory snapshot`

---

## Phase 5 — Memory and Handoff

### `/bq-memory`
- **Purpose:** read / write BeQuite memory snapshots
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/state/MEMORY_SNAPSHOT_<date>.md` (when `snapshot` subcommand)
- **Quality gate sets:** `MEMORY_SNAPSHOT ✅` (on snapshot)
- **Next:** `/bq-handoff` or cycle complete

### `/bq-recover`
- **Purpose:** resume after a session break; finds last green checkpoint
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** updates state files; suggests next command
- **Next:** whatever recover output says

### `/bq-handoff`
- **Purpose:** generate HANDOFF.md (engineer + vibe sections + receiver checklist)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `HANDOFF.md` at repo root
- **Quality gate sets:** `HANDOFF_DONE ⚪ optional ✅`
- **Next:** end of cycle

---

## Phase orchestrators

### `/bq-p0`
- **Purpose:** walk Phase 0 in order (`/bq-init` → `/bq-mode` → `/bq-discover` → `/bq-doctor`)
- **Required gates:** none
- **Quality gate sets:** all P0 gates `✅`
- **Next:** `/bq-p1`

### `/bq-p1`
- **Purpose:** walk Phase 1 in order (`/bq-clarify` → `/bq-research` → `/bq-scope` → optional `/bq-multi-plan` → `/bq-plan`)
- **Required gates:** P0 complete
- **Quality gate sets:** all P1 gates `✅`
- **Next:** `/bq-p2`

### `/bq-p2`
- **Purpose:** walk Phase 2 (`/bq-assign` → `/bq-implement` loop, OR `/bq-feature`, OR `/bq-fix`)
- **Required gates:** per mode (P1 complete for New Project; `MODE_SELECTED` only for Feature/Fix)
- **Quality gate sets:** mode-specific gate `✅`
- **Next:** `/bq-p3`

### `/bq-p3`
- **Purpose:** walk Phase 3 (`/bq-test` → `/bq-audit` if applicable → `/bq-review` → optional `/bq-red-team`)
- **Required gates:** code exists OR Existing Audit mode
- **Quality gate sets:** all P3 gates `✅`
- **Next:** `/bq-p4`

### `/bq-p4`
- **Purpose:** walk Phase 4 (`/bq-verify` → `/bq-changelog` → `/bq-release` instructions)
- **Required gates:** P3 complete OR Release Readiness mode
- **Quality gate sets:** all P4 gates `✅`
- **Next:** `/bq-p5`

### `/bq-p5`
- **Purpose:** walk Phase 5 (`/bq-memory snapshot` → optional `/bq-handoff`)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Quality gate sets:** `MEMORY_SNAPSHOT ✅`
- **Next:** cycle complete

---

## Autonomous runner

### `/bq-auto`
- **Purpose:** walk ALL phases (P0 → P5) end-to-end, pause only at hard human gates
- **Required gates:** `BEQUITE_INITIALIZED`
- **Quality gate sets:** depends on completion
- **Hard human gates (12):** Mode selection, Clarify, Scope, Multi-plan decision, Plan approval, Release approval, Destructive ops, DB migrations, Server/VPS changes, Cost ceiling, Banned weasel words, 3 consecutive failures
- **Next:** `/bq-handoff` or cycle complete

---

## Skill activation matrix

| Command | Skills activated |
|---|---|
| `/bq-research` | researcher, security-reviewer, ux-ui-designer (if UI) |
| `/bq-scope` | product-strategist |
| `/bq-plan` | project-architect, backend-architect, database-architect, security-reviewer, devops-cloud, ux-ui-designer (if UI), frontend-quality, testing-gate |
| `/bq-multi-plan` | multi-model-planning, project-architect |
| `/bq-feature` | per 12-type router (frontend / backend / database / auth / automation / scraping / cloud / admin / dashboard / cli / integration / security) |
| `/bq-fix` | per 15-type router (frontend / backend / database / auth / build / test / deploy / perf / security / dep / config / network / memory / race / cross-browser) — always plus problem-solver |
| `/bq-audit` | security-reviewer, frontend-quality (if UI), testing-gate, devops-cloud |
| `/bq-review` | security-reviewer, testing-gate |
| `/bq-red-team` | security-reviewer, problem-solver |
| `/bq-test` | testing-gate |
| `/bq-verify` | release-gate, testing-gate, devops-cloud |
| `/bq-release` | release-gate |
| `/bq-changelog` | release-gate |

---

## Summary

34 commands, 14 skills, 6 modes, 6 phases, 23 gates, 12 hard human gates.

**Discipline + memory + verified evidence > velocity without a plan.**
