# BeQuite Changelog

Format: [Keep a Changelog v1.1](https://keepachangelog.com/en/1.1.0/) · Versioning: [Semantic Versioning](https://semver.org/).

Legacy (v0.x → v2.0.0-alpha.6 heavy-direction) archived at [`docs/legacy/CHANGELOG-legacy.md`](../legacy/CHANGELOG-legacy.md) after Phase B cleanup.

---

## [Unreleased — alpha.14]

- USING_BEQUITE_COMMANDS.md updated with /bq-presentation walkthrough + delegate walkthrough
- Cross-references: MULTI_MODEL_PLANNING_STRATEGY.md ↔ delegate; MEMORY_FIRST_BEHAVIOR.md ↔ token-saver; RESEARCH_DEPTH_STRATEGY.md ↔ deep
- Live verification of all 4 modes + /bq-presentation against a real project (user action)
- Decision: optional `/bq-deck` alias for `/bq-presentation` if user pressure demands

---

## [v3.0.0-alpha.13] — 2026-05-13

### Added — Creative and Content Workflows category

- **`/bq-presentation`** — premium PPTX or HTML presentation builder. World-class output, designed to feel professional rather than generic AI.
  - Natural-language syntax (quotes optional)
  - Options: `format` (pptx / html / both / auto), `variants` (1–10), `source` (folder / pdf / word / docx / url / mixed / topic-only), `strict` / `creative`, `audience`, `style`, `duration`, `language`, `topic`, `brand`, `references`, `notes`, `motion`
  - Strict mode preserves source claims (PDF / Word / scientific source) — no unsupported facts
  - Creative mode adds structure (hooks, story arcs, examples) with assumptions marked
  - Variants 1–10: different design directions (Academic Clean / Premium Cinematic / Corporate Keynote / Medical Conference / Minimal Lecture / Dark Futuristic / Light Editorial / Data-Dashboard / Student-Friendly / Brand-Led — candidates only)
  - **Morph-like PPTX motion** — same object across sequential slides with stable IDs; duplicate slides for movement; 1–2 transformations at a time; 0.3–0.8s timing
  - **HTML motion vocabulary** — title glow, staged bullets, card focus, light sweep, smooth section transitions (every effect earns its place; no random animation)
  - Brand asset extraction (palette / typography / layout / icon style — writes `DESIGN_BRIEF.md` BEFORE any slide)
  - 14-item verification checklist
  - Operating modes composable: `deep` / `fast` / `token-saver` / `delegate`
  - Tool neutrality: python-pptx / pptxgenjs / reveal.js / Slidev / Marp / Spectacle / Impress.js / GSAP / Motion One / Playwright are CANDIDATES only — none installed by default
- **`bequite-presentation-builder`** skill — encodes the 14-step workflow, PPTX vs HTML decision rule, morph-like discipline, AI-slop reject list, variants discipline, strict-vs-creative content rules, brand-asset extraction, verification checklist
- **`.bequite/presentations/`** memory folder with 9 templates:
  - `PRESENTATION_BRIEF.md` — what / why / who / format / strict-vs-creative
  - `CONTENT_OUTLINE.md` — title / hook / story arc / slide outline / references plan
  - `SLIDE_PLAN.md` — slide-by-slide content (purpose / headline / body / visual / speaker-note pointer / source / motion ref)
  - `DESIGN_BRIEF.md` — palette / typography / grid / icon style / AI-slop reject list / brand extraction
  - `MOTION_PLAN.md` — PPTX morph-like discipline + HTML motion vocabulary + audience-fit motion baseline
  - `SPEAKER_NOTES.md` — per-slide talking points (strict-mode source-traced; creative-mode assumptions marked)
  - `REFERENCES.md` — sources, citations, attribution, anti-hallucination check
  - `PRESENTATION_VARIANTS_REPORT.md` — per-variant visual direction + pros/cons + recommendation; user picks winner
  - `EXPORT_LOG.md` — every export attempt + tool chosen + verification result
  - `assets/.gitkeep`, `outputs/.gitkeep`

### Changed

- README.md — new "Creative and Content Workflows (alpha.13)" section + version bump to alpha.13 + skill count 20 → 21 + command count 43 → 44 + skill list updated
- commands.md — new "Creative and Content Workflows (alpha.13)" section with full `/bq-presentation` spec + ToC entry + version bump
- `.claude/commands/bequite.md` — new "Creative and Content Workflows (alpha.13)" block in root menu
- `.claude/commands/bq-help.md` — added `/bq-presentation` to alpha.5+ surface list
- `.claude/commands/bq-suggest.md` — added presentation keyword triggers (slides / presentation / lecture / PowerPoint / PPTX / keynote / deck / convert PDF / Word file → slides)
- `.claude/skills/bequite-workflow-advisor/SKILL.md` — added `/bq-presentation` routing patterns + new "Creative + Content" command-table row
- `docs/specs/COMMAND_CATALOG.md` — full `/bq-presentation` entry + tallies bumped to 44 commands / 21 skills
- `CLAUDE.md` — spec bumped to alpha.13 + Creative + Content Workflows mention + presentation memory path
- `scripts/install-bequite.{ps1,sh}` — bumped to alpha.13 + scaffold `.bequite/presentations/` (+ `assets/`, `outputs/`) + copy the 9 presentation templates + updated install banner
- `BEQUITE_VERSION.md` — bumped to alpha.13

### Naming decisions

- One canonical command: `/bq-presentation`. Optional alias `/bq-deck` deferred to alpha.14 (avoid command clutter; alpha.13 is 44 commands — enough).
- Skill is `bequite-presentation-builder` (consistent with naming convention).
- Memory folder is `.bequite/presentations/` (plural, parallel to `jobs/`, `money/`, `uiux/`).

### Parser discipline (important)

- Natural language understood — quotes NOT required
- Mode words (`deep`, `fast`, `delegate`, `uiux`, `presentation`, `pptx`, `html`) treated as flags ONLY when:
  - `key=value`
  - inside brackets `[format=pptx, variants=3]`
  - immediately after the command name as known flag
  - clearly separated from the natural-language task
- If a word appears naturally inside the topic text (e.g. "explain fast learning") it stays as topic text, NOT a mode

### Acceptance (alpha.13 — all met)

- `/bq-presentation` command file exists with full spec ✅
- `bequite-presentation-builder` skill exists ✅
- README mentions presentation capability + new section ✅
- commands.md has full entry ✅
- COMMAND_CATALOG.md updated ✅
- `/bequite` root menu shows Creative + Content Workflows ✅
- `/bq-help` updated ✅
- `/bq-suggest` recommends `/bq-presentation` for slide/lecture/PowerPoint/PDF/Word keywords ✅
- `bequite-workflow-advisor` routes presentation queries ✅
- Memory folder `.bequite/presentations/` exists with 9 templates + assets/ + outputs/ ✅
- Strict vs creative documented ✅
- PPTX vs HTML decision logic documented ✅
- Variants discipline (1–10, different *directions*) documented ✅
- Morph-like PPTX motion planning documented ✅
- Source / reference handling documented ✅
- AGENT_LOG updated ✅
- CHANGELOG updated (this entry) ✅
- Installer carries the new templates ✅
- No heavy dependencies added ✅ (no python-pptx, pptxgenjs, reveal.js, Slidev, Playwright — all candidates only)

### Not done (deferred to alpha.14)

- USING_BEQUITE_COMMANDS.md walkthrough with worked presentation example
- `/bq-deck` alias (only if user demand justifies)
- Decision section example in `DECISIONS.md` for a chosen PPTX library (will run when user invokes `/bq-presentation` for real implementation)
- Live verification on a real project (user action)

---

## [v3.0.0-alpha.12] — 2026-05-12

### Added — 4 composable operating modes

- **Deep Mode** — full 11-dim research + community sources (GitHub / Reddit / HN / X / Product Hunt / niche forums / non-English) + multi-plan prompted + red-team mandatory + full audit. For new SaaS / regulated / production-bound / high-stakes work.
- **Fast Mode** — short discovery + shallow research (3 dims) + reuse memory. Still tests + verifies + logs. Not low-quality mode; just skips what isn't needed.
- **Token Saver Mode** (alias: `lean`) — read core memory first + focused files only + reuse cached research + compact reports. **Different from Fast Mode**: optimizes token cost, not speed. Naming correction: NOT "token-free".
- **Delegate Mode** (Architect Delegate pattern) — strong model architects + writes task pack at `.bequite/tasks/DELEGATE_*.md` → cheaper model implements exactly in separate session → strong model reviews at `.bequite/audits/DELEGATE_REVIEW_REPORT.md`. 40-70% cost savings on large features.

Modes compose: `deep delegate` (recommended for new features), `fast token-saver`, `deep token-saver`, `uiux variants=5 deep`, etc. Conflict resolution defaults provided.

### Added — skill + memory

- `bequite-delegate-planner` skill — full strong-model-plans-cheap-model-implements-strong-model-reviews workflow with task-pack format, hard-gate handling, mode composition, cost discipline
- 5 new memory templates: `.bequite/tasks/DELEGATE_TASKS.md`, `DELEGATE_INSTRUCTIONS.md`, `DELEGATE_ACCEPTANCE_CRITERIA.md`, `DELEGATE_TEST_PLAN.md`, `.bequite/audits/DELEGATE_REVIEW_REPORT.md`
- 1 new state file: `.bequite/state/MODE_HISTORY.md` (tracks mode usage + outcome per run; informs `/bq-suggest` and `bequite-workflow-advisor`)

### Changed

- `bequite-workflow-advisor` skill extended with mode-controller logic (decision matrix + composition table + conflict resolution + MODE_HISTORY.md learning loop)
- `/bq-auto.md` — full Mode section rewrite covering all 4 modes + composition + conflict resolution + mode tracking. Mistake-memory section now also appends to MODE_HISTORY.
- `docs/architecture/AUTO_MODE_STRATEGY.md` §11 — comprehensive new mode section
- `README.md` — top-level "Operating Modes" section near the top (major selling point). Version bumped to alpha.12. New "4 modes" badge.
- `/bequite` root menu — new "Operating modes" section
- `/bq-help` — modes table
- `commands.md` — top-level "Operating modes (alpha.12)" section with mode table + composition + conflict + delegate-specific link
- `CLAUDE.md` — version bump + 4 composable modes mention
- `docs/specs/COMMAND_CATALOG.md` — full mode decision matrix
- `BEQUITE_VERSION.md` — bumped to alpha.12

### Naming decisions

- Renamed user-suggested "Architect Delegate Mode" → **"Delegate Mode"** (short for the flag; the longer name describes the pattern in docs)
- Added `lean` as alias for `token-saver`
- No new `/bq-delegate` command — delegate is a mode flag (avoids command clutter)

### Tally after alpha.12

- Commands: 43 (unchanged — modes are flags, not new commands)
- Skills: 19 → 20 (+1: bequite-delegate-planner)
- Memory templates: +6 (5 delegate + 1 MODE_HISTORY)
- Operating modes: 0 → **4 composable**

---

## [v3.0.0-alpha.11] — 2026-05-12

### Added
- Installer scripts (PowerShell + bash) now copy alpha.10 templates into target projects on `/bq-init`:
  - jobs deep-intelligence: `HIDDEN_GEMS.md`, `COMMUNITY_SIGNALS.md`, `AI_ASSISTED_WORK.md`
  - money deep-intelligence: `HIDDEN_GEMS.md`, `COMMUNITY_SIGNALS.md`, `AI_ASSISTED_PATHS.md`
  - version + update tracking: `BEQUITE_VERSION.md`, `UPDATE_SOURCE.md`, `UPDATE_LOG.md`
- Directory scaffold extended: `.bequite/backups/`
- Final install banner now shows "Maintenance (alpha.10)" section with `/bq-update`
- CLAUDE.md template updated to surface `/bq-update`, deep intelligence flags, and memory-first principle reference

### Changed
- Installer version messaging: `v3.0.0-alpha.8` → `v3.0.0-alpha.10`
- Installer banner counts: "42 slash commands" → "43"; "18 specialist skills" → "19"

### Effect
New BeQuite installs match alpha.10 functionality immediately. `/bq-update` works from day one because BEQUITE_VERSION.md + UPDATE_SOURCE.md are present.

---

## [v3.0.0-alpha.10] — 2026-05-12

### Added

#### Maintenance command
- `/bq-update` — safely update BeQuite (commands / skills / docs / templates) from GitHub or local source. Modes: check / safe (default) / force / source=local / source=github. Backs up before changes; never overwrites project memory; surfaces conflicts as `.bequite-update.md` sibling files.
- `bequite-updater` skill — version detection / source resolution / SHA-256 diff / merge per file class / conflict handling / logging / rollback / test-after-update discipline.
- Memory files: `.bequite/state/BEQUITE_VERSION.md`, `.bequite/state/UPDATE_SOURCE.md`, `.bequite/logs/UPDATE_LOG.md`, `.bequite/backups/`

#### Deep Opportunity Intelligence
- `/bq-job-finder` + `/bq-make-money` extended with deep intelligence:
  - **Community + conversation sources:** Reddit / Indie Hackers / Hacker News / Product Hunt / X / public LinkedIn / Facebook / Discord / Slack / YouTube creator communities / app reviews
  - **Trending + short-window opportunities:** new AI task platforms, data labeling campaigns, app testing, research panels, browser panels
  - **AI-assisted work paths:** catalog of work where AI stack is a multiplier
  - **Hidden Gems** logic with full per-gem fields
- **11 new tracks:** `worldwide_hidden`, `trending_now`, `community_discovered`, `AI_assisted`, `no_calls`, `fast_first_payout`, `highest_payout`, `beginner_friendly`, `skilled_remote`, `local_country`, `non_english_platforms` — stackable
- **Multi-language search:** 13 languages + user-listed
- **Per-opportunity required fields:** confidence level added (in addition to existing trust check fields)
- 6 new memory files: `.bequite/jobs/{HIDDEN_GEMS,COMMUNITY_SIGNALS,AI_ASSISTED_WORK}.md` + `.bequite/money/{HIDDEN_GEMS,COMMUNITY_SIGNALS,AI_ASSISTED_PATHS}.md`

#### Memory-First Behavior
- `docs/architecture/MEMORY_FIRST_BEHAVIOR.md` — universal principle for all action-taking commands
- Core memory list + optional memory list + per-command read/write matrix for all 43 commands
- Token-saving memory strategy
- Auto-mode memory strategy
- Mistake memory strategy
- Standardized memory preflight + writeback templates

### Changed

- `/bequite` root menu — added "Maintenance" section with `/bq-update`
- `/bq-help` — added `/bq-update` + alpha.10 deep intelligence note
- `README.md` — version bump to alpha.10; 43-command badge; new Opportunity and Workflows + Maintenance sections in command map; deep intelligence highlighted
- `CLAUDE.md` — version bump; memory-first principle referenced; new memory paths
- `docs/specs/COMMAND_CATALOG.md` — added `/bq-update` entry; added deep intelligence flags table; tallies bumped to 43/19
- `commands.md` — added Maintenance section with full `/bq-update` entry

### Tally

- Commands: 42 → 43 (+1)
- Skills: 18 → 19 (+1)
- New memory files: +9 (6 opportunity + 3 version/update)
- New memory directory: +1 (backups/)
- Architecture docs: +1 (MEMORY_FIRST_BEHAVIOR.md)
- New tracks: +11 (deep intelligence flags)

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
