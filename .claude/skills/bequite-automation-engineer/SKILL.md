---
name: bequite-automation-engineer
description: Automation & bot engineering discipline — workflow/trigger/action design, tool-neutral platform selection (n8n / Make / Zapier / Activepieces / Temporal / Inngest / cron / GitHub Actions / queues / custom worker), official-API-first, idempotency keys, retry limits, dead-letter/failure handling, webhook replay protection, secret handling, dry-run + manual-approval gates, bot safety (Telegram/Discord/WhatsApp/web/admin). Loaded by /bq-automation and /bq-local-business; pairs with scraping-automation (web side) and backend-architect (services). Tool-neutral — installs nothing.
---

# bequite-automation-engineer — automation & bot discipline

## Purpose

Design reliable, tool-neutral automation and bot workflows as blueprints — never installing or requiring a tool by default. Distilled (alpha.24) from BeQuite's retired v2 `automation-architect` persona + the bundled ai-automation references (concept merge, not a copy; legacy at `skill/`, see LEGACY_SKILL_FOLDER_AUDIT). Pairs with `bequite-scraping-automation` (the web-data side) and `bequite-backend-architect` (services/queues).

## When this skill activates

- `/bq-automation` (workflow + bot profiles) · `/bq-local-business` (automation portions) · `/bq-integrate` when a workflow spans triggers→actions · `/bq-offer`/`/bq-pain-radar` when an automation service/idea is the deliverable.

## When NOT to use

Pure web-scraping/crawling (that's `scraping-automation`); a single API call inside app code (that's `backend-architect`); anything requiring a tool to be installed by default (refuse — blueprint only).

## Platform selection (tool-neutral; official-API-first)

Decide per the 10 tool-neutrality questions. Candidates (examples, never defaults; re-verify freshness before recommending): **no-code/low-code** n8n · Make · Zapier · Activepieces · Pipedream. **durable/code** Temporal · Inngest · Trigger.dev · AWS Step Functions. **primitives** cron · GitHub Actions · queues/workers (Redis/SQS-class) · webhooks · custom worker. **Decision rule:** official API of the source/target first; no-code for simple linear flows + non-technical maintainers; durable engine for long-running/stateful/retry-heavy; primitives when the project already has the runtime. Browser automation (Playwright) only when there is no API and ToS permits (Article VIII via scraping-automation).

## Reliability discipline (every automation blueprint includes)

- **Idempotency keys** — every action that can be retried must be safe to run twice (dedupe on a stable key).
- **Duplicate-trigger prevention** — webhooks fire more than once; dedupe by event ID.
- **Retry limits + backoff** — bounded retries; never infinite. **Dead-letter/failure queue** concept for what exhausts retries.
- **Webhook replay protection** — verify signatures + reject stale/duplicate deliveries.
- **Secrets** — never inline; env/secret-manager only; never logged; R3 file-risk gate applies.
- **Logs + audit trail** — every run leaves a trace; failures are visible, not swallowed.
- **Dry-run** + **manual-approval gates** for risky actions (sending money, mass messages, deletes, prod changes — these are hard human gates).
- **Rate limits** respected; **alerting** on failure; **rollback/disable switch** (kill switch) for every live automation.

## Bot profiles (the `bot` mode)

Platforms: Telegram · Discord · WhatsApp (API-safe/legal only) · website chat · internal admin bot. **Bot safety (mandatory):** explicit permission scopes · abuse/rate limits · command whitelist · user identity/auth · full logs · escalation-to-human path · never expose secrets or internal data · no destructive command without confirmation. WhatsApp: official Business API or approved provider only — no unofficial automation that violates terms.

## Output discipline

Blueprints only (TRIGGER_MAP · ACTION_MAP · DATA_FLOW · TOOL_DECISION · IDEMPOTENCY_PLAN · RETRY_AND_FAILURE_PLAN · SECURITY_AND_SECRETS · TEST_PLAN · HANDOFF). Mark any tool as a candidate + the decision rationale; never claim it's installed. UNVERIFIED for any platform behavior not confirmed from docs.

## Quality gate

Before claiming an automation design complete: official-API-first justified · idempotency + retry + failure-handling present · secrets handled (no inline) · risky actions gated · kill switch defined · no tool installed/required by default · evidence/UNVERIFIED labels on platform claims. Bot designs additionally: permission scopes + whitelist + escalation + no-secret-exposure verified.
