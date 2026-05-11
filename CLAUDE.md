# CLAUDE.md

Claude-Code-specific operating instructions for the **BeQuite** repository.

Read this on every session start.

---

## What this repo is

BeQuite is a **lightweight Claude Code skill pack** you install into any project. v3.0.0+ direction (per `docs/decisions/ADR-001-lightweight-skill-pack-first.md`).

This repo IS the source of the skill pack. Its `.claude/commands/` + `.claude/skills/` are the files that get copied into target projects by `scripts/install-bequite.{ps1,sh}`.

The heavy `studio/` directory (Next.js marketing + dashboard + Hono API + Docker compose) and Python CLI are **paused, not deleted** — see `.bequite/audits/DIRECTION_RESET_AUDIT.md` (Cycle 2).

---

## Current spec: v3.0.0-alpha.2

- **34 slash commands** (`.claude/commands/bequite.md` + 33 × `.claude/commands/bq-*.md`)
- **14 skills** (`.claude/skills/bequite-*/SKILL.md`)
- **6 explicit modes** — New Project, Existing Audit, Add Feature, Fix Problem, Research Only, Release Readiness
- **6 workflow phases** — P0 Setup → P1 Framing → P2 Build → P3 Quality → P4 Release → P5 Memory
- **23 workflow gates** tracked in `.bequite/state/WORKFLOW_GATES.md` (block out-of-order commands)
- **Phase orchestrators** — `/bq-p0` … `/bq-p5` walk a single phase end-to-end
- **Autonomous runner** — `/bq-auto` walks ALL phases, pausing only at hard human gates

---

## Where things live

| Need | Path |
|---|---|
| Slash commands (34) | `.claude/commands/bequite.md` + `.claude/commands/bq-*.md` |
| Skills (14) | `.claude/skills/bequite-*/SKILL.md` |
| BeQuite memory | `.bequite/` |
| Workflow gate ledger | `.bequite/state/WORKFLOW_GATES.md` |
| Mode selector | `.bequite/state/CURRENT_MODE.md` |
| Phase selector | `.bequite/state/CURRENT_PHASE.md` |
| Project's own Memory Bank | `.bequite/memory/` (v2.x history) |
| Direction reset audit | `.bequite/audits/DIRECTION_RESET_AUDIT.md` |
| Paused Studio | `studio/` |
| Paused Docker | `docker-compose.yml`, `Dockerfile`, `.dockerignore` |
| Paused e2e tests | `tests/e2e/` |
| Paused Python CLI | `cli/` |
| Original brief | `BEQUITE_BOOTSTRAP_BRIEF.md` |
| Master file | `BeQuite_MASTER_PROJECT.md` |
| Install scripts | `scripts/install-bequite.{ps1,sh}` |
| ADR-001 (lightweight) | `docs/decisions/ADR-001-lightweight-skill-pack-first.md` |
| ADR-002 (mandatory gates) | `docs/decisions/ADR-002-mandatory-workflow-gates.md` |
| Command catalog | `docs/specs/COMMAND_CATALOG.md` |
| Heavy-app ADRs (paused) | `.bequite/memory/decisions/ADR-008..016` |

---

## Core operating rules

1. **Never claim a task is "done" unless `/bq-verify` passes.**
2. **Always update `.bequite/logs/AGENT_LOG.md` when you take a real action.**
3. **Always update `.bequite/state/CURRENT_PHASE.md` when the workflow phase changes.**
4. **Always update `.bequite/state/WORKFLOW_GATES.md` when a gate is met.**
5. **Banned weasel words in completion reports:** should, probably, seems to, appears to, I think it works, might, hopefully, in theory. Replace with concrete verification or admit you didn't verify.
6. **Iron Law X:** every change ships in operationally complete state. No "feature added but needs restart."
7. **PhantomRaven defense:** never import a package without verifying it exists in the relevant registry in this session.
8. **Read before editing.** Use Read / Glob / Grep first; Edit only after.
9. **Inspect before assuming.** The `bequite-problem-solver` skill's "reproduce-first" discipline applies to every bug.
10. **No out-of-order commands.** If a command's required gates aren't met, refuse and suggest the prerequisite command.

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

---

## Quick commands

```
/bequite              → gate-aware menu + recommended next 3
/bq-help              → full command reference
/bq-init              → initialize (writes baseline state files)
/bq-mode              → select / show the workflow mode
/bq-p0                → run Phase 0 in one pass
/bq-auto              → walk all phases, pause at hard gates
/bq-verify            → full local verification before shipping
/bq-recover           → resume after a session break
```

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

## Hard human gates (the only places /bq-auto pauses)

Even in autonomous mode, the agent MUST pause for explicit user confirmation at:

1. Mode selection
2. Clarify answers
3. Scope approval
4. Multi-model planning decision (yes/no)
5. Implementation plan approval
6. Release approval (`git push`, `git tag`)
7. Destructive operations (`rm -rf`, `terraform destroy`, etc.)
8. Database migrations against shared / production DBs
9. Server / VPS configuration changes
10. Cost ceiling reached
11. Banned-weasel-word trip
12. 3 consecutive task failures

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

## Two-track history

This repo has gone through two design tracks. Both are preserved:

- **v0.1.0 → v2.0.0-alpha.6 (paused):** the heavy app — Studio + Docker + multi-app. See `CHANGELOG.md`, ADR-008..016, `studio/`.
- **v3.0.0+ (current):** the lightweight skill pack with mandatory gates. See ADR-001, ADR-002, `.claude/`, `.bequite/`.

The two tracks can coexist on disk. Track 1 is paused; track 2 is the current MVP path.
