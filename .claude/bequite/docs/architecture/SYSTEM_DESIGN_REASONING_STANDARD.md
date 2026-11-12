# System Design Reasoning Standard

A feature that looks good and fails functionally is a failure. This standard makes system-design reasoning **mandatory and structured** wherever it matters — so the workflow (not model brilliance) catches the one-item-two-buyers class of bug. Enforced via planning/implementation commands (plan · feature · implement · auto) and verified by review/verify + Guard Pass.

## 1. When the Risk Check is MANDATORY

Any task touching: payments · inventory · bookings · authentication · permissions/tenancy · database writes · concurrent actions · queues · external APIs · webhooks · file uploads · user-generated content · admin actions · production deployment · security-sensitive logic. Outside these domains the check may be marked `Not applicable — reason: …` (silent omission is a contract violation).

## 2. The mandatory output block

```
System Design Risk Check:
- Domain:
- Critical entities:
- State transitions:           (status machines; invalid transitions named)
- Concurrent user risks:       (what happens when two actors race?)
- Data consistency risks:      (partial failure, dual writes, retries)
- Failure modes:               (what breaks, how visibly)
- Recovery behavior:           (retry / rollback / compensate / alert)
- Security concerns:
- Edge cases:
- Tests required:              (race/idempotency/transition tests named)
- Confidence:                  (banded % per CONFIDENCE_RULES)
- Unknowns:                    (each one: blocking or accepted-risk?)
```

A plan whose risk check has blocking unknowns does not proceed to implementation.

## 3. Domain risk libraries (recognize these on sight)

**E-commerce:** double purchase of last stock item · payment succeeds but order creation fails · webhook retries create duplicate orders · refund state not synced with order state · cart price vs charge-time price drift.
**Booking:** two users book the same slot · cancellation-vs-booking race · timezone errors (store UTC, render local) · no-show/grace rules · double-reminder sends.
**SaaS:** cross-tenant data access via missing permission check · subscription state mismatch (provider vs DB) · usage-quota race · webhook idempotency failure · trial/paid boundary bugs.
**Dashboards:** stale metrics presented as live · wrong aggregation (avg of avgs) · missing empty/zero states · misleading chart scales · timezone-split daily buckets.
**AI apps:** prompt injection · data leakage into prompts/logs · tool over-permission · memory poisoning · unsafe action execution without human gate.
**Automation:** duplicate triggers · retry storms · webhook replay · partial failure mid-pipeline · missing idempotency keys · runaway schedules (watch-budget rule from scraping skill applies).

## 4. The reasoning drill (how to fill the block honestly)

1. Name the **entities** and draw their **status machines** (an order is not a row; it's a state machine).
2. For every write: *what if it runs twice?* (idempotency) *what if it half-finishes?* (consistency) *what if two run at once?* (locking/reservation).
3. For every external call: *what if it's slow, fails, succeeds-but-times-out, or retries?*
4. For every user-visible flow: *what does each user see when the race is lost?* (honest error beats silent corruption).
5. Convert each identified risk into a **named test** — a risk without a test is a wish.

## 5. Verification linkage

`/bq-review` checks the diff against the plan's risk block (risks without mitigations = finding). `/bq-verify` runs the named tests; Guard Pass hunts hardcoded-success/catch-alls that *mask* these failures. Confidence may not exceed 89% while any concurrency/consistency risk lacks a passing test.
