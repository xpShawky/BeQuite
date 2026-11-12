# Workflow Export — `/bq-handoff workflow-export` (alpha.24)

Export a BeQuite workflow into reusable, **secret-safe** instructions/playbooks. Shape: **argument under `/bq-handoff`** (it is a handoff variant — no standalone command needed). Skill: context-engineer + security-reviewer (secret scan).

## Why an argument (not a command)

Export is "hand this workflow to someone/something else" — that is `/bq-handoff`'s job. A standalone `/bq-export` would duplicate handoff's purpose. The Workflow-Export V2 promotion condition ("secret-scan design first") is satisfied by the mandatory scan below.

## Outputs — `.bequite/exports/`

WORKFLOW_PLAYBOOK (the steps as a reusable playbook) · PROMPT_PACK (Claude/Codex/Cursor-compatible prompt snippets) · COMMAND_SEQUENCE (the catalog-ID sequence + required skills + memory files + gates + evidence requirements) · SAFETY_AND_SECRET_SCAN · HANDOFF_NOTES.

## Mandatory secret/privacy scan (before any export)

Run the scan checklist FIRST. **Never export:** secrets · API keys · private client data · personal data · hidden credentials · internal paths (unless safe) · env values · copyrighted/private content without permission. The export is blocked until SAFETY_AND_SECRET_SCAN passes (R3-grade gate). AGENTS.md-ready output reuses the cross-agent bridge format. **Built alpha.24 — NOT live-tested.**
