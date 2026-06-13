# Legacy `skill/` Folder Audit (alpha.24, 2026-06-13)

The root `skill/` directory is the **retired v2 heavy-direction** tree (ADR-004). 119 files / 948K: 20 agent personas, 20 commands, 13 doctrines, 15 hooks, references, `skills-bundled/` (ai-automation + impeccable), templates, `SKILL.md`, `routing.json`. Inventoried fully; **nothing deleted**.

## Classification

| Class | Contents | Action |
|---|---|---|
| **A — useful unique content** | `skills-bundled/ai-automation/references/` (n8n · make · zapier · temporal · inngest · patterns) + `agents/automation-architect.md` (platform selection, idempotency/retry/DLQ/observability discipline) | **MERGED** — distilled into the new `bequite-automation-engineer` skill (alpha.24) that powers `/bq-automation`. The merge is concept-level (BeQuite's own wording), not a copy; legacy files stay as historical source |
| **B — duplicate** | agents/commands that mirror current skills (backend/database/devops/security/frontend/research/testing/qa/red-team/skeptic; commands audit/plan/implement/review/research/recover/release/memory/discover) | current `.claude/skills/bequite-*` + `.claude/commands/` are source of truth; legacy versions superseded — pointer added in `skill/README.md` |
| **C — heavy-era retired** | `routing.json`, persona/model-tier machinery, `default_model: claude-opus-4-7` frontmatter, `skill-install`/`cost`/`freshness` commands, Studio-era assumptions | **NOT merged** — conflicts with ADR-001/004 lightweight direction; legacy-marked |
| **D — unique future idea** | `doctrines/` (13 layered doctrines incl. fintech-pci/healthcare-hipaa/gov-fedramp/mena-pdpl) richer than the current CLAUDE.md doctrine list; `skills-bundled/impeccable` (craft/harden/polish) | logged to MASTER §E as a parked idea ("doctrine-pack import" — promotion: when a regulated project needs it); impeccable already informs the frontend skill (alpha.17) |
| **E — unsafe / deletion candidate** | `hooks/*.sh` (15 shell hooks incl. pentest-authorization, no-malware, cve-poc-context) — overlap the alpha.18 opt-in hooks but are NOT wired | **NOT deleted** — listed for user decision; the active hooks live in `.claude/hooks/` (opt-in). Recommend: keep as legacy reference or user removes manually |

## Final state

A `skill/README.md` DEPRECATED/LEGACY pointer is added (below) so no reader mistakes it for an active system. **The active skill system is `.claude/skills/bequite-*/` (now 31 skills).** The legacy tree is not moved to `docs/legacy/` this pass (low risk; a 119-file move is noisier than a pointer — deferred as a safe option if the user prefers). No two active skill systems exist: legacy is clearly marked, its one piece of unique active value (automation references) is merged.
