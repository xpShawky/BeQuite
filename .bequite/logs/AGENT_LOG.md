# Agent log

Append-only chronicle of every BeQuite command run. Newest at top.

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
