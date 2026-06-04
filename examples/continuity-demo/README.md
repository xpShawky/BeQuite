# Design Continuity Gate — dogfood validation

**Purpose:** prove the alpha.17 Design Continuity Gate actually *catches* middle-section drift on a rendered multi-section page — not just that it exists and is wired. This is the live-UI validation that `.bequite/audits/VERIFY_REPORT.md` flagged as the honest next step. ("BeQuite eats its own food" — CLAUDE.md rule 14.)

**Product under test:** "Cadence" — a running-coach app marketing landing page. Zero dependencies — plain self-contained HTML/CSS (no framework, no npm, no build). Open either file directly in a browser.

## Files

| File | What it is |
|---|---|
| `DESIGN_DNA.md` | The locked visual identity Cadence ships against |
| `before-drifted.html` | Hero is polished; sections 2–4 deliberately drift (the failure this whole upgrade targets) |
| `after-fixed.html` | Same page, every section pulled back to the DNA |
| `DESIGN_CONTINUITY_REPORT.md` | The gate run: FAIL on `before`, PASS on `after`, with the exact drift tells + CSS line evidence |
| `VISUAL_QA_REPORT.md` | Tier-3 (code-inspection) visual QA — honestly labeled; no browser automation was available this session |

## How to read the result

1. Open `before-drifted.html` — the hero looks intentional; scroll down and the Features grid, the "How it works" band, and the Testimonials degrade (generic cards, ALL-CAPS wide-tracked titles, an off-DNA purple→pink gradient, gray-on-clay text, a 32px radius blob, uneven spacing). That is exactly "the hero is good, the middle is filler."
2. `DESIGN_CONTINUITY_REPORT.md` shows the gate flagging each of those with severity + the CSS that triggers it + the quality-cliff verdict (hero strong, sections 2–4 below the bar).
3. Open `after-fixed.html` — every section now uses the DNA tokens; the gate re-runs to PASS.

## Honest boundary

No pixel screenshots were captured — there is no Playwright/browser MCP in this session, so visual QA ran at **tier 3 (code inspection)**, which the skill explicitly permits and which this report labels as such. The drift tells here are determinable from the markup with certainty (e.g. `letter-spacing: 0.22em` on a 3-word heading *is* the wide-tracking tell regardless of render). To capture screenshots, run the gate in a host with a browser tool available; the `after` page is built to pass that too.

The independent audit in `DESIGN_CONTINUITY_REPORT.md` § "Independent verification" was produced by a fresh subagent that read both HTML files against the DNA + `references/design-continuity-checklist.md` — not by self-assessment.
