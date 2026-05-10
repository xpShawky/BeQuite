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

## Quickstart (after v1.0.0 ships)

```bash
# Install
uvx --from git+https://github.com/xpshawky/bequite bequite --version

# Initialize a project
uvx bequite init my-app --doctrine default-web-saas --scale 5000

# One-click run-to-completion (with safety rails)
uvx bequite auto --feature add-confirmation-flow --max-cost-usd 10
```

`bequite auto` runs P0 → P7 sequentially with phase-by-phase commits, Skeptic gates at every boundary, hard cost ceiling, hard wall-clock ceiling, and 3-failure-threshold pause-for-human. Auto-mode never bypasses hooks, never auto-runs one-way-door operations (PyPI publish, git push, terraform apply), and never skips Phase 0.

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md) for the 5-minute path.

---

## Status

🚧 **Pre-release.** Tracking toward `v1.0.0`. See [`CHANGELOG.md`](CHANGELOG.md) for the sub-version progress (`v0.1.0` → `v1.0.0`).

The full [build plan](docs/HOW-IT-WORKS.md) lives under `docs/`. The original brief that initiated this project is preserved at `BEQUITE_BOOTSTRAP_BRIEF.md`.

---

## Doctrine packs (v1.0.0)

| Doctrine | Use case |
|---|---|
| `default-web-saas` | Web SaaS with shadcn/ui, tokens.css, Playwright walks, axe-core gate |
| `cli-tool` | Pure-CLI tools — semver-strict, man-page generation, bash completions |
| `ml-pipeline` | Reproducible training, dataset versioning, GPU-cost discipline |
| `desktop-tauri` | Tauri v2 + OS keychain (NOT Stronghold) + notarytool + AzureSignTool + Keygen |
| `library-package` | Public-API freezing, semver-strict, no telemetry without opt-in |
| `mena-bilingual` | Arabic + Egyptian dialect, RTL-by-default, Tajawal/Cairo/Readex Pro |
| `fintech-pci` | PCI DSS controls, audit log retention, cardholder data segregation |
| `healthcare-hipaa` | PHI handling, BAA list, audit trail |
| `gov-fedramp` | FedRAMP control families, FIPS-validated crypto |

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
