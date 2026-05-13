# BeQuite Changelog

Format: [Keep a Changelog v1.1](https://keepachangelog.com/en/1.1.0/) · Versioning: [Semantic Versioning](https://semver.org/).

Legacy (v0.x → v2.0.0-alpha.6 heavy-direction) archived at [`docs/legacy/CHANGELOG-legacy.md`](../legacy/CHANGELOG-legacy.md) after Phase B cleanup.

---

## [Unreleased — alpha.10]

- Live verification of `/bequite` against fresh real-world projects (user-action — installer is now feature-complete)
- Architecture docs expanded from concise summaries to full reference depth
- `/bq-help` extended with full standardized fields (currently has alignment notice + brief block)

---

## [v3.0.0-alpha.9] — 2026-05-12

### Added
- Installer scripts (PowerShell + bash) now copy alpha.8 opportunity-memory templates into target projects on `/bq-init`:
  - `.bequite/jobs/` — JOB_PROFILE, JOB_SEARCH_LOG, OPPORTUNITIES, APPLICATION_TRACKER, PITCH_TEMPLATES
  - `.bequite/money/` — MONEY_PROFILE, MONEY_SEARCH_LOG, OPPORTUNITIES, TRUST_CHECKS, ACTION_PLAN
- Directory scaffold extended: `.bequite/jobs/`, `.bequite/money/`
- Final install banner includes "Opportunity and Workflows (alpha.8)" section listing `/bq-suggest`, `/bq-job-finder`, `/bq-make-money` + the `worldwide_hidden=true` flag

### Changed
- Installer version messaging: `v3.0.0-alpha.5` → `v3.0.0-alpha.8`
- Installer banner counts: "37 slash commands" → "42"; "15 specialist skills" → "18"
- CLAUDE.md template (created on first install) now references the 3 new opportunity commands

### Effect
New BeQuite installs match alpha.8 functionality immediately — no manual file copying.

---

## [v3.0.0-alpha.8] — 2026-05-12

### Added — Opportunity and Workflows

- `/bq-suggest "<situation>"` — BeQuite workflow advisor; recommends best commands/skills/mode/gates for the goal. Read-only. Activates `bequite-workflow-advisor` skill (knows all 42 commands + 18 skills + 23 gates + 17 hard human gates).
- `/bq-job-finder` — real work opportunity finder. Intake → JOB_PROFILE.md → live research → trust check → ranked classification → pitches. Supports `worldwide_hidden=true` (multilingual hidden opportunities).
- `/bq-make-money` — earning opportunity finder. 10 tracks (highest-payout / easiest-start / fastest-first-dollar / long-term-stable / ai-assisted / no-calls / remote-global / local-only / beginner / skilled). Supports `worldwide_hidden=true` for Hidden Gems. 7-day action plan output. Repeat-search comparison.
- 3 new skills: `bequite-workflow-advisor`, `bequite-job-finder`, `bequite-make-money`
- New memory folders: `.bequite/jobs/` (5 templates: JOB_PROFILE, JOB_SEARCH_LOG, OPPORTUNITIES, APPLICATION_TRACKER, PITCH_TEMPLATES); `.bequite/money/` (5 templates: MONEY_PROFILE, MONEY_SEARCH_LOG, OPPORTUNITIES, TRUST_CHECKS, ACTION_PLAN)
- Strict safety rules across opportunity commands: no scams, fake reviews, VPN misrepresentation, upfront-fee, identity misuse, CAPTCHA farms, platform abuse, fake accounts, fake engagement, spam, unrealistic income promises

### Changed

- `/bequite` root menu — added "Opportunity and Workflows" section
- `/bq-help` — added new commands to alpha.2+ list
- `README.md` — version bump to alpha.8; 42-command badge; new commands + Worldwide Hidden Opportunity Search section in main body
- `CLAUDE.md` — version bump; new commands referenced; new memory paths in "Where things live"
- `docs/specs/COMMAND_CATALOG.md` — full entries for 3 new commands; tallies bumped
- `commands.md` — Opportunity and Workflows section with examples + Worldwide Hidden Opportunity Search explainer

### Constraints honored

- No heavy app added · no dashboard added · no big CLI added · no heavy dependencies added by default
- Commands + skills + docs + memory updates only
- No actual job APIs or browser automation runtime added — live research happens via WebFetch/WebSearch when the user invokes the command

---

## [v3.0.0-alpha.7] — 2026-05-12

### Added
- `/bq-spec "<feature>"` — Spec Kit-compatible one-page spec writer. Bridges BeQuite to the GitHub Spec Kit ecosystem. Writes `specs/<slug>/spec.md` with What / Why / Who / Acceptance / Out-of-scope / Constraints / Open questions / Success metric. Activates `bequite-product-strategist` for JTBD discipline.
- `/bq-explain "<target>"` — plain-English explainer for files / functions / decisions / concepts / BeQuite artifacts. 4-section structured output. Read-only. Use cases: onboarding, vibe-handoff prep, understanding inherited code, learning what `/bq-auto` did.

### Changed
- `bq-help.md` — added alpha.5+ alignment notice at top pointing to `commands.md`; added standardized command fields block at the end; documented updated phase names + commands added in alpha.2+
- `README.md` — version bump to alpha.7; 39-command badge; new commands added to command map + MVP roadmap
- `CLAUDE.md` — version bump; new commands referenced
- `docs/specs/COMMAND_CATALOG.md` — added `/bq-spec` + `/bq-explain` entries
- `commands.md` — added `/bq-spec` + `/bq-explain` full entries with examples + skill activation

---

## [v3.0.0-alpha.6] — 2026-05-12

### Added
- Installer scripts (both PowerShell + bash) updated to copy alpha.5 templates into target projects:
  - `.bequite/principles/TOOL_NEUTRALITY.md`
  - `.bequite/state/MISTAKE_MEMORY.md`, `ASSUMPTIONS.md`
  - `.bequite/uiux/SECTION_MAP.md`, `LIVE_EDIT_LOG.md`, `UIUX_VARIANTS_REPORT.md`, `selected-variant.md`
  - `.bequite/uiux/screenshots/`, `.bequite/uiux/archive/`
  - `commands.md` at project root
- 19 alpha.1 commands extended with "Standardized command fields (alpha.6)" section: bq-init, bq-discover, bq-doctor, bq-clarify, bq-scope, bq-assign, bq-implement, bq-test, bq-audit, bq-review, bq-red-team, bq-verify, bq-release, bq-changelog, bq-memory, bq-recover, bq-handoff, bequite (root), bq-add-feature
- Each gained: Phase / When NOT to use / Preconditions / Required previous gates / Quality gate (success criteria) / Failure behavior / Memory updates / Log updates

### Changed
- Installer CLAUDE.md template (created or appended) now references `/bq-now`, `/bq-auto`, `commands.md`, TOOL_NEUTRALITY.md, gates
- Installer end-of-install message highlights autonomous mode + new commands

---

## [v3.0.0-alpha.5] — 2026-05-12

### Added
- `/bq-now` — one-line orientation command (faster than `/bequite`)
- `commands.md` at repo root — full human-readable command reference, workflow-ordered, linked from README
- `--mode fast | deep | token-saver` flag on `/bq-auto` (depth adjustment; does NOT skip safety gates)
- Mistake-memory writes wired into 7 commands (`/bq-fix`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`, `/bq-auto`, `/bq-live-edit`)

### Removed
- `studio/` directory (full Next.js app: marketing + api + dashboard + brand)
- `docker-compose.yml` (Studio Docker orchestration)
- `scripts/docker-up.ps1`, `scripts/docker-up.sh` (Studio dev runners)
- Git history retains all of the above (ADR-004)

### Changed
- README: badge updated to 37 commands; `commands.md` link surfaced near the top; alpha.5 roadmap consolidated
- CLAUDE.md: version bump; new file paths; mistake-memory + `/bq-now` + `commands.md` referenced
- COMMAND_CATALOG.md: `/bq-now` entry added; tallies bumped; pointed at `commands.md`

### Kept (per user "remove only studio") — explicitly NOT removed
- `cli/`, `tests/`, `template/`, `evidence/`, `examples/`, `prompts/`, `state/`, `skill/`
- `.dockerignore`, `.env.example`, `Makefile`, `package.json`, `.commitlintrc.json`
- `scripts/bootstrap.{ps1,sh}`, `scripts/install.{ps1,sh}`
- `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md`, `docs/runbooks/LOCAL_DEV.md`
- `BeQuite_MASTER_PROJECT.md`, root `CHANGELOG.md`

---

## [v3.0.0-alpha.4] — 2026-05-12

### Added — workflow upgrades
- **Scoped `/bq-auto`** — parses `$ARGUMENTS` for 17 intent types (`new | existing | feature | fix | uiux | frontend | backend | database | security | testing | devops | scraping | automation | deploy | live-edit | variants | release`). Continues by default; pauses only at 17 hard human gates.
- **UI/UX variants** — `/bq-uiux-variants [N]` generates 1-10 isolated design directions. Each lives in `/uiux/v1` route or `src/uiux-variants/Variant01/` component. Original UI untouched. User picks winner; agent merges.
- **Live edit workflow** — `/bq-live-edit` lightweight section-by-section frontend edits. Maps visible sections to source files (SECTION_MAP.md). Three-tier browser inspection (Playwright MCP → project-local Playwright → code-only).
- New skill: `bequite-live-edit`
- New strategy docs: AUTO_MODE_STRATEGY, UIUX_VARIANTS_STRATEGY, LIVE_EDIT_STRATEGY
- New memory tree: `.bequite/uiux/` (SECTION_MAP, LIVE_EDIT_LOG, UIUX_VARIANTS_REPORT, selected-variant, screenshots/, archive/)

### Changed (alpha.4)
- `/bq-auto` fully rewritten — 17 intents + 17 hard human gates (replaced alpha.2's 12)
- CLAUDE.md updated to v3.0.0-alpha.4 spec; 36 commands, 15 skills
- COMMAND_CATALOG.md added bq-uiux-variants, bq-live-edit; expanded bq-auto entry
- USING_BEQUITE_COMMANDS.md added v3.0.0-alpha.4 examples section
- 5 existing skills extended with activation lists

### Tally
- Commands: 34 → 36 (+2)
- Skills: 14 → 15 (+1)
- Auto intents: 0 → 17
- Hard human gates in /bq-auto: 12 → 17
- Architecture docs: 1 → 4

---

## [v3.0.0-alpha.3] — 2026-05-11

### Added — tool neutrality
- `.bequite/principles/TOOL_NEUTRALITY.md` — canonical source of truth
- `docs/decisions/ADR-003-tool-neutrality.md` — formalizes the decision
- **10 decision questions** every major tool pick must answer
- **Decision section format** required before tool adoption
- **Do-not-auto-install defaults** — no deps / frontend libs / Docker / testing frameworks / monitoring / auth libs added by default
- **Research-depth rule** — 11 dimensions; tool choice AFTER project understanding

### Changed (alpha.3)
- CLAUDE.md — tool neutrality is now Core Operating Rule #1
- All 11 tool-touching skills updated with Tool Neutrality block
- All 8 tool-touching commands updated with Tool Neutrality block
- Standardized phrasing: "X is one candidate. Research and compare against other options. Use it only if it fits this project."

---

## [v3.0.0-alpha.2] — 2026-05-11

### Added — mandatory workflow gates + scoped modes + specialist skills
- **23 workflow gates** at `.bequite/state/WORKFLOW_GATES.md`
- **6 explicit modes** — New Project, Existing Audit, Add Feature, Fix Problem, Research Only, Release Readiness
- **10 new commands** — `/bq-mode`, `/bq-new`, `/bq-existing`, `/bq-feature` (12-type router), `/bq-auto`, `/bq-p0` through `/bq-p5`
- **Phase orchestrators** — `/bq-p0` … `/bq-p5` walk one phase end-to-end
- **Autonomous runner** — `/bq-auto` walks all phases with 12 hard human gates
- **7 new specialist skills** — researcher (11 dims), product-strategist, ux-ui-designer, backend-architect, database-architect, security-reviewer, devops-cloud
- **Add Feature 12-type router** + **Fix 15-type router**
- ADR-002 — mandatory workflow gates
- COMMAND_CATALOG.md — single source of truth

### Changed (alpha.2)
- `/bequite` root menu now gate-aware
- `/bq-research` expanded from 1 dim → 11 dims
- `/bq-plan` activates multi-skill thinking (15 sections including §11 security and §12 devops)
- `/bq-multi-plan` enforces unbiased external prompts (zero mention of Claude's plan)
- `/bq-fix` reproduce-first procedure with 15-type classification
- CLAUDE.md reflects 34 commands, 14 skills, modes, gates

---

## [v3.0.0-alpha.1] — 2026-05-11

### Added — lightweight skill pack MVP
- 24 slash commands at `.claude/commands/`
- 7 focused skills at `.claude/skills/`
- `.bequite/` memory tree (state, logs, plans, tasks, prompts, audits)
- Lightweight installer scripts (`scripts/install-bequite.{ps1,sh}`)
- ADR-001 — lightweight-skill-pack-first decision
- README rewritten to lead with skill-pack install
- CLAUDE.md shortened to point at `.claude/` + `.bequite/`

### Paused (kept on disk; not deleted in alpha.1)
- `studio/` (marketing + dashboard + api + brand)
- `docker-compose.yml`, `.dockerignore`, Dockerfiles
- `tests/e2e/`
- `scripts/docker-up.{ps1,sh}`
- Root `package.json` + `Makefile`
- `cli/` (Python CLI)

(Per DIRECTION_RESET_AUDIT.md — deletion gated on explicit user approval; delivered in alpha.5 cleanup phase B.)

---

## Pre-reset history (v0.1.0 → v2.0.0-alpha.6)

Heavy-direction lineage: Studio + Docker + heavy CLI. Archived at `docs/legacy/CHANGELOG-legacy.md` (after Phase B cleanup completes).
