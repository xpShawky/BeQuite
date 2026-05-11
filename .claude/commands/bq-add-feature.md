---
description: Add a feature safely. Mini spec → mini plan → implementation → tests, atomically. For features that fit inside one session.
---

# /bq-add-feature — safe feature addition

You are adding **one feature**. Tighter than `/bq-plan` + `/bq-implement` (which are the full workflow); this is a focused mini-cycle that fits in one session.

## When to use this vs /bq-plan + /bq-implement

| Use /bq-add-feature when... | Use full /bq-plan workflow when... |
|---|---|
| Feature is small (~1-3 hours of work) | Feature is large (multi-day) |
| Stack + architecture already locked | Stack/architecture choice is part of the feature |
| One person can do it | Multiple people coordinate |
| Acceptance is obvious | Acceptance needs negotiation |

## Step 1 — Get the feature description

If the user typed `/bq-add-feature` alone, ask:
> "What feature? One sentence. (Example: 'Add a CSV export button on the bookings page')"

If they passed an argument like `/bq-add-feature "csv export"`, use that.

## Step 2 — Read context

- `.bequite/state/PROJECT_STATE.md` — current stack
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (if exists) — existing architecture
- `.bequite/audits/DISCOVERY_REPORT.md` — to know where things live in the repo

## Step 3 — Write a mini-spec

Save to `.bequite/plans/feature-<slug>.md`:

```markdown
# Feature: <one-line title>

**Generated:** <date>
**Spec author:** /bq-add-feature

## What

(2-3 sentences describing what the feature does.)

## Why

(1 sentence: what problem does this solve / which user wins.)

## In scope (this feature)

- (list of concrete deliverables)

## Out of scope (intentionally)

- (related things this feature does NOT include)

## Files this will touch

| File | Action |
|---|---|
| `app/dashboard/bookings/page.tsx` | MODIFIED (add CSV button) |
| `app/api/bookings/export/route.ts` | NEW |
| `lib/csv.ts` | NEW (helper) |
| `tests/e2e/bookings-csv.spec.ts` | NEW |

## Acceptance criteria

- (specific, testable, no weasel words)

## Test plan

- Unit: `lib/csv.ts` round-trips a known set of rows.
- E2E: navigate to /dashboard/bookings, click Export CSV, file downloads, content matches.

## Implementation order

1. Add `lib/csv.ts` (smallest unit, easy to test)
2. Add API route `/api/bookings/export`
3. Add CSV button to page
4. Add E2E test
5. Run /bq-verify subset
```

## Step 4 — Present + confirm

Show the user the mini-spec. Ask:
> "Spec looks good? I'll implement once you say yes (or fix what's wrong)."

## Step 5 — Implement (only after confirmation)

Once confirmed, work through the "Implementation order" in §Step 3:
- Read files first
- Make minimal changes per file
- Run the test after each material change (or at the end if test suite is fast)
- Verify the acceptance criterion explicitly

This is essentially `/bq-implement` but scoped to one feature.

## Step 6 — Update logs + tests

- Append to `.bequite/logs/CHANGELOG.md` under [Unreleased]:
  ```
  ### Added
  - <feature title> (see .bequite/plans/feature-<slug>.md)
  ```
- Append to `.bequite/logs/AGENT_LOG.md`:
  ```
  /bq-add-feature: <title>; <count> files touched; tests <pass / fail>
  ```
- Update `.bequite/state/LAST_RUN.md`

## Step 7 — Report back

```
✓ Feature added — <title>

Spec:           .bequite/plans/feature-<slug>.md
Files touched:  <count>
Tests:          <pass / total>
Acceptance:     <one-line confirmation>

Next: /bq-review (review your own changes) or /bq-test (full test sweep)
```

## Rules

- **Spec first.** Don't write code until the user confirms the mini-spec.
- **Acceptance criteria are concrete.** "Working" is not. "Returns 200 with a CSV body" is.
- **Add a test.** Every new feature has at least one test. No exceptions for "trivial" features.
- **Update CHANGELOG.** Even small features.

## Memory files this command reads

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/plans/IMPLEMENTATION_PLAN.md`
- `.bequite/audits/DISCOVERY_REPORT.md`

## Memory files this command writes

- `.bequite/plans/feature-<slug>.md` (new)
- The feature's source files (new + modified)
- `.bequite/logs/CHANGELOG.md` (appended)
- `.bequite/logs/AGENT_LOG.md` (appended)
- `.bequite/state/LAST_RUN.md` (updated)

## Usual next command

- `/bq-review` — review the feature
- `/bq-test` — full test sweep
- `/bq-add-feature` — add another
