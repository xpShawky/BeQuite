# tests/walkthroughs/

> Natural-language walkthrough specs that drive the **qa-engineer** persona's `planner → spec writer → generator → healer` pattern (Constitution Article II — verification before completion; Article VI — honest reporting).
>
> One file per role. The qa-engineer reads these, explores the running app, generates Playwright tests using `getByRole` accessibility-first locators, and heals broken selectors as the app evolves.

## Files

- `admin-walk.md` — what the admin role does, end-to-end, in plain English.
- `user-walk.md` — what a regular user does, end-to-end.
- (Optional) `<role>-walk.md` per additional role declared in the project (e.g. `support-agent-walk.md`, `read-only-walk.md`).

## Format

Each walkthrough is Markdown with a frontmatter block + flow sections + assertions. The qa-engineer's planner agent reads this Markdown, opens the running app via Playwright, explores until it can write a deterministic test that satisfies every assertion.

```markdown
---
role: admin
viewport: [360, 1440]            # mobile + desktop walked
locale: [en-US, ar-EG]           # both when mena-bilingual Doctrine active
seed_user: admin@test.local      # seeded into DB by tests/seed.spec.ts
seed_password: env:TEST_ADMIN_PASSWORD
---

# Admin walkthrough

## Flow 1 — Sign in

1. Visit `/`.
2. Click "Sign in".
3. Enter email + password.
4. Expect redirect to `/admin`.
5. Expect "Admin Dashboard" heading.

**Assertions:**
- `getByRole('heading', { name: /admin dashboard/i })` is visible.
- No console errors during the flow.
- No 4xx/5xx network responses (except OPTIONS preflight).

## Flow 2 — Create a record

...
```

## What the planner agent does

For each walkthrough:

1. **Explore** the running app at `BASE_URL` (default `http://localhost:3000`).
2. **Map** each declared flow to actual DOM selectors using `getByRole` / `getByLabel` / `getByText`.
3. **Emit** Playwright `.spec.ts` files into `tests/e2e/<role>/<flow>.spec.ts`.
4. **Run** the suite. Capture trace + screenshots into `evidence/P6/<task>/playwright-traces/`.
5. **Heal** broken selectors with condition-based waits (`expect(...).toBeVisible()` instead of `waitForSelector`).
6. **Report** per-flow: pass / fail / flaky; surface flaky tests with quarantine ticket (don't silently skip).

## Per-Mode rigour

- **Fast Mode** — smoke walks only (sign in + main happy path).
- **Safe Mode** — full walks at viewport 360 + 1440.
- **Enterprise Mode** — full walks + visual diff + accessibility deep-dive (axe-core on every page) + RTL walks (when `mena-bilingual` Doctrine active) at locale `en-*` and `ar-*`.

## Anti-patterns (qa-engineer refuses)

- Walkthroughs that say "click the third button" — selector-fragile. Use role/label/text.
- Walkthroughs without assertions — passes are unprovable.
- Walkthroughs that depend on external state (live API, third-party service) without a stub. Use MSW / Mirage / Playwright route mocks.
- Walkthroughs that reuse seeded credentials across tests without isolation.

## Cross-references

- `skill/agents/qa-engineer.md` — the persona that consumes these walkthroughs.
- `skill/references/playwright-walks.md` — canonical reference + examples (drafted v0.6.0).
- `skill/templates/tests/seed.spec.ts.tpl` — seeds the test users referenced by walkthroughs.
- `bequite verify` (Phase 6) — runs all walkthroughs as a phase gate.
