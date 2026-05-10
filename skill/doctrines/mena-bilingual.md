---
name: mena-bilingual
version: 1.0.0
applies_to: [web-saas, frontend, mobile]
supersedes: null
maintainer: Ahmed Shawky (xpShawky)
ratification_date: 2026-05-10
license: MIT
introduced: v0.11.0
stacks_with: [default-web-saas, mena-pdpl, eu-gdpr]
---

# Doctrine: mena-bilingual v1.0.0

> The first-class Arabic + RTL layer for BeQuite-managed projects. Loaded by `.bequite/bequite.config.toml::doctrines = ["mena-bilingual"]`. Stacks cleanly with `default-web-saas` (UI rules), `mena-pdpl` (jurisdictional data protection — Egypt PDPL Law 151/2020, Saudi PDPL SDAIA, UAE Federal Decree-Law 45/2021 + DIFC + ADGM).
>
> **Why this Doctrine exists:** the AI vibe-coding tool space ships English-first and RTL-as-an-afterthought. MENA-region engineers building for MENA users get broken layouts, missing locale strings, and no Arabic-friendly typography out of the box. BeQuite's MENA bilingual module makes Arabic + RTL + Egyptian-dialect transcription **first-class** from day one.

## 1. Scope

Projects targeting MENA users (Egypt, Saudi Arabia, UAE, Jordan, Lebanon, Morocco, Kuwait, Bahrain, Qatar, Oman). Covers:

- **Locale: `ar-EG` default** (Egyptian Modern Standard + dialect transcription). Other locales: `ar-SA` (Saudi), `ar-AE` (UAE), `ar-MA` (Maghrebi), `ar-LB`/`ar-JO`/`ar-PS` (Levant). Each maps to specific font + dialect rules.
- **RTL layout** (`html[dir="rtl"]` + Tailwind/CSS logical properties).
- **Arabic-friendly typography** (Tajawal / Cairo / Readex Pro / Noto Sans Arabic as the canonical stack — none banned; recorded font choice per Doctrine `default-web-saas` Rule 2).
- **Bilingual UX** — every string in both `en-*` and `ar-*` (or whichever locale set the project declares). String-extraction discipline.
- **Egyptian-dialect transcription** — when scraping/researching MENA sources (Twitter/X, Telegram, Arabic news), preserve dialect markers; do not auto-normalize Egyptian dialect ("هتعمل ايه؟" → "ماذا ستفعل؟") unless the user explicitly requests Modern-Standard normalization.

**Does NOT cover:** Hebrew (RTL but different language family — separate doctrine if needed); Persian/Farsi (RTL, partial overlap with Arabic typography but different lexicon).

## 2. Rules

### Rule 1 — Locale-binding declared in project.yaml
**Kind:** `block`
**Statement:** `state/project.yaml::locales` MUST list the active locales explicitly (e.g. `["en-US", "ar-EG"]`). The CLI generates per-locale Playwright projects automatically.
**Check:** `bequite audit` parses project.yaml; flags missing or empty locales when `mena-bilingual` is loaded.
**Why:** locale-by-default is silently English; declared locales prevent regression.

### Rule 2 — `dir="rtl"` for ar-* locales
**Kind:** `block`
**Statement:** When the active locale is `ar-*`, the root HTML element MUST set `dir="rtl"`. The application MUST switch direction dynamically when locale changes (no full reload required).
**Check:** Playwright RTL walks at `?locale=ar-EG`; visual regression catches LTR-only assumptions.
**Why:** mirrored layout is the difference between an app that works and one that doesn't.

### Rule 3 — Logical properties only (no left/right)
**Kind:** `block`
**Statement:** CSS uses `margin-inline-start` / `padding-inline-end` / `border-inline-start` etc., NOT `margin-left` / `padding-right` / `border-left`. Tailwind classes use `ms-` / `me-` / `ps-` / `pe-` prefixes (Tailwind v3.3+ logical-properties classes), not `ml-` / `mr-` / `pl-` / `pr-`.
**Check:** `bequite audit` rule pack scans CSS + TSX/JSX for hardcoded directional properties; flags violations.
**Why:** logical properties auto-mirror under `[dir="rtl"]`; explicit left/right break.

### Rule 4 — Arabic-friendly font stack with recorded reason
**Kind:** `block`
**Statement:** `tokens.css` MUST declare an Arabic-friendly font stack under `[dir="rtl"]` override. Acceptable defaults: Tajawal (geometric, modern), Cairo (warm, body-friendly), Readex Pro (high x-height, dense interfaces), Noto Sans Arabic (broad subset coverage). The `--font-sans` override comment MUST explain *why this font fits this product* (Doctrine `default-web-saas` Rule 2).
**Check:** `bequite audit` greps `tokens.css` for `[dir="rtl"]` block + font-family declaration with adjacent comment.
**Why:** the system Arabic font on macOS / Windows / Linux looks dated; deliberate web-font choice is the differentiator.

### Rule 5 — Slightly larger body type + more leading for Arabic
**Kind:** `recommend`
**Statement:** Under `[dir="rtl"]`, body text size increases ~1pt (16px → 17px default) and `line-height` increases ~10% (1.6 → 1.7). Arabic glyphs are taller than Latin glyphs at the same nominal size; uniform sizing makes Arabic appear cramped.
**Check:** advisory; applied in default `tokens.css.tpl`.
**Why:** legibility, not arbitrary scale-bumping.

### Rule 6 — Bilingual string extraction with no inline translations
**Kind:** `block`
**Statement:** All user-facing strings MUST live in `apps/web/messages/<locale>.json` (or the i18n framework's equivalent). NO inline ternaries like `{locale === 'ar' ? 'مرحبا' : 'Hello'}` — these don't survive translator workflows.
**Check:** `bequite audit` greps source for `locale === 'ar'` / `locale === 'en'` ternaries on user-facing strings; flags violations.
**Why:** strings drift; centralized message catalogs are the only path to professional translation pipelines.

### Rule 7 — Egyptian dialect preserved by default (no auto-normalization)
**Kind:** `recommend`
**Statement:** When the Researcher persona scrapes MENA-locale sources (Twitter/X, Telegram, Arabic news), it MUST preserve Egyptian dialect (e.g., "هتعمل ايه؟" / "إزيك") in quotes + summaries. Auto-normalizing to Modern Standard Arabic is permitted ONLY when the user explicitly requests it (e.g., `bequite research <topic> --normalize-arabic`).
**Check:** advisory; documented in `skill/agents/research-analyst.md` extension.
**Why:** dialect carries cultural information; flattening it discards research signal.

### Rule 8 — RTL Playwright walks for every UI feature
**Kind:** `block`
**Statement:** When `mena-bilingual` is loaded alongside a frontend Doctrine, the Playwright config MUST add an `ar-EG` (or the project's primary Arabic locale) project per role. The walks at viewport 360 + 1440 MUST run for both LTR + RTL.
**Check:** `playwright.config.ts.tpl` reads `state/project.yaml::locales` and auto-generates projects.
**Why:** RTL bugs are silent in LTR-only test runs.

### Rule 9 — Mirrored icons + arrows
**Kind:** `recommend`
**Statement:** Directional UI cues (back arrow, forward arrow, chevron) MUST mirror under `[dir="rtl"]`. Standard pattern: `transform: scaleX(-1);` on the icon container under RTL, OR use icon-set variants where available (Lucide / Phosphor / Tabler all ship pre-mirrored variants for the most common ones).
**Check:** advisory; reviewed in design-audit.
**Why:** an arrow pointing right means "back" in RTL; "next" in LTR. Same pixels; opposite intent.

### Rule 10 — Number + date formatting per locale
**Kind:** `block`
**Statement:** Numbers, dates, currency MUST go through `Intl.NumberFormat` / `Intl.DateTimeFormat` with the active locale. Hardcoded `"$1,234.56"` or `"2026-05-10"` formats are forbidden in user-facing positions.
**Check:** `bequite audit` flags hardcoded `$|€|£|¥`-prefixed numbers in TSX/JSX.
**Why:** Egyptian Pound (EGP) formats differently than USD; Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩) vs Latin digits is a locale preference; Arabic dates use Hijri calendar in some contexts.

### Rule 11 — Skeptic kill-shot for MENA UX

When this Doctrine is loaded, the Skeptic at every UI phase boundary MUST ask:

> "What happens when an Arabic-speaking user on a phone (viewport 360, RTL, Tajawal font) navigates this flow end-to-end? What breaks first?"

The answer is recorded in `evidence/<phase>/skeptic-mena.md`.

## 3. Stack guidance

### i18n libraries

| Choice | When |
|---|---|
| **next-intl** | Next.js App Router (default for `default-web-saas`). |
| **i18next** + `react-i18next` | Framework-agnostic; mature; handles plural rules. |
| **lingui** | Compile-time messages; smallest runtime. |

### Arabic fonts (canonical stack)

| Font | Best for | Foundry | License |
|---|---|---|---|
| **Tajawal** | Modern, geometric, dense UI | Boutros / Mostafa El Abasiry | OFL |
| **Cairo** | Body text, warm | Mohamed Gaber | OFL |
| **Readex Pro** | Long-form reading, high x-height | Thomas Jockin / Yanek Iontef | OFL |
| **Noto Sans Arabic** | Broad subset coverage; fallback | Google | OFL |
| **IBM Plex Sans Arabic** | Tech-product feel | IBM | OFL |

All OFL-licensed = embeddable in commercial apps without per-seat fees.

### MENA-specific MCPs / data sources

- **Twitter/X MENA accounts** (configured per project; Researcher persona uses).
- **Telegram MENA channels** (config-listed; never auto-discovered for Article IV reasons).
- **Arab News / Asharq Al-Awsat / Al-Ahram English** for cross-checked news.
- **Local accelerators / VCs** (Flat6Labs, Wamda, MAGNiTT) for market signal.

## 4. Verification

`bequite verify` runs the following additional gates for projects loaded with this Doctrine:

1. **RTL Playwright walks** — admin + user at viewport 360 + 1440 + locale `ar-EG`.
2. **String-extraction audit** — flag inline ternaries on user-facing strings.
3. **Logical-property audit** — flag hardcoded `margin-left` / `padding-right` / etc.
4. **Number/date format audit** — flag hardcoded currency / date strings.
5. **Font-stack audit** — verify `[dir="rtl"]` block exists in `tokens.css`.
6. **Mirrored-icon spot check** (visual regression) — icons that should mirror, do.

## 5. Examples and references

- next-intl: https://next-intl-docs.vercel.app/
- i18next: https://www.i18next.com/
- lingui: https://lingui.dev/
- Tajawal: https://fonts.google.com/specimen/Tajawal
- Cairo: https://fonts.google.com/specimen/Cairo
- Readex Pro: https://fonts.google.com/specimen/Readex+Pro
- Logical Properties (MDN): https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values
- Tailwind logical properties: https://tailwindcss.com/docs/margin#logical-properties

## 6. Forking guidance

Common forks:

- **`mena-bilingual-saudi`** — Saudi-first variant; `ar-SA` default; SDAIA PDPL strict; Hijri calendar default for date formatting.
- **`mena-bilingual-uae`** — UAE-first; `ar-AE` default; DIFC DPL 5/2020 layered (financial-zone projects).
- **`mena-bilingual-mghreb`** — Maghreb (Morocco / Algeria / Tunisia); `ar-MA` default; Berber + French layered.

Pattern:
1. Copy this file to `.bequite/doctrines/<your-name>.md`.
2. Bump version to `0.1.0`.
3. Set `supersedes: mena-bilingual@1.0.0`.
4. Add `## Changes` section.
5. Load via `.bequite/bequite.config.toml::doctrines`.

## 7. Cross-references

- **`tokens.css.tpl`** at `skill/templates/tokens.css.tpl` — already ships `[dir="rtl"]` block since v0.6.1.
- **`research-analyst.md`** persona — bilingual research extension lands at v0.11.0+ refresh.
- **`mena-pdpl.md`** Doctrine — jurisdictional data protection; auto-stacks with this Doctrine for MENA-region projects.
- **`default-web-saas.md`** Doctrine — UI/UX rules; this Doctrine extends with locale-specific additions.
- **Playwright config template** at `skill/templates/playwright.config.ts.tpl` — auto-detects `ar-*` locales and adds RTL projects.

## 8. Changelog

```
1.0.0 — 2026-05-10 — Initial draft (BeQuite v0.11.0). 11 rules covering locale binding, dir="rtl", logical properties, Arabic font stack, body-type sizing, string extraction, dialect preservation, RTL Playwright walks, mirrored icons, number/date formatting, Skeptic kill-shot.
```
