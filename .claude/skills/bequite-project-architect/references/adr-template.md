# Decision record template (MADR 4.0.0 shape, with Nygard's status)

Save as `.bequite/decisions/ADR-NNN-<slug>.md` (or the project's own `docs/decisions/`). One decision per file. Short: a page or less.

```markdown
---
status: proposed | accepted | deprecated | superseded by ADR-MMM
date: YYYY-MM-DD
decision-makers: <names or roles>
---

# ADR-NNN: <short noun phrase>

## Context and problem statement
<two to four sentences: the situation and the question>

## Decision drivers
- <constraint or quality that matters, e.g. "one developer", "Arabic RTL first", "under $20 a month">

## Considered options
1. <option A, including "keep what we have">
2. <option B>
3. <the simplest option>

## Decision outcome
Chosen: <option>, because <the drivers it satisfies>.

### Consequences
- Good: ...
- Bad: ...

### Confirmation
<how and when we check the decision holds: a test, a measurement, a date>

## Pros and cons of the options
<one short block per option; versions and licences checked on YYYY-MM-DD>
```

## Filled example (from this pack, 2026-11-21)

```markdown
---
status: accepted
date: 2026-11-21
decision-makers: track C1C2
---
# ADR: Skills carry no stack-defaults table

## Context and problem statement
The architect skill listed "known-good defaults" with versions. On 2026-11-21 two of them were out of date (Next.js 16.4.6 current vs "15" in the table; Tailwind 4.3.5 stable vs "v4 when stable").

## Decision drivers
- Freshness: skills are re-verified every 120 days, packages ship monthly.
- Tool neutrality: the pack names candidates, not defaults.

## Considered options
1. Keep the table and refresh it each release.
2. Remove it; check registries during each plan.

## Decision outcome
Chosen: 2, because a plan-day check is always current and costs one registry call per candidate.

### Consequences
- Good: no stale versions shipped. Bad: each plan spends a few calls on checks.

### Confirmation
Proposed for the skill audit (not built yet): flag any version number in a skill whose `last_verified` is older than 120 days.
```
