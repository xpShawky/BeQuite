# Project changelog

Tracked by BeQuite. Use `/bq-changelog` to add entries. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added (v3.0.0-alpha.4 — scoped auto, UI variants, live edit)
- **`/bq-auto [intent] "task"`** — scoped autonomous runner. Parses 17 intent types from `$ARGUMENTS` (new / existing / feature / fix / uiux / frontend / backend / database / security / testing / devops / scraping / automation / deploy / live-edit / variants / release). Continues by default until task is complete, tested, verified, logged. Pauses only at 17 hard human gates.
- **`/bq-uiux-variants [N] "task"`** — generate 1-10 isolated UI design directions. Variants live in `/uiux/v1`…`/uiux/vN` routes or `src/uiux-variants/Variant0N/` components. User picks winner; agent merges; rejected archive to `.bequite/uiux/archive/`. UIUX_VARIANTS_REPORT.md captures the comparison.
- **`/bq-live-edit "task"`** — lightweight section-by-section frontend edit. Maps visible sections to source files via SECTION_MAP.md; applies targeted edits; verifies via build + (optional, never auto-installed) browser screenshots. LIVE_EDIT_LOG.md captures every edit with before/after diff.
- **`bequite-live-edit`** skill — 14-section deep procedure for live edits (stack detection, dev server detection, three-tier browser inspection, section mapping, edit strategy, screenshots, tests, rollback).
- **3 architecture docs:** AUTO_MODE_STRATEGY.md, UIUX_VARIANTS_STRATEGY.md, LIVE_EDIT_STRATEGY.md.
- **5 memory templates** under `.bequite/uiux/`: SECTION_MAP.md, LIVE_EDIT_LOG.md, UIUX_VARIANTS_REPORT.md, selected-variant.md, screenshots/ + archive/ directories.
- **17 hard human gates** (expanded from 12 in alpha.2): added VPS/Nginx/SSL change, paid service activation, secret/key handling, project architecture change, deleting old impl with callers; clarified UI variant winner selection + release git ops.

### Changed (v3.0.0-alpha.4)
- `CLAUDE.md` — v3.0.0-alpha.4 spec; 36 commands, 15 skills; hard gate list expanded to 17; new file paths and architecture docs registered.
- `docs/specs/COMMAND_CATALOG.md` — added bq-uiux-variants + bq-live-edit; bq-auto entry expanded with 17 intent types + 17 hard gates.
- `docs/runbooks/USING_BEQUITE_COMMANDS.md` — v3.0.0-alpha.4 examples section appended.
- `bequite-frontend-quality` skill — activation list extended to include uiux-variants, live-edit, and auto intents.
- `bequite-ux-ui-designer` skill — new sections for "When activated by /bq-uiux-variants" + "When activated by /bq-live-edit".
- `bequite-testing-gate` skill — new section for variant + live-edit verification.
- `bequite-problem-solver` skill — note about scoped auto fix + live-edit fix-shaped tasks.
- `bequite-project-architect` skill — activation list extended.

### Added (v3.0.0-alpha.3 — tool neutrality principle)
- `.bequite/principles/TOOL_NEUTRALITY.md` — canonical source of truth for the rule that every named tool is an EXAMPLE, not a default.
- `docs/decisions/ADR-003-tool-neutrality.md` — formalizes the decision.
- **10 decision questions** every major tool pick must answer (project type, problem, scale, constraints, stack, UX, failure risks, proven tools, overkill, complexity).
- **Decision section format** required before any tool pick (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan).
- **Do-not-auto-install defaults** — no dependencies, scraping tools, frontend libs, Docker, testing frameworks, deployment tools, monitoring, or auth libs added by default.
- **Research-depth rule** — 11 dimensions of research, not just stack. Tool choice comes AFTER project understanding.

### Changed (v3.0.0-alpha.3)
- `CLAUDE.md` — tool neutrality is now Core Operating Rule #1; 10 decision questions enumerated.
- All 11 tool-touching skills (researcher, project-architect, frontend-quality, ux-ui-designer, backend-architect, database-architect, security-reviewer, testing-gate, devops-cloud, scraping-automation, release-gate) — appended Tool Neutrality block.
- All 8 tool-touching commands (bq-research, bq-plan, bq-feature, bq-fix, bq-audit, bq-review, bq-red-team, bq-verify) — appended Tool Neutrality block.
- Canonical phrasing standardized: replace "Use X." with "X is one candidate. Research and compare against other options. Use it only if it fits this project."

### Added (v3.0.0-alpha.2 — direction reset Cycle 2)
- **Mandatory workflow gate system** — `.bequite/state/WORKFLOW_GATES.md` ledger with 23 gates across 6 phases. Commands refuse to run when required gates aren't met.
- **6 explicit modes** — `.bequite/state/CURRENT_MODE.md`: New Project, Existing Audit, Add Feature, Fix Problem, Research Only, Release Readiness.
- **10 new commands** — `/bq-mode`, `/bq-new`, `/bq-existing`, `/bq-feature`, `/bq-auto`, `/bq-p0`..`/bq-p5`. Total now 34 commands.
- **Phase orchestrators** — `/bq-p0` through `/bq-p5` walk one phase end-to-end.
- **Autonomous runner** — `/bq-auto` walks ALL phases with 12 hard human gates.
- **7 new specialist skills** — bequite-researcher (11 dimensions), bequite-product-strategist, bequite-ux-ui-designer, bequite-backend-architect, bequite-database-architect, bequite-security-reviewer, bequite-devops-cloud. Total now 14 skills.
- **Add Feature 12-type router** — `/bq-feature` classifies into Frontend / Backend / Database / Auth / Automation / Scraping / Cloud / Admin / Dashboard / CLI / Integration / Security and activates matching skills.
- **Fix 15-type router** — `/bq-fix` classifies into Frontend / Backend / Database / Auth / Build / Test / Deploy / Perf / Security / Dep / Config / Network / Memory / Race / Cross-browser and activates matching skills.
- **ADR-002** — mandatory workflow gates.
- **COMMAND_CATALOG.md** — single source of truth for all 34 commands with their gates + skills + reads/writes.

### Changed (v3.0.0-alpha.2)
- `/bequite` root menu now **gate-aware** — reads `WORKFLOW_GATES.md`, displays phase gate status, refuses to recommend commands whose required gates aren't met.
- `/bq-research` expanded from single-dimension freshness probe to **11 dimensions** (stack, product, competitors, failures, success, user journey, UX/UI, security, scalability, deployment, differentiation).
- `/bq-plan` activates **multi-skill** thinking (project-architect + backend-architect + database-architect + security-reviewer + devops-cloud + ux-ui-designer + frontend-quality + testing-gate). 15 sections including §11 security and §12 devops.
- `/bq-multi-plan` enforces **unbiased external prompts** — external model prompts contain ZERO mention of Claude's plan. Both models propose independently from the same briefing.
- `/bq-fix` reproduce-first procedure now classifies into one of 15 problem types and activates matching specialist skills.
- `CLAUDE.md` reflects 34 commands, 14 skills, modes, gates, hard human gates, required-reads list.

### Added (v3.0.0-alpha.1 direction)
- v3.0.0-alpha.1: BeQuite is a lightweight project skill pack at `.claude/commands/` + `.claude/skills/` + `.bequite/` memory.
- 24 slash commands: `/bequite` (root menu) + 23 `/bq-*` workflow commands across 5 phases.
- 7 focused skills: project-architect, problem-solver, frontend-quality, testing-gate, release-gate, scraping-automation, multi-model-planning.
- Lightweight installer scripts.
- ADR-001: lightweight-skill-pack-first.

### Changed (v3.0.0-alpha.1)
- README rewritten to lead with skill-pack install + `/bequite` usage.
- CLAUDE.md shortened — points at the new `.claude/commands/` + `.claude/skills/` + `.bequite/` structure.

### Paused (kept on disk; not deleted)
- `studio/` (marketing + dashboard + api + brand)
- `docker-compose.yml`, `.dockerignore`, Dockerfiles
- `tests/e2e/` (Playwright Studio tests)
- `scripts/docker-up.{ps1,sh}`
- Root `package.json` + `Makefile`

(per DIRECTION_RESET_AUDIT.md — deletion gated on explicit user approval)

---

## (Pre-reset history)

For releases v0.1.0 → v2.0.0-alpha.6 (the heavy-app direction), see the repo-root `CHANGELOG.md`. This `.bequite/logs/CHANGELOG.md` tracks the skill-pack era going forward.
