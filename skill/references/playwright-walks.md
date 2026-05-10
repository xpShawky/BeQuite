# Playwright walks reference

> Canonical reference for the **qa-engineer** persona's `planner → spec writer → generator → healer` pattern. Loaded in P5 (when frontend tasks ship walkthrough updates) and P6 (validation mesh runs the suite).
>
> Per Constitution Article II — verification before completion. The walks ARE the acceptance evidence for any frontend phase exit.

## 1. The four-step pattern

### Step 1 — Planner (explores running app)

Reads `tests/walkthroughs/<role>-walk.md`. Opens the running app at `BASE_URL`. Walks each declared flow manually (programmatically — clicking, typing). Maps each natural-language step to a stable selector via Playwright's accessibility-first locators:

- `getByRole('button', { name: /sign in/i })` (preferred — matches assistive tech)
- `getByLabel('Email')` (form fields)
- `getByText('Welcome back')` (visible text)
- `getByPlaceholder('your@email.com')`
- `getByTestId('submit-button')` (last resort; only when role/label/text fail)

Outputs: a **selector map** at `tests/_planner/<role>-selector-map.json` keyed by walkthrough flow + step.

### Step 2 — Spec writer (composes Playwright tests)

Reads the selector map + the walkthrough Markdown. Generates `tests/e2e/<role>/<flow>.spec.ts` files. One file per flow. Each file:

- Imports `@playwright/test`.
- Has `test.describe(...)` per flow.
- Has `test(...)` per assertion group.
- Uses `expect(...)` not `assert` — Playwright's auto-retry semantics are crucial.
- Embeds the walkthrough's natural-language as code comments above each block.

### Step 3 — Generator (runs the suite)

`npx playwright test --project=<role>-<viewport>-<locale>`. Captures:

- Trace ZIP (`evidence/P6/<role>/playwright-traces/`).
- Screenshots on failure.
- Video on failure.
- Console errors (via `page.on('console')`).
- Network failures (via `page.on('requestfailed')`).
- 4xx/5xx responses (via `page.on('response')` + status check).

### Step 4 — Healer (repairs broken selectors)

Runs after a failure. The healer:

1. Re-explores the same flow. If a selector that worked before now misses, find the new selector via DOM diff.
2. Updates the selector map.
3. Regenerates the spec file.
4. Re-runs.
5. If healed, marks the test green + logs the fix to `evidence/P6/<role>/healer-log-<date>.md`.
6. If still failing, escalates: file a new task for the architect (the failure is structural, not selector-drift).

### Anti-flake patterns the healer enforces

- **No `waitForSelector` with hardcoded timeout** — use `expect(...).toBeVisible({ timeout: 5000 })`.
- **No `setTimeout(...)`** — use `await expect(...)` with auto-retry.
- **No URL hash polling** — use `page.waitForURL(...)`.
- **No race-condition selectors** — use the most-stable role/label/text; only fall back to `getByTestId` when nothing else works.

## 2. Per-Mode rigour (Constitution v1.0.1 — Modes)

| Gate | Fast | Safe | Enterprise |
|---|---|---|---|
| seed.spec.ts (DB seed) | ✓ | ✓ | ✓ |
| Smoke walks (sign in + main happy path) | ✓ | ✓ | ✓ |
| Full role walks (admin + user + ...) | ✗ | ✓ | ✓ |
| Viewport: 360 + 1440 | optional | ✓ | ✓ |
| Locale: en-* + ar-* (mena-bilingual) | optional | ✓ when active | ✓ when active |
| Visual diff vs prior baseline | ✗ | optional | ✓ |
| axe-core deep-dive (every page) | optional | ✓ key pages | ✓ every page |
| Negative paths (auth failures, IDOR, CSRF) | optional | ✓ | ✓ |
| Network HAR captured | optional | ✓ | ✓ |
| Console error capture | ✓ | ✓ | ✓ |

## 3. Standard walkthrough fixtures (per Doctrine)

When a Doctrine is active, the qa-engineer adds these walks to the suite:

- **default-web-saas** — admin-walk + user-walk + a11y deep-dive + tokens-only audit (axe + custom rule).
- **fintech-pci** — additional walks for: PAN-masking-in-UI, CDE-segregation-via-network-tab, audit-log-visibility.
- **healthcare-hipaa** — additional walks for: PHI-redaction-in-UI, minimum-necessary-access, audit-trail-per-PHI-touch.
- **gov-fedramp** — additional walks for: FIPS-validated-TLS-suite, MFA-on-privileged-actions, immutable-audit-log.
- **mena-bilingual** — additional walks for: ar-EG locale, RTL layout, Arabic-friendly font rendered.
- **eu-gdpr** — additional walks for: cookie banner reject-all parity, data subject rights endpoints, breach-notification panel.
- **ai-automation** — walks for the workflow admin panel (when present).
- **vibe-defense** — adds harden-on-deploy gate visualisation walk.

## 4. Examples

### Example flow (TS) — admin sign-in

```typescript
// tests/e2e/admin/sign-in.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Admin sign-in', () => {
  test('admin signs in with valid credentials', async ({ page }) => {
    // 1. Visit /
    await page.goto('/');

    // 2. Click "Sign in"
    await page.getByRole('link', { name: /sign in/i }).click();

    // 3. Enter credentials
    await page.getByLabel('Email').fill(process.env.TEST_ADMIN_EMAIL!);
    await page.getByLabel('Password').fill(process.env.TEST_ADMIN_PASSWORD!);

    // 4. Submit
    await page.getByRole('button', { name: /sign in/i }).click();

    // 5. Assertion: redirect + heading
    await expect(page).toHaveURL(/\/admin/);
    await expect(page.getByRole('heading', { level: 1, name: /admin dashboard/i })).toBeVisible();

    // 6. No console errors
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        throw new Error(`Console error: ${msg.text()}`);
      }
    });
  });

  test('wrong password shows error and does not leak token', async ({ page }) => {
    await page.goto('/sign-in');
    await page.getByLabel('Email').fill(process.env.TEST_ADMIN_EMAIL!);
    await page.getByLabel('Password').fill('wrong-password');
    await page.getByRole('button', { name: /sign in/i }).click();

    await expect(page.getByRole('alert')).toContainText(/invalid credentials/i);
    // Article IV — no token leaked in error response.
    const cookies = await page.context().cookies();
    expect(cookies.find((c) => /session|auth|token/i.test(c.name))).toBeUndefined();
  });
});
```

## 5. Receipt schema (cross-reference v0.7.0)

When v0.7.0 ships the receipts system, every Playwright run emits a receipt:

```json
{
  "version": "1",
  "phase": "P6",
  "timestamp_utc": "2026-05-10T14:23:01Z",
  "command": "npx playwright test --project=admin-desktop-1440-en-US",
  "exit": 0,
  "stdout_hash": "sha256:...",
  "tests": {
    "total": 12,
    "passed": 12,
    "failed": 0,
    "skipped": 0,
    "flaky": 0
  },
  "evidence": {
    "trace_zip": "evidence/P6/admin/playwright-traces/...zip",
    "screenshots": ["..."],
    "junit_xml": "evidence/P6/playwright-junit.xml"
  },
  "doctrine_gates": {
    "default-web-saas-rule-7": "pass",
    "default-web-saas-rule-8-axe-core": "pass"
  }
}
```

## 6. Cross-references

- **`skill/agents/qa-engineer.md`** — the persona that runs this pattern.
- **`skill/templates/tests/walkthroughs/`** — Markdown templates the planner reads.
- **`skill/templates/tests/seed.spec.ts.tpl`** — DB seed for the suite.
- **`skill/templates/playwright.config.ts.tpl`** — Playwright config template.
- **`skill/templates/scripts/self-walk.sh.tpl`** — cheap-curl sweep complementing the heavier suite.
- **`skill/templates/scripts/smoke.sh.tpl`** — API smoke alongside Playwright walks.
- **`cli/bequite/verify.py`** — Phase 6 orchestrator (v0.6.0+); runs walks + axe + smoke + audit.

## 7. Forking guidance

- For projects with multi-tenant role hierarchies, fork to `<role>-walk.md` per role; reference each in `playwright.config.ts::projects`.
- For fragile-DOM stacks (heavy React Server Components churn), tighten healer escalation thresholds.
- For air-gapped CI, replace Playwright's hosted browser download with bundled `@playwright/browser-chromium` cached.
