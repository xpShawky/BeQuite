---
name: ai-automation
version: 1.0.0
applies_to: [automation, workflow, integration, n8n, make, zapier, temporal, inngest]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
---

# Doctrine: ai-automation v1.0.0

> Doctrine for projects whose primary deliverable is an **automation pipeline / workflow** — n8n flows, Make.com (formerly Integromat) scenarios, Zapier zaps, Pipedream workflows, Temporal workflows, Inngest functions, Trigger.dev jobs, AWS Step Functions. Loaded by `.bequite/bequite.config.toml::doctrines = ["ai-automation"]`.
>
> Stack with `default-web-saas` when the automation has a web dashboard, with `cli-tool` when it ships as a CLI runner, with `library-package` when it's distributable. `ai-automation` governs the workflow-specific overlays.

## 1. Scope

Applications and projects where the **core value** is moving data + triggering actions across systems. Includes: lead-routing flows, ETL pipelines, AI agent chains, Slack-bot automations, e-commerce order routing, billing reconciliation, marketing-attribution flows, customer-support routing, RPA-style workflows, scheduled reports, webhook fan-outs.

**Does NOT cover:** projects that *use* automation as a small sub-feature (use the relevant primary Doctrine instead, with a single ADR for the automation choice). Long-running ML training pipelines (use `ml-pipeline`).

## 2. Rules

### Rule 1 — Workflows are version-controlled source code
**Kind:** `block`
**Statement:** Every automation workflow is exported and committed to git. n8n: `.n8n/workflows/<flow>.json`. Make: `scenarios/<scenario>.json` (via the Make API export). Zapier: `zaps/<zap>.zap.yml` (Zapier's CLI export). Temporal: TypeScript / Go / Python source in `workflows/`. Inngest / Trigger.dev: TypeScript source. The vendor's UI is for visualisation, not authoritative storage.
**Check:** `bequite audit` checks for at least one file under `.n8n/workflows/` / `scenarios/` / `zaps/` / `workflows/` / `inngest/` and flags any flow whose UI version differs from the committed JSON (when API access available).
**Why:** UI-only flows die with the vendor; vendor-locked state is unauditable.

### Rule 2 — Idempotency is non-negotiable
**Kind:** `block`
**Statement:** Every flow node that mutates external state (creates a record, sends an email, posts to Slack, charges a card) is idempotent on retry. Approved patterns: idempotency keys (Stripe-style), upsert-by-business-key (not by surrogate ID), conditional updates (e.g. update only if `version == previous`), exactly-once semantics via Inngest / Temporal, deduplication by message ID for queue-driven flows.
**Check:** `bequite audit` reviews flow nodes for known mutation actions; flags missing idempotency keys.
**Why:** retries are inevitable; double-execution is a real-money bug.

### Rule 3 — Retries with exponential backoff + jitter + dead-letter
**Kind:** `block`
**Statement:** Every external-call node has a documented retry policy: max attempts, backoff strategy (exponential), jitter (full or equal), retry-only-on (5xx / 429 / specific error codes — never on 4xx auth or validation errors). Failed-after-max-retries goes to a dead-letter queue / table / alert channel, not silently discarded.
**Check:** `bequite audit` parses node configs for retry settings; flags missing or naive (e.g. linear backoff without jitter, retry-on-everything).
**Why:** thundering-herd recovery storms + silent data loss.

### Rule 4 — Secrets via connector / env, never in flow JSON
**Kind:** `block`
**Statement:** API keys, OAuth tokens, database passwords go through the platform's credential store (n8n Credentials, Make Connections, Zapier auth, Temporal secret stores, env vars). The exported flow JSON refers to credentials by ID; never embeds secret values. PreToolUse hook + git pre-commit greps for secret-shaped strings in any committed flow file.
**Check:** `bequite audit` scans `.n8n/workflows/` / `scenarios/` / `zaps/` / `workflows/` / `inngest/` for secret-shaped strings; flags violations. Iron Law IV binding.
**Why:** flow JSON is committed to git; secrets in git are breaches.

### Rule 5 — Observability — every run is traceable
**Kind:** `block`
**Statement:** Every workflow execution carries a `correlation_id` / `trace_id` / `request_id` propagated across all nodes and external calls. n8n: use the Execution metadata field. Make: pass through the bundle. Temporal: native workflow ID + run ID. Inngest: Run ID. Logs / observability backend (Datadog / Sentry / Honeycomb / Better Stack) ingest the trace ID for cross-cutting search.
**Check:** `bequite audit` greps for trace-ID-shaped propagation in flow JSON / source.
**Why:** "the flow ran 6 times yesterday and one failed silently" is unsolvable without trace correlation.

### Rule 6 — Test fixtures + dry-run mode
**Kind:** `block`
**Statement:** Every flow has at least one runnable test fixture: a sample webhook payload, a mock external response, a test-mode toggle. Dev/staging environments use the platform's sandbox / test mode (Stripe Test, Shopify Dev Store, Slack test workspace, Sandbox HubSpot). Real production data never reaches non-prod.
**Check:** `bequite audit` checks for a `tests/automation/` directory with at least one fixture per flow.
**Why:** flows are easy to break by upstream API changes; fixtures catch regressions.

### Rule 7 — Error notification routing
**Kind:** `block`
**Statement:** Failed runs trigger a notification to a documented channel: Slack alert / PagerDuty / email / Sentry issue. The notification carries: flow name, run ID, error message, retry count, link to the failed run in the platform UI. Severity tiered: warn (single failure), critical (DLQ entry / threshold breached).
**Check:** `bequite audit` checks for error-handler node / on-error route in every flow + a notification config in `.bequite/bequite.config.toml::ai_automation.error_routing`.
**Why:** silent failures rot for weeks.

### Rule 8 — Schema validation at the boundary
**Kind:** `block`
**Statement:** Every external webhook input + every API response that drives downstream logic is schema-validated (Zod / Pydantic / Valibot / JSON Schema) at the first node. Unexpected payload shape stops the flow with a clear error; downstream nodes never fork on `if (data.foo)` without confirming the shape.
**Check:** `bequite audit` checks for validation nodes / steps at flow entry points.
**Why:** silent garbage propagation is the #2 automation bug.

### Rule 9 — AI-agent chains with budget + circuit breaker
**Kind:** `block`
**Statement:** Flows that include LLM calls / AI-agent loops have a per-run cost ceiling (USD), a max-iterations cap, and a circuit breaker (auto-disable if N consecutive failures or cost-runaway detected). The agent's tool call list is curated (no arbitrary code-exec, no arbitrary file write, no arbitrary HTTP egress beyond the documented allow-list).
**Check:** `bequite audit` parses agent-node configs; flags missing budget / max-iter / circuit breaker. Prompt-injection rule (Article IV / master §19.5) binding: external content into LLM prompts MUST be sanitised + structured-input-separated.
**Why:** AI-agent runaway loops = real money + supply-chain risk.

### Rule 10 — Rate-limit awareness for upstream APIs
**Kind:** `block`
**Statement:** Flows respect upstream API rate limits. Token-bucket pacing or platform-native throttling (n8n's Wait node, Make's "Stop after X requests", Temporal's rate-limiter activity). Documented in `docs/automation/rate-limits.md` per upstream service.
**Check:** `bequite audit` checks for the rate-limits doc + pacing nodes in flows that call high-volume APIs.
**Why:** crashing the partner's API is a relationship-killer + may incur lock-out.

### Rule 11 — Versioned flow upgrades
**Kind:** `block`
**Statement:** When a flow is updated, the new version is committed with a new ID (or a `_v2` suffix) — old flow stays running for a deprecation window before retirement. Migration of in-flight executions is documented.
**Check:** `bequite audit` checks for version suffix / commit history showing parallel-run pattern.
**Why:** in-flight runs at upgrade time are otherwise lost.

### Rule 12 — Cost roll-up per flow per day
**Kind:** `recommend`
**Statement:** Cost (platform op-counts + LLM tokens + external API call costs) rolled up per flow per day to a dashboard / log. Anomaly alarms when daily cost > 1.5× rolling-7-day average.
**Check:** advisory; receipts / observability config.
**Why:** the silent killer of automations is the cost runaway.

## 3. Stack guidance

### Workflow platforms (pick by use case)

| Platform | Best for | Strength | Watch out |
|---|---|---|---|
| **n8n** | Self-hostable, fair-code, JS/TS-fluent teams, AI-heavy flows | Full source-code escape hatch (Function node), AI nodes (LangChain integration, Anthropic/OpenAI/Gemini built-in), 400+ integrations, self-host = no per-op pricing | Single-tenant queue management; workspace isolation manual |
| **Make.com** | Non-engineer power-users, deep tier of integrations | 1500+ apps, scenario visual builder, error handler routing, scheduling, repeat aggregator | Per-operation pricing scales fast; vendor lock-in; no source-code escape |
| **Zapier** | Marketing / sales / ops teams, simplest UX | 7000+ apps, easiest to teach non-technical users | Per-task pricing; weak for complex branching; limited code steps |
| **Temporal** | Mission-critical, long-running, durably-consistent workflows | Code-first (TS / Go / Python / Java); replay debugging; durable timers; signals + queries | Steeper learning curve; self-host or Temporal Cloud |
| **Inngest** | TypeScript-first, event-driven, serverless | Step functions in TS, automatic retry, replay, parallel; native fan-out | TS-only at present; smaller ecosystem |
| **Trigger.dev** | TypeScript-first alt to Inngest | Open-source, self-host or hosted | Younger; ecosystem catching up |
| **AWS Step Functions** | AWS-native, serverless | Tight AWS integration, ASL JSON | Vendor lock-in; steep DSL |
| **Pipedream** | Code-first power-users, hosted | Free tier generous; TypeScript steps | Smaller ecosystem |

### Recommended default

For new BeQuite-managed automation projects:

- **Self-hostable + AI-heavy + JS-fluent team:** n8n (community edition, deployed via Docker Compose).
- **Non-engineer power-users + many third-party apps:** Make.com (with cost ceiling alarm).
- **Mission-critical + long-running:** Temporal (Temporal Cloud for managed).
- **TypeScript SaaS app needing background work:** Inngest (managed) or Trigger.dev (self-host).

When uncertain, the Architect runs `bequite freshness` against each candidate before signing the ADR. Stack ADR-AUTO-001 captures the choice.

### Recommended observability

- **Datadog Workflow Insights** or **Better Stack** or **Honeycomb** for trace propagation.
- **Sentry** for error capture (every flow's error-handler node sends to Sentry).
- **Slack** or **PagerDuty** for human alerts.

### Recommended secret management

- **Doppler / Infisical / 1Password Connect / Vault** for credentials shared across n8n + Make + Temporal + Inngest deployments.
- **Per-platform credential store** for platform-specific tokens.
- **Never** put secrets in flow JSON (Rule 4 binding).

## 4. Verification

`bequite verify` for ai-automation projects (in addition to the primary Doctrine's gates):

1. **Flow JSON commit check** — every flow exported, committed, no UI-only drift.
2. **Idempotency simulation** — for every mutation node, run twice with identical input; assert end state identical (no double-create).
3. **Retry policy presence** — every external-call node has documented retry config.
4. **Secret-shaped strings in flow JSON** — git-pre-commit + `bequite audit` scan returns zero matches.
5. **Trace-ID propagation** — sampling a flow run end-to-end, the trace ID appears in every external-call log.
6. **Test fixtures** — at least one fixture per flow.
7. **Error notification dry-run** — force an error; assert the notification fires with the expected payload shape.
8. **Schema validation at entry** — sample malformed payload; flow rejects cleanly.
9. **AI-agent budget check** — simulate runaway; assert circuit breaker fires.
10. **Rate-limit pacing** — a flow that calls a rate-limited API maintains < limit/sec across a 60-second test.

## 5. Examples and references

- n8n: https://n8n.io/ · docs https://docs.n8n.io · GitHub https://github.com/n8n-io/n8n
- Make: https://www.make.com/ · documentation https://www.make.com/en/help
- Zapier: https://zapier.com/ · CLI https://github.com/zapier/zapier-platform-cli
- Temporal: https://temporal.io/ · docs https://docs.temporal.io
- Inngest: https://www.inngest.com/ · docs https://www.inngest.com/docs
- Trigger.dev: https://trigger.dev/ · docs https://trigger.dev/docs
- Pipedream: https://pipedream.com/
- AWS Step Functions: https://aws.amazon.com/step-functions/

Bundled skill at `skill/skills-bundled/ai-automation/` provides deeper per-platform expertise (n8n.md, make.md, zapier.md, temporal.md, inngest.md, patterns.md).

## 6. Forking guidance

Common forks:
- **`ai-automation-no-code-only`** — drop Rule 1's source-code-escape preference; for teams that cannot use code-step nodes.
- **`ai-automation-regulated`** — overlay HIPAA / PCI / SOC 2 controls on top (combine with `healthcare-hipaa` / `fintech-pci` Doctrines).
- **`ai-automation-llm-agent-heavy`** — strengthen Rule 9 (per-call budget; per-tool allow-lists; deeper prompt-injection guardrails).
- **`ai-automation-internal-rpa`** — for browser-automation / RPA flows (Playwright in n8n; Browserbase; Stagehand). Adds desktop / browser session management rules.

Pattern:
1. Copy this file to `.bequite/doctrines/<your-name>.md`.
2. Bump `version` to `0.1.0`.
3. Set `supersedes: ai-automation@1.0.0`.

## 7. Changelog

```
1.0.0 — 2026-05-10 — initial draft. Rules 1–12 ratified. Stack matrix as of May 2026. n8n / Make as the default-recommended pair.
```
