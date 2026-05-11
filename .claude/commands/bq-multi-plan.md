---
description: Unbiased multi-model planning via manual paste. External-model prompts contain ZERO mention of Claude's plan — each model starts from the same raw briefing and proposes independently. Merges into a final plan. ToS-clean, zero provider auth.
---

# /bq-multi-plan — independent multi-model planning

## Purpose

Get a genuinely **independent second opinion** on the plan. The external model (ChatGPT / Gemini / other) is given the **same raw briefing** Claude received — and **explicitly NOT told what Claude proposed**. This is the unbiased-merge protocol: each model thinks alone, BeQuite reconciles afterwards.

This is the key fix vs. naïve "ask another model to review the plan" — those reviews are biased toward agreement. Independent proposals reveal real disagreement.

ToS-clean — manual paste only, no provider API, costs $0 (uses your subscription tabs).

## When to use it

- High-stakes architectural decisions (DB choice, auth provider, scaling tier)
- Stack picks where two options have genuine trade-offs
- When `/bq-plan` produces output but you sense bias
- When `/bq-research` left a tie

**Don't use for**: trivial features, fix cycles, prototypes. Use `/bq-plan` alone.

## Preconditions

- `BEQUITE_INITIALIZED ✅`
- `MODE_SELECTED ✅`
- `RESEARCH_DONE ✅` (you need verified research to brief external models)
- `SCOPE_LOCKED ✅`

## Required previous gates

- `BEQUITE_INITIALIZED`
- `MODE_SELECTED`
- `CLARIFY_DONE`
- `RESEARCH_DONE`
- `SCOPE_LOCKED`

## Files to read

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/audits/RESEARCH_REPORT.md`
- `.bequite/plans/SCOPE.md`
- `.bequite/state/DECISIONS.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (if exists — used internally for comparison ONLY; **not** included in external prompts)

## Files to write

- `.bequite/prompts/generated_prompts/PROMPT_CLAUDE.md`
- `.bequite/prompts/generated_prompts/PROMPT_EXTERNAL.md` (for ChatGPT / Gemini / etc.)
- `.bequite/prompts/model_outputs/RESPONSE_CLAUDE.md` (user pastes Claude.ai response here, or you save it)
- `.bequite/prompts/model_outputs/RESPONSE_EXTERNAL.md` (user pastes external model response here)
- `.bequite/plans/MULTI_MODEL_COMPARISON.md`
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (rewritten — merged version)
- `.bequite/plans/IMPLEMENTATION_PLAN_PRE_MERGE.md` (the single-model plan, preserved)
- `.bequite/state/WORKFLOW_GATES.md` (`MULTI_PLAN_DONE ✅` once user picks: yes-merged / no-skipped)
- `.bequite/state/DECISIONS.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## The unbiased-prompt protocol

**Critical:** the external-model prompt MUST contain:

✅ The same project context Claude has (stack, scope, decisions, open questions)
✅ The same research briefing (RESEARCH_REPORT.md excerpts)
✅ The same output schema (13 sections, per `/bq-plan`)
✅ The same constraints (be specific, cite versions, mark uncertainty)

❌ **No mention of Claude's plan**
❌ **No mention of Claude's recommendations**
❌ **No mention of what BeQuite already proposed**
❌ **No phrases like "review", "improve", "critique" — the external model is a primary proposer, not a reviewer**

The external model starts from zero. It writes its own plan independently.

## Steps

### 1. Generate two prompts

#### Prompt for Claude (`PROMPT_CLAUDE.md`)

```markdown
You are a senior software architect. Write an implementation plan for the project below.

## Project context

<excerpts from DISCOVERY_REPORT.md, SCOPE.md, DECISIONS.md>

## Verified research

<excerpts from RESEARCH_REPORT.md, all 11 dimensions>

## Open questions

<list from OPEN_QUESTIONS.md>

## Output schema (15 sections)

1. Vision
2. Current context
3. Non-goals
4. Architecture
5. Stack decision
6. File plan
7. Phase plan
8. Task plan (atomic ≤5min tasks)
9. Test plan
10. Risks
11. Security considerations
12. Deployment + DevOps
13. Acceptance criteria
14. Rollback plan
15. Open questions

## Constraints

- Be specific. Cite library versions. Mark uncertainty explicitly.
- No "should / probably / seems to / appears to / I think it works / might".
- Each task has ONE acceptance criterion.
- No code — markdown only.
```

#### Prompt for external model (`PROMPT_EXTERNAL.md`)

**Identical to Claude's prompt** — same context, same research, same questions, same schema, same constraints.

**Do NOT include any of these phrases:**
- "Claude proposed..."
- "Improve on the existing plan..."
- "Review the following..."
- "Critique..."
- "Anthropic..." / "Claude..." / "BeQuite..." anywhere in the prompt

The external model is a **primary proposer**, not a reviewer.

### 2. Tell the user what to do

Print in chat:

```
Two prompts generated:

  .bequite/prompts/generated_prompts/PROMPT_CLAUDE.md
  .bequite/prompts/generated_prompts/PROMPT_EXTERNAL.md

Both prompts are IDENTICAL except for which model gets which file.
Neither prompt mentions the other model. Both start from zero.

Steps:
  1. Open Claude (claude.ai or claude.com) in your browser
  2. Paste PROMPT_CLAUDE.md → wait for response → copy response
  3. Save Claude's response to: .bequite/prompts/model_outputs/RESPONSE_CLAUDE.md
  4. Open ChatGPT (chat.openai.com) OR Gemini (gemini.google.com) — your call
  5. Paste PROMPT_EXTERNAL.md → wait for response → copy response
  6. Save external response to: .bequite/prompts/model_outputs/RESPONSE_EXTERNAL.md
  7. Come back here and run /bq-multi-plan merge

(Or paste both responses here in chat — I'll save them for you.)
```

### 3. Wait for the user

The user pastes both responses (either to disk or in chat).

Once both files exist:

### 4. Read both responses + compare

Section by section, identify:

- **Agreements** — both models propose the same thing
- **Soft disagreements** — different details, same intent
- **Hard disagreements** — fundamentally different approach
- **Unique additions** — one model raised something the other missed

Build the comparison table:

```markdown
| Section | Claude proposed | External proposed | Agreement? |
|---|---|---|---|
| Stack: framework | Next.js 15 | Next.js 15 | ✓ same |
| Stack: ORM | Drizzle | Prisma | ✗ hard disagree |
| Auth | Better-Auth | Clerk | ✗ hard disagree |
| Test runner | Vitest | Vitest | ✓ same |
| Hosting | Vercel | Fly.io | ✗ hard disagree |
| Database | Supabase Postgres | Neon Postgres | ⚠ soft disagree (same DB, different host) |
| Email | Resend | Postmark | ✗ hard disagree |
| ... | | | |
```

### 5. Resolve disagreements via tie-break order

**Tie-break order:**

1. **Iron Law beats Doctrine** — if one option violates an Iron Law (e.g. exfiltrates PII, breaks honest reporting), reject it
2. **Doctrine beats convention** — active doctrine wins over generic best practice
3. **Latest-verified-research beats memory** — if RESEARCH says option A is fresher / safer / cheaper in 2026, prefer A
4. **User picks the rest** — for genuine ties or user-preference items

For each hard disagreement:
- Present BOTH arguments verbatim
- Pull in related RESEARCH evidence
- Apply tie-break order
- If still tied → ask user

### 6. Write the merged plan

`.bequite/plans/IMPLEMENTATION_PLAN.md` (overwrites; the single-model version is preserved as `IMPLEMENTATION_PLAN_PRE_MERGE.md`):

```markdown
# Implementation Plan (multi-model merge)

**Generated:** <ISO 8601 UTC>
**Models consulted:** Claude, <External model name>
**Disagreements:** <count>
**Tie-breaks applied:** <count>
**User picks:** <count>

## ... (15 sections, same structure as /bq-plan)
```

For sections where models disagreed, note which model proposed what + why we picked the chosen option.

### 7. Write the comparison file

`.bequite/plans/MULTI_MODEL_COMPARISON.md`:

```markdown
# Multi-model plan comparison

**Date:** <date>
**Models:** Claude, <External>

## Agreement areas

(items both models agreed on — copy verbatim)

## Soft-disagreement areas

| Topic | Claude | External | Resolution |
|---|---|---|---|

## Hard-disagreement areas

| Topic | Claude argument | External argument | Resolution | Rationale |
|---|---|---|---|---|

## Tie-breaks applied

- (Iron Law III → use option that integrates with .bequite/state)
- (Doctrine web-saas → axe-core CI gate required)
- (RESEARCH §1 freshness → Drizzle (2026-04) over Prisma (2026-02))
- (User pick: Vercel over Fly.io)

## Unique additions

- (Claude raised X that External missed)
- (External raised Y that Claude missed)
```

### 8. Update state

- Append "Multi-model plan merged on <date>" to `DECISIONS.md`
- Mark `MULTI_PLAN_DONE ✅` in `WORKFLOW_GATES.md`
- `LAST_RUN.md` updated
- `AGENT_LOG.md` appended

### 9. Report back

```
✓ Multi-model planning complete

Models consulted:    Claude, <External>
Sections agreed:     <count>
Hard disagreements:  <count>
Tie-breaks applied:  <count>
User picks:          <count>

Final plan:    .bequite/plans/IMPLEMENTATION_PLAN.md
Pre-merge:     .bequite/plans/IMPLEMENTATION_PLAN_PRE_MERGE.md
Comparison:    .bequite/plans/MULTI_MODEL_COMPARISON.md

Next: /bq-assign — break the merged plan into actionable tasks
```

## Output format

Step-by-step narration. User confirms each tie-break that requires their pick.

## Quality gate

- Both prompts are byte-identical except for filename
- External prompt does NOT mention Claude / BeQuite / "review" / "critique"
- Both responses saved as files
- Every disagreement resolved (none left "TBD")
- Tie-breaks logged with rationale
- Merged plan has same 15-section structure as `/bq-plan` output
- `IMPLEMENTATION_PLAN_PRE_MERGE.md` preserved for diff review

## Failure behavior

- User can't paste responses (browser issues, etc.) → save the prompts to disk and continue manually later
- External model refuses or produces low-quality output → save what we got + note quality concern; fall back to single-model plan
- Hard disagreement that user can't resolve → pause, document in OPEN_QUESTIONS.md, exit gracefully
- More than 50% disagreement → suggest the user pause and re-run `/bq-research` (fundamental gap)

## Rules

- **Manual paste, not API.** Respects Anthropic and OpenAI ToS.
- **Both prompts identical.** No bias contamination from either side.
- **Tie-break order is fixed.** Don't ad-hoc.
- **Preserve the pre-merge plan** as `IMPLEMENTATION_PLAN_PRE_MERGE.md` so users can diff.
- **Cost: $0** (uses subscription plans, not API tokens).

See `.claude/skills/bequite-multi-model-planning/SKILL.md` for the deep procedure (5 collaboration modes: Parallel / Specialist / Debate / Judge / Red-Team).

## Skills activated

- `bequite-multi-model-planning` (the core procedure)
- `bequite-project-architect` (for architecture reconciliation)

## Usual next command

- `/bq-assign` — break the merged plan into actionable tasks
- `/bq-implement` — start the workhorse loop
