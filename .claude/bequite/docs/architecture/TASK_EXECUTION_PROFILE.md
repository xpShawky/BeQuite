# Task Execution Profile (alpha.25)

Every task in `/bq-assign` (and every phase in `/bq-plan`) carries an **execution profile**: which model to run it on, at what effort, with what confidence, using which skills. This makes delegation explicit and lets the user route each task to the right-cost model.

## The profile block (per task / per phase)

```
Execution profile:
- Selected skills:    <skill(s) from the registry that this task needs>
- Recommended model:  <model id> (tier A frontier | B mid | C small/local)
- Effort:             <quick | standard | high | max>   (aliases: ultracode≈max, xhigh≈high+, high, med, low)
- Confidence:         <banded % + evidence level>       (per CONFIDENCE_RULES.md)
- Why:                <one line: why this model/effort for this task>
```

Example task list:
```
T1  Scaffold routes + types       skills: backend-architect · recommended: claude-sonnet-4-6 · effort: standard · confidence: 92% (verified)
T2  Payment + idempotency logic    skills: backend-architect, security-reviewer · recommended: claude-opus-4-8 · effort: max · confidence: 78% (inferred — concurrency risk)
T3  Update docs + changelog        skills: anti-hallucination · recommended: claude-haiku-4-5 · effort: quick · confidence: 95% (verified)
```

## Honest rules (read these)

- **BeQuite recommends a model; it does NOT switch models.** The active model is set by the user / the harness (`/model`). The profile says "run this task on X" — acting on it is the user's choice. BeQuite never silently changes model and reports any reroute (CLAUDE.md model rule).
- **Model names are examples, tool-neutral.** Current Claude IDs: `claude-opus-4-8` (frontier), `claude-sonnet-4-6` (mid), `claude-haiku-4-5` (small), `claude-fable-5`. Non-Claude models map to the same A/B/C tiers (`LOW_COST_MODEL_RULES.md`). Pick by task, not by habit.
- **Effort** = how much depth/verification the task gets (and, where the harness exposes it, the thinking/effort setting). `max`/`ultracode` = full reasoning + red-team + exhaustive verify; `quick` = smallest safe path. Effort is a discipline level, not a hard API guarantee.
- **Tier ↔ risk gate:** never recommend tier C (small/local) for the never-give-small list (production security, DB migrations, auth, payments, destructive edits, broad refactors, release approval — `LOW_COST_MODEL_RULES.md`). Those force tier A or A-reviewed.
- **Confidence** follows the banded forecast and must move with evidence; concurrency/consistency risk caps it at 89% until tests pass (`SYSTEM_DESIGN_REASONING_STANDARD.md`).

## Where it's written

`/bq-plan` → an execution profile per **phase** inside `IMPLEMENTATION_PLAN.md`. `/bq-assign` → an execution profile per **task** inside `TASK_LIST.md` (+ `TASK_CONFIDENCE.md` for the confidence trajectory). Delegate mode (`bequite-delegate-planner`) consumes the per-task model recommendation: tier-A model writes the pack, the recommended tier-B/C model executes each task, tier-A reviews.
