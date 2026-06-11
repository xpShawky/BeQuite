---
name: bequite-frontier-reasoning-coach
description: Frontier operating discipline coach — forces any model (cheaper, smaller, different) to follow frontier-class workflow via the Operating Playbook checklists. Loads on deep-mode work, delegate task-pack writing/review, red-team, verify, and skill audits. Not chain-of-thought — external checklists only.
allowed-tools: Read, Glob, Grep
---

# bequite-frontier-reasoning-coach — discipline, portable

## Purpose

Frontier-model output quality comes less from raw capability than from OPERATING DISCIPLINE: recover-before-act, audit-before-add, evidence-over-claims, calibrated confidence, single-source-of-truth, full-scope completion. This skill makes any model follow that discipline by enforcing the checklists in `docs/architecture/FRONTIER_MODEL_OPERATING_PLAYBOOK.md`. It contains **no private chain-of-thought** — only external, reusable execution patterns.

## When this skill activates

- `/bq-auto deep` · `/bq-plan deep` (complex-task approach + decomposition checklists)
- `/bq-assign delegate` (task-pack writing rules §14) · `/bq-review delegate` (cheap-output review §15)
- `/bq-review` · `/bq-red-team` · `/bq-verify` (evidence + drift checks)
- `/bq-skill-audit` (audit-before-add discipline)
- Confidence forecasts (pairs with CONFIDENCE_CALIBRATION_STRATEGY)

## The enforcement moves

1. **At task start:** require the §1 ritual — recover memory, verify current reality, restate goal + DONE definition. Block "build" framing until the audit-before-add check ran.
2. **At decomposition:** apply §2 — artifact-shaped tasks, ≤5 files each, dependency-ordered; >5 files → File-Responsibility Map.
3. **During work:** §3–§5 — externalize at boundaries, label every claim verified/inferred/assumed, UNVERIFIED for gaps.
4. **At uncertainty:** §6 — one question with default, or spike for 25–49% confidence; never promise through uncertainty.
5. **At delegate handoff:** §14 — no-guessing task packs + neutral prompts + the 10-rule card embedded.
6. **At review/verify:** §15–§16 — re-run evidence yourself; scan for drift symptoms (invented paths, stale counts, flat confidence, weasel words).
7. **Always:** the 10-rule card (`.bequite/state/FRONTIER_REASONING_SUMMARY.md`) is the minimum bar — if any rule would be violated, stop and fix before proceeding.

## When NOT to use this skill

- Trivial one-file tasks in fast mode (the contract alone suffices; coach adds overhead)
- Pure read-only orientation (`/bq-now`, `/bequite`)
- As a replacement for domain specialists — the coach governs HOW work proceeds, never WHAT the domain answer is

## Quality gate

- [ ] §1 ritual ran before first mutating tool call (evidence: memory reads visible)
- [ ] Claims labeled verified/inferred/assumed; UNVERIFIED used where honest
- [ ] No second source of truth created (extend/index instead)
- [ ] Confidence stated per CONFIDENCE_CALIBRATION_STRATEGY where tasks were forecast
- [ ] Delegate packs (if any) contain the 10-rule card + named disciplines
- [ ] Writeback complete (LAST_RUN / AGENT_LOG / CHANGELOG / SKILL_USAGE_LOG)

## Common mistakes

Loading the coach for trivia (overhead) · treating the playbook as commentary instead of checklists · letting "verify current reality" slide because the request sounded authoritative · flat confidence numbers · reviewing cheap-model output for style before acceptance criteria

## Failure handling

Playbook conflicts with an explicit user instruction → user wins; log the deviation · checklist can't be satisfied (e.g. no memory exists yet) → run `/bq-init` path first · drift symptoms detected in own output → stop, re-read sources, restate from evidence
