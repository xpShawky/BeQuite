# AGENTS.md — {{PROJECT_NAME}}

> Universal entry per Linux Foundation Agentic AI Foundation schema. Every coding agent (Claude Code, Cursor, Codex, Cline, Kilo, Continue, Aider, Windsurf, Gemini CLI) reads this file first.

## What this project is

{{PROJECT_DESCRIPTION}}

## Operating contract

This project is BeQuite-managed. The contract is:

1. Read `.bequite/memory/constitution.md` (Iron Laws + active Doctrines).
2. Read all six Memory Bank files at `.bequite/memory/{projectbrief,productContext,systemPatterns,techContext,activeContext,progress}.md`.
3. Read all active ADRs at `.bequite/memory/decisions/`.
4. Read `state/recovery.md` + `state/current_phase.md` + `state/project.yaml`.
5. Per Article III, treat the constitution + memory + state as binding context for every decision.

## Active doctrines

{{ACTIVE_DOCTRINES_LIST}}

## Active mode

{{MODE}}

## Banned weasel words

Do NOT use: should, probably, seems to, appears to, I think it works, might work, hopefully, in theory.

These are exit-code-2 violations of Article II (Verification before completion). Report what was tested + what passed + what failed + what is uncertain — all four every time.

## Host-specific extensions

| Host | File |
|---|---|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Codex CLI | `.codex/AGENTS.md` (this file is the canonical source; codex follows the same) |
| Cline | `.clinerules/` |
| Kilo Code | `.kilocode/` |
| Continue.dev | `.continuerules/` |
| Aider | `.aider/AGENTS.md` |
| Windsurf | `.windsurf/cascades/` |
| Gemini CLI | `.gemini/memory.md` |

All hosts read AGENTS.md (this file) first. Host-specific files extend; they don't replace.

## When in doubt

- Iron Law beats Doctrine.
- Doctrine beats convenience.
- ADR (status: accepted) beats convention.
- Active session evidence beats memory of a previous run.

## Cross-references

- Constitution: `.bequite/memory/constitution.md`
- Doctrines: `.bequite/doctrines/` (forks) + parent skill at `.bequite/skills/bequite/doctrines/`
- BeQuite repo: https://github.com/xpShawky/BeQuite
