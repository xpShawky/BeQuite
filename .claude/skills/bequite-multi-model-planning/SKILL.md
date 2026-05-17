---
name: bequite-multi-model-planning
description: Deep procedure for multi-model planning via manual paste. 5 collaboration modes (Parallel/Specialist/Debate/Judge/Red-Team). ToS-clean — no provider API. Invoked by /bq-multi-plan.
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Write"]
---

# bequite-multi-model-planning

You facilitate **multi-model thinking** for high-stakes decisions. Two (or more) frontier models think independently, then merge.

**Mode: manual paste.** User copies prompts from BeQuite into Claude.ai + ChatGPT browser tabs, copies responses back into BeQuite. No provider auth complexity, ToS-clean, $0 (uses subscription plans not API tokens).

**Browser-session reuse of consumer subscriptions is explicitly NOT recommended:** Anthropic + OpenAI ToS both forbid driving non-API endpoints from session cookies. Brittle to UI changes. Detection risk. Don't.

## When this skill activates

`/bq-multi-plan` is the slash command entry point. Reasons to invoke:

- Architectural decisions with two reasonable answers (Drizzle vs Prisma; Better-Auth vs Clerk; SQL vs document DB)
- Stack picks at scale tier transitions
- "We have a plan but I want a second opinion"
- Red-team review of a complete plan

## 5 collaboration modes

### 1. Parallel (default)

Both models plan independently, see neither output. BeQuite merges + identifies disagreements.

**Use when:** you want unbiased second opinion. Highest signal.

**Procedure:**
1. Generate identical prompts (only role-flavoring tweak)
2. User pastes both into their respective browser tabs
3. User pastes both responses back
4. BeQuite produces `MULTI_MODEL_COMPARISON.md` + final merged `IMPLEMENTATION_PLAN.md`

### 2. Specialist

Each model takes a different role. E.g. Claude as "frontend architect" and ChatGPT as "backend architect."

**Use when:** problem cleanly decomposes by area.

### 3. Debate

After Round 1 (Parallel), both models see the OTHER model's plan + respond. Round 2 is "now that you've read X's plan, what do you change / keep / refute?"

**Use when:** Round 1 surfaced specific disagreements you want each model to argue.

### 4. Judge

A third model (or a fresh instance) reads Round 1 outputs + picks/synthesizes the winner.

**Use when:** Parallel produced two reasonable answers and you want a tiebreaker.

### 5. Red-Team

After a plan exists, both models adversarially attack it. Goal: find what's broken.

**Use when:** you want to stress-test a committed plan before implementation.

## Prompt template (Parallel mode)

For each model, write a prompt at `.bequite/prompts/generated_prompts/PROMPT_<MODEL>.md`:

```markdown
# Planning prompt for <Claude | ChatGPT>

You are a senior software architect. Write an implementation plan for the
project described below. Produce the same structure /bq-plan would produce:

1. Vision
2. Current context
3. Non-goals
4. Architecture
5. Stack decision
6. File plan
7. Phase plan
8. Task plan
9. Test plan
10. Risks
11. Acceptance criteria
12. Rollback plan
13. Open questions

## Project context

<paste from DISCOVERY_REPORT.md §1-3>
<paste from SCOPE.md>

## Locked decisions

<paste from DECISIONS.md>

## Open questions

<paste from OPEN_QUESTIONS.md>

## Constraints

- Use 2026 stable versions only. Cite versions explicitly.
- Mark uncertainty explicitly — never "should work" or "probably."
- Cite license-incompatible libraries (AGPL is closed-source blocker for commercial).
- For every library mentioned, verify it exists on its registry; never propose a library you haven't seen.

Now write the plan.
```

Both prompts are **identical** — same body. The only differences:
- `PROMPT_CLAUDE.md` opens with "You are a senior software architect. (For Claude.)"
- `PROMPT_CHATGPT.md` opens with "You are a senior software architect. (For ChatGPT.)"

This way responses are comparable.

## Merge procedure

After the user pastes both responses:

### Step A — Save responses

- `.bequite/prompts/model_outputs/RESPONSE_CLAUDE.md`
- `.bequite/prompts/model_outputs/RESPONSE_CHATGPT.md`

### Step B — Build comparison table

For each section of the plan, walk through both responses:

| Section | Claude | ChatGPT | Agreement |
|---|---|---|---|
| Stack: framework | Next.js 15 | Next.js 15 | ✓ |
| Stack: ORM | Drizzle | Prisma | ✗ |
| Auth | Better-Auth | Clerk | ✗ |

### Step C — Tie-break

For each disagreement, apply the tie-break order:

1. **Iron Law wins.** E.g. Article IV "no destructive ops without ADR" trumps any specific tool pick.
2. **Doctrine wins.** E.g. `default-web-saas` Rule 9 mandates Better-Auth / Clerk / Supabase Auth → reject any "custom auth" suggestion.
3. **Freshness wins.** The option backed by /bq-research RESEARCH_REPORT.md with cited URLs.
4. **User picks.** Surface both sides + recommend; user chooses.

Capture the tie-breaks in `.bequite/plans/MULTI_MODEL_COMPARISON.md`:

```markdown
## Tie-breaks invoked

| Section | Choice | Rationale |
|---|---|---|
| Stack: ORM | Drizzle | Both Claude + ChatGPT had good arguments. Tie-break: Drizzle's migration story is more transparent for v1; user picked. |
| Auth | Better-Auth | Doctrine `default-web-saas` Rule 9 mandates one of Better-Auth/Clerk/Supabase. Both responses listed Better-Auth as second choice if not Clerk; Better-Auth chosen on no-vendor-lock-in preference. |
```

### Step D — Synthesize the final plan

Write `.bequite/plans/IMPLEMENTATION_PLAN.md` (preserve pre-merge as `IMPLEMENTATION_PLAN_PRE_MERGE.md`).

Combine:
- The agreement points (always go in the plan as-is)
- The disagreement-resolution choices
- Annotations where the tie-break came from

### Step E — Record decisions

Append to `.bequite/state/DECISIONS.md`:

```markdown
## <date> — Multi-model plan resolved

Models consulted: Claude (Opus 4.7), ChatGPT
Mode: Parallel

Decisions made via tie-break:
- Stack ORM: Drizzle (Claude favored; user picked)
- Auth: Better-Auth (Doctrine Rule 9)
- ...
```

## Cost framing (manual paste)

- $0 in API tokens (uses subscriptions you already pay for)
- Time cost: ~10 minutes per round (write prompt, paste, get responses, paste back)
- Quality: very high — two frontier models thinking independently catches MUCH more than one alone

For comparison: a Claude Code session for this same planning round might burn $5-$15 in Opus 4.7 tokens.

## Output discipline

When this skill produces a merged plan:

- Cite which model contributed each major decision (in comments)
- Highlight where both agreed (low-risk)
- Highlight where they disagreed (areas needing user attention)
- Never claim "the right answer" — surface options + tie-break + final choice
- Preserve PRE_MERGE plan so the user can audit the merge later

## When NOT to use multi-model

- **Simple feature work.** `/bq-plan` alone is enough.
- **Hot fixes.** `/bq-fix` is faster.
- **Trivial code reviews.** `/bq-review` alone is enough.
- **Decisions where you already have a strong recommendation from `/bq-research`.** No second opinion needed.

Use it sparingly. The multi-model overhead is ~10 minutes per cycle.

## Anti-patterns

- **Asking both models the SAME question with different phrasing.** Identical prompts only.
- **Showing Model B's answer to Model A and asking "is this right?"** That's Debate mode, not Parallel. Mode it correctly.
- **Picking the "more confident" response.** Confidence is not correctness. Use the tie-break order.
- **Merging by averaging.** Some choices are binary. Pick one + cite why.

---

## Quality gate (alpha.15)

Before claiming this skill's work complete:

- [ ] Artifacts produced match the skill's expected outputs
- [ ] All discipline rules in this skill were respected
- [ ] No banned weasel words in any completion claim
- [ ] Any tool / library added has a decision section per `.bequite/principles/TOOL_NEUTRALITY.md`
- [ ] Acceptance criteria for the invoking command's task are met
- [ ] `.bequite/state/MISTAKE_MEMORY.md` updated when a project-specific lesson surfaced
- [ ] `.bequite/logs/AGENT_LOG.md` entry appended

If any item fails, do not claim done — report PARTIAL with the specific gap.
