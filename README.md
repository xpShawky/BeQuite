# BeQuite

> **Build it right the first time. No chatter. No debug spirals.**

BeQuite is a host-portable harness that turns Claude (and any peer coding agent — GPT-5, Codex, Cursor, Cline, Roo, Kilo) into a senior tech-lead capable of shipping software projects from research to handoff **without producing the broken half-builds that dominate today's "vibe coding" output.**

By **xpShawky** ([Ahmed Shawky](https://github.com/xpShawky)).

[![v1.0.3](https://img.shields.io/badge/release-v1.0.3-E5B547?style=flat&labelColor=0a0a0a)](docs/RELEASES/v1.0.0.md) [![v2.0.0-alpha.2](https://img.shields.io/badge/studio-v2.0.0--alpha.2-E5B547?style=flat&labelColor=0a0a0a)](docs/RELEASES/v2.0.0-alpha.1.md) [![Constitution v1.3.0](https://img.shields.io/badge/Constitution-v1.3.0-E5B547?style=flat&labelColor=0a0a0a)](.bequite/memory/constitution.md) [![License: MIT](https://img.shields.io/badge/License-MIT-E5B547?style=flat&labelColor=0a0a0a)](LICENSE)

---

## Install — one command (vibecoder-friendly)

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.ps1 | iex
```

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.sh | bash
```

That's it. The bootstrap will:

1. Check that **Python 3.11+** and **git** are installed — and tell you exactly how to install them if they're not (one-click installer links).
2. Clone the repo into `./BeQuite/`.
3. Create a Python venv inside the clone.
4. Install the `bequite` CLI in editable mode.
5. Verify everything works.
6. Print the next-step commands.

**Want the Studio (dashboard + marketing + API) too?**

```powershell
# Windows
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.ps1))) -Studio
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.sh | bash -s -- --studio
```

---

## Run — three commands

```bash
# 1. Enter the project + activate the venv (every new shell)
cd BeQuite
# Windows:  .\.venv\Scripts\Activate.ps1
# Unix:     source ./.venv/bin/activate

# 2. Read the friendly first-time guide
bequite quickstart

# 3. Initialize a new project + run the full workflow
bequite init my-app --doctrine default-web-saas
cd my-app
bequite auto --feature "add health endpoint" --max-cost-usd 10
```

`bequite auto` runs the **7-phase workflow** (Research → Stack → Plan → Phases → Tasks → Implement → Verify → Handoff) sequentially with phase-by-phase commits, Skeptic gates at every boundary, hard cost ceiling, hard wall-clock ceiling, and a 3-failure-threshold pause-for-human. It never bypasses hooks, never runs one-way-door operations, and never skips Phase 0.

---

## What ships

Two layers, one brain — both shipping today:

### 🧠 Layer 1 Harness — `v1.0.3` (Production/Stable)

The CLI + Skill + Memory Bank + Hooks + Doctrines + Templates. Markdown + Python 3.11+ + bash hooks. Distributable via `uvx`/`pipx`/`pip install` (once PyPI publish lands).

**[→ v1.0.0 release notes](docs/RELEASES/v1.0.0.md)**

### 🎨 Layer 2 Studio — `v2.0.0-alpha.2` (First pre-release)

The visual surface — three Next.js + Hono apps sharing the gold-on-black brand:

- **`studio/marketing/`** — cinematic landing page (Apple-grade scroll choreography) + 6 deep MDX vibecoder tutorials at `/docs`.
- **`studio/dashboard/`** — operations console with dual-mode loader (filesystem ↔ HTTP), live SSE updates, xterm.js terminal in HTTP mode.
- **`studio/api/`** — Hono on Bun back-end. Three-mode auth, append-only writes, four SSE streams, terminal exec (allow-list-gated per ADR-016).

**[→ v2.0.0-alpha.1 release notes](docs/RELEASES/v2.0.0-alpha.1.md)**

---

## Why BeQuite exists

Current AI coding tools routinely:

- Build a frontend without a working backend.
- Hallucinate libraries (the **PhantomRaven** campaign — Koi Security, 2025 — exploited 126 such hallucinated names).
- Generate UIs with the same AI-slop tells (Inter font by default, purple-blue gradients, nested cards, gray-on-color text, bounce easings).
- Leak secrets to client code (Veracode 2025 GenAI Code Security Report: ~45% of generated code samples have OWASP Top-10 issues).
- Hand off "I built X, please test" without ever booting the app themselves.
- Lose all context between sessions.
- Pick stacks silently — no explanation, no scale check, no ADR.

BeQuite **prevents these errors with deterministic gates** instead of fixing them after the fact:

- **A versioned Constitution** — Iron Laws (universal) + forkable Doctrines (per project type).
- **A six-file Memory Bank** (Cline pattern) — durable cross-session brain.
- **PreToolUse hooks** that block destructive operations, secret writes, and hallucinated package imports.
- **Skeptic-as-adversary** at every phase boundary — distinct from the Reviewer; produces kill-shot questions before phases exit.
- **Reproducibility receipts** — every phase emits an ed25519-signed JSON receipt (model, prompt hash, memory snapshot, diff, tests, cost). Auditable AI-generated code.
- **Knowledge-freshness probes** — before any stack pick, `bequite freshness` verifies candidates aren't deprecated, EOL'd, or replaced.
- **The verification gate** — Playwright walks (admin + user), smoke tests, `axe-core`, secret-scan. No phase exits "done" without acceptance evidence executed in this session.
- **Banned weasel-words** — `should`, `probably`, `seems to`, `appears to`, `I think it works` are exit-code-2 violations in completion messages.
- **Iron Law X — operational completeness** (v0.16.0+). Every change reports the *fully working* state — build re-run, docker-compose'd, frontend wired to backend. The "feature added but needs restart" pain is solved by construction.

---

## The seven non-skippable phases

| Phase | Output artifact | Owner persona | Gate to next phase |
|---|---|---|---|
| **P0 Research** | `specs/<feature>/research.md` | Researcher | Findings quoted back, user acknowledges |
| **P1 Stack** | `.bequite/memory/decisions/ADR-001-stack.md` | Architect | Educational explainer + scale dialog complete; ADR signed; freshness probe green |
| **P2 Plan** | `specs/<feature>/{spec.md, plan.md, data-model.md, contracts/}` | Architect | Skeptic adversarial review; analyze passes |
| **P3 Phases** | `specs/<feature>/phases/*.md` | ScrumMaster | Each phase has acceptance evidence defined |
| **P4 Tasks** | `specs/<feature>/phases/*/tasks.md` | ScrumMaster | Tasks atomic (≤5 min each), dependency-ordered |
| **P5 Implement** | source code + commits + signed receipts | Implementer + Reviewer | All tests in this phase green; receipt signed |
| **P6 Verify** | Playwright walks, smoke test, secret scan, axe-core | QA + Security Auditor | App boots, every route walked admin & user, zero console errors |
| **P7 Handoff** | `HANDOFF.md` + screencast | TechWriter | A second engineer can run locally + deploy from docs alone |

---

## Quickstart

```bash
# Install (post-PyPI publish; one-way door — Ahmed-gated)
uvx bequite --version
# or
pipx install bequite
# or
pip install bequite

# Initialize a project
bequite init my-app --doctrine default-web-saas --scale small_saas

# One-click run-to-completion with safety rails
bequite auto --feature add-confirmation-flow --max-cost-usd 10
```

`bequite auto` runs P0 → P7 sequentially with phase-by-phase commits, Skeptic gates at every boundary, hard cost ceiling, hard wall-clock ceiling, and a 3-failure-threshold pause-for-human. Auto-mode never bypasses hooks, never auto-runs one-way-door operations (PyPI publish, git push, terraform apply), and never skips Phase 0.

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for the 5-minute path.

---

## Doctrine packs (13)

Loaded per project via `bequite.config.toml::doctrines`. Forkable. See [`docs/DOCTRINE-AUTHORING.md`](docs/DOCTRINE-AUTHORING.md).

| Doctrine | Use case |
|---|---|
| `default-web-saas` | Web SaaS with shadcn/ui, tokens.css, Playwright walks, axe-core gate |
| `cli-tool` | Pure-CLI tools — semver-strict, man-page generation, bash completions |
| `ml-pipeline` | Reproducible training, dataset versioning, GPU-cost discipline |
| `desktop-tauri` | Tauri v2 + OS keychain (NOT Stronghold) + notarytool + AzureSignTool + Keygen |
| `library-package` | Public-API freezing, semver-strict, no telemetry without opt-in |
| `fintech-pci` | PCI DSS controls, audit log retention, cardholder data segregation |
| `healthcare-hipaa` | PHI handling, BAA list, audit trail |
| `gov-fedramp` | FedRAMP control families, FIPS-validated crypto |
| `ai-automation` | n8n / Make / Zapier / Temporal / Inngest expertise; idempotency + retry + DLQ |
| `vibe-defense` | **Default for `audience: vibe-handoff`.** 15 extra-strict rules — HIGH-SAST blocks merge, exact-pinned prod deps, RLS deny-by-default, locked-down CSP, mandatory `bequite audit` clean. |
| `mena-pdpl` | Egyptian PDPL (Law 151/2020), Saudi PDPL (SDAIA), UAE Federal PDPL. Jurisdiction-branched (UAE Federal vs DIFC vs ADGM vs DHCC). |
| `eu-gdpr` | GDPR 2016/679 — Art. 6, data subject rights, DPIA, RoPA, breach 72h, Schrems II + SCCs 2021. Stacks with `mena-pdpl`. |
| `mena-bilingual` | Arabic + Egyptian dialect, RTL-by-default, Tajawal/Cairo/Readex Pro |

---

## Hosts (9)

BeQuite runs first-class in:

- **Claude Code** (the reference host — uses native skills, hooks, settings.json)
- **Cursor** (`.cursor/skills/SKILL.md` + `.cursor/rules/*.mdc`)
- **Codex CLI** (via `AGENTS.md`)
- **Gemini CLI** (via `.gemini/`)
- **Windsurf** (via `.windsurf/`)
- **Cline** (via Memory Bank — natively compatible)
- **Kilo Code** (Cline + Roo + autocomplete fork)
- **Continue.dev** (compliance-friendly, on-prem deployable)
- **Aider** (architect mode wrap)

Per-host install is one command: `bequite skill install`. See [`docs/HOSTS.md`](docs/HOSTS.md).

---

## Architecture: two layers, one brain

BeQuite is built in two layers sharing a single source of truth (`.bequite/memory/` + `state/` + `evidence/` + `receipts/`):

```
┌─────────────────────────────────────────────────────────────┐
│                     Source of truth                         │
│  .bequite/memory/  +  state/  +  evidence/  +  receipts/    │
└──────────────┬──────────────────────────┬───────────────────┘
               │                          │
       ┌───────▼────────┐         ┌───────▼─────────────┐
       │  Layer 1       │         │  Layer 2            │
       │  Harness       │         │  Studio Edition     │
       │  (v1.0.0)      │         │  (v2.0.0-alpha.1)   │
       │                │         │                     │
       │  • SKILL.md    │         │  • marketing/  :3000│
       │  • bequite CLI │         │  • dashboard/  :3001│
       │  • Hooks       │         │  • api/        :3002│
       │  • Doctrines   │         │                     │
       │  • Templates   │         │  Reads what Layer 1 │
       └────────────────┘         │  writes; the visual │
       Writes the truth.          │  surface.           │
                                  └─────────────────────┘
```

Layer 1 is the kernel. Layer 2 is the operating system on top of the kernel.

---

## Status

**v1.0.0 = Production/Stable.** All sub-versions from `v0.1.0` through `v0.20.5` consolidated into v1.0.0. See [`CHANGELOG.md`](CHANGELOG.md) for per-version detail. Sources:

- The original brief that initiated this project: [`BEQUITE_BOOTSTRAP_BRIEF.md`](BEQUITE_BOOTSTRAP_BRIEF.md).
- The expanded master file (introduced post-`v0.1.1`, prescribing the Layer 2 stack): [`BeQuite_MASTER_PROJECT.md`](BeQuite_MASTER_PROJECT.md).
- The merge audit reconciling the two: [`docs/merge/MASTER_MD_MERGE_AUDIT.md`](docs/merge/MASTER_MD_MERGE_AUDIT.md).

---

## Acknowledgements

BeQuite stands on the shoulders of:

- **[Spec-Kit](https://github.com/github/spec-kit)** — spec-driven workflow grammar
- **[Cline Memory Bank](https://docs.cline.bot/features/memory-bank)** — six-file durable memory pattern
- **[BMAD-Method](https://github.com/bmad-code-org/BMAD-METHOD)** — phase decomposition + persona patterns
- **[Superpowers (Jesse Vincent)](https://github.com/obra/superpowers)** — TDD + brainstorm + plan workflow
- **[Aider architect mode](https://aider.chat/2024/09/26/architect.html)** — frontier reasoner / cheap editor split
- **[Impeccable (Paul Bakaus)](https://github.com/pbakaus/impeccable)** — design language and 23 UI/UX commands; bundled (pinned snapshot, MIT) as the default frontend Doctrine
- **[Anthropic Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)** — SKILL.md format
- **[AGENTS.md](https://agents.md/)** — universal coding-agent entry, stewarded by the Linux Foundation Agentic AI Foundation
- **[Playwright MCP (Microsoft)](https://github.com/microsoft/playwright-mcp)** — accessibility-first verification
- **[shadcn/ui](https://ui.shadcn.com/)** + **[tweakcn](https://tweakcn.com/)** + **[21st.dev Magic](https://21st.dev/)** + **[context7](https://github.com/upstash/context7)** — frontend module
- **[Hono](https://hono.dev/)** — the smallest possible TS edge backend, powering the Studio API
- **[xterm.js](https://xtermjs.org/)** — live terminal renderer

---

## License

MIT. See [`LICENSE`](LICENSE).

## Maintainer

**Ahmed Shawky** ([@xpShawky](https://github.com/xpShawky)).
