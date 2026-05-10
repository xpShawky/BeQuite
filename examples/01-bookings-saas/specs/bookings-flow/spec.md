# Spec — Bookings flow

> Phase 2 (Plan + Contracts) artifact. Technology-agnostic spec; the implementation choices live in ADR-001-stack.md.

## Personas

1. **Customer** — books appointments at a tenant's resources. Self-serve sign-up.
2. **Admin** — configures availability, manages customers, views the bookings dashboard.
3. **Tenant owner** — invites admins; configures branding + business hours; sees usage / billing.

## Primary value-prop

A customer can find an available slot and book it in **≤ 30 seconds** without account creation friction.

## Flows

### Flow 1 — Customer signs up + books
1. Land on `/`. Hero CTA: "Book an appointment".
2. Pick a tenant (when multi-tenant; for example: barber shop).
3. Pick a resource (e.g. specific stylist).
4. Pick a date + time slot.
5. Email + name (no password — magic link auth via Better-Auth).
6. Confirm.
7. Email arrives with calendar invite.

**Acceptance:** end-to-end test books a slot, asserts:
- Slot disappears from availability after booking.
- Confirmation email triggered (verified via Mailhog mock in test).
- New customer record visible in admin dashboard.

### Flow 2 — Admin manages availability
1. Sign in as admin → `/admin`.
2. Click "Resources" → pick a resource.
3. Click "Availability" tab.
4. Edit weekly hours (Mon-Sun) + holiday exceptions.
5. Save.

**Acceptance:** customer flow respects updated availability. Smoke test: edit Mondays to closed → customer can't book Monday slots.

### Flow 3 — Admin views bookings dashboard
1. Sign in as admin → `/admin/bookings`.
2. See: today's bookings, this-week's bookings, customer search.
3. Click a booking → see customer + slot detail.
4. Optional: cancel booking → triggers customer notification.

### Flow 4 — Tenant owner invites admin
1. Sign in as owner → `/admin/team`.
2. Invite by email → admin receives magic link.
3. Once accepted, admin role is granted (RBAC via Better-Auth).

## Non-goals (deferred)

- Multi-resource booking (booking a stylist + a chair simultaneously).
- Recurring appointments.
- Custom intake forms per resource.
- Payment processing.
- Mobile native apps.

## Constraints (binding)

- **Article V scale honesty**: declared 5,000 MAU tier; implementation must not synchronously process emails in-process at scale. Use a queue (Inngest / Trigger.dev / Supabase Cron).
- **Article IV security**: auth via Better-Auth; never roll-your-own JWT; HTTPS only; CSP scaffolded.
- **Doctrine Rule 5**: no gray-on-color; axe-core gate must pass.
- **Doctrine Rule 7**: works at viewport 360 px and 1440 px.
- **Doctrine Rule 12**: Playwright walks for both admin + customer roles.
- **PII handling**: customer email + name are PII. Apply EU-GDPR Doctrine when shipping to EU customers (future iteration).

## Skeptic kill-shot

> "What happens when a customer tries to book a slot that just got booked by someone else 200ms before they hit submit?"

**Answer (encoded in implementation):** the booking endpoint takes a row-level lock on the slot record + checks availability inside the transaction. On conflict, returns 409 + a friendly "this slot just got booked, please choose another" toast. Tested via concurrent-booking integration test.

## Cross-references

- ADR-001 stack: `../../.bequite/memory/decisions/ADR-001-stack.md`
- Plan: `plan.md`
- Phases: `phases.md`
- Tasks: `tasks.md`
- Doctrine: `../../../skill/doctrines/default-web-saas.md`
