# Section Map

Maps every visible frontend section to its source file **and its acceptance criteria**. The contract between the rendered UI and the code. Built by `/bq-live-edit` / the section-by-section loop; read before building or editing any section. Owner skills: `bequite-frontend-design-system` (loop) + `bequite-live-edit` (mapping).

**Project:** `<name>`
**Frontend stack:** `<e.g. Next.js 15 App Router + Tailwind v4>`
**Dev URL:** `<e.g. http://localhost:3000>`
**Design DNA:** `.bequite/design/DESIGN_DNA.md` (every section must match it)
**Last refresh:** `<ISO 8601 UTC | "not yet built">`

---

## How to use this file

- Before building/editing a section, read its entry here + the Design DNA.
- Each section carries **acceptance criteria** — that's what the Design Continuity Gate checks the built section against.
- If a section is missing, add it before editing. If structure changes, update the entry after.
- Keep section names stable (they're the lookup key for `/bq-live-edit`).

---

## Section entry template (richer — alpha.17)

```markdown
### <Section Name>
- **Route:** </path>
- **Purpose:** <what this section is for, in one line>
- **Source file:** <path/to/file.tsx>
- **Component:** <exported component name>
- **Visual role:** <hero | primary content | supporting | social proof | conversion | navigation | footer | utility>
- **Content rules:** <copy tone, what must/mustn't appear, no Lorem ipsum, real data>
- **Layout constraints:** <grid/flex, max-width, density, alignment, token usage>
- **Responsive behavior:** <how it reflows at 360 / 768 / 1440>
- **Known risks:** <e.g. "long titles overflow at 360px", "tends toward generic card grid">
- **Acceptance criteria:** <specific, testable — matches DNA §; no all-caps misuse; contrast ≥4.5:1; real states; passes continuity gate>
```

---

## Page: /

(no sections mapped yet — run `/bq-live-edit` or the section-by-section loop to build)

> Example of a filled entry: see `.claude/skills/bequite-frontend-design-system/examples/section-map-example.md`.

---

## Page: /dashboard

(no sections mapped yet)

---

## Notes

- Auto-managed by `/bq-live-edit` and the master skill's section loop.
- Acceptance criteria here are the per-section bar the Design Continuity Gate enforces — keep them concrete.
- Manual edits are fine but may be refreshed on the next mapping pass.
