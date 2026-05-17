# Project state

**Initialized:** 2026-05-11
**Last refreshed:** 2026-05-17 (alpha.14 audit)
**Project type:** BeQuite itself (this repo is the source of the skill pack)
**Active stack:** Lightweight Claude Code skill pack — markdown commands + skills + memory templates
**Paused on disk (per ADR-001 + ADR-004):** `cli/` (Python CLI), `studio/` (heavy direction), `docker-compose.yml`, `tests/e2e/`, `template/`, `evidence/`, `skill/`. Not active; retained for historical reference.
**Repository:** https://github.com/xpShawky/BeQuite

## Project summary

BeQuite is a lightweight Claude Code skill pack you install into any project to give the coding agent a reliable workflow. v3.0.0 direction (canonical): **lightweight skill pack only**. Heavy direction (Studio + Docker + Python CLI) retired per ADR-001 + ADR-004.

**Current spec:** v3.0.0-alpha.14 — discipline-restoration release after alpha.13's Presentation Builder shipped without following the full workflow. See `.bequite/audits/FULL_SYSTEM_ALIGNMENT_AUDIT.md`.

## What BeQuite tracks for this project

- `state/CURRENT_PHASE.md` — workflow phase (Phase 0 → Phase 5)
- `state/LAST_RUN.md` — most recent BeQuite command run + result
- `state/DECISIONS.md` — running list of decisions made
- `state/OPEN_QUESTIONS.md` — questions awaiting answers
- `logs/AGENT_LOG.md` — every command, append-only
- `audits/`, `plans/`, `tasks/`, `prompts/` — per-command artifacts

## Notes for other projects

This `PROJECT_STATE.md` is the TEMPLATE that `/bq-init` copies into your project. The /bq-init command overwrites the values above with your project's actual stack + summary.

If you're reading this in the BeQuite repo itself: this file describes BeQuite. The skill pack you install into YOUR project starts with a fresh PROJECT_STATE.md.
