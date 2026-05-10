# Temporal — Brief reference

> Quick reference for the **automation-architect** when the project uses Temporal. Pair with `references/patterns.md`.

Temporal is the platform for **mission-critical, long-running, durable** workflows. Code-first (TS / Go / Python / Java); replay debugging; durable timers; signals + queries. Steeper learning curve than n8n / Make / Zapier; pays back when correctness matters.

---

## Why Temporal

- **Durable execution.** Workflows survive crashes, restarts, deploys.
- **Replay debugging.** Re-run a workflow from history; reproduce bugs deterministically.
- **Long-running** — workflows can run for weeks / months / years.
- **Signals + queries** — runtime input + introspection.
- **Native cron / scheduling.**
- **Versioning.** Safe migrations of in-flight workflows.
- **Native exactly-once semantics** — workflow ID + run ID.

## Why NOT

- Steep learning curve. Workflow vs activity vs task queue, deterministic constraints.
- Self-host = Temporal server + Postgres / Cassandra + Elasticsearch (heavy).
- Temporal Cloud = managed, but per-action pricing.
- Overkill for "send a Slack message when X happens" — use n8n / Inngest / Zapier instead.

## Pricing (May 2026)

- **Self-host**: free; pay infra. ~5GB DB for moderate volume.
- **Temporal Cloud**: per-action, regional. ~$0.025 per 10k actions for Standard tier.

## Architecture

```
[Worker process] (your code) ←──── [Task Queue] ←──── [Temporal Server] ←──── [Postgres / Cassandra]
                                                              │
                                                              └── workflow history (immutable, replayable)
```

## Workflow vs Activity

- **Workflow** = orchestration logic. Deterministic. No I/O. No clocks. No randomness without `workflow.random()`.
- **Activity** = side-effects. Make HTTP calls, write to DB, send email, etc.

```typescript
// workflow.ts — deterministic
import { proxyActivities } from '@temporalio/workflow';
import * as activities from './activities';

const { sendEmail, chargeCard, recordTransaction } = proxyActivities<typeof activities>({
  startToCloseTimeout: '1 minute',
  retry: { initialInterval: '1s', backoffCoefficient: 2.0, maximumAttempts: 5 },
});

export async function processOrder(orderId: string): Promise<void> {
  await chargeCard(orderId);
  await recordTransaction(orderId);
  await sendEmail(orderId);
}
```

## Patterns

- **Idempotency**: workflow ID = order ID. Starting the workflow twice with the same ID returns `WorkflowExecutionAlreadyStarted`.
- **Retry**: built-in `RetryPolicy` per activity. Exponential backoff + jitter native.
- **Timeouts**: `startToCloseTimeout`, `scheduleToCloseTimeout`, `heartbeatTimeout`.
- **Signals**: external events into a running workflow (`workflow.signal('cancel', payload)`).
- **Queries**: read-only introspection of workflow state (`workflow.query('status')`).
- **Versioning**: `workflow.getVersion('change-name', defaultVersion, currentVersion)` + `patched(...)` for safe migration.
- **Schedules**: native cron / interval; durable.

## AI workflows in Temporal

```typescript
const { generateWithLLM, callTool, validateOutput } = proxyActivities<typeof activities>({
  startToCloseTimeout: '5 minutes',
});

export async function aiAgentLoop(input: string): Promise<AgentResult> {
  let iterations = 0;
  let context = input;
  const MAX_ITER = 10;

  while (iterations++ < MAX_ITER) {
    const llmResp = await generateWithLLM(context);
    if (llmResp.action === 'finish') return { result: llmResp.output };
    const toolResult = await callTool(llmResp.action, llmResp.input);
    context = `${context}\n\nTool ${llmResp.action} returned: ${toolResult}`;
  }
  return { result: 'iteration cap reached', error: true };
}
```

The workflow is durable — if the worker crashes mid-run, it resumes from history. Activities are retried per their RetryPolicy. Cost ceiling enforced via accumulating tokens / dollars in workflow state.

## When Temporal is the wrong choice

- Single-step "trigger → action" flows — overkill; use n8n / Make / Zapier.
- Non-engineer authors — code-first; not for them.
- Tight budget — self-host setup + ops.

## Verification

- [ ] Rule 1 — Workflow + activity TS / Go / Python source committed.
- [ ] Rule 2 — Workflow ID = business key (order ID, user ID).
- [ ] Rule 3 — Activity RetryPolicy explicit; no retry-on-everything.
- [ ] Rule 4 — Secrets via env / KMS; never in workflow code.
- [ ] Rule 5 — Workflow ID + run ID = native trace; OTel SDK auto-instruments.
- [ ] Rule 6 — `replay-test`s using workflow history JSON fixtures.
- [ ] Rule 7 — Failed-workflow handler signals on-call channel.
- [ ] Rule 8 — Activity input types validated (TS strict + Zod).
- [ ] Rule 9 — AI agent loop has iteration cap + cost-state in workflow.
- [ ] Rule 10 — Activity `RateLimiter` for pacing.
- [ ] Rule 11 — `getVersion` / `patched` for safe in-flight migration.
- [ ] Rule 12 — Cost accumulator in workflow state; periodic dump to observability.

## References

- Docs: https://docs.temporal.io
- TypeScript SDK: https://docs.temporal.io/dev-guide/typescript
- Patterns: https://docs.temporal.io/encyclopedia/patterns
- Replay testing: https://docs.temporal.io/dev-guide/typescript/testing
- Temporal Cloud: https://temporal.io/cloud
