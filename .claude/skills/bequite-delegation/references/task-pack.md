# Task pack format (load on demand)

One file, `work/<id>/tasks.md`, so the builder reads one thing. Each task block:

```markdown
## T3 - Add CSV export to the bookings page        [ ] pending
Why: owners reconcile bookings in a spreadsheet every week.
Read (do not edit): src/bookings/list.ts, src/lib/csv.ts
Edit: src/bookings/export.ts (new), src/bookings/routes.ts
Do not touch: anything else; especially src/auth/**
Steps:
1. Create export.ts with exportBookings(rows) using csv.ts toCsv().
2. Add GET /bookings/export in routes.ts after the GET /bookings route.
Edge cases: zero rows -> header line only. Over 10,000 rows -> stream; if unsure, mark [?].
Common mistakes (from MISTAKE_MEMORY): dates must be ISO 8601 UTC.
Test: npm test -- bookings.export   -> expect "3 passed, 0 failed"
Hard gate: none
Rollback: git checkout -- src/bookings/routes.ts && rm src/bookings/export.ts
```

Builder status marks: `[x]` passed with the test pasted · `[!]` failed twice, stopped · `[?]` the pack is unclear, stopped · `[gate]` waiting for the user.

## Review block (strong model, after the build)

```markdown
## Review T3: approved with comments
- placement, naming, integration, tests, security: ok
- comment: no test for zero rows; add one (follow-up T3b)
```

Rejected: the reason with `path:line`, the exact fix steps, and "re-run T3 after the fix".

## Neutral briefing for independent plans (shape B)

```markdown
# Planning brief (identical for every model)
Problem: <from spec.md, verbatim>
Constraints: <stack, budget, scale, deadlines>
Locked decisions: <from DECISIONS.md>
Open questions: <list>
Write: architecture, stack choice with versions, phases, risks, acceptance criteria, rollback, open questions.
Rules: name only libraries you can point to in their registry; mark uncertainty explicitly.
```

Never include another model's plan, the agent's own preference, or "we are leaning towards".
