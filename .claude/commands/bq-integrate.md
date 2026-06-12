---
description: Integration Blueprint (C7). Turn API docs, OpenAPI specs, or SDK docs into a working integration blueprint — auth flow, endpoint map, error matrix, retry/idempotency, rate limits, test plan, example skeleton. Never invents undocumented endpoints; marks unknowns UNVERIFIED. Tool-neutral; installs nothing.
---

# /bq-integrate — API docs → integration blueprint (C7)

Full spec: `docs/specs/INTEGRATION_BLUEPRINT.md`. Follows the 12-step execution contract including skill routing, Confidence Forecast, and the step-12 router block.

## Syntax

```
/bq-integrate "<API docs URL | OpenAPI spec path>" [stack=<target stack>] [workflow="<desired flow>"]
```

## Preconditions / gates

`BEQUITE_INITIALIZED`. Auth details accepted as **types/scopes only — never credential values** (secret handling = hard human gate).

## Steps (after contract steps 1–7)

1. **Ground in docs** — fetch/read the API docs or spec. Every claim in the blueprint cites a doc section. No doc ⇒ no claim; probable-but-undocumented behavior is marked **`UNVERIFIED`** with reasoning.
2. **Map** — `ENDPOINT_MAP.md` (used endpoints only, with citations) · `AUTH_FLOW.md` (key storage, scopes, rotation notes, webhook signature verification) · `ERROR_MATRIX.md` (status × cause × app response).
3. **Resilience plan** — `RETRY_IDEMPOTENCY_PLAN.md` + `RATE_LIMIT_PLAN.md` (documented limits or UNVERIFIED + safe defaults).
4. **Test + skeleton** — `TEST_PLAN.md` (ERROR_MATRIX rows → test cases; contract tests) + `EXAMPLE_SKELETON.md` (shape only; client library chosen per the 10 decision questions — nothing installed).
5. **Blueprint** — `INTEGRATION_BLUEPRINT.md` ties it together with per-section confidence, failure modes, security concerns.

## Writes

`.bequite/integrations/{INTEGRATION_BLUEPRINT,AUTH_FLOW,ENDPOINT_MAP,ERROR_MATRIX,RETRY_IDEMPOTENCY_PLAN,RATE_LIMIT_PLAN,TEST_PLAN,EXAMPLE_SKELETON}.md` + AGENT_LOG + LAST_RUN.

## Skill routing (auto)

backend-architect · security-reviewer · testing-gate · anti-hallucination · researcher (doc fetch).

## Next Command Recommendations (typical)

Required next: **W1.4 `/bq-plan`** (slot the blueprint into the codebase) — can auto-run: yes. Set: W2.3 `/bq-feature` (build) · W3.1 `/bq-test from-spec` (matrix → tests) · W4.1 `/bq-verify`. Do not run yet: W2.3 before the blueprint's UNVERIFIED items are resolved or accepted as risks.
