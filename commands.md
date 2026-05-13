# BeQuite — Commands reference

> Complete command index, organized by workflow phase. Each entry has a one-line purpose, when to use, required gates, inputs, key reads/writes, and example.
>
> For full procedural detail per command, click through to the matching file at `.claude/commands/<name>.md`.

**Version:** v3.0.0-alpha.8 · 42 slash commands · 18 specialist skills · 6 workflow phases · 23 workflow gates · 17 hard human gates

---

## Table of contents

- [Root](#root)
- [Phase 0 — Setup and Discovery](#phase-0--setup-and-discovery)
- [Phase 1 — Product Framing and Research](#phase-1--product-framing-and-research)
- [Phase 2 — Planning and Build](#phase-2--planning-and-build)
- [Phase 3 — Quality and Review](#phase-3--quality-and-review)
- [Phase 4 — Release](#phase-4--release)
- [Phase 5 — Memory and Handoff](#phase-5--memory-and-handoff)
- [Phase orchestrators](#phase-orchestrators)
- [Autonomous mode](#autonomous-mode)
- [UI / UX](#ui--ux)
- [Quick orientation](#quick-orientation)
- [How to read this file](#how-to-read-this-file)

---

## How to read this file

Each command entry:

| Field | Meaning |
|---|---|
| **Phase** | Which of the 6 workflow phases this command serves (or "Any") |
| **Purpose** | One-line summary |
| **When to use** | The trigger conditions |
| **Required gates** | What must be `✅` in `WORKFLOW_GATES.md` for this command to run |
| **Inputs** | Arguments accepted (in quotes or via `$ARGUMENTS`) |
| **Reads** | Files this command depends on |
| **Writes** | Files this command creates or updates |
| **Skills activated** | Which `.claude/skills/bequite-*` skills are loaded |
| **Quality gate** | What this command marks `✅` on success |
| **Failure** | How it handles failures |
| **Next** | Recommended next command |
| **Example** | A real call |
| **Full spec** | Link to `.claude/commands/<name>.md` for the full procedure |

**Workflow order:** read this file top-to-bottom for the natural flow of a project. Commands later in the file generally require gates from earlier commands.

---

## Root

### `/bequite`

The gate-aware project menu. Read-only.

- **Phase:** Any
- **Purpose:** Show current state, current mode, current phase, gate status, last command, blockers, and recommended next 3 commands.
- **When to use:** orientation; before any other command; after a break.
- **Required gates:** none
- **Inputs:** none
- **Reads:** `.bequite/state/*`, `.bequite/logs/AGENT_LOG.md`
- **Writes:** nothing
- **Quality gate:** none (read-only)
- **Failure:** if `.bequite/` doesn't exist, recommends `/bq-init`
- **Next:** the first item in "Recommended next 3"
- **Example:** `/bequite`
- **Full spec:** [`.claude/commands/bequite.md`](.claude/commands/bequite.md)

### `/bq-help`

Full command reference (this file's source — read by Claude Code on demand).

- **Phase:** Any
- **Purpose:** print all 37 commands grouped by phase
- **Inputs:** none
- **Next:** any command from the list
- **Full spec:** [`.claude/commands/bq-help.md`](.claude/commands/bq-help.md)

### `/bq-explain "<target>"` (NEW in alpha.7)

Plain-English explainer for files / functions / decisions / concepts / artifacts.

- **Phase:** Any (read-only)
- **Purpose:** Take a piece of code or a decision and explain it in 4 sections — What it is / What it does / Why it matters / Things to be careful of.
- **When to use:** AI-generated code you don't understand; vibe-handoff prep; inherited project; understanding `/bq-auto` output.
- **When NOT to use:** writing new code (use `/bq-feature`); fixing bugs (use `/bq-fix`).
- **Required gates:** `BEQUITE_INITIALIZED`
- **Inputs:** file path, function name, concept, decision, or BeQuite artifact name
- **Writes:** nothing by default (chat only); optional `.bequite/handoff/explain-<slug>.md`
- **Examples:**
  ```
  /bq-explain "lib/auth.ts"
  /bq-explain "the PricingCards component"
  /bq-explain "ADR-002"
  /bq-explain "what /bq-auto did last run"
  ```
- **Full spec:** [`.claude/commands/bq-explain.md`](.claude/commands/bq-explain.md)

### `/bq-now` (NEW in alpha.5)

One-line orientation. Faster than `/bequite`.

- **Phase:** Any
- **Purpose:** Single-line current state + suggested next command. No menu.
- **When to use:** daily-driver checks; mid-cycle returns; inside loops.
- **When NOT to use:** first-time setup (use `/bequite`)
- **Required gates:** none
- **Inputs:** none
- **Reads:** `.bequite/state/{CURRENT_PHASE,CURRENT_MODE,LAST_RUN,WORKFLOW_GATES,OPEN_QUESTIONS}.md`
- **Writes:** nothing
- **Example output:**
  ```
  P2 build · mode: Add Feature · last: /bq-implement T-2.3 ✓ · next: /bq-test
  ```
- **Full spec:** [`.claude/commands/bq-now.md`](.claude/commands/bq-now.md)

---

## Phase 0 — Setup and Discovery

Goal: learn what's there. No decisions about what to build yet.

### `/bq-init`

Initialize the `.bequite/` tree.

- **Phase:** P0
- **Purpose:** create memory + state file skeletons; append BeQuite section to CLAUDE.md.
- **When to use:** once per project, first time BeQuite is run.
- **Required gates:** none
- **Inputs:** optional `new` flag for empty folders
- **Writes:** `.bequite/state/*` baseline files, CLAUDE.md addition
- **Quality gate:** sets `BEQUITE_INITIALIZED ✅`
- **Next:** `/bq-mode`
- **Example:** `/bq-init`
- **Full spec:** [`.claude/commands/bq-init.md`](.claude/commands/bq-init.md)

### `/bq-mode`

Select / show workflow mode.

- **Phase:** P0
- **Purpose:** pick one of 6 modes — New Project / Existing Audit / Add Feature / Fix Problem / Research Only / Release Readiness.
- **When to use:** after `/bq-init`, before any P1+ command.
- **Required gates:** `BEQUITE_INITIALIZED`
- **Inputs:** mode name (optional)
- **Writes:** `.bequite/state/CURRENT_MODE.md`
- **Quality gate:** sets `MODE_SELECTED ✅`
- **Next:** mode-specific (see below)
- **Example:** `/bq-mode add-feature`
- **Full spec:** [`.claude/commands/bq-mode.md`](.claude/commands/bq-mode.md)

### `/bq-new`

Begin a New Project workflow (empty folder).

- **Phase:** P0
- **Purpose:** mode entry for fresh-from-scratch projects
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `CURRENT_MODE.md` → New Project; pre-queues foundational questions
- **Next:** `/bq-p0` or `/bq-clarify`
- **Example:** `/bq-new`
- **Full spec:** [`.claude/commands/bq-new.md`](.claude/commands/bq-new.md)

### `/bq-existing`

Begin an Existing Project Audit workflow.

- **Phase:** P0
- **Purpose:** mode entry for auditing an existing codebase
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `CURRENT_MODE.md` → Existing Audit
- **Next:** `/bq-discover` → `/bq-doctor` → `/bq-audit`
- **Example:** `/bq-existing`
- **Full spec:** [`.claude/commands/bq-existing.md`](.claude/commands/bq-existing.md)

### `/bq-discover`

Inspect repo → `DISCOVERY_REPORT.md`.

- **Phase:** P0
- **Purpose:** detect stack, entry points, ports, tests, CI, docs, smells
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/audits/DISCOVERY_REPORT.md`
- **Quality gate:** sets `DISCOVERY_DONE ✅`
- **Next:** `/bq-doctor`
- **Example:** `/bq-discover`
- **Full spec:** [`.claude/commands/bq-discover.md`](.claude/commands/bq-discover.md)

### `/bq-doctor`

Environment health → `DOCTOR_REPORT.md`.

- **Phase:** P0
- **Purpose:** probe Node / Python / Docker / package managers / ports / env vars / CI
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/audits/DOCTOR_REPORT.md`
- **Quality gate:** sets `DOCTOR_DONE ✅`
- **Next:** `/bq-clarify` or `/bq-p1`
- **Example:** `/bq-doctor`
- **Full spec:** [`.claude/commands/bq-doctor.md`](.claude/commands/bq-doctor.md)

---

## Phase 1 — Product Framing and Research

Goal: decide what to build. No code yet.

### `/bq-clarify`

3-5 high-value clarifying questions.

- **Phase:** P1
- **Purpose:** surface unstated assumptions about scope, scale, users, constraints
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`
- **Writes:** `.bequite/state/OPEN_QUESTIONS.md` (answers)
- **Quality gate:** sets `CLARIFY_DONE ✅`
- **Next:** `/bq-research`
- **Example:** `/bq-clarify`
- **Full spec:** [`.claude/commands/bq-clarify.md`](.claude/commands/bq-clarify.md)

### `/bq-research`

11-dimension verified evidence — stack / product / competitors / failures / success / user journey / UX/UI / security / scalability / deployment / differentiation.

- **Phase:** P1
- **Purpose:** replace memory-based assumptions with live WebFetch evidence
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `CLARIFY_DONE` (recommended)
- **Writes:** `.bequite/audits/RESEARCH_REPORT.md`, `DECISIONS.md` (appended), resolves items in `OPEN_QUESTIONS.md`
- **Quality gate:** sets `RESEARCH_DONE ✅`
- **Skills activated:** `bequite-researcher`, `bequite-security-reviewer`, `bequite-ux-ui-designer` (if UI)
- **Next:** `/bq-scope`
- **Example:** `/bq-research`
- **Full spec:** [`.claude/commands/bq-research.md`](.claude/commands/bq-research.md)

### `/bq-scope`

Lock IN / OUT / NON-GOALS.

- **Phase:** P1
- **Purpose:** prevent scope creep before the plan; force MVP commitment
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `RESEARCH_DONE` (recommended)
- **Writes:** `.bequite/plans/SCOPE.md`
- **Quality gate:** sets `SCOPE_LOCKED ✅`
- **Skills activated:** `bequite-product-strategist`
- **Next:** `/bq-plan` or `/bq-multi-plan`
- **Example:** `/bq-scope`
- **Full spec:** [`.claude/commands/bq-scope.md`](.claude/commands/bq-scope.md)

### `/bq-plan`

Write `IMPLEMENTATION_PLAN.md` (15 sections).

- **Phase:** P1
- **Purpose:** vision, architecture, stack, file plan, phase plan, task plan, test plan, risks, security, devops, acceptance, rollback, open questions
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `SCOPE_LOCKED` (strongly recommended)
- **Writes:** `.bequite/plans/IMPLEMENTATION_PLAN.md`
- **Quality gate:** sets `PLAN_APPROVED ✅` (after user confirms)
- **Skills activated:** project-architect + backend-architect + database-architect + security-reviewer + devops-cloud + ux-ui-designer (if UI) + frontend-quality + testing-gate
- **Next:** `/bq-assign` or `/bq-multi-plan`
- **Example:** `/bq-plan`
- **Full spec:** [`.claude/commands/bq-plan.md`](.claude/commands/bq-plan.md)

### `/bq-spec "<feature>"` (NEW in alpha.7)

One-page Spec Kit-compatible spec.

- **Phase:** P1 / P2 (framing-shaped or feature-shaped)
- **Purpose:** write a focused one-page spec at `specs/<slug>/spec.md` with What / Why / Who / Acceptance / Out-of-scope / Constraints / Open questions / Success metric. Spec Kit-compatible path so other tools can pick it up.
- **When to use:** documenting a feature for stakeholders before engineering; portable spec across BeQuite + Spec Kit; bridging team conversation to technical plan.
- **When NOT to use:** full project planning (use `/bq-plan`); Add Feature mini-cycle (use `/bq-feature`); quick fix (use `/bq-fix`).
- **Required gates:** `BEQUITE_INITIALIZED`; `MODE_SELECTED` recommended
- **Inputs:** feature or product idea in quotes
- **Writes:** `specs/<slug>/spec.md`, `.bequite/plans/spec-<slug>.md`, `DECISIONS.md`, `OPEN_QUESTIONS.md`
- **Skills activated:** `bequite-product-strategist` (JTBD framework)
- **Examples:**
  ```
  /bq-spec "Add CSV export to bookings page"
  /bq-spec "Patient intake form for the clinic SaaS"
  /bq-spec "Lead capture landing page"
  ```
- **Full spec:** [`.claude/commands/bq-spec.md`](.claude/commands/bq-spec.md)

### `/bq-multi-plan`

Unbiased multi-model planning via manual paste.

- **Phase:** P1
- **Purpose:** Claude + ChatGPT (or Gemini) propose plans independently; agent merges
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `CLARIFY_DONE`, `RESEARCH_DONE`, `SCOPE_LOCKED`
- **Writes:** `.bequite/prompts/generated_prompts/*`, `.bequite/prompts/model_outputs/*`, `MULTI_MODEL_COMPARISON.md`, merged `IMPLEMENTATION_PLAN.md`
- **Quality gate:** sets `MULTI_PLAN_DONE ✅` (optional)
- **Skills activated:** `bequite-multi-model-planning`
- **Next:** `/bq-assign`
- **Example:** `/bq-multi-plan`
- **Full spec:** [`.claude/commands/bq-multi-plan.md`](.claude/commands/bq-multi-plan.md)

---

## Phase 2 — Planning and Build

Goal: build it.

### `/bq-assign`

Break `IMPLEMENTATION_PLAN.md` → atomic `TASK_LIST.md`.

- **Phase:** P2
- **Purpose:** ≤5min tasks, dependency-ordered, one acceptance criterion each
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `PLAN_APPROVED`
- **Writes:** `.bequite/tasks/TASK_LIST.md`
- **Quality gate:** sets `ASSIGN_DONE ✅`
- **Next:** `/bq-implement`
- **Example:** `/bq-assign`
- **Full spec:** [`.claude/commands/bq-assign.md`](.claude/commands/bq-assign.md)

### `/bq-implement`

Implement ONE approved task at a time.

- **Phase:** P2
- **Purpose:** pick next `[ ] pending` task; read files; minimal change; run test; mark `[x]`
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `PLAN_APPROVED`, `ASSIGN_DONE`
- **Writes:** source files, `TASK_LIST.md` updated, `CHANGELOG [Unreleased]`
- **Quality gate:** sets `IMPLEMENT_DONE ✅` when task list empty
- **Skills activated:** depends on task type
- **Next:** `/bq-implement` (next task) or `/bq-test`
- **Example:** `/bq-implement T-2.3`
- **Full spec:** [`.claude/commands/bq-implement.md`](.claude/commands/bq-implement.md)

### `/bq-feature "<title>"`

Add Feature workflow with 12-type router.

- **Phase:** P2
- **Purpose:** mini-cycle for one feature; classify into 12 types; activate matching skills
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`
- **Inputs:** feature title in quotes
- **Writes:** `.bequite/plans/feature-<slug>.md`, source files, tests
- **Quality gate:** sets `FEATURE_DONE ✅`
- **Skills activated:** per 12-type router (frontend / backend / database / auth / automation / scraping / cloud / admin / dashboard / cli / integration / security)
- **Next:** `/bq-review`
- **Example:** `/bq-feature "CSV export on the bookings page"`
- **Full spec:** [`.claude/commands/bq-feature.md`](.claude/commands/bq-feature.md)

### `/bq-fix "<symptom>"`

Fix workflow with 15-type router; reproduce-first.

- **Phase:** P2
- **Purpose:** reproduce → root cause → smallest patch → regression test → verify
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`
- **Inputs:** symptom description in quotes
- **Writes:** source fix, regression test, `ERROR_LOG.md`, `FIX_<slug>.md`, CHANGELOG if user-visible, MISTAKE_MEMORY if patterned
- **Quality gate:** sets `FIX_DONE ✅`
- **Skills activated:** per 15-type router (frontend / backend / database / auth / build / test / deploy / perf / security / dep / config / network / memory / race / cross-browser) + always `bequite-problem-solver`
- **Next:** `/bq-test`
- **Example:** `/bq-fix "Login button doesn't respond on Safari"`
- **Full spec:** [`.claude/commands/bq-fix.md`](.claude/commands/bq-fix.md)

---

## Phase 3 — Quality and Review

Goal: confirm it works.

### `/bq-test`

Run + write tests.

- **Phase:** P3
- **Purpose:** detect framework (vitest / jest / pytest / cargo test); run; identify coverage gaps; offer to write missing tests
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** test files
- **Quality gate:** sets `TEST_DONE ✅` when all green
- **Skills activated:** `bequite-testing-gate`
- **Next:** `/bq-review` or `/bq-implement` (continue loop)
- **Example:** `/bq-test`
- **Full spec:** [`.claude/commands/bq-test.md`](.claude/commands/bq-test.md)

### `/bq-audit`

10-area full project audit.

- **Phase:** P3
- **Purpose:** Install / Run / Frontend / API / CLI / Tests / Docs / UX / Security / Release — severity-tagged findings
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/audits/FULL_PROJECT_AUDIT.md`, MISTAKE_MEMORY entries for patterns
- **Quality gate:** sets `AUDIT_DONE ✅` (optional unless Release Readiness mode)
- **Skills activated:** `bequite-security-reviewer`, `bequite-frontend-quality` (UI), `bequite-testing-gate`, `bequite-devops-cloud`
- **Next:** `/bq-fix` per findings, or `/bq-verify`
- **Example:** `/bq-audit`
- **Full spec:** [`.claude/commands/bq-audit.md`](.claude/commands/bq-audit.md)

### `/bq-review`

Per-file review of uncommitted diff + recent commits.

- **Phase:** P3
- **Purpose:** correctness / tests / security / style / naming / DRY / performance / reversibility
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/audits/REVIEW-<timestamp>.md`, MISTAKE_MEMORY for repeat patterns
- **Quality gate:** sets `REVIEW_DONE ✅`
- **Skills activated:** `bequite-security-reviewer`, `bequite-testing-gate`
- **Verdict:** Approved / Approved-with-comments / Blocked
- **Next:** `/bq-verify` or `/bq-fix` per verdict
- **Example:** `/bq-review`
- **Full spec:** [`.claude/commands/bq-review.md`](.claude/commands/bq-review.md)

### `/bq-red-team`

Adversarial Skeptic review — 9 attack angles (security, architecture, testing, deployment, scalability, UX, token-waste, hidden assumptions, tool-choice).

- **Phase:** P3
- **Purpose:** find what's actually broken before ship
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/audits/RED_TEAM-<timestamp>.md`, MISTAKE_MEMORY for BLOCKER/HIGH
- **Quality gate:** sets `RED_TEAM_DONE ⚪ optional ✅`
- **Skills activated:** `bequite-security-reviewer`, `bequite-problem-solver`
- **Next:** `/bq-fix` for findings
- **Example:** `/bq-red-team`
- **Full spec:** [`.claude/commands/bq-red-team.md`](.claude/commands/bq-red-team.md)

---

## Phase 4 — Release

Goal: ship.

### `/bq-verify`

Full local gate matrix — install + lint + typecheck + unit + integration + build + smoke + e2e + secret-scan + lockfile sanity.

- **Phase:** P4
- **Purpose:** prove ship-readiness with a single command
- **Required gates:** `TEST_DONE`, `REVIEW_DONE`
- **Writes:** `.bequite/audits/VERIFY_REPORT.md`, MISTAKE_MEMORY if patterned failure
- **Quality gate:** sets `VERIFY_PASS ✅`
- **Skills activated:** `bequite-release-gate`, `bequite-testing-gate`, `bequite-devops-cloud`
- **Verdict:** PASS / FAIL (no "probably" allowed)
- **Next:** `/bq-changelog` then `/bq-release`
- **Example:** `/bq-verify`
- **Full spec:** [`.claude/commands/bq-verify.md`](.claude/commands/bq-verify.md)

### `/bq-changelog`

Categorize commits per Keep a Changelog v1.1 — Added / Changed / Fixed / Deprecated / Removed / Security.

- **Phase:** P4
- **Purpose:** sharpen entries; no internal-only noise
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/logs/CHANGELOG.md`
- **Quality gate:** sets `CHANGELOG_READY ✅`
- **Skills activated:** `bequite-release-gate`
- **Next:** `/bq-release`
- **Example:** `/bq-changelog`
- **Full spec:** [`.claude/commands/bq-changelog.md`](.claude/commands/bq-changelog.md)

### `/bq-release`

Final release prep. Bumps version. Prints `git push` + `git tag` commands — **you run them**.

- **Phase:** P4
- **Purpose:** never auto-pushes; never auto-deploys
- **Required gates:** `VERIFY_PASS`, `CHANGELOG_READY`
- **Writes:** version files, CHANGELOG entry move (`[Unreleased]` → `[vX.Y.Z]`)
- **Quality gate:** sets `RELEASE_READY ✅` after user runs git commands
- **Skills activated:** `bequite-release-gate`
- **Hard gate:** user runs `git push` / `git tag` themselves (17th hard human gate)
- **Next:** `/bq-memory snapshot`
- **Example:** `/bq-release`
- **Full spec:** [`.claude/commands/bq-release.md`](.claude/commands/bq-release.md)

---

## Phase 5 — Memory and Handoff

Goal: continue or hand off.

### `/bq-memory`

Read / write memory snapshots.

- **Phase:** P5
- **Purpose:** checkpoint state before risky work; inspect what BeQuite remembers
- **Required gates:** `BEQUITE_INITIALIZED`
- **Subcommands:** `show`, `snapshot`, `refresh`
- **Writes:** `.bequite/state/MEMORY_SNAPSHOT_<date>.md` (on snapshot)
- **Quality gate:** sets `MEMORY_SNAPSHOT ✅` (on snapshot)
- **Next:** `/bq-handoff` or cycle complete
- **Example:** `/bq-memory snapshot`
- **Full spec:** [`.claude/commands/bq-memory.md`](.claude/commands/bq-memory.md)

### `/bq-recover`

Resume after a session break. Finds the last green checkpoint.

- **Phase:** P5
- **Purpose:** single most useful command after a break — reads all `.bequite/`, derives where you are, says what's safe to do next
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** updates `LAST_RUN.md` with recovery context
- **Next:** whatever recover output says
- **Example:** `/bq-recover`
- **Full spec:** [`.claude/commands/bq-recover.md`](.claude/commands/bq-recover.md)

### `/bq-handoff`

Generate `HANDOFF.md` for another engineer.

- **Phase:** P5
- **Purpose:** two-section handoff — engineer (technical) + vibe (non-engineer); receiver checklist
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `HANDOFF.md` at repo root
- **Quality gate:** sets `HANDOFF_DONE ⚪ optional ✅`
- **Next:** end of cycle
- **Example:** `/bq-handoff`
- **Full spec:** [`.claude/commands/bq-handoff.md`](.claude/commands/bq-handoff.md)

---

## Phase orchestrators

Walk one phase in order.

### `/bq-p0` — `/bq-p5`

- **Purpose:** run all commands in a single phase end-to-end
- **Required gates:** per phase
- **Quality gate:** sets all phase gates `✅`
- **Next:** `/bq-p<next>`
- **Example:** `/bq-p1`
- **Full spec:** `.claude/commands/bq-p<N>.md`

| Command | Walks |
|---|---|
| `/bq-p0` | `/bq-init` → `/bq-mode` → `/bq-discover` → `/bq-doctor` |
| `/bq-p1` | `/bq-clarify` → `/bq-research` → `/bq-scope` → optional `/bq-multi-plan` → `/bq-plan` |
| `/bq-p2` | `/bq-assign` → `/bq-implement` loop OR `/bq-feature` OR `/bq-fix` (per mode) |
| `/bq-p3` | `/bq-test` → `/bq-audit` (if applicable) → `/bq-review` → optional `/bq-red-team` |
| `/bq-p4` | `/bq-verify` → `/bq-changelog` → `/bq-release` (prints commands) |
| `/bq-p5` | `/bq-memory snapshot` → optional `/bq-handoff` |

---

## Autonomous mode

### `/bq-auto [intent] [options] "<task>"`

Scoped autonomous workflow runner.

- **Phase:** Any
- **Purpose:** drive a task end-to-end; pause only at 17 hard human gates
- **Intent types (17):** `new | existing | feature | fix | uiux | frontend | backend | database | security | testing | devops | scraping | automation | deploy | live-edit | variants | release`
- **Options:** `variants=N`, `--mode fast|deep|token-saver`, `--max-cost-usd <n>`, `--max-wall-clock-hours <n>`, `--manual-approval`
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** every artifact each underlying command writes; auto-state machine; MISTAKE_MEMORY for patterns
- **Hard human gates (17):**
  1. Destructive file deletion · 2. DB migration on shared/prod · 3. Production server change · 4. VPS / Nginx / SSL · 5. Paid service signup · 6. Secret rotation · 7. Auth/security model · 8. Architecture change · 9. Deleting old impl · 10. Scope contradiction · 11. Manual-approval flag · 12. Cost ceiling · 13. Wall-clock ceiling · 14. Banned weasel words · 15. 3 consecutive failures · 16. UI variant winner selection · 17. Release `git push` / `git tag`
- **Examples:**
  ```
  /bq-auto new "Build a SaaS dashboard for clinic bookings"
  /bq-auto fix "Fix hidden text on /dashboard"
  /bq-auto uiux variants=5 "Five dashboard design directions"
  /bq-auto security "Audit + patch OWASP top 10"
  /bq-auto deploy "VPS deployment plan + execute"
  /bq-auto fix "..." --mode fast
  /bq-auto new "..." --mode deep
  ```
- **Strategy doc:** [`docs/architecture/AUTO_MODE_STRATEGY.md`](docs/architecture/AUTO_MODE_STRATEGY.md)
- **Full spec:** [`.claude/commands/bq-auto.md`](.claude/commands/bq-auto.md)

---

## UI / UX

### `/bq-uiux-variants [count] "<scope>"`

Generate 1-10 isolated UI design directions.

- **Phase:** Any (lives in P2 / P3 typically)
- **Purpose:** parallel design exploration; original UI stays intact; user picks winner; agent merges
- **Required gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`; frontend exists
- **Inputs:** count (1-10; default 3); scope description
- **Writes:** N isolated variants (`app/uiux/v1/…` or `src/uiux-variants/Variant01/…`), `.bequite/uiux/UIUX_VARIANTS_REPORT.md`, screenshots, `selected-variant.md` after pick
- **Hard gate:** user picks winner (16th hard human gate)
- **Skills activated:** `bequite-ux-ui-designer`, `bequite-frontend-quality`
- **Examples:**
  ```
  /bq-uiux-variants 3
  /bq-uiux-variants 5 "five dashboard concepts"
  /bq-uiux-variants 10 "ten landing page directions"
  ```
- **Strategy doc:** [`docs/architecture/UIUX_VARIANTS_STRATEGY.md`](docs/architecture/UIUX_VARIANTS_STRATEGY.md)
- **Full spec:** [`.claude/commands/bq-uiux-variants.md`](.claude/commands/bq-uiux-variants.md)

### `/bq-live-edit "<task>"`

Lightweight section-by-section frontend live edit.

- **Phase:** Any
- **Purpose:** map visible sections to source files; apply smallest possible edit; verify via build + (optional) screenshots
- **Required gates:** `BEQUITE_INITIALIZED`; frontend exists
- **Inputs:** task description in quotes
- **Writes:** source edits, `.bequite/uiux/SECTION_MAP.md`, `.bequite/uiux/LIVE_EDIT_LOG.md`, before/after screenshots (if browser automation available)
- **Browser inspection tiers:** Playwright MCP → project-local Playwright → code-only (always works; never auto-installs Playwright)
- **Skills activated:** `bequite-live-edit`, `bequite-frontend-quality`
- **Examples:**
  ```
  /bq-live-edit "Make pricing cards less crowded"
  /bq-live-edit "Improve empty state on /dashboard"
  /bq-live-edit "Fix mobile layout overflow on hero"
  ```
- **Strategy doc:** [`docs/architecture/LIVE_EDIT_STRATEGY.md`](docs/architecture/LIVE_EDIT_STRATEGY.md)
- **Full spec:** [`.claude/commands/bq-live-edit.md`](.claude/commands/bq-live-edit.md)

---

## Opportunity and Workflows (NEW in alpha.8)

### `/bq-suggest "<situation>"`

BeQuite workflow advisor — recommends the best commands, skills, gates, and mode for your goal. Read-only.

- **Phase:** Any
- **Purpose:** lost in the command catalog? describe your situation → get a structured recommendation (workflow / skills / mode / one next command)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Skills activated:** `bequite-workflow-advisor`
- **Examples:**
  ```
  /bq-suggest "I want to improve UI/UX and security"
  /bq-suggest "I have a broken frontend and API"
  /bq-suggest "I want to build a scraper and deploy it on VPS"
  /bq-suggest "I have a project idea and want to know where to start"
  /bq-suggest "I need UX + backend + testing"
  ```
- **Full spec:** [`.claude/commands/bq-suggest.md`](.claude/commands/bq-suggest.md)

### `/bq-job-finder`

Find real work opportunities — full-time / part-time / remote / freelance / tasks / AI gigs — based on country + skills + languages + AI tools + payment methods.

- **Phase:** Any (lifestyle / career command)
- **Modes:** default (country-focused) | `worldwide_hidden=true` (overlooked multilingual platforms)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/jobs/` 5 files
- **Skills activated:** `bequite-job-finder`
- **Safety:** strict — no scams / fake reviews / VPN misrepresentation / upfront-fee / identity misuse / CAPTCHA farms
- **Examples:**
  ```
  /bq-job-finder
  /bq-job-finder "Remote AI-assisted gigs"
  /bq-job-finder worldwide_hidden=true
  /bq-job-finder worldwide_hidden=true "Find overlooked remote tasks"
  ```
- **Full spec:** [`.claude/commands/bq-job-finder.md`](.claude/commands/bq-job-finder.md)

### `/bq-make-money`

Find legitimate earning opportunities — 10 tracks (highest payout / easiest start / fastest first dollar / long-term / AI-assisted / no-calls / remote / local / beginner / skilled).

- **Phase:** Any (lifestyle / earning command)
- **Modes:** default | `worldwide_hidden=true` (Hidden Gems section)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Writes:** `.bequite/money/` 5 files + 7-day action plan
- **Skills activated:** `bequite-make-money`
- **Safety:** strict — no fraud / fake accounts / platform abuse / spam / VPN / upfront-fee / unrealistic claims
- **Repeat-search behavior:** compares with previous run; marks 🆕 / ✅ / ❌ / ⚠ / ⬆ / 🔍
- **Examples:**
  ```
  /bq-make-money "Egypt, AI image editing, 3 hours daily, want remote tasks"
  /bq-make-money "Find easy AI-assisted tasks with real payout"
  /bq-make-money worldwide_hidden=true "Find hidden legitimate earning opportunities worldwide"
  /bq-make-money track=highest-payout country=Egypt skills='AI tools, writing, image editing'
  /bq-make-money track=easiest-start worldwide_hidden=true
  ```
- **Full spec:** [`.claude/commands/bq-make-money.md`](.claude/commands/bq-make-money.md)

### 🌍 Worldwide Hidden Opportunity Search

Both `/bq-job-finder` and `/bq-make-money` support `worldwide_hidden=true` — searches beyond user's country + famous English platforms. Finds overlooked legitimate opportunities in:
- Non-English markets (Portuguese, Spanish, German, French, Italian, Turkish, Polish, Romanian, Indonesian, Hindi, Arabic + English)
- Country-specific microtask platforms (Yandex Toloka, Wuzzuf, Brighter Monday, Get on Board, Wantedly, etc.)
- AI training task platforms (Outlier, Mercor, Mindrift, Surge, Data Annotation)
- Research panels (User Interviews, Respondent, dscout, Prolific)
- Testing platforms (UserTesting, UserBrain, Userlytics)
- App-based earning programs (Premise, Field Agent, Streetbees)
- Small companies hiring globally
- Niche platforms by skill / region

Per-opportunity trust check: legitimacy / country eligibility / payout method / VPN policy / ID verification / upfront-fee red flags / scam reports / realistic payout / time to first payout / why hidden.

---

## Quick orientation

Three commands for daily-driver use:

| Command | Output | When to use |
|---|---|---|
| `/bq-now` | One line — phase + last + next | quick status check |
| `/bequite` | Full menu — gate status + recommended 3 | orientation, first time each session |
| `/bq-help` | Full command reference (in chat) | when learning the system |
| `/bq-explain "<target>"` | Plain-English explanation in 4 sections | understanding inherited code / decisions / artifacts |

---

## Anti-patterns (what NOT to do)

- ❌ Running `/bq-implement` before `/bq-plan` — refused by gate system
- ❌ Manually editing `WORKFLOW_GATES.md` to mark gates ✅ — gates only set on actual command success
- ❌ Skipping `/bq-verify` for "trivial" changes — Iron Law X says ship in operationally complete state
- ❌ Using `--mode fast` to skip safety gates — modes adjust depth, NOT safety; all 17 hard human gates apply regardless
- ❌ Auto-installing dependencies — tool neutrality (ADR-003) requires a decision section first
- ❌ Pushing to `git tag` from BeQuite — release gates are user-run (hard human gate #17)
- ❌ Asking "should I continue?" between every step in `/bq-auto` — auto-mode continues by default

---

## What this file is

`commands.md` is a navigable INDEX. Each entry summarizes the command. For the full procedure (steps, edge cases, output formats), click through to the matching `.claude/commands/<name>.md`.

**This file is read-friendly.** The `.claude/commands/*.md` files are agent-friendly (more procedural, more detailed). Both stay in sync.

---

## Related docs

- [`README.md`](README.md) — project overview + install
- [`CLAUDE.md`](CLAUDE.md) — Claude-Code operating instructions
- [`docs/architecture/`](docs/architecture/) — strategy docs per workflow + auto mode + variants + live edit + workflow gates + research depth + feature/fix workflows + devops safety
- [`docs/decisions/`](docs/decisions/) — 4 ADRs
- [`docs/specs/COMMAND_CATALOG.md`](docs/specs/COMMAND_CATALOG.md) — terse machine-readable catalog (this file is the human-readable one)
- [`docs/specs/MVP_LIGHTWEIGHT_SCOPE.md`](docs/specs/MVP_LIGHTWEIGHT_SCOPE.md) — MVP boundaries
- [`docs/runbooks/USING_BEQUITE_COMMANDS.md`](docs/runbooks/USING_BEQUITE_COMMANDS.md) — practical walkthroughs with output examples
- [`.bequite/principles/TOOL_NEUTRALITY.md`](.bequite/principles/TOOL_NEUTRALITY.md) — tool-choice discipline
- [`.bequite/plans/FEATURE_EXPANSION_ROADMAP.md`](.bequite/plans/FEATURE_EXPANSION_ROADMAP.md) — v2 feature families
