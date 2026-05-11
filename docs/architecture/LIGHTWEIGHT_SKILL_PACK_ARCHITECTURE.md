# BeQuite — Lightweight Skill Pack Architecture (v3.0.0+)

This doc describes the **current architecture** of BeQuite. Per ADR-001 (2026-05-11), BeQuite's MVP is a lightweight project skill pack — not a standalone app.

For the **paused** heavy-app architecture (Studio + Docker + Hono API), see `.bequite/memory/decisions/ADR-013-studio-v2-architecture.md` and `studio/` on disk.

---

## 1. One-paragraph summary

BeQuite is a folder you copy into any project. After install, the project has:

- A set of slash commands (`/bequite`, `/bq-init`, `/bq-discover`, ...) at `.claude/commands/`
- A set of skills (deeper procedures the agent loads when needed) at `.claude/skills/bequite-*/`
- A memory directory at `.bequite/` that the commands read + write

Claude Code (or any compatible coding agent) discovers the slash commands by scanning `.claude/commands/`. When the user types `/bq-something`, Claude Code dispatches the corresponding markdown file as the agent's instruction set. Skills are progressively-disclosed — Claude Code (or the agent runtime) loads them only when the commands reference them.

There is no daemon, no separate process, no Docker, no localhost, no database for BeQuite itself.

---

## 2. The three layers

```
┌──────────────────────────────────────────────────────────────┐
│  L1 — Slash commands (.claude/commands/)                     │
│                                                              │
│  24 markdown files. Each defines:                            │
│   • YAML frontmatter (description for the command picker)    │
│   • Step-by-step procedure for the agent                     │
│   • Memory files read / written                              │
│   • Usual next command                                       │
│                                                              │
│  Surfaced to the user as /bequite, /bq-init, /bq-help, etc.  │
└────────────────────────┬─────────────────────────────────────┘
                         │ references / invokes
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  L2 — Skills (.claude/skills/bequite-*/SKILL.md)             │
│                                                              │
│  7 markdown files (Anthropic Skills SKILL.md format). Each:  │
│   • Has YAML frontmatter (name, description, allowed-tools)  │
│   • Documents deeper procedures, checklists, patterns        │
│   • Progressively disclosed — agent loads on relevance       │
│                                                              │
│  Not directly invoked by user. Commands reference them.      │
└────────────────────────┬─────────────────────────────────────┘
                         │ reads + writes
                         ▼
┌──────────────────────────────────────────────────────────────┐
│  L3 — Memory (.bequite/)                                     │
│                                                              │
│  Persistent project state across sessions:                   │
│   • state/        live workflow state                        │
│   • logs/         append-only history                        │
│   • prompts/      multi-model paste artifacts                │
│   • audits/       discovery + doctor + verify + audit + RT   │
│   • plans/        implementation plan + scope + features     │
│   • tasks/        task list                                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. L1 — slash commands

### File format

Each `.claude/commands/<name>.md`:

```markdown
---
description: One-sentence description shown in Claude Code's command picker.
---

# /<name> — short title

(Procedure for the agent to follow when the user types /<name>.)

## Memory files this command reads
- ...

## Memory files this command writes
- ...

## Usual next command
- /<next-name>
```

### Filename → command name

Claude Code derives the command name from the filename:

| File | Command |
|---|---|
| `.claude/commands/bequite.md` | `/bequite` |
| `.claude/commands/bq-init.md` | `/bq-init` |
| `.claude/commands/bq-discover.md` | `/bq-discover` |
| ... | ... |

This is why we use `bq-<verb>` not `bq:<verb>` — Claude Code's slash-command convention is based on filenames, not subdirectory namespacing. Per the user's brief.

### Workflow phases

Commands are grouped by **workflow phase** (the order users actually work in):

| Phase | Commands | Goal |
|---|---|---|
| 0 — Setup & Understanding | `/bequite`, `/bq-help`, `/bq-init`, `/bq-discover`, `/bq-doctor` | Learn what's there |
| 1 — Problem Framing | `/bq-clarify`, `/bq-research`, `/bq-scope`, `/bq-plan`, `/bq-multi-plan` | Decide what to build |
| 2 — Build | `/bq-assign`, `/bq-implement`, `/bq-add-feature`, `/bq-fix` | Build it |
| 3 — Quality | `/bq-test`, `/bq-audit`, `/bq-review`, `/bq-red-team` | Confirm it works |
| 4 — Ship | `/bq-verify`, `/bq-release`, `/bq-changelog` | Release |
| 5 — Continue Later | `/bq-memory`, `/bq-recover`, `/bq-handoff` | Resume + hand off |

The `/bequite` root command renders this map and recommends 3 next commands based on what's in `.bequite/state/`.

---

## 4. L2 — skills

### File format

Each `.claude/skills/bequite-<name>/SKILL.md`:

```markdown
---
name: bequite-<name>
description: One-sentence description. Triggers when the agent recognizes this domain in a command.
allowed-tools: ["Read", "Glob", "Grep", ...]
---

# bequite-<name>

(Deep procedures, checklists, principles, anti-patterns.)
```

### The 7 skills

| Skill | When it activates | Procedures inside |
|---|---|---|
| `bequite-project-architect` | `/bq-plan`, `/bq-research` | Stack matrix, ADR discipline, scale tiers, file-plan rigor, phase-plan acceptance |
| `bequite-problem-solver` | `/bq-fix`, `/bq-implement` (when stuck) | Reproduce-first, binary search, git bisect, 5-whys, common root-cause patterns |
| `bequite-frontend-quality` | `/bq-audit`, `/bq-add-feature` (UI), `/bq-review` (UI) | 10 design principles, 15 AI-slop patterns, component sourcing order, axe-core, tokens.css |
| `bequite-testing-gate` | `/bq-test`, `/bq-add-feature`, `/bq-fix` | Test pyramid, contract tests, snapshot rules, per-stack starter tests |
| `bequite-release-gate` | `/bq-verify`, `/bq-release`, `/bq-changelog` | Release matrix, CI parity, semver, CHANGELOG hygiene, signing, one-way doors |
| `bequite-scraping-automation` | `/bq-clarify` (when scraping in scope) | Article VIII discipline, polite-mode default, 2026 tool catalog, watch-and-trigger |
| `bequite-multi-model-planning` | `/bq-multi-plan` | 5 collaboration modes, prompt templates, merge procedure, tie-break order |

### Why skills are separate from commands

- **Progressive disclosure** — the agent loads the skill only when relevant. Saves tokens.
- **Reusability** — multiple commands can reference the same skill. E.g. both `/bq-add-feature` and `/bq-audit` use `bequite-frontend-quality`.
- **Depth** — commands are entry points (50-150 lines); skills are deep procedures (200+ lines).

---

## 5. L3 — memory

### Directory tree

```
.bequite/
├── state/
│   ├── PROJECT_STATE.md       — project identity + stack snapshot
│   ├── CURRENT_PHASE.md       — which workflow phase we're in
│   ├── LAST_RUN.md            — last command + outcome
│   ├── DECISIONS.md           — append-only decision history
│   └── OPEN_QUESTIONS.md      — unresolved questions
├── logs/
│   ├── AGENT_LOG.md           — append-only chronicle of every command
│   ├── CHANGELOG.md           — project changelog (or pointer to repo-root one)
│   └── ERROR_LOG.md           — bug + cause + fix history
├── prompts/
│   ├── user_prompts/          — original prompts from the user
│   ├── generated_prompts/     — prompts BeQuite generates (e.g. for /bq-multi-plan)
│   └── model_outputs/         — pasted-back responses (for /bq-multi-plan)
├── audits/                    — DISCOVERY_REPORT, DOCTOR_REPORT, RESEARCH_REPORT,
│                                FULL_PROJECT_AUDIT, VERIFY_REPORT, REVIEW-*, RED_TEAM-*
├── plans/                     — IMPLEMENTATION_PLAN, SCOPE, feature-*, MULTI_MODEL_COMPARISON
└── tasks/                     — TASK_LIST.md
```

### Memory discipline

- **Append-only logs:** `AGENT_LOG.md`, `ERROR_LOG.md` — never rewrite history.
- **State files mutate:** `CURRENT_PHASE.md`, `LAST_RUN.md` reflect current state.
- **Audits are timestamped:** `REVIEW-<YYYYMMDD-HHMMSS>.md` so multiple runs coexist.
- **Snapshots are immutable:** `state/SNAPSHOT-<timestamp>.md` for resumable checkpoints.

---

## 6. Install topology

```
                  ┌──────────────────────────┐
                  │  github.com/xpShawky/    │
                  │       BeQuite            │
                  │  (canonical source)      │
                  └──────────┬───────────────┘
                             │ shallow clone via installer
                             ▼
┌───────────────────────────────────────────────────────────────┐
│  user runs:                                                    │
│    irm .../install-bequite.ps1 | iex                          │
│       (or curl ... | bash on Unix)                            │
│                                                                │
│  installer copies:                                             │
│    .claude/commands/*  →  <target-project>/.claude/commands/  │
│    .claude/skills/*    →  <target-project>/.claude/skills/    │
│    scaffolds .bequite/{state,logs,prompts,...}/               │
│    appends BeQuite section to CLAUDE.md                       │
│                                                                │
│  installer does NOT install:                                   │
│    npm / pip / cargo dependencies                              │
│    Docker / containers                                         │
│    daemons / background services                               │
└───────────────────────────────────────────────────────────────┘
```

The installer is ~150 lines of PowerShell (Windows) + ~120 lines of bash (Unix). No third-party dependencies for the installer itself — just `git` for cloning and standard shell builtins.

---

## 7. Host compatibility

### Claude Code (primary)

Native. Reads `.claude/commands/*.md` (slash commands) + `.claude/skills/*/SKILL.md` (skills).

### Codex / Cursor / Antigravity / Other agents

Out of scope for v3.0.0. The markdown files themselves are portable; the dispatch mechanism is Claude-Code-specific.

For Codex / Cursor: a v3.1 effort can author `AGENTS.md` orchestrator that the agent reads to know about the commands + skills. Slash commands won't work natively but `/bequite` becomes "read `.claude/commands/bequite.md` and act on its instructions."

---

## 8. What this architecture does NOT include

- **A web dashboard** — paused in v3.0.0 (was the v2.0.0-alpha.x Studio direction)
- **A Hono API** — paused
- **xterm.js terminal** — paused
- **R3F particle effects** — paused
- **Docker compose orchestration** — paused
- **Bun runtime requirement** — paused
- **Better-Auth integration** — paused (no auth needed; memory is local files)
- **Postgres mirror** — paused
- **Multi-user cloud operation** — paused

All of the above are still on disk in `studio/` / `docker-compose.yml` / `tests/e2e/`. If the user later wants them back, it's a configuration switch, not a rebuild.

---

## 9. The Python CLI's relationship to this architecture

The Python CLI (`cli/`, v1.0.4) is an **optional supplemental tool**. It does most of what the skill pack does, but as a terminal command outside Claude Code.

- Skill pack is the MVP path
- CLI is for scripting / CI / power users / non-Claude-Code workflows

Both work; they don't conflict; they share no runtime state. The CLI writes to a different memory location (`<cli's cwd>/.bequite/`).

For maintenance: the CLI lives in its own subdirectory + has its own version + its own integration test suite (125+ tests, all green on Python 3.14). It doesn't slow the skill pack's iteration.

---

## 10. Invariants

These hold for every BeQuite installation:

- **No daemons.** Nothing runs in the background.
- **No global state.** Each project has its own `.bequite/`.
- **No phone-home.** The installer downloads from GitHub once; nothing else network-connects.
- **No mandatory dependencies.** Skill pack runs with just markdown files + Claude Code.
- **`.bequite/` is the only memory.** Outside that directory, BeQuite leaves no trace.
- **Idempotent install.** Running the installer twice doesn't break things; it refuses to overwrite memory without `--force`.

---

## 11. Future evolution

Likely v3.x roadmap (not committed; user discretion):

- v3.0.1+ — bug fixes from real-world skill-pack use
- v3.1 — Codex / Cursor / Antigravity adapters (AGENTS.md orchestrator)
- v3.2 — Per-Doctrine skill bundles (`bequite-fintech-pci`, `bequite-healthcare-hipaa`)
- v3.3 — Skill marketplace concept (community skills the user can opt into)

Studio (v2.0.0-alpha.x line) is **paused indefinitely**. If it resumes, it'll be as a separate product layer (e.g. `bequite-cloud` or `bequite-dashboard` as opt-in extras), not a forced part of the MVP.
