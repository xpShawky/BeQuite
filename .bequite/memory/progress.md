# Progress: BeQuite

> The evolution log. What works, what's left, what changed and why.

---

## Current state

- **Sub-version:** `v0.2.1` (AI automation skill module — committing this turn; v0.2.0 tagged)
- **Constitution version:** `1.0.1` (amended in v0.1.2; patch bump; additive only — ADR-008-master-merge)
- **Active doctrines:** `library-package`, `cli-tool`, `mena-bilingual` (BeQuite-itself); 8 Doctrines shipped for downstream projects (`default-web-saas`, `cli-tool`, `ml-pipeline`, `desktop-tauri`, `library-package`, `fintech-pci`, `healthcare-hipaa`, `gov-fedramp`)
- **Active mode:** Safe Mode (master §4, adopted v1.0.1)
- **Phases shipped:** v0.1.0, v0.1.1 (v0.1.2 in this commit). Target: v1.0.0 (full release of Layer 1 Harness). Layer 2 Studio: v2.0.0+.
- **Open features:** 1 (the BeQuite v1.0.0 build; 15 sub-versions per approved plan + post-merge updates)
- **Receipt chain integrity:** intact — chain begins in v0.7.0

## What works (verified, with receipts)

Nothing yet. v0.1.0 is the first cut. Receipt-emitting infrastructure ships in v0.7.0; until then, "what works" is verified by the file-presence tests in `tests/integration/` (those land in v0.3.0).

## What's left (in priority order)

The 15-sub-version roadmap from the approved plan:

| Sub-version | Goal | Status |
|---|---|---|
| v0.1.0 | Foundation & Constitution v1.0.0 | ✅ tagged 2026-05-10 |
| v0.1.1 | Doctrines pack (8 default Doctrines) | ✅ tagged 2026-05-10 |
| v0.1.2 | Master-file merge integration (state/, prompts/, evidence/, CLAUDE.md, AGENTS.md, ADR-008, Constitution v1.0.1) | ✅ tagged 2026-05-10 |
| v0.2.0 | Skill orchestrator (SKILL.md + 11 personas + routing.json + bequite.config.toml.tpl + skill-install template) | ✅ tagged 2026-05-10 |
| v0.2.1 | AI automation skill module (ai-automation Doctrine + automation-architect 12th persona + bundled n8n/Make/Zapier/Temporal/Inngest expertise + patterns) | 🟡 committing now |
| v0.3.0 | Hooks (deterministic gates) | pending |
| v0.4.0 | Slash commands wave 1 (Spec-Kit-extends, 9 commands) | pending |
| v0.4.1 | Slash commands wave 2 (BeQuite-adds, 9 commands) | pending |
| v0.4.2 | `bequite audit` (Constitution drift detector) | pending |
| v0.4.3 | `bequite freshness` (knowledge probe) | pending |
| v0.5.0 | CLI thin wrapper | pending |
| v0.6.0 | Verification gates (Playwright + smoke + walks) | pending |
| v0.6.1 | Frontend Quality Module (Impeccable + shadcn + Magic + context7) | pending |
| v0.7.0 | Reproducibility receipts (JSON) | pending |
| v0.7.1 | Signed receipts (ed25519) | pending |
| v0.8.0 | Multi-model routing (cost-aware) | pending |
| v0.8.1 | Live pricing fetch (best-effort) | pending |
| v0.9.0 | Three example projects | pending |
| v0.9.1 | End-to-end test harness | pending |
| v0.10.0 | Auto mode (one-click run-to-completion) | pending |
| v0.10.1 | Auto-mode resilience hardening | pending |
| v0.11.0 | MENA bilingual module | pending |
| v0.12.0 | Universal entry (AGENTS.md + per-host adapters) | pending |
| v0.13.0 | Vibe-to-handoff artifact discipline | pending |
| v0.14.0 | Documentation | pending |
| v0.15.0 | Release engineering | pending |
| **v1.0.0** | **Full release** | pending |

## What's uncertain

- **Freshness probe brittleness.** Vendor pricing pages and registry APIs change. Mitigation: 24h cache + offline fallback + best-effort tag + ongoing v1.x tuning.
- **Skill format constraints.** Anthropic API skills cannot install packages. Mitigation: two skill modes (`claude-code-full` and `api-portable`) documented in `docs/HOSTS.md` (lands v0.14.0).
- **Anthropic beta header lifetime.** `code-execution-2025-08-25`, `skills-2025-10-02`, `files-api-2025-04-14` are beta. Mitigation: receipts log header version; `bequite doctor` surfaces deprecations.

## Evolution log (newest first)

```
2026-05-10  v0.2.1 committing — AI automation skill module per Ahmed's request to "add AI automation features and be expert in n8n and Make." `skill/doctrines/ai-automation.md` (12 binding rules); `skill/agents/automation-architect.md` (12th persona); `skill/skills-bundled/ai-automation/` with README + 6 references (n8n + Make deep, Zapier/Temporal/Inngest brief, patterns cross-platform). SKILL.md + routing.json + bequite.config.toml.tpl updated for the 12th persona and the bundled skill loading rules.
2026-05-10  v0.2.0 tagged — Skill orchestrator. skill/SKILL.md (Anthropic Skills frontmatter, 7-phase router, Fast/Safe/Enterprise mode selector, 19-command surface). 11 personas (master's 10 + Skeptic): product-owner, research-analyst, software-architect, frontend-designer (Impeccable-loaded), backend-engineer, database-architect, qa-engineer, security-reviewer, devops-engineer, token-economist, skeptic. skill/routing.json (provider abstraction, AkitaOnRails 2026 split-only-when-parallel rule, Aider architect-mode review pattern). bequite.config.toml.tpl (per-project config schema). template/.claude/skills/bequite/README.md (skill-install target).
2026-05-10  v0.1.2 tagged — master-file merge: docs/merge/MASTER_MD_MERGE_AUDIT.md (Buckets A/B/C/D/E classification), root CLAUDE.md + AGENTS.md, state/{project.yaml, current_phase.md, recovery.md, task_index.json, decision_index.json, evidence_index.json}, prompts/{master, discovery, research, stack_decision, implementation, review, recovery}, evidence/README.md, ADR-008-master-merge, Constitution v1.0.0 → v1.0.1 patch (additive: Modes, command-safety three-tier, prompt-injection rule, three-level def-of-done, state/ refs). README + CHANGELOG updated. Two-layer architecture decided: Harness (current) + Studio (v2.0.0+). Commit 64c6a74.
2026-05-10  v0.1.1 tagged — 8 default Doctrines: default-web-saas, cli-tool, ml-pipeline, desktop-tauri, library-package, fintech-pci, healthcare-hipaa, gov-fedramp. Each ~150 lines with rules, stack guidance, verification gates, forking guidance. mena-bilingual deferred to v0.11.0. Commit 50ebfe6.
2026-05-10  v0.1.0 tagged — repo skeleton, Iron Laws Constitution v1.0.0, 6 Memory Bank templates, ADR template, Doctrine schema authored. Plan snapshotted. Ahmed authorised autonomous execution through v1.0.0. Commit 22330e7.
2026-05-10  ExitPlanMode accepted. Build plan at .bequite/memory/prompts/v1/2026-05-10_initial-plan.md.
2026-05-10  4 forks resolved by Ahmed: engineer-first (with vibe-handoff seeded) / skill-first / layered Constitution / full-power v1.
2026-05-10  Brief verification complete. 10 surgical updates baked into Constitution + templates (Aider direction, Stronghold deprecation, EV cert obsolescence, Spec-Kit command count, Roo Code shutdown, shadcn MCP move, Clerk MAU, Vercel timeout, Supavisor, PhantomRaven naming).
2026-05-10  Initial brief (BEQUITE_BOOTSTRAP_BRIEF.md) read in full. Three parallel research agents dispatched: spec-driven tools, AI coding tool landscape, security/quality fact-check.
```

## Decisions made (newest first)

```
2026-05-10  ADR-008 accepted: two-layer architecture (Harness v0.1.0 → v1.0.0, Studio v2.0.0+); Constitution v1.0.0 → v1.0.1 patch amendment (additive only: Modes, command-safety three-tier, prompt-injection rule, three-level def-of-done, state/ refs).
2026-05-10  Personas merge (DEC-007): master's 10 named roles (product-owner, research-analyst, software-architect, frontend-designer, backend-engineer, database-architect, qa-engineer, security-reviewer, devops-engineer, token-economist) + Skeptic + FrontendDesign-Impeccable = 12 personas. To author in v0.2.0.
2026-05-10  Slash commands merge (DEC-008): master's 12 names (/discover, /research, /decide-stack, /plan, /implement, /review, /validate, /recover, /design-audit, /impeccable-craft, /evidence, /release) + BeQuite's 7 unique extras (/audit, /freshness, /auto, /memory, /snapshot, /cost, /skill-install) = 19 commands. To author in v0.4.0–v0.4.3.
2026-05-10  Master file scope deferred (DEC-005): TypeScript monorepo + Postgres + Next.js dashboard + NestJS API + Worker → Studio Layer 2 (v2.0.0+). Layer 1 Harness (current) preserved.
2026-05-10  (informal, pending ADR-001 in v0.5.0) BeQuite stack: Python 3.11+ CLI via hatchling/click/anthropic/rich/httpx/pydantic/cryptography. Reasoning: matches Spec-Kit's proven pattern (uvx/pipx); Python's ML/data ecosystem; offline-friendly tomllib in stdlib.
2026-05-10  Iron Laws are 7 articles (Spec, Verify, Memory, Security, Scale, Honest, Hallucination). Stack discipline (was Article IV in brief), UI distinctiveness (was VII), and Research-first (was VIII) are NOT Iron Laws — they're Doctrines or implicit in the seven phases. Reasoning: a CLI tool / library / ML pipeline doesn't need Article-VII UI rules; layered Constitution is more honest.
2026-05-10  (DEC-002) Skill-first distribution: SKILL.md is source of truth, CLI is thin Python wrapper, host adapters generated.
2026-05-10  (DEC-001) Engineer-first v1, with vibe-handoff seeded into artifact discipline.
2026-05-10  (DEC-003) Layered Constitution: 7 Iron Laws + forkable Doctrines. Impeccable bundled as default-loaded Doctrine for frontend projects.
2026-05-10  (DEC-004) Full v1 power from day 1; autonomous execution authorised by Ahmed; 15 sub-versions to v1.0.0.
```

## Failures and learnings

```
(none yet)
```
