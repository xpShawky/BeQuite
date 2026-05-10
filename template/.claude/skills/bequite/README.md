# template/.claude/skills/bequite/

> When `bequite init <project>` runs, this directory is populated by **copying** (or symlinking on POSIX) from the BeQuite repo's `skill/` directory. The fresh project then has `SKILL.md`, `agents/`, `commands/`, `hooks/`, `templates/`, `doctrines/`, `references/`, `routing.json`, and `skills-bundled/impeccable/` all under `.claude/skills/bequite/`.
>
> Claude Code discovers skills by walking `.claude/skills/<skill-name>/SKILL.md`. Cursor 3.0+ uses `.cursor/skills/<skill-name>/SKILL.md`. Codex CLI reads `AGENTS.md` (universal entry; no skill folder convention yet).
>
> The CLI command that wires this is `bequite skill install` (v0.12.0). Until v0.5.0 ships the CLI, the wiring is manual. See `docs/HOSTS.md` (drafted v0.14.0) for per-host install instructions.

## What gets populated here on `bequite init`

```
.claude/skills/bequite/
├── SKILL.md                      ← copied from skill/SKILL.md
├── agents/                       ← copied from skill/agents/
│   ├── product-owner.md
│   ├── research-analyst.md
│   ├── software-architect.md
│   ├── frontend-designer.md
│   ├── backend-engineer.md
│   ├── database-architect.md
│   ├── qa-engineer.md
│   ├── security-reviewer.md
│   ├── devops-engineer.md
│   ├── token-economist.md
│   └── skeptic.md
├── commands/                     ← copied from skill/commands/ (v0.4.0+)
├── hooks/                        ← copied from skill/hooks/ (v0.3.0+)
├── templates/                    ← copied from skill/templates/
├── doctrines/                    ← only the Doctrines listed in bequite.config.toml::doctrines
├── references/                   ← copied from skill/references/
├── routing.json                  ← copied from skill/routing.json
└── skills-bundled/impeccable/    ← copied if a frontend Doctrine is loaded
```

## Why copy (not symlink)

Symlinks don't work cleanly on Windows or in some Docker volumes. Copying gives every project a frozen, reproducible snapshot of BeQuite at init time, which is auditable. Re-running `bequite skill install` updates the snapshot.
