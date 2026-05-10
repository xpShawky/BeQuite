# System Patterns: {{PROJECT_NAME}}

> The architecture, the recurring design patterns, and the ADR index. The single place where the question "how does this system actually work?" gets a complete answer.
>
> Updated whenever a new pattern emerges or an ADR lands. Linked from `plan.md` for each feature.

---

## 1. The high-level shape

A diagram (ASCII or external link to a Mermaid / draw.io / Excalidraw asset). Keep it accurate; an out-of-date diagram is worse than no diagram.

```
{{HIGH_LEVEL_DIAGRAM}}
```

## 2. The seams

The boundaries that matter. For each seam, list:

- The contract (function signatures, HTTP endpoints, message schemas, table schemas).
- The owner (which team / persona / agent owns the seam's evolution).
- The compatibility policy (semver-strict, in-flight rolling, breaking-with-deprecation-window).

| Seam | Contract location | Owner | Policy |
|---|---|---|---|
| | | | |

## 3. Recurring design patterns

The patterns this codebase uses repeatedly, with one-line "why this and not that" rationale.

- **{{PATTERN_NAME}}** — used at: `{{LOCATIONS}}`. Rationale: {{RATIONALE}}. Anti-pattern: {{ANTI_PATTERN}}.

## 4. State management

Where state lives, how it propagates, what's authoritative for what.

- **System of record for {{ENTITY}}:** {{SOURCE}}
- **Caches:** {{CACHES}} (with invalidation strategy per cache)
- **Background jobs:** {{JOBS}} (queue, worker, retry policy)

## 5. Cross-cutting concerns

| Concern | Strategy | Where it lives |
|---|---|---|
| Auth | | |
| Authz | | |
| Logging | | |
| Tracing / observability | | |
| Errors | | |
| Rate limiting | | |
| Feature flags | | |
| i18n | | |

## 6. The ADR index

Every architectural decision lives at `.bequite/memory/decisions/`. This is the index.

| ADR | Title | Status | Touches Iron Law(s) | Touches Doctrine(s) |
|---|---|---|---|---|
| ADR-001-stack | | | | |

(Auto-regenerable via `bequite memory show adr-index`.)

## 7. The receipts

Every implementation phase emits a signed receipt at `.bequite/receipts/<sha>-<phase>.json`. The chain proves the project's history is reproducible.

- **Latest receipt:** `{{LATEST_RECEIPT_PATH}}`
- **Receipt count:** `{{RECEIPT_COUNT}}`
- **Verification:** `bequite verify-receipts`

## 8. Known sharp edges

The places future engineers will trip. Document them so the trip doesn't ruin a sprint.

- {{SHARP_EDGE_1}}
- {{SHARP_EDGE_2}}
