---
name: bequite-database-architect
description: Database design procedures — schema design, indexing strategy, forward-only migrations, ORM patterns, transaction isolation, N+1 detection, connection pooling, soft vs hard deletes, read replicas, sharding triggers, backup + recovery. Loaded by /bq-plan, /bq-feature, /bq-fix for DB work.
allowed-tools: Read, Glob, Grep, Bash
---

# bequite-database-architect — data discipline

## Why this skill exists

A bad schema costs years. A missing index costs uptime. A destructive migration costs trust. This skill encodes the patterns that keep your data sane through v1 → v10.

Default to Postgres for v1. Reasons:
- Best ORM support (Drizzle, Prisma, Kysely, sqlx)
- JSONB for flexible fields
- Strong typing
- Excellent extension ecosystem (pg_cron, pg_vector, etc.)
- Managed options that scale: Supabase, Neon, RDS, Postgres on Fly

SQLite is fine for: solo CLI tools, desktop apps, single-server projects < 1K users.
MySQL: only if mandated.
MongoDB / DynamoDB / Firestore: avoid for v1 unless schemaless is a hard requirement.

---

## Schema design principles

### 1. UUIDs as primary keys

```sql
id uuid PRIMARY KEY DEFAULT gen_random_uuid()
```

Why:
- Don't leak row counts in URLs
- Generate client-side without round-trip
- Easier to merge data across databases

Sequential IDs are fine for internal foreign keys (smaller, faster joins) but never expose them in URLs.

### 2. Created/updated timestamps everywhere

```sql
created_at timestamptz NOT NULL DEFAULT now()
updated_at timestamptz NOT NULL DEFAULT now()
```

Always `timestamptz`, never `timestamp without time zone`. The former stores UTC and converts on read; the latter creates time-zone bugs forever.

### 3. Soft deletes for user-facing data

```sql
deleted_at timestamptz
```

Then:
```sql
CREATE VIEW active_bookings AS
SELECT * FROM bookings WHERE deleted_at IS NULL;
```

Why: GDPR + audit + accidental deletion recovery.

Exceptions: ephemeral data (session tokens, cache entries) — hard delete.

### 4. Foreign keys + ON DELETE strategy

Every relation has explicit ON DELETE:
- `CASCADE` — only when child rows are meaningless without parent (e.g. user_settings on user delete)
- `SET NULL` — when child rows can survive (e.g. booking on agent delete)
- `RESTRICT` — when you want to force explicit deletion (e.g. invoice on customer)
- `NO ACTION` (default) — sometimes correct, but ambiguous; prefer explicit

### 5. NOT NULL by default

Make every column `NOT NULL` unless absence is a meaningful business state. Cleaner queries, fewer bugs.

### 6. Constraints + checks

Use database-level constraints:
```sql
CHECK (price >= 0)
CHECK (email ~* '^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$')
UNIQUE (org_id, slug)
```

App-level validation is UX; DB-level constraints are the truth.

### 7. JSON / JSONB for flexible fields

Use JSONB for:
- User preferences
- Feature flags
- Webhook payloads (audit log)
- Tags / labels with arbitrary structure

Don't use JSONB for:
- Things you'll query / filter on (use proper columns)
- Things with strict schemas (use proper columns)
- Foreign-key relationships (you'll regret it)

---

## Indexing strategy

### What to index

- Every foreign key (Postgres doesn't auto-index FKs)
- Every column in WHERE clauses of high-traffic queries
- Every column in ORDER BY of paginated lists
- Composite indexes for (frequently-filtered, then-ordered) pairs

### What NOT to index

- Columns that get written more than read (each write maintains the index)
- Low-cardinality columns alone (e.g. `status` with 3 values — composite with another col)
- Large text columns (use full-text search index separately)

### Detect missing indexes

Postgres:
```sql
SELECT
  schemaname,
  tablename,
  seq_scan,
  seq_tup_read,
  idx_scan,
  seq_tup_read / NULLIF(seq_scan, 0) AS avg_seq_read
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan AND seq_tup_read > 10000
ORDER BY seq_tup_read DESC;
```

High seq_scan with high avg_seq_read = missing index.

### Detect unused indexes

```sql
SELECT
  schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexname NOT LIKE '%pkey'
ORDER BY pg_relation_size(indexrelid) DESC;
```

Drop unused indexes (they cost write performance + disk).

---

## Forward-only migrations

**Never write a destructive migration.** Iron Law.

Rules:
1. Adding a column: `NULL` default; backfill in a separate migration; THEN `NOT NULL` once all rows have values
2. Removing a column: leave it for one release cycle; remove only after code stops writing to it
3. Renaming a column: add the new column, dual-write, copy data, switch reads, drop old (4-step process)
4. Changing a type: same pattern as rename
5. Adding an index: use `CREATE INDEX CONCURRENTLY` in Postgres (doesn't lock the table)

Tooling for 2026:
- **Drizzle Kit** — TypeScript-native, good for solo / small teams
- **Atlas** — declarative + strong online migration support
- **Liquibase / Flyway** — Java ecosystems
- **Supabase migrations** — wraps psql; good for Supabase users
- **Prisma Migrate** — fine, but slower iteration than Drizzle

NEVER:
- `DROP COLUMN` in the same migration as code that stopped reading it (deploy-skew bugs)
- `ALTER COLUMN ... TYPE ...` without a safety plan
- `DELETE FROM <table>` in a migration

---

## Transaction isolation

Postgres default: `READ COMMITTED` (good for most cases).

Use stricter when:
- **Repeatable read** — for reports that need consistent snapshots
- **Serializable** — for financial logic, race-prone counters, double-spend prevention

Pattern:
```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- logic
COMMIT;
```

Be ready to retry on serialization failures (rare in low-traffic apps, common at scale).

---

## ORM patterns

### Drizzle (recommended for TS in 2026)

```ts
import { pgTable, uuid, text, timestamp } from "drizzle-orm/pg-core";

export const bookings = pgTable("bookings", {
  id: uuid("id").primaryKey().defaultRandom(),
  customerId: uuid("customer_id").notNull().references(() => customers.id, { onDelete: "cascade" }),
  startsAt: timestamp("starts_at", { withTimezone: true }).notNull(),
  notes: text("notes"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  deletedAt: timestamp("deleted_at", { withTimezone: true }),
});
```

Why Drizzle over Prisma in 2026:
- Faster iteration (no codegen step on every change)
- Better query performance (no abstraction tax)
- Better edge-runtime compatibility
- TypeScript-first (Prisma is JS-first with TS types added)

Prisma is fine if you're already on it; don't migrate without reason.

### N+1 detection

The killer pattern:
```ts
const bookings = await db.select().from(bookingsTable);
for (const b of bookings) {
  const customer = await db.select().from(customersTable).where(eq(customersTable.id, b.customerId));
  // 100 bookings = 101 queries
}
```

Fix:
```ts
const result = await db
  .select()
  .from(bookingsTable)
  .leftJoin(customersTable, eq(bookingsTable.customerId, customersTable.id));
// 1 query
```

Detect in CI:
- Drizzle: log query count per request; alert if > 10 for non-list endpoints
- Prisma: built-in query logging
- Manual: add a per-request query counter via OpenTelemetry

---

## Connection pooling

Serverless + DB = connection-exhaustion bug waiting to happen.

For Postgres in 2026:
- **Supabase**: use Supavisor (transaction mode) — built in
- **Neon**: serverless-native, automatic pooling
- **RDS / Postgres elsewhere**: PgBouncer in transaction mode
- **Vercel Functions + Postgres**: must use a pooler; direct connections will exhaust limits

Transaction-mode pooling has limitations:
- No `LISTEN/NOTIFY` (use a different pool for those)
- No `PREPARE` statements (workaround: query strings each time)
- No session-level settings (set per query)

---

## Backup + recovery

Per managed DB:
- **Supabase Pro**: 14 days point-in-time recovery
- **Neon**: 7 days PITR on free tier, 30+ on paid
- **RDS**: 35 days PITR
- **Self-hosted**: pg_dump nightly + WAL archiving for PITR

Test the restore once before you need it. Bookmark the runbook.

---

## When activated by /bq-plan

Write the data section:
- Schema diagram (entities + relationships)
- Index list (every FK + every high-traffic WHERE/ORDER BY column)
- Migration strategy (forward-only commitment)
- Pooler choice (per host)
- Backup tier
- Soft-delete policy per table

---

## When activated by /bq-feature

For features touching DB:
- Add migration (forward-only)
- Add indexes for new query patterns
- Verify no N+1 in the new code path
- Write a test that hits the actual DB (or test-container DB), not a mock

---

## When activated by /bq-fix

DB bug types (per the 15-type router):
- **Database bug (query/data)** → EXPLAIN ANALYZE the query; check for missing index, bad join, type mismatch
- **Performance regression** with DB cause → check `pg_stat_statements` for slow queries
- **Data corruption** → check constraint coverage; consider this the worst-case fix and pair with backups

---

## What this skill does NOT do

- Pick the DB host (use `bequite-devops-cloud`)
- Design the API around the DB (use `bequite-backend-architect`)
- Run query optimization beyond EXPLAIN ANALYZE (use a DBA for serious tuning)
- Sharding strategy (out of scope until 50K+ users)

---

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, design system, or workflow named in this file (Postgres, MySQL, SQLite, MongoDB, DynamoDB, Firestore, Drizzle, Prisma, Kysely, sqlx, Supabase, Neon, RDS, PgBouncer, Supavisor, Atlas, Liquibase, Flyway, etc.) is an EXAMPLE, not a mandatory default.**

The patterns (UUIDs, timestamps, soft deletes, forward-only migrations, indexing strategy, transaction isolation) are **universal database discipline**. Specific DB engine + ORM + migration tool picks are candidates per project.

**Do not say:** "Use Postgres."
**Say:** "Postgres is one candidate. Compare against SQLite (for solo / single-server projects), MongoDB (only when data is truly document-shaped), or managed alternatives based on this project's data shape, scale, query patterns, and team expertise. Use it only if it fits."

The 10 decision questions:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

Write a decision section before adopting (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan).

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.
