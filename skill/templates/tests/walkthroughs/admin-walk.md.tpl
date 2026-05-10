---
role: admin
viewport: [360, 1440]
locale: [{{LOCALES}}]
seed_user: {{SEED_ADMIN_EMAIL}}
seed_password: env:TEST_ADMIN_PASSWORD
base_url: env:BASE_URL  # default http://localhost:3000
---

# Admin walkthrough — {{PROJECT_NAME}}

> Natural-language walkthrough that the **qa-engineer** persona converts to Playwright tests. **Edit this file**, not the generated `tests/e2e/admin/*.spec.ts` — the spec files regenerate when the qa-engineer's healer agent runs.

## Pre-conditions

- Test database seeded by `tests/seed.spec.ts` (run once before the suite).
- Admin user `{{SEED_ADMIN_EMAIL}}` exists with role `admin`.
- App is running at `BASE_URL` (default `http://localhost:3000`).
- Cookies + localStorage clean at flow start.

## Flow 1 — Sign in as admin

1. Visit `/`.
2. Click the "Sign in" link/button.
3. Enter email = `{{SEED_ADMIN_EMAIL}}`.
4. Enter password = `process.env.TEST_ADMIN_PASSWORD`.
5. Submit the form.

**Assertions:**

- After submit, URL matches `/admin` or `/dashboard` (whichever is the admin landing).
- `getByRole('heading', { level: 1 })` contains text matching `/admin|dashboard/i`.
- `getByRole('navigation')` exists and contains admin-only links (e.g. "Users", "Settings", "Audit log").
- No console errors.
- No 4xx/5xx network responses (except OPTIONS preflight).

## Flow 2 — View the user list (admin-only route)

1. From the admin landing, click "Users" in navigation.
2. URL matches `/admin/users`.

**Assertions:**

- `getByRole('table')` is visible.
- Table contains at least the seeded user.
- Pagination present when > 25 users.

## Flow 3 — Create a new resource (replace with project's admin action)

> Replace this with the project's primary admin action (e.g. "create a clinic location," "approve a booking," "publish a post"). The qa-engineer flags walkthroughs without project-specific actions as smoke-only.

1. From the admin landing, click "{{PRIMARY_ADMIN_ACTION_LABEL}}" (e.g. "New clinic", "Approve booking").
2. Fill the form with `{{TEST_RESOURCE_NAME}}`.
3. Submit.

**Assertions:**

- After submit, redirect to the resource detail page.
- New resource visible in the corresponding list page.
- Audit-log entry created (visible at `/admin/audit-log` or equivalent).

## Flow 4 — Sign out

1. Click the user menu (`getByRole('button', { name: /menu|profile|account/i })`).
2. Click "Sign out".

**Assertions:**

- URL returns to `/`.
- Cookies cleared.
- Returning to `/admin` redirects to sign-in.

## Mobile (viewport 360) special checks

- Navigation collapses into a hamburger menu (`getByRole('button', { name: /menu|navigation/i })`).
- Touch targets ≥ 44 × 44 px on every interactive element (Doctrine `default-web-saas` Rule 7).
- Forms scroll into view on focus (no fixed-header occlusion).

## RTL (when `mena-bilingual` Doctrine active, locale `ar-*`)

- `dir="rtl"` set on `<html>` or `<body>`.
- Layout mirrored — primary actions on the left (Arabic reading direction).
- Arabic text rendered with declared RTL-friendly font (Tajawal / Cairo / Readex Pro per `tokens.css`).
- No layout overflow.

## Negative paths (Iron Law II — verification before completion)

- Wrong password → error message visible; no token leaked in error response.
- Direct visit to `/admin` while signed out → redirect to sign-in (status 302/303 OR client-side router redirect).
- Direct visit to `/admin` as a non-admin user → 403 page or sign-out prompt.
- Submit form with empty required fields → field-level error messages; no network request.

## Skeptic kill-shot

> The qa-engineer + skeptic produce one kill-shot question for this walkthrough. Answered in `evidence/P6/admin-walk-skeptic.md` before phase exit.

Example: "What happens to an in-flight admin form when the session token expires mid-submit?"

Answer recorded with the test that proves the behaviour.

## Evidence to capture

- Trace ZIPs at `evidence/P6/admin-walk/playwright-traces/<flow>-<viewport>-<locale>.zip`.
- Screenshots before + after each flow at `evidence/P6/admin-walk/screenshots/`.
- Network HAR (when relevant) at `evidence/P6/admin-walk/network/<flow>.har`.
- axe-core report at `evidence/P6/admin-walk/a11y-<page>.json`.

## Skip / quarantine policy

- Flaky tests → `tests/e2e/admin/quarantine.txt` (filename per project convention) with date + reason. Do NOT silently `test.skip`.
- Genuinely broken (selector drifted) → file a new task for the qa-engineer's healer agent to fix.

## Forking guidance

For a downstream project that has more admin roles (super-admin, billing-admin), copy this template per role and adjust the seed user + flows.
