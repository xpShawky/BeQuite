# ADR-002 — Mandatory workflow gates

**Status:** Accepted
**Date:** 2026-05-11
**Supersedes:** none
**Superseded by:** none
**Related:** ADR-001 (lightweight skill pack first)

---

## Context

v3.0.0-alpha.1 shipped 24 slash commands with phase grouping (P0–P5) but **no enforcement** of the order. Users could run `/bq-implement` without `/bq-plan`. They could run `/bq-release` without `/bq-verify`. The phase grouping was advisory only — convention, not contract.

Three problems followed:

1. **Skipped planning produced low-quality work.** Without a written plan, `/bq-implement` ran on vague intent. Output was reasonable for one task, incoherent across a feature.
2. **Skipped research produced stale recommendations.** Without `/bq-research`, the plan was built on training-corpus memory (2024 facts in 2026 work).
3. **Skipped verification produced "done but not done" claims.** Tasks marked `[x]` complete without `/bq-verify` could ship broken builds.

The brief explicitly requires that BeQuite **prevent skipping important steps** and force the AI to think like a senior product engineer, architect, researcher, designer, security reviewer, and DevOps engineer before implementation. The current advisory-only ordering doesn't enforce any of that.

## Decision

Introduce a **mandatory workflow gate system**:

1. A new file `.bequite/state/WORKFLOW_GATES.md` tracks the state of every workflow gate (`✅ done`, `❌ pending`, `⚪ optional`, `[!] blocked`).
2. Every command declares two new sections in its YAML+markdown spec:
   - **Required previous gates** — gates that must be `✅` before the command runs
   - **Quality gate** — the gates this command marks `✅` on successful completion
3. Commands refuse to run when their required gates aren't met. They print which gate is missing + suggest the prerequisite command.
4. The `/bequite` root command becomes **gate-aware** — it reads `WORKFLOW_GATES.md` and never recommends a command whose required gates aren't met.
5. Six explicit **modes** select which gates apply per workflow (a Fix mode doesn't need a SCOPE_LOCKED gate; a Feature mode is self-contained).
6. Six **phase orchestrators** (`/bq-p0` through `/bq-p5`) walk one phase end-to-end.
7. One **autonomous runner** (`/bq-auto`) walks ALL phases, pausing only at hard human gates (mode selection, clarification, scope approval, plan approval, release approval, destructive ops, DB migrations, server changes, cost ceilings, banned weasel words, repeated failures).

## Consequences

### Positive

- **Cannot skip planning.** `/bq-implement` requires `PLAN_APPROVED ✅`. Forces a written plan.
- **Cannot skip research.** `/bq-plan` strongly recommends `RESEARCH_DONE ✅`. Forces verified evidence.
- **Cannot skip verification.** `/bq-release` requires `VERIFY_PASS ✅`. Forces a passing gate matrix.
- **Mode-aware gates.** Fix mode skips scope/plan (a bug fix doesn't need a SCOPE.md); Feature mode is self-contained (12-type router activates relevant skills); Audit mode produces a report, not code.
- **Autonomous + safe.** `/bq-auto` runs the entire cycle, but never auto-pushes, never auto-deploys, never `terraform destroy`. Hard human gates protect against runaway loops.
- **Better resume after breaks.** `/bq-recover` reads `WORKFLOW_GATES.md` and surfaces "next safe step" precisely.

### Negative

- **More state files to maintain.** `WORKFLOW_GATES.md` adds a new file every command must update. Mitigation: each command's spec lists what to update; `/bq-recover` re-derives state if a file is corrupted.
- **Higher friction for prototypes.** A 30-minute hack still has to pass through `/bq-mode` → `/bq-init`. Mitigation: `Add Feature` mode is short (mini-spec → implement → test → log).
- **More commands to learn (34 vs 24).** Mitigation: `/bequite` recommends the next 3 every time; users rarely need to know all 34.

### Neutral

- The 24 existing commands continue to work; they gain `Preconditions`, `Required previous gates`, `Quality gate`, `Failure behavior` sections.
- 10 new commands are introduced: `/bq-mode`, `/bq-new`, `/bq-existing`, `/bq-feature`, `/bq-auto`, `/bq-p0` through `/bq-p5`.
- 4 commands are rewritten for the v3.0.0-alpha.2 spec: `/bq-research` (11 dimensions), `/bq-plan` (multi-skill activation), `/bq-multi-plan` (unbiased external prompts), `/bq-fix` (15-type router).

## Alternatives considered

### A — Keep advisory-only ordering (status quo from v3.0.0-alpha.1)

Pros: simpler. Cons: doesn't solve the skipping problem; doesn't satisfy the brief.

### B — Hard-coded sequential workflow (no flexibility)

Force every project to follow P0 → P1 → P2 → P3 → P4 → P5 in strict order, no mode selection. Pros: simplest mental model. Cons: doesn't fit Fix workflows, Audit workflows, or mid-cycle re-research. Rejected as too rigid.

### C — Mandatory gates with no orchestrators or auto-mode

Pros: less complexity. Cons: power-users want one-command workflows; manual chaining of 8-10 commands is tedious. Rejected as half-measure.

### D — Soft gates with warning, not refusal

Refuse with override flag. Pros: emergency-escape valve. Cons: every override becomes a habit; gates become noise. Rejected — gates that can be ignored are not gates.

**Chosen: hard gates + mode-specific overrides + hard human gates in /bq-auto.**

## Implementation notes

The gate ledger schema lives in `.bequite/state/WORKFLOW_GATES.md`:

```markdown
# Workflow Gates

## P0 — Setup and Discovery
- [x] BEQUITE_INITIALIZED      done 2026-05-11
- [x] MODE_SELECTED            done 2026-05-11
- [x] DISCOVERY_DONE           done 2026-05-11
- [x] DOCTOR_DONE              done 2026-05-11

## P1 — Product Framing and Research
- [ ] CLARIFY_DONE             pending
- [ ] RESEARCH_DONE            pending
- [ ] SCOPE_LOCKED             pending
- [ ] PLAN_APPROVED            pending
- [ ] MULTI_PLAN_DONE          optional

## P2 — Planning and Build
- [ ] ASSIGN_DONE              pending
- [ ] IMPLEMENT_DONE           pending
- [ ] FEATURE_DONE             n/a (only for Add Feature mode)
- [ ] FIX_DONE                 n/a (only for Fix Problem mode)

## P3 — Quality and Review
- [ ] TEST_DONE                pending
- [ ] AUDIT_DONE               optional
- [ ] REVIEW_DONE              pending
- [ ] RED_TEAM_DONE            optional

## P4 — Release
- [ ] VERIFY_PASS              pending
- [ ] CHANGELOG_READY          pending
- [ ] RELEASE_READY            pending

## P5 — Memory and Handoff
- [ ] MEMORY_SNAPSHOT          pending
- [ ] HANDOFF_DONE             optional

## Blocked
(none)
```

Each command updates the ledger atomically on success.

## Migration from v3.0.0-alpha.1

For users on alpha.1:
- Re-run installer to copy new commands + skills + state file templates
- Run `/bq-init` once to materialize `WORKFLOW_GATES.md` + `CURRENT_MODE.md`
- Existing memory (`PROJECT_STATE.md`, `DECISIONS.md`, etc.) is preserved
- The 24 alpha.1 commands continue to work; gates are advisory until the user opts into mode-aware routing via `/bq-mode`

## References

- `BEQUITE_BOOTSTRAP_BRIEF.md` — original brief requiring "prevent skipping important steps"
- `.bequite/audits/DIRECTION_RESET_AUDIT.md` (Cycle 2) — full keep/pause/delete inventory for v3.0.0-alpha.2
- `docs/specs/COMMAND_CATALOG.md` — full catalog of all 34 commands with their gates
- ADR-001 — the lightweight-skill-pack-first reset
