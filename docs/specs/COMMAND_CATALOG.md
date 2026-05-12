# BeQuite Command Catalog (v3.0.0-alpha.4)

**Status:** authored 2026-05-11; expanded 2026-05-12 (alpha.4: scoped auto + variants + live edit)
**Total commands:** 36 (1 root menu + 35 `/bq-*`)
**Total skills:** 15 (7 baseline + 7 specialist + 1 live-edit)

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

### `/bq-uiux-variants [count] "task"` (NEW in alpha.4)
- **Purpose:** generate 1-10 isolated UI design directions; user picks winner; agent merges
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`; frontend exists
- **Writes:** N isolated variants (`app/uiux/v1/…` or `src/uiux-variants/Variant01/…`), `.bequite/uiux/UIUX_VARIANTS_REPORT.md`, `.bequite/uiux/SECTION_MAP.md`, screenshots, `selected-variant.md` after pick
- **Hard gate:** user picks winner (step 6)
- **Skills activated:** `bequite-ux-ui-designer`, `bequite-frontend-quality`
- **Strategy doc:** `docs/architecture/UIUX_VARIANTS_STRATEGY.md`
- **Next:** `/bq-live-edit` for refinement

### `/bq-live-edit "task"` (NEW in alpha.4)
- **Purpose:** section-by-section frontend edits via SECTION_MAP + targeted edits + (optional) browser inspection
- **Required gates:** `BEQUITE_INITIALIZED`; frontend exists
- **Writes:** source edits, `.bequite/uiux/SECTION_MAP.md`, `.bequite/uiux/LIVE_EDIT_LOG.md`, before/after screenshots if browser automation available
- **Skills activated:** `bequite-live-edit`, `bequite-frontend-quality`
- **Strategy doc:** `docs/architecture/LIVE_EDIT_STRATEGY.md`
- **Next:** another `/bq-live-edit` or `/bq-test`

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

### `/bq-auto [intent] [options] "task"` (UPDATED in alpha.4 — scoped + $ARGUMENTS)
- **Purpose:** scoped autonomous workflow runner; parses 17 intent types and runs only the relevant scope
- **Intents:** `new | existing | feature | fix | uiux | frontend | backend | database | security | testing | devops | scraping | automation | deploy | live-edit | variants | release`
- **Required gates:** `BEQUITE_INITIALIZED`
- **Behavior:** continues by default; does NOT pause for "approve the plan?" — only at hard human gates
- **Hard human gates (17):**
  1. Destructive file deletion
  2. DB migration against shared/prod DB
  3. Production server change
  4. VPS / Nginx / SSL change
  5. Paid service activation
  6. Secret / key handling
  7. Changing auth/security model
  8. Changing project architecture
  9. Deleting old implementation
  10. Scope contradiction
  11. User explicit manual-approval
  12. Cost ceiling
  13. Wall-clock ceiling
  14. Banned-weasel-word trip
  15. 3 consecutive failures
  16. UI variant winner selection (after `/bq-uiux-variants`)
  17. Release `git push` / `git tag`
- **Strategy doc:** `docs/architecture/AUTO_MODE_STRATEGY.md`
- **Skills activated:** all 15 (per intent)
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

36 commands, 15 skills, 6 modes, 6 phases, 23 gates, 17 hard human gates.

**Discipline + memory + verified evidence > velocity without a plan.**

**Scoped auto-mode means: continue by default until task is complete, tested, verified, and logged. Pause only at hard human gates.**
