# CLAUDE.md

Claude-Code-specific operating instructions for the **BeQuite** repository.

Read this on every session start.

---

## What this repo is

BeQuite is a **lightweight Claude Code skill pack** you install into any project. v3.0.0+ direction (per `docs/decisions/ADR-001-lightweight-skill-pack-first.md`).

This repo IS the source of the skill pack. Its `.claude/commands/` + `.claude/skills/` are the files that get copied into target projects by `scripts/install-bequite.{ps1,sh}`.

**Direction:** lightweight only. No Studio. No heavy CLI / TUI. No localhost dashboard. No Docker. No frontend / API / database / 3D required by default (ADR-004).

---

## Current spec: v3.0.0-alpha.7

- **39 slash commands** (`.claude/commands/bequite.md` + 38 × `.claude/commands/bq-*.md`)
- **15 skills** (`.claude/skills/bequite-*/SKILL.md`)
- **6 explicit modes** — New Project, Existing Audit, Add Feature, Fix Problem, Research Only, Release Readiness
- **6 workflow phases** — P0 Setup → P1 Framing → P2 Build → P3 Quality → P4 Release → P5 Memory
- **23 workflow gates** tracked in `.bequite/state/WORKFLOW_GATES.md` (block out-of-order commands)
- **Phase orchestrators** — `/bq-p0` … `/bq-p5` walk a single phase end-to-end
- **Scoped autonomous runner** — `/bq-auto [intent] [--mode fast|deep|token-saver] "task"` parses 17 intent types; pauses only at hard human gates
- **UI/UX variants** — `/bq-uiux-variants [N] "task"` generates 1-10 isolated design directions
- **Live edit** — `/bq-live-edit "task"` section-by-section frontend edits with section mapping
- **Mistake memory** — wired into 7 commands (fix / audit / review / red-team / verify / auto / live-edit); writes to `.bequite/state/MISTAKE_MEMORY.md`
- **Quick orientation** — `/bq-now` returns one-line status (faster than `/bequite`)
- **Spec Kit interop** — `/bq-spec "<feature>"` writes one-page `specs/<slug>/spec.md`
- **Plain-English explainer** — `/bq-explain "<target>"` for files / functions / decisions / artifacts
- **Public command reference** — `commands.md` at repo root

---

## Where things live

| Need | Path |
|---|---|
| Slash commands (39) | `.claude/commands/bequite.md` + `.claude/commands/bq-*.md` |
| Skills (15) | `.claude/skills/bequite-*/SKILL.md` |
| Public command reference | `commands.md` (repo root) |
| BeQuite memory | `.bequite/` |
| Workflow gate ledger | `.bequite/state/WORKFLOW_GATES.md` |
| Mode selector | `.bequite/state/CURRENT_MODE.md` |
| Phase selector | `.bequite/state/CURRENT_PHASE.md` |
| Project's own Memory Bank | `.bequite/memory/` (v2.x history, internal) |
| Direction reset audit (Cycle 1+2) | `.bequite/audits/DIRECTION_RESET_AUDIT.md` |
| GitHub-ready cleanup audit | `.bequite/audits/GITHUB_READY_CLEANUP_AUDIT.md` |
| Mistake memory | `.bequite/state/MISTAKE_MEMORY.md` |
| Assumptions | `.bequite/state/ASSUMPTIONS.md` |
| Feature expansion roadmap | `.bequite/plans/FEATURE_EXPANSION_ROADMAP.md` |
| Original brief | `BEQUITE_BOOTSTRAP_BRIEF.md` |
| Master file | `BeQuite_MASTER_PROJECT.md` |
| Install scripts | `scripts/install-bequite.{ps1,sh}` |
| ADR-001 (lightweight) | `docs/decisions/ADR-001-lightweight-skill-pack-first.md` |
| ADR-002 (mandatory gates) | `docs/decisions/ADR-002-mandatory-workflow-gates.md` |
| ADR-003 (tool neutrality) | `docs/decisions/ADR-003-tool-neutrality.md` |
| Auto-mode strategy | `docs/architecture/AUTO_MODE_STRATEGY.md` |
| UI/UX variants strategy | `docs/architecture/UIUX_VARIANTS_STRATEGY.md` |
| Live edit strategy | `docs/architecture/LIVE_EDIT_STRATEGY.md` |
| Tool neutrality principle | `.bequite/principles/TOOL_NEUTRALITY.md` |
| UI/UX memory | `.bequite/uiux/` (SECTION_MAP, LIVE_EDIT_LOG, UIUX_VARIANTS_REPORT, selected-variant, screenshots/) |
| Command catalog | `docs/specs/COMMAND_CATALOG.md` |
| Heavy-app ADRs (paused) | `.bequite/memory/decisions/ADR-008..016` |

---

## Core operating rules

1. **Tool neutrality.** Named tools are EXAMPLES, not commands. BeQuite must research, compare, justify, and choose the best tool for the current project instead of blindly using any named tool. See `.bequite/principles/TOOL_NEUTRALITY.md`.
2. **Never claim a task is "done" unless `/bq-verify` passes.**
3. **Always update `.bequite/logs/AGENT_LOG.md` when you take a real action.**
4. **Always update `.bequite/state/CURRENT_PHASE.md` when the workflow phase changes.**
5. **Always update `.bequite/state/WORKFLOW_GATES.md` when a gate is met.**
6. **Banned weasel words in completion reports:** should, probably, seems to, appears to, I think it works, might, hopefully, in theory. Replace with concrete verification or admit you didn't verify.
7. **Iron Law X:** every change ships in operationally complete state. No "feature added but needs restart."
8. **PhantomRaven defense:** never import a package without verifying it exists in the relevant registry in this session.
9. **Read before editing.** Use Read / Glob / Grep first; Edit only after.
10. **Inspect before assuming.** The `bequite-problem-solver` skill's "reproduce-first" discipline applies to every bug.
11. **No out-of-order commands.** If a command's required gates aren't met, refuse and suggest the prerequisite command.
12. **Do not auto-install dependencies.** No new deps, scraping tools, frontend libs, Docker, testing frameworks, deploy tools, monitoring, or auth libs added by default. Only when justified per the 10 decision questions.

### The 10 decision questions (apply before any major tool pick)

1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

**Do not say:** "Use X."
**Say:** "X is one candidate. Research and compare against other options. Use it only if it fits this project."

For each major pick: write a decision section (short for small projects; full ADR at `.bequite/decisions/ADR-XXX-<tool>-choice.md` for large / regulated projects). Format: Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan.

---

## The 6 modes

| Mode | Entry command | When to use |
|---|---|---|
| New Project | `/bq-new` | Empty folder, starting from scratch |
| Existing Project Audit | `/bq-existing` | Existing repo, audit what's there |
| Add Feature | `/bq-feature "title"` | Add one feature to existing project |
| Fix Problem | `/bq-fix` | Diagnose + repair a bug |
| Research Only | `/bq-mode research-only` | Just research; no code |
| Release Readiness | `/bq-mode release` | Pre-release verification + audit |

Active mode lives in `.bequite/state/CURRENT_MODE.md`.

---

## The 6 phases

| Phase | Name | Commands | Goal |
|---|---|---|---|
| P0 | Setup and Discovery | `/bq-init`, `/bq-mode`, `/bq-discover`, `/bq-doctor` | Learn what's there |
| P1 | Product Framing and Research | `/bq-clarify`, `/bq-research`, `/bq-scope`, `/bq-plan`, `/bq-multi-plan` | Decide what to build |
| P2 | Planning and Build | `/bq-assign`, `/bq-implement`, `/bq-feature`, `/bq-fix` | Build it |
| P3 | Quality and Review | `/bq-test`, `/bq-audit`, `/bq-review`, `/bq-red-team` | Confirm it works |
| P4 | Release | `/bq-verify`, `/bq-release`, `/bq-changelog` | Ship |
| P5 | Memory and Handoff | `/bq-memory`, `/bq-recover`, `/bq-handoff` | Continue / hand off |

Phase orchestrators: `/bq-p0` through `/bq-p5` (walk one phase in order). Autonomous: `/bq-auto` (walks all phases, pauses at hard gates).

---

## The 14 skills

7 baseline (existing):
- `bequite-frontend-quality` — UI quality + AI-slop detection
- `bequite-multi-model-planning` — manual-paste multi-model collaboration
- `bequite-problem-solver` — reproduce-first diagnostics
- `bequite-project-architect` — stack + ADR + scale-tier procedures
- `bequite-release-gate` — CI parity + semver + signing
- `bequite-scraping-automation` — Article VIII + polite mode
- `bequite-testing-gate` — test pyramid + coverage targets

7 specialist (new in v3.0.0-alpha.2):
- `bequite-researcher` — 11-dimension verified evidence
- `bequite-product-strategist` — JTBD + persona + MVP scoping
- `bequite-ux-ui-designer` — design principles + AI-slop anti-patterns
- `bequite-backend-architect` — API + async + caching + observability
- `bequite-database-architect` — schema + migrations + indexing
- `bequite-security-reviewer` — OWASP + supply-chain + secrets
- `bequite-devops-cloud` — CI/CD + deploys + safety gates

1 frontend live-edit (new in v3.0.0-alpha.4):
- `bequite-live-edit` — section-mapped frontend edits + browser inspection tiers

---

## Quick commands

```
/bequite                                    → gate-aware menu + recommended next 3
/bq-help                                    → full command reference
/bq-init                                    → initialize
/bq-mode                                    → select / show workflow mode
/bq-auto [intent] "task"                    → scoped autonomous runner (17 intents)
/bq-uiux-variants [N] "task"                → 1-10 isolated UI directions
/bq-live-edit "task"                        → section-by-section frontend edits
/bq-p0..p5                                  → walk one phase in order
/bq-verify                                  → full local verification
/bq-recover                                 → resume after session break
```

### `/bq-auto` intent types (17)

`new | existing | feature | fix | uiux | frontend | backend | database | security | testing | devops | scraping | automation | deploy | live-edit | variants | release`

Auto-mode continues by default — does NOT pause for "should I continue?" or "approve the plan?" Pauses only at hard human gates (see below).

For everything else, run `/bq-help` or `/bequite`.

---

## Required reads on every session start

(In order)

1. This `CLAUDE.md`
2. `.bequite/state/PROJECT_STATE.md`
3. `.bequite/state/CURRENT_MODE.md`
4. `.bequite/state/CURRENT_PHASE.md`
5. `.bequite/state/WORKFLOW_GATES.md`
6. `.bequite/state/LAST_RUN.md`
7. `.bequite/state/OPEN_QUESTIONS.md`
8. `.bequite/state/DECISIONS.md`
9. `.bequite/logs/AGENT_LOG.md` (last 5 entries)

If any of those are missing, run `/bq-init` first.

---

## Hard human gates (the only places /bq-auto pauses) — v3.0.0-alpha.4

Even in autonomous mode, the agent MUST pause for explicit user confirmation at:

1. **Destructive file deletion** (`rm -rf` on tracked code)
2. **Database migration against shared / production DBs**
3. **Production server change** (SSH, systemd, firewall on prod)
4. **VPS / Nginx / SSL change**
5. **Paid service activation** (new SaaS signup with payment)
6. **Secret / key handling** (rotation, generation)
7. **Changing auth / security model**
8. **Changing project architecture**
9. **Deleting old implementation** with active callers
10. **Scope contradiction** (task contradicts locked SCOPE.md)
11. **User explicit manual-approval** (`--manual-approval` or "stop and ask me")
12. **Cost ceiling reached**
13. **Wall-clock ceiling reached**
14. **Banned-weasel-word trip**
15. **3 consecutive failures on the same task**
16. **UI variant winner selection** (after `/bq-uiux-variants` finishes)
17. **Release `git push` / `git tag`** (always user-run)

Auto-mode does NOT pause after plan / scope / clarify if the intent is scoped — it continues autonomously per AUTO_MODE_STRATEGY.md.

---

## Doctrines that may be active

Per the project's `.bequite/state/DECISIONS.md`. Common ones:

- `default-web-saas` — UI rules (no Inter without recorded reason; tokens.css required; axe-core gate)
- `cli-tool` — semver discipline, exit codes, completions
- `ml-pipeline` — reproducible training, dataset versioning
- `desktop-tauri` — OS keychain (not Stronghold), notarytool, AzureSignTool
- `library-package` — public API freeze, semver-strict
- `fintech-pci` / `healthcare-hipaa` / `gov-fedramp` — regulated
- `ai-automation` — n8n / Make / Zapier discipline
- `mena-bilingual` — Arabic + RTL
- `mena-pdpl` / `eu-gdpr` — privacy compliance
- `vibe-defense` — extra-strict for vibe-handoff audience

The active Doctrine(s) are declared in `.bequite/state/DECISIONS.md`. If none declared, default to `default-web-saas` for web projects.

---

## When in doubt

- Iron Law beats Doctrine
- Doctrine beats convention
- Latest-verified-research beats memory
- Active session evidence beats memory of a previous run
- Run `/bequite` for orientation
- Refuse to run commands whose required gates aren't met

---

## History

BeQuite went through a v0.1.0 → v2.0.0-alpha.6 heavy-direction lineage (Studio + Docker + multi-app). That direction is **retired** (ADR-004 — "no heavy Studio or CLI in the GitHub-facing project"). Git history retains the heavy assets; the active main branch is lightweight-only.

The current MVP path is v3.0.0+ (lightweight command + skill pack with mandatory gates + tool neutrality). See ADR-001 (lightweight skill pack first), ADR-002 (mandatory workflow gates), ADR-003 (tool neutrality), ADR-004 (no heavy Studio or CLI).
