# Example 01 — Bookings SaaS

> A small-scale bookings application demonstrating BeQuite's `default-web-saas` Doctrine end-to-end.

## What this example is

A multi-tenant bookings application: customers can browse appointments, book a slot, see their bookings; admins can configure availability, manage customers, view bookings dashboard.

This is a **scaffold + spec'd walkthrough**, not a production-quality app. The point is to demonstrate the BeQuite tree shape + Doctrine wiring + per-phase artifact discipline. Production-grade implementation is a downstream exercise (or a v1.x example refinement).

## Stack (decided in P1; ADR-001)

| Layer | Choice | Why |
|---|---|---|
| Frontend framework | Next.js (App Router) | Default for unknown; SEO + edge ready; React talent pool widest. |
| UI components | shadcn/ui v3+ + tweakcn theme | Doctrine Rule 3 sourcing order; full ownership. |
| Styling | Tailwind v4 + `tokens.css` | Doctrine Rule 1 (tokens-only). |
| Backend | Hono on Bun | Smallest edge-friendly TS backend. |
| Database | Supabase (Postgres + RLS) | Built-in auth + storage; SOC 2; scale-to-pro path. |
| Auth | Better-Auth | MIT, self-hosted, 2FA / passkeys / orgs / RBAC; Doctrine Rule 9. |
| Hosting | Vercel | Default Next.js; Pro extends timeout to 800s. |
| Pooling | Supavisor (Supabase) | Replaces PgBouncer there. |
| Validation | Zod | Doctrine Rule 11 (input validation everywhere). |
| Forms | React Hook Form + Zod resolver | |
| State | Zustand + TanStack Query | Server state via TQ; client state via Zustand. |
| i18n | next-intl | App-router-aware. |
| Testing | Playwright + Vitest + axe-playwright | Doctrine Rule 12 + Rule 8 (axe-core gate). |
| Observability | Sentry (review BSL/FSL license) + PostHog | |

## Phases (decomposed in P3)

### P0 — Discovery
- Product owner interview: what bookings, who books, who admins, what data lives where.
- Competitor scan: Calendly / Cal.com / Acuity / SavvyCal.
- Output: `docs/PRODUCT_REQUIREMENTS.md`.

### P1 — Stack ADR
- See ADR-001-stack.md.
- `bequite freshness` ran against each candidate; all green.

### P2 — Plan + Contracts
- API contracts (Zod schemas shared between Next.js + Hono).
- DB schema + RLS policies (deny-by-default per Doctrine Rule 10).
- Data model: User, Tenant, Resource, Slot, Booking, Customer.

### P3 — Phases
- phase-1: Foundation (auth + RLS scaffold + tokens.css).
- phase-2: Customer flow (browse → book).
- phase-3: Admin flow (manage availability + bookings dashboard).
- phase-4: Notifications (email confirmations).
- phase-5: Polish + Verify (Playwright + axe + smoke).

### P4 — Tasks
Per phase, atomic tasks ≤5 min each. See `specs/bookings-flow/tasks.md`.

### P5 — Implementation
Per task: read spec → implement → format → test → commit. Receipt emitted per task.

### P6 — Verify
- `bequite verify` runs:
  - Lint + typecheck (eslint + tsc).
  - Unit + component (Vitest).
  - Playwright admin-walk + user-walk at viewport 360 + 1440.
  - axe-core gate (zero WCAG AA violations).
  - Smoke: every public endpoint via curl.
  - Secret scan + audit + freshness.
- Receipts archived per gate.

### P7 — Handoff
See `HANDOFF.md`.

## How to walk this example yourself

```bash
# From BeQuite repo root:
cd examples/01-bookings-saas/

# Inspect the trees:
ls .bequite/memory/                    # 6 Memory Bank files
ls .bequite/memory/decisions/          # ADR-001 + future ADRs
ls specs/bookings-flow/                # spec / plan / phases / tasks
cat HANDOFF.md                          # the handoff target
cat state/recovery.md                   # how to resume

# After receipt key generated (v0.7.1+):
python -m cli.bequite keygen --repo .   # generates .bequite/keys/public.pem

# Run BeQuite gates (some will be N/A because no code yet):
PYTHONPATH=../../cli python -m bequite.verify --mode safe
```

## What's deliberately NOT shipped here

- Actual application code (apps/web, apps/api). The scaffold is the contract; production code is downstream.
- Live Supabase project + Clerk app (requires per-developer credentials).
- Real screencast (deferred to v1.0.0 release prep).
- CI workflows specific to this example (covered by v0.9.1 e2e harness).

## Cross-references

- Doctrine: `../../skill/doctrines/default-web-saas.md`
- Frontend stack reference: `../../skill/references/frontend-stack.md`
- Frontend MCPs reference: `../../skill/references/frontend-mcps.md`
- Tokens template: `../../skill/templates/tokens.css.tpl`
- Playwright config template: `../../skill/templates/playwright.config.ts.tpl`
- Walkthrough templates: `../../skill/templates/tests/walkthroughs/`
