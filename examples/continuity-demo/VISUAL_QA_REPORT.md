# Visual QA Report — Cadence continuity-demo

**Generated:** 2026-06-04 (UTC)
**Inspection tier used:** **Tier 3 — code inspection** (no Playwright/browser MCP available in this session; the skill explicitly permits tier 3 and requires it be labeled as such — Article VI). No pixel screenshots were captured.
**Files:** `before-drifted.html`, `after-fixed.html` (self-contained static HTML/CSS, zero dependencies — open directly in a browser).
**Overall:** `before` = FAIL · `after` = PASS

> Honesty note: the drift here is determinable from the markup with certainty — `letter-spacing:0.22em` on a 3-word heading IS the wide-tracking tell, `#9ca3af` on `#b14a2e` IS 2.13:1, regardless of render. What tier 3 cannot do is catch render-only surprises (font fallback metrics, sub-pixel overflow). To capture screenshots and confirm pixel-level layout, run this in a host with Playwright MCP — the `after` page is built to pass that too.

---

### Route: before-drifted.html — tier 3

| Check | Result | Evidence |
|---|---|---|
| File loads / valid HTML | ✅ | self-contained, no external assets |
| No console / network errors | ✅ | no scripts, no fetches |
| Buttons clickable | ⚠ | CTAs are `<a href="#">` (placeholder, demo) — present, not dead-styled |
| Text visible (no color≈bg) | ❌ | Testimonials quote `#9ca3af` on clay = 2.13:1 — effectively hidden |
| No text escaping containers | ❌ | `.overflow-note` 220px fixed width + long unbroken token, no wrap guard |
| Hero quality | ✅ | on-DNA, Fraunces, clay CTA |
| Middle: Features | ❌ | nested cards + ALL-CAPS 0.22em titles |
| Middle: How it works | ❌ | purple→pink gradient + 01/02/03 eyebrows + 36px blob |
| Middle: Testimonials | ❌ | gray-on-clay quote (2.13:1) |
| Final: Footer | ✅ | on-DNA |
| Responsive 360 | ⚠ | `.feat-grid`/`.steps` are fixed `repeat(3,1fr)` — will crowd at 360 (not the focus of this demo, but flagged) |
| Dark/light contrast (WCAG 2.2 AA) | ❌ | multiple < 4.5:1 on clay/gradient (see continuity report rows 9–11) |
| Empty/loading/error states | n/a | marketing page; no data states |

**Route verdict: FAIL** — the middle is below the hero; primary testimonial text is illegible.

---

### Route: after-fixed.html — tier 3

| Check | Result | Evidence |
|---|---|---|
| File loads / valid HTML | ✅ | self-contained |
| No console / network errors | ✅ | no scripts |
| Buttons clickable | ✅ | CTA present |
| Text visible | ✅ | blockquote `--paper` on clay = 5.02:1; cite `--paper` = 5.02:1 |
| No text escaping containers | ✅ | `.tag{min-width:0;overflow-wrap:anywhere}` + short token |
| Hero quality | ✅ | unchanged, on-DNA |
| Middle: Features | ✅ | single-depth cards, sentence-case Fraunces titles |
| Middle: How it works | ✅ | paper band, clay numerals, hairline steps, 4/8 spacing |
| Middle: Testimonials | ✅ | on-color text, overflow guarded |
| Final: Footer | ✅ | on-DNA |
| Responsive 360 | ⚠ | grids still `repeat(3,1fr)` — acceptable for the demo; a production page would add a 360 breakpoint (out of scope) |
| Dark/light contrast (WCAG 2.2 AA) | ✅ | body 5.28:1 on paper; quote/cite 5.02:1 on clay; footer 4.85:1 |
| Empty/loading/error states | n/a | marketing page |

**Route verdict: PASS** (the one `cite` residual at 4.17:1 was caught and closed → 5.02:1).

---

## Failures & follow-ups

| # | Route | Failure | Severity | Action |
|---|---|---|---|---|
| 1 | before | gray-on-clay quote 2.13:1 | BLOCKER | fixed in `after` → 5.02:1 |
| 2 | before | purple→pink gradient (off-DNA) | BLOCKER | fixed in `after` → paper band |
| 3 | before | nested cards | BLOCKER | fixed in `after` → one depth |
| 4 | both | grids fixed at 3 columns (360px crowding) | LOW | out of scope for this gate demo; note for a production build |

**Final status:** the gate + tier-3 visual QA correctly separate the drifted page (FAIL) from the consistent page (PASS). For pixel-screenshot evidence, re-run in a browser-enabled host.
