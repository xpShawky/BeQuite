# Guard Pass Report — seed run (alpha.22, 2026-06-12)

Skill: `bequite-guard-pass` · scope: docs guard over release-facing docs (code/test guards N/A — no app code in this pass; markdown-only release).

## Findings

| # | Guard | Severity | Evidence | Status |
|---|---|---|---|---|
| 1 | docs | HIGH | `docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md:30-31` — "`.claude/commands/` — 24 slash commands" + "`.claude/skills/bequite-*` — 7 skills" while actual counts were 46 active commands / 27 skills (alpha.21). Stale since alpha.1; survived 20 releases. **Credit: caught by the user**, which is the strongest possible argument for an automated docs guard. | **FIXED in alpha.22** (counts corrected + pointer to canonical count source added) |
| 2 | docs | MEDIUM | Same runbook scaffold list (lines ~33-38) omitted memory dirs added alpha.8–alpha.22 (jobs/, money/, presentations/, design/, writing/, research/, reference/, knowledge/, courses/, pain-radar/, integrations/, proposals/) | **FIXED in alpha.22** (scaffold list updated to point at installer as source of truth) |

## Checked (coverage statement — required by the skill's quality gate)

README.md counts · commands.md counts · CLAUDE.md spec header · docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md · docs/runbooks/USING_BEQUITE_COMMANDS.md (no stale counts found beyond the above) · installer version strings (alpha.22 bump verified in this release's verify step).

## Verdict

FINDINGS (2) — both fixed this pass. Standing rule going forward: counts live canonically in `COMMAND_ID_MAP.md` + `SKILL_REGISTRY.md`; other docs reference rather than restate where possible; `/bq-verify drift` re-checks mechanically.
