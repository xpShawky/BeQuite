import { defineConfig, devices } from "@playwright/test";

/**
 * BeQuite end-to-end Playwright config (Phase 3 / Phase 7).
 *
 * Tests assume the Studio stack is already running on localhost:3000-3002.
 * In CI we'll add a webServer block to spin docker compose; for local
 * iteration we just `docker compose up -d` first then `npm test` here.
 */
export default defineConfig({
  testDir: "./specs",
  fullyParallel: false,           // these talk to a single API
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,                     // SSE + shared state -> serial is safe
  reporter: [
    ["list"],
    ["html", { outputFolder: "../../docs/audits/screenshots/_playwright-report", open: "never" }],
  ],
  outputDir: "../../docs/audits/screenshots/_playwright-output",
  use: {
    baseURL: "http://localhost:3000",   // marketing
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    actionTimeout: 10_000,
    navigationTimeout: 30_000,
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
