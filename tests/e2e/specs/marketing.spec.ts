import { test, expect } from "@playwright/test";
import path from "node:path";

/**
 * Marketing site smoke (http://localhost:3000).
 *
 * Covers Phase 1 audit findings F-1, F-2, F-7, F-10.
 * Captures screenshots into docs/audits/screenshots/.
 */

const SCREENSHOT_DIR = path.join(__dirname, "../../../docs/audits/screenshots");

test.describe("marketing site", () => {
  test("home page renders + no console errors", async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on("console", (msg) => {
      if (msg.type() === "error") consoleErrors.push(msg.text());
    });
    page.on("pageerror", (err) => consoleErrors.push("pageerror: " + err.message));

    const res = await page.goto("/", { waitUntil: "domcontentloaded" });
    expect(res?.status()).toBeLessThan(400);

    // Hero text visible
    await expect(page.locator("h1")).toContainText("Plan it.");
    await expect(page.locator("h1")).toContainText("Build it.");
    await expect(page.locator("h1")).toContainText("Be quiet.");

    // Nav present
    await expect(page.getByRole("link", { name: "Docs" }).first()).toBeVisible();
    await expect(page.getByRole("link", { name: "Get started" }).first()).toBeVisible();

    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "marketing-home.png"),
      fullPage: false,
    });

    // No console errors after a brief settle
    await page.waitForTimeout(500);
    expect(consoleErrors, `console errors: ${JSON.stringify(consoleErrors)}`).toHaveLength(0);
  });

  test("F-1: How it works anchor scrolls somewhere visible (not 0,0)", async ({ page }) => {
    await page.goto("/");

    // Click the "How it works" nav link. Either it scrolls to a real anchor
    // (post-fix) or it stays at the top (pre-fix bug).
    const link = page.getByRole("link", { name: /how it works/i }).first();
    await link.click();

    // Give the smooth scroll time to settle.
    await page.waitForTimeout(800);

    const scrollY = await page.evaluate(() => window.scrollY);

    // Pre-fix: scrollY is 0 because #how-it-works doesn't exist.
    // Post-fix: scrollY > 200 because PhasesScroll is well below the fold.
    expect(scrollY, "expected scroll past hero — #how-it-works anchor should exist").toBeGreaterThan(200);
  });

  test("F-2: Features anchor scrolls to Features section", async ({ page }) => {
    await page.goto("/");
    const link = page.getByRole("link", { name: /^Features$/ }).first();
    await link.click();
    await page.waitForTimeout(800);
    const scrollY = await page.evaluate(() => window.scrollY);
    expect(scrollY).toBeGreaterThan(400);
  });

  test("Get started CTA goes to /docs/quickstart", async ({ page }) => {
    await page.goto("/");
    const cta = page.getByRole("link", { name: "Get started" }).first();
    await Promise.all([page.waitForURL(/\/docs\/quickstart$/), cta.click()]);
    await expect(page.locator("h1, h2").first()).toBeVisible();
  });

  test("/docs index page renders with 6 tutorial cards", async ({ page }) => {
    await page.goto("/docs");
    // 6 tutorials shipped: quickstart, from-scratch, retrofit, multi-model-planning, auto-mode, troubleshooting
    // Each tutorial can have multiple links (card title + sidebar). Check
    // that each *distinct* href appears at least once.
    const expectedSlugs = ["quickstart", "from-scratch", "retrofit", "multi-model-planning", "auto-mode", "troubleshooting"];
    for (const slug of expectedSlugs) {
      const link = page.locator(`a[href='/docs/${slug}']`).first();
      await expect(link, `expected link to /docs/${slug}`).toBeVisible({ timeout: 5000 });
    }

    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "marketing-docs-index.png"),
      fullPage: false,
    });
  });

  test("/docs/quickstart renders MDX content", async ({ page }) => {
    await page.goto("/docs/quickstart");
    await expect(page.locator("h1, h2").first()).toBeVisible();
    // MDX renders code blocks
    await expect(page.locator("pre, code").first()).toBeVisible();
  });

  test("F-10: text contrast on hero — body text not too dim", async ({ page }) => {
    await page.goto("/");
    // Find the subhead and check it's actually rendered with reasonable contrast.
    // We don't compute WCAG ratio here (would need axe-core); just verify the
    // subhead is non-empty and visible.
    const subhead = page.locator("text=The AI project operating system").first();
    await expect(subhead).toBeVisible();
    const color = await subhead.evaluate((el) => getComputedStyle(el).color);
    // Should NOT be pure black or pure transparent
    expect(color).not.toBe("rgb(0, 0, 0)");
    expect(color).not.toMatch(/rgba\(.+, 0\)$/);
  });
});
