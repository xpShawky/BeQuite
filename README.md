# BeQuite

> **Build it right the first time. No chatter. No debug spirals.**

BeQuite is a host-portable harness that turns Claude (and any peer coding agent — GPT-5, Codex, Cursor, Cline, Roo, Kilo) into a senior tech-lead capable of shipping software projects from research to handoff **without producing the broken half-builds that dominate today's "vibe coding" output.**

It ships as three artifacts that share one brain:

1. **A Claude Skill** (`skill/SKILL.md` + agents + commands + hooks + templates) — works inside Claude Code, Claude.ai, Cursor with skills enabled, Codex CLI, OpenCode, Gemini CLI, Kiro, Trae, Rovo, and any SKILL.md-compatible host.
2. **A standalone CLI** (`bequite`, distributable via `uvx` / `pipx`) — modeled on Spec-Kit, with 18 commands (`init, research, constitution, specify, stack, clarify, plan, phases, tasks, analyze, implement, verify, review, handoff, resume, doctor, audit, freshness, auto`) plus the design alias surface from Impeccable.
3. **A GitHub repo template** — `.bequite/{constitution, memory, specs, phases, tasks, prompts, logs, receipts}/`, `AGENTS.md`, `CLAUDE.md`, per-host adapters under `.cursor/`, `.codex/`, `.gemini/`, `.windsurf/`. The same project moves seamlessly between hosts.

By **xpShawky** (Ahmed Shawky).

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
- **Reproducibility receipts** — every phase emits a signed JSON receipt (model, prompt hash, memory snapshot, diff, tests, cost). Auditable AI-generated code.
- **Knowledge-freshness probes** — before any stack pick, `bequite freshness` verifies candidates aren't deprecated, EOL'd, or replaced (catches Stronghold, Roo Code, EV cert obsolescence in 2026).
- **The verification gate** — Playwright walks (admin + user), smoke tests, `axe-core`, secret-scan. No phase exits "done" without acceptance evidence executed in this session.
- **Banned weasel-words** — `should`, `probably`, `seems to`, `appears to`, `I think it works` are exit-code-2 violations in completion messages.

---

## The seven non-skippable phases

| Phase | Output artifact | Owner persona | Gate to next phase |
|---|---|---|---|
| **P0 Research** | `specs/<feature>/research.md` | Researcher | Findings quoted back, user acknowledges |
| **P1 Stack** | `.bequite/memory/decisions/ADR-001-stack.md` | Architect | Educational explainer + scale dialog complete; ADR signed; freshness probe green |
| **P2 Plan** | `specs/<feature>/{spec.md, plan.md, data-model.md, contracts/}` | Architect | Skeptic adversarial review; analyze passes |
| **P3 Phases** | `specs/<feature>/phases/*.md` | ScrumMaster | Each phase has acceptance evidence defined |
| **P4 Tasks** | `specs/<feature>/phases/*/tasks.md` | ScrumMaster | Tasks atomic (≤5 min each), dependency-ordered |
| **P5 Implement** | source code + commits + receipts | Implementer + Reviewer | All tests in this phase green; receipt signed |
| **P6 Verify** | Playwright walks, smoke test, secret scan | QA + Security Auditor | App boots, every route walked admin & user, zero console errors |
| **P7 Handoff** | `HANDOFF.md` + screencast | TechWriter | A second engineer can run locally + deploy from docs alone |

---

## Quickstart

> **Status (May 2026):** the GitHub remote at `https://github.com/xpShawky/BeQuite` exists but is **not yet populated** — the local repo has 13 tags committed but the first push is owner-gated. The CLI is runnable today from a local checkout (`python -m cli.bequite.audit`, `python -m cli.bequite.freshness`); `uvx --from git+...` and `pip install bequite` activate after the first push + the v1.0.0 PyPI publish (`docs/MAINTAINER.md`, drafted v0.14.0).

### Today (from a local checkout)

```bash
git clone https://github.com/xpShawky/BeQuite   # post-first-push
cd BeQuite

# Run the working Python modules directly (v0.4.2 + v0.4.3):
python -m cli.bequite.audit              # Constitution + Doctrine drift detector
python -m cli.bequite.freshness --all    # Knowledge probe (npm/PyPI/crates.io/GitHub)

# Once dependencies are installed (`pip install -e ./cli`):
bequite --version                         # bequite 0.5.0
bequite doctor                            # environment + scaffolding check
bequite memory show                       # print Memory Bank
```

### After v1.0.0 ships

```bash
# Install (post-first-push + v1.0.0 PyPI publish)
uvx --from git+https://github.com/xpShawky/BeQuite bequite --version
# or
pipx install bequite

# Initialize a project
bequite init my-app --doctrine default-web-saas --scale small_saas

# One-click run-to-completion with safety rails (v0.10.0+)
bequite auto --feature add-confirmation-flow --max-cost-usd 10
```

`bequite auto` will run P0 → P7 sequentially with phase-by-phase commits, Skeptic gates at every boundary, hard cost ceiling, hard wall-clock ceiling, and 3-failure-threshold pause-for-human. Auto-mode never bypasses hooks, never auto-runs one-way-door operations (PyPI publish, git push, terraform apply), and never skips Phase 0.

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) (drafted v0.14.0) for the 5-minute path.

---

## Architecture: two layers, one brain

BeQuite is built in two layers sharing a single source of truth (`.bequite/memory/` + `state/` + `evidence/` + `receipts/`):

- **Layer 1 — Harness** (current; v0.1.0 → v1.0.0). SKILL.md + Python CLI + repo template. Markdown + Python 3.11+ + bash hooks. Runs locally on a developer laptop or in CI. Distributable via `uvx`/`pipx`.
- **Layer 2 — Studio** (planned; v2.0.0+). Next.js dashboard + NestJS API + Worker + Postgres. TypeScript pnpm + Turborepo. Reads what Layer 1 writes; the visual surface (project wizard, phase board, evidence viewer, recovery screen).

Layer 1 is the kernel. Layer 2 is the operating system on top of the kernel. The CLI writes the truth; the dashboard displays it.

Sources:
- The original brief that initiated this project: [`BEQUITE_BOOTSTRAP_BRIEF.md`](BEQUITE_BOOTSTRAP_BRIEF.md).
- The expanded master file (introduced post-`v0.1.1`, prescribing the Layer 2 stack): [`BeQuite_MASTER_PROJECT.md`](BeQuite_MASTER_PROJECT.md).
- The merge audit reconciling the two: [`docs/merge/MASTER_MD_MERGE_AUDIT.md`](docs/merge/MASTER_MD_MERGE_AUDIT.md).

## Status

🚧 **Pre-release.** Tracking toward `v1.0.0`. **13 sub-versions tagged** (`v0.1.0` → `v0.5.2`). 24,132 lines across 16 commits, 153 tracked files. **Constitution at v1.2.0** (3 amendments via ADR-008/009/010). Five operational modules: skill orchestrator + AI automation + hooks + scraping (Article VIII) + cybersecurity (Article IX). See [`CHANGELOG.md`](CHANGELOG.md) for per-version detail.

| Sub-version | Goal | Status |
|---|---|---|
| `v0.1.0` | Foundation & Constitution v1.0.0 (7 Iron Laws) | ✅ tagged 2026-05-10 |
| `v0.1.1` | Doctrines pack — 8 default Doctrines | ✅ tagged 2026-05-10 |
| `v0.1.2` | Master-file merge — two-layer architecture; Constitution v1.0.1 | ✅ tagged 2026-05-10 |
| `v0.2.0` | Skill orchestrator + 11 personas + routing.json + config TOML | ✅ tagged 2026-05-10 |
| `v0.2.1` | AI automation skill (n8n/Make/Zapier/Temporal/Inngest; automation-architect persona) | ✅ tagged 2026-05-10 |
| `v0.3.0` | 10 deterministic-gate hook scripts | ✅ tagged 2026-05-10 |
| `v0.4.0` | 12 master-aligned slash commands | ✅ tagged 2026-05-10 |
| `v0.4.1` | 7 BeQuite-unique slash commands (audit, freshness, auto, memory, snapshot, cost, skill-install) | ✅ tagged 2026-05-10 |
| `v0.4.2` | `bequite audit` Python — Constitution + Doctrine drift detector | ✅ tagged 2026-05-10 |
| `v0.4.3` | `bequite freshness` Python — knowledge probe | ✅ tagged 2026-05-10 |
| `v0.5.0` | Python CLI thin wrapper (`bequite` + `bq`; 19 subcommands wired) | ✅ tagged 2026-05-10 |
| `v0.5.1` | Article VIII Scraping & automation discipline (Constitution v1.1.0) | ✅ tagged 2026-05-10 |
| `v0.5.2` | Article IX Cybersecurity & authorized-testing discipline (Constitution v1.2.0) | ✅ tagged 2026-05-10 |
| `v0.6.0` → `v1.0.0` | Verification (Playwright), Impeccable bundle, signed receipts, multi-model, 3 example projects, auto-mode, MENA bilingual, per-host adapters, vibe-handoff exporters, docs, release engineering | 🟡 in progress |
| `v2.0.0+` | Studio (Next.js dashboard + NestJS API + Postgres + Worker) | planned post-`v1.0.0` |

The original brief is preserved at [`BEQUITE_BOOTSTRAP_BRIEF.md`](BEQUITE_BOOTSTRAP_BRIEF.md). The master file (introduced mid-session, post-`v0.1.1`) is preserved at [`BeQuite_MASTER_PROJECT.md`](BeQuite_MASTER_PROJECT.md). The merge audit explaining what was adopted, what was kept, and what was deferred to Studio v2.0.0+ lives at [`docs/merge/MASTER_MD_MERGE_AUDIT.md`](docs/merge/MASTER_MD_MERGE_AUDIT.md).

---

## Doctrine packs

12 Doctrines shipped (mena-bilingual at v0.11.0). Loaded per project via `bequite.config.toml::doctrines`.

| Doctrine | Use case | Shipped in |
|---|---|---|
| `default-web-saas` | Web SaaS with shadcn/ui, tokens.css, Playwright walks, axe-core gate | v0.1.1 |
| `cli-tool` | Pure-CLI tools — semver-strict, man-page generation, bash completions | v0.1.1 |
| `ml-pipeline` | Reproducible training, dataset versioning, GPU-cost discipline | v0.1.1 |
| `desktop-tauri` | Tauri v2 + OS keychain (NOT Stronghold) + notarytool + AzureSignTool + Keygen | v0.1.1 |
| `library-package` | Public-API freezing, semver-strict, no telemetry without opt-in | v0.1.1 |
| `fintech-pci` | PCI DSS controls, audit log retention, cardholder data segregation | v0.1.1 |
| `healthcare-hipaa` | PHI handling, BAA list, audit trail | v0.1.1 |
| `gov-fedramp` | FedRAMP control families, FIPS-validated crypto | v0.1.1 |
| `ai-automation` | n8n / Make / Zapier / Temporal / Inngest expertise; idempotency + retry + DLQ + observability + AI-agent budget discipline | v0.2.1 |
| `vibe-defense` | **Default for `audience: vibe-handoff`.** Extra-strict response to Veracode 2025's 45% OWASP-Top-10 hit rate on AI-generated code. 15 rules: HIGH-SAST blocks merge with 90d-expiring-ADR-override, exact-pinned prod deps, RLS deny-by-default, locked-down CSP, secret-scan on every commit, axe-core every deploy, mandatory `bequite audit` clean. | v0.5.2 |
| `mena-pdpl` | Egyptian PDPL (Law 151/2020), Saudi PDPL (SDAIA), UAE Federal PDPL (Decree-Law 45/2021). Jurisdiction-branched (UAE Federal vs DIFC vs ADGM vs DHCC). | v0.5.2 |
| `eu-gdpr` | GDPR 2016/679 — Art. 6 lawful basis, data subject rights, DPIA, RoPA, breach 72h, DPO, ePrivacy cookie consent, Schrems II + SCCs 2021. Stacks with `mena-pdpl`. | v0.5.2 |
| `mena-bilingual` | Arabic + Egyptian dialect, RTL-by-default, Tajawal/Cairo/Readex Pro | v0.11.0 (planned) |

Doctrines are forkable. See [`docs/DOCTRINE-AUTHORING.md`](docs/DOCTRINE-AUTHORING.md).

---

## Hosts

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

---

## License

MIT. See [`LICENSE`](LICENSE).

## Maintainer

**Ahmed Shawky** ([@xpshawky](https://github.com/xpshawky)).

> ما تتسهلش في الإجابة. رد براحتك. شوف كل الاحتمالات. اقترح إضافات من عندك. فكّر معايا، مش بدالي.
