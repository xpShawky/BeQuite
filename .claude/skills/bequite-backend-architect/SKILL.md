---
name: bequite-backend-architect
description: Backend design procedures — API patterns (REST/RPC/GraphQL pick), error handling, input validation, async + queues + background jobs, caching layers, rate limiting, idempotency, observability. Pairs with bequite-database-architect for data. Loaded by /bq-plan, /bq-feature, /bq-fix for backend work.
allowed-tools: Read, Glob, Grep, Bash
---

# bequite-backend-architect — server-side discipline

## Why this skill exists

The backend bugs that take a week to debug are usually the simple ones — missing await, wrong env var, sync I/O in a hot path, no rate limit on a public endpoint. This skill encodes the patterns that prevent them.

Pairs with:
- `bequite-database-architect` for schema + queries
- `bequite-security-reviewer` for auth + input validation
- `bequite-devops-cloud` for deployment + monitoring

---

## API style: which to pick

Three reasonable defaults for 2026:

### REST + Zod schemas (default for most v1s)

Use when:
- Solo founders / small teams
- Public API consumers expected
- Simple CRUD dominates
- Tooling matters (curl, Postman, browser devtools)

Pattern:
```ts
// app/api/bookings/route.ts
import { z } from "zod";

const Body = z.object({
  customerId: z.string().uuid(),
  startsAt: z.string().datetime(),
  notes: z.string().max(500).optional(),
});

export async function POST(req: Request) {
  const parsed = Body.safeParse(await req.json());
  if (!parsed.success) {
    return Response.json({ error: parsed.error.flatten() }, { status: 400 });
  }
  // ... handler
}
```

### tRPC / RPC (default for typescript-only stacks)

Use when:
- 100% TypeScript end-to-end
- No public API consumers
- Type safety is the dominant value

### GraphQL (default only for complex frontends)

Use when:
- Many client variants (web + mobile + admin) need different shapes
- Federation is a real need (microservices)

Almost never for v1. Adds complexity, doesn't pay off until ~5K users.

---

## Error-handling layers

Three layers, three error types:

1. **Validation errors** (400): bad input. Return structured field errors. Zod's `flatten()` is perfect.
2. **Auth errors** (401 / 403): no token / wrong permissions. NEVER leak why (e.g. "user not found" vs "wrong password" — both → "invalid credentials").
3. **Server errors** (5xx): your bug. Log full context server-side; return `{ error: "internal_server_error", requestId }` to client. The requestId is what the user gives support.

NEVER:
- Return stack traces to clients
- Use HTTP 200 with `{ ok: false }` patterns (proxies + CDNs assume 200 = success)
- Throw without logging

---

## Input validation discipline

Every public API endpoint validates:
- Body: Zod / Pydantic / Valibot schema
- Query params: same
- Path params: type-coerced + bounded (no `parseInt(id)` without bounds check)
- Headers: only the ones you read; ignore the rest
- File uploads: size limit, MIME-type allowlist, content-type-vs-extension check

Server-side ONLY. Client-side validation is UX, not security.

---

## Async patterns

### Missing await — the #1 bug

```ts
// ✗ silently never runs in time
const result = somethingAsync();

// ✓
const result = await somethingAsync();
```

Lint with ESLint `@typescript-eslint/no-floating-promises` (treat as error, not warning).

### Background jobs

For work that's slow or shouldn't block the response:

- Email sending
- Webhooks to third parties
- Report generation
- Cache warming

Options for 2026:
- **Inline + log if fails** — only if duration < 1s and failure is OK (e.g. analytics ping)
- **Vercel Cron + DB queue table** — simple, no extra infra; fine for low-volume
- **Inngest** — managed serverless jobs, generous free tier; recommended for v1
- **Trigger.dev** — open-source alternative to Inngest
- **BullMQ + Redis** — if you already have Redis; otherwise overkill for v1
- **Temporal** — durable workflows; overkill until you need it

Never fire-and-forget without retry + dead-letter queue. Lost jobs = lost trust.

---

## Caching

Three layers, three TTLs:

1. **In-memory** (per process / per Lambda) — milliseconds; for hot computations
2. **Redis / Upstash / KV** — seconds to hours; for shared cache across instances
3. **CDN / browser** — hours to days; for public assets and immutable responses

Cache invalidation is the hard part. Patterns:
- **TTL only** — simple, accepts stale data; use for analytics, recommendations
- **Write-through** — invalidate on every write; use for user-data caches
- **Tag-based** — invalidate by tag (e.g. all "user:123" caches); use for complex deps
- **Event-driven** — pub/sub invalidation; use for multi-region

Default: TTL + write-through for v1. Add tag-based when complexity grows.

For Next.js 16: Cache Components with `cacheLife`, `cacheTag`, `updateTag` — see vercel:next-cache-components skill.

---

## Rate limiting

Every public endpoint has rate limits:
- Auth endpoints: 5 attempts per 15 min per IP + per account
- API endpoints: 100 req/min per token
- Public reads: 1000 req/min per IP (or higher; depends on cost)

Implementation:
- **Upstash Ratelimit** — managed Redis, generous free tier (recommended)
- **Vercel Firewall rate-limit rules** — at edge, before code runs
- **next-rate-limit middleware** — DIY in middleware

Never run without any rate limiting. The first DDoS is free; the second one costs you a customer.

---

## Idempotency

For any non-GET endpoint that could be retried (network failure, browser refresh, etc.):
- Accept an `Idempotency-Key` header
- Store the key + response for 24h
- On repeat with same key + same body → return the stored response

Critical for:
- Payments (Stripe, Lemonsqueezy require this)
- Order creation
- Email sending
- Webhook receivers (the third party WILL retry)

---

## Observability (the 3 pillars)

1. **Logs** — structured JSON, with `requestId` per request, `userId` when known, never log secrets
2. **Metrics** — request count, p50/p95/p99 latency, error rate per endpoint
3. **Traces** — for distributed flows (auth → DB → external API → response)

Recommended 2026 stack:
- **Sentry** — errors (it's standard for a reason)
- **Vercel Analytics** — page-level metrics
- **Axiom or Datadog** — structured logs
- **OpenTelemetry** — traces (vendor-neutral)

Sentry's bug: don't capture PII in `extra` data. Configure `beforeSend` to scrub.

---

## Sync vs async I/O

The killer pattern:
```ts
// ✗ blocks the event loop on Node single-thread
const file = fs.readFileSync("./data.json");

// ✓ non-blocking
const file = await fs.promises.readFile("./data.json");
```

Same for:
- `crypto.pbkdf2Sync` — use async version + worker thread
- `child_process.execSync` — use `exec` with promise wrapper
- Image processing on the main thread — offload to worker / queue

If a single request can block the event loop > 100ms, it kills concurrency.

---

## Server-side vs edge

Pick per-route:
- **Edge (Cloudflare Workers, Vercel Edge)** — for routes that need < 50ms global latency. Stateless. No long-running.
- **Serverless (Vercel Functions, AWS Lambda)** — for most routes. Up to 300s on Vercel Pro.
- **Long-running (Vercel Fluid Compute, dedicated server)** — for AI streaming, file uploads, anything > 300s.

Never pick edge for routes that:
- Need Node.js APIs (`fs`, `child_process`)
- Use heavy libraries (Drizzle ORM full driver, etc.)
- Need long-lived DB connections (use pooled connections via Supavisor / PgBouncer)

---

## Background-task safety

For jobs that mutate state:
- Use database transactions
- Make idempotent (a job that runs twice produces the same result)
- Set max execution time + memory limit
- Send to dead-letter queue on > 3 failures
- Alert on dead-letter queue > 10 items

---

## When activated by /bq-fix

Backend bug types (per the 15-type router):
- **Backend bug (API/logic)** → check the handler's error paths, validation, DB calls
- **Auth bug** → check token validation, cookie / session handling, CORS
- **Performance regression** → profile (clinic.js, Node --prof, or APM); look for sync I/O, N+1, missing index
- **Race condition** → check await order, parallel state updates, missing locks
- **Memory leak** → check for closures holding refs, unbounded arrays, missing cleanup in long-running processes

---

## When activated by /bq-plan

Write the §11 (security) and §12 (devops) sections in detail. Include:
- Auth flow diagram (sign-up, sign-in, password reset, MFA if needed)
- Rate limits per endpoint family
- Background-job catalog (what jobs run when)
- Cache layers + invalidation strategy
- Error-response shape

---

## What this skill does NOT do

- Pick the database (use `bequite-database-architect`)
- Set up CI/CD (use `bequite-devops-cloud`)
- Do penetration testing (use `bequite-security-reviewer` + a real pentester)
- Design the UI (use `bequite-ux-ui-designer`)

---

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, design system, or workflow named in this file (Zod, tRPC, GraphQL, Inngest, Trigger.dev, BullMQ, Temporal, Upstash, Redis, Sentry, Vercel, AWS Lambda, Cloudflare Workers, OpenTelemetry, Better-Auth, Clerk, etc.) is an EXAMPLE, not a mandatory default.**

The patterns (validate inputs server-side, async correctness, idempotency, rate limits, observability layers) are **universal**. Specific tool picks are candidates per project.

**Do not say:** "Use Inngest."
**Say:** "Inngest is one candidate for background jobs. Compare against Trigger.dev, BullMQ + Redis, Temporal, or a simple DB-queue table for this project's job volume, durability needs, and team expertise. Use it only if it fits."

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

---

## When NOT to use this skill (alpha.15)

- The task at hand doesn't touch this skill's domain — defer to the right specialist skill
- A faster / simpler skill covers the same need — pick the simpler one and document why
- The skill's core invariants don't apply to the current project (e.g. regulated-mode rules on a prototype)
- The command that would activate this skill is already running with another specialist that fits better

If unsure, surface the trade-off in the command's output and let the user decide.

## Quality gate (alpha.15)

Before claiming this skill's work complete:

- [ ] Artifacts produced match the skill's expected outputs
- [ ] All discipline rules in this skill were respected (not just glanced at)
- [ ] No banned weasel words in any completion claim — `should`, `probably`, `seems to`, `appears to`, `might`, `hopefully`, `in theory`
- [ ] Any tool / library / framework added during this run has a decision section per `.bequite/principles/TOOL_NEUTRALITY.md`
- [ ] Acceptance criteria for the invoking command's task are met (or honestly reported as PARTIAL / FAIL)
- [ ] `.bequite/state/MISTAKE_MEMORY.md` updated when a project-specific lesson surfaced
- [ ] `.bequite/logs/AGENT_LOG.md` entry appended for the run
- [ ] Memory state files (LAST_RUN, WORKFLOW_GATES, CURRENT_PHASE) updated when gate state changed

If any item fails, do not claim done — report PARTIAL with the specific gap.
