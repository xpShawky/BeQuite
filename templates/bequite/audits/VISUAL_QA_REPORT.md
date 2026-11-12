# Visual QA Report

Browser-or-manual render verification for a frontend. Code inspection alone does not catch middle-section drift — you have to render the page and look at section 5. Owner skill: `bequite-frontend-design-system`; browser tiers from `bequite-live-edit`.

**Project:** `<name>`
**Generated:** `<ISO 8601 UTC | "template — not yet run">`
**Inspection tier used:** `<Playwright MCP | project Playwright | code inspection + user screenshots>`
**Dev URL:** `<http://localhost:3000 | n/a>`
**Overall:** `<PASS | PARTIAL | FAIL | template>`

---

## Inspection strategy (highest available tier — never auto-install)

1. **Playwright MCP** (`mcp__playwright__*`) — preferred when available in the agent host.
2. **Project Playwright** — if `@playwright/test` already in devDependencies, drive via a script.
3. **Code inspection + screenshots** — Read/Grep the source; ask the user for screenshots when visual context matters. Document manual steps.
4. **Claude Code bundled run/verify** — use if available.

Do **not** install Playwright for a visual QA pass. If the project genuinely needs it, surface a decision section; otherwise use tier 3.

---

## Checklist (per route)

```markdown
### Route: /<path>   — tier: <MCP | project | code+manual>

| Check | Result | Evidence |
|---|---|---|
| Route loads (200, renders) | ✅ / ❌ | <status / note> |
| No console errors | ✅ / ❌ | <count + messages> |
| No network errors (4xx/5xx on load) | ✅ / ❌ | <list> |
| All important buttons clickable (have handlers) | ✅ / ❌ | <dead clicks found> |
| Text visible (no color≈bg, no overflow/clipping) | ✅ / ❌ | <where> |
| No text escaping containers | ✅ / ❌ | <where> |
| First section quality | ✅ / ⚠ / ❌ | <note> |
| **Middle sections quality (each)** | ✅ / ⚠ / ❌ | **<the drift hotspot — list each middle section + verdict>** |
| Final sections quality | ✅ / ⚠ / ❌ | <note> |
| Responsive 360 (mobile) | ✅ / ❌ | <overflow? touch targets ≥44px?> |
| Responsive 768 (tablet) | ✅ / ❌ | <note> |
| Responsive 1440 (desktop) | ✅ / ❌ | <note> |
| Mobile view usable (thumb zones, no h-scroll) | ✅ / ❌ | <note> |
| Dark/light contrast (if relevant) | ✅ / ❌ / n/a | <WCAG 2.2 AA: body 4.5:1, large/UI 3:1> |
| Empty / loading / error states render usefully | ✅ / ❌ | <which mocked> |

**Screenshots:** <.bequite/uiux/screenshots/qa-<route>-<viewport>-<ts>.png ...>
**Route verdict:** <PASS | PARTIAL | FAIL>
```

---

## Routes

(no routes inspected yet — populated when visual QA runs against a real frontend)

---

## Failures & follow-ups

| # | Route | Failure | Severity | Action |
|---|---|---|---|---|
| (none yet) | | | | |

---

## Honesty note (Article VI)

State what actually ran, in this session, against this code. If browser automation was unavailable, say "tier 3 — code inspection; visual confirmation requested from user," not "PASS." Do not claim a visual PASS you did not see. Banned weasel words apply.

**Final status:** `template — not yet run`
