---
description: Lock the problem's boundaries — what's IN, what's OUT, what's a NON-GOAL. Writes .bequite/work/<id>/spec.md.
---

# /bq-scope — lock the boundaries

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

You are forcing the user to commit to **what's in this version, what's out, and what's a permanent non-goal**. Scoping is the cheapest way to ship faster.

## Step 1 — Read context

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/work/<id>/research.md` (if exists)
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

## Step 4 — Write `work/<id>/spec.md`

`.bequite/work/<id>/spec.md`:

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

Full scope: .bequite/work/<id>/spec.md

Next: /bq-plan — write the implementation plan from these boundaries
```

## Rules

- **Force a target version on OUT items.** "Someday" is not a target.
- **Be specific about NON-GOALS.** "Won't ship X because Y" is reviewable. "Out of scope" alone is not.
- The user can override anything; this is a facilitation command, not a gate.

## Gates and failure behaviour

**Phase:** P1 — Product Framing and Research
**When NOT to use:** scope already locked and stable — use `/bq-feature` to add inside scope, or amend `work/<id>/spec.md` directly + re-`/bq-scope` for scope changes.
**Preconditions:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`
**Required previous gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`; `RESEARCH_COMPLETE` (recommended, not required)
**Quality gate:**
- `work/<id>/spec.md` exists with IN / OUT / NON-GOALS clearly written
- Every IN item has a concrete acceptance signal
- User has explicitly confirmed
- Marks `SCOPE_LOCKED ✅`
**Failure behavior:**
- User keeps moving items between IN/OUT → re-draft once; if disagreement persists, ask which underlying assumption is unresolved (log to `ASSUMPTIONS.md`)
- Scope conflicts with prior `DECISIONS.md` entry → surface the conflict; require user resolution before advancing
**Memory updates:** Sets `SCOPE_LOCKED ✅`. Writes `work/<id>/spec.md`. Appends decision entry to `DECISIONS.md`.
**Log updates:** `AGENT_LOG.md`.

## Memory files this command reads

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/work/<id>/research.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md`

## Memory files this command writes

- `.bequite/work/<id>/spec.md` (new)
- `.bequite/state/DECISIONS.md` (appended)
- `.bequite/state/OPEN_QUESTIONS.md` (resolved-items marked)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

`/bq-plan` — write the implementation plan

---

## Argument workflow

- **`/bq-scope from-interview "<transcript path>"`** — stakeholder interview transcript → spec + scope + assumptions + open questions + milestone sketch. Quotes from the transcript anchor every IN/OUT ruling; unstated wishes go to OPEN_QUESTIONS, not into scope.

## Next Command Recommendations

Per contract step 12: Required next W1.4 `/bq-plan`; router block per `COMMAND_ROUTER.md`.
