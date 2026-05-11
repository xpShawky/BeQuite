# Decisions log

Append decisions as the project evolves. Newest at top.

## 2026-05-11 — Direction reset: lightweight skill pack as the MVP

**Decision:** BeQuite MVP is a lightweight project skill pack at `.claude/commands/` + `.claude/skills/` + `.bequite/` memory, installable into any Claude Code project. The Studio (marketing + dashboard + API) is paused (kept on disk, deferred to v4+).

**Rationale:**
- Less install friction (cp -r, not docker compose up --build)
- Smaller surface area
- Lower token waste
- Works directly inside Claude Code (matches the user's actual workflow)
- Avoids the recurring "shipped without verifying from fresh clone" failure pattern from the v2.x line
- Focuses on output quality (the agent's thinking + execution discipline), not on a fancy dashboard

**Documented in:** ADR-001-lightweight-skill-pack-first.md (`docs/decisions/`) + DIRECTION_RESET_AUDIT.md (`.bequite/audits/`)

**Files paused (not deleted):**
- `studio/` (marketing + dashboard + api + brand)
- `docker-compose.yml`, all `Dockerfile`s
- `tests/e2e/`
- `scripts/docker-up.{ps1,sh}`
- Root `package.json` + `Makefile` (still useful if Studio resumes)

**Files kept (still useful):**
- `cli/` — Python CLI v1.0.4 as optional supplemental tool
- `skill/` — source material for the new `.claude/skills/`
- `template/` — source for the lightweight installer
- All `docs/`, `examples/`, `evidence/`, `prompts/`, `state/`, `.bequite/memory/`

---

## 2026-05-10 — Iron Law X (operational completeness) added to Constitution v1.3.0

**Decision:** Constitution Article X — every change ships in operationally complete state. No "feature added but needs restart" hand-offs.

**Documented in:** ADR-014-iron-law-x-operational-completeness.md (`.bequite/memory/decisions/`)

(... older decisions preserved in `.bequite/memory/decisions/ADR-008` through `ADR-016` — see that directory for the full architectural history)

---

## For installed projects

When users install BeQuite into THEIR project via `/bq-init`, this file starts fresh:

```markdown
## <date> — BeQuite installed
Decision: Use BeQuite skill pack for this project's coding-agent workflow.
Rationale: Improve output quality with fewer errors via spec-driven gates.
```
