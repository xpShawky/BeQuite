---
name: bequite-localization-rtl
description: Localization + RTL discipline — Arabic-first localization, RTL layout rules, i18n audit, string extraction, translation memory, number/date/currency formatting, MENA UX tone, font readability, icon mirroring. Auto-attaches on Arabic / MENA / Egypt / RTL / bilingual signals in any workflow (course, feature, presentation, reference, live-edit).
---

# bequite-localization-rtl — Arabic / MENA / RTL discipline

## Purpose

Make any BeQuite output genuinely usable in Arabic/MENA contexts — not literal translation pasted into an LTR layout. Skill-first by design: there is **no `/bq-localize` command** (optional proposal only, see `docs/specs/LOCALIZATION_RTL.md`); this skill auto-attaches via the Skill Router.

## When this skill activates

Signals (any workflow): Arabic · MENA · Egypt/Gulf/Saudi/UAE market · RTL · bilingual Arabic/English · "Arabic course / app / presentation / website" · `mena-bilingual` doctrine in DECISIONS.md.

## When NOT to use

Pure-LTR projects with no MENA/Arabic requirement; generic i18n for non-RTL languages (basic i18n hygiene lives in frontend skills).

## Language discipline

1. **Tone localization over literal translation** — Arabic UX copy follows local register (formal MSA vs Egyptian/Gulf colloquial — ask which); never machine-literal phrasing.
2. **Mixed Arabic/English rules** — technical terms either consistently transliterated or consistently English; bidi isolation for inline Latin (`dir`/`bdi`), no broken bracket/punctuation mirroring.
3. **Numbers** — decide once per project: Arabic-Indic (٠١٢٣) vs Western (0123) digits; record in PROJECT_DNA/DESIGN_DNA. Dates: Gregorian vs Hijri awareness. Currency: EGP/SAR/AED placement conventions.

## RTL engineering discipline

1. **Layout:** logical CSS properties (`margin-inline-start`, not `margin-left`); `dir="rtl"` at the root; test both directions when bilingual.
2. **Icon mirroring:** mirror directional icons (arrows, back, progress); **never** mirror logos, media controls, clocks, or checkmarks.
3. **Width expansion:** Arabic labels run +20–40% wider — buttons/navs sized for it; no truncation-by-default.
4. **Typography:** Arabic body fonts chosen for readability (never Latin-display-only stacks); line-height ≥1.6 for Arabic body; font pairing recorded in DESIGN_DNA.
5. **i18n audit:** hardcoded strings extracted; translation memory table maintained where a translation workflow exists; pluralization uses CLDR Arabic rules (6 plural forms).

## Memory rules

Write localization decisions into the active workflow's artifacts: DESIGN_DNA gains an RTL/Arabic section; courses gain language plans (COURSE_BRIEF/RECORDING_PLAN); presentations gain RTL slide rules. No dedicated memory dir.

## Quality gate

Before claiming Arabic/RTL work complete: root `dir` correct · no mirrored logo/media icons · no truncated Arabic labels · digits/dates decision recorded · body font readability verified (visual check when browser tooling available) · bidi text renders correctly with inline Latin. Findings carry file:line evidence per anti-hallucination rules.
