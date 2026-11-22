---
description: Unbiased multi-model planning via manual paste. External-model prompts contain ZERO mention of Claude's plan — each model starts from the same raw briefing and proposes independently. Merges into a final plan. ToS-clean, zero provider auth.
---

# /bq-multi-plan: a second plan that never saw the first

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

For high-stakes plans. A second model that is shown the first plan reviews it and anchors on it; a second model given the same raw briefing proposes its own. The user carries the prompt and the answer by hand between their own subscriptions: no API key, no provider login, no extra cost. Procedure: `bequite-delegation` (the collaboration modes: parallel, specialist, debate, judge, red team).

## Gates

Needs `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `CLARIFY_ANSWERED`, `RESEARCH_COMPLETE`, `SCOPE_LOCKED` (the briefing is built from verified research and a locked scope). Sets `MULTI_PLAN_DECISION` when the user picks: merged, or skipped.

## Steps

1. **Read** `work/<id>/spec.md`, `research.md`, `plan.md` if one exists, `.bequite/state/DECISIONS.md`, `OPEN_QUESTIONS.md`.
2. **Write one briefing, twice:** `.bequite/prompts/generated_prompts/PROMPT_CLAUDE.md` and `PROMPT_EXTERNAL.md`, identical except for the file name. Each holds the project context (stack, scope, decisions, open questions), the research excerpts, the output schema (the same sections as `/bq-plan`), and the constraints (be specific, cite versions, mark uncertainty).
3. **Keep the external prompt clean.** It must not mention any existing plan, recommendation or earlier proposal, and must not contain "review", "improve" or "critique": the external model is a first proposer, not a reviewer.
4. **Tell the user what to do:** paste `PROMPT_EXTERNAL.md` into the other model (ChatGPT, Gemini or another), and paste its full answer back or save it to `.bequite/prompts/model_outputs/RESPONSE_EXTERNAL.md`. Claude's own answer to the same prompt goes to `RESPONSE_CLAUDE.md`. Then wait.
5. **Compare** into `.bequite/plans/MULTI_MODEL_COMPARISON.md`: where they agree, soft disagreements (same goal, different route), hard disagreements, and what only one of them thought of.
6. **Resolve every hard disagreement**, showing both arguments in their own words, in this order:
   1. an option that breaks a hard rule (leaks data, hides a failure, skips a human gate) loses;
   2. a recorded project decision beats generic best practice;
   3. the freshest verified research beats memory;
   4. anything still tied is the user's choice.
7. **Write the merged plan** to `work/<id>/plan.md`, keeping the single-model plan as `work/<id>/plan-pre-merge.md` so the two can be compared. Each tie-break is logged with its reason in the comparison file and `DECISIONS.md`.
8. **Present** the merged plan and wait for approval, as `/bq-plan` does.

## Output

```
Multi-plan: agreed <n>, soft disagreements <n>, hard disagreements <n> (all resolved), unique additions <n>
Merged plan: .bequite/work/<id>/plan.md   before the merge: plan-pre-merge.md
Comparison: .bequite/plans/MULTI_MODEL_COMPARISON.md
Next after approval: /bq-assign
```

## Quality gate

The two prompts are identical; the external prompt names no model, tool or earlier plan; both answers are saved as files; no disagreement is left open; the pre-merge plan is preserved.

## Next Command Recommendations (typical)

`/bq-assign` after approval · `/bq-red-team "plan"` to attack the merged plan.
