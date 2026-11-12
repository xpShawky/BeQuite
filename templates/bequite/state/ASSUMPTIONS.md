# Assumptions

Things BeQuite is currently assuming about this project. Each entry includes evidence, confidence, and a sunset condition (when the assumption should be re-verified or invalidated).

**Read on:** every `/bq-plan`, `/bq-research`, `/bq-fix`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`, `/bq-auto` call
**Written by:** `/bq-discover`, `/bq-doctor`, `/bq-clarify`, `/bq-research`, and the user (manually)

---

## Why this file exists

Plans built on unstated assumptions break. Examples:

- Plan assumes the user has Docker installed — they don't.
- Plan assumes the project will hit < 5K MAU — it actually targets 500K.
- Plan assumes the dev DB is shared — it's actually per-PR.
- Plan assumes English-only — user is in Egypt + needs Arabic + RTL.
- Plan assumes Postgres — DBA mandates MySQL.

When an assumption is wrong, downstream work is wrong. This file makes assumptions visible so they can be challenged.

---

## Entry template

```markdown
## <ISO 8601 UTC> — <one-line assumption>

**Evidence:** <how we came to this conclusion>
**Confidence:** <high | medium | low>
**Source:** <user statement | DISCOVERY_REPORT | research | inferred>
**Sunset condition:** <what would invalidate this; when to re-verify>
**Affects:** <which plans / decisions depend on this>
```

---

## Entries (newest at top)

<!--
  Example:

  ## 2026-05-12T14:30Z — Project targets 5K MAU within 12 months
  **Evidence:** User answered "scale tier?" with "small_saas" during /bq-clarify
  **Confidence:** medium
  **Source:** user statement (no validated traction yet)
  **Sunset condition:** real MAU exceeds 1K → re-verify scale tier; or product pivots to enterprise → scale up
  **Affects:** IMPLEMENTATION_PLAN §5 (stack — Supabase free tier OK; PgBouncer not needed yet), §9 (no Redis cache in v1)
-->

(no assumptions recorded yet — populated as `/bq-discover`, `/bq-clarify`, `/bq-research` run)

---

## Categories

- **Scale** — user count, request volume, data volume
- **Stack** — assumed runtime / framework / DB / hosting choices
- **Team** — solo vs. team, time budget, expertise
- **Domain** — industry, regulations, region
- **User behavior** — assumed flows, mobile vs. desktop, accessibility needs
- **Performance** — assumed latency budgets, response times
- **Security** — threat model, compliance scope
- **Budget** — cost ceiling, paid vs. free tools

---

## Rules

- **Make assumptions explicit.** Don't bake unstated assumptions into a plan; surface them here first.
- **Confidence honestly.** "High" means user explicitly confirmed. "Medium" means inferred from research + plausible. "Low" means we're guessing.
- **Sunset condition concrete.** "Re-verify someday" is not concrete. "Re-verify when MAU exceeds 1K" is.
- **Cite affects.** Which plan section / decision depends on this assumption? When the assumption changes, that section / decision needs re-review.

---

## What this file is NOT

- Not a substitute for `/bq-research` (research gathers verified evidence; assumptions list unverified bets)
- Not a brain dump (one entry = one specific assumption with evidence)
- Not permanent (entries get sunset and invalidated as the project evolves)
