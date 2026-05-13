# BeQuite

> **The thinking layer for AI coding agents.** Make Claude Code plan, research, test, verify, and ship — without skipping critical thinking.

A lightweight skill pack + memory system. Install once. Works everywhere Claude Code runs.

**Latest:** `v3.0.0-alpha.10` · **Previous:** `v3.0.0-alpha.9` · MIT · by [@xpShawky](https://github.com/xpShawky)

**📖 Full command reference: [`commands.md`](commands.md)** — every command explained, ordered by workflow.

<p>
  <a href="#install"><img alt="Install" src="https://img.shields.io/badge/install-one_command-0ea5e9?style=flat-square"></a>
  <a href="commands.md"><img alt="43 commands" src="https://img.shields.io/badge/slash_commands-43-7c3aed?style=flat-square"></a>
  <a href="#how-to-use"><img alt="15 skills" src="https://img.shields.io/badge/skills-15-10b981?style=flat-square"></a>
  <a href="#workflow"><img alt="6 phases" src="https://img.shields.io/badge/phases-6-f59e0b?style=flat-square"></a>
  <a href="#what-bequite-is-not"><img alt="No Docker" src="https://img.shields.io/badge/no-Docker-64748b?style=flat-square"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-000000?style=flat-square"></a>
</p>

---

## What is BeQuite?

**BeQuite is a lightweight command-and-skill layer that turns Claude Code into a disciplined senior engineer.** No Docker. No dashboard. No heavy runtime. Just markdown files that make the agent think before it codes.

It gives every project:

- **43 slash commands** — `/bq-init`, `/bq-research`, `/bq-plan`, `/bq-feature`, `/bq-fix`, `/bq-auto`, `/bq-uiux-variants`, `/bq-live-edit`, `/bq-now`, `/bq-spec`, `/bq-explain`, `/bq-suggest`, `/bq-job-finder`, `/bq-make-money`, `/bq-update`, … (full reference: [`commands.md`](commands.md))
- **19 specialist skills** — researcher, product-strategist, backend-architect, database-architect, security-reviewer, devops-cloud, frontend-quality, ux-ui-designer, testing-gate, release-gate, live-edit, scraping-automation, problem-solver, multi-model-planning, project-architect, workflow-advisor, job-finder, make-money, updater
- **6 workflow phases** with **mandatory gates** that block out-of-order commands
- **Persistent memory** in `.bequite/` — state, plans, audits, logs, mistake memory
- **Tool neutrality** — every named tool is a candidate, not a default

Designed for Claude Code first. Skill format follows the Anthropic SKILL.md spec.

---

## Why BeQuite?

AI coding agents have predictable failure modes. BeQuite addresses each:

| Common AI mistake | BeQuite's defense |
|---|---|
| Skips discovery — starts coding immediately | `/bq-discover` writes a `DISCOVERY_REPORT.md` first |
| Produces weak plans built on stale memory | `/bq-research` covers 11 dimensions with verified 2026 evidence |
| Forgets context between sessions | `.bequite/` memory + `/bq-recover` resumes from last green checkpoint |
| Claims "done" without testing | `/bq-verify` runs the full gate matrix; banned weasel words rejected |
| Makes UI bugs (hidden text, dead buttons, AI-slop gradients) | `bequite-frontend-quality` + `bequite-ux-ui-designer` skills enforce 10 principles + reject 15 anti-patterns |
| Overbuilds — installs deps "just in case" | Tool neutrality rule: every tool needs a decision section |
| Leaves broken setup steps | Iron Law X: every change ships in operationally complete state |
| Doesn't think about security / scale / deployment | 11-dimension research + 7 specialist skills cover each domain |
| Restarts the whole lifecycle for a tiny fix | Scoped auto-mode runs only the relevant scope |
| Pauses on every step for approval | Auto-mode continues by default; pauses only at 17 hard human gates |

---

## Install

One command. Run it from inside the project folder you want to enhance.

```powershell
# Windows
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash
```

This copies:

- `.claude/commands/` — 42 slash commands
- `.claude/skills/bequite-*/` — 18 specialist skills
- `.bequite/` — memory + logs + plans + tasks + uiux + principles
- A short `BeQuite` section appended to your `CLAUDE.md`

**No dependencies installed. No daemons started. No Docker.** Just markdown files.

Idempotent — won't overwrite your `.bequite/` memory unless you pass `--force`.

---

## Quick start (3 minutes)

```
1. Open the project in Claude Code
2. Type:    /bequite
3. Read:    the menu shows state + recommends next 3 commands
4. Type:    the first recommended command
5. From there: BeQuite drives until you ship
```

Or skip straight to autonomous mode:

```
/bq-auto new "Build a SaaS dashboard for clinic bookings"
/bq-auto fix "Fix hidden text on the dashboard"
/bq-auto uiux variants=5 "Five dashboard design directions"
/bq-live-edit "Make the pricing cards less crowded"
```

---

## How to use

### For beginners

| Situation | Command |
|---|---|
| **I have a new project (empty folder)** | `/bq-new` or `/bq-auto new "what you're building"` |
| **I have an existing project I want audited** | `/bq-existing` or `/bq-auto existing "specific concern"` |
| **I want to add a feature** | `/bq-feature "feature description"` or `/bq-auto feature "..."` |
| **I want to fix a bug** | `/bq-fix "what's broken"` or `/bq-auto fix "..."` |
| **I want to improve UI/UX** | `/bq-uiux-variants 5 "what to redesign"` or `/bq-auto uiux ...` |
| **I want a live edit (text, spacing, colors)** | `/bq-live-edit "section + change"` |
| **I want to build automation/scraping** | `/bq-auto scraping "what to scrape"` or `/bq-auto automation "..."` |
| **I want release readiness** | `/bq-verify` then `/bq-release` |
| **I'm coming back after a break** | `/bq-recover` — finds last green checkpoint |

### For advanced users

| Capability | Command |
|---|---|
| **Auto mode (full lifecycle)** | `/bq-auto "task"` — agent runs P0 → P5; pauses only at hard human gates |
| **Phase orchestrators** | `/bq-p0` … `/bq-p5` — run one phase end-to-end |
| **Scoped auto mode (17 intents)** | `/bq-auto fix "..."` / `uiux` / `security` / `backend` / `database` / `deploy` / etc. — runs only the relevant scope |
| **Multi-model planning** | `/bq-multi-plan` — independent Claude + ChatGPT/Gemini plans, then merged |
| **UI/UX variants (1-10 directions)** | `/bq-uiux-variants [N] "scope"` — isolated routes; user picks winner |
| **Live edit workflow** | `/bq-live-edit "task"` — section-mapped frontend edits |
| **Adversarial review** | `/bq-red-team` — Skeptic mode; 8 attack angles |
| **Full audit** | `/bq-audit` — 10-area product audit with severity-tagged findings |
| **Memory snapshot** | `/bq-memory snapshot` — checkpoint before risky work |
| **Mistake memory** | Auto-updated by `/bq-fix`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`, `/bq-auto`, `/bq-live-edit` |
| **Handoff to another engineer** | `/bq-handoff` — writes `HANDOFF.md` |

### Workflow

The 6 phases (gates prevent skipping):

```
P0 Setup and Discovery        — learn what's there
  /bq-init  /bq-mode  /bq-discover  /bq-doctor

P1 Product Framing and Research — decide what to build
  /bq-clarify  /bq-research  /bq-scope  /bq-plan  /bq-multi-plan

P2 Planning and Build           — build it
  /bq-assign  /bq-implement  /bq-feature  /bq-fix

P3 Quality and Review           — confirm it works
  /bq-test  /bq-audit  /bq-review  /bq-red-team

P4 Release                      — ship
  /bq-verify  /bq-release  /bq-changelog

P5 Memory and Handoff           — continue or hand off
  /bq-memory  /bq-recover  /bq-handoff
```

A command refuses to run when its required gates aren't met. Example:

```
You:      /bq-implement
BeQuite:  Blocked — PLAN_APPROVED is ❌ pending.
          Run /bq-plan first, or use /bq-auto for autonomous scoped mode.
```

---

## Command map (39 commands)

Organized by phase, not alphabetically. **Full details for every command:** [`commands.md`](commands.md).

### Root
- `/bequite` — gate-aware menu + recommended next 3
- `/bq-help` — full command reference
- `/bq-now` — one-line orientation (faster than `/bequite`)
- `/bq-explain "<target>"` — plain-English explainer for files / functions / decisions

### Phase 0 — Setup and Discovery
- `/bq-init` — initialize `.bequite/` in this repo
- `/bq-mode` — select / show workflow mode
- `/bq-new` — begin a New Project workflow
- `/bq-existing` — begin an Existing Project Audit
- `/bq-discover` — inspect repo → `DISCOVERY_REPORT.md`
- `/bq-doctor` — environment health → `DOCTOR_REPORT.md`

### Phase 1 — Product Framing and Research
- `/bq-clarify` — 3-5 high-value clarifying questions
- `/bq-research` — 11-dimension verified evidence
- `/bq-scope` — lock IN / OUT / NON-GOALS
- `/bq-spec "<feature>"` — one-page Spec Kit-compatible spec (alpha.7)
- `/bq-plan` — write `IMPLEMENTATION_PLAN.md` (15 sections, no code yet)
- `/bq-multi-plan` — unbiased multi-model planning (manual paste, ToS-clean)

### Phase 2 — Planning and Build
- `/bq-assign` — break plan into atomic tasks
- `/bq-implement` — implement ONE task at a time
- `/bq-feature` — Add Feature workflow (12-type router)
- `/bq-fix` — Fix workflow (15-type router; reproduce-first)

### Phase 3 — Quality and Review
- `/bq-test` — run + write tests
- `/bq-audit` — 10-area full project audit
- `/bq-review` — review uncommitted diff + recent commits
- `/bq-red-team` — adversarial Skeptic review (8 attack angles)

### Phase 4 — Release
- `/bq-verify` — full local gate matrix
- `/bq-release` — release prep (prints commands; you run `git push`/`git tag`)
- `/bq-changelog` — categorize commits per Keep a Changelog

### Phase 5 — Memory and Handoff
- `/bq-memory` — read / write snapshots
- `/bq-recover` — resume after a break; finds last green checkpoint
- `/bq-handoff` — generate `HANDOFF.md` for another engineer

### Orchestrators
- `/bq-p0` … `/bq-p5` — walk one phase end-to-end
- `/bq-auto [intent] [--mode fast|deep|token-saver] "task"` — scoped autonomous runner (17 intents)

### UI/UX (alpha.4)
- `/bq-uiux-variants [N] "scope"` — generate 1-10 isolated UI directions
- `/bq-live-edit "task"` — section-by-section frontend edits

### Quick orientation (alpha.5)
- `/bq-now` — single-line status; faster than `/bequite`

### Opportunity and Workflows (alpha.8 + deepened in alpha.10)
- `/bq-suggest "<situation>"` — workflow advisor; recommends the best commands + mode for your goal
- `/bq-job-finder` — find real work opportunities (jobs, freelance, AI gigs); deep intelligence: community signals + trending + AI-assisted + 11 tracks
- `/bq-make-money` — find legitimate earning opportunities; deep intelligence + Hidden Gems + community signals + AI-assisted paths

### Maintenance (alpha.10)
- `/bq-update` — update BeQuite itself (safe, non-destructive; modes: check / safe / force / local / github)
- `/bq-memory` — memory snapshots
- `/bq-recover` — resume after a break
- `/bq-handoff` — generate HANDOFF.md

**For full procedural detail on every command:** see [`commands.md`](commands.md).

---

## 🆕 How to use the 3 new opportunity commands

**Important:** these commands run **inside Claude Code (or any Claude host)**. **Claude does the searching, not you.** You invoke the command, answer a short intake, and Claude:

- Uses WebFetch + WebSearch (built-in) by default
- Falls back to Chrome MCP (`mcp__claude-in-chrome__*`) when JS-rendered pages or DOM inspection are needed
- Falls back to Computer Use MCP (`mcp__computer-use__*`) as last resort — only with your explicit `request_access` permission

You sit back. Claude reports findings, classifies by fit + trust, writes everything to `.bequite/jobs/` or `.bequite/money/`. You decide what to act on.

### `/bq-suggest` — what should I do next?

Stuck in the command catalog? Describe your situation; Claude recommends the right route. Read-only — never implements.

```
/bq-suggest "I want to improve UI/UX and security"
/bq-suggest "I have a broken frontend and API"
/bq-suggest "I want to build a scraper and deploy it on VPS"
/bq-suggest "I have a project idea and want to know where to start"
/bq-suggest "I need UX + backend + testing"
```

**You get back:** recommended workflow (1-5 commands), skills activated, mode (fast / deep / token-saver), required gates, ONE recommended next command, and "why NOT each alternative".

### `/bq-job-finder` — find real work

Find full-time / part-time / remote / freelance / task / AI-gig opportunities. Claude does the search; you sit back.

**First run** asks a short intake (country, languages, skills, AI tools, payout methods, etc.). Saved to `.bequite/jobs/JOB_PROFILE.md` and re-used on later runs.

```
/bq-job-finder
/bq-job-finder "Remote AI-assisted gigs"
/bq-job-finder worldwide_hidden=true
/bq-job-finder worldwide_hidden=true "Find overlooked remote tasks"
```

**You get back:** ranked opportunities (Best fit / Easy start / High pay / Fast application / Needs portfolio / Needs learning / Risky / Not recommended / Hidden Gems), trust check per platform, application link, suggested pitch, next action — all written to `.bequite/jobs/OPPORTUNITIES.md` for you to review.

### `/bq-make-money` — find legitimate earning opportunities (with focus on Worldwide Hidden mode)

Find legitimate earning opportunities ranked by your goals. 10 tracks; supports `worldwide_hidden=true` for opportunities people in your country usually don't find.

**First run** asks intake (country, languages, skills, AI tools, devices, payment methods, target income, risk tolerance, time per day, fast money vs. sustainable income, calls okay or text only, preferred track).

#### Pick a track

| Track flag | Best for |
|---|---|
| `track=highest-payout` | Highest $/hour or $/task — even if harder |
| `track=easiest-start` | No portfolio, instant signup, fast verify |
| `track=fastest-first-payout` | Get paid this week if possible |
| `track=long-term-stable` | Recurring monthly income, not one-offs |
| `track=ai-assisted` | Use your AI tools as multiplier |
| `track=no-calls` | Async only, text-based |
| `track=remote-global` | Works regardless of your location |
| `track=local-only` | Tied to your country + language |
| `track=beginner` | No prior experience needed |
| `track=skilled` | Premium rate; expertise required |

If you don't specify, Claude auto-picks based on your profile.

#### Basic examples

```
/bq-make-money
/bq-make-money "Egypt, AI image editing, 3 hours daily, want remote tasks"
/bq-make-money "Find easy AI-assisted tasks with real payout"
/bq-make-money track=highest-payout country=Egypt skills='AI tools, writing, image editing'
/bq-make-money "Update previous search and find new opportunities"
```

#### 🌍 Worldwide Hidden mode (the high-value flag)

Add `worldwide_hidden=true` to search **beyond** famous English platforms and your home country. Claude looks for overlooked legitimate opportunities in:

- **Non-English markets** — Portuguese / Spanish / German / French / Italian / Turkish / Polish / Romanian / Indonesian / Hindi / Arabic + English
- **Country-specific microtask platforms** — Yandex Toloka, Wuzzuf, Brighter Monday, Get on Board, Wantedly, etc.
- **AI training task platforms** — Outlier, Mercor, Mindrift, Surge, Data Annotation, Scale, Appen
- **Research panels** — User Interviews, Respondent, dscout, Prolific
- **Testing platforms** — UserTesting, UserBrain, Userlytics
- **App-based earning programs** — Premise, Field Agent, Streetbees
- **Small companies hiring globally** — Wellfound, RemoteRocketship
- **Niche platforms by skill / region** — searched live per profile

**Examples:**

```
/bq-make-money worldwide_hidden=true "Find hidden legitimate earning opportunities worldwide"
/bq-make-money track=highest-payout worldwide_hidden=true
/bq-make-money track=easiest-start worldwide_hidden=true
/bq-make-money worldwide_hidden=true "Search high-paying remote task platforms for Arabic and English speakers"
```

**You get back:**

- **10 ranked sections** — Best hidden / Highest payout / Easiest start / Fastest first payout / Best AI-assisted / Best no-call / Best long-term / Best for your country / Best worldwide remote / Risky or not recommended
- **Hidden Gems section** — lesser-known but legitimate opportunities not in normal job searches; each with platform / country / language / work type / why hidden / payout method / eligibility / difficulty / risk level / first step / trust check result
- **Per-opportunity trust check** — legitimacy / country eligibility / payout method / VPN policy / ID verification / upfront-fee red flags / scam reports / realistic payout / time to first payout / what makes it hidden
- **7-day action plan** — concrete daily actions; first-payout target by end of week if possible

All saved to `.bequite/money/` (OPPORTUNITIES.md, TRUST_CHECKS.md, ACTION_PLAN.md). Re-run later to compare with previous results; Claude marks 🆕 new / ✅ still active / ❌ expired / ⚠ risk increased / ⬆ better alternative / 🔍 needs verification.

#### Strict safety rules (Claude refuses)

❌ Scams / fraud / fake reviews / fake accounts / fake engagement
❌ CAPTCHA bypass / CAPTCHA farms (likely abuse, low pay)
❌ Spam / mass cold outreach / VPN misrepresentation / identity misuse
❌ Upfront-fee scams / passive-income MLM / crypto pump-and-dump
❌ "Make $500/day from your phone with no skills" promises
❌ Adult / NSFW unless you explicitly opt in
❌ Anything failing the trust check — clearly marked "Not recommended" with reason

---

## Architecture

```
your-project/
├── .claude/
│   ├── commands/              ← 36 slash commands (markdown)
│   │   ├── bequite.md
│   │   ├── bq-init.md
│   │   └── … (34 more)
│   └── skills/                ← 15 specialist skills
│       ├── bequite-researcher/SKILL.md
│       ├── bequite-product-strategist/SKILL.md
│       ├── bequite-ux-ui-designer/SKILL.md
│       ├── bequite-backend-architect/SKILL.md
│       ├── bequite-database-architect/SKILL.md
│       ├── bequite-security-reviewer/SKILL.md
│       ├── bequite-devops-cloud/SKILL.md
│       ├── bequite-frontend-quality/SKILL.md
│       ├── bequite-testing-gate/SKILL.md
│       ├── bequite-release-gate/SKILL.md
│       ├── bequite-live-edit/SKILL.md
│       ├── bequite-scraping-automation/SKILL.md
│       ├── bequite-problem-solver/SKILL.md
│       ├── bequite-multi-model-planning/SKILL.md
│       └── bequite-project-architect/SKILL.md
├── .bequite/                  ← persistent memory
│   ├── principles/
│   │   └── TOOL_NEUTRALITY.md
│   ├── state/
│   │   ├── PROJECT_STATE.md
│   │   ├── CURRENT_MODE.md
│   │   ├── CURRENT_PHASE.md
│   │   ├── WORKFLOW_GATES.md
│   │   ├── LAST_RUN.md
│   │   ├── DECISIONS.md
│   │   ├── OPEN_QUESTIONS.md
│   │   ├── ASSUMPTIONS.md
│   │   └── MISTAKE_MEMORY.md
│   ├── logs/                  ← AGENT_LOG, CHANGELOG, ERROR_LOG
│   ├── research/              ← (created on demand)
│   ├── audits/                ← DISCOVERY_REPORT, DOCTOR_REPORT, AUDIT, VERIFY_REPORT, REVIEW-*, RED_TEAM-*
│   ├── plans/                 ← IMPLEMENTATION_PLAN, SCOPE, FEATURE_EXPANSION_ROADMAP
│   ├── tasks/                 ← TASK_LIST, CURRENT_TASK
│   ├── prompts/               ← user/generated/model_outputs
│   ├── uiux/                  ← SECTION_MAP, LIVE_EDIT_LOG, UIUX_VARIANTS_REPORT, selected-variant, screenshots, archive
│   └── handoff/               ← (created on demand)
└── CLAUDE.md                  ← BeQuite section appended on install
```

That's the whole footprint. No `node_modules`, no Docker, no Python, no daemons.

---

## Examples

Practical, real-world calls:

```
/bq-auto new "Build a SaaS dashboard for clinic bookings"
/bq-auto fix "Fix hidden text and dead buttons on localhost:3000"
/bq-auto uiux variants=5 "Create 5 dashboard design directions"
/bq-auto security "Audit and patch OWASP top 10 coverage"
/bq-auto deploy "Plan + execute VPS deployment with safety gates"

/bq-live-edit "Make the pricing cards less crowded"
/bq-live-edit "Improve the empty state on /dashboard"
/bq-live-edit "Fix mobile layout overflow on hero"

/bq-multi-plan
/bq-verify
/bq-red-team
/bq-recover
```

---

## Feature highlights

- **Mandatory workflow gates** — `.bequite/state/WORKFLOW_GATES.md` blocks out-of-order commands. Can't `/bq-implement` without `PLAN_APPROVED ✅`.
- **Next best command** — every command tells you what to run next. `/bequite` shows the recommended next 3 based on current state.
- **Scoped auto mode** — `/bq-auto fix "..."` doesn't restart the whole project lifecycle. It runs only the relevant scope.
- **Deep research before planning** — `/bq-research` covers 11 dimensions (stack, product, competitors, failures, success, user journey, UX/UI, security, scalability, deployment, differentiation). Live WebFetch, not memory.
- **UI/UX variants** — 1-10 isolated design directions; user picks winner; agent merges. Original UI stays intact until selection.
- **Live edit workflow** — section-mapped frontend edits. Maps visible sections to source files; applies the smallest possible edit; verifies via build + (optional) screenshots. **Never auto-installs browser tools.**
- **Mistake memory** — `.bequite/state/MISTAKE_MEMORY.md` captures every fix + prevention rule. Re-read on session start.
- **Before/after proof** — every edit logged with before/after diff. No "should work" claims.
- **Fresh install check** — `/bq-doctor` validates env on every cycle.
- **Red-team review** — `/bq-red-team` actively tries 9 attack angles (security, architecture, testing, deployment, scalability, UX, token-waste, hidden assumptions, tool-choice).
- **Multi-model planning** — `/bq-multi-plan` runs unbiased Claude + ChatGPT/Gemini plans (manual paste, ToS-clean), merges them.
- **Release readiness** — `/bq-verify` full gate matrix; `/bq-release` never auto-pushes (you run `git push`/`git tag`).
- **DevOps/cloud safety gates** — production server / VPS / Nginx / SSL changes always pause for user.
- **Scraping and automation skill** — `bequite-scraping-automation` enforces Article VIII (robots.txt respect, polite-rate default, no captcha-solving).
- **Tool neutrality** — every named tool is a candidate, not a default. Decision sections required before adopting.
- **Bot/product builder roadmap** — see [`docs/specs/FEATURE_EXPANSION_ROADMAP.md`](.bequite/plans/FEATURE_EXPANSION_ROADMAP.md) for the family of future feature commands.

---

## Tool neutrality (the golden rule)

Every tool, library, framework, design system, or workflow mentioned anywhere in BeQuite is an **example**, not a fixed mandatory choice.

❌ **Do not say:** "Use X."
✅ **Say:** "X is one candidate. Research and compare against other options. Use it only if it fits this project."

Before any major tool pick, the agent answers 10 decision questions:

1. Project type? · 2. Actual problem? · 3. Scale? · 4. Constraints? · 5. Existing stack? · 6. UX needed? · 7. Failure risks? · 8. Proven tools? · 9. Overkill? · 10. Best output / least complexity?

Then writes a decision section: Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan.

Full rule: [`.bequite/principles/TOOL_NEUTRALITY.md`](.bequite/principles/TOOL_NEUTRALITY.md) · ADR-003.

---

## What BeQuite is NOT

- ❌ Not a heavy IDE
- ❌ Not a Studio / dashboard
- ❌ Not a replacement for Claude Code (it runs **inside** Claude Code)
- ❌ Not a dependency-heavy framework
- ❌ Not a one-click magic app generator
- ❌ Not a tool that skips testing or judgment
- ❌ Not a Python CLI / Docker stack / npm package

BeQuite is markdown files + a directory scaffold. That's the whole product.

---

## Roadmap

### MVP (now — v3.0.0-alpha.8)
- ✅ 42 slash commands across 6 phases + Opportunity & Workflows
- ✅ 18 specialist skills
- ✅ Mandatory workflow gates (23 gates)
- ✅ 17 hard human gates in auto-mode
- ✅ Scoped autonomous runner (17 intents) with `--mode fast|deep|token-saver`
- ✅ UI/UX variants (1-10 isolated directions)
- ✅ Live edit workflow (section-mapped)
- ✅ Tool neutrality principle (ADR-003)
- ✅ Mistake memory wired into 7 commands (fix / audit / review / red-team / verify / auto / live-edit)
- ✅ `/bq-now` — one-line orientation
- ✅ `/bq-spec` — Spec Kit-compatible spec writer (alpha.7)
- ✅ `/bq-explain` — plain-English explainer for files / functions / decisions (alpha.7)
- ✅ `commands.md` — full command reference, workflow-ordered
- ✅ Studio direction removed from main (history preserved in git, ADR-004)
- ✅ 4 architecture docs created (WORKFLOW_GATES, RESEARCH_DEPTH_STRATEGY, FEATURE_AND_FIX_WORKFLOWS, DEVOPS_CLOUD_SAFETY)
- ✅ Installer auto-copies alpha.5 templates into target projects (alpha.6)
- ✅ 19 alpha.1 commands extended with standardized fields (alpha.6); 36 of 39 commands have full template
- ✅ `/bq-suggest` — workflow advisor (alpha.8)
- ✅ `/bq-job-finder` — real work opportunity finder with worldwide_hidden mode (alpha.8)
- ✅ `/bq-make-money` — earning opportunity finder with 10 tracks + Hidden Gems (alpha.8)
- ✅ Strict safety rules across opportunity commands (no scams, no fraud, no abuse)

### v1 (next — alpha.9)
- Live verification of `/bequite` against fresh real-world projects (user action)
- Architecture docs expanded (from concise summaries to full reference content)
- `/bq-help` extended with full standardized fields
- Installer updated to copy `.bequite/jobs/` + `.bequite/money/` templates

### v2 (later, roadmap only — see `FEATURE_EXPANSION_ROADMAP.md`)
- Grouped feature families: `/bq-build-bot`, `/bq-monitor`, `/bq-automation`, `/bq-content`, `/bq-data`, `/bq-report`, `/bq-saas` (names TBD)
- Bot builder, website change monitor, scraping product factory, lead finder, report generator, QA bot, decision support, etc.
- Off-label uses: lecture builder, academic writing, marketing campaign builder, course builder, support bot, sales agent (everything goes through the same gates + skills + memory)

**Not overpromised. The lightweight skill pack stays lightweight.** Future commands are grouped families, not 100 new slash commands.

---

## Off-label use cases

BeQuite was designed for shipping software. The same discipline applies elsewhere:

- **Lecture / course builder** — research-before-planning works for educational content too
- **Academic writing** — the 11-dimension research model is excellent for literature review
- **Research assistant** — `/bq-research` + `/bq-multi-plan` on its own is a competitive intelligence engine
- **Marketing campaign builder** — JTBD + persona + differentiation tests (from `bequite-product-strategist`)
- **Bot maker / automation factory** — Article VIII discipline + n8n/Make/Zapier as candidates (per tool neutrality)
- **Booking automation** — full lifecycle from /bq-clarify to /bq-deploy
- **Internal tool builder** — small SaaS dashboards with all the gates
- **Style cloner / persona simulator** — multi-model planning makes the prompts independently
- **Auto documentation builder** — the same workflow that ships code also ships docs
- **Tender / proposal writer** — 11-dimension research + product-strategist + write discipline
- **Medical / pharmacy assistant builder** — domain-specific knowledge plus safety gates

The lightweight skill pack is the core. Any project that benefits from "research → plan → build → verify → log" benefits from BeQuite.

---

## Docs

- **Install:** [`docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md`](docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md)
- **Using BeQuite:** [`docs/runbooks/USING_BEQUITE_COMMANDS.md`](docs/runbooks/USING_BEQUITE_COMMANDS.md)
- **Architecture:** [`docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md`](docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md)
- **Auto-mode strategy:** [`docs/architecture/AUTO_MODE_STRATEGY.md`](docs/architecture/AUTO_MODE_STRATEGY.md)
- **UI/UX variants strategy:** [`docs/architecture/UIUX_VARIANTS_STRATEGY.md`](docs/architecture/UIUX_VARIANTS_STRATEGY.md)
- **Live edit strategy:** [`docs/architecture/LIVE_EDIT_STRATEGY.md`](docs/architecture/LIVE_EDIT_STRATEGY.md)
- **Multi-model planning:** [`docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md`](docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md)
- **Command catalog:** [`docs/specs/COMMAND_CATALOG.md`](docs/specs/COMMAND_CATALOG.md)
- **MVP scope:** [`docs/specs/MVP_LIGHTWEIGHT_SCOPE.md`](docs/specs/MVP_LIGHTWEIGHT_SCOPE.md)
- **Tool neutrality:** [`.bequite/principles/TOOL_NEUTRALITY.md`](.bequite/principles/TOOL_NEUTRALITY.md)
- **ADRs:** [`docs/decisions/`](docs/decisions/) (4 decisions)
- **Feature roadmap:** [`.bequite/plans/FEATURE_EXPANSION_ROADMAP.md`](.bequite/plans/FEATURE_EXPANSION_ROADMAP.md)
- **Changelog:** [`docs/changelogs/CHANGELOG.md`](docs/changelogs/CHANGELOG.md)
- **Agent log:** [`docs/changelogs/AGENT_LOG.md`](docs/changelogs/AGENT_LOG.md)

---

## Contributing

BeQuite is opinionated. PRs welcome for:

- New skills (per `bequite-skill-creator` pattern)
- Doctrine packs (per-industry rule packs)
- Bug fixes
- Documentation improvements
- Off-label use case write-ups

Open an issue first for anything that adds a new top-level slash command or changes the gate model.

---

## License

MIT. See [LICENSE](LICENSE).

## Maintainer

**Ahmed Shawky** ([@xpShawky](https://github.com/xpShawky)).

Built in Egypt 🇪🇬. Available in English; doctrine packs for Arabic + RTL on the roadmap.
