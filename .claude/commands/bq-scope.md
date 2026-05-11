---
description: Lock the problem's boundaries — what's IN, what's OUT, what's a NON-GOAL. Writes .bequite/plans/SCOPE.md.
---

# /bq-scope — lock the boundaries

You are forcing the user to commit to **what's in this version, what's out, and what's a permanent non-goal**. Scoping is the cheapest way to ship faster.

## Step 1 — Read context

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/audits/RESEARCH_REPORT.md` (if exists)
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md`

## Step 2 — Draft the three lists

### IN scope (this version ships these)
Concrete, deliverable features. "Login with email + password" not "auth system".

### OUT of scope (later but not now)
Features that are valid but deferred. Set a target version (`v2`, `v1.1`, etc.).

### NON-GOALS (never)
Things explicitly NOT in this product's mission. Helps reviewers reject scope-creep PRs later.

Examples:

```
IN scope (v1):
  - User can sign up with email + password
  - User can create a booking
  - Admin can view today's bookings
  - Email confirmation via Resend

OUT of scope (v2):
  - Recurring bookings
  - Multi-tenant (per-business)
  - SMS notifications
  - Mobile app

NON-GOALS:
  - Marketplace (this is a single-business app)
  - Payment processing (paid offline)
  - AI suggestions
```

## Step 3 — Present + confirm

Show the draft to the user. They can:
- Accept as-is
- Move items between IN / OUT / NON-GOALS
- Add items

Iterate once. After the user accepts, write the report.

## Step 4 — Write SCOPE.md

`.bequite/plans/SCOPE.md`:

```markdown
# Scope

**Locked:** <date>
**Target version:** v1 (or as agreed)

## IN scope

- (...)

## OUT of scope (deferred)

| Item | Target version |
|---|---|
| ... | v1.1 |
| ... | v2 |

## NON-GOALS

- (...)

## Acceptance criteria

- All "IN scope" items have an acceptance test in /bq-plan's test plan.
- The plan's task list only contains IN-scope tasks.
- A PR that adds an OUT-of-scope feature is rejected at review.

## Re-scoping triggers

If any of these happen, run /bq-scope again:

- Scope creep PR proposed
- New stakeholder request that doesn't fit IN
- Unexpected blocker forces dropping an IN item to OUT
```

## Step 5 — Update state

- Append "Scope locked" + summary to `.bequite/state/DECISIONS.md`
- Mark relevant items resolved in `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/logs/AGENT_LOG.md` entry

## Step 6 — Report back

```
✓ Scope locked

IN:        <count> items
OUT:       <count> items (deferred)
NON-GOALS: <count> items

Full scope: .bequite/plans/SCOPE.md

Next: /bq-plan — write the implementation plan from these boundaries
```

## Rules

- **Force a target version on OUT items.** "Someday" is not a target.
- **Be specific about NON-GOALS.** "Won't ship X because Y" is reviewable. "Out of scope" alone is not.
- The user can override anything; this is a facilitation command, not a gate.

## Memory files this command reads

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/audits/RESEARCH_REPORT.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md`

## Memory files this command writes

- `.bequite/plans/SCOPE.md` (new)
- `.bequite/state/DECISIONS.md` (appended)
- `.bequite/state/OPEN_QUESTIONS.md` (resolved-items marked)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

`/bq-plan` — write the implementation plan
