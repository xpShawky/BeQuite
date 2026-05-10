---
name: bequite.discover
description: Phase 0 — product discovery interview. Loads the product-owner persona; conducts a grouped-decision-block interview per prompts/discovery_prompt.md; produces docs/PRODUCT_REQUIREMENTS.md + state/project.yaml + risk register + recommended-improvements list.
phase: P0
persona: product-owner
prompt_pack: prompts/discovery_prompt.md
---

# /bequite.discover

When the user invokes this command (or runs `bequite discover` from the CLI):

## Step 1 — Read context

Per Article III, read on entry:

- `AGENTS.md` + `CLAUDE.md`
- `.bequite/memory/constitution.md`
- All six Memory Bank files
- `state/project.yaml` (if exists)

If the project is fresh (no `state/project.yaml`), this is the first invocation; proceed.
If the project exists, surface the current state + ask the user whether to **amend** the existing requirements or **start over** (the latter requires an ADR documenting why).

## Step 2 — Load product-owner persona

Switch context to `skill/agents/product-owner.md`. The persona conducts the eight-question-group interview per `prompts/discovery_prompt.md`:

1. Product identity
2. Output target
3. Scale
4. Security
5. UX direction
6. Automation depth
7. Licensing / pricing
8. Deployment

For each group: ask, propose recommended default, list alternatives, document risk if skipped. Master §3.4 binding (no five-question wall-of-text).

## Step 3 — Surface improvements (master §3.5)

After interview: propose improvements the user did not mention. Classify:

- Must add now
- Should add soon
- Can wait
- Avoid for now

User accepts / rejects / modifies. Defaults applied if user says "continue" — defaults documented.

## Step 4 — Produce outputs

Write:

- `docs/PRODUCT_REQUIREMENTS.md`
- `state/project.yaml::audience, mode, active_doctrines, scale_tier, compliance, locales` populated
- `docs/risks.md` (or `state/project.yaml::risks` array)
- `docs/improvements.md` (the recommended-improvements log + acceptances)

## Step 5 — Skeptic gate

Skeptic produces ≥1 kill-shot question on the just-completed discovery. Owner answers. Receipt records both (v0.7.0+).

## Stop condition

This command exits when:

- All eight question groups have answers (or default-applied with user acknowledgment).
- `state/project.yaml::mode + audience + active_doctrines + scale_tier + compliance + locales` populated.
- `docs/PRODUCT_REQUIREMENTS.md` covers all eight groups.
- Skeptic kill-shot answered in `docs/PRODUCT_REQUIREMENTS.md::skeptic-acknowledgments`.
- `state/recovery.md` updated to "Phase 0 discovery complete; ready for /bequite.research."

Then suggest: `/bequite.research` (Phase 0 continued) before `/bequite.decide-stack` (Phase 1).

## Anti-patterns

- Skipping the eight groups for a "quick start" — refuse; offer Fast Mode if the project is genuinely small.
- Asking groups out of order — refuse; sequence matters (security depends on scale; UX depends on platform).
- Going to Phase 1 before Skeptic kill-shot is answered — refuse.

## Related commands

- `/bequite.research` — Phase 0 continued (research scan)
- `/bequite.decide-stack` — Phase 1 (stack ADR)
- `/bequite.recover` — resume mid-discovery in a new session
