# Automation Engine — `/bq-automation` (C12) — alpha.24

Turn a workflow or bot idea into a **tool-neutral automation blueprint**. Command: `bq-automation.md`. Skill: `bequite-automation-engineer` (distilled from the retired v2 automation-architect + ai-automation references; see LEGACY_SKILL_FOLDER_AUDIT). **Installs nothing — designs only.**

## Why a command (not an argument)

Distinct recurring workflow (triggers→actions→reliability→security), its own 10-artifact set, its own skill, reusable across projects and by `/bq-local-business`. Bots are a **profile** (`bot`), not a separate command — same engine, extra safety section.

## Outputs — `.bequite/automation/`

AUTOMATION_BRIEF · TRIGGER_MAP · ACTION_MAP · DATA_FLOW · TOOL_DECISION · IDEMPOTENCY_PLAN · RETRY_AND_FAILURE_PLAN · SECURITY_AND_SECRETS · TEST_PLAN · HANDOFF (created on first run).

## Discipline (mandatory in every blueprint)

Official-API-first → idempotency keys → duplicate-trigger dedup (by event ID) → bounded retries + backoff → dead-letter/failure handling → webhook replay protection → secrets in env/manager only (never inline/logged; R3 gate) → logs + audit trail → dry-run + manual-approval gates for risky actions (money/mass-message/delete = hard human gate) → rate limits → alerting → kill switch. Tool candidates (never defaults): n8n · Make · Zapier · Activepieces · Pipedream · Temporal · Inngest · Trigger.dev · cron · GitHub Actions · queues/workers · Playwright (API-less + ToS-permitting only).

## Bot safety (the `bot` profile)

Telegram/Discord/WhatsApp(official API only)/web/admin: permission scopes · command whitelist · user identity · abuse/rate limits · logs · escalation-to-human · no secret exposure · no destructive command without confirm.

## Honesty + neutrality

UNVERIFIED for unconfirmed platform behavior; every tool is a candidate with a decision rationale; no install, no provider keys, no daemon. **Built alpha.24 — NOT live-tested.**
