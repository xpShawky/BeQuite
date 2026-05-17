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

## Standardized command fields (alpha.6)

**Phase:** P1 — Product Framing and Research
**When NOT to use:** scope already locked and stable — use `/bq-feature` to add inside scope, or amend `SCOPE.md` directly + re-`/bq-scope` for scope changes.
**Preconditions:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`
**Required previous gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`; `RESEARCH_DONE` (recommended, not required)
**Quality gate:**
- `SCOPE.md` exists with IN / OUT / NON-GOALS clearly written
- Every IN item has a concrete acceptance signal
- User has explicitly confirmed
- Marks `SCOPE_LOCKED ✅`
**Failure behavior:**
- User keeps moving items between IN/OUT → re-draft once; if disagreement persists, ask which underlying assumption is unresolved (log to `ASSUMPTIONS.md`)
- Scope conflicts with prior `DECISIONS.md` entry → surface the conflict; require user resolution before advancing
**Memory updates:** Sets `SCOPE_LOCKED ✅`. Writes `SCOPE.md`. Appends decision entry to `DECISIONS.md`.
**Log updates:** `AGENT_LOG.md`.

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

---

## Gate check + memory preflight (alpha.15)

Before doing any work:

1. **Gate check.** Read `.bequite/state/WORKFLOW_GATES.md`. If this command's required gates aren't `✅`, refuse:
   > "You're trying to run this command, but `<required-gate>` is pending. Run `<prerequisite-command>` first."

   Don't proceed when a required gate is missing. Recommend the prerequisite + how to resume.

2. **Memory preflight.** Read these files first (per `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`):

   - `.bequite/state/PROJECT_STATE.md`
   - `.bequite/state/CURRENT_MODE.md`
   - `.bequite/state/CURRENT_PHASE.md`
   - `.bequite/state/LAST_RUN.md`
   - `.bequite/state/MISTAKE_MEMORY.md` — top 10–20 entries (skip mistakes already learned)
   - Other state files only when relevant to this command's scope (`DECISIONS.md` for architectural questions, `OPEN_QUESTIONS.md` for phase transitions, `MODE_HISTORY.md` when invoked via `/bq-auto`-style flows)

   **Use focused reads.** Don't load all of `.bequite/` every command.

## Memory writeback (alpha.15)

After successful completion:

- `.bequite/state/LAST_RUN.md` — this command + outcome
- `.bequite/state/WORKFLOW_GATES.md` — set this command's gate to `✅` if applicable
- `.bequite/state/CURRENT_PHASE.md` — advance if phase transitioned
- `.bequite/logs/AGENT_LOG.md` — append entry
- `.bequite/logs/CHANGELOG.md` `[Unreleased]` — only when material files changed (skip for read-only commands)
- `.bequite/state/MISTAKE_MEMORY.md` — append when a project-specific lesson surfaced
- `.bequite/state/MODE_HISTORY.md` — append mode + outcome (when invoked via `/bq-auto`-style mode)

**Failure behavior:** don't claim `✅ done` if any of the above wasn't completed. Report PARTIAL with the specific gap.
