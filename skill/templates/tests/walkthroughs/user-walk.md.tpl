---
role: user
viewport: [360, 1440]
locale: [{{LOCALES}}]
seed_user: {{SEED_USER_EMAIL}}
seed_password: env:TEST_USER_PASSWORD
base_url: env:BASE_URL
---

# User walkthrough — {{PROJECT_NAME}}

> Natural-language walkthrough for the regular-user role. Pairs with `admin-walk.md`.

## Pre-conditions

- Test DB seeded (`tests/seed.spec.ts`).
- User `{{SEED_USER_EMAIL}}` exists with role `user`.
- App running at `BASE_URL`.
- Cookies + localStorage clean.

## Flow 1 — Sign up (when self-serve)

> Skip if the project is invitation-only.

1. Visit `/`.
2. Click "Sign up".
3. Enter email + password + accept terms checkbox.
4. Submit.

**Assertions:**

- Confirmation email triggered (mocked in tests via Mailhog / MailDev / Playwright route mock).
- Redirect to onboarding or dashboard.
- New user record visible to admin (cross-walkthrough verification).

## Flow 2 — Sign in

1. Visit `/`.
2. Click "Sign in".
3. Enter email + password.
4. Submit.

**Assertions:**

- Redirect to user dashboard (`/app` or `/dashboard`).
- `getByRole('heading')` welcomes the user (by name when displayed).
- Navigation does NOT show admin-only links.

## Flow 3 — Primary user action (replace with project's main use case)

> Replace with the project's primary user value-prop (e.g. "book a clinic appointment", "publish a post", "submit a question"). The qa-engineer flags walkthroughs without project-specific actions as smoke-only.

1. From the user dashboard, click "{{PRIMARY_USER_ACTION_LABEL}}".
2. Walk through the flow per the project's UX direction.
3. Submit / confirm.

**Assertions:**

- Confirmation visible (page redirect, success toast, or modal).
- Resource visible in the user's "My X" list (e.g. "My bookings").
- Optional notification triggered (email / push / in-app).

## Flow 4 — View own profile + edit

1. Click user menu → "Profile" or "Account".
2. Edit a field (e.g. display name).
3. Save.

**Assertions:**

- Save button shows pending → success state.
- Field value persists on page reload.
- No PII leaked in network responses (Article IX hook scans).

## Flow 5 — Sign out

1. Click user menu → "Sign out".

**Assertions:**

- Redirect to `/`.
- Cookies cleared.
- Returning to `/app` redirects to sign-in.

## Negative paths

- Sign in with wrong password → error message; no token leaked.
- Direct visit to `/admin` as user → 403 OR redirect to user dashboard.
- Submit with empty required fields → field-level errors; no network request.
- Try to access another user's resource by URL ID → 403 or 404 (NOT 200 with someone else's data — IDOR test).

## Mobile (viewport 360) special checks

- Same as admin: hamburger menu, touch targets ≥ 44 × 44 px, no layout overflow.

## RTL (mena-bilingual)

- Same as admin: `dir="rtl"`, mirrored layout, Arabic-friendly font.

## Accessibility deep-dive (Enterprise Mode)

- Tab through every interactive element on every page; focus order makes sense.
- Screen-reader announcements (use Playwright's `aria-` attribute checks; or run `axe-core` on every page).
- Forms have `<label>` + `for=` connections.
- Errors announced via `aria-live`.

## Skeptic kill-shot

Example: "What happens when the user tries to submit a form they no longer have permission to submit (their role was downgraded mid-session)?"

## Evidence to capture

Same paths as admin-walk: traces / screenshots / HAR / a11y per role + viewport + locale.

## Forking guidance

For projects with multiple user-tier roles (free / pro / enterprise), copy this template per tier and adjust the seed user + permitted flows.
