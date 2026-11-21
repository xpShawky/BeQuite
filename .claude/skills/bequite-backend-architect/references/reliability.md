# Reliability: timeouts, retries, jobs, caching, rate limits (verified 2026-11-21)

Sources: AWS Builders' Library "Timeouts, retries and backoff with jitter" (Marc Brooker); Google SRE book "Addressing cascading failures"; RFC 6585 (429).

## Timeouts and deadlines

- Every outbound call (HTTP, DB, cache, queue) has a timeout. No default "wait forever".
- Pick the timeout from the dependency's measured latency: accept a false-timeout rate (for example 0.1%) and use the matching percentile (p99.9).
- Propagate the deadline: set it at the edge and pass the remaining time down. With a 30 s budget and 7 s spent, the next call gets 23 s minus transit.
- A caller's timeout must be longer than the sum of what it waits on, or work continues after nobody is listening.

## Retries

- Retry only idempotent operations (RFC 9110) or writes protected by an idempotency key.
- One layer retries. Retries multiply across layers: 4 attempts at each of 3 layers is 64 calls at the bottom.
- Capped exponential backoff with full jitter: `sleep = random(0, min(cap, base * 2**attempt))`.
- Retry budget per process (example from the SRE book: 60 retries per minute) so an outage does not become a retry storm.
- Do not retry 4xx except 408, 425, 429 (honour `Retry-After`).

## Background jobs

| Need | Rule |
|---|---|
| Duplicate delivery | Jobs are idempotent (a second run changes nothing), keyed by a job ID |
| Stuck jobs | Max duration and memory; a watchdog marks timeouts as failed |
| Failures | Backoff retries, then a dead-letter queue; alert when it holds more than a set number |
| Ordering | Do not assume it unless the queue guarantees it; carry a version or timestamp |
| Visibility | Each job logs start, end, attempts and its request or trace ID |

Candidates range from a DB table polled by a worker, to a Redis-backed queue, to a managed or durable-workflow service. Pick with the ten questions (volume, durability, existing stack, ops skill).

## Caching

| Strategy | Use for | Test |
|---|---|---|
| TTL only | Data where staleness is acceptable (stats, recommendations) | Value changes after TTL |
| Write-through or delete-on-write | User-owned data | A write is visible on the next read |
| Tag-based | Many keys depending on one entity | Invalidating the tag clears every dependent key |

Never cache responses that vary by user under a shared key. Cache stampede: one request recomputes, others wait or serve stale.

## Rate limits

- Every public route; stricter on auth, search and anything that costs money (LLM calls).
- Limit per account and per IP; 429 with `Retry-After`; a 429 response is not cacheable (RFC 6585).
- The IETF `RateLimit-Policy` / `RateLimit` fields (draft -12, 2026-11-20) are a candidate for telling clients their quota.
- LLM features also get a cost ceiling per user per day.

## Event-loop and thread traps

- Synchronous file, crypto or process calls in a request path block every other request on that worker (Node `*Sync` APIs, CPU-heavy work on the main thread). Move them to async APIs, a worker or a job.
- Floating promises: lint with `no-floating-promises` as an error.
- Set a project threshold for main-thread blocking per request (a working rule, not a published standard; 100 ms is a common starting point) and measure with a profiler before changing code.
