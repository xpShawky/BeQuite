# Project state

**Initialized:** 2026-05-11
**Project type:** BeQuite itself (this repo is the source of the skill pack)
**Stack detected:** Python CLI (`cli/`) + paused Studio (`studio/`) + lightweight skill pack (`.claude/`)
**Repository:** https://github.com/xpShawky/BeQuite

## Project summary

BeQuite is a lightweight Claude Code skill pack you install into any project to give the coding agent a reliable workflow. v3.0.0 direction: lightweight skill pack first; heavy Studio app paused.

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
