# ADR-004 — No heavy Studio or CLI in the GitHub-facing project

**Status:** Accepted
**Date:** 2026-05-12
**Supersedes:** none (extends ADR-001)
**Superseded by:** none
**Related:** ADR-001 (lightweight skill pack first), ADR-002 (mandatory workflow gates), ADR-003 (tool neutrality)

---

## Context

After ADR-001 chose the lightweight skill-pack direction, the heavy assets (Studio Next.js app, Hono API, Python CLI, Docker compose, top-level template/, evidence/, skill/, state/ folders, root package.json + Makefile) remained on disk in a "paused, kept on disk" state.

That ambiguity created three real problems:

1. **The GitHub-facing repo looked bloated.** 484 tracked files; ~MB of code under `studio/` and `cli/` that wasn't part of the active direction.
2. **New users couldn't tell what was active.** README still mentioned the Python CLI as "optional supplemental." That implied the CLI was a real path; it was actually retired.
3. **Docs and CLAUDE.md referenced "two-track history."** Reading the project felt like reading two competing products.

User correction (2026-05-12): kill the old Studio / heavy CLI / TUI direction from the GitHub-facing project. Stop suggesting BeQuite requires Studio, localhost dashboard, heavy CLI, Docker, frontend, API, database, or a large runtime. The active direction is lightweight only.

## Decision

1. **Remove all heavy-direction assets from the GitHub-facing main branch:**
   - `studio/`, `cli/`, `tests/` (heavy-direction tests), `template/`, `evidence/`, `examples/`, `prompts/` (root), `state/` (root), `skill/` (root)
   - `docker-compose.yml`, `.dockerignore`, `.env.example`, `Makefile`, `package.json` (root), `.commitlintrc.json`
   - `scripts/docker-up.{ps1,sh}`, `scripts/bootstrap.{ps1,sh}`, `scripts/install.{ps1,sh}` (heavy installers)
   - `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md`, `docs/runbooks/LOCAL_DEV.md` (if heavy-direction-specific)

2. **Archive (not delete) two large historical docs:**
   - `BeQuite_MASTER_PROJECT.md` (49KB) → `docs/legacy/MASTER_PROJECT.md`
   - `CHANGELOG.md` (148KB heavy-history) → `docs/legacy/CHANGELOG-legacy.md`
   - Replace root `CHANGELOG.md` with a slim pointer to `docs/changelogs/CHANGELOG.md`

3. **Rewrite the GitHub-facing surface:**
   - `README.md` — full rewrite, 12 sections per spec; no Studio / CLI / Docker references
   - `CLAUDE.md` — drop "two-track history" framing; reference the lightweight direction only
   - All `docs/` rewrites point at `.claude/` + `.bequite/` only

4. **Git history retains everything.** Anyone can `git checkout <sha-before-cleanup> -- studio/` if they ever need to recover the heavy assets.

5. **Keep:** `.claude/`, `.bequite/`, `docs/`, `scripts/install-bequite.{ps1,sh}`, `BEQUITE_BOOTSTRAP_BRIEF.md` (historical brief), `LICENSE`, `README.md` (rewritten), `CLAUDE.md` (rewritten).

## Consequences

### Positive

- **Repo size drops materially.** From 484 tracked files to ~150-200. From ~MB to ~few-hundred-KB.
- **New users understand what BeQuite is in 5 minutes.** README leads with the skill-pack install command; no parallel-CLI confusion.
- **No more "paused, kept on disk" cognitive load.** The active direction is the only direction.
- **GitHub presentation is clean.** Logo / wordmark slot ready; feature highlights catchy; roadmap section honest.
- **Mistake memory + assumptions files** added to memory tree.
- **Tool neutrality (ADR-003) is more visible** since it's no longer competing with two implementation tracks.

### Negative

- **External users with bookmarks to `scripts/bootstrap.ps1`** get a 404. Mitigation: README's only install command is `scripts/install-bequite.{ps1,sh}`; broken bootstrap links are corrected in the public docs.
- **The `.github/workflows/`** may have referenced paths under `cli/`, `studio/`, `tests/e2e/` for CI. Mitigation: audit `.github/workflows/` after cleanup; remove or update any heavy-direction job.
- **`.bequite/memory/` (the v2.x Memory Bank with ADR-008..016)** stays — it's internal context, not in public docs. Some users might find references to it in old commits; they can ignore.

### Neutral

- The brief (`BEQUITE_BOOTSTRAP_BRIEF.md`) stays at root as historical context. It's 35KB. Anyone reading it will see the heavy-direction ideas; that's fine because it's clearly the BRIEF, not the current spec.
- The 11-dimension research model + mandatory gates + tool neutrality are unchanged. Only the surface area changes.

## Alternatives considered

### A — Keep "paused" framing forever

Pros: nothing destructive. Cons: confuses new users; bloats repo; sends mixed signal that BeQuite has two products. **Rejected.**

### B — Move heavy assets to a separate branch (`legacy/v2.x`)

Pros: preserves discoverability. Cons: branches expire from people's mental model; users won't find them anyway. Git history serves the same purpose. **Rejected.**

### C — Move heavy assets to a separate repo (`xpShawky/BeQuite-Studio`)

Pros: clean separation. Cons: more repos to maintain; nobody will use them; the heavy direction is retired. **Rejected.**

### D — Delete + archive small set; clean GitHub-facing surface

This ADR's choice. Surface is rewritten; heavy assets removed via `git rm`; two largest historical docs archived to `docs/legacy/`. Git history retains everything.

**Chosen: D.**

## Implementation

Phase A (non-destructive, this cycle):
1. Write `.bequite/audits/GITHUB_READY_CLEANUP_AUDIT.md`
2. Rewrite `README.md`, `CLAUDE.md`
3. Create `MISTAKE_MEMORY.md`, `ASSUMPTIONS.md`, `FEATURE_EXPANSION_ROADMAP.md`
4. Create 4 missing architecture docs + `docs/changelogs/CHANGELOG.md`
5. Update logs

Phase B (destructive — pauses for user authorization per ADR-002 hard human gate):
6. `git rm -r studio/ cli/ tests/ template/ evidence/ examples/ prompts/ state/ skill/`
7. `git rm docker-compose.yml .dockerignore .env.example Makefile package.json .commitlintrc.json`
8. `git rm scripts/docker-up.* scripts/bootstrap.* scripts/install.{ps1,sh}` (keep `install-bequite.*`)
9. `git rm docs/architecture/CLI_AUTHENTICATION_STRATEGY.md docs/runbooks/LOCAL_DEV.md`
10. Move `BeQuite_MASTER_PROJECT.md` → `docs/legacy/MASTER_PROJECT.md`
11. Move `CHANGELOG.md` → `docs/legacy/CHANGELOG-legacy.md`; replace root with slim pointer
12. Audit + clean `.github/workflows/`

Phase C: commit + push + (optional) tag v3.0.0-alpha.5.

## Rollback

If the cleanup is regretted within 30 days:
- `git revert <cleanup-commit-sha>` restores all deleted files
- No external systems depend on the deleted paths (no CI cron, no scheduled jobs)

## References

- User correction 2026-05-12 (in /bq-auto cleanup task)
- `.bequite/audits/GITHUB_READY_CLEANUP_AUDIT.md`
- ADR-001 (lightweight skill pack first)
- ADR-002 (mandatory workflow gates)
- ADR-003 (tool neutrality)
