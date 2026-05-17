---
name: bequite-live-edit
description: Lightweight live-edit procedures for a running frontend. Detects framework + dev server, maps visible sections to source files, applies targeted code edits, verifies via build + (optional) browser screenshots. No heavy Studio. Browser automation only when already available. Invoked by /bq-live-edit and /bq-auto live-edit.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash
---

# bequite-live-edit — agent-assisted section edits

## Purpose

Encode the discipline for **lightweight, agent-assisted frontend edits** that respect:
- Section-first mapping (don't edit blind)
- Smallest-possible-change discipline
- Existing design system preservation
- Optional (not required) browser automation
- Verifiable rollback for every edit

Activated by `/bq-live-edit` and `/bq-auto live-edit`.

---

## When to use this skill

- Targeted edits to a running frontend
- Section-by-section visual fixes
- Iterating on a chosen UI direction (after `/bq-uiux-variants`)
- Quick text / spacing / color changes
- Improving empty / loading / error states

## When NOT to use this skill

- Generating new UI directions (use `bequite-ux-ui-designer` via `/bq-uiux-variants`)
- New components or pages (use `bequite-frontend-quality` via `/bq-feature`)
- Backend / API edits (use `bequite-backend-architect`)
- No-frontend projects (skill stays dormant)

---

## Required inputs

The skill expects:
- A frontend project (Next.js / Nuxt / SvelteKit / Vite + React / plain HTML / etc.)
- A way to run the dev server (`npm run dev` or equivalent)
- Optional: browser automation already installed or available via MCP

Without those, the skill cannot operate. Exit cleanly.

---

## 1. Frontend stack detection

Read these files in order to detect the stack:

| Signal | File / clue |
|---|---|
| Next.js | `package.json` has `"next": "..."` + `app/` or `pages/` |
| Nuxt | `nuxt.config.{js,ts}` + `pages/` |
| SvelteKit | `svelte.config.js` + `src/routes/` |
| Vite + React | `vite.config.{js,ts}` + `src/main.tsx` + `react` in deps |
| Vite + Vue | Same but with `vue` |
| Astro | `astro.config.{js,mjs}` + `src/pages/` |
| Plain HTML | `index.html` at root, no framework deps |
| Other | Read README + package.json scripts |

Record the detected stack in SECTION_MAP.md header.

---

## 2. Dev server detection

Look for the dev script:

```json
"scripts": {
  "dev": "next dev",          // Next.js
  "dev": "vite",              // Vite
  "dev": "astro dev",         // Astro
  "dev": "nuxt dev",          // Nuxt
  "dev": "vite dev",          // SvelteKit
  "start": "live-server",     // plain HTML (sometimes)
}
```

Default URL is usually `http://localhost:3000` (Next.js, Nuxt) or `5173` (Vite, SvelteKit) or `4321` (Astro).

**Don't start the dev server unilaterally.** Ask:
> "Is the dev server already running? URL? If not, want the command to start it?"

---

## 3. Browser inspection strategy

Inspection has three tiers — use the highest tier available without installing anything:

### Tier 1: Playwright MCP (preferred when available)

If Playwright MCP is loaded in the agent host (`mcp__playwright__*` tools available), use it:
- `page.goto(url)`
- `page.screenshot({ path: "..." })`
- `page.locator(selector).boundingBox()`
- DOM inspection

### Tier 2: Playwright already installed in the project

If the project has `@playwright/test` in `devDependencies`, drive it via a script:
```ts
// scripts/inspect.ts
import { chromium } from "playwright";
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("http://localhost:3000");
await page.screenshot({ path: ".bequite/uiux/screenshots/before-...png" });
await browser.close();
```

### Tier 3: Code inspection only

If neither is available:
- Read source files (Read tool)
- Grep for the section name
- Ask the user for a manual screenshot if visual context matters
- Document the manual verification steps

**Never auto-install Playwright.** If the task genuinely needs it and the project doesn't have it, surface as a recommendation with a decision section.

---

## 4. Section mapping strategy

The SECTION_MAP.md is the contract between visible UI and source files.

### When to build / refresh

- First `/bq-live-edit` run in a project → build from scratch
- After major refactor or new feature → user can run `/bq-live-edit "refresh section map"`
- If a section is missing from the map → add it on the fly during the edit

### How to build

1. Walk `components/`, `app/`, `pages/`, `src/routes/` (per stack)
2. Identify exported components with visible names (Hero, NavBar, PricingCards, etc.)
3. For each, record:
   - Source path
   - Visual description (1-2 sentences)
   - Key classes / token usage
   - Text content (current)
   - Responsive concerns
   - Editable fields
   - Known problems
4. (Optional) Take section-level screenshots if Playwright is available

### Heuristics for identifying sections

- Component names ending in `Section`, `Panel`, `Block`, `Card`, `Hero`, `Nav`, `Footer`, `Sidebar`, `Form`, `List`
- Top-level children of `page.tsx` / `page.vue` / `+page.svelte`
- Components with `id="..."` attributes (anchor targets)
- Components imported by route files

---

## 5. Source-file mapping for an edit

User's request → SECTION_MAP entry → source file(s).

### Match strategies

1. **Exact name match:** "pricing cards" → `PricingCards` in map
2. **Synonym match:** "the price box" → `PricingCards` (the map records visual descriptions)
3. **Page-based:** "the header on /dashboard" → look up `/dashboard` page + find NavBar / Header component
4. **Visual description:** "the big banner at the top" → match to Hero

If multiple matches → ask **one** disambiguation question.

If no matches → walk source, propose 2-3 candidates, ask user to confirm.

---

## 6. Edit strategy

### The smallest-change rule

For each edit type, prefer the most localized change:

| Edit type | Preferred change locus |
|---|---|
| Text | Component file's JSX/template OR content file |
| Spacing | Component's className / style OR tokens.css if global |
| Font size | tokens.css if changing scale; component file if one-off |
| Color | tokens.css if changing system; component file if one-off |
| Layout (flex/grid) | Component file |
| Motion | Component file or motion config |
| Image | `public/` or asset import path |
| Responsive | Component file (Tailwind breakpoints or CSS media queries) |
| Accessibility | Component file (ARIA, focus styles) |

### What NOT to edit

- Don't rewrite the whole page when the user asked about one section
- Don't change the design system tokens for a one-off issue (unless the issue is systemic)
- Don't add a new library to support a small edit
- Don't refactor neighboring code (out of scope for the request)

---

## 7. Responsive check

If the edit touches layout / spacing / sizing:

- Test at 360px (mobile baseline — iPhone SE)
- Test at 768px (tablet)
- Test at 1440px (desktop standard)

Via browser automation if available; via responsive class inspection if not.

Common pitfalls:
- Text overflowing cards
- Buttons < 44px touch target
- Horizontal scroll on body
- Hidden text (contrast or overflow)

---

## 8. Screenshot strategy (if browser automation available)

- Before screenshot → `.bequite/uiux/screenshots/before-<ts>-<section>.png`
- After screenshot → `.bequite/uiux/screenshots/after-<ts>-<section>.png`
- Mobile screenshot for responsive changes
- Annotate the diff in LIVE_EDIT_LOG (which area changed)

If automation is NOT available:
- Skip screenshots; note in LIVE_EDIT_LOG "manual verification recommended"
- Optionally ask the user to take a screenshot for the record

---

## 9. Test strategy

- Run `npm run build` (or equivalent) — catches typeerrors + bad imports
- Run frontend tests if any exist (vitest, jest, etc.)
- (Optional) Run lint
- (Optional) Run axe-core if installed

If any test fails after the edit → roll back, log the failure, ask user.

---

## 10. Failure handling

| Failure | Recovery |
|---|---|
| No frontend in project | Exit; suggest `/bq-feature` or `/bq-fix` |
| Dev server won't start | Pause; ask for correct command + env |
| Section ambiguous | One question; then proceed |
| Section not findable | Walk source; propose 2-3 candidates; ask |
| Build red after edit | `git stash` to roll back; re-attempt with smaller scope |
| Visual regression | Roll back; ask user to confirm intent |
| Test red after edit | `git stash`; re-attempt; if persists, pause |
| Playwright not available + task needs visual confirmation | Document manual verification steps; ask user for screenshot |
| Multiple files match the section | Edit the most-specific; log decision |

---

## 11. Rollback strategy

Every edit must be reversible:

- Git working-tree edits → `git checkout -- <file>` or `git stash`
- Token changes → record original value in LIVE_EDIT_LOG.md before editing
- Component rewrites → preserve original in `<Component>.tsx.before-<timestamp>` if non-trivial (rare; live edits are small)

If user says "undo last live edit":
- Read LIVE_EDIT_LOG.md
- Restore from the "Before" snippet using Edit tool
- Append a new entry "Reverted: <original ts>"

---

## 12. Common mistakes to avoid

- **Editing without a section map** ("I'll just open files") → wrong-file edits
- **Rewriting whole page for one-section ask**
- **Auto-installing Playwright** to take screenshots for a 2-line CSS change
- **Adding new design library** mid-edit (this is a feature, not a live edit)
- **Skipping the LIVE_EDIT_LOG entry** ("it's small") — every edit logged
- **Changing tokens.css** without recording in DECISIONS.md
- **Starting the dev server** without user consent
- **Claiming "looks great"** without verification (banned weasel)
- **Not testing on mobile** when the edit touched layout

---

## 13. Tool neutrality (global rule)

⚠ **Every tool named in this skill (Playwright, Chromatic, Percy, Storybook, Tailwind, axe-core, etc.) is an EXAMPLE, not a default.**

The three-tier browser inspection strategy explicitly **avoids** installing tools. Tier 3 (code inspection) is fine and works without any browser automation.

If the task truly requires a tool not present:
- Write a decision section (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan)
- Surface to user; let them decide whether to add it
- Don't auto-install

The 10 decision questions still apply:
1. Project type? 2. Actual problem? 3. Scale? 4. Constraints? 5. Existing stack? 6. UX needed? 7. Failure risks? 8. Proven tools? 9. Overkill? 10. Best output / least complexity?

See `.bequite/principles/TOOL_NEUTRALITY.md`.

---

## 14. What this skill does NOT do

- Build a heavy Studio
- Drag-and-drop WYSIWYG editing
- Auto-install browser tooling
- Replace the designer (this executes design intent, doesn't invent it)
- Operate without a frontend
- Edit blindly without section mapping

---

## Quality gate (alpha.15)

Before claiming this skill's work complete:

- [ ] Artifacts produced match the skill's expected outputs
- [ ] All discipline rules in this skill were respected
- [ ] No banned weasel words in any completion claim
- [ ] Any tool / library added has a decision section per `.bequite/principles/TOOL_NEUTRALITY.md`
- [ ] Acceptance criteria for the invoking command's task are met
- [ ] `.bequite/state/MISTAKE_MEMORY.md` updated when a project-specific lesson surfaced
- [ ] `.bequite/logs/AGENT_LOG.md` entry appended

If any item fails, do not claim done — report PARTIAL with the specific gap.
