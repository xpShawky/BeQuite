---
name: bequite-backend-architect
description: Use when designing, building or fixing server code, such as an API route, error responses, input validation, retries and timeouts, background jobs, caching, rate limits, idempotent writes, webhooks or tracing. Gives standards-based defaults (RFC 9457 errors, Idempotency-Key, deadlines, jittered backoff) and a check per pattern. Pairs with database-architect for data.
last_verified: 2026-11-21
sources:
  - https://www.rfc-editor.org/rfc/rfc9457 (read 2026-11-21) problem details error shape
  - https://www.rfc-editor.org/rfc/rfc9110#section-9.2.2 (read 2026-11-21) safe and idempotent methods
  - https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ (read 2026-11-21) draft-09 key rules, 400/409/422
  - https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/ (read 2026-11-21) draft-12 RateLimit fields
  - https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter (read 2026-11-21) retries, jitter, timeouts
  - https://sre.google/sre-book/addressing-cascading-failures/ (read 2026-11-21) retry budgets, deadline propagation
  - https://opentelemetry.io/docs/specs/semconv/http/http-spans/ (read 2026-11-21) stable HTTP span attributes
  - https://docs.stripe.com/api/idempotent_requests (read 2026-11-21) a production key policy
allowed-tools: Read, Glob, Grep, Bash
---

# bequite-backend-architect

The backend bugs that cost a week are usually plain: a write that ran twice on retry, a retry storm, a timeout longer than the caller's, an error body that leaks a stack trace. This skill gives one default per pattern, taken from the standard, plus the test that proves it.

## When to use

- `/bq-plan`: the API, jobs, caching and observability parts of the plan.
- `/bq-feature`: any new route, handler, job, webhook receiver or outbound call.
- `/bq-fix`: backend, race, timeout or performance bugs (with `bequite-problem-solver`).

Not for: schema, indexes and migrations (`bequite-database-architect`), auth and threat review (`bequite-security-reviewer`), hosting and CI (`bequite-devops-cloud`), UI.

## Procedure

1. **Inventory.** List each endpoint or job the work touches: method, caller, side effects, external calls, expected rate. Read the existing handlers first; match the project's style before adding a new one.
2. **Pick the API style** with the ten questions (`references/api-patterns.md`): plain HTTP+JSON is the default; RPC when one typed client owns both sides; GraphQL only when many clients need different shapes. Write one line on why.
3. **Errors.** One shape for every error: RFC 9457 problem details (`application/problem+json`, `type`, `title`, `status`, `detail`, `instance`, plus a `request_id` extension). Never a 200 with `ok: false`; never a stack trace to the client.
4. **Validate** every body, query, path and header the handler reads, on the server, against a schema. Bound numbers and lengths.
5. **Idempotent writes.** RFC 9110 makes POST and PATCH non-idempotent. Any POST or PATCH that a client, proxy or queue may retry (payments, orders, emails, webhook receivers) takes an `Idempotency-Key`: 400 when missing, 422 when reused with a different payload, 409 while the first request is still running, the stored response on a true retry. Publish the expiry (24 h is a common policy).
6. **Timeouts and retries** (`references/reliability.md`): a timeout on every outbound call, chosen from the dependency's latency percentile; pass the remaining deadline downstream; retry only idempotent calls, at one layer, with capped exponential backoff and full jitter, inside a retry budget.
7. **Slow work goes to a job**: email, third-party webhooks, reports. Jobs are idempotent, have a max duration, retry with backoff, and land in a dead-letter queue after N failures with an alert. Compare queue options with the ten questions; a DB table plus a worker is a valid first candidate.
8. **Rate limits** on every public route; 429 with `Retry-After`. The IETF `RateLimit` fields are still a draft (-12): a candidate, not a requirement.
9. **Cache** only with a written invalidation rule (TTL, write-through, or tag) and a test that a write is visible after invalidation.
10. **Observe.** Structured logs with `request_id`; HTTP server spans named `{method} {route}` with the stable attributes `http.request.method`, `url.path`, `http.route`, `http.response.status_code`; p50/p95/p99 latency and error rate per route. No secrets or full tokens in logs.
11. **Prove it.** For each pattern touched, one test: duplicate request with the same key, timeout path, retry exhaustion, 429, a problem-details body. Paste command, exit code and output.

## Worked example (real run, 2026-11-21)

Task: `POST /orders` must not charge twice when the mobile client retries. An in-process implementation of step 5 (`idem_demo.py`, key `5f2b8c1e-...`, payload `{"amount": 4900}`) printed:

```
1 first           (201, {'order_id': 'ord_d50909c403fc', 'amount': 4900})
2 same retry      (201, {'order_id': 'ord_d50909c403fc', 'amount': 4900})   same id, no second charge
3 diff payload    422
4 missing key     400
5 concurrent dup  409    (original still processing, 0.3 s)
6 original done   201
exit=0
```

Design notes that came out of the run: the key record is written as `processing` under a lock before the side effect, so a duplicate arriving mid-flight gets 409 instead of a second charge; the payload fingerprint is a SHA-256 of the sorted JSON body; keys expire after 24 h. In a real service the record lives in the database with a unique index on the key, not in memory.

## Quality gate

- Every touched endpoint has: a validated input schema, the problem-details error shape, a stated timeout for each outbound call, and a test.
- Every retried write has an idempotency test showing the duplicate returns the stored response.
- No retry loop without a cap, jitter and an idempotency reason.
- Each tool or service picked has a decision note (ten questions); none was installed without the user's yes.
- Evidence holds commands, exit codes and output. No "should work".

## Boundaries

- Does not choose the database or write migrations; hand off to `bequite-database-architect`.
- Production config, paid services and secrets are hard human gates.
- Libraries and services named in references (validation libraries, queue services, rate limiters, tracing vendors) are candidates; verify each in its registry this session before naming a version.

## References (load on demand)

- `references/api-patterns.md`: API style choice, problem-details example, validation, pagination, webhooks, versioning.
- `references/reliability.md`: timeouts, deadlines, retries, budgets, jobs, caching, rate limits, sync I/O traps.
