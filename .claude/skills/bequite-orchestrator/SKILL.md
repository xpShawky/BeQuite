---
name: bequite-orchestrator
description: BeQuite's global orchestration brain — knows all command families, all 30 skills, gates, routers, auto-mode rules, context compaction, and system-design risk rules. Activates on /bequite, /bq-suggest, /bq-discover, /bq-plan, /bq-auto, /bq-implement, /bq-review, /bq-verify, /bq-skill-audit, and whenever there is command/skill conflict, confusion, duplicated workflow, unclear next step, or a task no existing capability covers (missing-capability detection).
---

# bequite-orchestrator — the global brain

## Purpose

One skill that holds the map of everything BeQuite can do, so major workflows choose commands and skills from the **Orchestration Map** instead of vibes — and admit it when nothing fits. Source of truth: `.bequite/state/ORCHESTRATION_MAP.md` · model: `docs/architecture/BEQUITE_ORCHESTRATION_MODEL.md`. Markdown only — this is a map + protocol, not a runtime.

## When this skill activates

- The 9 orchestration-consulting commands: bequite · suggest · discover · plan · auto · implement · review · verify · skill-audit
- ANY conflict: two commands seem right · skills overlap · routers disagree · duplicated workflow suspected
- ANY confusion about next step, or a task that matches no existing command/skill/workflow

## Procedure

1. **Read the map first** (`ORCHESTRATION_MAP.md`) — it's a compact index; never load the full corpus to orient.
2. **Locate the task** in the pipeline: intent → command router → skill router → risk check → confidence → plan → implement → guard → verify → evidence → writeback → next.
3. **Resolve conflicts by boundary, not preference** — apply the map's near-miss distinctions (audit≠review · scope≠spec≠plan · pain-radar≠make-money · proposal≠offer · verify≠release-readiness). Still ambiguous → ask ONE high-value question.
4. **Detect missing capability honestly.** Nothing fits ⇒ emit:

```
Missing Capability Detected:
- Needed capability:
- Why existing commands/skills are not enough:
- Temporary workaround:
- Recommended new skill/command/spec:
- Should this be built now or parked?
- Confidence:
```

…log to `OPEN_QUESTIONS.md` / `FEATURE_EXPANSION_ROADMAP.md`; proceed with the workaround only if safe. Never stretch a wrong command to fake coverage.
5. **Enforce the sequence guards:** auto mode follows the 15-step anti-skip sequence (`AUTO_MODE_RULES.md`); risky domains get the System Design Risk Check; context pressure triggers compaction (`CONTEXT_COMPACTION_RULES.md`); smaller models get tiered per `LOW_COST_MODEL_RULES.md`.

## What this skill reads / writes

Reads: ORCHESTRATION_MAP · COMMAND_ID_MAP · SKILL_REGISTRY (+ routers on demand) · gates · phase/mode. Writes: nothing of its own — it directs other layers' writes (NEXT_COMMAND_LOG entries, OPEN_QUESTIONS for missing capabilities).

## When NOT to use

Trivial single-step reads (now/help/explain) — they have fixed behavior. Don't re-derive the map per message; consult it at decision points.

## Quality gate

An orchestration decision must name the map section it used (category boundary, signal row, journey route, or missing-capability ruling). "I picked X" without a cited boundary is vibes — redo it. Conflicts resolved without consulting the map = drift violation (skill-audit checks NEXT_COMMAND_LOG for this).
