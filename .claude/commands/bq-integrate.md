---
description: Integration Blueprint (C7). Turn API docs, OpenAPI specs, or SDK docs into a working integration blueprint — auth flow, endpoint map, error matrix, retry/idempotency, rate limits, test plan, example skeleton. Never invents undocumented endpoints; marks unknowns UNVERIFIED. Tool-neutral; installs nothing.
---

# /bq-integrate — API docs → integration blueprint (C7)

<!-- bq:contract -->
> **Every run follows the contract** (`.claude/bequite/docs/architecture/COMMAND_EXECUTION_CONTRACT.md`):
> 1. **Skills first:** announce the `Skill Selection:` block before any plan, edit or tool call for the task.
> 2. **Resolve the work:** read `.bequite/ACTIVE.md`; use `.bequite/work/<id>/`, or create the next work folder if this is new work (`/bq-work`).
> 3. **Gates:** project gates in `.bequite/state/WORKFLOW_GATES.md`, work gates in `work/<id>/gates.md`. Refuse and name the missing gate.
> 4. **Plan first:** non-trivial work gets a plan the user approves before output. Hard human gates always wait for a yes.
> 5. **Evidence:** every check goes to `work/<id>/evidence.md` (command + exit code + output) or is marked `UNVERIFIED:`.
> 6. **Write back:** `work/<id>/log.md`, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, and `.bequite/state/MISTAKE_MEMORY.md` when a lesson surfaced.
> 7. **Finish** with the Next Command Recommendations block.
<!-- /bq:contract -->

Full spec: `.claude/bequite/docs/specs/INTEGRATION_BLUEPRINT.md`. Follows the 12-step execution contract including skill routing, Confidence Forecast, and the step-12 router block.

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
