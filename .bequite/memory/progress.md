# Progress: BeQuite

> The evolution log. What works, what's left, what changed and why.

---

## Current state

- **Sub-version:** `v0.1.0` (in progress)
- **Constitution version:** `1.0.0`
- **Active doctrines:** `library-package`, `cli-tool`, `mena-bilingual` (BeQuite-itself); `default-web-saas` is shipped for downstream projects
- **Phases shipped:** none yet (v1.0.0 is the target full-release)
- **Open features:** 1 (the BeQuite v1.0.0 build itself; broken into 15 sub-versions per the approved plan at `prompts/v1/`)
- **Receipt chain integrity:** intact — chain begins in v0.7.0

## What works (verified, with receipts)

Nothing yet. v0.1.0 is the first cut. Receipt-emitting infrastructure ships in v0.7.0; until then, "what works" is verified by the file-presence tests in `tests/integration/` (those land in v0.3.0).

## What's left (in priority order)

The 15-sub-version roadmap from the approved plan:

| Sub-version | Goal | Status |
|---|---|---|
| v0.1.0 | Foundation & Constitution v1.0.0 | **in progress** |
| v0.1.1 | Doctrines pack (8 default Doctrines) | next |
| v0.2.0 | Skill orchestrator (SKILL.md + 9 personas + routing) | pending |
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
2026-05-10  v0.1.0 in progress — repo skeleton, Iron Laws Constitution v1.0.0, 6 Memory Bank templates, ADR template, Doctrine schema authored. Plan snapshotted. Ahmed authorised autonomous execution through v1.0.0.
2026-05-10  ExitPlanMode accepted. Build plan at .bequite/memory/prompts/v1/2026-05-10_initial-plan.md.
2026-05-10  4 forks resolved by Ahmed: engineer-first (with vibe-handoff seeded) / skill-first / layered Constitution / full-power v1.
2026-05-10  Brief verification complete. 10 surgical updates baked into Constitution + templates (Aider direction, Stronghold deprecation, EV cert obsolescence, Spec-Kit command count, Roo Code shutdown, shadcn MCP move, Clerk MAU, Vercel timeout, Supavisor, PhantomRaven naming).
2026-05-10  Initial brief (BEQUITE_BOOTSTRAP_BRIEF.md) read in full. Three parallel research agents dispatched: spec-driven tools, AI coding tool landscape, security/quality fact-check.
```

## Decisions made (newest first)

```
2026-05-10  (informal, pending ADR-001 in v0.5.0) BeQuite stack: Python 3.11+ CLI via hatchling/click/anthropic/rich/httpx/pydantic/cryptography. Reasoning: matches Spec-Kit's proven pattern (uvx/pipx); Python's ML/data ecosystem; offline-friendly tomllib in stdlib.
2026-05-10  Iron Laws are 7 articles (Spec, Verify, Memory, Security, Scale, Honest, Hallucination). Stack discipline (was Article IV in brief), UI distinctiveness (was VII), and Research-first (was VIII) are NOT Iron Laws — they're Doctrines or implicit in the seven phases. Reasoning: a CLI tool / library / ML pipeline doesn't need Article-VII UI rules; layered Constitution is more honest.
2026-05-10  Skill-first distribution: SKILL.md is source of truth, CLI is thin Python wrapper, host adapters generated. Reasoning: nobody currently does this; one brain, two faces; aligned with Anthropic Skills direction.
2026-05-10  Engineer-first v1, with vibe-handoff seeded into artifact discipline: every spec.md / plan.md / tasks.md / AGENTS.md is designed to be picked up by Claude Code / Cursor / Codex without rewriting, so a v2 vibe-coder UI can drive the same brain.
2026-05-10  Impeccable bundled as the default-loaded Doctrine for frontend projects (pinned snapshot, attributed Paul Bakaus, MIT). Article-VII UI ban softened to "no design choice without a recorded reason." Reasoning: Linear/Vercel/Stripe use Inter; outright ban overcorrects.
```

## Failures and learnings

```
(none yet)
```
