---
description: DEPRECATED ALIAS — use /bq-feature instead. /bq-add-feature is preserved for backwards compatibility; routes to /bq-feature's 12-type router.
---

# /bq-add-feature — ⚠ DEPRECATED ALIAS for `/bq-feature`

> **Status (alpha.14):** This command is a deprecated alias preserved for backwards compatibility. New work should use `/bq-feature` directly.
>
> **Why it's deprecated:** `/bq-feature` (alpha.2+) supersedes this. `/bq-feature` has a 12-type router (frontend / backend / database / auth / automation / scraping / cloud / admin / dashboard / cli / integration / security) that activates the right specialist skills automatically. `/bq-add-feature` predates this and lacks the router.
>
> **What happens if you run `/bq-add-feature`:** The agent recognizes the alias and routes to `/bq-feature` with the same arguments. Update your habits / scripts to call `/bq-feature` directly.

## Migration

Old:
```
/bq-add-feature "user can export bookings to CSV"
```

New:
```
/bq-feature "user can export bookings to CSV"
```

The new form auto-detects this as a backend + frontend feature; activates `bequite-backend-architect` + `bequite-frontend-quality` skills accordingly.

## Original spec (preserved below for reference)

> ⚠ The content below is the alpha.1 spec for `/bq-add-feature`. Kept for historical context. **Do not use this as the active workflow** — go to `/bq-feature`.

---

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

## Standardized command fields (alpha.6)

**Phase:** P2 — Planning and Build
**Status:** legacy alias — `/bq-feature` is the canonical command (alpha.2). This file remains for backwards compatibility.
**When NOT to use:** prefer `/bq-feature` for all new feature work — it includes the 12-type router + specialist skill activation.
**Preconditions:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`
**Required previous gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`
**Quality gate:** same as `/bq-feature` — mini-spec exists, user confirmed, files compile, test passes, acceptance verified, CHANGELOG updated
**Failure behavior:** same as `/bq-feature`
**Memory updates:** sets `FEATURE_DONE ✅`
**Log updates:** `AGENT_LOG.md`; CHANGELOG `[Unreleased]`

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
