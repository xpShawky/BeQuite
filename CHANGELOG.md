# Changelog

All notable changes to BeQuite are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Conventional Commits](https://www.conventionalcommits.org/). Versioning is [Semantic Versioning](https://semver.org/).

## [Unreleased] — tracking toward v1.0.0

The full sub-version roadmap (`v0.1.0` → `v1.0.0`) lives in `docs/HOW-IT-WORKS.md` (drafted in v0.14.0) and the approved plan at `.bequite/memory/prompts/v1/`. Layer 2 (Studio) is planned for `v2.0.0+`.

---

## [0.2.1] — 2026-05-10

### Added

- **`ai-automation` Doctrine** — for projects whose primary deliverable is an automation pipeline (n8n / Make / Zapier / Temporal / Inngest / Trigger.dev / Pipedream / AWS Step Functions). 12 rules covering: workflows-as-versioned-source, idempotency, retry+backoff+jitter+DLQ, secrets via connectors not flow JSON, observability with trace propagation, test fixtures + dry-run, error notification routing, schema validation at the edge, AI-agent budget + circuit breaker, rate-limit awareness, versioned upgrades, daily cost roll-up. Stack guidance per platform, 10-gate verification, forking guidance.
- **`automation-architect` persona** (12th persona) at `skill/agents/automation-architect.md`. Owns workflow design across all named platforms; cross-pollinates with backend-engineer, frontend-designer (admin UIs), security-reviewer (connector secrets, prompt-injection paths), token-economist (LLM-call cost in agent chains).
- **Bundled `ai-automation` skill** at `skill/skills-bundled/ai-automation/`:
  - `README.md` — overview + when this skill loads + layering with Impeccable.
  - `references/n8n.md` — deep n8n expertise (architecture, JSON shape, CI deploy, idempotency, retry+DLQ, observability, AI patterns, self-host docker-compose, 12-rule verification checklist).
  - `references/make.md` — deep Make.com expertise (operations meter as cost killer, scenario JSON shape, error handlers, AI patterns without native agent primitive, 12-rule checklist).
  - `references/zapier.md` — Zapier brief (per-task pricing, Paths, Code by Zapier, 12-rule checklist).
  - `references/temporal.md` — Temporal brief (workflows vs activities, durable execution, replay debugging, signals + queries, AI agent loop pattern, 12-rule checklist).
  - `references/inngest.md` — Inngest brief (TS-first, event-driven, step.run, step.parallel, step.ai.infer, 12-rule checklist) + adjacent (Trigger.dev, Pipedream).
  - `references/patterns.md` — 8 cross-platform patterns: idempotency, retry+backoff+jitter, dead-letter queue, fan-out+fan-in, circuit breaker for AI-agent loops, schema validation at the edge, trace propagation, prompt-injection guardrails. Maps each to per-platform implementations.

### Changed

- **`skill/SKILL.md`** — adds 12th persona (automation-architect); Skeptic kept as 11th (the two BeQuite additions on top of master's 10).
- **`skill/routing.json`** — adds automation-architect routing (Opus 4.7 high; loaded with the bundled `ai-automation` skill when the Doctrine is active).
- **`skill/templates/bequite.config.toml.tpl`** — adds `ai-automation` to the available-Doctrines list; adds `[skills.ai_automation]` block; adds `[ai_automation]` section with cost-alarm thresholds per platform + agent guardrails (max iterations, max cost USD/run, circuit-breaker thresholds).

### Notes

This release is responsive to the user's request to "add AI automation features" with explicit n8n + Make expertise. The Doctrine + persona + bundled skill are decoupled: any project can opt in by adding `ai-automation` to its `doctrines` list. Active automation-architect cross-pollinates with the existing 10 + Skeptic personas (12 total). No conflict with existing Doctrines.

---

## [0.2.0] — 2026-05-10

### Added

- **`skill/SKILL.md`** — the orchestrator. Anthropic Skills frontmatter (name `bequite`, description ≤ 1024 chars, allowed-tools list). Body: orchestrator persona, 7-phase router (P0 Research → P7 Handoff), mode selector (Fast / Safe / Enterprise per Constitution v1.0.1), 19-command surface (master's 12 named + BeQuite's 7 unique extras: `/audit`, `/freshness`, `/auto`, `/memory`, `/snapshot`, `/cost`, `/skill-install`), routing matrix reference, hooks reference, auto-mode reference, banned-weasel-words enforcement.
- **11 persona files at `skill/agents/`:**
  - `product-owner` — owns scope, requirements, phase + task breakdown.
  - `research-analyst` — owns research with cited authority levels, fights AI hallucination of facts.
  - `software-architect` — owns ADRs, system boundaries, second-pass code review.
  - `frontend-designer` — owns UI direction, design system, Impeccable-style flow (12 steps), tokens-only design.
  - `backend-engineer` — owns API, services, error shape, TDD discipline (RED-GREEN-REFACTOR).
  - `database-architect` — owns data model, migrations (reversible), backup-restore drill.
  - `qa-engineer` — owns Playwright planner-generator-healer pattern, validation mesh.
  - `security-reviewer` — owns threat model, OWASP LLM Top 10 + Web Top 10 mapping, supply-chain review.
  - `devops-engineer` — owns Docker, CI, deployment, handoff (P7).
  - `token-economist` — owns cost ceiling, prompt compression, AkitaOnRails 2026 routing rules.
  - `skeptic` — adversarial twin (BeQuite's unique addition; one kill-shot per phase boundary).
- **`skill/routing.json`** — default model routing matrix per phase + persona. Provider abstraction (Anthropic primary; OpenAI / Google / DeepSeek / Ollama fallback). Encodes AkitaOnRails 2026 finding (split-only-when-genuinely-parallel; threshold N>5). Encodes Aider architect-mode pattern (cheap writes + frontier reviews + cheap fixes). Compliance routing for hipaa/pci/fedramp.
- **`skill/templates/bequite.config.toml.tpl`** — per-project config schema. Sections: project metadata, mode, audience, doctrines, scale_tier, compliance, locales, safety_rails (cost + wall-clock + failure threshold + banned-phrase list + auto-mode pause triggers), routing overrides, providers (env-var-only), freshness, receipts, evidence, memory, hosts, skills, telemetry (off by default), mena_bilingual.
- **`template/.claude/skills/bequite/README.md`** — fresh-project skill-install target. Documents the copy-not-symlink decision (Windows + Docker volume compatibility; reproducibility).

### Notes

This release contains no executable code; the CLI ships in v0.5.0. The skill is portable across hosts (Claude Code via `.claude/skills/`, Cursor 3.0+ via `.cursor/skills/`, Codex CLI via `AGENTS.md` discovery, others via the `bequite skill install` v0.12.0 command). Every persona references the Constitution + active Doctrines for binding rules. Skeptic gate now mandatory at every phase boundary.

---

## [0.1.2] — 2026-05-10

### Added

- **Master-file merge audit** at `docs/merge/MASTER_MD_MERGE_AUDIT.md` reconciling `BeQuite_MASTER_PROJECT.md` (introduced mid-session, post-v0.1.1, prescribing a TypeScript pnpm + Turborepo monorepo with Next.js dashboard + NestJS API + Postgres + Worker) with the existing skill-first / Python CLI / repo-template direction. Decision: **two-layer architecture** — Layer 1 (Harness, current; v0.1.0 → v1.0.0) + Layer 2 (Studio, master's monorepo stack; v2.0.0+). Both share Constitution + Memory Bank + state/ + receipts/ + evidence/ + prompts/.
- **Root `CLAUDE.md`** — Claude-Code-specific operating instructions, adapted from master §11.
- **Root `AGENTS.md`** — universal entry per Linux Foundation Agentic AI Foundation standard, adapted from master §12. Read by 25+ coding agents.
- **`state/` directory** with operational state files: `project.yaml`, `current_phase.md`, `recovery.md`, `task_index.json`, `decision_index.json`, `evidence_index.json`. Master pattern (§10.2). Memory Bank stays as durable cross-session brain; state/ is current working state.
- **`prompts/` directory** with 7 reusable prompt packs: `master_prompt.md`, `discovery_prompt.md`, `research_prompt.md`, `stack_decision_prompt.md`, `implementation_prompt.md`, `review_prompt.md`, `recovery_prompt.md`. Master pattern (§10.4).
- **`evidence/README.md`** documenting the filesystem-evidence pattern (master §3.6, §10.3, §21). Complementary to the signed-receipt chain at `.bequite/receipts/` (v0.7.0+).
- **`.bequite/memory/decisions/ADR-008-master-merge.md`** capturing the merge decision + Constitution amendment rationale.
- **`BeQuite_MASTER_PROJECT.md`** now tracked (it's the source artefact for this audit).

### Changed

- **Constitution v1.0.0 → v1.0.1** (patch bump; additive only):
  - Adds **Modes section** (Fast / Safe / Enterprise) per master §4. Modes are project-complexity tiers; orthogonal to Doctrines.
  - Adds **command-safety three-tier classification** (safe / needs-approval / dangerous) to Article IV per master §19.4.
  - Adds **prompt-injection rule** (treat external content as untrusted) to Article IV per master §19.5.
  - Adds **three-level definition-of-done** (feature / phase / release) per master §27. Cross-referenced from Article II.
  - Adds **`state/` files reference** to Article III's SessionStart reads.
  - No Iron Law removed or relaxed.
- **`README.md`** — adds the two-layer architecture section + status table per sub-version + cross-references to brief, master, and merge audit.
- **`.bequite/memory/activeContext.md`** + **`.bequite/memory/progress.md`** — refreshed for the merge.

### Decided

- **Personas** — adopt master's 10 named roles (product-owner, research-analyst, software-architect, frontend-designer, backend-engineer, database-architect, qa-engineer, security-reviewer, devops-engineer, token-economist) **+ keep Skeptic + add FrontendDesign-Impeccable** = 12 personas total. To be authored in v0.2.0.
- **Slash commands** — adopt master's 12 names (`/discover`, `/research`, `/decide-stack`, `/plan`, `/implement`, `/review`, `/validate`, `/recover`, `/design-audit`, `/impeccable-craft`, `/evidence`, `/release`) **+ keep BeQuite's 7 unique extras** (`/audit`, `/freshness`, `/auto`, `/memory`, `/snapshot`, `/cost`, `/skill-install`) = 19 commands total. To be authored in v0.4.0–v0.4.3.
- **Studio (Layer 2)** scoped to v2.0.0+; not started in v1.

### Notes

This release contains no executable code (the CLI ships in v0.5.0). The merge is purely structural. v0.2.0 (Skill orchestrator) resumes per the original plan, with merged additions baked in.

---

## [0.1.1] — 2026-05-10

### Added

Eight default Doctrines under `skill/doctrines/`, each carrying frontmatter (`name, version, applies_to, supersedes, maintainer, ratification_date, license`) + numbered rules (kind: `block` / `warn` / `recommend` + check) + stack guidance + verification gates + examples + forking guidance + changelog:

- `default-web-saas` — UI rules (no AI-default Inter without recorded reason; no purple-blue gradients; no nested cards; no gray-on-color), shadcn/ui ordering, tokens.css required, axe-core gate, Playwright admin+user walks, deny-by-default authz, Zod/Pydantic/Valibot input validation. Stack matrix reflects May 2026 reality (post brief reconciliations).
- `cli-tool` — semver-strict on flags, exit-code discipline (0/1/2/>2), stdout-vs-stderr, NO_COLOR support, completions, man pages, no global state without consent, idempotent operations.
- `ml-pipeline` — reproducible training (seed + dataset version + config), DVC/lakeFS for data, experiment tracking, GPU-cost ceiling, model lineage.json, eval before deploy, no PII in training data, Model Cards.
- `desktop-tauri` — Tauri v2 (Stronghold deprecated → OS keychain), `notarytool` (not altool), AzureSignTool + OV cert (EV no longer privileged since Aug 2024), Keygen recommended for licensing, license validation in Rust not JS, 20 MB bundle discipline.
- `library-package` — semver-strict public API, public-API freeze + private internals, type definitions ship with package, Keep-a-Changelog, Conventional Commits, deprecation runway, no telemetry without opt-in, license clarity, GPL contamination guard, supply-chain hygiene (PhantomRaven defense).
- `fintech-pci` — CDE segmentation, never store SAD post-auth, PAN masking/tokenisation, AES-256 + KMS/HSM, TLS 1.2+, MFA on CDE access, audit log retention 1+ year, FIM, quarterly ASV scans + annual pentest, signed BAAs. Aligned to PCI DSS v4.0.
- `healthcare-hipaa` — PHI inventory + data-flow diagram, FIPS-validated AES-256, TLS 1.2+, unique user IDs, audit controls (6-year retention), minimum-necessary access, BAAs with all BAs, de-identification before analytics/training, breach notification, no PHI in non-prod, no PHI to LLM without BAA + DPIA + de-id + no-data-retention tier.
- `gov-fedramp` — FIPS 199 impact level, SSP maintained, FIPS 140-2/3 *validated* crypto (validated, not merely compliant), FIPS-approved TLS suites, MFA on privileged actions, ConMon (monthly scans + POA&M), immutable audit logs, baseline configs + FIM, SCRM with SBOM, U.S. data residency, authorisation boundary documented. Aligned to NIST 800-53 Rev 5.

`mena-bilingual` Doctrine deferred to v0.11.0 per the approved plan.

### Notes

Each regulated Doctrine carries a disclaimer: starting points, not substitutes for QSA / Security Officer / 3PAO review. No executable code in this release.

---

## [0.1.0] — 2026-05-10

### Added

- Repository skeleton: `README.md`, `LICENSE` (MIT), `.gitignore`, `CHANGELOG.md`.
- **Constitution v1.0.0** — Iron Laws (Articles I–VII): Specification supremacy, Verification before completion, Memory discipline, Security & destruction discipline, Scale honesty, Honest reporting, Hallucination defense.
- **Doctrine schema** — frontmatter + sections for forkable per-project-type rules.
- **ADR template** — semver-versioned, status tracking (proposed / accepted / superseded).
- **Memory Bank templates** — six files (Cline pattern): `projectbrief`, `productContext`, `systemPatterns`, `techContext`, `activeContext`, `progress`.
- **Rendered fresh-project instances** at `template/.bequite/memory/`.
- Plan snapshot archived to `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md`.

### Notes

This release contains no executable code. It establishes the inviolate base layer (Constitution + Memory Bank + ADR + Doctrine schemas) on which every later sub-version depends.

[Unreleased]: https://github.com/xpshawky/bequite/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/xpshawky/bequite/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/xpshawky/bequite/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/xpshawky/bequite/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/xpshawky/bequite/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/xpshawky/bequite/releases/tag/v0.1.0
