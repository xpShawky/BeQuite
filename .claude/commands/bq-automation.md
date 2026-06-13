---
description: Automation Engine (C12). Turn a workflow or bot idea into a tool-neutral automation blueprint — trigger map, action map, data flow, tool decision (official-API-first), idempotency + retry/failure plan, secret handling, test plan, handoff. Bot profiles (Telegram/Discord/WhatsApp/web/admin) via the `bot` profile. Installs nothing; designs only.
---

# /bq-automation — workflow & bot automation blueprints (C12)

Full spec: `docs/specs/AUTOMATION_ENGINE.md`. Follows the 12-step execution contract. Skill: `bequite-automation-engineer` (+ scraping-automation for web triggers, backend-architect for services). **Tool-neutral — no tool installed or required by default.**

## Syntax

```
/bq-automation "<workflow in plain words>"          ← workflow blueprint
/bq-automation bot "<bot purpose + platform>"       ← bot profile
/bq-automation workflow "<trigger → steps → action>"
/bq-automation local-business "<business>"          ← SMB automation set (also reachable via /bq-local-business)
```
Examples: `/bq-automation "Telegram alert when a tracked page changes"` · `/bq-automation "new Shopify order → Google Sheet → customer WhatsApp message"` · `/bq-automation bot "Telegram bot for course students"` · `/bq-automation workflow "lead form → CRM → email follow-up"`.

## Steps (after contract steps 1–7)

1. **Brief** — `AUTOMATION_BRIEF.md`: goal, source(s), target(s), volume, who maintains it, risk level (money/mass-message/delete = hard gate).
2. **Map** — `TRIGGER_MAP.md` (events + dedupe-by-event-ID) · `ACTION_MAP.md` (each action + idempotency key) · `DATA_FLOW.md` (source→transform→target, what data, PII?).
3. **Decide tools** — `TOOL_DECISION.md`: official-API-first; pick a candidate (n8n/Make/Zapier/Activepieces/Temporal/Inngest/cron/GH Actions/queue/custom worker) per the 10 tool-neutrality questions; rationale + why-not-others. Nothing installed.
4. **Resilience** — `IDEMPOTENCY_PLAN.md` + `RETRY_AND_FAILURE_PLAN.md` (bounded retries + backoff + dead-letter + webhook replay protection + kill switch).
5. **Security** — `SECURITY_AND_SECRETS.md` (env/secret-manager only, never inline/logged; risky actions gated; rate limits; audit trail).
6. **Test + handoff** — `TEST_PLAN.md` (dry-run, duplicate-trigger, failure-path, idempotency tests) + `HANDOFF.md`.

**Bot profile** adds: permission scopes · command whitelist · user identity · abuse/rate limits · logs · escalation-to-human · never-expose-secrets · no destructive command without confirm. WhatsApp = official Business API/approved provider only.

## Writes

`.bequite/automation/{AUTOMATION_BRIEF,TRIGGER_MAP,ACTION_MAP,DATA_FLOW,TOOL_DECISION,IDEMPOTENCY_PLAN,RETRY_AND_FAILURE_PLAN,SECURITY_AND_SECRETS,TEST_PLAN,HANDOFF}.md` (created on first run) + AGENT_LOG + LAST_RUN.

## Next Command Recommendations (typical)

Required next: **W1.4 `/bq-plan`** if implementation follows (slot into the codebase). Set: C7 `/bq-integrate` (API specifics) · W2.3 `/bq-feature` (build the admin/worker) · C11 `/bq-offer` (if automation is a sellable service) · C13 `/bq-local-business`. Do not run yet: any live automation touching money/mass-messages/deletes without an explicit human-approval gate (hard gate).
