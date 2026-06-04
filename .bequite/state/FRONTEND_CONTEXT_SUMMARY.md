# Frontend Context Summary

**The 1-screen design digest. Read this before every frontend task** (cheapest way to keep the design in context). It links to the full files; escalate to them only when this isn't enough. Keep it under one screen. See `docs/architecture/FRONTEND_CONTEXT_ENGINEERING.md`.

**Last updated:** `<ISO 8601 UTC | "not yet built">`

---

## Design DNA gist  (full: `.bequite/design/DESIGN_DNA.md`)

- **Product type:** `<...>`
- **Mood / adjectives:** `<...>`
- **Primary color / on-color:** `<...>` · **Background (tinted neutral):** `<...>`
- **Display font / Body font:** `<... / ...>` (reason recorded in tokens.css)
- **Spacing scale:** `4/8/12/16/24/32/48/64/96` · rhythm: tight within groups, 48–96 between sections
- **Radius scale:** `<...>` · **Motion:** exponential ease-out, no bounce, reduced-motion fallback
- **Accessibility target:** `<WCAG 2.2 AA | AAA for regulated>`
- **Top anti-patterns to avoid here:** `<e.g. purple gradient, nested cards, all-caps eyebrows, Inter-default>`

## Active frontend task

- **Task:** `<what's being built/edited right now>`
- **Operating mode / effort:** `<deep|fast|token-saver|delegate / low|medium|high|xhigh>`

## Pages / routes touched

- `<route — status: planned | building | continuity-passed | qa-passed>`

## Components touched

- `<Component — file — status>`

## Known design risks

- `<e.g. "section 4 card grid trending generic — watch on next pass">`

## Pending visual checks

- `<e.g. "tablet 768 not yet rendered", "dark mode contrast unverified">`

## Last visual QA result

- `<PASS | PARTIAL | FAIL | not yet run>` — `<date>` — see `.bequite/audits/VISUAL_QA_REPORT.md`

## Last Design Continuity result

- `<PASS | PARTIAL | FAIL | not yet run>` — `<date>` — see `.bequite/design/DESIGN_CONTINUITY_REPORT.md`

---

> Updated after every frontend step. If you can't state the font + primary color + spacing scale + product type from this file, re-read the full DNA before continuing. Never build a section from vague memory.
