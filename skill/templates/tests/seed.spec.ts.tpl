/**
 * tests/seed.spec.ts — seeds the test database for end-to-end Playwright walks.
 *
 * Run ONCE before the e2e suite via:
 *   npx playwright test tests/seed.spec.ts --project=setup
 *
 * The qa-engineer's planner reads tests/walkthroughs/*.md and assumes:
 *   - Admin user exists (email = TEST_ADMIN_EMAIL, password = TEST_ADMIN_PASSWORD).
 *   - Regular user exists (TEST_USER_EMAIL, TEST_USER_PASSWORD).
 *   - Seed data per the project's data-model.md is loaded.
 *
 * This file is template-rendered by `bequite init`; placeholders below get
 * filled with the chosen stack's idioms (Drizzle, Prisma, raw SQL, etc.).
 */

import { test as setup, expect } from '@playwright/test';
import { execSync } from 'node:child_process';

setup.describe.configure({ mode: 'serial' });

const TEST_ADMIN_EMAIL = process.env.TEST_ADMIN_EMAIL ?? '{{SEED_ADMIN_EMAIL}}';
const TEST_USER_EMAIL = process.env.TEST_USER_EMAIL ?? '{{SEED_USER_EMAIL}}';
const TEST_ADMIN_PASSWORD = process.env.TEST_ADMIN_PASSWORD;
const TEST_USER_PASSWORD = process.env.TEST_USER_PASSWORD;
const BASE_URL = process.env.BASE_URL ?? 'http://localhost:3000';

if (!TEST_ADMIN_PASSWORD || !TEST_USER_PASSWORD) {
  throw new Error(
    'TEST_ADMIN_PASSWORD and TEST_USER_PASSWORD env vars must be set for the seed.spec.ts run.\n' +
      'Set them in .env.test (gitignored) or pass via the CI env. Article IV (Iron Law) — never hardcode passwords.'
  );
}

setup('reset and seed test database', async () => {
  // Reset to known-empty state.
  // Adjust for the project's stack:
  //   - Drizzle:    `npx drizzle-kit push --config=drizzle.config.test.ts`
  //   - Prisma:     `npx prisma migrate reset --force --skip-seed`
  //   - Raw SQL:    `psql $TEST_DB_URL -f scripts/test-reset.sql`
  console.log('[seed] resetting test DB...');
  execSync('{{RESET_DB_COMMAND}}', { stdio: 'inherit' });

  // Apply migrations.
  console.log('[seed] applying migrations...');
  execSync('{{MIGRATE_DB_COMMAND}}', { stdio: 'inherit' });

  // Seed data per data-model.md.
  console.log('[seed] inserting seed data...');
  execSync('{{SEED_DB_COMMAND}}', { stdio: 'inherit' });
});

setup('verify seeded admin user can sign in', async ({ request }) => {
  // Hit the auth endpoint directly (no UI) to confirm the seed worked.
  const response = await request.post(`${BASE_URL}/{{AUTH_LOGIN_PATH}}`, {
    data: { email: TEST_ADMIN_EMAIL, password: TEST_ADMIN_PASSWORD },
  });
  expect(response.status()).toBe(200);
  const body = await response.json();
  expect(body).toHaveProperty('{{SESSION_TOKEN_FIELD}}');
});

setup('verify seeded regular user can sign in', async ({ request }) => {
  const response = await request.post(`${BASE_URL}/{{AUTH_LOGIN_PATH}}`, {
    data: { email: TEST_USER_EMAIL, password: TEST_USER_PASSWORD },
  });
  expect(response.status()).toBe(200);
});

setup('write seed evidence to evidence/P6/seed/', async () => {
  // The qa-engineer's healer reads this to confirm seed reproducibility.
  const fs = await import('node:fs/promises');
  const path = await import('node:path');
  const evidenceDir = path.resolve('evidence/P6/seed');
  await fs.mkdir(evidenceDir, { recursive: true });
  await fs.writeFile(
    path.join(evidenceDir, `seed-${new Date().toISOString().replace(/[:.]/g, '-')}.json`),
    JSON.stringify(
      {
        seeded_at: new Date().toISOString(),
        admin_email: TEST_ADMIN_EMAIL,
        user_email: TEST_USER_EMAIL,
        base_url: BASE_URL,
        // No passwords in evidence; Article IV.
      },
      null,
      2
    )
  );
});
