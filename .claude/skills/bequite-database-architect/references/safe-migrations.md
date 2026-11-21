# Safe migrations (PostgreSQL examples, verified 2026-11-21)

Sources: PostgreSQL 19 docs (`CREATE INDEX`, `ALTER TABLE`), strong_migrations README. Other engines: check their own lock docs before copying a step.

## Session settings for every migration

```sql
SET lock_timeout = '10s';        -- a blocked DDL fails fast instead of queuing all traffic behind it
SET statement_timeout = '1h';    -- long enough for a backfill batch, not unbounded
```

Under transaction-mode pooling set these on the migration role (`ALTER ROLE migrator SET lock_timeout = '10s'`), since session settings do not stick.

## Operation table

| Operation | Unsafe form | Safe sequence |
|---|---|---|
| Add index | `CREATE INDEX` (blocks writes for the build) | `CREATE INDEX CONCURRENTLY`, outside a transaction block. On failure the index is INVALID: drop it (`DROP INDEX CONCURRENTLY`) or `REINDEX INDEX CONCURRENTLY`. Not supported on partitioned tables (build per partition). |
| Add column | Volatile default (`DEFAULT now()` style functions, `random()`) rewrites the table | Add nullable or with a non-volatile default (no rewrite), backfill in batches, then add the constraint. |
| Make a column NOT NULL | `SET NOT NULL` scans under an exclusive lock | Add `CHECK (col IS NOT NULL) NOT VALID`; `VALIDATE CONSTRAINT` in a second migration (SHARE UPDATE EXCLUSIVE, reads and writes continue); then `SET NOT NULL` (uses the validated check) and drop the check. Current docs also allow a not-null constraint `NOT VALID` directly. |
| Add foreign key or CHECK | Validates the whole table under lock | `ADD CONSTRAINT ... NOT VALID`, then `VALIDATE CONSTRAINT` separately. |
| Add UNIQUE | `ADD CONSTRAINT UNIQUE` builds the index under lock | `CREATE UNIQUE INDEX CONCURRENTLY`, then `ADD CONSTRAINT ... UNIQUE USING INDEX`. |
| Change type | `ALTER COLUMN TYPE` rewrites the table (except some widening changes) | Expand and contract: new column, dual-write, backfill, move reads, stop writes, drop old. |
| Rename column or table | Breaks every deployed reader at once | Expand and contract, or a view for the transition. |
| Remove column | Code still selecting it breaks after deploy | Stop reading and writing it in code, deploy, then drop. ORMs with a column cache need the column marked ignored first. |
| Backfill | One `UPDATE` over millions of rows | Batches (for example 10,000 rows) by primary key range, each its own transaction, with a pause; resumable. |

## Deploy order (expand and contract)

1. Migration: add the new structure (nothing reads it yet).
2. Deploy code that writes both old and new.
3. Backfill.
4. Deploy code that reads new.
5. Deploy code that stops writing old.
6. Migration: drop old (one release later, after the rollback window).

Each step is a separate deploy, so any one can be rolled back without data loss.

## Before running anywhere shared

- Run up on a fresh database and on a copy with production-like row counts; time it.
- Print the plan for the user: statements, expected lock, expected duration, rollback (usually "roll forward" for data steps).
- The user runs it against shared or production databases.
