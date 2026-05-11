---
id: ADR-001
title: BeQuite MVP — lightweight skill pack first, not standalone app
status: accepted
date: 2026-05-11
supersedes: null
authors: [xpShawky, BeQuite Builder]
related: [DIRECTION_RESET_AUDIT.md, previous decisions in .bequite/memory/decisions/ADR-008..016]
---

## Context

For roughly 48 hours BeQuite was built as a heavy standalone product:

- A Python CLI (v1.0.4) shipping 21+ subcommands
- A three-app Studio (`studio/marketing/`, `studio/dashboard/`, `studio/api/`) — Next.js 15 + Tailwind v4 + R3F + xterm.js + Hono on Bun
- Docker Compose orchestration
- Multi-stage Dockerfiles
- Bootstrap one-liner installers
- 24-test Playwright e2e suite
- The works

Audit cycle (v2.0.0-alpha.6) caught 14 install-path + UX bugs across 48 hours. Every CHANGELOG entry that claimed "installable from a fresh clone" had to be re-attested live to actually verify. The recurring pattern: **shipping without verifying from fresh clone**.

The user (xpShawky) re-evaluated and gave new direction (2026-05-11):

> BeQuite = lightweight project skill pack + slash command pack. It should install inside any existing project folder and work mainly inside Claude Code, Codex, and similar coding agents. The goal is not to build a big dashboard first. The goal is to make BeQuite a powerful thinking and execution system that improves project output quality with fewer errors.

## Decision

**BeQuite's MVP is a lightweight Claude Code skill pack** consisting of:

```
.claude/commands/        — 24 markdown slash commands (/bequite + /bq-*)
.claude/skills/          — 7 focused skills (bequite-*/SKILL.md)
.bequite/                — persistent project memory (state, logs, plans, etc.)
scripts/install-bequite.{ps1,sh}  — light installer (copies files; no deps)
```

It installs into any project via a one-liner:

```powershell
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex
```

```bash
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash
```

The user then types `/bequite` inside Claude Code → sees the menu → follows the workflow commands.

**Constraints:**

- No heavy default dependencies. No Node modules. No Python venv (per-project). No Docker.
- No frontend, API, database, or dashboard required for BeQuite itself.
- No localhost app.
- Mostly markdown-based commands. Minimal scripts.
- Skills loaded only when relevant (Claude Code's progressive disclosure).
- Works inside Claude Code first; adapts to Codex / Antigravity / other hosts later.

## Alternatives considered

### A. Continue the heavy-app direction
- Pros: visually impressive, demos well
- Cons: 14 install-path bugs in 48h proved it's fragile; install friction is huge (Docker, Node 20+, Bun, Next.js 15, Tailwind v4); the dashboard is **the wrong abstraction layer** — users live in Claude Code, not in a separate browser tab; token spend on every dashboard render
- Rejected: doesn't match the user's actual workflow

### B. Just a Python CLI (v1.0.x line)
- Pros: works today; integration tests pass
- Cons: invokes a separate process; doesn't have access to the agent's tool surface; adds an install step (pip / pipx / uv) even when the user just wants to use Claude Code
- Status: kept as **optional supplemental tool**, not the MVP path

### C. Lightweight skill pack (chosen)
- Pros: zero install friction (just file copies); lives inside the agent's context; uses Claude Code's native slash-command + skill mechanisms; small surface = small audit area = fewer bugs
- Cons: tied to Claude Code first (adaptation to other agents is a v3.1 problem)
- Accepted

### D. Hybrid: skill pack + CLI both as first-class
- Pros: supports both workflows
- Cons: maintenance burden; users get confused about which to use
- Decided: keep CLI as optional supplemental, lead README with the skill pack

## Consequences

### Positive

- **Install becomes a `cp -r`** (or `iex` of the installer). No Docker, no Node, no Bun, no native compilation.
- **BeQuite lives in the agent's context** — slash commands invoke directly, skills are progressive-disclosure-loaded only when relevant.
- **Lower attack surface** for the recurring "ship without verify" failure pattern. The skill pack can't have a "frontend dead click" or "Turbopack panic" — there's no frontend.
- **Easier for vibecoders** — no "what's Docker?" friction.
- **Easier to validate** — a single Claude Code session can exercise the entire surface; no multi-terminal orchestration.

### Negative

- **Tied to Claude Code mechanisms first.** Slash commands + skills are Claude-Code-native. Adapting to Codex / Antigravity / Cursor needs a translation layer (mostly documentation, since the markdown files themselves are portable).
- **No visual dashboard.** Users who liked the Studio's xterm.js terminal + LiveIndicator + receipt list lose that view. (It still exists in `studio/` — paused, not deleted.)
- **CLI v1.0.4 path now has unclear positioning.** It works, but the README leads with slash commands. Some users will be confused which to install.

### Neutral

- **Heavy assets paused, not deleted.** `studio/`, `docker-compose.yml`, `tests/e2e/`, Dockerfiles all stay on disk. If the user later wants the Studio back, it's a `git checkout + docker compose up` away.
- **CHANGELOG history preserved.** The v0.1.0 → v2.0.0-alpha.6 era is documented; ADR-008 through ADR-016 stay valid for the heavy-app track.

## Implementation

This ADR was accepted alongside the implementation:

- `.bequite/audits/DIRECTION_RESET_AUDIT.md` — full keep/pause/delete-later inventory
- `.claude/commands/*` × 24 — all slash commands
- `.claude/skills/bequite-*/SKILL.md` × 7 — all focused skills
- `.bequite/state/*.md` — template state files
- `.bequite/logs/*.md` — append-only logs
- `.bequite/{prompts,plans,tasks,audits}/` — directory scaffold
- `scripts/install-bequite.{ps1,sh}` — light installer
- Rewritten `README.md` — leads with skill-pack install
- Shortened `CLAUDE.md` — points at new structure
- `docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md` — deeper architectural overview
- `docs/specs/MVP_LIGHTWEIGHT_SCOPE.md` — exact MVP scope
- `docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md` — install runbook
- `docs/runbooks/USING_BEQUITE_COMMANDS.md` — command usage runbook

## Verification

- Every `.claude/commands/*.md` has YAML frontmatter with `description:` (Claude Code requirement for slash commands)
- Every `.claude/skills/bequite-*/SKILL.md` follows Anthropic Skills SKILL.md format
- `.bequite/` memory scaffold is real (not just .gitkeep placeholders) — every state file has real template content
- `scripts/install-bequite.*` is **idempotent** (won't overwrite existing `.bequite/` memory without `--force`)
- The Studio + Docker + e2e directories still exist but are documented as paused

Live verification inside Claude Code (post-push):

```
1. Open any project in Claude Code
2. Run: irm .../install-bequite.ps1 | iex
3. Run: /bequite
4. Expect: menu showing current state + recommended next 3 commands
5. Run: /bq-help
6. Expect: full reference of all 24 commands grouped by phase
```

Pending — this is what the user does to validate after this PR lands.

## What this ADR explicitly does NOT decide

- **Whether to delete `studio/`, `docker-compose.yml`, `tests/e2e/`.** PAUSED only. Deletion gated on explicit user approval.
- **Whether to retag from v2.x to v3.0.0-alpha.1.** Tagging deferred until live verification passes inside Claude Code.
- **Whether the Python CLI continues to v1.1+.** Stays as v1.0.4 for now; user-call on whether v1.1 is worth investing in.
- **Whether to publish to PyPI / npm.** Out of scope.

## References

- `.bequite/audits/DIRECTION_RESET_AUDIT.md` — full inventory
- `.bequite/memory/decisions/ADR-013-studio-v2-architecture.md` — the now-PAUSED Studio architecture decision
- `.bequite/memory/decisions/ADR-014-iron-law-x-operational-completeness.md` — Iron Law X (still binding in the lightweight pack)
- `.bequite/memory/decisions/ADR-016-terminal-execution-rules-of-engagement.md` — paused with the Studio
- [Anthropic Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — SKILL.md format reference
- [Claude Code slash commands](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/slash-commands) — `.claude/commands/` filename convention
