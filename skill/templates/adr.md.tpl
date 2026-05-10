---
adr_id: {{ADR_ID}}                # e.g. ADR-001-stack
title: {{ADR_TITLE}}
status: {{ADR_STATUS}}            # proposed | accepted | superseded | deprecated
date: {{ADR_DATE}}                # ISO 8601 — UTC
deciders: [{{DECIDERS}}]          # names / handles of who signed off
supersedes: {{SUPERSEDES}}        # null, or `ADR-NNN-<slug>@<version>` of the ADR this replaces
superseded_by: {{SUPERSEDED_BY}}  # null, or the ADR-id that replaces this one
constitution_version: {{CONSTITUTION_VERSION}}  # which Constitution version this ADR was made under
related_articles: [{{RELATED_ARTICLES}}]        # I, II, III, IV, V, VI, VII (Iron Laws this ADR touches)
related_doctrines: [{{RELATED_DOCTRINES}}]
---

# {{ADR_ID}}: {{ADR_TITLE}}

> Status: **{{ADR_STATUS}}** · Date: {{ADR_DATE}} · Decided by: {{DECIDERS}}

## Context

What problem are we solving? What forces — technical, economic, organisational, regulatory — are at play? Cite specific evidence (Memory Bank entries, research findings, prior ADRs, scale tier from `plan.md`, threat model from `SECURITY.md`). Quote, do not paraphrase, the constraints that bind this decision.

## Decision

What did we decide? Be specific:

- For stack choices: name the library + version; the alternatives considered; the freshness-probe verdict; the package-allowlist entry.
- For architectural choices: the boundary, the contract, the explicit non-goals.
- For policy choices: the rule, the scope, the enforcement mechanism (hook, audit rule, doctrine).

## Rationale

Why this decision over the alternatives? Trade-offs explicit. Cite:

- The applicable Iron Law(s) and Doctrine rule(s).
- The scale tier — does this decision support it?
- The freshness probe — was the candidate alive, supported, free of unfixed criticals, with the assumed pricing tier?
- The Skeptic's kill-shot question — what failure mode did we consider and accept?

## Alternatives considered

| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| | | | |

## Consequences

- **Positive:** what becomes easier, cheaper, safer, faster.
- **Negative:** what becomes harder, more expensive, riskier, slower.
- **Constitutional impact:** does this decision require an Iron Law amendment or a new Doctrine? If yes, link the proposal.
- **Refactoring path:** what would have to change to revisit this decision later (a superseding ADR is the formal path).

## Verification

How do we know this decision was applied correctly?

- Acceptance criteria (testable).
- Automated check (audit rule, contract test, lint rule).
- Receipt artifact (which receipt JSON proves this ADR is honoured).

## References

- Related ADRs: {{RELATED_ADRS}}
- External docs:
- Receipts:
- Memory Bank entries: `activeContext.md::{{SECTION}}`, `systemPatterns.md::{{SECTION}}`

## Amendments

```
{{AMENDMENTS_LOG}}
```
