<div align="center">

# BeQuite

**A disciplined AI-engineering workflow for coding agents — slash commands, expert skills, persistent memory, and quality gates, all in plain markdown.**

**Latest:** `v3.0.0-alpha.24` · MIT · by [@xpShawky](https://github.com/xpShawky)

<a href="commands.md"><img alt="60 commands" src="https://img.shields.io/badge/slash_commands-60-7c3aed?style=flat-square"></a>
<a href="#skills"><img alt="31 skills" src="https://img.shields.io/badge/skills-31-10b981?style=flat-square"></a>
<img alt="zero runtime deps" src="https://img.shields.io/badge/runtime_deps-0-0ea5e9?style=flat-square">
<img alt="markdown only" src="https://img.shields.io/badge/install-markdown_only-f59e0b?style=flat-square">

</div>

---

## What is BeQuite?

BeQuite turns a coding agent into a disciplined senior engineering team. You describe a goal; BeQuite supplies the **workflow** (research → scope → plan → build → test → verify → release), the **expertise** (31 specialist skills the agent loads automatically), the **memory** (a `.bequite/` folder that survives context loss and session breaks), and the **brakes** (workflow gates, hard human approval points, and evidence rules that ban "should probably work" as a completion claim).

It installs into any project as markdown files. No server, no database, no daemon, no dependencies — if you can read it in a text editor, that's all of it.

**Who it's for:** developers and indie builders using Claude Code (or other coding agents) who want consistent, verifiable output instead of one-shot vibes — and freelancers who want the same discipline applied to courses, proposals, knowledge bases, and client work, not just code.

## Why it exists

Coding agents drift. They skip research, forget decisions mid-session, claim "done" without verifying, redesign your architecture while fixing a button, and produce heroes with beautiful headers and broken middles. BeQuite exists to make drift structurally hard:

- **Memory-first** — every command reads project state before acting; decisions persist in files, not fading chat context.
- **Gates** — 23 workflow gates block out-of-order work; 17 hard human gates stop the agent before anything destructive, paid, or irreversible.
- **Evidence over claims** — completion requires command + exit code + output. Weasel words ("should work", "seems to") are banned in completion reports.
- **Confidence as a report** — every plan and task carries a calibrated success percentage with its evidence level, and the number must move as evidence arrives.
- **Guard Pass** — a second-pass review that hunts AI-specific failure modes (hallucinated APIs, hardcoded success, over-mocked tests, stale docs) after work is produced, before it ships.

## Quick start

```powershell
# Windows (run inside the project you want to enhance)
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash
```

Then, in Claude Code:

```
/bequite          → menu: project state + the next 3 recommended commands
/bq-suggest "what I want to do"   → the navigation assistant picks your route
/bq-auto new "Build a booking dashboard for clinics"   → autonomous, gate-aware
```

The installer copies `.claude/commands/` (59 active slash commands + 1 deprecated alias), `.claude/skills/` (31 skills), and scaffolds `.bequite/` memory. It never overwrites existing memory without `--force`. Canonical counts live in [`COMMAND_ID_MAP.md`](.bequite/commands/COMMAND_ID_MAP.md) and [`SKILL_REGISTRY.md`](.bequite/skills/SKILL_REGISTRY.md).

## The BeQuite workflow

Six phases, each with commands and gates:

```
P0 Setup      →  P1 Framing     →  P2 Build       →  P3 Quality     →  P4 Release   →  P5 Memory
init/discover    clarify/research   assign/implement   test/audit       verify/release   memory/recover
mode/doctor      scope/plan         feature/fix        review/red-team  changelog        handoff
```

Walk one phase with `/bq-p0` … `/bq-p5`, or let `/bq-auto` drive end-to-end (it pauses **only** at hard human gates — destructive ops, production touches, payments, secrets, scope contradictions, release pushes).

## Command map

Every command has a stable catalog ID — workflow (`W0.1`–`W5.3`), navigation (`N`), orchestrators (`O`), capabilities (`C`), maintenance (`M`). IDs appear in menus, docs, and every recommendation, so the catalog teaches itself. Full map with purposes, sequencing, and auto-run flags: [`COMMAND_ID_MAP.md`](.bequite/commands/COMMAND_ID_MAP.md) · full reference: [`commands.md`](commands.md).

| Family | Commands |
|---|---|
| **W0 Setup** | `/bequite` · `/bq-init` · `/bq-discover` · `/bq-doctor` · `/bq-mode` · `/bq-new` · `/bq-existing` |
| **W1 Framing** | `/bq-clarify` · `/bq-research` · `/bq-scope` · `/bq-plan` · `/bq-spec` · `/bq-multi-plan` |
| **W2 Build** | `/bq-assign` · `/bq-implement` · `/bq-feature` · `/bq-fix` · `/bq-uiux-variants` · `/bq-live-edit` |
| **W3 Quality** | `/bq-test` · `/bq-audit` · `/bq-review` · `/bq-red-team` |
| **W4 Release** | `/bq-verify` · `/bq-release` · `/bq-changelog` |
| **W5 Memory** | `/bq-memory` · `/bq-recover` · `/bq-handoff` |
| **N Navigation** | `/bq-now` · `/bq-help` · `/bq-explain` · `/bq-suggest` |
| **O Orchestrators** | `/bq-p0`…`/bq-p5` · `/bq-auto` |
| **C Capabilities** | `/bq-presentation` · `/bq-writing-dna` · `/bq-reference` · `/bq-knowledge` · `/bq-course` · `/bq-pain-radar` · `/bq-integrate` · `/bq-proposal` · `/bq-offer` · `/bq-job-finder` · `/bq-make-money` |
| **M Maintenance** | `/bq-update` · `/bq-skill-audit` |

Many commands take argument workflows instead of spawning new commands: `/bq-verify regressions|drift`, `/bq-release readiness|announce|proof|demo-video`, `/bq-plan from-issues|migration`, `/bq-scope from-interview`, `/bq-test from-spec`, `/bq-handoff client`, `/bq-audit client|a11y`, and more — BeQuite deliberately grows arguments, not command count.

## Capability commands

Beyond software workflows, BeQuite ships engines for the work *around* building:

- **`/bq-presentation`** — premium PPTX or HTML decks (design variants, strict source-fidelity or creative mode, motion planning).
- **`/bq-writing-dna`** — extract a reusable writing profile from your samples; generate content in *your* voice (ethics-bound: no fabricated citations, no detector-evasion).
- **`/bq-reference`** — a screenshot, competitor URL, or app flow → design-system extraction + an original, clone-safe rebuild blueprint with mandatory differentiation.
- **`/bq-knowledge`** — a docs pile → searchable knowledge pack, FAQ, glossary, troubleshooting trees, grounded Q&A, and a tool-neutral RAG blueprint (no vector DB installed by default).
- **`/bq-course`** — a full Course Engine: market-gap validation → learner persona → promise/offer → curriculum → lessons/exercises/quizzes → slides → launch plan. Handles text **and scanned/OCR PDFs** (12-rule source intake, page-level confidence, never invents missing content). Arabic/MENA/RTL-aware.
- **`/bq-pain-radar`** — mine *public* complaints in a niche → ranked MVP / service / course / automation opportunities with source confidence. Strict ethics: official APIs, user exports, or public sources only.
- **`/bq-integrate`** — API docs → integration blueprint (auth flow, endpoint map, error matrix, retry/idempotency, rate limits, test plan). Never invents endpoints; unknowns are marked `UNVERIFIED`.
- **`/bq-proposal`** — a job post or RFP → an honest, tailored proposal in your voice with milestones, pricing options, and explicit scope boundaries. Never claims experience you don't have on record.
- **`/bq-offer`** — a skill, niche, or pain point → a sellable productized offer: specific target client, deliverables with explicit exclusions, pricing tiers, a guarantee you can actually honor, outreach, demo idea, and proof checklist. Completes the monetization chain (pain-radar → make-money → offer → proposal → proof). No invented demand, no income hype.
- **`/bq-offer`** — a skill/niche/pain → a sellable productized offer (target client, deliverables + exclusions, pricing tiers, honorable guarantee); `business-system`/`agency` modes build a whole service business. No invented demand, no income hype.
- **`/bq-automation`** — a workflow or bot idea → a tool-neutral automation blueprint (official-API-first, idempotency, retry/failure, secrets, bot safety). Installs nothing.
- **`/bq-local-business`** — an offline business → a practical minimum digital system (MENA/WhatsApp-aware). **`/bq-brand-kit`** — a non-generic brand identity. **`/bq-community`** — a community plan. **`/bq-recording`** — a long video → structured knowledge (transcript-first). **`/bq-start`** — choose how to start (profile vs brand, which platform, niche, career).
- **`/bq-job-finder`** / **`/bq-make-money`** — verified work opportunities and legitimate earning tracks, safety-first.

## How it works together

An **orchestration layer** ties everything into one pipeline — intent → command routing → skill routing → system-design risk check → confidence forecast → plan → implement → Guard Pass → verify → evidence → memory → next steps. A source-of-truth map (`.bequite/state/ORCHESTRATION_MAP.md`) resolves conflicts and makes the agent admit when no capability fits instead of improvising. For risky domains (payments, inventory, bookings, auth, concurrency), a mandatory **System Design Risk Check** answers questions like "one item in stock, two simultaneous buyers — what happens?" before any code is written. The same workflows also lift **smaller and local models**: structure, checklists, evidence rules, and tiered task assignment narrow the gap to frontier models (see the [smaller-models runbook](docs/runbooks/USING_BEQUITE_WITH_SMALLER_MODELS.md) — honest framing, no magic claims).

Two routers, two questions:

- The **Skill Router** answers *"which expert procedures should load?"* — you describe the goal; BeQuite selects from 31 skills (frontend design system, security reviewer, database architect, scraping discipline, localization/RTL, anti-hallucination, …) and tells you what it picked and why. You never name skills manually.
- The **Command Router** answers *"what should happen next?"* — every non-trivial command ends with a recommendation block: the required next step, a 2–6 command set with reasons and auto-run flags, optional accelerators, and "do not run yet" warnings with the blocking gate named.

The **memory system** (`.bequite/`) holds state, gates, decisions, mistakes, research, evidence logs, and per-capability workspaces (courses, proposals, knowledge packs, design DNA…). Commands read it before acting and write back after — which is why a new session, a compacted context, or a different agent can pick up exactly where the last one stopped.

## Skills

31 specialist skills encode senior-practitioner procedure: project architecture, research with verified evidence, product strategy, UX/UI + AI-slop detection, a frontend design-system master that kills "middle-section drift", backend/database/security/DevOps review, testing discipline, scraping & web automation (API-first, robots/ToS-respecting, tool catalog from Scrapy to Playwright to Scrapling), localization/RTL for Arabic/MENA work, delegate planning (strong model architects, cheaper model implements, strong model reviews), anti-hallucination, context engineering, and the Guard Pass. Registry: [`SKILL_REGISTRY.md`](.bequite/skills/SKILL_REGISTRY.md).

## Scenarios

| You want to… | Run | Likely skills | You get |
|---|---|---|---|
| Start a new project | `/bq-auto new "<idea>"` or `/bq-p0` → `/bq-p1` → … | architect, researcher, product-strategist | research report, scope, plan, built + verified project |
| Audit an existing repo | `/bq-existing` → `/bq-discover` → `/bq-audit` | researcher, security-reviewer, frontend-quality | discovery report + full audit with evidence |
| Fix a bug safely | `/bq-fix "<symptom>"` | problem-solver (+ domain) | reproduced root cause, smallest patch, regression guard |
| Build a feature | `/bq-feature "<title>"` | per 12-type router | scoped mini-cycle: plan → build → test → continuity checks |
| Explore UI directions | `/bq-uiux-variants 5 "<task>"` | frontend-design-system, ux-ui-designer | 5 isolated design directions; you pick the winner |
| Create a course | `/bq-course "<idea>"` | researcher, writing-dna, presentation-builder | validation → curriculum → lessons → slides briefs → launch plan |
| Build a knowledge pack | `/bq-knowledge build "<docs>"` | researcher, anti-hallucination | chunked pack, FAQ, glossary, troubleshooting, RAG blueprint |
| Extract a design direction | `/bq-reference screenshot "<goal>"` | frontend-design-system | design extraction + originality guardrails + rebuild blueprint |
| Find pain in a niche | `/bq-pain-radar "<niche>"` | researcher, make-money | pain map + ranked opportunity briefs with confidence |
| Turn a job post into a proposal | `/bq-proposal "<post>"` | writing-dna, product-strategist | honest proposal + milestones + pricing options + questions |
| Plan an API integration | `/bq-integrate "<docs URL>"` | backend-architect, security-reviewer | blueprint: auth, endpoints, errors, retries, tests |
| Prepare a release | `/bq-verify` → `/bq-release readiness` | release-gate, devops-cloud | verification evidence + ship/no-ship scorecard + launch kit |
| Hand off to a client | `/bq-handoff client` | context-engineer, security-reviewer | runbooks, credential checklist (no values), maintenance calendar |
| Use BeQuite outside Claude Code | follow the [outside-Claude-Code runbook](docs/runbooks/USING_BEQUITE_OUTSIDE_CLAUDE_CODE.md) | manual skill selection | same playbooks + memory with Codex/Cursor/other agents |

## Cross-agent compatibility

BeQuite is Claude-Code-first, but ~85% of it is agent-agnostic by construction: every command is a readable markdown playbook, and the memory contract is plain files. Codex/ChatGPT-style agents, Cursor, and other harnesses can run BeQuite playbooks today via the [compatibility strategy](docs/architecture/CROSS_AGENT_COMPATIBILITY_STRATEGY.md), the [outside-Claude-Code runbook](docs/runbooks/USING_BEQUITE_OUTSIDE_CLAUDE_CODE.md), and the [agent matrix](docs/specs/AGENT_COMPATIBILITY_MATRIX.md). **Per-agent setup** (Antigravity, Gemini CLI, Cursor, Codex app+CLI, Kimi, MiniMax, DeepSeek, Ollama, OpenClaw, Hermes — Windows/macOS/Linux, global or per-project): [INSTALL_FOR_OTHER_AGENTS.md](docs/runbooks/INSTALL_FOR_OTHER_AGENTS.md). What doesn't port (and what to do about it) is documented honestly: slash invocation, skill auto-attach, and the opt-in safety hooks.

## Design philosophy

**Lightweight on purpose.** No Studio app, no heavy CLI/TUI, no dashboard, no Docker, no database — markdown in, markdown out (see ADR-001 and ADR-004 in `docs/decisions/`). **Tool-neutral:** named tools are candidates, never defaults; every significant pick runs through ten decision questions and gets a recorded rationale. **Anti-bloat:** new capabilities must justify their shape (command vs skill vs argument vs template vs docs) through a taxonomy before being built — that's why 52 commands cover what could have sprawled into 100. **Honest by contract:** unverified means saying `UNVERIFIED`; opt-in hooks can machine-enforce the safety subset (destructive-op blocking, secret scanning, weasel-word interception — review before enabling).

## Update · Docs · Roadmap

- **Update:** `/bq-update` — refreshes commands/skills/docs from GitHub, backs up first, never touches your project memory.
- **Docs:** [`commands.md`](commands.md) (full reference) · [`docs/specs/COMMAND_CATALOG.md`](docs/specs/COMMAND_CATALOG.md) · [`docs/runbooks/`](docs/runbooks/) (install, usage, outside-Claude-Code) · [`docs/architecture/`](docs/architecture/) (the strategy layer) · [`docs/changelogs/CHANGELOG.md`](docs/changelogs/CHANGELOG.md).
- **Roadmap:** newest command is `/bq-offer` (alpha.23, not yet live-tested); parked candidates (automation builder, data-to-product, agent-pack generator, and more) live in the canonical ledger `.bequite/tasks/REMAINING_WORK_MASTER.md` with explicit promotion conditions.

## Contributing & license

Issues and PRs welcome at [xpShawky/BeQuite](https://github.com/xpShawky/BeQuite). Keep contributions markdown-only and dependency-free; new commands/skills must pass the shape taxonomy and update the ID map + registry in the same PR. **License:** MIT.
