# Visual QA Checklist

Purpose: render the frontend and look at it — code inspection alone misses middle-section drift (generic cards, all-caps misuse, wide tracking, text overflow, lost identity).

Sibling references: `design-dna-template.md` (identity contract), the section-by-section loop (in `../SKILL.md`), `design-continuity-checklist.md` (the gate this feeds), `product-type-rules.md` (per-product checks).

---

## Browser inspection tiers

Use the highest tier available. NEVER auto-install a browser, Playwright, or any dependency to climb a tier — drop to a lower tier and say so.

| Tier | Tool | Use when | Capability |
|---|---|---|---|
| 1 | Playwright MCP (`mcp__playwright__*`) | MCP server is connected | Navigate, click, screenshot, read console + network — full visual pass |
| 2 | Project Playwright in `devDependencies` | Repo already lists `@playwright/test` / `playwright` | Run existing scripts; screenshot via project config |
| 3 | Code inspection + ask user for screenshots | No browser tool available | Read source, reason about render; request user screenshots per route |
| 4 | Claude Code bundled `/run` + `/verify` | Those commands exist this session | Launch app, smoke render, capture what the harness exposes |

Tier rule: try 1, then 2, then 4; if none, use 3 and request screenshots. Record the tier used in the report.

---

## Per-route checklist

Run for EVERY route. Result = PASS / FAIL / NOT-CHECKED. Evidence = screenshot filename, console excerpt, or "code inspection".

| Check | Result | Evidence |
|---|---|---|
| Route loads (HTTP 200 / renders without crash) | | |
| No console errors | | |
| No network errors (no 4xx / 5xx on load) | | |
| All important buttons clickable (real handlers — no dead clicks) | | |
| Text visible (no `color ~= background`, no clipping) | | |
| No text escaping containers (overflow / wrap correct) | | |
| FIRST section quality (hero / top) | | |
| MIDDLE section 1 quality — DRIFT HOTSPOT | | |
| MIDDLE section 2 quality — DRIFT HOTSPOT | | |
| MIDDLE section 3 quality — DRIFT HOTSPOT (list each middle section) | | |
| FINAL section quality (footer / CTA / closing) | | |
| Responsive @ 360px | | |
| Responsive @ 768px | | |
| Responsive @ 1440px | | |
| Mobile usable (thumb zones, no horizontal scroll, touch targets >=44px) | | |
| Dark/light contrast — WCAG 2.2 AA | | |
| Empty state renders usefully | | |
| Loading state renders usefully | | |
| Error state renders usefully | | |

List every middle section explicitly. Do not collapse them into one row — the middle is where AI frontends drift (generic cards, all-caps misuse, wide letter-spacing, text overflow, lost identity, code-looking output).

### Middle-section drift signals (look for these)

- Generic SaaS card grid that ignores Design DNA
- All-caps on more than 4-word labels, or tracking outside 0.05–0.12em
- Body text below 16px, or measure outside 45–75ch
- Heading line-height outside 1.1–1.2; body outside 1.5–1.7
- Text clipped or escaping its container at any viewport
- Purple/pink "AI gradient" or palette that drifts from brand
- Placeholder / lorem / code-looking output shipped as real content

---

## WCAG 2.2 AA numbers (contrast + touch)

| Item | Threshold |
|---|---|
| Body text contrast | 4.5:1 |
| Large text (18px+, or 14px bold) | 3:1 |
| UI components / focus indicators | 3:1 |
| AAA (where dashboard critical actions lean stricter) | 7:1 body / 4.5:1 large |
| Touch target — Apple HIG | 44 x 44 pt |
| Touch target — Android Material | 48 x 48 dp |
| Touch target — WCAG 2.2 floor | 24 x 24 CSS px |
| Spacing between targets | >= 8 dp |

Spacing uses the 4/8pt scale.

---

## Screenshot naming

Save under `.bequite/uiux/screenshots/`:

```
qa-<route>-<viewport>-<ts>.png
```

Examples:
- `qa-home-360-20260603T1430.png`
- `qa-dashboard-1440-20260603T1431.png`

---

## Honesty note (Article VI)

State what actually ran THIS session.

- If a browser tier (1, 2, or 4) ran: report screenshots and observed results.
- If tier 3: write `code inspection; visual confirmation requested` — never claim a visual PASS you did not see.
- No banned weasel words (should / probably / seems to / appears to / might / hopefully / in theory). Replace with concrete evidence or an explicit "not verified".

---

## Worked example — ClinicFlow

ClinicFlow = clinic booking platform: a public MARKETING LANDING PAGE + an internal STAFF DASHBOARD. Brand: trustworthy, calm, efficient; calm clinical teal (OKLCH), tinted-neutral backgrounds, NO purple/pink AI gradients. WCAG: AA for marketing, lean AAA for dashboard critical actions.

1. Landing page `/` — middle "Features" section flagged: generic 3-card grid with all-caps 6-word headings at 0.2em tracking. FAIL. Evidence `qa-home-1440-20260603T1430.png`. Fix per `design-continuity-checklist.md`; re-shoot.
2. Dashboard `/staff/schedule` — booking-confirm button checked for AAA contrast (7:1 teal-on-tinted-neutral) and 44x44pt touch target. PASS via Tier 1. Evidence `qa-schedule-1440-20260603T1432.png`.
3. Dashboard `/staff/patients` empty state — no patients renders a useful prompt, not a blank pane. Tier 3 this session: `code inspection; visual confirmation requested`.

---

## Output + gate

- Write findings to `.bequite/audits/VISUAL_QA_REPORT.md` (route list, per-check table, tier used, screenshots, honesty note).
- On full PASS with visual confirmation, set the `VISUAL_QA_DONE` gate in `.bequite/state/WORKFLOW_GATES.md`.

---

## Effort awareness

| Effort | Scope |
|---|---|
| low / medium | Spot-check the weakest middle sections only |
| high | Full per-route checklist for every route |
| xhigh / Ultracode | Browser pass (Tier 1/2) + screenshots per section |
