# Make.com — Expert reference

> Deep reference for the **automation-architect** persona when the project uses Make.com (formerly Integromat). Pair with `references/patterns.md` for cross-platform patterns.

Make is a no-code-friendly proprietary SaaS automation platform — 1500+ pre-built apps, scenario visual builder, error-handler routing, scheduling, repeat aggregator. The strongest fit when the user audience is **non-engineer power-users** and the integration breadth matters more than source-code escape.

---

## Why pick Make

- **1500+ apps** — broader than n8n in some domains (CRMs, CSV / Excel handlers, telephony).
- **Best-in-class no-code UX** — drag-and-drop scenarios; non-engineers can author and audit.
- **Error-handler routing** — *break*, *commit*, *resume*, *rollback* directives at every module.
- **Aggregators / iterators** — first-class for "for each row in this CSV, do X" patterns.
- **Schedule + cron** support, with retry queue.
- **Data stores** — built-in K-V tables for cross-scenario state.
- **OAuth-heavy app library** — handles the boring auth refresh dance for the team.

## Why NOT Make

- **Per-operation pricing scales fast.** Routers, iterators, aggregators amplify ops. A flow that processes 1k records with 10 steps each = 10k ops per run.
- **No source-code escape hatch.** The "Code" module is JS-only and limited (no npm install, no full Node runtime).
- **Vendor lock-in.** Scenarios are platform-specific; migration to another platform = rewrite.
- **No deep AI orchestration.** Can call OpenAI / Anthropic / Vertex via HTTP, but no native agent / tool-calling primitive.
- **Workspace isolation** is per-organisation; multi-tenant SaaS apps need careful design.

## Pricing (May 2026 — verify with `bequite freshness`)

- **Free**: 1k operations/mo, 2 active scenarios, 15-min minimum interval.
- **Core**: $9/mo (10k ops, 1-min interval).
- **Pro**: $16/mo (10k ops + premium apps + custom variables).
- **Teams**: $29/user/mo (shared connections, RBAC).
- **Enterprise**: custom (SSO, SCIM, audit log, dedicated support).

**Operations** are the cost unit, not scenarios. A cron scenario running every minute that does 5 ops = ~216k ops/mo.

---

## Scenario architecture

```
[Trigger module]   ──▶   [Action modules]   ──▶   [Aggregator / Router]   ──▶   [More actions]
   │
   ├── Webhook (instant)
   ├── Schedule (cron)
   ├── Mailhook (email-triggered)
   ├── Polling (vendor-watch — every X minutes)
   └── App-specific (e.g. "New Stripe customer")
```

Each module = 1 operation per execution. The scenario blueprint exports as JSON via the API.

## Scenario JSON shape (excerpt — Make API)

```json
{
  "name": "Lead → CRM + Slack",
  "blueprint": {
    "flow": [
      {
        "id": 1,
        "module": "gateway:CustomWebHook",
        "version": 1,
        "parameters": {
          "hook": { "type": "json" }
        },
        "mapper": {},
        "metadata": { "designer": { "x": 0, "y": 0 } }
      },
      {
        "id": 2,
        "module": "json:ParseJSON",
        "version": 1,
        "parameters": { "type": "object" },
        "mapper": { "json": "{{1.body}}" }
      }
      // ...
    ],
    "metadata": {
      "instant": true,
      "version": 1,
      "scenario": {
        "roundtrips": 1,
        "maxErrors": 3,
        "autoCommit": true,
        "autoCommitTriggerLast": true
      }
    }
  },
  "scheduling": { "type": "indefinitely" },
  "teamId": <team-id>,
  "folderId": <folder-id>
}
```

**Commit blueprint JSON to `scenarios/<scenario>.json`.** Use the Make API (`/api/v2/scenarios/{id}/blueprint`) to export and import.

## CI deployment

```yaml
# .github/workflows/make-deploy.yml (illustrative)
name: Deploy Make scenarios
on:
  push:
    branches: [main]
    paths: ['scenarios/**']
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Push scenarios to staging
        env:
          MAKE_TOKEN: ${{ secrets.MAKE_API_TOKEN }}
          MAKE_TEAM: ${{ secrets.MAKE_STAGING_TEAM_ID }}
        run: |
          for f in scenarios/*.json; do
            ID=$(jq -r .id "$f")
            curl -X PUT "https://eu1.make.com/api/v2/scenarios/$ID/blueprint" \
              -H "Authorization: Token $MAKE_TOKEN" \
              -H "Content-Type: application/json" \
              --data @"$f"
          done
```

## Idempotency in Make

- **Webhook trigger**: parse JSON; first action is a "Search" against the destination system (Search HubSpot for the email; Search Stripe customer); branch on found-or-not. Avoid blind-create.
- **Aggregators**: when iterating, deduplicate on a business key (email, external ID) before insert.
- **Data stores**: K-V cache the IDs already processed; check before mutating.
- **Stripe / payment processors**: use idempotency keys directly via the HTTP module.

## Retry + backoff in Make

- **Scenario settings**: max errors before halt (default 3). Set per scenario.
- **Module-level**: each module has "Process incomplete executions" → automatic retry queue. Configure max attempts.
- **Manual retry** via the Repeater module (controlled loop, with Wait between tries).
- **Error handlers** on each module: *break* (stop scenario), *commit* (mark success despite error), *resume* (continue with substitute), *rollback* (undo prior modules).

## Dead-letter pattern

```
[Action] ──(success)──▶ [Next]
   │
   └─(error)──▶ [Error handler: break]
                       │
                       └──▶ [Insert to data store: DLQ_table]
                              ──▶ [Slack alert with run link]
```

DLQ entries reviewed via a "DLQ replayer" scenario triggered manually or on schedule.

## Observability

- **Trace ID**: at scenario start, generate UUID via Tools → Set Variable; pass through every HTTP module's headers.
- **Sentry**: HTTP module POSTs to `/api/0/projects/{slug}/store/` with bundle data on error.
- **Datadog / Honeycomb**: same pattern via OTLP HTTP.
- **Built-in run history** at scenario.detail / executions; retain for X days based on plan.

## Cost control — the operations meter

This is the #1 thing you'll get wrong. Make charges per operation, and routers/iterators/aggregators multiply ops fast.

- **Audit per-scenario op count** weekly. Anomalies = investigate.
- **Use filters early** — drop irrelevant items before they enter expensive modules.
- **Bundle aggregator** — process N items as one HTTP request when possible.
- **Schedule infrequent triggers** — every 15 min / hour, not every 1 min, unless real-time required.
- **Cap iterators** — set "Maximum number of cycles" to prevent runaway.
- **Daily-op alarm** in `bequite.config.toml::ai_automation.cost_alarm_daily_ops_per_scenario`.

## Common AI patterns

### Single-shot LLM via OpenAI / Anthropic module

```
[Webhook] → [Parse JSON] → [OpenAI: chat completion] → [Format] → [Respond]
```

### Multi-step "AI processing" (no native agent — manual)

```
[Webhook] → [OpenAI: classify intent]
          → [Router]
                ├── (sales) → [HubSpot: create lead] → [Slack: notify sales]
                ├── (support) → [Zendesk: create ticket] → [Slack: notify support]
                └── (other) → [Email: human review]
```

For real "tool-calling agent" patterns, Make is weaker than n8n / LangChain — consider HTTP module → Anthropic with explicit tool definitions, then a Router on the tool-call response, then back to Anthropic in a Repeater.

## Connector secrets

- **Connections** stored encrypted at the team level.
- Never embed tokens in scenario blueprints; reference connection IDs.
- **Rotate** connections via the Make UI / API; scenarios pick up new credentials at next run.
- **Per-environment connections** — separate connection IDs for staging / prod.

## When Make is the wrong choice

- Engineering team wants source-code-first workflow → use **n8n** or **Inngest** / **Trigger.dev**.
- Long-running (> 40 min per execution) or durable-timer use cases → use **Temporal**.
- AI-agent-heavy with tool-calling chains → use **n8n** with LangChain or **Inngest** with native AI primitives.
- Per-execution cost optimisation matters → self-hosted **n8n** beats Make on volume.

## Verification checklist (Doctrine `ai-automation` Rules → Make specifics)

- [ ] Rule 1 — `scenarios/*.json` exists; matches the live blueprint via API diff.
- [ ] Rule 2 — Every mutation module has search-before-create / upsert / idempotency-key.
- [ ] Rule 3 — Module-level "Process incomplete executions" + scenario-level max errors set.
- [ ] Rule 4 — No secret-shaped strings in committed JSON; connections referenced by ID.
- [ ] Rule 5 — Trace ID set at start; propagated through HTTP modules.
- [ ] Rule 6 — `tests/automation/<scenario>/fixture.json` per scenario.
- [ ] Rule 7 — Error handlers route to Slack / DLQ data store.
- [ ] Rule 8 — Parse JSON / validation module at scenario entry; error handler on parse fail.
- [ ] Rule 9 — AI module flows have explicit budget + circuit-breaker (counter in data store).
- [ ] Rule 10 — Sleep / Tools → Set Variable / Repeater paces upstream-API calls.
- [ ] Rule 11 — Old scenario disabled + new scenario created; in-flight execution policy documented.
- [ ] Rule 12 — Daily op-count emitted to observability.

## References

- Docs: https://www.make.com/en/help
- API reference: https://www.make.com/en/api-documentation
- Blueprint export / import: https://www.make.com/en/help/scenarios/exporting-and-importing-scenarios
- OAuth connections: https://www.make.com/en/help/connections
- Built-in modules: https://www.make.com/en/help/tools
- Webhooks: https://www.make.com/en/help/tools/webhooks
- Pricing: https://www.make.com/en/pricing
