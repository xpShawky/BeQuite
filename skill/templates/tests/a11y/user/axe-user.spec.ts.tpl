/**
 * axe-user.spec.ts — axe-core walks for the regular-user role.
 *
 * Lands at `tests/a11y/user/axe-user.spec.ts` per `bequite init` for projects
 * loaded with a frontend Doctrine. Pairs with `axe-admin.spec.ts`. Doctrine
 * `default-web-saas` Rule 8: zero WCAG AA violations required for merge.
 *
 * Cross-references:
 * - skill/templates/tests/walkthroughs/user-walk.md.tpl — natural-language flow.
 * - cli/bequite/verify.py — orchestrator.
 */

import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import * as fs from 'node:fs';
import * as path from 'node:path';

const USER_ROUTES = [
  '/',
  '/sign-in',
  '/app',
  '/app/profile',
  // Add every user-walk route. Keep in sync with user-walk.md.
];

const EVIDENCE_DIR = 'evidence/P6/axe/user';

test.beforeAll(async () => {
  fs.mkdirSync(EVIDENCE_DIR, { recursive: true });
});

test.describe('axe-core walks — user role', () => {
  test.beforeEach(async ({ page }) => {
    // Sign in as a regular user.
    await page.goto('/');
    await page.getByRole('link', { name: /sign in/i }).click();
    await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!);
    await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!);
    await page.getByRole('button', { name: /sign in/i }).click();
    await page.waitForURL(/\/app/);
  });

  for (const route of USER_ROUTES) {
    test(`a11y: ${route}`, async ({ page }) => {
      await page.goto(route);
      await page.waitForLoadState('networkidle');

      const results = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
        .analyze();

      const safeRoute = route.replace(/[/]/g, '_') || '_root';
      fs.writeFileSync(
        path.join(EVIDENCE_DIR, `${safeRoute}.json`),
        JSON.stringify(results, null, 2),
      );

      expect(results.violations).toEqual([]);
    });
  }
});
