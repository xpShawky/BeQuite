# Project changelog

Tracked by BeQuite. Use `/bq-changelog` to add entries. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- v3.0.0-alpha.1 direction: BeQuite is now a lightweight project skill pack at `.claude/commands/` + `.claude/skills/` + `.bequite/` memory.
- 24 slash commands: `/bequite` (root menu) + 23 `/bq-*` workflow commands across 5 phases.
- 7 focused skills: project-architect, problem-solver, frontend-quality, testing-gate, release-gate, scraping-automation, multi-model-planning.
- Lightweight installer scripts (planned in this cycle).
- ADR-001: lightweight-skill-pack-first.

### Changed
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
