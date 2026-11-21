---
name: bequite-frontend-quality
description: Use when a frontend is about to be called done, reviewed, audited or shipped, or when a page "looks AI-made". Runs the owner's AI-tell sweep on the rendered page, checks accessibility (WCAG 2.2 AA) and Core Web Vitals, and checks for dead buttons, fake data and missing states, all measured in a real browser with every hit fixed or justified.
last_verified: 2026-11-21
sources:
  - https://www.w3.org/TR/WCAG22/ (read 2026-11-21) AA contrast, target size, focus
  - https://web.dev/articles/vitals (read 2026-11-21) LCP, INP, CLS thresholds at p75
  - https://web.dev/articles/optimize-inp (read 2026-11-21) input delay, processing, presentation
  - https://webaim.org/projects/million/ (read 2026-11-21) 2026 report, 95.9% home pages fail, low contrast 83.9%
  - https://github.com/dequelabs/axe-core (read 2026-11-21) v4.14.1, finds about 57% of WCAG issues automatically
  - https://github.com/ChromeDevTools/chrome-devtools-mcp (read 2026-11-21) v1.13.0, traces, network, console
  - https://github.com/pbakaus/impeccable (read 2026-11-21) named anti-patterns, deterministic detector
  - https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing (read 2026-11-21) copy tells
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, WebFetch, WebSearch
---

# bequite-frontend-quality

A page can pass the build and still fail people: grey text nobody can read, a button that does nothing, a chart with invented numbers, the same purple gradient every generated page has. This skill finds those on the rendered page, with numbers, and does not accept "looks fine to me".

## When to use

- Before a frontend task is marked done (`/bq-feature`, `/bq-live-edit`, `/bq-uiux-variants`), in `/bq-review`, `/bq-audit`, `/bq-red-team` of a UI, and in `/bq-verify`.
- When the user says the page looks generic or AI-made.

Not for: designing from scratch (`bequite-ux-ui-designer`) or the section loop (`bequite-frontend-design-system`).

## Procedure

1. **Render it.** Open the page in a browser tool (tiers in `bequite-live-edit`). Measure at desktop width and at 375 x 812 with real emulation; a hidden or 0x0 viewport gives wrong numbers.
2. **Console and network**: zero errors on load; no 4xx or 5xx except expected auth probes.
3. **Tell sweep.** Run `references/tell-sweep.js` in the page (read-only). Then the manual rows of `references/ai-tells.md` from a full-page screenshot. For each hit: fix it, or write one line of justification naming the reference or brand rule. Human sites hit some tells too (Stripe's brand purple trips the gradient check six times), so the count alone is not the verdict; defaults and dominance are.
4. **Copy.** Read every visible string against the copy tells (vague claims, "seamless", groups of three, a moral at the end). Replace with concrete facts from the product.
5. **Honest data and states.** No invented chart numbers or fake "live" counters; every list has empty, loading, error and success states, each reachable and shown on screen. A skeleton that never resolves becomes an error state.
6. **Interaction.** Click every primary button and link in the changed area; each does something visible. Tab through: focus is visible and never hidden behind sticky bars.
7. **Accessibility** (WCAG 2.2 AA): text contrast 4.5:1 (3:1 large), UI parts 3:1, targets at least 24 x 24 CSS px, labels on inputs, alt text, one h1. Run an automated checker if the project has one (axe-core finds about 57% of issues by its maker's count); do the rest by hand. Low contrast is the most common failure on the web (83.9% of home pages, WebAIM 2026), so check it first.
8. **Performance.** Core Web Vitals at p75 on mobile: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1. Use field data where the site is live, a lab trace (Lighthouse or a DevTools trace tool) for previews. For slow interactions, split the time into input delay, processing and presentation, and fix the largest part.
9. **Report** in `.bequite/audits/VISUAL_QA_REPORT.md`: measured values, screenshots (desktop and phone), each tell hit with its fix or justification, open items by severity.

## Worked example (real run, 2026-11-21)

Sweep on a clinic-booking test page in the built-in browser pane, 375 x 812:

```
before: tellsFound {gradientHeadlineText:1, purpleToBlueGradients:1, numberedSectionLabels:3,
                    thinBodyBoldHeadings:"body 300 / headings 800", oneRadiusEverywhere:"24px"}
        h1 72px/800, 5 lines; grid clipped; copy "Unlock the Future of Clinic Bookings"
after:  tellsFound {oneRadiusEverywhere:"12px"}  -> justified: one component type on the page
        h1 36px/560/-0.792px, 4 lines; horizontalScroll false
```

The same sweep on the references, as a false-positive check: Linear 1 hit, Apple 1 hit (a blurred media card), Stripe 4 kinds (brand purple gradients, one `0x` label, one emoji, one blurred card). The rule "fix or justify each hit" came from that check.

## Quality gate

- Every number in the report was measured on the rendered page in this session (viewport stated).
- Every tell hit has a fix or a one-line justification; manual rows were checked on a screenshot.
- Zero console errors on load; every changed button tested by clicking.
- Contrast, targets and focus checked; automated checker output pasted if one ran.
- Web Vitals measured (field or lab, said which) or the item is marked `UNVERIFIED:` with the reason.

## Boundaries

- The sweep and checks are read-only; fixes go through `bequite-live-edit` or the feature's own task.
- Checker tools, MCP servers and component sources are candidates; never installed without the user's yes.
- Never report a page as accessible or fast from code reading alone.

## References (load on demand)

- `references/ai-tells.md`: the owner's tell list (web, slides, motion, copy, images), validated on three live sites.
- `references/tell-sweep.js`: the read-only browser script.
- `references/states-and-sourcing.md`: real states checklist, component sourcing order, per-feature checklist.
