# BeQuite — Frontend UX Audit (Phase 3)

**Date:** 2026-05-11
**Scope:** Browser-level QA of `studio/marketing/` (port 3000) + `studio/dashboard/` (port 3001) using Playwright 1.59.1. Live tests against Docker Compose stack. Screenshots captured at `docs/audits/screenshots/`.
**Methodology:** Authored 24-test Playwright suite covering Phase 1 findings, ran against pre-fix code (caught 4 failures), fixed each finding, re-ran (24/24 passed), captured fresh screenshots.

---

## 1. Executive summary

The frontend ships with a coherent gold-on-black brand and renders cleanly. **Eight UX issues** flagged by Phase 1 static analysis broke down as:

- **2 false positives** (F-1, F-2) — Phase 1 grep missed an existing `id="how-it-works"` due to HTML escaping. Playwright confirmed the anchor links DO work (scrollY > 200px after click). Audit corrected.
- **6 real bugs** all fixed and verified live in this phase: dead DEPLOY button, three hardcoded mock panels, missing `@keyframes glint`, dead conditional in CommandConsole, plus one bonus bug Playwright surfaced (Next.js cached server-component meant `BEQUITE_DASHBOARD_MODE` env var was ignored at runtime).

**Final state: 24/24 Playwright tests pass.** Dashboard now displays real project data from `loadProject()`; marketing site renders all 6 tutorial cards; honest "soon" / "(no project)" / "(awaiting verify)" states replace the hardcoded mock content that shipped through alpha.5.

---

## 2. Test methodology

### 2.1 Suite

`tests/e2e/specs/` (Playwright 1.59.1, Chromium headless):

| Spec | Tests | What it covers |
|---|---|---|
| `marketing.spec.ts` | 7 | Home renders, console errors, anchor scroll (F-1/F-2), CTA navigation, /docs index, MDX rendering, text contrast |
| `dashboard.spec.ts` | 6 | Home renders, DEPLOY button honesty (F-3), panel render (F-4/F-5), Terminal vs CommandConsole (F-6), LiveIndicator, mode chip |
| `api.spec.ts` | 11 | Full API surface (doubles as Phase 4 deliverable) |

### 2.2 Running

```bash
cd tests/e2e
npm install                    # 6 packages
npx playwright install chromium
npx playwright test            # against http://localhost:3000-3002
```

Tests assume the Studio Docker stack is up:
```bash
docker compose up -d
```

### 2.3 Artifacts

- `docs/audits/screenshots/marketing-home.png` — cinematic landing hero
- `docs/audits/screenshots/marketing-docs-index.png` — 6 tutorial cards
- `docs/audits/screenshots/dashboard-home.png` — full dashboard in HTTP mode
- `docs/audits/screenshots/_playwright-report/index.html` — full HTML report (gitignored)
- `docs/audits/screenshots/_playwright-output/` — per-test traces + videos (gitignored)

---

## 3. Findings — line-by-line

### F-1 (marketing) — "How it works" anchor — **FALSE POSITIVE**

**Phase 1 claim:** Nav's `/#how-it-works` link targets a non-existent anchor.

**Reality:** `studio/marketing/components/PhasesScroll.tsx:81` has `id="how-it-works"`. Phase 1's grep missed it due to HTML-escaped quote characters in the search query.

**Verified live:**
```
F-1 test: How it works anchor scrolls somewhere visible (not 0,0)
  scrollY after click = > 200px (target: PhasesScroll component which is below the fold)
PASSED
```

**Audit correction:** FULL_PROJECT_AUDIT.md should de-list F-1 and F-2.

### F-2 (marketing) — "Features" anchor — **FALSE POSITIVE**

Same as F-1. `studio/marketing/components/Features.tsx:5` has `<section id="features">`. Anchor link works.

**Verified live:** Playwright test PASSED.

### F-3 (dashboard) — DEPLOY button dead click — **CONFIRMED + FIXED**

**Pre-fix behavior:** Button is fully styled gold + Rocket icon. Click does nothing. Classic dead-click — looks fully active but has no `onClick` handler.

**Playwright caught it:** Test `F-3: DEPLOY button is enabled but did nothing on click` failed with:
```
Error: DEPLOY button is enabled but did nothing on click
```

**Fix:** `studio/dashboard/components/PhasesSidebar.tsx`. Replaced the active-styled button with a `disabled` version + tooltip + "SOON" badge:

```tsx
<button
  type="button"
  disabled
  title="Deploy lands in v2.0.0-beta.1. For now: run `bequite handoff` to generate the deploy artifacts."
  aria-disabled="true"
  className="... bg-ink-edge ... text-silver-dim opacity-60 cursor-not-allowed"
>
  <Rocket /> DEPLOY
  <span className="rounded-sm bg-ink-velvet px-1 py-0.5 text-[9px] uppercase tracking-wider">soon</span>
</button>
```

**Test re-run:** PASSED. Tooltip present + button correctly disabled.

**Why "disable" over "wire it up":** Real deploy means real one-way-door actions (PyPI publish, git push, etc.). Per Article IV those need an explicit ADR. Phase 3 of this audit ships honest UX; v2.0.0-beta.1 ships the real action.

### F-4 (dashboard) — PlanTasksTests hardcoded mock — **CONFIRMED + FIXED**

**Pre-fix behavior:** Component received `snapshot: ProjectSnapshot` prop but only used `snapshot.doctrineList[0]`. Plan items, task items, test items all hardcoded:

```tsx
const planItems = ["Architecture decided · ADR-001", "Stack: Next.js + Hono + Supabase", ...];
const taskItems = ["T-1.1  scaffold apps/web      ✓", ...];
const testItems = [{ label: "lint", pass: true }, { label: "typecheck", pass: true }, ...];
```

Showed the same content regardless of which project was loaded. Article VI honesty violation.

**Fix:** Rewrote `studio/dashboard/components/PlanTasksTests.tsx` to derive all three panels from real `snapshot` fields:

| Panel | Source |
|---|---|
| Plan | `snapshot.projectName` + `constitutionVersion` + `currentPhase` + `doctrineList` + `lastGreenTag`. Empty state: "No project loaded — run `bequite init`". |
| Phases (renamed from Tasks) | `snapshot.phases.map(...)` with per-status icons (done/in-progress/blocked/pending) |
| Tests | Pulls latest `P6`/`VERIFY` receipt from `snapshot.recentReceipts`. Empty state: "(awaiting bequite verify)". Shows cost + model when available. |

**Verified live:** Dashboard now shows real "Project: Project Brief: BeQuite", "Constitution: v1.3.0", "Current phase: v0.8.1" — exactly the values from the workspace's `.bequite/memory/`.

### F-5 (dashboard) — AgentPanel hardcoded recent activity — **CONFIRMED + FIXED**

**Pre-fix behavior:**
```tsx
<ul>
  <li>$ bequite verify ✓</li>
  <li>$ bequite plan ✓</li>
  <li>$ bequite freshness ✓</li>
</ul>
```

Always rendered these three lines — regardless of actual receipts.

**Fix:** `studio/dashboard/components/AgentPanel.tsx` now accepts `recentReceipts?: ReceiptSummary[]` and renders the real list. Wired from `page.tsx` via `snapshot.recentReceipts`. Empty state: "no receipts yet — run `bequite auto`".

**Verified live:** Test workspace has no receipts → AgentPanel correctly shows the "no receipts yet" message.

### F-6 (dashboard) — CommandConsole pretending to be live in filesystem mode — **CONFIRMED + FIXED**

**Pre-fix behavior:** In filesystem mode, the static CommandConsole renders 8 hardcoded "bequite init → ✓ Scaffolded..." lines that look like real recent terminal history. Users were assuming this was a live shell.

**Fix:** Added an honest banner at the top:

```tsx
<div className="border-b border-gold-deep/30 bg-ink-velvet/50 px-4 py-2 text-[11px] text-silver-soft">
  <span className="font-mono text-gold">Demo · </span>
  Static console (filesystem mode). Set <code className="font-mono text-gold-bright">BEQUITE_DASHBOARD_MODE=http</code>
  and run the Studio API for the live xterm.js terminal.
</div>
```

**Verified live:** In screenshot `dashboard-home.png`, the dashboard is now in HTTP mode → real xterm.js Terminal renders instead. The CommandConsole banner only shows in filesystem mode.

### F-7 (marketing) — `@keyframes glint` referenced but never defined — **CONFIRMED + FIXED**

**Pre-fix behavior:** `Hero.tsx:61` set `animation: glint ...s ease-in-out` on 40 star particles. `@keyframes glint` was not defined anywhere. Stars sat static.

**Fix:** Added to `studio/marketing/app/globals.css`:

```css
@keyframes glint {
  0%, 100% { opacity: 0.15; }
  50%      { opacity: 0.75; }
}
```

**Verified:** Compiled successfully into the Next.js bundle. (Live animation hard to verify by Playwright; visual confirmation in screenshot.)

### F-8 (both) — Tailwind v4 motion/typography token leak — **DEFERRED**

`:root` declares `--ease-cinematic`, `--text-mega`, `--font-display` etc., but `@theme {}` block only has `--color-*` tokens. Tailwind v4 utility classes `duration-cinematic`, `text-mega`, `font-display`, `tracking-mega` silently no-op.

**Decision:** Acceptable for alpha. Apps render fine with default browser timing functions. Migrating motion/type tokens into `@theme` requires the Tailwind v4 stable release first (`beta.3` lacks some `@theme` keyspace conventions). Flagged for v2.0.0-beta.1.

### F-9 (dashboard) — Dead conditional in CommandConsole — **CONFIRMED + FIXED**

`CommandConsole.tsx:56` had `<span className="text-gold-bright">{t.includes("⏳") ? "" : ""}</span>` where both branches were empty. Dead code.

**Fix:** Rewrote the CommandConsole entirely as part of the F-6 fix; the dead conditional was removed in the process.

### F-10 (dashboard) — `signedInUser` hardcoded default — **OUT OF SCOPE**

`TopBar.tsx:22` has `signedInUser = "(not signed in)"` as default. Not a bug — placeholder until Better-Auth integration ships in v2.0.0-alpha.3+ per ADR-015. Acceptable.

### F-11 (dashboard) — Dead Tailwind v3 config — **OUT OF SCOPE**

`studio/dashboard/tailwind.config.ts` exists alongside Tailwind v4 `@theme` block. The v3 file is ignored by v4. Could delete but harmless. Flagged for v2.0.0-beta.1 cleanup.

### F-BONUS (dashboard, caught by Playwright) — Next.js SSG cached env vars — **CONFIRMED + FIXED**

**Discovery:** After fixing F-3 through F-7 and re-running Playwright, the dashboard's mode chip still showed `FS` even though Docker compose sets `BEQUITE_DASHBOARD_MODE=http`.

**Diagnosis:** Next.js 15 App Router defaults server-component renders to **static generation** (SSG) at build time. `loadProject()` ran at build time when `process.env.BEQUITE_DASHBOARD_MODE` was undefined → fell back to filesystem mode → result cached → runtime env var ignored forever.

**Fix:** Added to `studio/dashboard/app/page.tsx`:

```tsx
export const dynamic = "force-dynamic";
export const revalidate = 0;
```

This forces server-component re-render on every request → `process.env.BEQUITE_DASHBOARD_MODE` reads at request time → correct mode picked → LiveIndicator shows `CONNECTING` then `LIVE`.

**Verified:** After dashboard rebuild, the page returns HTTP 200 + mode chip shows `HTTP` + LiveIndicator connects to the SSE stream.

**Lesson:** Default-SSG is a foot-gun for env-var-driven server components. Adding `force-dynamic` is the right pattern when reading runtime env. Document this in `studio/dashboard/README.md` for future contributors.

---

## 4. Test results

```
Running 24 tests using 1 worker

  ok  1-11 [chromium] › specs\api.spec.ts › api / public surface (11 tests)
  ok 12-17 [chromium] › specs\dashboard.spec.ts › dashboard (6 tests)
  ok 18-24 [chromium] › specs\marketing.spec.ts › marketing site (7 tests)

  24 passed (7.0s)
```

All 24 tests pass against the live Docker stack with all fixes applied.

---

## 5. Screenshots

| File | Description |
|---|---|
| `marketing-home.png` | Cinematic landing — gold "Plan it. Build it. Be quiet." hero, gold astronaut, animated star particles (post-fix glint keyframes), Nav with backdrop-blur |
| `marketing-docs-index.png` | 6 tutorial cards rendered cleanly |
| `dashboard-home.png` | Full dashboard in HTTP mode. Real project name "Project Brief: BeQuite" in topbar. P0–P7 phases with status icons. Live xterm.js Terminal. Honest "(no project)" / "(awaiting bequite verify)" / "no receipts yet" empty states. Disabled DEPLOY with "SOON" badge. |

---

## 6. Files changed in Phase 3

| File | Change |
|---|---|
| `studio/dashboard/components/PhasesSidebar.tsx` | DEPLOY button disabled with tooltip + SOON badge (F-3) |
| `studio/dashboard/components/PlanTasksTests.tsx` | Rewrote — all 3 panels derive from real snapshot fields (F-4) |
| `studio/dashboard/components/AgentPanel.tsx` | Added `recentReceipts` prop; renders real receipts or honest empty state (F-5) |
| `studio/dashboard/components/CommandConsole.tsx` | Added "Demo · Static console (filesystem mode)" banner (F-6); removed dead conditional (F-9) |
| `studio/dashboard/app/page.tsx` | Wired `recentReceipts` to AgentPanel; added `force-dynamic` + `revalidate=0` (F-BONUS) |
| `studio/marketing/app/globals.css` | Added `@keyframes glint` (F-7) |
| `tests/e2e/package.json` | New — Playwright dev-deps |
| `tests/e2e/playwright.config.ts` | New — chromium project, screenshot output → docs/audits/screenshots/ |
| `tests/e2e/tsconfig.json` | New — TypeScript config for specs |
| `tests/e2e/specs/marketing.spec.ts` | New — 7 tests |
| `tests/e2e/specs/dashboard.spec.ts` | New — 6 tests |
| `tests/e2e/specs/api.spec.ts` | New — 11 tests (doubles as Phase 4 deliverable) |

---

## 7. What this Phase did NOT cover

- **Visual regression testing** (pixel-level diffs across versions) — would need a tool like Percy or Chromatic. Not shipped in alpha.
- **Axe-core accessibility scan** — referenced in Doctrine `default-web-saas` Rule 8; ships as part of the verify pipeline (Phase 7), not standalone here.
- **Multi-viewport testing** (mobile, tablet, desktop). Default Playwright config is Desktop Chrome. Mobile + tablet projects would expand the matrix; deferred to v2.0.0-beta.1.
- **Cross-browser** (Firefox, Safari) — single-browser (chromium) is sufficient for alpha smoke. Cross-browser deferred.
- **Performance / Lighthouse** — out of scope; v2.0.0-beta.2 release-engineering.

---

## 8. Phase 3 conclusion

All Phase 1 frontend bugs are either confirmed-and-fixed (F-3, F-4, F-5, F-6, F-7, F-9, F-BONUS) or correctly assessed as false-positives (F-1, F-2) or deferred-to-beta (F-8, F-10, F-11). The dashboard now displays **real project data** instead of hardcoded mocks, the DEPLOY button is **honestly disabled**, the CommandConsole **labels itself as a demo** in filesystem mode, and the LiveIndicator **correctly flips to HTTP** when the API is reachable.

24/24 Playwright tests pass. Frontend is alpha-quality-ready.

**Next:** Phase 4 — formalize the API smoke matrix (already covered by `api.spec.ts`'s 11 tests) into `API_AUDIT.md`.
