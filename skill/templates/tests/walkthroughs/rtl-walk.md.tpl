---
role: rtl-user
viewport: [360, 1440]
locale: ar-EG
direction: rtl
seed_user: {{SEED_USER_EMAIL}}
seed_password: env:TEST_USER_PASSWORD
base_url: env:BASE_URL
---

# RTL walkthrough — {{PROJECT_NAME}} (Arabic / `ar-EG`)

> Natural-language walkthrough for the Arabic-locale RTL flow. Pairs with `admin-walk.md` and `user-walk.md`. Loaded ONLY when Doctrine `mena-bilingual` is active.

## Pre-conditions

- Test DB seeded.
- App running at `BASE_URL`.
- User has `locale: ar-EG` set in their profile (or path includes `?locale=ar-EG`).

## Flow 1 — Locale-switch from English to Arabic preserves session

1. Sign in as the user (LTR / `en-US`).
2. Open language switcher in the user menu.
3. Pick **العربية (مصر)** → page rerenders with `dir="rtl"`.

**Assertions:**

- `<html dir="rtl">` set without page reload.
- Session cookie + JWT preserved (no re-auth required).
- Sidebar moves to right side; main content moves to left.
- Logo + brand text remain horizontally centered.
- Localized strings load: "Hello, Ahmed" → "مرحبا، أحمد".
- Numbers + dates re-format per `ar-EG` (Arabic-Indic digits if user prefers; Hijri date alongside Gregorian if app declared).

## Flow 2 — Mirrored navigation icons

1. From the dashboard, click "Back" on a detail page.

**Assertions:**

- Back-arrow icon points to the **right** (in RTL, "back" = right of viewport).
- Forward / next-step icons point to the **left**.
- Chevron / disclosure indicators on accordions mirror.

## Flow 3 — Form input at viewport 360 in RTL

1. Open the primary form (e.g. booking creation).
2. Tap each field; type Arabic text.

**Assertions:**

- Input direction follows the text (Arabic right-to-left within field).
- Labels appear right-aligned; placeholder text right-aligned.
- Error messages right-aligned + readable.
- Form-submit button at the **start** of the form's inline-end direction (right side in RTL).
- Touch targets ≥ 44 × 44 px (per Doctrine `default-web-saas` Rule 7).

## Flow 4 — Tabular data + sorting

1. Open a data table (e.g. bookings list).
2. Sort by date (newest first).

**Assertions:**

- Column headers right-aligned in RTL.
- Sort-indicator chevron mirrored.
- Numeric columns: numbers display with locale-correct grouping (Arabic-Indic comma separator vs Latin).
- Date column shows `ar-EG`-formatted dates (or Hijri if app declared).

## Flow 5 — Modal + toast positioning

1. Trigger a confirmation modal.
2. Trigger a success toast.

**Assertions:**

- Modal centered (no LTR-leaning).
- Toast in inline-end (= left in RTL) corner — opposite of LTR convention.
- Modal "Confirm" button on inline-start side; "Cancel" on inline-end.

## Flow 6 — Search + filter chips

1. Use the global search.
2. Apply 2+ filter chips.

**Assertions:**

- Search input direction follows query language (Arabic input → RTL within field).
- Filter chips wrap in RTL natural reading order (right to left).
- Removing a chip via "×" button targets the chip on the user's reading-direction side.

## Flow 7 — Empty states + onboarding

1. Navigate to a section with no data yet.

**Assertions:**

- Empty state text in `ar-EG` per the Doctrine — explain why empty + next-action CTA.
- Illustrations (if used) mirrored or RTL-neutral.
- CTA button on the inline-start side.

## Negative paths

- **Mixed-direction text** (Arabic with English brand name embedded). The brand stays LTR within the Arabic flow — verify `<bdi>` or `unicode-bidi` is correctly applied.
- **Form validation in mixed language** (user types English in an Arabic-labeled field). Validation messages should still appear in active locale.
- **URL with locale switch + deep link** (`/app/bookings/123?locale=ar-EG`). Preserves the deep link + applies the new locale.

## Mobile (viewport 360) special checks

- Hamburger menu opens from inline-end side (= right in RTL).
- Bottom-tab navigation order mirrors (1st tab on right side).
- Pull-to-refresh works.
- Touch swipe gestures for back-navigation: a right-swipe means "back" in RTL (opposite of LTR).

## Skeptic kill-shot

> "What happens when the user has Arabic-Indic-digit preference set in OS but the app uses Latin digits in financial fields (or vice versa)? Are the numbers parseable correctly when re-submitted to the server?"

Answer recorded in `evidence/<phase>/skeptic-mena.md`.

## Evidence to capture

- Traces / screenshots / HAR for every flow at `evidence/P6/rtl/<role>/`.
- Visual diff vs LTR baseline (if Mode is Enterprise or Doctrine `vibe-defense` is loaded).
- axe-core accessibility check on every page in RTL (focus rings still visible; tab order correct in RTL reading order).

## Cross-references

- Doctrine: `../../../skill/doctrines/mena-bilingual.md`
- Tokens template (already RTL-ready since v0.6.1): `../../../skill/templates/tokens.css.tpl`
- Playwright config template: `../../../skill/templates/playwright.config.ts.tpl`
