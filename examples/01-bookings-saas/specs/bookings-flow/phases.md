# Phases — Bookings flow

> Decomposition into atomic phases. Each phase is committable and testable on its own. Per the build plan, exit each phase with: artifact + Skeptic kill-shot answered + verify-gate green + receipt emitted + tagged commit.

## phase-1 — Foundation

**Goal:** project boots; auth scaffolded; tokens.css + design system present; CI green on a hello-world page.

**Tasks** (~5 min each):
- Scaffold `apps/web` (Next.js App Router) + `apps/api` (Hono on Bun).
- Drop in `tokens.css` from BeQuite template (record font choice in comment).
- Wire Better-Auth (email + magic link).
- Scaffold Supabase migrations (deny-by-default RLS).
- Hello-world `/` page with one shadcn button + one tokens-only color.
- CI: lint + typecheck + axe-on-`/`.

**Exit gate:** `bequite verify --mode safe` green. Skeptic kill-shot: "What happens if Supabase auth is unreachable on first load?" Answer: graceful degradation to anonymous-browse.

## phase-2 — Customer flow

**Goal:** end-to-end customer can browse + book.

**Tasks:**
- Models (Zod + Supabase migrations): Tenant, Resource, Slot, Booking, Customer.
- API endpoints (Hono):
  - `GET /tenants/:slug` — public
  - `GET /tenants/:slug/resources` — public
  - `GET /resources/:id/slots?from=&to=` — public, returns available slots
  - `POST /bookings` — auth (magic link); takes row lock; returns 201 or 409
  - `GET /me/bookings` — auth
- Web pages:
  - `/[tenant]/book` — slot picker
  - `/[tenant]/book/confirm` — final confirm
  - `/me/bookings` — customer's bookings
- Email confirmation via Resend (queued via Inngest — Article V scale honesty).
- Playwright user-walk per `tests/walkthroughs/user-walk.md`.

**Exit gate:** Playwright user-walk green at viewport 360 + 1440. axe-core green. Concurrent-booking conflict test green.

## phase-3 — Admin flow

**Goal:** admin can configure availability + view bookings.

**Tasks:**
- API endpoints (Hono, admin-RBAC-gated):
  - `PUT /resources/:id` — update resource
  - `PUT /resources/:id/availability` — weekly hours + exceptions
  - `GET /admin/bookings?from=&to=&customer=` — search
  - `DELETE /bookings/:id` — cancel + notify
- Web pages:
  - `/admin` — dashboard
  - `/admin/resources` — resource manager
  - `/admin/resources/:id/availability` — availability editor
  - `/admin/bookings` — bookings table
  - `/admin/team` — invite admins
- RBAC via Better-Auth (`role: 'owner' | 'admin' | 'customer'`).
- Playwright admin-walk per `tests/walkthroughs/admin-walk.md`.

**Exit gate:** admin-walk green. Cross-walk verification (admin sees customer's booking from phase-2).

## phase-4 — Notifications

**Goal:** confirmation + reminder emails fire reliably.

**Tasks:**
- Email templates (Resend + React Email).
- Inngest functions:
  - `customer.booking.confirmed` → send confirmation
  - `customer.booking.reminder` → send 24h before slot
  - `admin.booking.cancelled` → notify admin when customer cancels
- Mailhog mock for tests; real Resend for staging/prod.
- Idempotency keys (booking_id) so retries don't double-send.

**Exit gate:** integration test sends + receives in Mailhog mock. Inngest dashboard shows zero retries on happy path.

## phase-5 — Polish + Verify

**Goal:** ship-ready quality.

**Tasks:**
- `bequite design audit` — walk Impeccable's 23 commands; remediate findings.
- Empty / loading / error states for every interactive component (Impeccable `harden`).
- a11y: keyboard-tab through every page; focus rings visible; aria-live for errors.
- Performance: Lighthouse CI gate (95+ across all pages).
- Security: OWASP Top 10 spot-check via `bequite audit` Article-V rules.
- Smoke: `scripts/smoke.sh` per `skill/templates/scripts/smoke.sh.tpl`.

**Exit gate:** all `bequite verify` gates green; `bequite design audit` zero block-class findings; Lighthouse CI 95+.

## phase-6 — Verify (cross-cutting)

`bequite verify --mode safe` runs the full validation mesh:
- Lint + typecheck (eslint + tsc).
- Unit + component (Vitest).
- Playwright admin-walk + user-walk + axe walks at viewport 360 + 1440.
- Smoke (curl every public endpoint per spec).
- Secret scan + audit + freshness.
- Receipts archived per gate.

## phase-7 — Handoff

`bequite handoff` generates `HANDOFF.md`:
- Engineer-facing: how to clone + boot + deploy + add a feature.
- Vibe-handoff: non-engineer summary of what the app does + how to operate it.
- Screencast checklist (deferred to v1.0.0 release prep).

## Receipt chain

Every phase exit emits a signed receipt (v0.7.1+). The chain is committed at `.bequite/receipts/`. `bequite verify-receipts` validates the chain on every push.

## Skeptic kill-shots per phase

- phase-1: "Without auth, can someone browse a tenant's resource list and learn the customer roster from RLS leakage?" Answer: RLS deny-by-default; tested.
- phase-2: "Concurrent booking on the same slot — race condition?" Answer: row lock + 409 fallback; tested.
- phase-3: "Admin sees PII (customer email). Is it logged anywhere unexpected?" Answer: no; logger redacts via Article-V rule pack; spot-check via `bequite audit`.
- phase-4: "Email queue backlog if Resend is down?" Answer: Inngest's retry + dead-letter queue.
- phase-5: "Mobile keyboard on viewport 360 — does the slot picker stay usable?" Answer: tested in Playwright mobile project.
