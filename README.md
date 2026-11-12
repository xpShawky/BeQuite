<div align="center">

# BeQuite

**A disciplined AI-engineering and creative workflow for coding agents: slash commands, expert skills, persistent memory, and quality gates, all in plain markdown.**

**Latest:** `v4.0.0` "Titan" · MIT · by [@xpShawky](https://github.com/xpShawky)

<a href="commands.md"><img alt="55 commands" src="https://img.shields.io/badge/slash_commands-55-7c3aed?style=flat-square"></a>
<a href="#skills"><img alt="35 skills" src="https://img.shields.io/badge/skills-35-10b981?style=flat-square"></a>
<img alt="zero runtime deps" src="https://img.shields.io/badge/runtime_deps-0-0ea5e9?style=flat-square">
<img alt="markdown only" src="https://img.shields.io/badge/install-markdown_only-f59e0b?style=flat-square">

</div>

---

## What is BeQuite?

BeQuite turns a coding agent into a disciplined senior team. You describe a goal; BeQuite supplies:

- **the workflow:** research → scope → plan → build → test → verify → release;
- **the expertise:** 35 specialist skills the agent selects and announces before it acts;
- **the memory:** a `.bequite/` folder with **one folder per piece of work**, so nothing is lost between sessions;
- **the brakes:** gates, hard human approval points, plan-first approval, and evidence rules that ban "should probably work" as a completion claim.

It installs into any project as markdown. No server, no database, no daemon, no dependencies.

**Who it's for:** developers and indie builders using Claude Code (or other coding agents) who want consistent, verifiable output, and creators who want the same discipline for films, courses, proposals and client work.

## What's new in v4 "Titan"

- **Work folders.** Every feature, fix, film or course gets `.bequite/work/NNNN-slug/` with its own brief, research, spec, plan, tasks, gates, evidence and log, Spec Kit / OpenSpec style. Gates are per work; finished work converges, merges into living specs and is archived. New `/bq-work`.
- **Motion studio.** `/bq-motion` directs a film like a motion director: references → script and beats → style lock → tool and render plan → animatic → build rounds → voice and sound → render and QC → platform recuts, launch posts and a making-of guide. It is plan-first and tool-neutral (After Effects, Remotion/HyperFrames, Blender, DaVinci Resolve, AI video), and it stops before paid credits, the final render and any posting.
- **Web motion that stays fast on phones.** Scroll stories, frame sequences, depth and 3D with a mobile performance budget, full / lite / static device tiers, and a `PERF_BUDGET_PASS` gate.
- **Rules that are checked, not just written.** Every action command carries the same contract block (skills first, resolve the work, gates, plan first, evidence, write back), and `scripts/bq_check.py` runs in CI.
- **Clean installs.** Your project gets a clean memory scaffold (earlier versions leaked BeQuite's own logs into it), plus BeQuite's reference docs, so every pointer in a command resolves.
- **Leaner.** v2 leftovers removed (kept on the `archive/v2` branch), `/bq-p0`…`/bq-p5` folded into `/bq-auto phase=…`, `/bq-now` folded into `/bequite short`.

Full notes: [CHANGELOG.md](CHANGELOG.md).

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
/bequite                                    menu: project state + next recommended commands
/bq-suggest "what I want to do"             the navigation assistant picks your route
/bq-auto new "Build a booking dashboard for clinics"
/bq-motion "45s launch film for my app, Apple-style, 16:9 + 9:16"
```

The installer copies `.claude/commands/`, `.claude/skills/`, BeQuite's reference docs (`.claude/bequite/`), the opt-in safety hooks, and a clean `.bequite/` scaffold. Re-running with `--force` (`$env:BEQUITE_FORCE=1` on Windows) refreshes commands and skills; **your project memory is never overwritten.**

## How it works

```
.bequite/
  ACTIVE.md          which piece of work is active
  work/0007-launch-film/
    brief · research · spec · plan · tasks · gates · evidence · review · verify · log
    assets/ outputs/
  specs/             the living truth that finished work merges into
  archive/           closed work, by date
  state/ logs/ ...   project-wide memory: mode, gates, decisions, mistake memory, design DNA
```

Every command follows one **contract**: announce the skills it will use → resolve the active work → check gates → plan first for non-trivial work → write evidence (command + exit code + output) → write back to the work log and project memory → end with the next recommended commands. Contract: [COMMAND_EXECUTION_CONTRACT.md](.claude/bequite/docs/architecture/COMMAND_EXECUTION_CONTRACT.md) · work folders: [WORK_FOLDERS.md](.claude/bequite/docs/architecture/WORK_FOLDERS.md).

Two routers, two questions:

- The **Skill Router** answers *"which expert procedures should load?"* You describe the goal; BeQuite selects from 35 skills and says what it picked and why.
- The **Command Router** answers *"what should happen next?"* Every non-trivial command ends with the required next step, a short recommended set, and "do not run yet" warnings with the blocking gate named.

For risky domains (payments, inventory, bookings, auth, concurrency), a **System Design Risk Check** answers questions like "one item in stock, two buyers at once: what happens?" before any code is written. A **Guard Pass** hunts AI-specific failure modes (hallucinated APIs, hardcoded success, over-mocked tests, stale docs) before anything ships.

## Operating modes

Composable depth and cost flags for any command: `deep` (full research and red-team), `fast` (short discovery, still tests and verifies), `token-saver` (focused reads, reuse cached research), and `delegate` (a strong model plans and reviews, a cheaper model implements). Hard human gates apply in every mode.

## Command map

Every command has a stable catalog ID: workflow (`W`), navigation (`N`), orchestrator (`O`), capability (`C`), maintenance (`M`). Full map: [COMMAND_ID_MAP.md](templates/bequite/commands/COMMAND_ID_MAP.md) · reference: [commands.md](commands.md).

| Family | Commands |
|---|---|
| **W0 Setup** | `/bequite` · `/bq-init` · `/bq-discover` · `/bq-doctor` · `/bq-mode` · `/bq-new` · `/bq-existing` · `/bq-work` |
| **W1 Framing** | `/bq-clarify` · `/bq-research` · `/bq-scope` · `/bq-plan` · `/bq-spec` · `/bq-multi-plan` |
| **W2 Build** | `/bq-assign` · `/bq-implement` · `/bq-feature` · `/bq-fix` · `/bq-uiux-variants` · `/bq-live-edit` |
| **W3 Quality** | `/bq-test` · `/bq-audit` · `/bq-review` · `/bq-red-team` |
| **W4 Release** | `/bq-verify` · `/bq-release` · `/bq-changelog` |
| **W5 Memory** | `/bq-memory` · `/bq-recover` · `/bq-handoff` |
| **N Navigation** | `/bq-help` · `/bq-explain` · `/bq-suggest` |
| **O Orchestrator** | `/bq-auto` (18 intents, `phase=P0..P5`) |
| **C Capabilities** | `/bq-presentation` · `/bq-writing-dna` · `/bq-reference` · `/bq-knowledge` · `/bq-course` · `/bq-pain-radar` · `/bq-integrate` · `/bq-proposal` · `/bq-job-finder` · `/bq-make-money` · `/bq-offer` · `/bq-automation` · `/bq-local-business` · `/bq-brand-kit` · `/bq-community` · `/bq-recording` · `/bq-start` · `/bq-motion` |
| **M Maintenance** | `/bq-update` · `/bq-skill-audit` · `/bq-hooks` |

Many commands take argument workflows instead of new commands (`/bq-verify drift`, `/bq-release readiness`, `/bq-plan migration`, `/bq-handoff client`, `/bq-spec export=speckit`, ...). BeQuite grows arguments, not command count.

## Motion studio

`/bq-motion` directs a film; it does not "make an animation". The flow, with a ✋ wherever it waits for your yes:

| Phase | Output | ✋ |
|---|---|---|
| M0 Brief · M1 References | goal, audience, platforms, budget; 2-3 reference options from your `motion-library/` ("we could do it like X or like Y, because…") | |
| M2 Script + beats | script, story shape, beat sheet (≤ 3 s per beat), a type treatment per line | ✋ |
| M3 Style lock | 2-3 styleframes of the same key frame → Motion DNA | ✋ |
| M4 Tool + render plan | engine per shot with reasons, render plan, every paid credit priced | ✋ |
| M5 Animatic · M6 Build rounds | timing with a free scratch voice; contact sheets and phone previews per round | ✋ picture lock |
| M7 Voice + sound | voice auditions in the mix, music edited to picture, sparse SFX, −14 LUFS master | ✋ before paid credits |
| M8 Render + QC · M9 Delivery | QC with commands; real recuts per platform (reframed, not letterboxed), captions, posts for Instagram / TikTok / Facebook / LinkedIn, comment-to-DM plan, making-of guide | ✋ final render · you post |

`motion-library/` is your reference memory: drop films into `motion-library/inbox/`, run `/bq-motion study`, and each film gets a written breakdown (story, beats, techniques, when to use it). Films and frames stay local; only the breakdowns are tracked.

## Capability commands

Beyond software workflows, BeQuite ships engines for the work *around* building:

- **`/bq-presentation`**: premium PPTX or HTML decks (design variants, strict source fidelity or creative mode, motion planning).
- **`/bq-writing-dna`**: a reusable writing profile from your samples; content in *your* voice (no fabricated citations, no detector evasion).
- **`/bq-reference`**: a screenshot, competitor URL or app flow → design extraction plus an original, clone-safe rebuild blueprint.
- **`/bq-knowledge`**: a pile of docs → a searchable knowledge pack, FAQ, glossary, troubleshooting trees and a tool-neutral RAG blueprint.
- **`/bq-course`**: market-gap validation → learner persona → curriculum → lessons and quizzes → slides → launch plan; handles scanned/OCR PDFs; Arabic/MENA/RTL-aware.
- **`/bq-pain-radar`**: public complaints in a niche → ranked MVP / service / course / automation opportunities (official APIs and public sources only).
- **`/bq-integrate`**: API docs → integration blueprint; never invents endpoints (unknowns are marked `UNVERIFIED`).
- **`/bq-proposal`**: a job post or RFP → an honest, tailored proposal with milestones, pricing options and scope boundaries.
- **`/bq-offer`**: a skill, niche or pain → a sellable productized offer; `business-system` / `agency` modes build a whole service business. No invented demand, no income hype.
- **`/bq-automation`**: a workflow or bot idea → a tool-neutral automation blueprint (official API first, idempotency, retries, secrets, bot safety). Installs nothing.
- **`/bq-local-business`** (offline business → minimum digital system) · **`/bq-brand-kit`** (non-generic identity) · **`/bq-community`** (community plan) · **`/bq-recording`** (long video → structured knowledge) · **`/bq-start`** (choose how to start).
- **`/bq-job-finder`** / **`/bq-make-money`**: verified work opportunities and legitimate earning tracks, safety-first.

Honest status: the capability commands are complete playbooks but most have not yet run on a real project; the first live runs will tune them.

## Skills

35 specialist skills encode senior-practitioner procedure: project architecture, verified research, product strategy, UX/UI and AI-slop detection, a frontend design-system master (Design DNA, section-by-section continuity, web motion with a performance budget), backend / database / security / DevOps review, testing discipline, scraping and automation, localization/RTL for Arabic/MENA, delegate planning, anti-hallucination, context engineering, the Guard Pass, and the motion team (director, kinetic type, sound and voice, render pipeline). Registry: [SKILL_REGISTRY.md](templates/bequite/skills/SKILL_REGISTRY.md).

## Scenarios

| You want to… | Run | You get |
|---|---|---|
| Start a new project | `/bq-auto new "<idea>"` | research, scope, plan (approved by you), built and verified project |
| Audit an existing repo | `/bq-existing` → `/bq-discover` → `/bq-audit` | discovery report and full audit with evidence |
| Fix a bug safely | `/bq-fix "<symptom>"` | reproduced root cause, smallest patch, regression test |
| Build a feature | `/bq-feature "<title>"` | its own work folder: spec → plan → build → test → verify |
| Make a launch film or reel | `/bq-motion "<idea>"` | reference options, script, styleframes, render plan, film, recuts, posts |
| Explore UI directions | `/bq-uiux-variants 5 "<task>"` | 5 isolated design directions; you pick the winner |
| Create a course | `/bq-course "<idea>"` | validation → curriculum → lessons → slide briefs → launch plan |
| Turn a job post into a proposal | `/bq-proposal "<post>"` | honest proposal, milestones, pricing options |
| Prepare a release | `/bq-verify` → `/bq-release readiness` | verification evidence and a ship / no-ship scorecard |
| Use BeQuite outside Claude Code | [outside-Claude-Code runbook](.claude/bequite/docs/runbooks/USING_BEQUITE_OUTSIDE_CLAUDE_CODE.md) | the same playbooks and memory with other agents |

## Cross-agent compatibility

BeQuite is Claude-Code-first, but most of it is agent-agnostic: every command is a readable markdown playbook and the memory contract is plain files. Per-agent setup (Antigravity, Gemini CLI, Cursor, Codex, Kimi, MiniMax, DeepSeek, Ollama and others; Windows / macOS / Linux): [INSTALL_FOR_OTHER_AGENTS.md](.claude/bequite/docs/runbooks/INSTALL_FOR_OTHER_AGENTS.md) · [agent matrix](.claude/bequite/docs/specs/AGENT_COMPATIBILITY_MATRIX.md). What doesn't port (slash invocation, skill auto-attach, the opt-in hooks) is documented honestly. Smaller and local models: [smaller-models runbook](.claude/bequite/docs/runbooks/USING_BEQUITE_WITH_SMALLER_MODELS.md).

## Design philosophy

**Lightweight on purpose:** no Studio app, no heavy CLI, no dashboard, no Docker, no database. **Tool-neutral:** named tools are candidates, never defaults; every significant pick runs through ten decision questions and gets a recorded reason. **Anti-bloat:** a new capability must justify its shape (command vs skill vs argument vs template) before it is built. **Honest by contract:** unverified means saying `UNVERIFIED`; opt-in hooks can machine-enforce the safety subset (destructive-op blocking, secret scanning, weasel-word interception; review before enabling with `/bq-hooks`).

## Update · docs · contributing

- **Update:** `/bq-update` refreshes commands, skills and docs, backs up first, and never touches your project memory.
- **Safety hooks (opt-in):** `/bq-hooks status|enable|disable|test`. Off by default because they run shell on every tool call. See [CLAUDE_CODE_HOOKS_STRATEGY.md](.claude/bequite/docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md).
- **Docs:** [commands.md](commands.md) · [usage guide](.claude/bequite/docs/runbooks/USING_BEQUITE_COMMANDS.md) · [architecture](.claude/bequite/docs/architecture/) · [specs](.claude/bequite/docs/specs/) · [decisions](.claude/bequite/docs/decisions/) · [CHANGELOG.md](CHANGELOG.md).
- **Contributing:** issues and PRs welcome at [xpShawky/BeQuite](https://github.com/xpShawky/BeQuite). Keep contributions markdown-first and dependency-free, and run `python3 scripts/bq_check.py` before a PR (CI runs it too).

**License:** MIT.
