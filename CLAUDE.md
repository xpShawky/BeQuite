# CLAUDE.md

Operating instructions for working **on the BeQuite repository** (the source of the pack). Read on every session start. Keep this file lean: detail lives in skills and `.claude/bequite/docs/`.

## What this repo is

BeQuite is a lightweight workflow pack for Claude Code (and other agents): slash commands, skills, a `.bequite/` memory scaffold, gates and evidence rules, all markdown. Current version: **v4.0.0 "Titan"**. Direction: lightweight only. No Studio, no heavy CLI/TUI, no dashboard, no Docker, no database (ADR-001, ADR-004).

## Layout

| Path | What it is | Ships to user projects |
|---|---|---|
| `.claude/commands/` | 55 active commands + 7 deprecated redirects (catalog IDs in `templates/bequite/commands/COMMAND_ID_MAP.md`) | yes |
| `.claude/skills/bequite-*/` | 35 skills (registry: `templates/bequite/skills/SKILL_REGISTRY.md`) | yes |
| `.claude/bequite/docs/` | reference docs commands cite: `architecture/`, `specs/`, `decisions/` (ADRs), `runbooks/` | yes |
| `.claude/hooks/`, `.claude/settings*.json.example` | opt-in safety hooks (never active by default) | yes |
| `templates/bequite/` | the clean `.bequite/` scaffold (incl. `work/_template/`) | yes, never overwriting |
| `templates/CLAUDE.bequite.md` | the BeQuite block both installers write into a project's CLAUDE.md | yes |
| `scripts/install-bequite.{ps1,sh}` | installers | entry point |
| `scripts/bq_check.py` | self-check: rules as failing checks (CI runs it) | no |
| `motion-library/` | studied reference films for `/bq-motion` (media gitignored; breakdowns tracked) | no |
| `commands.md`, `README.md`, `CHANGELOG.md`, `AGENTS.md` | public docs | `commands.md` yes |
| `.bequite/` | **this repo's own working memory, local only (gitignored)**; Titan plan + research live there | no |

## Rules for changing the pack

1. **Run `python3 scripts/bq_check.py` before every commit** and keep it green. It checks installer safety, frontmatter, references, counts, the contract block and gate names.
2. **Installers:** `install-bequite.ps1` must stay pure ASCII, no BOM, no `param()` / `CmdletBinding`, no `exit` (it runs through `irm | iex`). Never write it with `utf-8-sig` or PowerShell's default encoding. Test both installers end to end (bash, and PowerShell via `[Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes(...)) | iex`) when they change.
3. **Every action command carries the standard contract block.** Don't hand-edit it; change it in `bq_check.py` and run `python3 scripts/bq_check.py --fix contract`.
4. **Memory paths:** per-work artifacts live in `.bequite/work/<id>/` (spec: `.claude/bequite/docs/architecture/WORK_FOLDERS.md`). Never point a command at the old flat files (`SCOPE.md`, `IMPLEMENTATION_PLAN.md`, `TASK_LIST.md`, `VERIFY_REPORT.md`).
5. **New gate?** Add it to `templates/bequite/state/WORKFLOW_GATES.md` (project) or `templates/bequite/work/_template/gates.md` (work) first.
6. **New command or skill:** justify the shape (command vs argument vs skill, `FEATURE_TYPE_TAXONOMY.md`), then update in the same commit: `COMMAND_ID_MAP.md` / `SKILL_REGISTRY.md` / `SKILL_ROUTER.md`, `ORCHESTRATION_MAP.md`, `commands.md`, `README.md`, `/bq-help`, the `/bequite` menu, and `CHANGELOG.md`.
7. **Never commit third-party media** (reference films, frames, audio). `.gitignore` covers `motion-library/`.
8. **Releases:** a `v*.*.*` tag runs `bq_check` and creates a GitHub Release from `CHANGELOG.md`. Tags and pushes to a release are the owner's decision; ask first.

## Core operating rules

1. **Tool neutrality.** Named tools are examples. Research, compare and justify with the 10 decision questions below.
2. **Plan first.** Non-trivial work: research (the web when no reference is given) → plan → approval → output.
3. **Skills first.** Announce the `Skill Selection:` block before acting on any command.
4. **Evidence over claims.** No "done" without command + exit code + output; otherwise `UNVERIFIED:`. Banned in completion reports: should, probably, seems to, appears to, I think it works, might, hopefully, in theory.
5. **Verify each phase** before starting the next; failures go to `/bq-fix`.
6. **Write back** after real actions: `AGENT_LOG`, `LAST_RUN`, the work `log.md`, `MISTAKE_MEMORY` when a lesson surfaced, and `CHANGELOG.md` when behaviour changed.
7. **Iron Law X:** every change ships operationally complete.
8. **PhantomRaven defense:** never add a package without verifying it in its registry in this session.
9. **Read before editing; reproduce before fixing.**
10. **No out-of-order commands.** Missing gate → refuse and name the prerequisite.
11. **No auto-installed dependencies** (scraping tools, frontend libs, Docker, test frameworks, deploy or auth libs) without the 10 decision questions.
12. **Frontend quality promise:** every visible section meets the Design DNA; motion pages pass the performance budget (`bequite-frontend-design-system`, `references/web-motion.md`).
13. **Models:** BeQuite recommends a model per task; it never switches models. Report the model actually running.
14. **BeQuite eats its own food:** when discipline drifts, audit before adding features.

### The 10 decision questions

1. What is the project type? 2. What is the actual problem? 3. What scale is expected? 4. What constraints exist? 5. What stack already exists? 6. What user experience is required? 7. What failure risks exist? 8. What tools are proven for this case? 9. What tools are overkill? 10. What gives the best output with the least complexity?

Don't say "Use X." Say "X is one candidate; compare it with the alternatives and use it only if it fits."

## Hard human gates

Even in auto mode, stop for an explicit yes before: destructive deletion · migrations on shared/production DBs · production server, VPS, Nginx or SSL changes · paid services or paid credits · secret/key handling · auth or security model changes · architecture changes · deleting implementations with live callers · scope contradictions · explicit manual-approval requests · cost or time ceilings · banned-word trips · 3 consecutive failures · UI variant winner selection · release push/tag · and, for creative work, the script, style and render plan (`/bq-motion` M2-M4).

## History

v0.1 → v2.0.0-alpha.6 was a heavy direction (Studio, Docker, CLI), retired by ADR-004; it lives on the `archive/v2` branch. v3 alphas built the lightweight pack. v4 "Titan" added work folders, enforcement, the motion studio, web motion and clean installs. See `CHANGELOG.md`.
