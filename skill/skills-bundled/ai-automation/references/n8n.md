# n8n — Expert reference

> Deep reference for the **automation-architect** persona when the project uses n8n. Pair with `references/patterns.md` for cross-platform patterns.

n8n is fair-code-licensed (Sustainable Use License + commercial use under most conditions), Node.js-based, self-hostable or cloud-hosted, with 400+ integrations and first-class AI nodes (LangChain integration, Anthropic, OpenAI, Gemini, Cohere, Ollama). The strongest fit when the team is JS/TS-fluent, wants source-code escape hatches, and prefers self-host.

---

## Why pick n8n

- **Self-hostable** via Docker or `npm i n8n -g`. No per-execution pricing in self-host.
- **Source-code escape hatch** — Function node + Code node + LangChain Code node give you arbitrary JS / Python.
- **AI native** — AI Agent node, ToolsAgent, structured-output enforcement, vector store nodes, LangChain integrations.
- **Workflow JSON is the source of truth** — `n8n export:workflow` / `n8n import:workflow` make CI / git-versioning straightforward.
- **400+ integrations** — Slack, GitHub, Stripe, Hubspot, Airtable, Google Sheets, Postgres, Mongo, Notion, Discord, Telegram, Webflow, Vercel, Sentry, etc.

## Why NOT n8n

- **Single-tenant by default.** Multi-tenant SaaS where each customer has isolated workflows requires extra engineering (or an instance per tenant).
- **Queue-mode setup is non-trivial** — production reliability needs Bull (Redis) workers + a queue-aware deployment.
- **Workflow-state migrations** during upgrades require care; older flows can break on n8n major-version bumps.
- **No built-in workspace-level RBAC** (Cloud has it; community needs custom auth proxy).

## Pricing (May 2026)

- **Community Edition**: free, self-host. Compute + Redis cost only.
- **n8n Cloud Starter**: from $20/mo for 5k executions; scales by execution count + active workflows.
- **n8n Enterprise**: from $50k/yr for SAML / RBAC / SSO / multi-tenancy.

(Verify via `bequite freshness` before signing the ADR — pricing changes.)

---

## Architecture cheatsheet

```
[Trigger Node] ──▶ [Logic Nodes] ──▶ [Action Nodes]
   │
   ├── Webhook (HTTP)
   ├── Cron (schedule)
   ├── Queue (Redis / RabbitMQ)
   ├── Database changes
   ├── Email / Discord / Slack message
   └── Vendor-specific (Github push, Stripe webhook, etc.)
```

A workflow is a DAG of nodes connected by edges. Each node receives an array of *items* and emits an array. Branching happens via the **IF** node, **Switch** node, or **Router** node (community).

## Workflow JSON shape (excerpt)

```json
{
  "name": "Lead routing",
  "nodes": [
    {
      "id": "n1",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {
        "path": "leads/inbound",
        "httpMethod": "POST",
        "responseMode": "responseNode"
      }
    },
    {
      "id": "n2",
      "name": "Validate payload",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [440, 300],
      "parameters": {
        "jsCode": "const schema = z.object({ email: z.string().email(), name: z.string() }); const r = schema.safeParse($input.first().json); if (!r.success) { throw new Error('Invalid payload: ' + r.error.message); } return r.data;"
      }
    }
    // ...
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Validate payload", "type": "main", "index": 0 }]] }
    // ...
  },
  "settings": {
    "executionOrder": "v1",
    "timezone": "America/New_York"  // explicit; never rely on host TZ
  },
  "tags": [{"id": "lead-flows"}],
  "id": "<workflow-id>",
  "versionId": "<version-id>"
}
```

**Commit this JSON to `.n8n/workflows/<flow>.json`.** Strip `versionId` and `id` on commit if they churn; preserve them if the team uses n8n's API to push back.

## CI workflow for n8n

```yaml
# .github/workflows/n8n-deploy.yml (illustrative)
name: Deploy n8n workflows
on:
  push:
    branches: [main]
    paths: ['.n8n/workflows/**']
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Push workflows to staging
        env:
          N8N_HOST: ${{ secrets.N8N_STAGING_URL }}
          N8N_API_KEY: ${{ secrets.N8N_STAGING_API_KEY }}
        run: |
          for f in .n8n/workflows/*.json; do
            curl -X PUT "$N8N_HOST/api/v1/workflows/$(jq -r .id $f)" \
              -H "X-N8N-API-KEY: $N8N_API_KEY" \
              -H "Content-Type: application/json" \
              --data @"$f"
          done
      # Smoke test: trigger a manual run; assert 200
```

## Idempotency in n8n

The platform itself does not enforce idempotency. Author it in:

- **Webhook trigger**: include `Idempotency-Key` header validation in the Validate node; reject duplicates by checking against a Redis SET / Postgres unique constraint.
- **Action nodes**: prefer **upsert** over **insert** (Postgres `ON CONFLICT`, Stripe idempotency keys, Salesforce upsert by external ID).
- **Custom Function nodes**: `if (await redis.set('flow:lead:' + email, '1', { NX: true, EX: 86400 })) { /* first time */ } else { return [{json: {dedup: true}}]; }`.

## Retry + backoff

n8n's per-node retry settings (Workflow → Settings → "Continue on fail" + "Retry on fail" + "Wait between tries"):

- Set "Retry on fail" = true on every external-call node.
- Max tries: 3–5.
- Wait: exponential — 1s, 4s, 16s — with `Math.random() * 1000` jitter via Function node when needed.
- "Continue on fail" → route to error handler (a separate branch ending in a notification + DLQ insert).

For more complex retry patterns, use a Wait node (timer) + an IF node that checks an attempt counter pulled from the execution metadata.

## Dead-letter pattern

```
[External Call] ──(success)──▶ [Mark success]
        │
        └─(fail-after-retries)──▶ [Insert into DLQ table] ──▶ [Slack alert] ──▶ [Stop and Error]
```

DLQ table schema (Postgres):

```sql
create table dlq_n8n (
  id uuid primary key default gen_random_uuid(),
  flow_name text not null,
  execution_id text not null,
  payload jsonb not null,
  error_message text not null,
  failed_at timestamptz not null default now(),
  retried_at timestamptz,
  resolved_at timestamptz,
  resolved_by text
);
create index on dlq_n8n (flow_name, failed_at) where resolved_at is null;
```

Human / on-call retries from the DLQ via a separate "DLQ replayer" workflow.

## Observability

- **Trace ID propagation**: in Function node at flow entry, generate a UUID + write to `$execution.metadata.traceId`. Pass through every HTTP node's headers (`X-Trace-Id: {{ $execution.metadata.traceId }}`).
- **Sentry**: install the Sentry node; configure error route to send `error_message + flow_name + execution_id + traceId`.
- **Datadog / Honeycomb**: use the HTTP Request node to POST trace events to the OTLP endpoint.

## Cost control

- **Self-host**: compute is the cost; right-size Postgres for execution history. n8n Cloud bills per execution, so high-volume cron flows can rack up.
- **Cap on retries** to avoid retry-storm cost.
- **AI agent flows**: budget per run via a counter (Function node decrements from a Redis budget; circuit-breaker if zero).
- **Daily op-count alarm** in `bequite.config.toml::ai_automation.cost_alarm_daily_ops_per_scenario` (relevant for n8n Cloud).

## Common AI patterns

### Single-shot LLM call
```
[Webhook] → [Validate] → [Anthropic / OpenAI node] → [Format output] → [Respond]
```

### Tool-calling agent (LangChain)
```
[Webhook] → [AI Agent node (Anthropic) + Tool 1 + Tool 2 + Tool 3] → [Respond]
```

Set `max_iterations` on the AI Agent node; add a **Stop and Error** path for cost / iteration overflow. Tools allow-listed; never give the agent arbitrary HTTP / shell tools.

### RAG pipeline (n8n + vector DB)
```
[Webhook (question)] → [Query Pinecone / Qdrant / Weaviate node]
                     → [Anthropic with retrieved context]
                     → [Respond + log to observability]
```

## Deployment templates

For self-host:

```yaml
# docker-compose.yml — n8n self-host with queue mode + Postgres + Redis
version: "3.8"
services:
  n8n:
    image: n8nio/n8n:latest
    restart: unless-stopped
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${DB_PASSWORD}
      - QUEUE_BULL_REDIS_HOST=redis
      - EXECUTIONS_MODE=queue
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - N8N_BASIC_AUTH_ACTIVE=false
      # SSO / OAuth proxied at the load balancer.
    ports: ["5678:5678"]
    depends_on: [postgres, redis]
  worker:
    image: n8nio/n8n:latest
    command: worker
    environment:
      # same as above
    depends_on: [postgres, redis]
    deploy:
      replicas: 3
  postgres:
    image: postgres:16
    environment:
      - POSTGRES_DB=n8n
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes: [pg_data:/var/lib/postgresql/data]
  redis:
    image: redis:7-alpine
volumes:
  pg_data:
```

## When n8n is the wrong choice

- The team is non-engineer; UX needs to be hand-holding-simple → use **Make** or **Zapier**.
- Mission-critical, long-running (hours / days), needs durable timers + replay → use **Temporal**.
- TypeScript SaaS app's background jobs → use **Inngest** or **Trigger.dev**.
- AWS-deep stack → use **Step Functions**.

## Verification checklist (Doctrine `ai-automation` Rules → n8n specifics)

- [ ] Rule 1 — `.n8n/workflows/*.json` exists; matches the staging instance via API diff.
- [ ] Rule 2 — Every action node has idempotency key / upsert pattern / dedup check.
- [ ] Rule 3 — "Retry on fail" + exponential wait + jitter + DLQ branch.
- [ ] Rule 4 — Credentials referenced by name; no secret-shaped strings in JSON.
- [ ] Rule 5 — Trace ID generated at entry + propagated through HTTP node headers.
- [ ] Rule 6 — `tests/automation/<flow>/fixture.json` + `expected.json` per workflow.
- [ ] Rule 7 — Error route ends in Slack / Sentry node.
- [ ] Rule 8 — Validate node at flow entry; rejects malformed payloads.
- [ ] Rule 9 — AI Agent node has max_iterations + budget Function node + circuit-breaker.
- [ ] Rule 10 — Wait nodes / rate-limit configs match documented upstream limits.
- [ ] Rule 11 — Old flow tagged + new flow created; in-flight migration documented.
- [ ] Rule 12 — Cost roll-up emits to observability daily.

## References

- Docs: https://docs.n8n.io
- GitHub: https://github.com/n8n-io/n8n
- API reference: https://docs.n8n.io/api/
- Workflow JSON schema: https://docs.n8n.io/workflows/export-import/
- LangChain integration: https://docs.n8n.io/advanced-ai/
- Self-host guide: https://docs.n8n.io/hosting/
- Queue mode: https://docs.n8n.io/hosting/scaling/queue-mode/
