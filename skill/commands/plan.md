---
name: bequite.plan
description: Phase 2 — plan. Loads the software-architect persona; produces specs/<feature>/{spec.md, plan.md, data-model.md, contracts/} for the active feature. Tech-agnostic spec + stack-bound plan + entity model + API/event schemas.
phase: P2
persona: software-architect
prompt_pack: prompts/stack_decision_prompt.md (cross-references)
---

# /bequite.plan [feature?]

When invoked (or `bequite plan <feature-slug>`):

## Step 1 — Read context

- `state/project.yaml` + Memory Bank.
- All accepted ADRs (Phase 1 outputs).
- `docs/PRODUCT_REQUIREMENTS.md` for the active feature.
- Active Doctrines.

## Step 2 — Load software-architect persona

For frontend / database / automation aspects, dispatch to **frontend-designer** / **database-architect** / **automation-architect** sub-personas as needed; coordinate via the orchestrator.

## Step 3 — Produce four artefacts

Under `specs/<feature>/`:

### `spec.md` — technology-agnostic

What's being built, for whom, why. References `projectbrief.md` + `productContext.md`. No mention of specific frameworks. Acceptance criteria expressed in user-observable terms.

### `plan.md` — stack-bound

The implementation plan. References ADRs. Component-by-component breakdown. API surface preview. Data flow. Failure modes. Dependencies on prior phases.

### `data-model.md` — entities

For each entity: fields + types + indexes + RLS/RBAC policies + retention + backup considerations. Cross-references `database-architect` persona outputs.

### `contracts/` — API + events

OpenAPI / GraphQL / Zod / Pydantic / Protocol Buffers / event schemas. Versioned. Schema source of truth (Doctrine Rule 8 binding).

For automation projects: also `specs/<feature>/automation-flows/<flow>.md` per workflow (automation-architect output).

## Step 4 — `/bequite.analyze` (adversarial pre-implementation review)

The Skeptic + reviewer + security-reviewer triad reviews the plan:

- Skeptic: kill-shot per artefact (≥4 total).
- Reviewer: architecture quality + module boundary critique.
- Security-reviewer: threat model + prompt-injection paths + OWASP coverage.

Findings recorded in `specs/<feature>/analyze.md`. Plan exits Phase 2 only after all blockers are resolved.

## Step 5 — Update state

- `state/recovery.md` — "Phase 2 complete; ready for /bequite.phases."
- `.bequite/memory/systemPatterns.md` — new patterns documented.
- `.bequite/memory/techContext.md` — new pinned versions.

## Stop condition

- Four artefacts exist + populated.
- `analyze.md` has zero blockers.
- Skeptic kill-shots answered.
- Receipt emitted.

Suggest next: `/bequite.phases` (Phase 3 decomposition).

## Anti-patterns

- Mentioning specific frameworks in `spec.md` (it's tech-agnostic).
- Plans without acceptance criteria.
- Data models without RLS / RBAC declared.
- Skipping `analyze.md` (master §3.5 binding).
