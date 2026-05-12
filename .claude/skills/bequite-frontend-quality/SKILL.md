---
name: bequite-frontend-quality
description: Frontend design + UX quality. Detects "AI-looking UI" — bad colors, dead buttons, hidden text, poor spacing, mock data masquerading as live. Loaded when the project has a UI. Pairs with Impeccable.
allowed-tools: ["Read", "Glob", "Grep", "WebFetch", "WebSearch", "Edit", "Write"]
---

# bequite-frontend-quality

Frontend quality discipline. Invoked when the project has UI — Next.js, Nuxt, SvelteKit, Vite + React, plain HTML, anything visual.

**References:**
- Impeccable (Paul Bakaus) — https://github.com/pbakaus/impeccable
- The 15 AI-slop patterns + the 10 design principles below
- shadcn/ui — https://ui.shadcn.com
- tweakcn theme editor — https://tweakcn.com

## When this skill activates

- `/bq-audit` when the discovered repo has a frontend
- `/bq-add-feature` when adding a UI feature
- `/bq-feature` when the feature is UI-typed (12-type router)
- `/bq-review` when reviewing a UI PR
- `/bq-red-team` when adversarial-reviewing a UI
- `/bq-uiux-variants` for variant quality checks (no broken layout, contrast, real states)
- `/bq-live-edit` for section-by-section edits (delegates section mapping to `bequite-live-edit`)
- `/bq-auto uiux` / `/bq-auto frontend` / `/bq-auto live-edit` / `/bq-auto variants`

## The 10 design principles

1. **Hierarchy** — every screen has one primary action. Others are secondary.
2. **Recorded typography** — pick a font deliberately. Inter is fine but state WHY it was chosen.
3. **Three-color system** — one primary brand, one neutral scale, one accent. More = AI-slop.
4. **Spacing scale: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128** — never `padding: 13px`.
5. **Eased motion** — `cubic-bezier(0.16, 1, 0.3, 1)` style. No bounce, no elastic.
6. **Real states** — empty, loading, error all real. Hardcoded "no data" placeholder is dishonest.
7. **Mobile-first + RTL + keyboard** — every screen passes axe-core + works at 360px + works for RTL locales.
8. **Density variants** — comfortable for mouse, compact for power users, generous for touch.
9. **Consistency over cleverness** — same button style across screens. Same heading scale. Same loading spinner.
10. **Skeptic kill-shot** — "what happens to this UI when the data is 10x bigger than I designed for?"

## The 15 AI-slop tells (refuse these)

1. **Inter font everywhere with no recorded reason.** Inter is fine but the choice must be recorded in tokens.css.
2. **Purple-blue gradients.** Used by 80% of AI-generated dashboards. Refuse unless brand is genuinely purple.
3. **Cards nested in cards.** One card depth. Maybe two for very specific reasons.
4. **Gray-on-color text.** Fails contrast. axe-core catches this. The fix is always to choose: text color or background color, not both gray.
5. **Bounce / elastic / spring animations.** Never. Apple's macbook-pro uses cubic-bezier(0.16, 1, 0.3, 1). Match that.
6. **Made-up chart data.** "Revenue chart" with fake bars. Either show real data or show the empty state.
7. **Skeleton loaders that never resolve.** If the skeleton hangs > 2s, fall back to a real error state.
8. **Weak empty states.** "No items found" with no action. The empty state must say "create one" with a button.
9. **Bad mobile layouts.** Buttons < 44px touch target. Text overlapping. Horizontal scroll on body.
10. **Poor contrast** that passes "looks OK in my Figma" but fails WCAG AA. Test with axe-core.
11. **Missing focus states.** Keyboard navigation invisible. Add `:focus-visible` styles.
12. **Repeated icons** that don't differentiate context. Trash icon used for "delete," "archive," AND "close" in the same screen.
13. **UX copy in passive voice.** "An error has occurred" → "We couldn't save your changes — try again."
14. **Wrong typographic hierarchy.** Body text = section heading. H1 = H4. Establish a scale and stick.
15. **Over-rounded everything.** `border-radius: 24px` on a 32px button = ovoid pill blob. Stick to the radius scale.

## Component sourcing order

When adding a new UI component, search in this order:

1. **Project's existing components** — does `components/` already have something similar? Use + extend.
2. **shadcn/ui** — `npx shadcn@latest add <component>` — copies the source into your repo, fully owned.
3. **tweakcn theme editor** — for theme customization, then export tokens.css.
4. **Aceternity UI / Magic / Origin UI** — for specific animations / templates. Vet license; some are commercial.
5. **21st.dev Magic MCP** — `@21st-dev/magic` — AI-assisted component generation. Per-prompt quota.
6. **context7** — `@upstash/context7-mcp` — version-pinned docs. Useful for "how does library X do Y?"
7. **Custom** — only if 1-6 didn't fit. Write the component yourself.

## Tokens.css discipline (when Doctrine `default-web-saas` active)

Every visual value comes from `tokens.css`:

```css
:root {
  /* Color (3-tier: primary brand + neutral scale + accent) */
  --color-brand: <chosen for a recorded reason>;
  --color-bg: <neutral 1>;
  --color-fg: <neutral 9>;
  --color-fg-muted: <neutral 6>;
  --color-accent: <complementary>;

  /* Spacing scale */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  /* ... */

  /* Type scale */
  --text-body: 1rem;
  --text-h3: 1.5rem;
  /* ... */

  /* Motion */
  --ease-cinematic: cubic-bezier(0.16, 1, 0.3, 1);
  --dur-base: 400ms;
}
```

No `padding: 13px` in component files. Always `padding: var(--space-3)`.

## Verification gates

When `/bq-audit` or `/bq-verify` exercise the frontend:

1. **axe-core** — accessibility violations
2. **Playwright walks** — admin + user flows
3. **Visual regression** (optional) — Percy / Chromatic
4. **Console errors** — page must boot with zero console errors
5. **Network errors** — no 4xx/5xx network requests on page load (other than expected auth probes)
6. **Mode chip honesty** — if a UI claims "live data", the data must be live (Article VI)
7. **Empty / loading / error states** — visit each state by mocking the API; each must render usefully

## Per-feature checklist (drop into /bq-add-feature for UI features)

- [ ] Component sourced from priority order above
- [ ] No hardcoded mock data unless the screen is explicitly "demo"
- [ ] Empty / loading / error states all real
- [ ] axe-core passes on the new screen
- [ ] Touch targets ≥ 44px
- [ ] Contrast ratio ≥ AA (use a contrast checker)
- [ ] Tested at 360px viewport
- [ ] Keyboard-navigable (tab → focus visible → activate)
- [ ] No new font added without recorded reason
- [ ] No new color added without recorded reason

## Anti-patterns to refuse

- **"It looks fine in Figma."** Verify in the browser. With real data.
- **"We'll add empty states later."** They'll never get added. Add them now.
- **"Just use Inter."** Inter is fine but state WHY.
- **"Make it pop with a gradient."** No. Apple, Linear, Vercel, Stripe, Raycast, Arc, Notion — none use gradients heavily. Match those, not the AI defaults.

---

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, design system, or workflow named in this file (Impeccable, shadcn/ui, Tailwind, tweakcn, Aceternity, Magic, context7, Inter, axe-core, Playwright, etc.) is an EXAMPLE, not a mandatory default.**

The 10 design principles + 15 AI-slop patterns are **universal rules**. The named tools that help implement them are candidates to evaluate per project.

**Do not say:** "Use shadcn/ui."
**Say:** "shadcn/ui is one candidate for the component layer. Compare against Radix primitives, Headless UI, Aria-Components, or framework-native components for this specific project's stack and complexity. Use it only if it fits."

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
