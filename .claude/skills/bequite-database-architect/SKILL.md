---
name: bequite-database-architect
description: Use when a task adds or changes tables, columns, indexes, constraints, migrations, queries, transactions, connection pooling or backups, or when a query is slow, data is wrong, or a deploy needs a schema change. Gives zero-downtime migration steps, index and N+1 checks with measured before and after, and isolation and retry rules.
last_verified: 2026-11-21
sources:
  - https://www.postgresql.org/docs/current/ (read 2026-11-21) current major is 19
  - https://www.postgresql.org/docs/current/functions-uuid.html (read 2026-11-21) uuidv7() since 18
  - https://www.postgresql.org/docs/current/sql-createindex.html (read 2026-11-21) CONCURRENTLY rules and caveats
  - https://www.postgresql.org/docs/current/sql-altertable.html (read 2026-11-21) NOT VALID then VALIDATE, lock level
  - https://www.postgresql.org/docs/current/transaction-iso.html (read 2026-11-21) isolation levels, SQLSTATE 40001 retry
  - https://github.com/ankane/strong_migrations (read 2026-11-21) unsafe operations and safe alternatives, timeouts
allowed-tools: Read, Glob, Grep, Bash
---

# bequite-database-architect

A bad schema costs years, a missing index costs uptime, and a locking migration costs a Friday night. This skill keeps changes forward-only, measured and reversible by design. Examples use PostgreSQL because most projects use it. The rules carry over to other engines; check that engine's own docs for each lock.

## When to use

- `/bq-plan`: the data model, index list, migration strategy, pooling and backup lines of the plan.
- `/bq-feature`: any migration, new query path or ORM model change.
- `/bq-fix`: slow queries, deadlocks, serialization errors, wrong or duplicated data.

Not for: API shape (`bequite-backend-architect`), DB hosting and credentials (`bequite-devops-cloud`), running migrations on shared or production databases (hard human gate: the agent prepares, the user runs).

## Procedure

1. **Read what exists.** Schema files or migrations, the ORM models, row counts of the touched tables (`SELECT relname, n_live_tup FROM pg_stat_user_tables`), and the engine's major version. Pick the engine with the ten questions when there is none yet; SQLite is a valid candidate for single-server and local-first apps.
2. **Model.** Explicit types, `NOT NULL` unless absence means something, `timestamptz` for times, database constraints (`CHECK`, `UNIQUE`, foreign keys with a chosen `ON DELETE`). Primary keys: identity integers internally; `uuidv7()` (PostgreSQL 18+) when IDs are public or generated off the DB, since time-ordered keys index better than random v4.
3. **Index from the queries, not the columns.** For each new query: the `WHERE` and `ORDER BY` columns become one composite index in that order; index every foreign key used in joins or deletes (PostgreSQL does not create them). Measure with `EXPLAIN (ANALYZE, BUFFERS)` before and after on realistic row counts. Paste both plans.
4. **Write the migration forward-only and lock-aware** (`references/safe-migrations.md`). Set `lock_timeout` (for example 10 s) so a blocked DDL fails fast instead of queuing every query behind it. Large-table changes use the expand and contract sequence; indexes use `CONCURRENTLY` outside a transaction; new constraints go in `NOT VALID`, then `VALIDATE` in a second migration.
5. **Deploy order.** Code that tolerates both schemas ships before the schema change; the old column is dropped only after no deployed code reads it. Write the order into the plan.
6. **Queries in code.** No query inside a loop over results (N+1): count queries per request in a test. Transactions are short; never hold one across a network call.
7. **Isolation.** Read Committed by default. Use Serializable (or row locks with `SELECT ... FOR UPDATE`) for money, stock and counters; retry the whole transaction on SQLSTATE `40001` with backoff.
8. **Pooling.** Serverless and many workers need a pooler. Transaction-mode pooling breaks session features (session `SET`, advisory locks held across statements, `LISTEN`); set timeouts on the role, not the session.
9. **Backups.** Know the host's point-in-time recovery window from its current docs and practise one restore into a scratch database. Record the time it took.
10. **Evidence.** Migration up on a fresh DB, the app's tests against a real database (container or local), plans before and after, query count per request.

## Worked example (real run, 2026-11-21)

Task: "the bookings page is slow for customers with history". Measured with `db_demo.py` (SQLite 3.50.4, 100,000 bookings, 5,000 customers), query `SELECT id, starts_at FROM bookings WHERE customer_id = ? ORDER BY starts_at DESC LIMIT 20`, 500 runs:

```
no index                  1.541 ms/query   plan: SCAN bookings | USE TEMP B-TREE FOR ORDER BY
(customer_id, starts_at)  0.007 ms/query   plan: SEARCH bookings USING COVERING INDEX bookings_customer_starts (customer_id=?)
N+1 loop queries: 51      (50 bookings, then one customer lookup each)
join queries:     1
```

Decision: one composite index in filter-then-sort order (a 220x drop here; the ratio on a real server will differ, so measure there too), and the list endpoint switched to the join. In PostgreSQL the migration is:

```sql
SET lock_timeout = '10s';
CREATE INDEX CONCURRENTLY IF NOT EXISTS bookings_customer_starts ON bookings (customer_id, starts_at DESC);
-- not inside a transaction block; if it fails, DROP INDEX CONCURRENTLY the INVALID index and retry
```

## Quality gate

- Every new query has a plan pasted before and after (or a reason it needs no index).
- Every migration names its lock level and has `lock_timeout`; no table rewrite on a large table without the expand and contract steps.
- No destructive statement (`DROP`, `TRUNCATE`, `DELETE` without `WHERE`, type change) in the same release as the code that stopped using it.
- A test runs against a real database engine, not a mock of the ORM.
- Shared or production migrations were printed for the user, not run.

## Boundaries

- Destructive changes and production migrations are hard human gates. Prepare, test on a copy, print the commands.
- ORMs, migration tools, poolers and hosts are candidates; compare with the ten questions and check each in its registry this session.
- Lock behaviour differs by engine and version: cite the current docs page for the claim, or mark it `UNVERIFIED:`.

## References (load on demand)

- `references/safe-migrations.md`: operation-by-operation safe sequences, lock levels, timeouts, deploy order.
- `references/query-checks.md`: SQL to find missing and unused indexes, slow statements, N+1 detection, isolation retry loop.
