# Visual QA Report — worked example: ClinicFlow

> Purpose: a realistic, partial-pass Visual QA artifact that shows the Design Continuity Gate catching middle-section drift on the ClinicFlow marketing landing page. Companion to `../SKILL.md` (the loop + gate), `./design-dna-example.md` (the locked DNA this is checked against), and `./section-checklist-example.md` (the per-section checklist this fills).

---

## Run header

| Field | Value |
|---|---|
| Product | ClinicFlow — clinic booking platform |
| Surface under test | Marketing landing page (public) |
| Route | `/` |
| Design DNA | `.bequite/uiux/DESIGN_DNA.md` v1 (calm clinical teal, OKLCH, humanist display + clean body, NO purple/pink gradients) |
| Doctrine | `default-web-saas` |
| Contrast target | AA (marketing surface) — body 4.5:1, large text 3:1, UI/focus 3:1 |
| Tier used | **Tier 3 — project Playwright** (already in repo `package.json`; no install) |
| Viewports | 360 (mobile), 768 (tablet), 1440 (desktop) |
| Tooling | Playwright screenshots + `@axe-core/playwright` (project dep) for contrast/role checks |
| Date | 2026-06-03 |
| Run ID | `vqa-2026-06-03-1` |

Tier selection note: Tier 1 (read-only static review) and Tier 2 (single screenshot) were skipped because Playwright is already a project dependency. No new dependency installed (tool-neutral; see CLAUDE.md rule 12).

---

## Per-route checklist — `/` (marketing)

Checked section-by-section against the locked Design DNA. Drift is scored relative to the **hero** as the identity anchor — the question at every row is "does this still look like the same product as the hero?"

| # | Section | Identity | Contrast (AA) | Type rules | Spacing 4/8 | Touch ≥24px | Motion / reduced-motion | Mobile 360 | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Hero | PASS | PASS (teal-on-cream 7.2:1) | PASS (display 1.15 lh, body 16px) | PASS | PASS (CTA 48px) | PASS (fade/translate 220ms, reduced-motion honored) | PASS | **PASS** |
| 2 | Logo strip | PASS | PASS | PASS | PASS | n/a | PASS | PASS | PASS |
| 3 | **Features** | **FLAG** | PASS | PASS | WARN (24/32 mix) | PASS | PASS | PASS | **FAIL** |
| 4 | **How it works** | **FLAG** | PASS | **FAIL** (eyebrow tracking) | PASS | PASS | PASS | PASS | **FAIL** |
| 5 | **Testimonials** | PASS | **FAIL** (gray-on-teal 3.1:1) | PASS | PASS | PASS | PASS | PASS | **FAIL** |
| 6 | **Pricing** | PASS | PASS | PASS | PASS | PASS | PASS | **FAIL** (overflow @360) | **FAIL** |
| 7 | FAQ | PASS | PASS | PASS | PASS | PASS (accordion 48px) | PASS | PASS | PASS |
| 8 | Footer | PASS | PASS | PASS | PASS | PASS | n/a | PASS | PASS |

### Route verdict: **PARTIAL** — 4 of 8 sections fail. Hero is clean; the middle of the page drifts. This is exactly the hero-to-middle quality cliff the gate exists to catch.

---

## Failures table

| ID | Section | Severity | Drift type | Evidence | Action |
|---|---|---|---|---|---|
| F1 | Features (#3) | **High** | Quality cliff / generic-card slop — three identical icon-over-title-over-paragraph cards, same outline icon weight, same gray body, zero hierarchy between them. Reads as a stock template, not the same product as the hero. | `screens/01-features-1440.png`, `screens/01-features-360.png` | Differentiate the three cards: vary card emphasis (one primary-tinted), replace identical generic icons with distinct duotone teal glyphs tied to each feature, add a short outcome line per card. Re-anchor to hero's calm/efficient tone. |
| F2 | How it works (#4) | **Medium** | Off-DNA typography — numbered eyebrow set in ALL-CAPS at `letter-spacing: 0.18em`. DNA caps rule is ≤4-word labels at **0.05–0.12em**; 0.18em is wide-tracking AI-slop and the label is a sentence fragment, not a short label. | `screens/02-howitworks-1440.png` | Reduce tracking to 0.08em, keep caps only on the 2-word step label ("STEP 01"), move the descriptive sentence to sentence-case body below. |
| F3 | Testimonials (#5) | **High (blocker)** | Contrast fail — gray quote text (`oklch(0.62 0 0)`) on the teal testimonial card (`oklch(0.55 0.09 195)`) measures **3.1:1**. Below AA body floor 4.5:1. axe-core flagged `color-contrast`. | `screens/03-testimonial-1440.png`, axe node `.testimonial-card blockquote` | Use cream/near-white text (`oklch(0.97 0.01 195)`) on the teal card → ~6.8:1. Reserve teal-on-cream for text on light surfaces only. |
| F4 | Pricing (#6) | **High** | Mobile overflow @360 — the 3-column price grid does not collapse; the third card and the "per month" suffix clip the viewport, triggering horizontal scroll. | `screens/04-pricing-360.png` (note the right-edge clip + scrollbar) | Stack price cards to 1 column below 640px; verify "per month" / currency does not wrap or clip. Re-test at 360 and 768. |
| F5 | Features (#3) | **Low** | Spacing scale mix — card gap 24px but section padding 32px on one axis and 28px on the other (28 is off the 4/8 scale). | `screens/01-features-1440.png` | Normalize to the 4/8 scale: section padding 32px both axes, card gap 24px. |

Severity legend: **Blocker** = ships broken (accessibility/legal or visible breakage) · **High** = strong identity/UX damage · **Medium** = noticeable off-DNA · **Low** = polish.

---

## Screenshots

```
.bequite/uiux/screenshots/vqa-2026-06-03-1/
  screens/
    00-hero-1440.png            PASS — identity anchor
    01-features-1440.png        FAIL — F1 generic 3-card grid, F5 spacing
    01-features-360.png         FAIL — F1 visible at mobile too
    02-howitworks-1440.png      FAIL — F2 0.18em all-caps eyebrow
    03-testimonial-1440.png     FAIL — F3 gray-on-teal 3.1:1
    04-pricing-360.png          FAIL — F4 horizontal overflow
    05-faq-1440.png             PASS
    06-footer-1440.png          PASS
  axe/
    home-axe.json               1 serious: color-contrast (F3)
```

---

## Honest note

This run did NOT verify the staff dashboard (`/dashboard/*`) — it is auth-gated and the test session had no seeded staff credentials. Dashboard AAA contrast on critical actions (the DNA's lean-AAA target for the internal surface) is therefore **unverified**, not passed. The hero passing does not make the page pass; four middle sections fail and F3 is an accessibility blocker. Two failures (F1 identity drift, F2 tracking) are subjective-leaning but both map to specific DNA rules, so they are recorded as fails, not opinions. No fixes were applied during this run — this report is the diagnosis only.

---

## Follow-up re-run (after fixes)

Fixes F1–F5 applied via `/bq-live-edit` section passes, then re-tested with the same Playwright tier and viewports.

| Field | Value |
|---|---|
| Run ID | `vqa-2026-06-03-2` |
| Changes | F1 card differentiation + duotone glyphs · F2 tracking 0.18em→0.08em, caps on 2-word label only · F3 quote text → cream (6.8:1) · F4 pricing stacks @<640px · F5 padding normalized to 4/8 |

### Re-run checklist — `/`

| # | Section | Identity | Contrast | Type | Spacing | Touch | Motion | Mobile 360 | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Hero | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 2 | Logo strip | PASS | PASS | PASS | PASS | n/a | PASS | PASS | PASS |
| 3 | Features | **PASS** | PASS | PASS | **PASS** | PASS | PASS | PASS | **PASS** |
| 4 | How it works | **PASS** | PASS | **PASS** | PASS | PASS | PASS | PASS | **PASS** |
| 5 | Testimonials | PASS | **PASS** (cream-on-teal 6.8:1) | PASS | PASS | PASS | PASS | PASS | **PASS** |
| 6 | Pricing | PASS | PASS | PASS | PASS | PASS | PASS | **PASS** (1-col @360) | **PASS** |
| 7 | FAQ | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 8 | Footer | PASS | PASS | PASS | PASS | PASS | n/a | PASS | PASS |

axe-core: 0 violations. Visual diff vs `00-hero-1440.png` confirms the middle sections now hold the hero's calm/efficient identity.

### Re-run route verdict: `/` → **PASS** (8/8 sections; AA met on the marketing surface)

Still outstanding (carried to next run): staff dashboard `/dashboard/*` AAA verification — unverified, not blocked, pending seeded credentials.
