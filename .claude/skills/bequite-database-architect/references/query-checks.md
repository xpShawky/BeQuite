# Query checks (PostgreSQL examples, verified 2026-11-21)

## Measure one query

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;   -- runs the query; use a copy for writes
```

Read: `Seq Scan` on a large table with a selective filter, `Sort` with `external merge`, estimated rows far from actual rows (stale statistics: `ANALYZE table`).

## Tables read mostly by sequential scans

```sql
SELECT relname, seq_scan, seq_tup_read, idx_scan,
       seq_tup_read / NULLIF(seq_scan, 0) AS avg_rows_per_scan
FROM pg_stat_user_tables
WHERE seq_scan > coalesce(idx_scan, 0) AND seq_tup_read > 10000
ORDER BY seq_tup_read DESC;
```

## Indexes never used (candidates to drop after checking replicas and rare jobs)

```sql
SELECT schemaname, relname, indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexrelname NOT LIKE '%pkey'
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Invalid indexes left by a failed concurrent build

```sql
SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;
```

## Slowest statements (needs the `pg_stat_statements` extension)

```sql
SELECT calls, round(mean_exec_time::numeric, 2) AS mean_ms, round(total_exec_time::numeric) AS total_ms, query
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;
```

## N+1 detection in tests

Count queries per request and fail above a limit. Python example with a driver hook; most ORMs have an equivalent event or logger:

```python
count = 0
def on_query(*_): 
    global count; count += 1
# attach on_query to the driver or ORM "before execute" event, call the endpoint, then:
assert count <= 3, f"{count} queries for one list request (N+1?)"
```

Fix: a join, an `IN (...)` batch load, or the ORM's eager-load option.

## Serializable retry loop

```python
for attempt in range(5):
    try:
        with conn.transaction(isolation="serializable"):
            debit(conn, account, amount)
        break
    except SerializationFailure:          # SQLSTATE 40001
        time.sleep(random.uniform(0, 0.05 * 2 ** attempt))
else:
    raise RuntimeError("gave up after 5 serialization failures")
```

The whole transaction is retried, never a single statement inside it.
