# CLAUDE.md

Claude-Code-specific operating instructions for the **BeQuite** repository.

Read this on every session start.

---

## What this repo is

BeQuite is a **lightweight Claude Code skill pack** you install into any project. v3.0.0+ direction (per `docs/decisions/ADR-001-lightweight-skill-pack-first.md`).

This repo IS the source of the skill pack. Its `.claude/commands/` + `.claude/skills/` are the files that get copied into target projects by `scripts/install-bequite.{ps1,sh}`.

The heavy `studio/` directory (Next.js marketing + dashboard + Hono API + Docker compose) is **paused, not deleted** — see `.bequite/audits/DIRECTION_RESET_AUDIT.md`.

---

## Where things live

| Need | Path |
|---|---|
| Slash commands (24) | `.claude/commands/bequite.md` + `.claude/commands/bq-*.md` |
| Skills (7) | `.claude/skills/bequite-*/SKILL.md` |
| BeQuite memory | `.bequite/` |
| Project's own Memory Bank | `.bequite/memory/` (the v2.x and earlier history) |
| Paused Studio | `studio/` |
| Paused Docker | `docker-compose.yml`, `Dockerfile` (in each studio app), `.dockerignore` |
| Paused e2e tests | `tests/e2e/` |
| Python CLI (optional supplemental) | `cli/` |
| Original brief | `BEQUITE_BOOTSTRAP_BRIEF.md` |
| Master file | `BeQuite_MASTER_PROJECT.md` |
| Lightweight install scripts | `scripts/install-bequite.{ps1,sh}` |
| Lightweight ADR | `docs/decisions/ADR-001-lightweight-skill-pack-first.md` |
| Heavy-app ADRs (paused) | `.bequite/memory/decisions/ADR-008..016` |

---

## Core operating rules

1. **Never claim a task is "done" unless `/bq-verify` passes.**
2. **Always update `.bequite/logs/AGENT_LOG.md` when you take a real action.**
3. **Always update `.bequite/state/CURRENT_PHASE.md` when the workflow phase changes.**
4. **Banned weasel words in completion reports:** should, probably, seems to, appears to, I think it works, might, hopefully, in theory. Replace with concrete verification or admit you didn't verify.
5. **Iron Law X:** every change ships in operationally complete state. No "feature added but needs restart."
6. **PhantomRaven defense:** never import a package without verifying it exists in the relevant registry in this session.
7. **Read before editing.** Use Read / Glob / Grep first; Edit only after.
8. **Inspect before assuming.** The `bequite-problem-solver` skill's "reproduce-first" discipline applies to every bug.

---

## Quick commands

```
/bequite              → menu + recommended next 3
/bq-help              → full reference
/bq-init              → initialize (writes baseline state files)
/bq-doctor            → environment health
/bq-plan              → write a real implementation plan (no code yet)
/bq-implement         → workhorse — one approved task at a time
/bq-verify            → full local verification before shipping
/bq-recover           → resume after a session break
```

For everything else, run `/bq-help` to see all 24 commands grouped by workflow phase.

---

## Required reads on every session start

(In order)

1. This `CLAUDE.md`
2. `.bequite/state/PROJECT_STATE.md`
3. `.bequite/state/CURRENT_PHASE.md`
4. `.bequite/state/LAST_RUN.md`
5. `.bequite/state/OPEN_QUESTIONS.md`
6. `.bequite/state/DECISIONS.md`
7. `.bequite/logs/AGENT_LOG.md` (last 5 entries)

If any of those are missing, run `/bq-init` first.

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

---

## Two-track history

This repo has gone through two design tracks. Both are preserved:

- **v0.1.0 → v2.0.0-alpha.6 (paused):** the heavy app — Studio + Docker + multi-app. See `CHANGELOG.md`, ADR-008..016, `studio/`.
- **v3.0.0+ (current):** the lightweight skill pack. See ADR-001, `.claude/`, `.bequite/`.

The two tracks can coexist on disk. Track 1 is paused; track 2 is the current MVP path.
