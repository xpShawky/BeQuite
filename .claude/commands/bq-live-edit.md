---
description: Lightweight section-by-section frontend live edit. Maps visible sections to source files (SECTION_MAP.md), applies targeted code edits, verifies via build + screenshots (if browser automation available). Not a heavy Studio. Browser automation used only if frontend exists and tool is already available.
---

# /bq-live-edit — agent-assisted live edits

## Purpose

Modify a frontend section through prompts while the site is running. The agent maps visible sections to source files, applies the smallest possible edit, re-runs / refreshes, verifies the section visually if possible, and logs the change.

**Lightweight.** No heavy Studio. No separate app. No Figma clone. Slash command + skill.

Full strategy: `docs/architecture/LIVE_EDIT_STRATEGY.md`.

## When to use it

- Targeted edits (text, spacing, font size, color, layout, motion)
- Visual fixes (overflow, contrast, alignment, responsive issues)
- Improving one section (hero, navbar, footer, card, panel, form)
- Iterating on a chosen UI direction (after `/bq-uiux-variants` selected)

## When NOT to use it

- Generating multiple design directions (use `/bq-uiux-variants`)
- New components / pages (use `/bq-feature`)
- Backend / API changes (use `/bq-fix backend` or `/bq-feature`)
- Major rewrites (use `/bq-fix` or `/bq-feature`)
- No frontend in the project → command exits gracefully

## Syntax

```
/bq-live-edit "<task>"
```

Examples:
- `/bq-live-edit` — interactive mode; ask the user what to edit
- `/bq-live-edit "Edit hero section text and spacing"`
- `/bq-live-edit "Make card titles bigger and fix mobile layout"`
- `/bq-live-edit "Make pricing cards less crowded"`
- `/bq-live-edit "Improve empty state on /dashboard"`
- `/bq-auto live-edit "Open live edit workflow for dashboard"` — same, via auto-mode dispatch

## Preconditions

- `BEQUITE_INITIALIZED`
- Frontend exists in the project

## Required previous gates

- `BEQUITE_INITIALIZED`

## Files to read

- `package.json` / equivalent (detect framework + dev script)
- `.bequite/uiux/SECTION_MAP.md` (if exists)
- `.bequite/uiux/LIVE_EDIT_LOG.md` (prior edits for context)
- `.bequite/state/DECISIONS.md` (design system, tokens)
- Existing `tokens.css` / theme file
- Source files for the target section

## Files to write

- The edit (source file)
- `.bequite/uiux/SECTION_MAP.md` (refresh / add section if missing)
- `.bequite/uiux/LIVE_EDIT_LOG.md` (append entry)
- `.bequite/uiux/screenshots/before-<ts>-<section>.png` (if browser automation)
- `.bequite/uiux/screenshots/after-<ts>-<section>.png` (if browser automation)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Steps

### 1. Detect frontend stack

Read `package.json` / equivalent. Identify framework, dev command, styling approach.

If no frontend detected → exit:
> "No frontend in this project. `/bq-live-edit` requires a frontend. Try `/bq-feature` or `/bq-fix` instead."

### 2. Detect dev server

Look for dev script (`npm run dev`, `pnpm dev`, `bun dev`, etc.).

Ask the user:
> "Is the dev server already running? If yes, what's the URL? If no, want me to print the command to start it?"

**Do not auto-start the dev server** without user OK (changes process state).

### 3. (Optional) Browser inspection

If Playwright (or compatible browser automation) is **already** in the project, or if Playwright MCP is available in the agent host:
- Open the dev URL
- Take initial screenshot → `.bequite/uiux/screenshots/before-<ts>-<section>.png`

If browser automation is **not** available:
- Use code inspection (Read + Grep)
- Ask the user for a screenshot if visual context matters
- Document manual verification steps

**Do NOT auto-install Playwright.** If the task truly needs it and it's not present, surface as a recommendation with a decision section — don't install.

### 4. Map sections (build or refresh SECTION_MAP.md)

If `SECTION_MAP.md` is empty or stale:
- Walk source tree (components, pages, layouts)
- Identify named sections (Hero, Navbar, Footer, PricingCards, DashboardPanel, etc.)
- Record source paths, key classes, props, responsive concerns, editable fields

If the map exists → use it; add the requested section if missing.

### 5. Match user request to a section

User says: "Make pricing cards less crowded."

Match to `PricingCards` entry → source file `components/PricingCards.tsx`.

If no match → ask **one** clarifying question:
> "Which section? I see: Hero, Features, Pricing, Testimonials, Footer."

If still unclear after one question → "I need to inspect the component tree before editing." → walk source, then proceed.

### 6. Apply targeted edit

- Read the relevant source file(s)
- Make the smallest edit that addresses the request
- Use design tokens (no inline `padding: 13px`)
- Preserve existing design system (unless changing it is the explicit goal)
- Don't rewrite the whole page

### 7. Verify

- (If browser automation) refresh + take after-screenshot
- Run frontend build (`npm run build`, `next build`, etc.) to catch typeerrors
- Run frontend tests if any
- Check 360px (mobile) + 1440px (desktop) if responsive matters
- Confirm no other sections regressed

### 8. Log the edit

Append to `.bequite/uiux/LIVE_EDIT_LOG.md`:

```markdown
## <ISO 8601 UTC> — <one-line request>

**Section:** PricingCards
**File(s) changed:** components/PricingCards.tsx
**Before:**
```css
padding: var(--space-2);
gap: var(--space-1);
```
**After:**
```css
padding: var(--space-4);
gap: var(--space-3);
```
**Test/check:** npm run build → OK; visual inspect at 360 + 1440 → no overflow
**Screenshots:**
  - .bequite/uiux/screenshots/before-2026-05-12T10:30Z-pricing.png
  - .bequite/uiux/screenshots/after-2026-05-12T10:35Z-pricing.png
**Notes:** none
```

### 9. Final report

```
✓ Live edit complete — <request>

Section:        <name>
Files changed:  <list>
Build:          OK (or specific output)
Visual check:   <ran via Playwright | manual screenshots requested | code-only>
Screenshots:    <paths if any>

Logged:
  .bequite/uiux/SECTION_MAP.md  (refreshed)
  .bequite/uiux/LIVE_EDIT_LOG.md

Next: another /bq-live-edit "<task>" — or /bq-test for full suite
```

## Edit categories supported

- **Text:** change copy, rewrite for tone, fix typos
- **Sizing:** font sizes, button sizes, icon sizes, container widths
- **Spacing:** padding, margin, gap (via tokens)
- **Colors:** update tokens.css or component-level (per design system)
- **Typography:** font weights, line heights, letter spacing
- **Layout:** flex / grid adjustments, alignment, ordering
- **Motion:** add / remove / tune transitions
- **Imagery:** replace images, adjust aspect ratios
- **Responsive:** fix mobile overflow, fix desktop sparseness
- **Accessibility:** focus states, ARIA labels, color contrast
- **States:** empty, loading, error
- **Copy style:** "make this button match that one"

## Output format

Narrate steps 1-9. Pause **only** to ask the user for dev-server URL or section disambiguation (one question each at most).

## Quality gate

- Section identified before editing (no random file edits)
- Smallest possible change (no full-page rewrite for a 1-section ask)
- Existing design system preserved (unless changing it is the goal)
- Build / tests pass after edit
- LIVE_EDIT_LOG.md entry written with before/after diff
- SECTION_MAP.md refreshed if needed
- No banned weasel words

## Failure behavior

- No frontend → exit cleanly with redirect to `/bq-feature` or `/bq-fix`
- Dev server won't start → pause; ask for correct command + env
- Section ambiguous → one question; then proceed
- Build red after edit → roll back via `git stash` → re-attempt with smaller scope
- Visual regression → roll back; ask user to confirm intent
- User says "undo" → read LIVE_EDIT_LOG, restore from "Before" snippet
- Section not in map AND not findable in source → "I need more context. Can you share a screenshot or describe what's on the page?"

## Mistake memory update

When a live edit surfaces a **frontend pattern worth remembering**, append a MISTAKE_MEMORY entry:

- Design-system slips ("we keep applying `--color-fg-muted` on colored backgrounds; fails AA")
- Responsive misses ("nav overflows at 360px; cards inside `<details>` don't reflow")
- Token-discipline violations ("inline `padding: 13px` found in 4 components; refactor when touched")
- Accessibility patterns ("focus rings missing on icon-only buttons")
- Section-mapping fixes ("PricingCards.tsx was wrong file; actual section is `app/(marketing)/pricing/page.tsx`")

Tag with `[fe]` + sub-tags (`[design]`, `[a11y]`, `[responsive]`, `[token]`). Update SECTION_MAP.md if the mapping changed.

Skip for purely cosmetic preferences (color tweaks the user requested).

See `.bequite/state/MISTAKE_MEMORY.md` template.

---

## Tool neutrality (global rule)

⚠ **Every tool named in this command (Playwright, Chromatic, Percy, Storybook, axe-core, Tailwind, etc.) is an EXAMPLE, not a default.**

Browser automation (Playwright / Puppeteer / WebDriver) is a **candidate** for visual verification. Use only if already installed or if the task genuinely requires visual confirmation. **Do not auto-install.**

CSS frameworks, motion libraries, and design tokens — use what the project already has. If the edit requires a new library, write a decision section (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan) before installing.

The 10 decision questions still apply:
1. Project type? 2. Actual problem? 3. Scale? 4. Constraints? 5. Existing stack? 6. UX needed? 7. Failure risks? 8. Proven tools? 9. Overkill? 10. Best output / least complexity?

See `.bequite/principles/TOOL_NEUTRALITY.md`.

## Usual next command

- `/bq-live-edit "<next task>"` — keep iterating
- `/bq-test` — full test pass after a batch of edits
- `/bq-verify` — full gate matrix
