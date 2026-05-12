---
description: Generate multiple UI/UX design directions in isolation. 1-10 variants. Each lives in an isolated route (/uiux/v1) or component (src/uiux-variants/Variant01). Original UI untouched. User picks winner; agent merges. Produces UIUX_VARIANTS_REPORT.md.
---

# /bq-uiux-variants — explore N design directions

## Purpose

Generate **N isolated UI variants** so the user can choose a design direction before committing. Each variant is a different direction (not a color tweak). Original UI stays intact. After selection, the winner merges into main UI; rejected variants archive.

Full strategy: `docs/architecture/UIUX_VARIANTS_STRATEGY.md`.

## When to use it

- Starting a new UI without a locked direction
- Redesigning an existing UI ("the dashboard feels off")
- Before committing to a major visual rewrite
- Exploring before a stakeholder review

## When NOT to use it

- Tiny tweaks (use `/bq-live-edit`)
- Single-component changes (use `/bq-live-edit` or `/bq-fix`)
- After a direction is already locked (use `/bq-live-edit` or `/bq-feature`)
- Non-UI changes (use other commands)

## Syntax

```
/bq-uiux-variants [count] "<task / scope>"
```

Examples:
- `/bq-uiux-variants 3` — generate 3 variants for the current main screen
- `/bq-uiux-variants 5 "five dashboard concepts"` — 5 variants of the dashboard
- `/bq-uiux-variants 10 "ten landing page concepts"` — 10 variants (rare — needs confirmation)
- `/bq-uiux-variants "redesign the hero"` — default 3 variants
- `/bq-auto uiux variants=5 "dashboard concepts"` — same, via auto-mode dispatch

## Count rules

| Signal | Default count |
|---|---|
| Number provided | Use it (1–10) |
| No number, small / utility project | 3 |
| No number, design-critical project | 5 |
| User says "many" | 5 |
| User explicitly requests 10 | 10 (with confirmation prompt) |

**Never exceed 10** without explicit user confirmation.

## Preconditions

- `BEQUITE_INITIALIZED`
- Frontend exists in the project (Next.js / Nuxt / SvelteKit / Vite + React / plain HTML / etc.)

## Required previous gates

- `BEQUITE_INITIALIZED`
- `MODE_SELECTED`

## Files to read

- `.bequite/audits/DISCOVERY_REPORT.md` (frontend stack + components)
- `.bequite/audits/RESEARCH_REPORT.md` (UX research if available)
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (if exists)
- `.bequite/state/DECISIONS.md` (locked design decisions)
- Existing `tokens.css` / theme file
- Existing component files

## Files to write

- N isolated variants in `app/uiux/v1/…` OR `src/uiux-variants/Variant01/…` (per stack)
- `.bequite/uiux/UIUX_VARIANTS_REPORT.md` — comparison + recommendation
- `.bequite/uiux/SECTION_MAP.md` (updated with variant sections)
- `.bequite/uiux/screenshots/v<N>-{desktop,mobile}.png` (if browser automation available)
- `.bequite/uiux/selected-variant.md` (after user picks)
- `.bequite/state/DECISIONS.md` (design direction recorded)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Steps

### 1. Read context + identify target users

Read project state. If user persona / target feeling are not yet recorded, ask 1-2 questions max:
- "Who are the primary users? (one sentence)"
- "What feeling should this UI convey? (premium / playful / functional / serious / …)"

Use defaults if user says "all defaults": power users + functional/clean.

### 2. Propose N variant directions

Pick directions based on project type, target users, brand tone. Output:

```
Variant directions proposed for this project:

  V1 — Premium cinematic (Linear-style)       — for users who value polish
  V2 — Enterprise SaaS (Salesforce-style)     — for procurement-driven buyers
  V3 — Minimal utility (Notion-style)         — for daily-driver power users
  V4 — Data-heavy command center              — for ops-focused viewers
  V5 — Light professional + serif headlines   — for trust-heavy contexts

Generating variants now…
```

Each direction is **different**, not a color shift.

### 3. Choose isolation strategy

Pick A, B, or C based on what the project already has:

- **A. Routed previews** — `app/uiux/v1/page.tsx`, `/uiux/v2`, etc.
- **B. Isolated components** — `src/uiux-variants/Variant01/`, `Variant02/`, etc.
- **C. Storybook stories** — if Storybook is already in the project

Don't install Storybook or any router just to use a strategy.

### 4. Generate variants

For each variant:
- Apply the direction's design tokens (font, color, spacing scale)
- Build one complete reference screen (the most-trafficked: dashboard home, landing hero, etc.)
- Include real states (data, empty, loading, error)
- Responsive: 360px mobile + 1440px desktop
- Add entry in SECTION_MAP.md
- (If browser automation available) screenshot both viewports

### 5. Write UIUX_VARIANTS_REPORT.md

```markdown
# UI/UX Variants Report

**Generated:** <ISO 8601 UTC>
**Project:** <name>
**Variants generated:** <N>
**Reference screen:** <e.g. Dashboard home>

## Direction palette chosen

| # | Direction | Target feeling | User fit | Why for this project |
|---|---|---|---|---|

## Variant 01 — <direction>
**Direction:** <name>
**Target feeling:** <emotion>
**User fit:** <persona>
**Components changed:** <list>
**Preview path:** /uiux/v1 (or src/uiux-variants/Variant01)
**Screenshot:** .bequite/uiux/screenshots/v1-desktop.png

**Strengths:** ...
**Weaknesses:** ...

(repeat per variant)

## Comparison

| Criterion | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| Fits primary user | ✓ | ✓ | ✗ | ⚠ | ✓ |
| Brand alignment | ✓ | ⚠ | ✓ | ✓ | ✓ |
| axe-core | ✓ | ✓ | ✓ | ⚠ | ✓ |
| Responsive | ✓ | ✓ | ✓ | ✓ | ✓ |
| Real states | ✓ | ✓ | ⚠ | ✓ | ✓ |
| Not AI-slop | ✓ | ✗ | ✓ | ✓ | ⚠ |

## Recommendation

**Winner: Variant <N> — <direction>**

Why:
1. <reason>
2. <reason>
3. <reason>

**Runner-up: Variant <M>**
```

### 6. Pause for user selection (hard human gate)

Print:

```
✓ <N> UI variants generated.

Preview at:
  V1 — <direction>: /uiux/v1
  V2 — <direction>: /uiux/v2
  ...

Full comparison: .bequite/uiux/UIUX_VARIANTS_REPORT.md
Recommendation: Variant <N> — <reasoning>

⏸ Pick a winner (reply with number, e.g. "3"). I'll merge it into the main UI.
```

Wait for user.

### 7. Merge winner

Once user picks (e.g. "3"):
- Copy V3's design tokens to main `tokens.css`
- Rewrite affected components / pages to use V3's patterns
- Update `.bequite/state/DECISIONS.md` with the design choice + reason
- Write `.bequite/uiux/selected-variant.md`

### 8. Archive rejected (default) or delete (if user confirms)

- **Default:** move rejected variants to `.bequite/uiux/archive/<timestamp>/`
- User can run `/bq-fix "delete archived variants"` later if disk space matters

### 9. Verify merged UI

- Run frontend build (`npm run build` or equivalent)
- (If browser automation) refresh + screenshot the merged screen
- Confirm no regressions on existing routes

### 10. Final report

```
✓ UI direction locked: Variant <N> — <direction>

Files changed:
  tokens.css            (design tokens swapped)
  components/<list>     (updated to new direction)
  app/<pages>           (re-themed)

Archived:
  V1, V2, V4, V5 → .bequite/uiux/archive/<timestamp>/

Verification:
  npm run build       → OK
  Visual regression   → reviewed (screenshots in .bequite/uiux/screenshots/)

Decision: .bequite/uiux/selected-variant.md
Updated:  .bequite/state/DECISIONS.md

Next: /bq-live-edit to refine sections — or /bq-feature for new pages
```

## Output format

Narrate each step. Pause **only** at step 6 (winner selection — the hard human gate).

## Quality gate

- Each variant passes the variant acceptance criteria (see UIUX_VARIANTS_STRATEGY.md §6)
- Original UI is untouched until user picks
- UIUX_VARIANTS_REPORT.md exists with full comparison
- User has explicitly picked a winner
- Merged UI passes build + visual check
- Rejected variants are archived (not deleted by default)
- No banned weasel words

## Failure behavior

- Frontend stack unclear → ask the user to confirm; don't assume
- User wants > 10 → confirm explicitly before generating
- A variant fails build → mark in the report; user can still pick it (will be fixed during merge)
- User rejects all variants → run `/bq-research` to surface what's missing in the project's design brief, then re-propose

## Tool neutrality (global rule)

⚠ **Every named style direction, component library, motion library, or design system in this command is an EXAMPLE, not a mandatory default.**

The directions listed in step 2 (Linear-style, Salesforce-style, Notion-style, etc.) are **references**, not commitments. Pick directions that fit the project — propose them with rationale.

**Do not auto-install:** Framer Motion, GSAP, Storybook, Chromatic, Tailwind plugins, or any new design library to support a variant. If a variant truly needs a library, write a decision section (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan) before installing.

The 10 decision questions still apply:
1. Project type? 2. Actual problem? 3. Scale? 4. Constraints? 5. Existing stack? 6. UX needed? 7. Failure risks? 8. Proven tools? 9. Overkill? 10. Best output / least complexity?

See `.bequite/principles/TOOL_NEUTRALITY.md`.

## Usual next command

- After merge: `/bq-live-edit "<refinement>"` to iterate within the chosen direction
- `/bq-feature` for new UI features
- `/bq-test` to verify the new UI doesn't break anything
