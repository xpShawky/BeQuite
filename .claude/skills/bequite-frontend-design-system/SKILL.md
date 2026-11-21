---
name: bequite-frontend-design-system
description: Use when building, redesigning, auditing or editing any page or app screen with more than one section, or any time a frontend must not look AI-made. Starts from measured human references, locks a Design DNA, builds section by section with a check after each, and verifies in a real browser at desktop and phone width. Master skill; it calls ux-ui-designer, frontend-quality and live-edit.
last_verified: 2026-11-21
sources:
  - https://web.dev/articles/vitals (read 2026-11-21) LCP 2.5 s, INP 200 ms, CLS 0.1 at p75
  - https://www.w3.org/TR/WCAG22/ (read 2026-11-21) contrast 4.5:1 and 3:1, target size 24 px, focus not obscured
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations (read 2026-11-21) Baseline 2026, newly available
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle (read 2026-11-21) resolved values for measuring
  - https://code.claude.com/docs/en/best-practices (read 2026-11-21) screenshot next to the target as the check
  - https://www.awwwards.com/websites/sites_of_the_day/ (read 2026-11-21) reference source, live on the day
  - https://linear.app, https://stripe.com, https://www.apple.com/airpods-pro/ (measured 2026-11-21) reference values in references/reference-first.md
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, WebFetch, WebSearch
---

# bequite-frontend-design-system

AI-made pages start strong at the hero and drift into generic cards by the middle, because the design lives only in the chat and the model falls back to its averages. This skill fixes that with three things: measured references before any design, a written DNA every section is checked against, and checks done by looking at the rendered page, not by reading the code.

## When to use

- New pages, redesigns, landing pages, dashboards, multi-section edits; `/bq-uiux-variants`, `/bq-feature` with a visible page, `/bq-live-edit` beyond one section, `/bq-audit` of a frontend.

Not for: a one-line tweak in one section (`bequite-live-edit` directly), backend work, projects with no UI.

## Who does what

| Need | Skill |
|---|---|
| Tokens, type, colour, layout decisions per section | `bequite-ux-ui-designer` |
| Tell sweep, accessibility and performance checks | `bequite-frontend-quality` |
| Editing a running app section by section with the browser | `bequite-live-edit` |

## Procedure

1. **References first** (`references/reference-first.md`). Use the user's references; otherwise collect 3 to 10 from the galleries listed there, show the set, and wait for a yes or a swap. Measure each live page in a browser tool: type, weights, colours, radii, motion media, the phone view. Numbers only. Tick `REFERENCES_STUDIED`.
2. **DNA.** Write or update `.bequite/design/DESIGN_DNA.md` from the measurements: rules with one measured example each, the never-list, the product type (`references/product-type-rules.md`). Lock it (`DESIGN_DNA_LOCKED`) before UI code.
3. **Section map.** `.bequite/uiux/SECTION_MAP.md`: every section with its job and acceptance criteria.
4. **Build one section, then look at it.** Render it in the browser (`bequite-live-edit` tiers), screenshot desktop and 375 x 812, run the tell sweep. Compare with the references side by side. Fix before the next section.
5. **Next section** is checked against the DNA and against the sections already built.
6. **Continuity audit** of the whole page: `references/design-continuity-checklist.md` → `.bequite/design/DESIGN_CONTINUITY_REPORT.md` (`DESIGN_CONTINUITY_PASS`).
7. **Accessibility and performance**: WCAG 2.2 AA (contrast 4.5:1 text, 3:1 large text and UI parts, targets at least 24 x 24 px, focus visible and not hidden); Core Web Vitals at p75 on mobile (LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1). Motion pages also load `references/web-motion.md` and set `PERF_BUDGET_PASS`.
8. **Visual QA** (`references/visual-qa-checklist.md`) → `.bequite/audits/VISUAL_QA_REPORT.md` (`VISUAL_QA_DONE`).
9. **Human test.** The side-by-side with three references, the tell sweep record and the phone check go in `evidence.md`; the owner's verdict closes it. Each correction becomes a DNA rule.

Keep `.bequite/state/FRONTEND_CONTEXT_SUMMARY.md` current after each section (font, colours, spacing, product type), so later sections read one screen instead of the chat.

## Worked example (real run, 2026-11-21)

References measured in the browser (full table in `references/reference-first.md`): Linear h1 64 px / 510 / -1.408 px; Stripe h1 48 px / 300 / -0.96 px; Apple cards at 28 px radius with 16 videos and 4 sticky scenes. DNA rules taken: headline tracking about -2%, medium weight; a grey ramp; radius by component size; never gradient headline text or numbered section labels.

A clinic-booking test page was built the AI-default way, then checked in the browser pane at 375 x 812:

| | Before | After (DNA applied) |
|---|---|---|
| h1 on phone | 72 px, weight 800, gradient text, 5 lines | 36 px (clamp), weight 560, -0.792 px, 4 lines |
| h1 on desktop | 72 px | 64 px, -1.408 px, 2 lines |
| Feature grid on phone | 3 columns, cards clipped | 1 column (`auto-fit, minmax(240px, 1fr)`) |
| Tell sweep hits | 5 (gradient text, purple-blue, `01 /` labels x3, 300/800 weights, one radius) | 1 (one radius: one component type, justified) |
| Copy | "Unlock the Future of Clinic Bookings" | "Bookings, reminders and deposits for small clinics" |

## Quality gate

- `references.md` (or the DNA header) lists the references with measured numbers; no adjectives-only blocks.
- Every built section has a desktop and a phone screenshot and a tell-sweep result; every hit is fixed or justified in one line.
- Continuity report and visual QA report exist with no open BLOCKER or HIGH item.
- Contrast, target size and focus were checked on the rendered page; Web Vitals measured where the page is deployed or previewed.
- No claim that the page "looks human": the evidence is the test record and the owner's verdict.

## Boundaries

- Learn a manner from references; never copy a site's assets, copy or code.
- Fonts, libraries and component kits are candidates; never installed without the user's yes.
- The owner picks between design variants (hard human gate).

## References (load on demand)

- `references/reference-first.md`: where to look, what to measure, the measured reference table.
- `references/design-continuity-checklist.md` · `references/visual-qa-checklist.md` · `references/product-type-rules.md` · `references/design-dna-template.md`
- `references/web-motion.md` (motion budget and device tiers) · `references/cinematic-ui-checklist.md` · `references/mobile-app-ui-checklist.md`
- Tell list and sweep script: `.claude/skills/bequite-frontend-quality/references/ai-tells.md`, `tell-sweep.js`
- Older research notes: `references/impeccable-notes.md`, `references/ui-ux-pro-max-notes.md`, `references/superpowers-notes.md`; worked files in `examples/`.
