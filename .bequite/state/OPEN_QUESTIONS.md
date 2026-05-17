# Open questions

Tracked questions awaiting answers. Set status to **resolved** when answered.

## For BeQuite itself

### Q1. Should studio/ + Docker assets be deleted now or kept paused on disk?

**Status:** ✅ RESOLVED (2026-05-17 — alpha.14 audit)
**Resolution:** Studio direction retired per ADR-004 (alpha.5 cleanup) — assets paused on disk; not active. No further action. Open Q to keep them deferred or delete is a v3.1+ concern.
**Source:** `docs/decisions/ADR-004-no-heavy-studio-or-cli.md`

### Q2. Should v3.0.0-alpha.1 be tagged + pushed immediately, or wait for live verification inside a Claude Code session?

**Status:** ✅ RESOLVED (alpha.1 long shipped; the system is now at alpha.13)
**Resolution:** Pushed to main; live-verified across alpha.1 → alpha.13 over 13 alpha releases. Question is obsolete.

### Q3. Should the Python CLI v1.0.4 stay as an optional install path, or be retired in favor of slash commands only?

**Status:** ✅ RESOLVED (2026-05-17 — alpha.14 audit)
**Resolution:** Python CLI is paused (heavy direction, ADR-004). Slash commands are the canonical MVP entry. The `cli/` directory remains on disk for historical reference. Active path: slash commands only.
**Source:** `docs/decisions/ADR-001-lightweight-skill-pack-first.md` + ADR-004

---

## For installed projects

When users install BeQuite into THEIR project, this file starts empty:

```markdown
# Open questions

(none yet — run /bq-clarify when ready to surface high-value questions)
```
