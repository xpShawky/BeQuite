# Hosts — per-host install + behavior

> BeQuite ships universal config + 9 host extensions. All hosts read AGENTS.md first (Linux Foundation Agentic AI Foundation schema). Host-specific files extend.

## Universal entry

Every BeQuite-managed project has `AGENTS.md` at the repo root. This is the universal entry every coding agent reads first.

## Supported hosts

| Host | Config file | Notes |
|---|---|---|
| **Claude Code** | `CLAUDE.md` (extends AGENTS.md) | Primary host BeQuite was developed in. |
| **Cursor** | `.cursor/rules/*.mdc` | Set `alwaysApply: true` per file. |
| **Codex CLI** | `.codex/AGENTS.md` (or AGENTS.md discovery) | Codex follows AGENTS.md natively. |
| **Cline** | `.clinerules/*.md` | Cline reads as system context. |
| **Kilo Code** | `.kilocode/*.md` | (Replaces Roo Code; Roo shut down 2026-05-15.) |
| **Continue.dev** | `.continuerules/*.md` | |
| **Aider** | `.aider/AGENTS.md` (or AGENTS.md discovery) | Aider's architect mode pairs well with BeQuite's review pattern. |
| **Windsurf** | `.windsurf/cascades/*.md` | |
| **Gemini CLI** | `.gemini/memory.md` | Gemini's memory pin. |

## Auto-detection + install

```bash
# Detect which hosts are present
bequite skill install
# (auto-detects + installs for each detected host)

# Or for a specific host
bequite skill install --host cursor
bequite skill install --host cline
```

The installer is **idempotent** — running twice doesn't overwrite. It also never deletes; if you want to remove BeQuite from a host, delete the host's config files manually.

## Host quirks

### Claude Code

- Loads `CLAUDE.md` + skills under `.claude/skills/bequite/` automatically.
- Hooks at `.claude/settings.json::hooks` enforce Iron Laws + Doctrine rules at exit-code-2.
- Skill format: full filesystem access; runs Python scripts.

### Cursor

- Reads `.cursor/rules/*.mdc` files; `alwaysApply: true` makes a rule apply to every prompt.
- BeQuite's installer creates `.cursor/rules/bequite-constitution.mdc` with the Iron Laws summary.
- Cursor doesn't run hooks at exit-code-2; rules are advisory in Cursor (the human enforces).

### Codex CLI

- Reads AGENTS.md natively (Linux Foundation schema).
- Codex 5.5 and later support `.codex/` extensions for codex-specific overrides.
- Review-mode role pending v0.10.x+ wiring.

### Cline / Kilo / Continue / Aider / Windsurf / Gemini

- All read their respective config dirs at session start.
- BeQuite's installer writes a stub file referencing AGENTS.md + Constitution.

## Adding a new host

1. Add the host to `cli/bequite/skill_install.py::HOSTS` dict (path) + `indicators` dict (detection paths).
2. Add a content function in `_content_for_host()` that emits the appropriate config format.
3. Add a row to the table above.
4. PR into BeQuite.

## Cross-references

- Installer module: `cli/bequite/skill_install.py`
- Universal entry template: `template/AGENTS.md.tpl`
- Cursor rules template: `template/.cursor/rules/bequite-constitution.mdc.tpl`
