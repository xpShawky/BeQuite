# Section Map

Maps visible frontend sections to source files. Built by `/bq-live-edit` on first run; refreshed when sections change.

**Project:** <name>
**Frontend stack:** <e.g. Next.js 15 App Router + Tailwind v4>
**Dev URL:** <e.g. http://localhost:3000>
**Last refresh:** <ISO 8601 UTC | "not yet built">

---

## How to use this file

When `/bq-live-edit` runs, it reads this map to identify which source files to edit for a given section.

If the map is empty, the command will build it by walking the source tree.

If a section is missing, the command will add it on the fly.

---

## Sections (one entry per visible UI section)

<!--
  Template per section:

  ### <Section Name>
  - **Source:** <path/to/file.tsx>
  - **Visual description:** <1-2 sentences>
  - **Key classes / tokens:** <list>
  - **Text content:** <current copy>
  - **Responsive concerns:** <e.g. stacks below 768px>
  - **Editable fields:** <e.g. headline, subhead, CTAs>
  - **Known problems:** <e.g. overflow at 360px>
-->

## Page: /

(no sections mapped yet — run `/bq-live-edit` to build)

---

## Page: /dashboard

(no sections mapped yet — run `/bq-live-edit` to build)

---

## Notes

- This file is auto-managed by `/bq-live-edit`
- Manual edits are fine but may be overwritten on next refresh
- Keep section names stable across edits (they're the lookup key)
