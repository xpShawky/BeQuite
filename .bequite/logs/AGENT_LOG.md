# Agent log

Append-only chronicle of every BeQuite command run. Newest at top.

## 2026-05-12 — workflow upgrades (v3.0.0-alpha.4): scoped auto + UI variants + live edit

**Action:** User requested three workflow upgrades to keep BeQuite lightweight while making it more useful:

1. **Scoped auto mode** — `/bq-auto` parses `$ARGUMENTS` for 17 intent types and runs ONLY the relevant scope. Continues by default; does NOT pause for plan / clarify / scope approval. Pauses only at 17 hard human gates.
2. **UI/UX variant mode** — `/bq-uiux-variants [N]` generates 1-10 isolated design directions; user picks winner; agent merges.
3. **Live edit mode** — `/bq-live-edit` section-by-section frontend edits using SECTION_MAP.md + (optional) browser automation. No heavy Studio. No auto-installed Playwright.

**Files created (this cycle):**
- `docs/architecture/AUTO_MODE_STRATEGY.md` — 11-section strategy (intent router, scope per intent, continue-by-default rules, hard human gates, output discipline, cost/time, failure handling, resume)
- `docs/architecture/UIUX_VARIANTS_STRATEGY.md` — 10-section strategy (count discipline, direction selection, isolation A/B/C, workflow, report template, acceptance criteria, tool neutrality, when not to use, anti-patterns)
- `docs/architecture/LIVE_EDIT_STRATEGY.md` — 13-section strategy (mental model, when to use / not, workflow, SECTION_MAP, LIVE_EDIT_LOG, edit categories, quality rules, tool neutrality, anti-patterns, failure modes, rollback)
- `.claude/commands/bq-uiux-variants.md` — new command (count rules, isolation strategies, full workflow, report template, hard gate at winner selection)
- `.claude/commands/bq-live-edit.md` — new command (stack detection, dev server detection, three-tier browser inspection, section mapping, edit, verify, log)
- `.claude/skills/bequite-live-edit/SKILL.md` — new skill (14 sections covering stack detection, browser inspection tiers, section mapping, source resolution, edit strategy, responsive checks, screenshots, tests, failures, rollback)
- `.bequite/uiux/SECTION_MAP.md` — template
- `.bequite/uiux/LIVE_EDIT_LOG.md` — template (append-only log)
- `.bequite/uiux/UIUX_VARIANTS_REPORT.md` — template
- `.bequite/uiux/selected-variant.md` — template (winner record)
- `.bequite/uiux/screenshots/.gitkeep`
- `.bequite/uiux/archive/.gitkeep`

**Files updated (this cycle):**
- `.claude/commands/bq-auto.md` — full rewrite: 17 intent types, $ARGUMENTS parsing, continue-by-default, 17 hard human gates (replaced the 12 from alpha.2)
- `CLAUDE.md` — v3.0.0-alpha.4 spec, 36 commands, 15 skills, hard gate list expanded, new file paths, new architecture docs, intent types
- `docs/specs/COMMAND_CATALOG.md` — added bq-uiux-variants, bq-live-edit, expanded bq-auto entry with intent types + 17 hard gates
- `docs/runbooks/USING_BEQUITE_COMMANDS.md` — added v3.0.0-alpha.4 section with examples for scoped auto / variants / live edit
- `.claude/skills/bequite-frontend-quality/SKILL.md` — activation list extended (uiux-variants, live-edit, auto intents)
- `.claude/skills/bequite-ux-ui-designer/SKILL.md` — new sections "When activated by /bq-uiux-variants" + "When activated by /bq-live-edit"
- `.claude/skills/bequite-testing-gate/SKILL.md` — new section for variant + live-edit verification
- `.claude/skills/bequite-problem-solver/SKILL.md` — note that scoped auto fix + live-edit fix-shaped tasks both invoke this skill
- `.claude/skills/bequite-project-architect/SKILL.md` — activation list extended (auto new, uiux-variants)

**Tally:**
- Commands: 34 → 36 (+2: bq-uiux-variants, bq-live-edit)
- Skills: 14 → 15 (+1: bequite-live-edit)
- Hard human gates in `/bq-auto`: 12 → 17 (added VPS/Nginx/SSL change, paid service activation, secret/key handling, architecture change, deleting old impl with callers; clarified variant winner selection + release git ops as gates)
- Auto intent types: 0 (unscoped) → 17 (new/existing/feature/fix/uiux/frontend/backend/database/security/testing/devops/scraping/automation/deploy/live-edit/variants/release)
- Architecture docs: 1 → 4 (+3)

**Heavy-app status unchanged.**
- No reintroduction of Studio
- No reintroduction of CLI/TUI
- No local dashboard for BeQuite itself
- No Playwright auto-installed (tier-3 code-inspection fallback documented)
- No frontend libs / Docker / testing frameworks added by default

**Result:** v3.0.0-alpha.4 spec complete on disk. Skills registry detects all 15 skills + 36 commands. Auto-mode now scopes per intent; UI/UX variants + live edit available.

**Pending (user-gated, intentionally not auto-done):**
- Live verification in Claude Code against a fresh project
- Tag `v3.0.0-alpha.4` after live verification
- Installer scripts update to copy `.bequite/uiux/` templates + `.bequite/principles/TOOL_NEUTRALITY.md` (carried over from alpha.3)
- 20 alpha.1 commands still don't have the new template sections (Preconditions / Required gates / etc.) — out-of-scope this cycle

**Article VI honest reporting:**
- Skills + commands are structurally correct (YAML validates, SKILL.md format matches Anthropic spec, gate references consistent)
- Cross-references between commands (e.g. `/bq-auto uiux variants=N` → `/bq-uiux-variants N`) are documented but the dispatch logic is the agent's responsibility at run time, not a hard wired router
- Not live-tested in Claude Code against a real project — same caveat as alpha.2/alpha.3
- Browser-automation tier-1 (Playwright MCP) and tier-2 (project-local Playwright) are described in the live-edit skill; the actual MCP tool detection happens at runtime
- No `.bequite/uiux/` templates yet auto-installed in target projects; needs installer update

---

## 2026-05-11 — global correction (v3.0.0-alpha.3): tool neutrality principle

**Action:** User correction. Every tool, library, repo, framework, design system, workflow, or method named in BeQuite is an EXAMPLE, not a fixed mandatory choice. BeQuite must research the project first, choose tools second, justify every pick.

**Files created:**
- `.bequite/principles/TOOL_NEUTRALITY.md` — canonical source of truth (the rule, 10 questions, decision section format, do-not-auto-install defaults, research-depth rule)
- `docs/decisions/ADR-003-tool-neutrality.md` — formalizes the decision

**Files updated (11 skills):**
- bequite-researcher
- bequite-project-architect
- bequite-frontend-quality
- bequite-ux-ui-designer
- bequite-backend-architect
- bequite-database-architect
- bequite-security-reviewer
- bequite-testing-gate
- bequite-devops-cloud
- bequite-scraping-automation
- bequite-release-gate

Each gained a "Tool neutrality (global rule)" section at the end with: the rule, the 10 decision questions, the decision section format, and a project-specific reframing (e.g. "Drizzle is one candidate. Compare against Prisma, Kysely, raw SQL...").

**Files updated (8 commands):**
- /bq-research — research enables decisions, not commitments
- /bq-plan — §5 stack picks require decision sections, not bare names
- /bq-feature — new deps need decision sections in the mini-spec
- /bq-fix — fixes should rarely add tools; if they do, decision section required
- /bq-audit — recommendations are diagnostic, not prescriptive
- /bq-review — flag any "use X" claim without justification as BLOCKER
- /bq-red-team — adds 9th attack angle: tool choice
- /bq-verify — flags new deps in build lacking decision sections (warning, not blocker)

**Files updated (1 root):**
- CLAUDE.md — tool neutrality is now Core Operating Rule #1; 10 decision questions enumerated; do-not-auto-install added as Rule #12

**Result:** every BeQuite material now explicitly frames named tools as candidates. Concrete examples remain in body text for learning value; the tool-neutrality block at the end of each file makes the framing explicit. Canonical phrasing standardized: "X is one candidate. Research and compare against other options. Use it only if it fits this project."

**Heavy-app status unchanged.** No deletions. No new dependencies installed. No installer changes.

**Pending (user-gated):**
- Live verification in Claude Code
- Tag v3.0.0-alpha.3 after live verification
- Installer scripts update to copy `.bequite/principles/TOOL_NEUTRALITY.md` template into target projects (currently the rule lives in BeQuite's own repo; needs propagation to target installs)
- Future pass to rewrite inline "use X" language across the body of skills/commands (currently the rule is enforced via the block at the end; body text is unchanged)

**Article VI honest reporting:**
- The tool-neutrality block is appended uniformly to all 11 skills + 8 commands; the existing body text still uses some "default X" phrasing in places. The block at the end overrides, but a future pass should rewrite inline language for full consistency.
- Installer scripts have NOT been updated to copy `.bequite/principles/TOOL_NEUTRALITY.md` into target projects. Follow-up task.

---

## 2026-05-11 — direction reset Cycle 2 (v3.0.0-alpha.2): mandatory workflow gates + modes + orchestrators + specialist skills

**Action:** second major direction reset on top of v3.0.0-alpha.1. The brief required BeQuite to **prevent skipping important steps** and force the AI to think like a senior product engineer, architect, researcher, designer, security reviewer, and DevOps engineer before implementation. The alpha.1 spec was advisory only. This cycle introduces enforcement.

**Files created (this cycle):**
- `.bequite/state/WORKFLOW_GATES.md` — gate ledger (23 gates across P0-P5)
- `.bequite/state/CURRENT_MODE.md` — 6-mode selector
- `.claude/commands/bq-mode.md` — mode selector command
- `.claude/commands/bq-new.md` — New Project workflow entry
- `.claude/commands/bq-existing.md` — Existing Project Audit workflow entry
- `.claude/commands/bq-feature.md` — Add Feature workflow with 12-type router
- `.claude/commands/bq-auto.md` — autonomous full-cycle runner with 12 hard human gates
- `.claude/commands/bq-p0.md` through `.claude/commands/bq-p5.md` — six phase orchestrators
- `.claude/skills/bequite-researcher/SKILL.md` — 11-dimension verified evidence
- `.claude/skills/bequite-product-strategist/SKILL.md` — JTBD + persona + MVP
- `.claude/skills/bequite-ux-ui-designer/SKILL.md` — 10 principles + 15 anti-patterns
- `.claude/skills/bequite-backend-architect/SKILL.md` — API + async + caching
- `.claude/skills/bequite-database-architect/SKILL.md` — schema + migrations + indexing
- `.claude/skills/bequite-security-reviewer/SKILL.md` — OWASP + supply-chain
- `.claude/skills/bequite-devops-cloud/SKILL.md` — CI/CD + deploys + safety
- `docs/decisions/ADR-002-mandatory-workflow-gates.md`
- `docs/specs/COMMAND_CATALOG.md`

**Files rewritten (this cycle):**
- `.bequite/audits/DIRECTION_RESET_AUDIT.md` (Cycle 2 appended)
- `.bequite/state/CURRENT_PHASE.md` (updated to 6 phases with orchestrators)
- `.claude/commands/bequite.md` (now gate-aware; reads WORKFLOW_GATES.md, blocks out-of-order recommendations)
- `.claude/commands/bq-research.md` (11 dimensions vs the alpha.1 single-dimension freshness probe)
- `.claude/commands/bq-plan.md` (15 sections; multi-skill activation; quality gate)
- `.claude/commands/bq-multi-plan.md` (unbiased external prompts — explicit no-mention-of-Claude protocol)
- `.claude/commands/bq-fix.md` (15-type problem router; skill activation per type)
- `CLAUDE.md` (reflects 34 commands, 14 skills, gates, modes, hard human gates)

**Tally:**
- Commands: 24 → 34 (+10)
- Skills: 7 → 14 (+7)
- Workflow gates: 0 → 23
- Hard human gates in /bq-auto: 0 → 12
- Modes: implicit → 6 explicit
- Phase orchestrators: 0 → 7 (`/bq-p0` through `/bq-p5` + `/bq-auto`)
- ADRs added: 1 (ADR-002)

**Heavy-app status unchanged (still paused):**
- `studio/`, `docker-compose.yml`, `tests/e2e/`, `cli/` — all paused per Cycle 1 audit; no deletion

**Result:** v3.0.0-alpha.2 spec complete on disk. Skills registry detects all 14 skills + all 34 commands. Ready for live verification inside Claude Code.

**Pending (user-gated, not auto-tagged):**
- Live verification: paste `/bequite` into Claude Code against a fresh project; confirm gate-aware menu renders + blocks out-of-order commands
- Tag `v3.0.0-alpha.2` after live verification
- Decision: continue extending existing 24 commands with full Preconditions / Required gates / Quality gate / Failure behavior sections, OR defer to alpha.3
- Decision: write remaining architecture docs (WORKFLOW_GATES.md narrative, RESEARCH_DEPTH_STRATEGY.md, FEATURE_AND_FIX_WORKFLOWS.md, DEVOPS_CLOUD_SAFETY.md) — currently they live inline within commands + skills

**Article VI honest reporting:**
- I have NOT live-tested `/bequite` inside Claude Code against the new gate-aware behavior. Skills + commands are structurally correct (YAML frontmatter validates, Anthropic Skills SKILL.md format matches, gate references are consistent across commands), but actual command-dispatch behavior is unverified.
- The 24 alpha.1 commands have NOT been retroactively updated with the new `Preconditions` / `Required previous gates` / `Quality gate` sections — only the 4 rewritten commands (research, plan, multi-plan, fix) and 10 new commands have the full template. The other 20 still work but their gate references are advisory until updated.
- I have NOT verified the installer scripts copy the new 7 skills + 10 commands + state file templates. They likely need an update; that's a follow-up.

---

## 2026-05-11 — direction reset to lightweight skill pack

**Action:** reset BeQuite from "heavy app" direction (Studio dashboard + Docker + multi-app) to lightweight project skill pack.

**Files created:**
- `.bequite/audits/DIRECTION_RESET_AUDIT.md` — full keep/pause/delete-later inventory
- `.claude/commands/bequite.md` + 23 `bq-*.md` files (24 total slash commands)
- `.claude/skills/bequite-project-architect/SKILL.md`
- `.claude/skills/bequite-problem-solver/SKILL.md`
- `.claude/skills/bequite-frontend-quality/SKILL.md`
- `.claude/skills/bequite-testing-gate/SKILL.md`
- `.claude/skills/bequite-release-gate/SKILL.md`
- `.claude/skills/bequite-scraping-automation/SKILL.md`
- `.claude/skills/bequite-multi-model-planning/SKILL.md`
- `.bequite/state/{PROJECT_STATE,CURRENT_PHASE,LAST_RUN,DECISIONS,OPEN_QUESTIONS}.md`
- `.bequite/logs/{AGENT_LOG,CHANGELOG,ERROR_LOG}.md`
- `.bequite/prompts/{user_prompts,generated_prompts,model_outputs}/.gitkeep`
- `.bequite/plans/.gitkeep`
- `.bequite/tasks/.gitkeep`

**Files paused (not deleted, per DIRECTION_RESET_AUDIT):**
- `studio/` (marketing + dashboard + api + brand)
- `docker-compose.yml`, `.dockerignore`
- `studio/*/Dockerfile`, `studio/*/.dockerignore`
- `tests/e2e/`
- `scripts/docker-up.{ps1,sh}`
- Root `package.json` + `Makefile`

**Result:** SUCCESS — lightweight skill pack structure complete. Ready for live verification inside Claude Code.

**Commits this cycle:**
- 215ed75 — direction reset audit + 5 Phase-0 commands
- 801b893 — 19 more commands (Phases 1-5)
- (this commit) — skills + memory scaffold + installer + docs + ADR-001

**Next:** user reviews + tests `/bequite` in a fresh Claude Code session against a sample project.

---

## (older entries preserved at `.bequite/memory/progress.md` and `docs/changelogs/AGENT_LOG.md`)

For BeQuite's pre-reset history (Studio v2.0.0-alpha.6 audit cycle), see `docs/changelogs/AGENT_LOG.md`.
