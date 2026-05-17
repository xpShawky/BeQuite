# How BeQuite works

> The architecture in one document. For the operating contract see `.bequite/memory/constitution.md`.

## The big idea

BeQuite is **not a code generator**. It's the **discipline layer** around the model that writes code: research → stack ADR → plan → phases → tasks → implement → verify → handoff. Seven non-skippable phases, with a deterministic gate at each transition.

## Two layers

| Layer | What | Status | Distribution |
|---|---|---|---|
| **Layer 1 — Harness** | SKILL.md + Python CLI + repo template | Current (v0.1.0 → v1.0.0) | `uvx bequite` / `pipx` / git clone |
| **Layer 2 — Studio** | Next.js dashboard + NestJS API + Worker + Postgres | Planned (v2.0.0+) | Self-hosted or hosted |

You're using Layer 1.

## The seven phases

Each phase has: an artifact (file at a known path), a Skeptic kill-shot, a verification gate, a receipt, and a per-phase commit.

| Phase | Persona | Artifact | Gate |
|---|---|---|---|
| P0 — Research | research-analyst | `docs/RESEARCH_SUMMARY.md` | freshness probe green |
| P1 — Stack | software-architect | ADR at `.bequite/memory/decisions/ADR-NNN-stack.md` | bequite freshness all green |
| P2 — Plan | software-architect | `specs/<feature>/plan.md` | spec validates |
| P3 — Phases | product-owner | `specs/<feature>/phases.md` | phase count > 0 + each has exit gate |
| P4 — Tasks | product-owner | `specs/<feature>/tasks.md` | tasks atomic (≤5 min); IDs assigned |
| P5 — Implement | backend/frontend/database engineer + reviewer | code diff per task | tests pass + format + typecheck |
| P6 — Verify | qa-engineer + security-reviewer | `evidence/P6/...` | Playwright walks + axe + smoke + audit + freshness all green |
| P7 — Handoff | tech-writer + devops | `HANDOFF.md` | hand-runnable by second engineer |

## Iron Laws (universal)

- I — Specification supremacy
- II — Verification before completion
- III — Memory discipline
- IV — Security & destruction
- V — Scale honesty
- VI — Honest reporting
- VII — Hallucination defense
- VIII — Scraping & automation discipline (added v0.5.1)
- IX — Cybersecurity & authorized-testing (added v0.5.2)

Iron Laws are immutable-ish (amendable only via ADR + version bump). See `.bequite/memory/constitution.md` for full text.

## Doctrines (forkable rule packs)

| Doctrine | When loaded |
|---|---|
| `default-web-saas` | Web SaaS with frontend |
| `cli-tool` | CLI tool / library |
| `ml-pipeline` | ML training pipelines |
| `desktop-tauri` | Tauri-based desktop apps |
| `library-package` | Library package |
| `fintech-pci` | PCI-DSS regulated |
| `healthcare-hipaa` | HIPAA-regulated |
| `gov-fedramp` | FedRAMP-controlled |
| `ai-automation` | n8n / Make / Zapier / Temporal projects |
| `vibe-defense` | Default for `audience: vibe-handoff` |
| `mena-pdpl` | MENA-region data protection |
| `eu-gdpr` | EU/EEA users |
| `mena-bilingual` | Arabic + RTL projects (v0.11.0+) |

Stack two or more (e.g. `default-web-saas + mena-bilingual + mena-pdpl`).

## Modes

- **Fast** — small tools, demos. Skips deep research + load testing.
- **Safe** (default) — real apps. Full discipline.
- **Enterprise** — sensitive data. Adds threat model + audit logs + access matrix + observability + IR runbook.

## Hooks (deterministic gates)

| Hook | Effect |
|---|---|
| `pretooluse-secret-scan.sh` | Block secrets in Edit/Write |
| `pretooluse-block-destructive.sh` | Block rm -rf, terraform destroy, DROP DATABASE, git push -f |
| `pretooluse-verify-package.sh` | PhantomRaven defense — verify packages exist in registry |
| `pretooluse-scraping-respect.sh` | robots.txt + ToS + rate-limit ≥3s |
| `pretooluse-pentest-authorization.sh` | RoE check before offensive tooling |
| `pretooluse-no-malware.sh` | Block stealer/RAT/ransomware/cryptojacker |
| `pretooluse-cve-poc-context.sh` | PoC requires ADR with 3 confirmations |
| `posttooluse-format.sh` | biome / prettier / black / ruff / clippy |
| `posttooluse-lint.sh` | warn-only |
| `posttooluse-audit.sh` | run lightweight bequite audit on Edit/Write |
| `stop-verify-before-done.sh` | banned-word check + incomplete-task check |
| `stop-cost-budget.sh` | enforce session cost ceiling |
| `sessionstart-load-memory.sh` | preload Memory Bank + ADRs + state/recovery.md |
| `sessionstart-cost-budget.sh` | load cost ceiling from config |

## Receipts (v0.7.0+)

Every model invocation emits a chain-hashed JSON receipt at `.bequite/receipts/<sha>-<phase>.json`. Schema includes prompt-hash + memory-snapshot-hash + diff-hash + cost + parent-receipt chain pointer. ed25519-signed since v0.7.1.

## Multi-model planning (v0.10.5+)

Two or more models think through a project independently, then BeQuite compares + merges. MVP: manual-paste mode (ToS-clean; works with consumer subscriptions). Direct-API mode v0.11.x+. See `docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md`.

## CLI auth (v0.10.6 stubs; v0.11.x+ working)

Device-code login as MVP (works headless / SSH / CI). OS-keychain token storage. CI mode separate (`BEQUITE_API_KEY`). See `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md`.

## Auto-mode (v0.10.0+)

State machine walking P0 → P7 with safety rails (cost ceiling, wall-clock ceiling, 3-failure threshold, banned-word check, hook-block respect, one-way-door pauses). Heartbeat updates `activeContext.md` every 5 minutes. See `docs/AUTONOMOUS-MODE.md`.

## Cross-references

- Constitution: `.bequite/memory/constitution.md`
- Quickstart: `docs/QUICKSTART.md`
- Hosts: `docs/HOSTS.md`
- Auto-mode: `docs/AUTONOMOUS-MODE.md`
- Security: `docs/SECURITY.md`
- Doctrine authoring: `docs/DOCTRINE-AUTHORING.md`
- Maintainer: `docs/MAINTAINER.md`
