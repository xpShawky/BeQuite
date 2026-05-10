# Progress: {{PROJECT_NAME}}

> The evolution log. What works, what's left, what changed and why. Updated at the end of every task; phase-snapshotted at the end of every phase.
>
> This file is the audit trail. If the project is ever handed off, this is the file the new owner reads first after `projectbrief.md`.

---

## Current state

- **Sub-version:** `{{CURRENT_VERSION}}`
- **Constitution version:** `{{CONSTITUTION_VERSION}}`
- **Active doctrines:** `{{ACTIVE_DOCTRINES}}`
- **Phases shipped:** `{{PHASES_SHIPPED}}`  (P0 / P1 / P2 / P3 / P4 / P5 / P6 / P7)
- **Open features:** `{{OPEN_FEATURES_COUNT}}`
- **Receipt chain integrity:** `{{RECEIPT_CHAIN_STATUS}}`  (intact / broken — link to incident)

## What works (verified, with receipts)

A list of features that have been built AND verified (Article II — verification before completion). Each line links to the receipt JSON that proves it.

- ✅ {{FEATURE_NAME}} — `{{RECEIPT_PATH}}`
- ✅ {{FEATURE_NAME}} — `{{RECEIPT_PATH}}`

## What's left (in priority order)

The roadmap. Pulled from `specs/<feature>/tasks.md` files; rolled up here for at-a-glance.

| Feature | Phase | Owner | ETA | Blocking |
|---|---|---|---|---|
| | | | | |

## What's uncertain

Where the team lacks confidence. Tagged so future ADRs can address them.

- {{UNCERTAIN_1}} — needs ADR? `{{ADR_LINK_OR_NULL}}`
- {{UNCERTAIN_2}}

## Evolution log (newest first)

Append-only. Each entry: timestamp, sub-version, one-line summary, link to receipt.

```
{{EVOLUTION_LOG}}
```

## Decisions made (newest first)

ADRs landed, with the reason. Cross-references `.bequite/memory/decisions/`.

```
{{DECISIONS_LOG}}
```

## Failures and learnings

When something failed, what we learned. Promotes "we won't repeat this" institutional memory. Each entry: date, what failed, root cause, mitigation, ADR-or-Doctrine-amendment if any.

```
{{FAILURES_LOG}}
```
