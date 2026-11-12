# AGENTS.md

Entry point for any AI coding agent working **in this repository** (Claude Code, Codex, Cursor, Gemini CLI, Copilot, Aider, Windsurf and others). Claude Code: also read `CLAUDE.md`, which has the full rules.

## What this repo is

The source of **BeQuite v4**, a markdown workflow pack: slash-command playbooks (`.claude/commands/`), skills (`.claude/skills/bequite-*/`), reference docs (`.claude/bequite/docs/`), a memory scaffold (`templates/bequite/`) and two installers (`scripts/install-bequite.{ps1,sh}`). There is no application to build or run; the "product" is the markdown plus the installers.

## Before you change anything

1. Read `CLAUDE.md` (layout, rules for changing the pack, hard human gates).
2. Read the files you will touch; grep for every place that references them.
3. Keep it lightweight: no new runtime dependencies, servers, databases or Docker.

## Checks (must pass before a commit or PR)

```bash
python3 scripts/bq_check.py
bash -n scripts/install-bequite.sh
```

`bq_check.py` checks installer safety (the PowerShell installer must stay pure ASCII with no BOM, no `param()` block and no `exit`), frontmatter, references, counts, the standard contract block in every action command, and gate names. Regenerate the contract block with `python3 scripts/bq_check.py --fix contract` instead of editing it by hand.

## Rules

- Named tools are examples; justify any tool choice (10 decision questions in `CLAUDE.md`).
- Evidence over claims: report the command, exit code and output, or say `UNVERIFIED`.
- Never commit secrets or third-party media (reference films stay in the gitignored `motion-library/inbox/`).
- Releases (tags) are the maintainer's decision.

## Using BeQuite with your agent in another project

Per-agent setup (Antigravity, Gemini CLI, Cursor, Codex, Kimi, MiniMax, DeepSeek, Ollama and others): `.claude/bequite/docs/runbooks/INSTALL_FOR_OTHER_AGENTS.md`. Running the playbooks without slash commands: `.claude/bequite/docs/runbooks/USING_BEQUITE_OUTSIDE_CLAUDE_CODE.md`.
