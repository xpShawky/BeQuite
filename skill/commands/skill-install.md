---
name: bequite.skill-install
description: Install BeQuite into a host (Claude Code / Cursor 3.0+ / Codex CLI / Gemini CLI / Windsurf / Cline / Kilo Code / Continue / Aider). BeQuite-unique. Detects host; copies skill/ + agents/ + commands/ + hooks/ + templates/ + doctrines/ + references/ + skills-bundled/ to the host's discovery path. Implementation lands in v0.12.0 as cli/bequite/skill_install.py.
phase: any (most often after init or before first session in a new host)
persona: devops-engineer (delegates to skill-install runner)
implementation: cli/bequite/skill_install.py (v0.12.0)
---

# /bequite.skill-install [host?]

When invoked (or `bequite skill install [host]`):

## Step 1 — Detect host

If no `--host` arg, auto-detect:

- `.claude/skills/` exists or Claude Code session detected → `claude-code`.
- `.cursor/skills/` exists or `.cursor/` exists → `cursor`.
- `AGENTS.md` exists at root + Codex-shaped tool calls → `codex`.
- `.gemini/` exists → `gemini`.
- `.windsurf/` exists → `windsurf`.
- `.clinerules` exists → `cline`.
- `.kilocode/` exists → `kilo`.
- `.continuerules` or `~/.continue/` → `continue`.
- `.aider.conf.yml` exists → `aider`.

If multiple, ask which one(s) to install for.

## Step 2 — Per-host install

### Claude Code

Target: `.claude/skills/bequite/`

- Copy `skill/SKILL.md` → `.claude/skills/bequite/SKILL.md`.
- Copy `skill/agents/*.md` → `.claude/skills/bequite/agents/`.
- Copy `skill/commands/*.md` → `.claude/skills/bequite/commands/`.
- Copy `skill/hooks/*.sh` → `.claude/skills/bequite/hooks/` (chmod +x).
- Copy `skill/templates/*.tpl` → `.claude/skills/bequite/templates/`.
- Copy active `skill/doctrines/<doctrine>.md` (per `state/project.yaml::active_doctrines`) → `.claude/skills/bequite/doctrines/`.
- Copy `skill/references/*.md` → `.claude/skills/bequite/references/`.
- Copy `skill/routing.json` → `.claude/skills/bequite/routing.json`.
- Copy active bundled skills (Impeccable when frontend Doctrine; ai-automation when ai-automation Doctrine) → `.claude/skills/bequite/skills-bundled/<name>/`.
- Merge `.claude/settings.json::hooks` from `template/.claude/settings.json` (preserves existing user hooks; appends BeQuite ones).

### Cursor 3.0+

Target: `.cursor/skills/bequite/` + `.cursor/rules/`

- Same copy as Claude Code, with the path prefix swapped.
- Additionally generate `.cursor/rules/bequite-constitution.mdc` referencing `.cursor/skills/bequite/SKILL.md`.

### Codex CLI

Target: `AGENTS.md` (universal entry) + `.codex/skills/bequite/`

- Ensure `AGENTS.md` references `.codex/skills/bequite/SKILL.md`.
- Copy skill content to `.codex/skills/bequite/`.

### Gemini CLI

Target: `.gemini/`

- Copy SKILL.md content into `GEMINI.md` (Gemini's primary entry).
- Copy agents + commands as referenced docs.

### Windsurf

Target: `.windsurf/rules/` + `.windsurf/skills/bequite/`

- Generate `.windsurf/rules/bequite.md` with the Constitution + key rules.
- Copy skill body.

### Cline

Target: `.clinerules` + `.cline/memory-bank/`

- Cline's Memory Bank is natively the same six-file pattern; symlink or copy `.bequite/memory/` ↔ `.cline/memory-bank/`.
- Generate `.clinerules` with key Constitution highlights.

### Kilo Code

Target: `.kilocode/`

- Generate `.kilocode/rules/` from active Doctrines.
- Copy skill body.

### Continue.dev

Target: `.continuerules` + `~/.continue/`

- Copy SKILL.md content to `.continuerules`.

### Aider

Target: `.aider.conf.yml` + `CONVENTIONS.md`

- Generate `CONVENTIONS.md` with Constitution highlights.
- Update `.aider.conf.yml::read` to include `CONVENTIONS.md`.

## Step 3 — Verify

After install: run a smoke test specific to the host:

- Claude Code: invoke `/bequite.recover`; assert paste-able prompt is rendered.
- Cursor: confirm `.cursor/rules/` populated; the agent reads them.
- Codex: confirm `AGENTS.md` references the skill and Codex finds it.
- Etc.

## Step 4 — Update state

- `state/project.yaml::hosts.generate_adapters_for` — append the just-installed host.
- `state/recovery.md::installed-hosts` — record.
- `evidence/<phase>/skill-install-<host>-<date>.md` — capture install diff.

## Stop condition

- Per-host files copied + verified.
- Smoke test passes.
- State updated.
- Receipt records the install.

## Anti-patterns

- Overwriting user-customised settings.json without merge.
- Copying inactive Doctrines (bloats the host context window).
- Skipping the smoke test ("the install succeeded" without a verified end-to-end).

## Related

- `template/.claude/skills/bequite/README.md` — describes what a fresh install looks like.
- `docs/HOSTS.md` (drafted v0.14.0) — per-host install guide for humans.
- `/bequite.recover` — the smoke test command for Claude Code.
