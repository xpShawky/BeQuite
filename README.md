# BeQuite

> **A lightweight Claude Code skill pack.** Install once into any project, get a strong workflow + memory + quality gates. No Docker. No dashboard. No heavy install.

By **xpShawky** ([Ahmed Shawky](https://github.com/xpShawky)). MIT.

---

## Install (one command)

```powershell
# Windows
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash
```

Run from inside the project folder you want to enhance. It copies:

- `.claude/commands/` — 24 slash commands
- `.claude/skills/bequite-*/` — 7 focused skills
- `.bequite/` — persistent memory + logs + plans + tasks
- A short `BeQuite` section appended to your `CLAUDE.md`

No dependencies installed. No daemons started. Just markdown files + a directory scaffold. **Idempotent** — won't overwrite your `.bequite/` memory unless you pass `--force`.

---

## Use (inside Claude Code)

After install, type these commands in Claude Code:

```
/bequite              # the menu — shows status + recommended next 3 commands
/bq-help              # full reference for every command
/bq-init              # formally initialize (write baseline state)
/bq-discover          # inspect this repo + write DISCOVERY_REPORT.md
/bq-doctor            # environment health check
```

That's typically all you need to onboard. From there, the workflow runs in five phases:

### Phase 0 — Setup and Understanding
`/bequite` · `/bq-help` · `/bq-init` · `/bq-discover` · `/bq-doctor`

### Phase 1 — Problem Framing
`/bq-clarify` · `/bq-research` · `/bq-scope` · `/bq-plan` · `/bq-multi-plan`

### Phase 2 — Build
`/bq-assign` · `/bq-implement` · `/bq-add-feature` · `/bq-fix`

### Phase 3 — Quality
`/bq-test` · `/bq-audit` · `/bq-review` · `/bq-red-team`

### Phase 4 — Ship
`/bq-verify` · `/bq-release` · `/bq-changelog`

### Phase 5 — Continue Later
`/bq-memory` · `/bq-recover` · `/bq-handoff`

Every command has YAML frontmatter so Claude Code surfaces it in the command picker. Each command's file (in `.claude/commands/`) is fully self-contained markdown — the actual procedure the agent follows.

---

## What BeQuite does for you

BeQuite is a **thinking + execution system** for AI coding agents:

- **Discipline** — every change runs through specification → plan → tasks → implementation → tests → verification.
- **Memory** — `.bequite/` keeps state across sessions. `/bq-recover` resumes where you left off.
- **Skeptic gate** — `/bq-red-team` actively tries to find what's broken in your plan before you ship it.
- **Honest reporting** — banned weasel words (`should`, `probably`, `seems to`, `appears to`, `I think it works`, `might`, `hopefully`, `in theory`). Pass or fail; no maybes.
- **Iron Law X** — every change ships in operationally complete state. No "feature added but needs restart."
- **PhantomRaven defense** — never imports a package without verifying it actually exists.
- **Doctrine-driven** — per-project rule packs (`default-web-saas`, `cli-tool`, `ai-automation`, `fintech-pci`, `mena-bilingual`, etc.) shape the agent's behavior.

---

## Architecture: skill pack + memory

```
your-project/
├── .claude/
│   ├── commands/                  ← 24 slash commands (markdown)
│   │   ├── bequite.md             /bequite (root menu)
│   │   ├── bq-help.md             /bq-help
│   │   ├── bq-init.md             /bq-init
│   │   ├── ... (21 more)
│   │   └── bq-handoff.md          /bq-handoff
│   └── skills/                    ← 7 focused skills (deeper procedures)
│       ├── bequite-project-architect/SKILL.md
│       ├── bequite-problem-solver/SKILL.md
│       ├── bequite-frontend-quality/SKILL.md
│       ├── bequite-testing-gate/SKILL.md
│       ├── bequite-release-gate/SKILL.md
│       ├── bequite-scraping-automation/SKILL.md
│       └── bequite-multi-model-planning/SKILL.md
├── .bequite/                      ← persistent memory
│   ├── state/
│   │   ├── PROJECT_STATE.md
│   │   ├── CURRENT_PHASE.md
│   │   ├── LAST_RUN.md
│   │   ├── DECISIONS.md
│   │   └── OPEN_QUESTIONS.md
│   ├── logs/
│   │   ├── AGENT_LOG.md           append-only
│   │   ├── CHANGELOG.md
│   │   └── ERROR_LOG.md
│   ├── prompts/
│   │   ├── user_prompts/
│   │   ├── generated_prompts/
│   │   └── model_outputs/         (for /bq-multi-plan manual paste)
│   ├── audits/                    DISCOVERY_REPORT, DOCTOR_REPORT, FULL_PROJECT_AUDIT, VERIFY_REPORT, REVIEW-*, RED_TEAM-*
│   ├── plans/                     IMPLEMENTATION_PLAN, SCOPE, feature-*
│   └── tasks/                     TASK_LIST.md
└── CLAUDE.md                       ← short BeQuite section appended
```

That's it. No `node_modules`. No `package.json` from BeQuite. No Docker.

---

## Workflow example — adding a feature to a real project

```
You: /bequite
BeQuite: shows the menu — "Recommended next: /bq-discover"

You: /bq-discover
BeQuite: writes .bequite/audits/DISCOVERY_REPORT.md
         "Detected: Next.js 15 + Drizzle + Supabase. Run /bq-doctor"

You: /bq-doctor
BeQuite: writes .bequite/audits/DOCTOR_REPORT.md
         "Node ✓ npm ✓ Docker ✓ ports 3000-3002 free. Ready"

You: /bq-add-feature "CSV export on bookings page"
BeQuite: writes a mini-spec, asks for approval
         (you say yes)
         implements the feature, writes a test, updates CHANGELOG

You: /bq-test
BeQuite: 47 unit + 4 e2e all pass. Updates state.

You: /bq-review
BeQuite: writes REVIEW-<timestamp>.md
         Verdict: Approved-with-comments (one nit about column ordering)

You: (fix the nit)
You: /bq-verify
BeQuite: full gate matrix — install + lint + types + tests + build + smoke
         All green. Updates VERIFY_REPORT.md.

You: /bq-release
BeQuite: bumps version, moves [Unreleased] → [1.3.0], prints git tag commands
         (you copy the commands and run them)
```

Total: about 30 minutes for a small feature, end to end, with discipline.

---

## Why a skill pack instead of a dashboard

BeQuite previously had a full Studio (marketing site + dashboard + Hono API + xterm terminal + Docker compose). It was impressive. It was also:

- Heavy: ~3GB Docker images, ~60s first build, requires Node 20 + Bun + Docker
- Fragile: 14 install-path bugs caught in 48 hours during one audit cycle
- Wrong abstraction: users live inside Claude Code, not in a separate browser tab

The skill pack:
- Is a `cp -r` install
- Lives where the user already works (Claude Code)
- Has zero install bugs because there's nothing heavy to break
- Focuses on the **thinking** (commands + skills + memory) instead of the **visualization**

The Studio is **paused, not deleted** (see `.bequite/audits/DIRECTION_RESET_AUDIT.md`). It's still in `studio/` and `docker-compose.yml` if you ever want it back.

---

## Optional: the BeQuite Python CLI

If you also want the Python CLI (`bequite` + `bq` console scripts) — useful for scripting and CI — install separately:

```powershell
# Windows
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.ps1 | iex
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.sh | bash
```

This is an **optional supplemental tool**, not required for the skill pack. The skill pack does everything the CLI does, just inside Claude Code.

---

## Docs

- **Install runbook:** [`docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md`](docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md)
- **Using BeQuite commands:** [`docs/runbooks/USING_BEQUITE_COMMANDS.md`](docs/runbooks/USING_BEQUITE_COMMANDS.md)
- **Architecture:** [`docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md`](docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md)
- **MVP scope:** [`docs/specs/MVP_LIGHTWEIGHT_SCOPE.md`](docs/specs/MVP_LIGHTWEIGHT_SCOPE.md)
- **Decision record:** [`docs/decisions/ADR-001-lightweight-skill-pack-first.md`](docs/decisions/ADR-001-lightweight-skill-pack-first.md)
- **Direction-reset audit:** [`.bequite/audits/DIRECTION_RESET_AUDIT.md`](.bequite/audits/DIRECTION_RESET_AUDIT.md)
- **Original brief:** [`BEQUITE_BOOTSTRAP_BRIEF.md`](BEQUITE_BOOTSTRAP_BRIEF.md)
- **Master file:** [`BeQuite_MASTER_PROJECT.md`](BeQuite_MASTER_PROJECT.md)
- **CHANGELOG:** [`CHANGELOG.md`](CHANGELOG.md)

---

## License

MIT. See [LICENSE](LICENSE).

## Maintainer

**Ahmed Shawky** ([@xpShawky](https://github.com/xpShawky)).
