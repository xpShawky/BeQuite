# Localization / RTL — skill-first (alpha.22)

**Shape ruling:** `bequite-localization-rtl` ships as an **auto-attached skill**; `/bq-localize` is an **optional command proposal only** (not built — it would duplicate the skill's auto-attach behavior ~70% of the time; promote it only if real usage shows users invoking localization as a standalone workflow).

## Auto-attach signals (Skill Router)

Arabic · MENA · Egypt/Gulf market · RTL · bilingual Arabic/English · "translate the app/site/course" · Arabic course/presentation/website requests. Attaches alongside whatever command is running (course, feature, presentation, reference, uiux-variants, live-edit).

## Skill scope

- **Language:** Arabic-first; mixed Arabic/English content rules; tone localization (not literal translation); MENA cultural context
- **i18n engineering:** i18n audit · string extraction · translation memory · number/date/currency formatting (Hijri/Gregorian awareness, Arabic-Indic digits decision) · pluralization rules
- **RTL UI:** layout direction (logical CSS properties) · icon mirroring rules (mirror directional, never mirror logos/media controls) · button/label width expansion (+20–40%) · font readability (Arabic needs larger x-height equivalents; never display-only Latin fonts for Arabic body) · bidi text handling
- **Doctrine link:** `mena-bilingual` doctrine activates this skill by default

## Memory

Writes localization decisions into the active workflow's artifacts (DESIGN_DNA gains an RTL section; course files gain language plans). No dedicated memory dir until `/bq-localize` exists.
