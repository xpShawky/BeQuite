# ⚠️ LEGACY / DEPRECATED — do not use this directory

This `skill/` tree is the **retired v2 heavy-direction** of BeQuite (Studio + persona/model-tier machinery + heavy commands), retired per **ADR-004** ("no heavy Studio or CLI in the GitHub-facing project"). It is preserved for history only.

**The active system is:**
- Commands → `.claude/commands/` (slash commands; catalog IDs in `.bequite/commands/COMMAND_ID_MAP.md`)
- Skills → `.claude/skills/bequite-*/` (31 skills; registry `.bequite/skills/SKILL_REGISTRY.md`)
- Memory → `.bequite/`
- Orchestration source of truth → `.bequite/state/ORCHESTRATION_MAP.md`

**Do not** load, install, or follow anything in this folder for active work. Its one piece of still-useful unique content — the AI-automation platform references (n8n/Make/Zapier/Temporal/Inngest) and automation-architect discipline — was distilled into the active `bequite-automation-engineer` skill in alpha.24 (concept merge, not a copy).

Full classification: `.bequite/audits/LEGACY_SKILL_FOLDER_AUDIT.md`. Parked future idea (the 13-doctrine pack) tracked in `.bequite/tasks/REMAINING_WORK_MASTER.md` §E. Nothing here is auto-deleted; removal is a user decision.
