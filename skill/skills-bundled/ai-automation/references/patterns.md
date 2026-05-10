# Cross-platform automation patterns

> Patterns that apply across n8n / Make / Zapier / Temporal / Inngest / Step Functions / Pipedream / Trigger.dev. The **automation-architect** persona references this when designing flows.

Eight pattern families. Each shows the goal, the failure mode it prevents, and the per-platform implementation.

---

## 1. Idempotency — "this runs twice; nothing breaks"

### Why
Retries are inevitable. Without idempotency, retries double-charge cards, double-send emails, or create duplicate records.

### Patterns

| Pattern | When | Implementation |
|---|---|---|
| **Idempotency key** | External API supports it (Stripe, Shippo, Twilio) | Generate stable UUID at flow entry; pass as `Idempotency-Key` header on every retry of the same logical operation |
| **Upsert by business key** | DB writes | `INSERT ... ON CONFLICT(email) DO UPDATE` (Postgres); `merge` (Drizzle); `upsert` (Prisma); Salesforce upsert by external ID |
| **Search-then-create** | Vendor APIs without idempotency keys | Search by business key first; create only if not found; race-condition window mitigated by retry |
| **Conditional update** | State machines | `UPDATE ... WHERE status = 'pending'` (idempotent re-execution returns 0 rows changed; that's fine) |
| **Dedup table** | Webhook deduplication | Table `(message_id PK, processed_at)`; `INSERT ... ON CONFLICT DO NOTHING` |
| **Exactly-once semantics** | Mission-critical | Use **Temporal** (workflow ID + run ID = exactly-once) or **Inngest** (event ID dedup) |

### Per-platform notes

- **n8n**: Function node with Redis SET NX, or Postgres node with ON CONFLICT.
- **Make**: Search module before Create module; Data Store as dedup table.
- **Zapier**: Filter step "Only continue if [field] does not exist in [destination]".
- **Temporal**: `WorkflowExecutionAlreadyStartedError` already handles workflow-level idempotency; activities use `RetryPolicy{MaximumAttempts}` + side-effect functions.
- **Inngest**: `step.run()` is automatically idempotent within a step; events with the same `id` are deduped.

---

## 2. Retry with exponential backoff + jitter

### Why
External services flake. Naive linear retry creates thundering herds. Jitter spreads recovery load.

### The right shape

```
attempt_n_delay = base_delay * (2 ^ n) + random(0, jitter_ms)
```

Defaults: `base_delay=1s`, `max_delay=300s`, `max_attempts=5`, `jitter=full`.

**Retry on**: 5xx, 429, network timeouts, connection-reset.
**Never retry on**: 4xx auth (401/403), validation (422), business-rule violation (409).

### Per-platform

- **n8n**: Per-node "Retry on fail" + "Wait between tries" + Function node for jitter.
- **Make**: Module-level "Process incomplete executions"; manual Repeater + Sleep + jitter via Variable.
- **Zapier**: Auto-retry up to 3 times (Pro+); custom code step for jitter.
- **Temporal**: `ActivityRetryPolicy{InitialInterval: 1s, BackoffCoefficient: 2.0, MaximumInterval: 5min, MaximumAttempts: 5}`. Built-in jitter.
- **Inngest**: Steps automatically retry with exponential backoff. Custom: `await step.run('call', { retries: 5 }, async () => { ... })`.

---

## 3. Dead-letter queue (DLQ) — "fail loudly, recover later"

### Why
After max retries, the alternative to DLQ is silent data loss.

### Shape

```
[Action] ──(success)──▶ [Next step]
        │
        └──(fail-after-retries)──▶ [Insert to DLQ store]
                                       │
                                       ├──▶ [Alert on-call]
                                       └──▶ [Stop flow gracefully]
```

DLQ store schemas:

```sql
-- Postgres
create table dlq (
  id uuid primary key default gen_random_uuid(),
  flow_name text not null,
  execution_id text not null,
  payload jsonb not null,
  error_message text not null,
  failed_at timestamptz default now(),
  retried_at timestamptz,
  resolved_at timestamptz,
  resolved_by text
);
create index on dlq (flow_name, failed_at) where resolved_at is null;
```

**DLQ replayer**: a separate flow scheduled hourly; selects unresolved DLQ entries; attempts replay; updates `retried_at` / `resolved_at` accordingly.

### Per-platform

- **n8n**: Error route to Postgres node + Slack node + Stop and Error.
- **Make**: Error handler "break" → Data Store insert + Slack module.
- **Zapier**: Path with "Filter on error"; Code step + Webhook to logging service.
- **Temporal**: Failed workflows persist in history forever — DLQ is implicit. Use a "DLQ workflow" to consume failed signals.
- **Inngest**: `failureHandler` step + send-to-DLQ event.

---

## 4. Fan-out + fan-in — "process 100 items in parallel; collect results"

### Why
Sequential processing of independent items wastes time. Naive fan-out creates rate-limit violations + memory blow-ups.

### Pattern

```
[Trigger] ──▶ [Splitter] ──▶ [Worker 1, Worker 2, ..., Worker N (parallel)] ──▶ [Aggregator] ──▶ [Final action]
```

**Fan-out cap**: `concurrency = min(items, max_workers)` where `max_workers` respects upstream-API rate limits.

**Aggregator collects**: success count, failure count, partial-failure handling, completion timestamp.

### Per-platform

- **n8n**: Split In Batches node + concurrent execution mode (queue-mode-only); Merge node for fan-in.
- **Make**: Iterator + Aggregator (Array, Numeric, Text); built-in.
- **Zapier**: Looping by Zapier (Pro+); limited fan-out, mostly sequential.
- **Temporal**: `Promise.all([activity1, activity2, ...])` — true parallelism within a workflow.
- **Inngest**: `step.parallel([...])` — true parallel; results collected.

---

## 5. Circuit breaker for AI-agent loops

### Why
LLM agent loops can run away — keep calling tools forever or hitting cost ceilings. The circuit breaker stops the bleeding.

### State machine

```
CLOSED ──(N failures)──▶ OPEN ──(timeout)──▶ HALF-OPEN ──(1 success)──▶ CLOSED
                                       └──(1 failure)──▶ OPEN
```

### Triggers

- **Iteration count** > `max_iterations` (default 10).
- **Cost** > `max_cost_usd` per run (token-economist tracks).
- **Consecutive failures** > 3.
- **Latency** sustained > p99 threshold for N minutes.

### Action when OPEN

- Stop the agent loop.
- Return a documented "circuit open" error to the caller.
- Page on-call after K consecutive trips.
- Auto-close after a documented cool-down (default 5 minutes).

### Per-platform

- **n8n**: Function node tracks state in Redis; IF node checks before each AI Agent invocation.
- **Make**: Data Store as state holder; Router on circuit-state.
- **Inngest**: `step.run()` with try/catch + state in event metadata.
- **Temporal**: Workflow-local variable + `condition()` wait; signal to reset.
- **Custom service**: a dedicated breaker library (e.g. `cockatiel`, `polly`).

---

## 6. Schema validation at the edge

### Why
Garbage-in propagates fastest in automation. Catch shape errors at the entry node.

### Pattern

```
[Webhook] ──▶ [Validate schema (Zod / Pydantic / JSON Schema)] ──┬──(valid)──▶ [Continue]
                                                                  └──(invalid)──▶ [400 response + log]
```

### Validators

- **n8n**: Code node with Zod / Joi.
- **Make**: Parse JSON module + Filter (catches some shape issues); for true validation use a custom HTTP module to a validator endpoint.
- **Zapier**: Filter step + Code step.
- **Temporal**: Validate in the workflow function (TS / Python type guards).
- **Inngest**: `event.schema()` with Zod.

### Schema source of truth

- A `schemas/` directory at the repo root with one file per webhook contract.
- Versioned (`v1`, `v2`); never breaking-change a webhook contract without a parallel-run.
- `bequite audit` checks every webhook trigger has a corresponding schema file.

---

## 7. Trace propagation — observability across the flow

### Why
Without a trace ID, "the flow ran 6 times yesterday and one failed" is unsolvable.

### Pattern

```
1. At flow entry: generate `trace_id` (UUID) OR adopt incoming `X-Trace-Id` / `traceparent` header.
2. Store in execution metadata.
3. Pass through every HTTP node's outgoing headers.
4. Include in every log line.
5. Sentry / Datadog / Honeycomb correlate via `trace_id`.
```

### Per-platform

- **n8n**: `$execution.metadata.traceId` + Function node at entry; HTTP node has "Send headers" config.
- **Make**: `Tools → Set Variable` + per-HTTP-module headers config.
- **Temporal**: workflow ID + run ID are native; OTel SDK auto-instruments.
- **Inngest**: event ID + step IDs are native; OTel exporter optional.
- **AWS Step Functions**: AWS X-Ray native.

### Storage

OTel JSON line per execution:

```json
{
  "trace_id": "01J5G...",
  "span_id": "...",
  "flow_name": "lead-routing",
  "execution_id": "n8n-exec-12345",
  "started_at": "2026-05-10T14:23:01Z",
  "ended_at": "2026-05-10T14:23:04Z",
  "status": "ok",
  "events": [
    { "node": "validate", "duration_ms": 12, "status": "ok" },
    { "node": "hubspot-upsert", "duration_ms": 832, "status": "ok" },
    { "node": "slack-notify", "duration_ms": 421, "status": "ok" }
  ]
}
```

---

## 8. AI-agent prompt-injection guardrails

### Why
External content reaching an LLM is the #1 prompt-injection attack vector. Article IV / master §19.5 binding.

### Patterns

| Pattern | Implementation |
|---|---|
| **Structured-input separation** | Always pass external content as a *user* message; never concatenate into the system prompt. Tag external content explicitly: `<<USER_INPUT>>...<<END_USER_INPUT>>` |
| **Tool allow-list** | Agent's tool list is curated; never `arbitrary_http_get`, `arbitrary_shell_exec`, `arbitrary_file_write` |
| **Output validation** | LLM output schema-validated before passing to next step (Zod / Pydantic). Refusals + jailbreak attempts caught here |
| **Cost ceiling per run** | Hard cap; token-economist enforces |
| **Iteration ceiling** | `max_iterations = 10` default; circuit-breaker on overrun |
| **No-data-retention model tier** | When external content is sensitive, use the model vendor's no-retention enterprise tier |

### Detect attempts (red flags in input)

- "Ignore prior instructions"
- "You are now ..."
- "<system>"
- Multiple language switches (jailbreak in another language)
- Instruction-shaped content embedded in data fields

When detected, the agent's first action is `noop` and the input is logged for security-reviewer.

### Sanitisers

- **HTML escape** when external content is rendered back to a user.
- **Shell escape** when external content reaches a command line (don't, ideally).
- **JSON escape** when external content is interpolated into structured payloads.

---

## Pattern composition reference

For a typical "lead-routing" flow:

```
Idempotency (1) at webhook entry
  ↓
Schema validation (6) at flow entry
  ↓
Trace-ID generation (7)
  ↓
External API calls with retry (2) + DLQ on max-fail (3)
  ↓
AI agent for classification with circuit-breaker (5) + prompt-injection guardrails (8)
  ↓
Fan-out (4) to multiple downstream actions
  ↓
Aggregator (4 — fan-in) for final response
  ↓
Trace exported to observability backend (7)
```

Every line above maps to a Doctrine `ai-automation` Rule. The persona's verification report walks each one.

---

## References

- *Release It!* by Michael Nygard — circuit breaker, bulkhead, timeout patterns.
- *Designing Data-Intensive Applications* by Martin Kleppmann — idempotency, exactly-once, fan-out.
- AWS Architecture Center — workflow patterns: https://aws.amazon.com/architecture/
- Temporal patterns: https://docs.temporal.io/dev-guide/typescript/foundations
- Anthropic prompt-injection mitigation guide: https://docs.anthropic.com/en/docs/agents-and-tools/computer-use
- OWASP LLM Top 10 (2025) — LLM01 Prompt Injection: https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
