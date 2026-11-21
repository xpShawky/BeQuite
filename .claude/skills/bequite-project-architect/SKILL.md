---
name: bequite-project-architect
description: Use when a plan needs structure decisions, such as picking or changing a stack, splitting into services, choosing a database or host, declaring the scale tier, writing an ADR, or drawing the file and phase plan. Builds an options board, checks every candidate's current version in its registry that day, and records the choice as a short decision record with a way to confirm it.
last_verified: 2026-11-21
sources:
  - https://adr.github.io/madr/ (read 2026-11-21) MADR 4.0.0 sections incl. Confirmation
  - https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions (read 2026-11-21) Nygard ADR
  - https://c4model.com/ (read 2026-11-21) context and container diagrams
  - https://www.thoughtworks.com/radar (read 2026-11-21) Vol 35, agent instruction bloat, progressive disclosure
  - https://martinfowler.com/bliki/MonolithFirst.html (read 2026-11-21) monolith first
  - https://registry.npmjs.org/ (read 2026-11-21) current versions of the common web stack
  - https://www.postgresql.org/docs/current/ (read 2026-11-21) current PostgreSQL major
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Edit, Write
---

# bequite-project-architect

Architecture mistakes are the expensive kind: they are made early, from memory, and paid for over years. This skill makes each structural choice from the project's real constraints and today's facts, lists the options it rejected, and writes it down short enough that someone reads it.

## When to use

- `/bq-plan`: stack, scale tier, architecture sketch, file plan, phase plan with acceptance evidence.
- `/bq-research` and `/bq-scope`: what fits this scale; what is out.
- `/bq-uiux-variants` or a feature that needs a structural change (a router, a queue, a new service): write a decision, do not install.

Not for: the inside of one layer (`bequite-backend-architect`, `bequite-database-architect`, `bequite-devops-cloud`), UI design.

## Procedure

1. **Read what exists.** `.bequite/audits/DISCOVERY_REPORT.md` if present, the manifests, the deploy config, existing ADRs. An existing stack is a constraint; replacing it needs its own decision.
2. **Declare the scale tier** and let it bind (`references/scale-tiers.md`): solo, team, small SaaS, large SaaS, regulated. Do not build above it; do not cap below it.
3. **Ask the ten questions** (project type, real problem, scale, constraints, existing stack, UX, failure risks, proven tools, overkill tools, least complexity). Write one line per answer.
4. **Options board.** For each open choice list 2 to 4 candidates, including "keep what we have" and the simplest one (a monolith, SQLite, a cron job, a static site). For each: fit, cost, risk, team familiarity, lock-in, licence.
5. **Check each candidate today.** Version and release date from its registry (npm, PyPI, crates, the vendor's docs), licence, last release, maintenance signals. A candidate that cannot be verified in this session is marked `UNVERIFIED:` and cannot be the pick. Flag AGPL and GPL for closed-source products.
6. **Pick and record** a decision (`references/adr-template.md`, MADR-shaped): context, drivers, options, outcome, consequences, and a **confirmation** line, meaning how and when we check the decision holds (a load test, a cost after one month, a migration that ran).
7. **Sketch** a system-context and a container view (C4 levels 1 and 2) as text or Mermaid. Deeper levels only when a reader needs them.
8. **File plan**: every path the work creates or changes, marked NEW, MODIFIED or DELETED, with one line each, specific enough to grep.
9. **Phase plan**: each phase ends in testable acceptance evidence ("sign-up end-to-end test passes and a row appears in `users`"), not "auth works".
10. **Keep it short.** Plans and memory files that grow long stop being read by people and by agents (the radar's "agent instruction bloat"). Put detail in linked files and load it when needed.

## Worked example (real registry check, 2026-11-21)

The old version of this skill shipped a "2026 known-good defaults" table. Checking it against the registries today:

```
next          16.4.6   2026-11-09   (table said "Next.js 15")
react         19.3.1   2026-10-14
tailwindcss   4.3.5    2026-11-06   (table said "v4 when stable": stable since, now 4.3)
vitest        5.1.1    2026-11-18
vite          8.3.8    2026-11-11
astro 7.4.13 · @sveltejs/kit 3.4.0 · hono 4.13.19 · drizzle-orm 0.45.4 · PostgreSQL 19 (docs, released 2026-11-19)
```

Two of the table's version claims were wrong within months. Decision recorded for this skill: **no defaults table**; every plan runs step 5 on the day and writes the versions it saw into the plan. Confirmation (proposed to the skill-auditor owner, not built yet): `/bq-skill-audit` flags any version number in a skill older than its `last_verified` window.

## Quality gate

- The scale tier is declared and every choice is consistent with it.
- Every pick has at least one rejected alternative with a reason, and a confirmation line.
- Every named package or service shows a version, date and licence checked in this session.
- The file plan lists real paths; the phase plan's evidence is testable.
- Nothing was installed or migrated during planning.

## Boundaries

- Architecture changes are a hard human gate: the plan proposes, the user approves.
- No stack is a default. Names in this skill and its references are examples.
- Never claim a version, price or limit from memory; check it or write `UNVERIFIED:`.

## References (load on demand)

- `references/scale-tiers.md`: tiers with architectural implications.
- `references/adr-template.md`: the decision template and a filled example.
