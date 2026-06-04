# Design Continuity Report

Written by the Design Continuity Gate (owner skill: `bequite-frontend-design-system`). One block **per page/route**. Compares every section against the Design DNA and against the strongest section on the page. See `docs/architecture/DESIGN_CONTINUITY_GATE.md`.

**Project:** `<name>`
**Generated:** `<ISO 8601 UTC | "template — not yet run">`
**DNA version:** `<DESIGN_DNA.md last-updated>`
**Effort level:** `<low | medium | high | xhigh/Ultracode>`
**Overall status:** `<PASS | PARTIAL | FAIL | template>`

---

## How to use this file

- The gate writes one `### Route:` block per page. Re-run regenerates the block for that route.
- A route is **PASS** only when every section is consistent with the DNA and no BLOCKER/HIGH issue remains.
- This report is required (alongside `VISUAL_QA_REPORT.md`) before any UI is claimed complete by `/bq-auto`, `/bq-feature`, or `/bq-verify`.

---

## Template (copy per route)

```markdown
### Route: /<path>

**Sections inspected:** <hero, features, pricing, testimonials, FAQ, footer — list ALL, not a sample>
**Design DNA summary:** <one line: product type · mood · primary color · display/body font · spacing rhythm>
**Components inspected:** <nav, cards, forms, buttons, modals, tables, empty/loading/error states>
**Responsive checked:** <360 / 768 / 1440 + named breakpoints>

#### Issues found

| # | Section / component | Issue (drift tell) | Severity | Fix applied | Verification method |
|---|---|---|---|---|---|
| 1 | Pricing cards | gray-on-color title fails 4.5:1 | HIGH | switched to on-surface token | axe-core + manual grayscale |
| 2 | "How it works" | all-caps eyebrow + 0.2em tracking (off-DNA) | MEDIUM | removed eyebrow; sentence-case h2 | visual diff at 1440 |
| 3 | Section 4 vs hero | generic icon-heading-text card grid; quality cliff | HIGH | re-laid out with varied rhythm per DNA §8 | screenshot compare |

#### Quality-cliff check (the core test)

- **Strongest section:** <e.g. hero>
- **Weakest section:** <e.g. section 4 "integrations">
- **Gap closed?** <yes — section 4 pulled up to hero bar | no — remaining gap described>

#### Screenshots (if browser automation available)

- <.bequite/uiux/screenshots/continuity-<route>-<section>-<ts>.png ...>

#### Remaining risks

- <e.g. "tablet 768 not visually verified — Playwright unavailable; documented manual steps">

**Route status:** <PASS | PARTIAL | FAIL>
```

---

## Routes

(no routes inspected yet — populated when the Design Continuity Gate runs against a real frontend)

---

## Roll-up

| Route | Sections | BLOCKER | HIGH | MEDIUM | LOW | Status |
|---|---|---|---|---|---|---|
| (none yet) | | | | | | |

**Final status:** `template — not yet run`
