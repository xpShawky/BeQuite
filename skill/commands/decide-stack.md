---
name: bequite.decide-stack
description: Phase 1 — stack ADR(s). Loads the software-architect persona; runs `bequite freshness` against every candidate; produces ADRs at .bequite/memory/decisions/ per prompts/stack_decision_prompt.md. Educational ADRs the human learns from.
phase: P1
persona: software-architect
prompt_pack: prompts/stack_decision_prompt.md
---

# /bequite.decide-stack

When invoked (or `bequite decide-stack`):

## Step 1 — Read context

- All Phase 0 outputs (`docs/RESEARCH_SUMMARY.md` + four sub-files).
- `state/project.yaml::audience, mode, active_doctrines, scale_tier, compliance`.
- All loaded Doctrines (each has "Stack guidance" section pre-narrowing the candidate menu).
- `skill/references/stack-matrix.md` (drafted v0.4.1+; reflects May 2026 reality with brief reconciliations).
- `skill/references/package-allowlist.md` (drafted v0.4.3).

## Step 2 — Load software-architect persona

Switch to `skill/agents/software-architect.md`.

## Step 3 — Apply binding brief reconciliations (always)

Treat the following as binding facts (the original brief and master file contain pre-2024 advice):

- Tauri **Stronghold deprecated** → use OS keychain.
- Windows: **OV cert + AzureSignTool** (NOT EV); AKV cert validity 1 year since Feb 2026.
- macOS: **`xcrun notarytool`** (NOT altool).
- Aider architect mode: frontier reasoner plans + cheap editor emits diffs (NOT reverse).
- **Roo Code shutting down 2026-05-15** → replace with Kilo Code.
- shadcn registry MCP: built into shadcn CLI v3+.
- Clerk free tier: **50k MAU** (was 10k).
- Vercel Pro timeout: configurable to **800s** (not hard 300s).
- PgBouncer → **Supavisor** on Supabase.
- npm hallucination attack name: **PhantomRaven** (Koi Security, 126 packages).
- Veracode 2025 "14 vulns/MVP" → drop; keep verified 45% OWASP figure.
- Impeccable: ~26.6k stars, 23 commands.

## Step 4 — For each consequential decision, write an ADR

Use `skill/templates/adr.md.tpl`. Master §3.2 binding — every ADR includes:

Options / Pros / Cons / Scale limit / Security implications / Cost implications / Maintenance burden / Recommendation / Why this fits / What would make it change.

Typical ADRs in a fresh project:

- `ADR-001-stack` — overall stack matrix
- `ADR-002-database` — DB choice + schema discipline
- `ADR-003-auth` — authn + authz model
- `ADR-004-hosting` — runtime + region + scale path
- `ADR-005-secrets` — secret management (Doppler / Vault / KMS)
- `ADR-006-ci-cd`
- `ADR-007-error-shape`
- `ADR-008-provider-adapter` — LLM provider boundary (master §16.5)
- `ADR-009-backup-restore`

Enterprise Mode + regulated Doctrines add: ADR-010 threat model, ADR-011 data classification, ADR-012 audit log retention, ADR-013 compliance mapping, ADR-014 IR runbook.

## Step 5 — Pre-sign mandatory checks

Each ADR `proposed → accepted` only after:

1. **`bequite freshness`** runs against every candidate package in the ADR; stale candidate **blocks** the ADR.
2. **Skeptic kill-shot** answered in Rationale / Consequences.
3. **Scale-tier coherence** (Article V — chosen stack supports declared tier).
4. **Doctrine alignment** — each loaded Doctrine's Stack guidance consulted; deviations require a `Why we deviated` note.
5. **`bequite audit` clean** — no Iron Law / Doctrine violation introduced.

## Step 6 — Update state

- `state/decision_index.json` — append accepted ADR(s).
- `.bequite/memory/techContext.md` — pinned versions + dev setup updated.
- `state/recovery.md` — "Phase 1 complete; ready for /bequite.plan."

## Stop condition

- Every required ADR `status: accepted`.
- Freshness probe green for every candidate.
- Skeptic kill-shots answered.
- `state/decision_index.json` and `techContext.md` updated.
- Receipt(s) emitted (v0.7.0+).

Suggest next: `/bequite.plan` (Phase 2).

## Anti-patterns

- Picking a stack from memory (Article VII binding — verify via freshness probe).
- Picking a stack without an ADR (Iron Law I + master §3.2).
- Re-litigating without a superseding ADR.
- Skipping the brief reconciliations.
- Weasel words in the ADR ("we should probably use Postgres" — no; pick or document the kill-shot that prevents picking).
