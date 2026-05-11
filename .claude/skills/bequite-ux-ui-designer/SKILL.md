---
name: bequite-ux-ui-designer
description: UX/UI design procedures — 10 design principles, 15 AI-slop anti-patterns, design tokens, hierarchy, density, typography, color, accessibility (WCAG 2.1 AA), responsive baseline, micro-interactions. Pairs with bequite-frontend-quality for implementation-side checks. Loaded by /bq-plan, /bq-feature, /bq-audit for UI projects.
allowed-tools: Read, Glob, Grep, WebFetch
---

# bequite-ux-ui-designer — make it not look AI-generated

## Why this skill exists

AI-generated UIs have a tell. Purple-to-blue gradients. Inter for everything. Bunch of nested cards with shadows. Three Lucide icons in a row. Lorem ipsum that looks "professional" but says nothing.

This skill encodes the 10 principles + 15 anti-patterns + token discipline that makes a UI **not look like every other AI demo**.

Pairs with `bequite-frontend-quality` (which detects AI-slop in shipped code).

---

## The 10 design principles

1. **Hierarchy first.** One primary action per screen. Secondary actions are clearly de-emphasized. Tertiary actions live in menus or hover states.

2. **Density is a feature.** Empty space communicates importance. But too much empty space looks like "I don't know what to put here."

3. **Type carries meaning.** Use exactly 2 fonts: one for body, one for display. Or use 1 with weight variation. Sans-serif default. Serif for editorial. NEVER Inter as a fallback for "I don't know what to pick."

4. **Color is signal, not decoration.** Brand color appears in:
   - Primary CTA
   - Active state of nav
   - Important data (alerts, links)
   Everywhere else: grayscale or muted tones.

5. **Whitespace > borders.** Group with space, separate with hairline rules. Cards with heavy borders + shadows = AI-slop.

6. **Motion has purpose.** Easing curves matter — `ease-out` for entry, `ease-in` for exit. Duration: 150-250ms for hover, 250-400ms for layout shifts. NO bounce effects unless playful brand.

7. **Real content, not Lorem ipsum.** Mock data should look like real data. Names, emails, times that make sense.

8. **Empty states aren't optional.** Every list-view has an empty state with: icon (one, simple), one-line headline, one-line subhead, ONE CTA.

9. **Error states aren't optional.** Every form field has error states. Every API call has loading, empty, error, success states.

10. **Mobile-first decisions.** Design for smallest viewport first. Desktop is the easy adaptation.

---

## The 15 AI-slop anti-patterns

When you see these in a UI, it's AI-generated:

1. **Purple-to-blue gradient** — banned. Use a single brand color or neutral.
2. **Three Lucide icons in a row** — banned. Use icons sparingly; never as a substitute for a label.
3. **Inter as default** — banned without explicit reasoning. Pick a deliberate font.
4. **Nested cards with shadows** — banned. One card depth max.
5. **"Powered by AI" badges** — banned in 2026. Users assume it. Don't brag.
6. **Lorem ipsum in screenshots** — banned. Use realistic placeholder data.
7. **Five-column feature grids on landing** — banned. Pick THE feature.
8. **Generic "trusted by" logos with no proof** — banned. If you don't have logos, say what you're working toward.
9. **Sparkle/star icons everywhere** — banned. Save sparkles for actual magic moments.
10. **Auto-generated SVG illustrations of "diverse teams"** — banned. They all look the same.
11. **Three-line headlines that say nothing** — banned. One line, concrete benefit.
12. **Hero CTAs that say "Get started" with no specificity** — banned. "Sign up free" or "Try it on your data" is better.
13. **Pricing tiers with checkmarks for "✓ AI-powered insights"** — banned. State what the feature DOES.
14. **Gray text on colored backgrounds (contrast fail)** — banned. WCAG 2.1 AA at minimum.
15. **"Open source" badge with no link to repo** — banned. If you're open source, link the repo.

---

## Design tokens (the contract)

Every project ships with `tokens.css`:

```css
:root {
  /* Color: deliberate palette, no AI-defaults */
  --color-bg: #fafaf9;            /* warm white, not pure */
  --color-fg: #1c1917;            /* warm dark, not pure black */
  --color-accent: #c2410c;        /* one brand color, picked deliberately */
  --color-muted: #78716c;
  --color-border: #e7e5e4;
  --color-success: #16a34a;
  --color-warning: #ca8a04;
  --color-danger: #dc2626;

  /* Type */
  --font-body: "Inter Tight", system-ui, sans-serif;  /* deliberate, not generic Inter */
  --font-display: "Spectral", Georgia, serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  /* Type scale */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.5rem;
  --text-2xl: 2rem;
  --text-3xl: 3rem;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --space-16: 4rem;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 12px;

  /* Motion */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-fast: 150ms;
  --duration-base: 250ms;
}
```

Rules:
- Never inline color values in components — use tokens
- Never `font-family: Inter` outside `tokens.css` (or whichever font you picked)
- Never `border-radius: 8px` outside tokens

---

## Hierarchy enforcement

Per screen:
- ONE primary action (filled button, brand color)
- 0-2 secondary actions (outline buttons)
- Many tertiary actions (text buttons, icon buttons in toolbars)

Per page:
- ONE H1
- 1-3 H2s
- H3s only where they nest meaningfully

Per text block:
- Body text: 16px+ (don't go below)
- Line-height: 1.5-1.7 for body
- Line-length: 50-75 characters (constrains paragraph width)

---

## Color discipline

**Brand color usage:**
- Primary CTA buttons
- Active state of navigation
- Links in body text
- Important data points (badges, indicators)

**NOT for:**
- Decorative gradients
- Background washes
- Random accent stripes
- Card hover states

**Neutral palette:**
- One warm or one cool base
- 5-7 steps from background → text
- Use Tailwind's stone / zinc / slate / neutral — not "gray" (too cold)

**Accessibility:**
- Contrast: WCAG 2.1 AA = 4.5:1 for body, 3:1 for large text
- Test with axe-core in CI
- Test in grayscale (does the UI still work?)

---

## Component patterns (shadcn/ui first)

Default to shadcn/ui components — copy-paste into your repo, own them. Why:
- Accessible by default (built on Radix UI primitives)
- Tailwind-native styling
- No version-lock to a UI lib

Customize per your tokens. Don't ship default shadcn — that's also AI-slop.

For 2026:
- shadcn v3+ has built-in registry MCP — use it via `shadcn registry:add`
- 21st.dev Magic MCP for AI-assisted component generation (paid)
- tweakcn.com for visual theme editing → export CSS variables

---

## Accessibility baseline

Every shipping UI passes:

- **axe-core** — zero serious or critical issues
- **Keyboard navigation** — every interactive element reachable via tab, activatable via enter/space
- **Focus indicators** — visible, 2px ring or outline; never `outline: none` without replacement
- **Color contrast** — WCAG 2.1 AA
- **Screen reader** — semantic HTML, ARIA only where HTML can't do it
- **Reduced motion** — respect `prefers-reduced-motion`
- **Touch targets** — min 44×44px for primary actions

---

## Responsive baseline

Three breakpoints minimum:
- Mobile: < 768px (design for this FIRST)
- Tablet: 768-1024px
- Desktop: > 1024px

Don't ship desktop-only. Even B2B users have phones.

---

## Micro-interactions

Add these sparingly:
- Button hover → subtle color shift + 1px transform
- Form field focus → 2px ring in brand color
- Toast notifications → slide in from top, 3-5s auto-dismiss, swipe to dismiss
- Loading states → skeleton screens (not spinners) for content; spinners only for actions
- Empty list → fade in, no animation

Avoid:
- Cursor trails
- Confetti without intent
- Page-load animations longer than 400ms
- Anything that delays user interaction

---

## When activated by /bq-feature (UI feature)

For a new UI feature:
1. Read existing tokens.css — match the language
2. Define what's on this screen (data + actions)
3. Pick the ONE primary action
4. Write empty / loading / error / success states
5. Run axe-core on the change
6. Test keyboard nav
7. Check on 375px viewport

---

## When activated by /bq-audit (UI audit)

For an existing UI:
1. Scan for the 15 AI-slop patterns
2. Verify tokens.css exists + is the source of truth
3. Run axe-core baseline
4. Sample 3 screens for hierarchy violations
5. Test mobile viewport
6. Note findings in FULL_PROJECT_AUDIT.md UI section

---

## When activated by /bq-fix (UI bug)

For UI bugs:
- Visual bug → check token usage, browser-specific CSS
- State bug → check React state lifting, stale closures, key prop on lists
- Accessibility bug → run axe-core, check the specific element

---

## What this skill does NOT do

- Generate art / illustrations (use design plugin or hire an illustrator)
- Pick a brand color from scratch (use a designer or be deliberate yourself)
- Write marketing copy (use brand-voice plugin)
- Replace usability testing with real users (irreplaceable)

---

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, design system, or workflow named in this file (Inter Tight, Spectral, JetBrains Mono, shadcn/ui, Radix, tweakcn, Magic, Mobbin, Dribbble, axe-core, Pa11y, etc.) is an EXAMPLE, not a mandatory default.**

The 10 design principles + 15 AI-slop anti-patterns + token discipline are **universal rules**. Specific font / library picks are candidates per project.

**Do not say:** "Use Inter Tight."
**Say:** "Inter Tight is one candidate for the body font. Compare against alternatives that fit the brand's voice and audience. Use it only if it fits — and record the reason in tokens.css."

The 10 decision questions:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

Write a decision section before adopting (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan).

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.
