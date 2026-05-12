# Live Edit strategy (v3.0.0-alpha.4)

**Status:** active
**Adopted:** 2026-05-12
**Command:** `/bq-live-edit "task"`
**Skill:** `bequite-live-edit`
**Reference:** TOOL_NEUTRALITY.md, AUTO_MODE_STRATEGY.md

---

## The principle

Lightweight, agent-assisted, section-by-section live edits on a running frontend.

**It is NOT:**
- A heavy Studio
- A separate app
- A Figma clone
- A local dashboard for BeQuite itself
- A browser-based visual editor

**It IS:**
- A slash command that runs inside Claude Code
- Inspects the running site (via browser automation **only** if frontend exists and the tool is available)
- Maps visible sections to source files
- Applies targeted code edits
- Re-runs / refreshes
- Verifies changed section
- Logs the edit

---

## 1. The mental model

The user describes a change to a section ("make the pricing cards less crowded"). The agent:

1. Identifies which section they mean
2. Finds the source file(s) for that section
3. Edits the smallest scope possible
4. Confirms the edit landed visually (if browser automation available) or via build + test
5. Logs the change

Section identification beats free-form editing. **Map first, edit second.**

---

## 2. When to use

- Targeted edits to a running frontend (text, spacing, font, color, layout, motion)
- Quick visual fixes (overflow, contrast, alignment)
- Improving a single section (hero, navbar, footer, dashboard panel, form, card)
- Iterating on a chosen UI direction (after `/bq-uiux-variants` selected)

## 3. When NOT to use

- Generating multiple design directions (use `/bq-uiux-variants`)
- Rewriting whole pages from scratch (use `/bq-feature` or `/bq-uiux-variants`)
- Backend / API changes (use `/bq-fix backend` or `/bq-feature`)
- New components (use `/bq-feature`)
- Major refactors (use `/bq-fix` or `/bq-feature`)

---

## 4. Workflow

### Step 1 — Detect frontend stack

Read `package.json` / equivalent to identify:
- Framework (Next.js / Nuxt / SvelteKit / Vite + React / plain HTML / etc.)
- Component conventions (App Router / Pages / file-based / etc.)
- Styling approach (Tailwind / CSS modules / styled-components / vanilla / tokens.css)

If no frontend detected → exit with an honest message: "No frontend in this project; `/bq-live-edit` requires a frontend."

### Step 2 — Detect dev server

Look for the dev script (`npm run dev`, `pnpm dev`, `bun dev`, etc.).

Ask the user:
- "Is the dev server already running? (URL: e.g. http://localhost:3000)"
- OR offer to print the start command for them to run

**Don't auto-start the dev server** without confirmation — it changes process state.

### Step 3 — (Optional) Browser inspection

If Playwright (or compatible browser automation) is **already** in the project, or if Playwright MCP is available in the agent host:
- Open the dev URL
- Take initial screenshot → `.bequite/uiux/screenshots/before-<timestamp>-<section>.png`
- Inspect the section the user mentioned

If browser automation is **not** available:
- Use code inspection (Read + Grep on components)
- Ask the user to take a screenshot if needed
- Document manual verification steps

**Never auto-install Playwright.** If it's not present and the task genuinely needs it, surface as a recommendation with a decision section.

### Step 4 — Build / update SECTION_MAP.md

`.bequite/uiux/SECTION_MAP.md` maps visible sections to source files.

If the map is empty or stale:
- Walk the source tree (components, pages, layouts)
- Identify named sections (Hero, Navbar, Footer, PricingCards, DashboardPanel, etc.)
- Record their source file paths, props, key classes, responsive concerns
- (Optional) Take section-level screenshots

If the map exists → use it; add the requested section if missing.

### Step 5 — Map user request to section

User says: "Make the pricing cards less crowded."

Agent matches to the SECTION_MAP entry for "PricingCards" → finds source file `app/(marketing)/pricing/page.tsx` or `components/PricingCards.tsx`.

If no match → ask one question: "Which section do you mean? I see: Hero, Features, Pricing, Testimonials, Footer."

### Step 6 — Apply targeted edit

- Read the relevant source file(s)
- Make the smallest edit that addresses the request
- For spacing: adjust padding/gap/margin tokens
- For text: change copy in component or content file
- For sizes: adjust font-size / icon-size tokens
- For colors: update tokens.css or component-level classes
- For layout: adjust flex/grid properties
- For motion: add/remove transitions

**Do NOT rewrite the entire page** unless asked.

### Step 7 — Verify

- If browser automation available: refresh, take after-screenshot → `.bequite/uiux/screenshots/after-<timestamp>-<section>.png`
- Run frontend build (`npm run build` or `next build` etc.) to catch typeerrors
- Run frontend tests if any exist
- For mobile: resize browser to 360px or check responsive class behavior
- For desktop: check at 1440px

### Step 8 — Log the edit

Append to `.bequite/uiux/LIVE_EDIT_LOG.md`:

```markdown
## <ISO 8601 UTC> — <one-line request>

**Section:** PricingCards
**File(s) changed:** components/PricingCards.tsx
**Before:** padding: var(--space-2); gap: var(--space-1);
**After:**  padding: var(--space-4); gap: var(--space-3);
**Test/check:** npm run build → OK; visual inspect at 360px + 1440px → no overflow
**Screenshots:**
  - .bequite/uiux/screenshots/before-2026-05-12T10:30Z-pricing.png
  - .bequite/uiux/screenshots/after-2026-05-12T10:35Z-pricing.png
**Notes:** none
```

### Step 9 — Report back

```
✓ Live edit complete — <request>

Section:        PricingCards
Files changed:  components/PricingCards.tsx
Verification:   build OK, visual diff captured
Screenshots:    .bequite/uiux/screenshots/{before,after}-*.png

Section map:    .bequite/uiux/SECTION_MAP.md (refreshed)
Edit log:       .bequite/uiux/LIVE_EDIT_LOG.md

Next: another /bq-live-edit "<task>" — or /bq-test if you want full test pass
```

---

## 5. SECTION_MAP.md template

```markdown
# Section Map

**Project:** <name>
**Frontend stack:** <e.g. Next.js 15 App Router + Tailwind v4>
**Dev URL:** http://localhost:3000
**Last refresh:** <ISO 8601 UTC>

## Page: /

### Hero
- **Source:** components/marketing/Hero.tsx
- **Visual description:** Large H1 + subhead + 2 CTAs + product screenshot on the right
- **Key classes / tokens:** `--space-12`, `--text-2xl`, `--color-brand`
- **Text content:** "Ship faster. Worry less." / "BeQuite is the AI tech-lead in your terminal." / "Get started free" / "Watch demo"
- **Responsive concerns:** Screenshot stacks below text on < 768px
- **Editable fields:** Headline, subhead, CTA labels, screenshot source
- **Known problems:** Subhead overflows on 360px iPhone SE

### Features
- **Source:** components/marketing/Features.tsx
- **Visual description:** 3-column grid of icon + title + description
- ...

### Pricing
- **Source:** components/marketing/PricingCards.tsx
- **Visual description:** 3-tier pricing table; highlighted middle tier
- ...

### Footer
- **Source:** components/global/Footer.tsx
- **Visual description:** ...
- ...

## Page: /dashboard

### NavBar
- **Source:** components/dashboard/NavBar.tsx
- ...

### Sidebar
- **Source:** components/dashboard/Sidebar.tsx
- ...

### MainPanel
- **Source:** app/dashboard/page.tsx + components/dashboard/Panels/*.tsx
- ...
```

---

## 6. LIVE_EDIT_LOG.md template

```markdown
# Live Edit Log

Append-only chronicle of every `/bq-live-edit` call. Newest at top.

## <ISO 8601 UTC> — <one-line request>

**Section:** <name from SECTION_MAP>
**File(s) changed:** <list>
**Before:** <diff snippet, ~3 lines>
**After:** <diff snippet, ~3 lines>
**Test/check run:** <commands + results>
**Screenshots:** <paths>
**Notes:** <free-form>

---

(more entries below)
```

---

## 7. Edit categories supported

- **Text:** change copy, rewrite for tone, fix typos
- **Sizing:** font sizes, button sizes, icon sizes, container widths
- **Spacing:** padding, margin, gap (uses design tokens)
- **Colors:** update tokens.css or component-level (per design system)
- **Typography:** font weights, line heights, letter spacing
- **Layout:** flex / grid adjustments, alignment, ordering
- **Motion:** add / remove / tune transitions, hover effects
- **Imagery:** replace images, adjust aspect ratios
- **Responsive:** fix mobile overflow, fix desktop sparseness
- **Accessibility:** focus states, ARIA labels, color contrast
- **States:** improve empty / loading / error states
- **Copy from one element to another:** "make this button match that one"

---

## 8. Quality rules during live edit

- Make small targeted edits
- Don't rewrite the full page unless asked
- Don't destroy working layout
- Preserve existing design system (unless changing it is the goal)
- Use design tokens — never inline `padding: 13px`
- Check desktop + mobile when feasible
- Run frontend build / tests if available
- Cite the line(s) changed in the log
- No banned weasel words in completion claims

---

## 9. Tool neutrality

Per TOOL_NEUTRALITY.md:

- **Playwright** is one candidate for browser automation. Use only if already installed or if the task genuinely requires it. Don't auto-install.
- **Storybook** is one candidate for component preview. Use only if already in project.
- **Chromatic / Percy** are candidates for visual regression. Don't add by default.
- **CSS frameworks** (Tailwind / vanilla / CSS modules / styled-components) — use what the project already uses.
- **Design tokens** — use what's already defined; don't invent a new system mid-edit.

---

## 10. Anti-patterns to refuse

- **Editing without a section map** ("I'll just open files and edit") — leads to wrong-file edits
- **Rewriting the full page** for a 1-section request
- **Installing Playwright** to take screenshots for a 2-line CSS change
- **Adding a new design library** mid-edit (use `/bq-feature` for new lib decisions)
- **Skipping the LIVE_EDIT_LOG entry** ("it's a small change") — every edit is logged
- **Editing tokens.css without recording the change** in DECISIONS.md (token changes affect the whole UI)
- **Auto-starting the dev server** without user consent (changes process state)
- **Claiming "looks great"** without verification (banned weasel)

---

## 11. Failure modes

| Failure | Recovery |
|---|---|
| Section not in map | Inspect source, add to map, then edit |
| Multiple components match the section | Ask user to disambiguate (one question) |
| Build red after edit | Roll back via git stash; re-attempt with smaller scope |
| Visual regression | Roll back; ask user to confirm the intent |
| Dev server won't start | Pause; ask user for correct command + env |
| No frontend | Exit; suggest `/bq-feature` or `/bq-fix` instead |

---

## 12. Rollback

Every live edit must be reversible:

- Git working-tree edits → `git checkout -- <file>` or `git stash`
- Token changes → record original value in LIVE_EDIT_LOG before changing
- Component rewrites → preserve original in `<Component>.tsx.before-<timestamp>` if non-trivial

If the user says "undo last live edit" → read LIVE_EDIT_LOG, restore from the "Before" snippet.

---

## 13. What this strategy is NOT

- **Not** a visual builder (no drag-and-drop, no WYSIWYG)
- **Not** auto-magic (every edit is traced to specific file lines)
- **Not** a substitute for a designer (this executes design decisions, doesn't replace them)
- **Not** browser-required (works with code inspection alone if browser automation isn't available)
- **Not** a Figma export (designs come from `/bq-uiux-variants` or external design files)
