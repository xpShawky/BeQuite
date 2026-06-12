# Integration Blueprint — `/bq-integrate` (C7) — alpha.22

Turn API docs / OpenAPI specs / SDK docs + integration requirements into a working integration blueprint for the target stack.

## Inputs

API docs URL · OpenAPI spec · SDK docs · auth details (types only — **never credential values**) · target app stack · desired workflow.

## Hard rules

1. **Never invent undocumented endpoints.** Everything in ENDPOINT_MAP cites the doc section it came from.
2. Undocumented-but-probable behavior is marked **`UNVERIFIED`** with the reason.
3. Every blueprint includes: confidence per section, failure modes, security concerns (key storage, scopes, webhook signature verification, PII flow).
4. Tool-neutral: no SDK installed by default; EXAMPLE_SKELETON shows the shape, the 10 decision questions pick the client library.

## Outputs — `.bequite/integrations/`

INTEGRATION_BLUEPRINT · AUTH_FLOW · ENDPOINT_MAP · ERROR_MATRIX · RETRY_IDEMPOTENCY_PLAN · RATE_LIMIT_PLAN · TEST_PLAN · EXAMPLE_SKELETON (per integration; created on first run).

## Routing

Skills: backend-architect + security-reviewer + testing-gate + anti-hallucination (doc-grounding) + researcher (docs fetch). Next: W1.4 plan → W2.3 feature → W3.1 test (ERROR_MATRIX rows become test cases) → W4.1 verify. Watch-item: V1 "Data-to-Product Builder" is parked with a merge-watch on this command (shape decisions §V1 #8).
