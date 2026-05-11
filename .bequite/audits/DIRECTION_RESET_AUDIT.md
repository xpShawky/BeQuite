# BeQuite — Direction Reset Audit

**Date:** 2026-05-11
**Trigger:** User direction change — "BeQuite = lightweight project skill pack + slash command pack. Not a big standalone app or heavy CLI product."
**Auditor:** Claude (Opus 4.7) acting as senior product engineer
**Methodology:** Inventory every directory + file in the current repo, classify as **KEEP** / **PAUSE** / **DELETE-LATER** under the new direction. No file is deleted in this pass.

---

## 1. New direction summary (user's brief)

BeQuite installs **inside any existing project folder** and works mainly inside **Claude Code** and similar coding agents. The user enters a project, installs BeQuite once, then uses **slash commands** to guide the agent through a strong workflow.

The goal is **output quality with fewer errors**, not a fancy dashboard.

**Architecture target:**

```
<target-project>/
├── .claude/
│   ├── commands/             ← 24 markdown slash commands
│   │   ├── bequite.md           /bequite root command
│   │   ├── bq-help.md           /bq-help
│   │   ├── bq-init.md           /bq-init
│   │   ├── bq-discover.md       /bq-discover
│   │   ├── bq-doctor.md         /bq-doctor
│   │   ├── bq-clarify.md        /bq-clarify
│   │   ├── bq-research.md       /bq-research
│   │   ├── bq-scope.md          /bq-scope
│   │   ├── bq-plan.md           /bq-plan
│   │   ├── bq-multi-plan.md     /bq-multi-plan
│   │   ├── bq-assign.md         /bq-assign
│   │   ├── bq-implement.md      /bq-implement
│   │   ├── bq-add-feature.md    /bq-add-feature
│   │   ├── bq-fix.md            /bq-fix
│   │   ├── bq-test.md           /bq-test
│   │   ├── bq-audit.md          /bq-audit
│   │   ├── bq-review.md         /bq-review
│   │   ├── bq-red-team.md       /bq-red-team
│   │   ├── bq-verify.md         /bq-verify
│   │   ├── bq-release.md        /bq-release
│   │   ├── bq-changelog.md      /bq-changelog
│   │   ├── bq-memory.md         /bq-memory
│   │   ├── bq-recover.md        /bq-recover
│   │   └── bq-handoff.md        /bq-handoff
│   └── skills/               ← 7 focused skills (deeper procedures)
│       ├── bequite-project-architect/SKILL.md
│       ├── bequite-problem-solver/SKILL.md
│       ├── bequite-frontend-quality/SKILL.md
│       ├── bequite-testing-gate/SKILL.md
│       ├── bequite-release-gate/SKILL.md
│       ├── bequite-scraping-automation/SKILL.md
│       └── bequite-multi-model-planning/SKILL.md
├── .bequite/                 ← persistent memory
│   ├── state/PROJECT_STATE.md  CURRENT_PHASE.md  LAST_RUN.md  DECISIONS.md  OPEN_QUESTIONS.md
│   ├── logs/AGENT_LOG.md  CHANGELOG.md  ERROR_LOG.md
│   ├── prompts/{user_prompts,generated_prompts,model_outputs}/
│   ├── audits/
│   ├── plans/
│   └── tasks/
├── CLAUDE.md                 ← short, points at the new structure
└── scripts/install-bequite.{ps1,sh}  ← lightweight installer
```

**Constraints:**

- No heavy default dependencies
- No Docker required
- No frontend / API / database / dashboard required
- No localhost app
- Mostly markdown-based commands; minimal scripts
- Skills loaded only when needed
- Works in Claude Code first; adapts to Codex / Antigravity later

---

## 2. Current repo inventory (what's actually there)

### 2.1 Root-level

| Path | What | Reset classification |
|---|---|---|
| `README.md` | Heavy-app pitch (Docker + bootstrap) | **REWRITE** — lead with skill-pack pitch |
| `CLAUDE.md` | 7.7k chars; many Layer-1/2/heavy-app references | **SHORTEN** — point at new structure |
| `AGENTS.md` | Universal agent entry | **KEEP** — still valuable for non-Claude hosts |
| `CHANGELOG.md` | 150k chars; full history through v2.0.0-alpha.6 | **KEEP** — append direction-reset entry |
| `LICENSE` | MIT | **KEEP** |
| `BEQUITE_BOOTSTRAP_BRIEF.md` | Original brief | **KEEP** (history) |
| `BeQuite_MASTER_PROJECT.md` | Expanded master file | **KEEP** (history) |
| `package.json` (root) | npm scripts for one-command Studio dev | **KEEP-DEFERRED** — useful if Studio resumes later |
| `Makefile` | Same | **KEEP-DEFERRED** |
| `docker-compose.yml` | Three-service Studio stack | **KEEP-DEFERRED** — paused, not deleted |
| `.dockerignore` | Image build context filter | **KEEP-DEFERRED** |
| `.env.example` | Studio env-var reference | **KEEP-DEFERRED** + add lightweight-pack section |
| `.gitignore` | Standard | **KEEP** |
| `.commitlintrc.json` | Conventional Commits enforcement | **KEEP** |

### 2.2 Top-level directories

| Path | What | Reset classification |
|---|---|---|
| `cli/` | Python CLI (bequite + bq); 21+ subcommands; 125+ integration tests | **KEEP-AS-OPTIONAL** — useful tool, not the MVP focus. v1.0.4 stays installable. |
| `skill/` | Original BeQuite skill bundle (orchestrator + 20 persona files + commands + hooks + templates + doctrines + references + bundled Impeccable) | **KEEP-REFACTOR** — source material for the new `.claude/skills/`. Pulled selectively. |
| `template/` | Repo template for `bequite init` | **KEEP-REFACTOR** — source for the new lightweight installer |
| `studio/` | Marketing + Dashboard + API + Brand. v2.0.0-alpha.6 | **PAUSE** — keep on disk; not the current path. The user explicitly said studio is future work. |
| `tests/integration/` | 125+ Python tests for CLI | **KEEP** — protects CLI surface |
| `tests/e2e/` | 24-test Playwright suite for Studio | **PAUSE** — only relevant when Studio resumes |
| `scripts/` | install.ps1, install.sh, bootstrap.{ps1,sh}, docker-up.{ps1,sh} | **MIXED** — `install.ps1`/`bootstrap.ps1`/`install.sh`/`bootstrap.sh` stay (CLI install). `docker-up.{ps1,sh}` becomes deferred. ADD: `install-bequite.{ps1,sh}` for the new skill-pack installer. |
| `docs/` | 9 main docs + RELEASES/ + architecture/ + specs/ + audits/ + runbooks/ + changelogs/ + merge/ + planning_runs/ | **KEEP-EXTEND** — add `decisions/`, `architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md`, `specs/MVP_LIGHTWEIGHT_SCOPE.md`, two new runbooks |
| `examples/` | 3 example projects | **KEEP** — useful references |
| `evidence/` | Filesystem-level audit artifacts | **KEEP** |
| `prompts/` | 7 reusable prompt packs | **KEEP** — source for the new `.bequite/prompts/` |
| `state/` | recovery.md, current_phase.md, project.yaml, task_index.json | **KEEP** — useful as templates for `.bequite/state/` |
| `.bequite/memory/` | Project's own Memory Bank | **KEEP** — preserves project history |
| `.github/` | ci.yml + release.yml + commitlint.yml | **KEEP** |

### 2.3 What's overbuilt for the new direction

| Component | Why overbuilt | What we do |
|---|---|---|
| `studio/marketing/` (Next.js cinematic landing + R3F + MDX docs) | Heavy frontend — Tailwind v4 beta, Framer Motion, R3F, Three.js, drei. ~525 npm deps. Not needed for skill-pack MVP. | PAUSE |
| `studio/dashboard/` (Next.js operations console + xterm.js) | Same heavy frontend stack. Useful but not MVP. | PAUSE |
| `studio/api/` (Hono on Bun) | Requires Bun runtime. Filesystem read/write API. Not needed if BeQuite is just files in `.claude/` + `.bequite/`. | PAUSE |
| `docker-compose.yml` + Dockerfiles | Heavy install path (~3GB images, ~60s first build) for a skill pack that should be a `cp -r` operation | PAUSE |
| `tests/e2e/` (Playwright) | Tests the Studio. Not relevant for skill pack. | PAUSE |
| Python CLI 19+ subcommands | The CLI is useful but conflates "BeQuite runtime" with "BeQuite skill pack". Slash commands now do most of what the CLI does — invoked from inside Claude Code, no separate install needed. | KEEP-AS-OPTIONAL — separate from MVP |

### 2.4 What's just right (keep + reuse)

| Component | Why valuable |
|---|---|
| `skill/agents/*.md` (20 personas) | Reference material for the new skills — pull persona texts into `bequite-*` skill files. |
| `skill/commands/*.md` (master slash commands + BeQuite-unique) | Reference for the new `.claude/commands/` files — many concepts already written. |
| `skill/hooks/*.sh` (14 deterministic gates) | Reference for `bq-verify` / `bq-doctor` checks. |
| `skill/templates/*.tpl` | Source material for what we generate during `bq-init`. |
| `skill/doctrines/*.md` (13 doctrines) | Reference for `bequite-project-architect` skill. |
| `skill/references/*.md` (stack-matrix, security, frontend-stack, etc.) | Reference for `bequite-frontend-quality` + `bequite-scraping-automation` skills. |
| `.bequite/memory/decisions/ADR-001..016` | Architectural history. Keep for context. |
| `.bequite/memory/constitution.md` | Iron Laws + Doctrines. Reference for the new lightweight pack. |
| `cli/bequite/` Python code | Still works as an optional supplemental tool. v1.0.4 stays installable. |
| `tests/integration/` | Protects what's still useful. |

### 2.5 What's broken (in the heavy direction; doesn't matter now)

| Issue | Was a problem? | New direction |
|---|---|---|
| 7 install-path bugs caught in 48h (cli/README.md missing, PowerShell quote escape, R3F React 19 peer-dep, pip stderr halt, Turbopack cross-package CSS, NodeNext .js extensions, Docker healthcheck) | Yes — recurring pattern of "ship without verifying from fresh clone" | NEW MVP avoids all of them by not needing a heavy install at all. `cp -r .claude/ .bequite/ <target-project>/` is the entire install. |
| Frontend dead clicks + hardcoded panels | Yes — caught + fixed in v2.0.0-alpha.6 audit | NEW MVP has no frontend |
| Docker compose healthcheck wget bug | Yes — caught + fixed | NEW MVP has no Docker |
| Tailwind v4 motion token leak (F-8) | Cosmetic | NEW MVP has no CSS |
| `signedInUser` placeholder (F-10) | Cosmetic | NEW MVP has no UI |

---

## 3. Migration plan: heavy app → lightweight skill pack

### 3.1 What we KEEP (no change)

- `cli/` — Python CLI v1.0.4 (optional supplemental tool, not MVP focus)
- `skill/` — source material library (not directly used in install; pulled into `.claude/` content during authoring)
- `template/` — source for the new installer
- `tests/integration/` — protects CLI
- `examples/` — reference projects
- `evidence/`, `prompts/`, `state/`, `.bequite/memory/` — historical artifacts
- `docs/` — extend, don't restructure
- `BEQUITE_BOOTSTRAP_BRIEF.md`, `BeQuite_MASTER_PROJECT.md`, `LICENSE`, `AGENTS.md` — preserve
- `CHANGELOG.md` — append direction-reset entry
- `scripts/install.ps1`, `scripts/install.sh`, `scripts/bootstrap.ps1`, `scripts/bootstrap.sh` — still useful for CLI install (optional path)

### 3.2 What we PAUSE (stay on disk; documented as deferred)

- `studio/` (marketing + dashboard + api + brand) — full directory
- `docker-compose.yml`, `.dockerignore`, `studio/*/Dockerfile`, `studio/*/.dockerignore`
- `tests/e2e/` (Playwright Studio tests)
- `scripts/docker-up.ps1`, `scripts/docker-up.sh`
- Root `package.json`, `Makefile` (npm/make targets that drive Docker) — keep but document as "if Studio resumes later"

These are flagged in the new `docs/decisions/ADR-001-lightweight-skill-pack-first.md` as **paused, available for later**. Not deleted.

### 3.3 What we ADD (the new lightweight pack)

```
.claude/
├── commands/
│   ├── bequite.md                     /bequite      (root menu)
│   ├── bq-help.md                     /bq-help
│   ├── bq-init.md                     /bq-init
│   ├── bq-discover.md                 /bq-discover
│   ├── bq-doctor.md                   /bq-doctor
│   ├── bq-clarify.md                  /bq-clarify
│   ├── bq-research.md                 /bq-research
│   ├── bq-scope.md                    /bq-scope
│   ├── bq-plan.md                     /bq-plan
│   ├── bq-multi-plan.md               /bq-multi-plan
│   ├── bq-assign.md                   /bq-assign
│   ├── bq-implement.md                /bq-implement
│   ├── bq-add-feature.md              /bq-add-feature
│   ├── bq-fix.md                      /bq-fix
│   ├── bq-test.md                     /bq-test
│   ├── bq-audit.md                    /bq-audit
│   ├── bq-review.md                   /bq-review
│   ├── bq-red-team.md                 /bq-red-team
│   ├── bq-verify.md                   /bq-verify
│   ├── bq-release.md                  /bq-release
│   ├── bq-changelog.md                /bq-changelog
│   ├── bq-memory.md                   /bq-memory
│   ├── bq-recover.md                  /bq-recover
│   └── bq-handoff.md                  /bq-handoff
└── skills/
    ├── bequite-project-architect/SKILL.md
    ├── bequite-problem-solver/SKILL.md
    ├── bequite-frontend-quality/SKILL.md
    ├── bequite-testing-gate/SKILL.md
    ├── bequite-release-gate/SKILL.md
    ├── bequite-scraping-automation/SKILL.md
    └── bequite-multi-model-planning/SKILL.md

.bequite/                                (the persistent memory)
├── state/
│   ├── PROJECT_STATE.md
│   ├── CURRENT_PHASE.md
│   ├── LAST_RUN.md
│   ├── DECISIONS.md
│   └── OPEN_QUESTIONS.md
├── logs/
│   ├── AGENT_LOG.md
│   ├── CHANGELOG.md
│   └── ERROR_LOG.md
├── prompts/
│   ├── user_prompts/
│   ├── generated_prompts/
│   └── model_outputs/
├── audits/
├── plans/
└── tasks/

scripts/install-bequite.ps1                (Windows, lightweight installer)
scripts/install-bequite.sh                 (macOS / Linux)

docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md
docs/specs/MVP_LIGHTWEIGHT_SCOPE.md
docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md
docs/runbooks/USING_BEQUITE_COMMANDS.md
docs/decisions/ADR-001-lightweight-skill-pack-first.md
```

### 3.4 What we REWRITE / SHORTEN

| File | Reason |
|---|---|
| `README.md` | Lead with "BeQuite is a Claude Code skill pack you install into any project." Studio becomes a "future / advanced" footnote. |
| `CLAUDE.md` | Strip down to: what BeQuite is, core operating rules, where commands/skills/memory/logs live, never claim done unless verified, always update logs. |

### 3.5 Implementation steps (for this and subsequent commits)

1. ✅ **This commit: DIRECTION_RESET_AUDIT.md** (you are reading it now)
2. **Next commits (this session):**
   - Author `.claude/commands/*.md` × 24
   - Author `.claude/skills/bequite-*/SKILL.md` × 7
   - Scaffold `.bequite/{state,logs,prompts,audits,plans,tasks}/` with template content
   - Author `scripts/install-bequite.{ps1,sh}`
   - Rewrite `README.md`
   - Shorten `CLAUDE.md`
   - Author 4 new docs + ADR-001
   - Update `CHANGELOG.md` + `docs/changelogs/AGENT_LOG.md`
3. **Deferred (post-confirmation from user):**
   - Mark heavy `studio/` as paused in CHANGELOG with a stop-the-clock note
   - Potentially delete `studio/`, `docker-compose.yml`, `tests/e2e/` IF the user explicitly approves — not before
   - Tag the new release (likely `v3.0.0-alpha.1 "BeQuite Lite"` or similar)

---

## 4. Risk register

| # | Risk | Mitigation |
|---|---|---|
| R-1 | The user might later want the Studio back. Deletion would be irreversible. | All heavy assets stay on disk. PAUSE not DELETE. Documented in this audit. |
| R-2 | Two install paths (CLI + skill pack) may confuse users. | README leads with skill pack as MVP; CLI is "optional supplemental tool" footnote. |
| R-3 | Slash commands may not render in Codex / Antigravity exactly as in Claude Code. | Use Claude Code conventions first (filename → command name; YAML frontmatter). Document portability nuances in `docs/runbooks/USING_BEQUITE_COMMANDS.md`. |
| R-4 | 24 commands is a lot. New users may not know where to start. | `/bequite` root command is the menu — recommends the next 3 commands based on `.bequite/state/` reads. |
| R-5 | Memory dir `.bequite/` may collide with target project's existing artifacts. | Installer checks for existing `.bequite/`; refuses to overwrite without `--force`. |
| R-6 | Skills are referenced from commands; if user installs only commands not skills, commands break. | Installer is atomic — copies both `.claude/commands/` and `.claude/skills/` together. |

---

## 5. Naming decision (corrects user's brief)

User's original brief suggested `/bequite:init`, `/bequite:discover`, etc. Then corrected:

> Claude Code project commands are created from Markdown filenames inside `.claude/commands/`. So do not rely on project commands being called as `/bequite:init`. Use safer command names: `/bequite`, `/bq-init`, `/bq-discover`, etc.

**Confirmed:** All commands use dash-separated filenames (`bq-init.md`, `bq-discover.md`) → invoked as `/bq-init`, `/bq-discover`. The root `/bequite` is `bequite.md` (no prefix). YAML frontmatter has a `description:` field for each so Claude Code can surface the command properly.

---

## 6. What this audit explicitly does NOT decide

- Whether `studio/` files should be deleted from the repo. (PAUSE only. Decision deferred.)
- Whether `docker-compose.yml` should be moved to a `legacy/` directory. (Deferred.)
- Whether to retag from v2.x to v3.0.0-alpha.1 "BeQuite Lite". (Deferred.)
- Whether the Python CLI continues to ship to PyPI in parallel. (Deferred.)

These are user-call decisions. This audit ships the new lightweight structure ADDITIVELY. The user can decide later whether to remove the heavy assets.

---

## 7. Phase-0 done — ready to build

Direction-reset inventory complete. 24 commands + 7 skills + memory scaffold + installer + 5 new docs + ADR-001 — the next 7 commits.

Building now.
