# Scale tiers (2026-11-21)

The tier is declared in the plan and binds every later choice. These rows are starting points from the pack's practice, not measured thresholds; adjust them in the plan with a reason.

| Tier | Who | Implications (candidates, not defaults) |
|---|---|---|
| solo | one user, usually the builder | local or single server; SQLite is a fair candidate; no multi-tenant auth; backups by copying the file |
| team | up to about 50 known users | one region; a managed Postgres or SQLite with replication; simple auth (magic link, SSO of the org); one deploy target |
| small SaaS | up to a few thousand monthly users | managed Postgres; real auth with sessions and MFA option; background jobs; error tracking; preview deploys; a monolith |
| large SaaS | tens of thousands and up | read replicas or caching layer; CDN; queue and worker tier; tracing; on-call; consider splitting services only where a team or a load profile demands it |
| regulated | any size with PCI, HIPAA, GDPR-heavy or government data | audit trail per write; encryption at rest and in transit with key management; access reviews; a decision record for every data flow; compliance owner named |

Rules:

- Start as a monolith (Fowler, MonolithFirst): service boundaries are hard to draw before the domain is understood.
- A tier change is itself a decision record.
- "We might need it at scale" is not a reason above the declared tier; write it under "later" with the trigger that would bring it in (a measured load, a customer requirement).
