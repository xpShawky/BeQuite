# BeQuite Command Catalog (v3.0.0-alpha.13)

**Status:** authored 2026-05-11; expanded 2026-05-12 across alpha.2–alpha.10; 4 operating modes added 2026-05-12 (alpha.12); Presentation Builder added 2026-05-13 (alpha.13)
**Total commands:** 44 (1 root menu + 43 `/bq-*`)
**Total skills:** 21 (7 baseline + 7 specialist + 1 live-edit + 3 opportunity + 1 updater + 1 delegate-planner + 1 presentation-builder)
**Operating modes (alpha.12):** 4 composable — Deep / Fast / Token Saver (alias `lean`) / Delegate
**Creative + Content Workflows (alpha.13):** `/bq-presentation`
**Human-readable reference:** [`commands.md`](../../commands.md) at repo root

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

### `/bq-now` (NEW in alpha.5)
- **Purpose:** one-line orientation; faster than `/bequite`
- **Phase:** any
- **Required gates:** none
- **Reads:** `.bequite/state/{CURRENT_PHASE,CURRENT_MODE,LAST_RUN,WORKFLOW_GATES,OPEN_QUESTIONS}.md`
- **Writes:** nothing (read-only)
- **Output:** single line, e.g. `P2 build · mode: Add Feature · last: /bq-implement T-2.3 ✓ · next: /bq-test`
- **Next:** command in the `next:` field

### `/bq-spec "<feature>"` (NEW in alpha.7)
- **Purpose:** write a one-page Spec Kit-compatible spec at `specs/<slug>/spec.md`
- **Phase:** P1 / P2 (framing-shaped or feature-shaped)
- **Required gates:** `BEQUITE_INITIALIZED`; `MODE_SELECTED` (recommended)
- **Reads:** `PROJECT_STATE.md`, `SCOPE.md` (if exists), `IMPLEMENTATION_PLAN.md` (if exists), `RESEARCH_REPORT.md` (if exists)
- **Writes:** `specs/<slug>/spec.md`, `.bequite/plans/spec-<slug>.md`, `DECISIONS.md`, `OPEN_QUESTIONS.md`
- **Skills activated:** `bequite-product-strategist` (for JTBD discipline)
- **Output:** structured one-page spec with What / Why / Who / Acceptance / Out-of-scope / Constraints / Open questions / Success metric
- **Next:** `/bq-plan` (turn spec into full plan) or `/bq-feature` (mini-cycle if scope small)

### `/bq-explain "<target>"` (NEW in alpha.7)
- **Purpose:** explain a file / function / decision / concept / BeQuite artifact in plain English
- **Phase:** any (read-only)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Reads:** the target file(s) + 1-2 hops of related files
- **Writes:** nothing by default; optionally `.bequite/handoff/explain-<slug>.md` if user saves
- **Output:** 4-section structured explanation — What it is / What it does / Why it matters / Things to be careful of
- **Use cases:** onboarding, vibe-handoff prep, inherited code, understanding what `/bq-auto` did
- **Next:** another `/bq-explain` or `/bq-handoff` (bundles explanations)

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

## Opportunity and Workflows (alpha.8)

### `/bq-suggest "<situation>"`
- **Purpose:** workflow advisor; recommends best commands/skills/mode for your goal
- **Phase:** Any (read-only)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Reads:** `.bequite/state/*` (all)
- **Writes:** `LAST_RUN.md`, `AGENT_LOG.md`
- **Skills activated:** `bequite-workflow-advisor`
- **Output:** structured recommendation — workflow / skills / mode / required gates / one next command + why NOT each alternative

### `/bq-job-finder`
- **Purpose:** find real work opportunities (jobs, freelance, tasks, AI gigs)
- **Phase:** Any (lifestyle/career)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Modes:** default (country-focused) | `worldwide_hidden=true` (multilingual hidden opportunities)
- **Reads:** `.bequite/jobs/*` (if prior search exists)
- **Writes:** `.bequite/jobs/{JOB_PROFILE, JOB_SEARCH_LOG, OPPORTUNITIES, APPLICATION_TRACKER, PITCH_TEMPLATES}.md`
- **Skills activated:** `bequite-job-finder`
- **Safety:** strict — no scams / fake reviews / VPN misrepresentation / upfront-fee / identity misuse / CAPTCHA farms

### `/bq-make-money`
- **Purpose:** find legitimate earning opportunities; 10 tracks (highest-payout / easiest-start / fastest-first-dollar / long-term / AI-assisted / no-calls / remote / local / beginner / skilled)
- **Phase:** Any
- **Required gates:** `BEQUITE_INITIALIZED`
- **Modes:** default | `worldwide_hidden=true` (Hidden Gems section)
- **Reads:** `.bequite/money/*` (if prior search exists)
- **Writes:** `.bequite/money/{MONEY_PROFILE, MONEY_SEARCH_LOG, OPPORTUNITIES, TRUST_CHECKS, ACTION_PLAN}.md`
- **Skills activated:** `bequite-make-money`
- **Safety:** strict — no fraud / fake accounts / platform abuse / spam / VPN / upfront-fee / unrealistic claims
- **Output:** ranked by 10 categories + Hidden Gems section + 7-day action plan + trust checks

---

## Creative and Content Workflows (alpha.13)

### `/bq-presentation` (NEW in alpha.13)
- **Purpose:** premium PPTX or HTML presentation builder from topic / files / brand assets / research; world-class output
- **Phase:** Any (creative + content; orthogonal to P0–P5)
- **Required gates:** `BEQUITE_INITIALIZED`
- **Inputs:** natural language; options as `key=value` or `[bracketed list]` or positional (`format`, `variants`, `source`, `strict`, `creative`, `audience`, `style`, `duration`, `language`, `topic`, `brand`, `references`, `notes`, `motion`)
- **Reads:** core memory + source files (PDF / Word / folder / URLs) + brand assets if given + `.bequite/presentations/*` if prior run
- **Writes:** `.bequite/presentations/{PRESENTATION_BRIEF, CONTENT_OUTLINE, SLIDE_PLAN, DESIGN_BRIEF, MOTION_PLAN, SPEAKER_NOTES, REFERENCES, EXPORT_LOG}.md`; `PRESENTATION_VARIANTS_REPORT.md` when `variants>1`; `.bequite/presentations/{assets,outputs}/`
- **Skills activated:** `bequite-presentation-builder`, `bequite-ux-ui-designer`, `bequite-frontend-quality` (HTML quality), `bequite-researcher` (when sources require fetch)
- **Output formats:**
  - **PPTX** — institutional / lecture / offline / speaker notes / Office users; morph-like motion via stable object IDs across slides
  - **HTML** — cinematic / responsive / product demo; restrained CSS/JS motion (title glow, staged bullets, card focus, light sweep)
  - **Both** — same content plan, two renders
- **Strict vs creative:**
  - **Strict** — PDF / Word / scientific source preserved; no unsupported claims; every fact in `REFERENCES.md`
  - **Creative** — topic-only / keynote / marketing; may add hooks + structure; assumptions marked
- **Variants:** 1–10 different design directions (Academic Clean / Premium Cinematic / Corporate Keynote / Medical Conference / Minimal Lecture / Dark Futuristic / Light Editorial / Data-Dashboard / Student-Friendly / Brand-Led — candidates only)
- **Quality gate sets:** N/A (creative workflow — verification produces 14-item checklist result, not a phase gate)
- **Hard human gates relevant:** tool install (python-pptx / pptxgenjs / reveal.js / Slidev / Playwright etc. never auto-installed); external publishing (SlideShare / Google Slides / SharePoint); variant winner selection; brand-asset usage rights
- **Operating modes (composable):** `deep` / `fast` / `token-saver` (`lean`) / `delegate`
- **Verification (14 items):** one purpose per slide, readable text, not crowded, strong hook, clear story flow, correct refs, purposeful imagery, consistent brand, earned animations, non-distracting transitions, aligned speaker notes, suitable format, supported claims (strict), usable output
- **Tool neutrality:** all libraries are CANDIDATES; decision section required before install
- **Next:** user picks variant if `variants>1`; render output if implementation requested; `/bq-verify` if shipping artifact

---

## Maintenance (alpha.10)

### `/bq-update` (NEW in alpha.10)
- **Purpose:** safely update BeQuite (commands / skills / docs / templates) from GitHub or local source
- **Phase:** Maintenance (not part of P0-P5)
- **Required gates:** `BEQUITE_INITIALIZED`; git on PATH (for github source)
- **Modes:** `check` (preview only) / safe (default — backup + merge) / `force` / `source=local path=X` / `source=github repo=X branch=Y` or `tag=Y`
- **Reads:** `.bequite/state/BEQUITE_VERSION.md`, `UPDATE_SOURCE.md`
- **Writes:** `BEQUITE_VERSION.md`, `UPDATE_SOURCE.md`, `UPDATE_LOG.md`, `.bequite/backups/<timestamp>/`
- **Skills activated:** `bequite-updater`
- **Hard rules:** never overwrites project memory (PROJECT_STATE / DECISIONS / MISTAKE_MEMORY / jobs / money / research / etc.); always backs up before changing `.claude/commands/` or `.claude/skills/`; local edits surface as `.bequite-update.md` sibling files

## Deep intelligence flags (alpha.10) for `/bq-job-finder` and `/bq-make-money`

11 new flags can stack:

| Flag | Purpose |
|---|---|
| `worldwide_hidden=true` | Search beyond country / famous English platforms |
| `trending_now=true` | Last-30-days surge opportunities |
| `community_discovered=true` | Prioritize community-signal-sourced opportunities |
| `AI_assisted=true` | Surface paths where user's AI stack is a multiplier |
| `no_calls=true` | Async-only |
| `fast_first_payout=true` | Time-to-first-payout optimized |
| `highest_payout=true` | Top $/hour or $/task |
| `beginner_friendly=true` | No prior experience |
| `skilled_remote=true` | Premium skilled remote |
| `local_country=true` | Tied to country + language |
| `non_english_platforms=true` | Specifically search non-English markets |

New memory files (alpha.10):
- `.bequite/jobs/{HIDDEN_GEMS,COMMUNITY_SIGNALS,AI_ASSISTED_WORK}.md`
- `.bequite/money/{HIDDEN_GEMS,COMMUNITY_SIGNALS,AI_ASSISTED_PATHS}.md`

---

## Operating Modes (alpha.12)

4 composable modes — Deep / Fast / Token Saver (alias `lean`) / Delegate. Set on any command as a positional flag. Modes adjust depth / cost / speed; they NEVER bypass safety. All 17 hard human gates apply regardless of mode.

### Mode decision matrix

| Mode | Best for | Avoid when | Research depth | Testing depth | Output length | Driving skill |
|---|---|---|---|---|---|---|
| **deep** | Quality-critical · production · regulated (PCI / HIPAA / FedRAMP) · big new builds | Trivial prototype · throwaway spike · "rename a button" | Full 11-dim + community + competitors + non-English + failure stories | Full + red-team if warranted | Long, detailed | `bequite-researcher` + 11-dim depth across specialist skills |
| **fast** | Small fix · scoped feature · prototype · trusted stack | Production-bound · security · new architecture decisions · regulated | 3 dims (stack / security / scale) + memory-first | Run tests for changed surface | Compact | `bequite-workflow-advisor` (mode controller) |
| **token-saver** *(alias `lean`)* | Long sessions · cost-sensitive · partial work · revisit cached research | First-time research · architecture · production sign-off | Reuse prior research + targeted grep + summaries | Scoped | Compact | `bequite-workflow-advisor` (mode controller) |
| **delegate** | Strong model designs → cheap model implements → strong model reviews | Trivial task (overhead) · no prior research (auto-compose with `deep`) | Strong model in Phase 1 | Cheap model runs task-pack tests; strong model verifies in Phase 3 | Variable | `bequite-delegate-planner` (alpha.12) |

### Composition rules

| Composition | Behavior |
|---|---|
| `deep` + `delegate` | Strongly recommended for large features — strong model researches deeply then writes delegate task pack |
| `fast` + `delegate` | OK for well-understood feature; saves cost |
| `fast` + `token-saver` | Quick small fix with low context use |
| `token-saver` + `delegate` | Cheap model implements from cached research |
| `deep` + `token-saver` | Thorough research on follow-up task using cached research |

### Conflict resolution

| Conflict | Resolution |
|---|---|
| `fast` + `deep` | Ask one question; default `deep` for quality-critical intents; `fast` for trivial scoped fixes |
| `delegate` + tiny task | Refuse delegate; recommend `fast` |
| `delegate` + no prior research | Auto-compose with `deep` |
| Any mode + hard human gate | Mode never bypasses safety; gate fires regardless |

### Mode-related files

- `.bequite/state/CURRENT_MODE.md` — active mode for current run
- `.bequite/state/MODE_HISTORY.md` — append-only history (which mode for which task; outcome; approx cost; tests pass/total)
- `.bequite/tasks/DELEGATE_TASKS.md` — task pack with Task ID / Goal / Files to inspect / Files to edit / Do not touch / Exact steps / Edge cases / Test commands / Acceptance criteria / Common mistakes / Rollback notes
- `.bequite/tasks/DELEGATE_INSTRUCTIONS.md` — strong-model warnings + constraints + common mistakes
- `.bequite/tasks/DELEGATE_ACCEPTANCE_CRITERIA.md` — concrete pass/fail per task
- `.bequite/tasks/DELEGATE_TEST_PLAN.md` — test commands cheap model must run
- `.bequite/audits/DELEGATE_REVIEW_REPORT.md` — Phase-3 strong-model verdict per task

### Phase-3 delegate review (strong-model check)

After cheap model implements from the task pack, strong model MUST review:
- File placement
- Function design
- Naming
- Integration
- Tests run + pass
- Security regressions
- UX regressions if relevant
- Docs / log updates

Verdict per task: ✅ APPROVED · ⚠ APPROVED-WITH-COMMENTS · ❌ REJECTED.

---

## Summary

44 commands, 21 skills, 6 workflow modes, **4 operating modes**, 6 phases, 23 gates, 17 hard human gates, **Creative + Content Workflows (alpha.13)**.

**Discipline + memory + verified evidence > velocity without a plan.**

**Scoped auto-mode means: continue by default until task is complete, tested, verified, and logged. Pause only at hard human gates. Operating modes (`deep | fast | token-saver | delegate`) adjust depth, cost, and speed — without skipping safety. Modes are composable.**
