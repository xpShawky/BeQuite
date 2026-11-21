---
name: bequite-localization-rtl
description: Use whenever output is in Arabic or for an Arabic-speaking or MENA audience - a page, an app, a deck, a post, a course, an email - or is bilingual Arabic and English, or mentions Egypt, the Gulf or RTL. Gets direction, mixed-script text, digits, dates, currency, plurals and the Arabic register right, and checks them in a real browser rather than by reading the code.
last_verified: 2026-11-21
sources:
  - https://www.w3.org/International/questions/qa-html-dir
  - https://www.w3.org/International/articles/inline-bidi-markup/
  - https://www.unicode.org/reports/tr9/
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values
  - https://www.unicode.org/cldr/charts/latest/supplemental/language_plural_rules.html
---

# bequite-localization-rtl

Arabic done properly is not translated English in a mirrored box. The right register, direction set in markup, mixed text isolated, numbers chosen on purpose, all looked at in a browser.

## When to use

- Any workflow (feature, live-edit, presentation, content, course) with Arabic, MENA, Egypt, Gulf, RTL or bilingual signals. Skill-first: there is no separate command.

Not for: projects with no Arabic or RTL requirement.

## Procedure

1. **Decide once, record in `DESIGN_DNA.md` (or `PROJECT_DNA.md`):**
   - register: Egyptian colloquial, Gulf, or Modern Standard Arabic. For anything a person reads as content, take it from the reference voice (the human-taste skill and writing DNA), never a default;
   - digits: Arabic-Indic (٠١٢٣) or Latin (0123), pinned in code with the locale extension (`ar-EG-u-nu-latn` or `ar-EG-u-nu-arab`), because defaults differ by locale (measured below);
   - calendar (Gregorian, or Hijri where it matters), currency code and symbol placement, and how technical terms appear (always English, or always transliterated; not mixed).
2. **Direction in markup, not CSS:** `<html dir="rtl" lang="ar">` (or `lang="ar-EG"`). `lang` alone does not set direction. Change direction below the root only where a block really changes (an English code sample, a quote).
3. **Isolate mixed text:** wrap each Latin phrase inside Arabic (and the reverse) in an element with `dir`; text of unknown direction (user names, inserted data) in `<bdi>` or `dir="auto"`; user input fields `dir="auto"` (and `dirname` if the server needs to know). Where markup is impossible (`<title>`, attributes), use RLI/LRI/FSI ... PDI (U+2067 / U+2066 / U+2068 ... U+2069). The cases that break without isolation: a phrase that starts with a number, ends in punctuation, or is followed by a number.
4. **Layout with logical CSS:** `margin-inline-start`, `padding-inline`, `inset-inline`, `text-align: start` (widely available since January 2020). No `left`/`right` for things that should follow direction. A `dir` on a table reverses its column order.
5. **Mirror what points, not what is:** mirror back and forward arrows, progress and sliders, list indents; do not mirror logos, media play controls, clocks, checkmarks, or images of real objects.
6. **Plurals and formatting through the platform:** `Intl.PluralRules` / ICU MessageFormat with all six Arabic categories (zero, one, two, few, many, other); `Intl.NumberFormat` and `Intl.DateTimeFormat` with the pinned locale. Never concatenate number + noun.
7. **Type:** an Arabic face chosen for reading (body) and one for display, each with its source; generous line height (start near 1.6 for body and adjust by eye); measure label widths in the browser instead of assuming a percentage.
8. **Check in a real browser** at desktop and phone width: screenshot the page in `ar` and, if bilingual, `en`; look for reversed punctuation, numbers jumping sides, truncated labels, mirrored logos. Record the screenshots in `evidence.md`.

## Worked example (measured, Node v24.12.0, 2026-11-21)

```
ar-EG            EGP 1234.5 -> ‏١٬٢٣٤٫٥٠ ج.م.‏    date 2026-11-21 -> ٢١ نوفمبر ٢٠٢٦
ar-EG-u-nu-latn  EGP 1234.5 -> ‏1,234.50 ج.م.‏    date -> 21 نوفمبر 2026
ar-AE            EGP 1234.5 -> ‏1,234.50 ج.م.‏    (Latin digits by default)
PluralRules('ar-EG'): 3 -> few, 11 -> many, 100 -> other   (CLDR: few = n%100 3..10, many = 11..99)
```

Lesson: `ar-EG` and `ar-AE` default to different digit systems in the same runtime, so a bilingual Egyptian site that wants Latin digits must say `-u-nu-latn` explicitly, and a price string must never be built by hand.

## Quality gate

- Root `dir` and `lang` set; no base direction set in CSS.
- Mixed-script strings isolated; a screenshot shows numbers and punctuation in the right place.
- Digits, calendar, currency and register decisions recorded.
- No mirrored logo or media control; no truncated Arabic label at phone width.
- Plurals cover all six categories.

## Boundaries

No machine-literal translation for anything a person reads: Arabic copy follows a studied reference voice. Findings carry `file:line` or a screenshot (anti-hallucination rule).
