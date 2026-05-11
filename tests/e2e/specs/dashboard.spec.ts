import { test, expect } from "@playwright/test";
import path from "node:path";

/**
 * Dashboard smoke (http://localhost:3001).
 * Covers Phase 1 audit findings F-3, F-4, F-5, F-6.
 */

const SCREENSHOT_DIR = path.join(__dirname, "../../../docs/audits/screenshots");

test.use({ baseURL: "http://localhost:3001" });

test.describe("dashboard", () => {
  test("home page renders + no console errors", async ({ page }) => {
    const consoleErrors: string[] = [];
    page.on("console", (msg) => {
      if (msg.type() === "error") consoleErrors.push(msg.text());
    });
    page.on("pageerror", (err) => consoleErrors.push("pageerror: " + err.message));

    const res = await page.goto("/", { waitUntil: "domcontentloaded" });
    expect(res?.status()).toBeLessThan(400);

    // TopBar present
    await expect(page.locator("header").first()).toBeVisible();
    // PhasesSidebar present (look for the gold "Phases" heading — first match)
    await expect(page.getByText("Phases", { exact: true }).first()).toBeVisible();
    // AgentPanel present (look for "Agent" — first match avoids "AGENT ONLINE" + "Agent")
    await expect(page.getByText(/^agent$/i).first()).toBeVisible();

    await page.screenshot({
      path: path.join(SCREENSHOT_DIR, "dashboard-home.png"),
      fullPage: true,
    });

    await page.waitForTimeout(500);
    expect(consoleErrors, `console errors: ${JSON.stringify(consoleErrors)}`).toHaveLength(0);
  });

  test("F-3: DEPLOY button is honest about not being wired yet", async ({ page }) => {
    await page.goto("/");

    const deployBtn = page.getByRole("button", { name: /deploy/i }).first();
    await expect(deployBtn).toBeVisible();

    // Post-v2.0.0-alpha.6: the DEPLOY button is INTENTIONALLY disabled with
    // a tooltip until a real deploy handler ships in v2.0.0-beta.1. The fix
    // for F-3 was to STOP pretending the button works — honest UX over
    // dead-click UX.
    const isDisabled = await deployBtn.isDisabled();
    expect(isDisabled, "DEPLOY button should be disabled until v2.0.0-beta.1").toBe(true);

    const title = await deployBtn.getAttribute("title");
    expect(title, "DEPLOY button needs a tooltip explaining why it's disabled").not.toBeNull();
    expect(title).toMatch(/v2\.0\.0-beta\.1|bequite handoff/);
  });

  test("F-4 + F-5: Plan/Tasks/Tests + Recent Activity panels render (data may be hardcoded — audit flag)", async ({ page }) => {
    await page.goto("/");
    // These three section titles come from PlanTasksTests.
    await expect(page.getByText("Plan", { exact: true }).first()).toBeVisible();
    await expect(page.getByText("Tasks", { exact: true }).first()).toBeVisible();
    await expect(page.getByText("Tests", { exact: true }).first()).toBeVisible();
    // Recent activity from AgentPanel.
    await expect(page.getByText(/recent activity/i)).toBeVisible();
  });

  test("CommandConsole renders in filesystem mode OR Terminal in HTTP mode", async ({ page }) => {
    await page.goto("/");
    // In HTTP mode (Docker compose default), the xterm.js Terminal renders.
    //   - has a "Run" button (filesystem mode disables it)
    //   - the xterm.js .xterm class is added after dynamic-import + term.open()
    //     so wait up to 5s for it to appear
    // In filesystem mode, the static CommandConsole renders ("Command Console" header).
    const terminalRun = page.getByRole("button", { name: /^run$/i });
    const commandConsole = page.getByText("Command Console").first();

    await Promise.race([
      terminalRun.waitFor({ state: "visible", timeout: 5000 }).catch(() => null),
      commandConsole.waitFor({ state: "visible", timeout: 5000 }).catch(() => null),
    ]);

    const runVisible = await terminalRun.isVisible().catch(() => false);
    const consoleVisible = await commandConsole.isVisible().catch(() => false);
    expect(
      runVisible || consoleVisible,
      "neither live Terminal (Run button) nor static CommandConsole rendered",
    ).toBe(true);
  });

  test("LiveIndicator pill present in TopBar", async ({ page }) => {
    await page.goto("/");
    // LiveIndicator has data-testid="live-indicator"
    const indicator = page.getByTestId("live-indicator");
    await expect(indicator).toBeVisible();
    // Text is one of LIVE / CONNECTING / STALE / OFFLINE / FS
    const text = await indicator.textContent();
    expect(text).toMatch(/LIVE|CONNECTING|STALE|OFFLINE|FS/);
  });

  test("footer has mode chip (FS or HTTP)", async ({ page }) => {
    await page.goto("/");
    const chip = page.getByText(/^(FS|HTTP)$/).first();
    await expect(chip).toBeVisible();
  });
});
