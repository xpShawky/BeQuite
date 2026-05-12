# UI/UX Variants strategy (v3.0.0-alpha.4)

**Status:** active
**Adopted:** 2026-05-12
**Command:** `/bq-uiux-variants [count] "task"`
**Skill orchestration:** `bequite-ux-ui-designer`, `bequite-frontend-quality`
**Reference:** TOOL_NEUTRALITY.md, AUTO_MODE_STRATEGY.md

---

## The principle

When the user wants to explore UI direction before committing, generate multiple **isolated** design variants in parallel. Compare. User picks one. Merge winner into main UI. Archive rejected.

The agent does NOT rewrite the existing UI in place. It creates side-by-side previews.

---

## 1. Count discipline

| Project signal | Default count | Allowed range |
|---|---|---|
| User explicitly requested N | N | 1–10 |
| No count provided, small project | 3 | – |
| Design-critical project | 5 | – |
| User says "many" / "lots" | 5 | – |
| User explicitly requests 10 | 10 | – |

**Never exceed 10 without explicit user confirmation.** 10 variants is expensive — token budget, attention budget, and code-review budget all suffer past 10.

---

## 2. Direction selection

Variant directions are **not hardcoded**. The agent picks them based on:

- Project type (admin dashboard vs. consumer marketing vs. medical records vs. game studio …)
- Target users (power users vs. first-time visitors vs. enterprise procurement)
- Brand tone (premium / playful / functional / serious / trustworthy)
- Existing design system (if any)
- Competitor study (if research exists)

### Example direction palette (illustrative — not mandatory)

For a SaaS admin dashboard, candidates could include:
- Premium cinematic (Linear-style)
- Enterprise SaaS (Salesforce-style)
- Developer tool (Vercel / Railway style)
- Minimal utility (focused on data density)
- Apple-like clean (lots of whitespace + serif headlines)
- Dark futuristic (high contrast + accent glow)
- Light professional (printable feel)
- Data-heavy command center

For consumer marketing, candidates could include:
- Premium product
- Playful illustrated
- Editorial magazine
- Conversion-focused
- Minimal landing

**These are examples, not defaults.** The agent picks directions that genuinely fit the project — and explains why.

Per tool neutrality: every named style / tool is a candidate. Reject any that doesn't fit the project.

---

## 3. Isolation strategy

Variants live in **isolated locations** so the original UI keeps working.

### Strategy A — routed previews (preferred when project has routing)

```
/uiux/v1
/uiux/v2
/uiux/v3
…
```

Each route renders one full variant. Original routes unchanged.

For Next.js App Router: `app/uiux/v1/page.tsx`
For Next.js Pages Router: `pages/uiux/v1.tsx`
For Nuxt: `pages/uiux/v1.vue`
For SvelteKit: `routes/uiux/v1/+page.svelte`
For plain HTML: separate static files under `uiux-v1/`, `uiux-v2/`

### Strategy B — isolated components (when routing is harder)

```
src/uiux-variants/Variant01/
src/uiux-variants/Variant02/
src/uiux-variants/Variant03/
```

Each folder is a self-contained component tree. Wire them to a single preview page or Storybook if available.

### Strategy C — Storybook stories (when Storybook is already in the project)

Add a `UIUX/Variants` category with one story per variant.

**The agent picks A, B, or C based on what already exists in the project.** Never installs Storybook just to use Strategy C.

---

## 4. Workflow

### Step 1 — Read context

- `.bequite/audits/DISCOVERY_REPORT.md` (frontend stack, existing components)
- `.bequite/audits/RESEARCH_REPORT.md` (UX research if available)
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (current plan)
- `.bequite/state/DECISIONS.md` (locked design decisions)
- Existing `tokens.css` / theme file (if any)
- Existing components and their patterns

### Step 2 — Identify target users + emotion

If not already in research, ask 1-2 questions:
- "Who are the primary users? (one sentence)"
- "What feeling should this UI convey? (premium / playful / functional / serious / …)"

Default answers: power users; functional + clean.

### Step 3 — Propose N variant directions

Output a table:

| # | Direction | Target feeling | User fit | Why this for this project |
|---|---|---|---|---|

Agent picks directions. Doesn't ask user to pick from a list (that's the user's job after they're built).

### Step 4 — Generate variants in isolation

For each variant:
- Create the isolated route or component
- Apply the direction's design tokens
- Build one complete screen (the most-trafficked, e.g. dashboard home or landing hero)
- Include real states (data, empty, loading, error) — no Lorem ipsum
- Make responsive (mobile 360px + desktop 1440px)
- Add to SECTION_MAP.md

### Step 5 — Comparison report

Write `.bequite/uiux/UIUX_VARIANTS_REPORT.md` (template below).

### Step 6 — Pause for user selection (hard human gate)

The agent stops and prints:

```
✓ <N> UI variants generated. Preview at:

  Variant 01 — <direction>: /uiux/v1
  Variant 02 — <direction>: /uiux/v2
  …

Comparison: .bequite/uiux/UIUX_VARIANTS_REPORT.md

Recommendation: Variant <N> — <reasoning>

Pick one (reply with the number, e.g. "3") and I'll merge it into the main UI.
```

### Step 7 — Merge winner

Once user picks:
- Copy the winner's design tokens + components to the main UI tree
- Update `tokens.css` / theme
- Rewrite affected pages to use the new direction
- Update `.bequite/state/DECISIONS.md` with the design choice
- Write `.bequite/uiux/selected-variant.md` recording which won and why

### Step 8 — Archive rejected

- Move rejected variants to `.bequite/uiux/archive/<timestamp>/`
- Or delete from disk if user confirms
- **Default:** archive (preserve for reference); user can delete later

---

## 5. UIUX_VARIANTS_REPORT.md template

```markdown
# UI/UX Variants Report

**Generated:** <ISO 8601 UTC>
**Project:** <name>
**Variants generated:** <N>
**Reference screen:** <which screen was redesigned, e.g. "Dashboard home">

## Direction palette chosen for this project

| # | Direction | Target feeling | User fit | Why |
|---|---|---|---|---|

## Variant 01 — <direction>

**Design direction:** <name>
**Target feeling:** <emotion>
**User fit:** <persona match>
**Components changed:** <list>
**Route or preview path:** /uiux/v1
**Screenshot:** .bequite/uiux/screenshots/v1-desktop.png + v1-mobile.png

**Strengths:**
- <bulleted>

**Weaknesses:**
- <bulleted>

(repeat for each variant)

## Comparison

| Criterion | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| Fits primary user | ✓ | ✓ | ✗ | ⚠ | ✓ |
| Brand alignment | ✓ | ⚠ | ✓ | ✓ | ✓ |
| Accessibility (axe) | ✓ | ✓ | ✓ | ⚠ | ✓ |
| Responsive | ✓ | ✓ | ✓ | ✓ | ✓ |
| Loading / empty / error states | ✓ | ✓ | ⚠ | ✓ | ✓ |
| Doesn't look AI-generated | ✓ | ✗ | ✓ | ✓ | ⚠ |

## Recommendation

**Winner: Variant <N> — <direction>**

**Why:**
1. <reason>
2. <reason>
3. <reason>

**Runner-up: Variant <M>**
(in case the user prefers another path)

## Variants to archive after selection

V1, V2, V3, V4 → `.bequite/uiux/archive/<timestamp>/`
```

---

## 6. Variant acceptance criteria

Every variant must pass:

- [ ] No broken layout at 360px or 1440px
- [ ] No hidden text (color ≠ background)
- [ ] No text escaping cards / containers
- [ ] No dead buttons (every interactive element does something or is `disabled`)
- [ ] Contrast passes WCAG 2.1 AA (axe-core green)
- [ ] Loading state present (skeleton, not spinner-forever)
- [ ] Empty state present (with action)
- [ ] Error state present
- [ ] Visual hierarchy clear (one primary action per screen)
- [ ] Motion is purposeful (not distracting)
- [ ] Design fits the project's actual users (not generic "modern dashboard")
- [ ] Doesn't trigger the 15 AI-slop anti-patterns (purple-blue gradients, three Lucide icons in a row, Inter without reason, nested cards with shadows, etc.)

Variants that fail any of these are flagged in the report; the user can still pick them if they want to fix during merge, but it's logged.

---

## 7. Tool neutrality

Per TOOL_NEUTRALITY.md:

- Impeccable is **one reference** — not mandatory
- shadcn/ui is **one candidate** for the component layer — not mandatory
- Tailwind / vanilla CSS / CSS modules / styled-components / Panda CSS — all candidates
- Motion libraries (Framer Motion / Motion One / GSAP) — only if already in project or justified
- Storybook — only if already in project

**Don't auto-install** any of these. If a variant direction requires a library, the agent writes a decision section before installing.

---

## 8. When NOT to use variants

- Tiny color tweaks (just change tokens.css directly)
- Single component edits (use `/bq-live-edit`)
- Backend / API changes (no UI involved)
- Quick fixes (use `/bq-fix`)

Variants are for **direction exploration**, not iteration on a chosen direction.

---

## 9. Anti-patterns

- **Rewriting the existing UI in place** — destroys reference; can't compare
- **Variants that differ only in color** — not different directions
- **5 variants when 3 would have answered the question** — wastes tokens
- **Picking the winner without user input** — this is the one hard gate; user owns design choice
- **Merging without archiving rejected** — loses reference for next iteration
- **Auto-installing Storybook / Framer Motion / etc.** to support a variant — violates tool neutrality

---

## 10. What this strategy is NOT

- **Not** a substitute for user research (variants explore execution, not strategy)
- **Not** a way to A/B test in production (variants are pre-production exploration)
- **Not** infinite-loop iteration (cap at 10; if user keeps rejecting all, run `/bq-research` to surface the real disagreement)
- **Not** a Figma replacement (this is code, not mockups)
