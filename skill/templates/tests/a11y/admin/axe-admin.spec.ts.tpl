/**
 * axe-admin.spec.ts — axe-core walks for the admin role.
 *
 * Lands at `tests/a11y/admin/axe-admin.spec.ts` per `bequite init` for projects
 * loaded with a frontend Doctrine. Doctrine `default-web-saas` Rule 8: zero
 * WCAG AA violations required for merge.
 *
 * Cross-references:
 * - skill/skills-bundled/impeccable/references/anti-patterns.md item #9 (poor contrast).
 * - skill/templates/tests/walkthroughs/admin-walk.md.tpl — the natural-language flow
 *   this spec mirrors. Each route walked here MUST appear in admin-walk.md.
 * - cli/bequite/verify.py — orchestrator that runs this gate per-Mode.
 */

import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import * as fs from 'node:fs';
import * as path from 'node:path';

const ADMIN_ROUTES = [
  '/',
  '/admin',
  '/admin/users',
  '/admin/settings',
  // Add every admin-walk route. Keep in sync with admin-walk.md.
];

const EVIDENCE_DIR = 'evidence/P6/axe/admin';

test.beforeAll(async () => {
  fs.mkdirSync(EVIDENCE_DIR, { recursive: true });
});

test.describe('axe-core walks — admin role', () => {
  test.beforeEach(async ({ page }) => {
    // Sign in as admin (replace with your project's auth flow).
    await page.goto('/');
    await page.getByRole('link', { name: /sign in/i }).click();
    await page.getByLabel('Email').fill(process.env.TEST_ADMIN_EMAIL!);
    await page.getByLabel('Password').fill(process.env.TEST_ADMIN_PASSWORD!);
    await page.getByRole('button', { name: /sign in/i }).click();
    await page.waitForURL(/\/admin/);
  });

  for (const route of ADMIN_ROUTES) {
    test(`a11y: ${route}`, async ({ page }) => {
      await page.goto(route);
      // Wait for content to settle (skeletons resolved). Tighten if your
      // app has a more reliable signal.
      await page.waitForLoadState('networkidle');

      const results = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
        .analyze();

      // Save the JSON for evidence even on pass.
      const safeRoute = route.replace(/[/]/g, '_') || '_root';
      fs.writeFileSync(
        path.join(EVIDENCE_DIR, `${safeRoute}.json`),
        JSON.stringify(results, null, 2),
      );

      // Hard fail on any WCAG AA violation. Doctrine Rule 8.
      expect(results.violations).toEqual([]);
    });
  }
});
