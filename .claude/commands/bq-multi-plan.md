---
description: Manual-paste multi-model planning. Generates prompts for Claude and ChatGPT, waits for the user to paste back both outputs, then merges into a final plan. ToS-clean, zero provider auth.
---

# /bq-multi-plan — Claude + ChatGPT think independently, then merge

You are facilitating a **multi-model planning session** where two frontier models think about the problem independently, and BeQuite merges their outputs into a final plan. This is the manual-paste mode — ToS-clean, no provider auth, works today with any Claude Pro + ChatGPT Plus subscription.

This commands invokes the `bequite-multi-model-planning` skill for the deep procedure.

## When to use this

- High-stakes architectural decisions
- Stack picks where two frameworks have genuine trade-offs
- When `/bq-plan` produces a plan but you sense bias toward one approach
- When `/bq-research` left a tie

**Don't use** for simple feature work — `/bq-plan` alone is sufficient.

## Step 1 — Read context

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/audits/RESEARCH_REPORT.md`
- `.bequite/plans/SCOPE.md`
- `.bequite/state/DECISIONS.md`
- `.bequite/state/OPEN_QUESTIONS.md`

## Step 2 — Generate two prompts

Write two prompts, one for each model. Each prompt is a self-contained briefing.

Save them:
- `.bequite/prompts/generated_prompts/PROMPT_CLAUDE.md`
- `.bequite/prompts/generated_prompts/PROMPT_CHATGPT.md`

Each prompt should include:

1. **Role:** "You are a senior software architect. Write an implementation plan for the project described below."
2. **Project context:** stack, scope, decisions so far (excerpts from BeQuite memory)
3. **Open questions to resolve:** from OPEN_QUESTIONS.md
4. **Output schema:** match the structure from `/bq-plan` (vision, architecture, stack decision, file plan, phase plan, task plan, risks, acceptance, rollback)
5. **Constraint:** "Be specific. Cite library versions. Mark uncertainty explicitly."

Phrase the prompt **identically** for both models — only the role-flavoring tweaks differ (e.g. one ends "from Claude's perspective"; the other "from GPT's perspective" — but the content is otherwise identical).

## Step 3 — Tell the user what to do

Print this in chat:

```
Two prompts generated:

  .bequite/prompts/generated_prompts/PROMPT_CLAUDE.md
  .bequite/prompts/generated_prompts/PROMPT_CHATGPT.md

Open each in your Claude (Claude.ai or claude.com) and ChatGPT (chat.openai.com)
browser tabs, paste each prompt, get the response, then come back and:

  1. Save Claude's response as: .bequite/prompts/model_outputs/RESPONSE_CLAUDE.md
  2. Save ChatGPT's response as: .bequite/prompts/model_outputs/RESPONSE_CHATGPT.md
  3. Run /bq-multi-plan merge

(or just paste both responses here and I'll save them for you)
```

## Step 4 — Wait for the user to paste responses

The user may either:
- Save the files manually and run `/bq-multi-plan merge`
- Paste the responses directly in chat → you save them to the model_outputs/ paths

## Step 5 — Merge

Once both files exist, read them and produce a comparison + merged plan.

### Comparison table

Section by section, what did each model say? Where do they agree? Where disagree?

```markdown
| Section | Claude said | ChatGPT said | Agreement? |
|---|---|---|---|
| Stack: framework | Next.js 15 | Next.js 15 | ✓ same |
| Stack: ORM | Drizzle | Prisma | ✗ disagree |
| Auth | Better-Auth | Clerk | ✗ disagree |
| ... |
```

### Where they disagree

For each disagreement:
1. Surface BOTH arguments side-by-side
2. Pull in any related items from `RESEARCH_REPORT.md`
3. Propose a tie-break — either by Iron Law beats Doctrine beats freshness, OR by asking the user to pick

### Final merged plan

Write `.bequite/plans/IMPLEMENTATION_PLAN.md` (overwrites the single-model plan if it exists):

```markdown
# Implementation Plan (multi-model merge)

**Generated:** <ISO 8601 UTC>
**Models consulted:** Claude (Opus 4.7), ChatGPT
**Merge strategy:** Iron Law beats Doctrine beats user-pick

## ... (same shape as /bq-plan output)
```

Plus a separate file documenting the comparison:

`.bequite/plans/MULTI_MODEL_COMPARISON.md`:

```markdown
# Multi-model plan comparison

**Date:** <date>
**Models:** Claude, ChatGPT

## Agreement areas

(items both models agreed on)

## Disagreement areas

| Topic | Claude | ChatGPT | Resolution | Rationale |
|---|---|---|---|---|

## Tie-breaks invoked

- (Iron Law III "memory discipline" → use the option that integrates with .bequite/state)
- (User preference for X)
- (...)
```

## Step 6 — Update state

- Append "Multi-model plan completed" to DECISIONS.md
- `.bequite/state/LAST_RUN.md` updated
- `.bequite/logs/AGENT_LOG.md` appended

## Step 7 — Report back

```
✓ Multi-model planning complete

Models consulted:    Claude, ChatGPT
Agreement points:    <count>
Disagreement points: <count>
Tie-breaks invoked:  <count>

Final plan:    .bequite/plans/IMPLEMENTATION_PLAN.md
Comparison:    .bequite/plans/MULTI_MODEL_COMPARISON.md

Next: /bq-assign — break the plan into actionable tasks
```

## Rules

- **Manual paste, not API.** This avoids provider auth complexity + respects Anthropic and OpenAI ToS (Browser-session reuse is explicitly NOT allowed in either provider's terms).
- **Same prompt for both models.** Only role-flavoring differs.
- **Tie-break order:** Iron Law beats Doctrine beats latest-research-evidence beats user-pick.
- **Cost:** $0 (uses subscription plans, not API tokens).

See `.claude/skills/bequite-multi-model-planning/SKILL.md` for the full deep procedure including the 5 collaboration modes (Parallel / Specialist / Debate / Judge / Red-Team).

## Memory files this command reads

- `.bequite/audits/*.md`
- `.bequite/plans/*.md`
- `.bequite/state/*.md`
- `.bequite/prompts/model_outputs/RESPONSE_CLAUDE.md` (when present)
- `.bequite/prompts/model_outputs/RESPONSE_CHATGPT.md` (when present)

## Memory files this command writes

- `.bequite/prompts/generated_prompts/PROMPT_CLAUDE.md`
- `.bequite/prompts/generated_prompts/PROMPT_CHATGPT.md`
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (overwrites — but preserve the pre-merge version as IMPLEMENTATION_PLAN_PRE_MERGE.md)
- `.bequite/plans/MULTI_MODEL_COMPARISON.md`
- `.bequite/state/DECISIONS.md` (appended)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

`/bq-assign` — break the merged plan into actionable tasks
