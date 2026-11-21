# The core pack

Always installed. The engineering pipeline and everything that keeps work honest: memory, research, plans, review, verification, the agent team and the harness commands. 45 commands and 26 skills; the authoritative lists are `templates/bequite/commands/COMMAND_ID_MAP.md` and `templates/bequite/skills/SKILL_REGISTRY.md` (Pack column).

## What it does

- **Setup and memory:** `/bequite`, `/bq-init`, `/bq-discover`, `/bq-doctor` (also writes `CAPABILITIES.md`), `/bq-mode`, `/bq-new`, `/bq-existing`, `/bq-work`, `/bq-memory`, `/bq-recover`, `/bq-handoff`.
- **Framing:** `/bq-clarify`, `/bq-research`, `/bq-scope`, `/bq-spec`, `/bq-plan` (with the options board), `/bq-multi-plan`.
- **Build:** `/bq-assign`, `/bq-implement`, `/bq-feature`, `/bq-fix`, `/bq-uiux-variants`, `/bq-live-edit`, `/bq-auto`.
- **Quality and release:** `/bq-test`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`, `/bq-release`, `/bq-changelog`.
- **Knowledge:** `/bq-knowledge` (build, ask, rag-plan, export, recording, reference, integrate, automation), `/bq-writing-dna`.
- **Agent team:** `/bq-team`, `/bq-operator`.
- **Harness:** `/bq-budget`, `/bq-taste`, `/bq-forge`, `/bq-eval`, `/bq-update`, `/bq-skill-audit`, `/bq-hooks`, `/bq-help`, `/bq-explain`, `/bq-suggest`.
- **Skills:** orchestrator, context-engineer, anti-hallucination, guard-pass, researcher, project-architect, product-strategist, backend-architect, database-architect, security-reviewer, devops-cloud, testing-gate, release-gate, problem-solver, frontend-design-system, ux-ui-designer, frontend-quality, live-edit, localization-rtl, automation, delegation, writing-dna, human-taste, agent-team, skill-auditor, updater.
- **Subagents:** `bq-researcher`, `bq-verifier`, `bq-red-team`, `bq-scout`.
- **Hooks:** SessionStart (session context), Stop (evidence before done), UserPromptSubmit (taste inbox).

## Install alone

`install-bequite.sh --packs core` or `$env:BEQUITE_PACKS="core"`. Routes into studio or business commands (for example a request for a reel) then say which pack to add instead of running.
