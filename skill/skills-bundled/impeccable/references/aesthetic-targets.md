# Aesthetic targets — what good looks like

> Reference points for the frontend-designer when applying Impeccable. Studying these isn't copying; it's understanding the principles applied well.

## The reference set (May 2026)

### Linear (https://linear.app)
- Tight 8-spacing scale; nothing wider than 1280 max-width.
- Inter, with weight contrast carrying hierarchy (not size alone).
- Single accent color (system-purple); used sparingly.
- Empty states tell you the rule, not just "nothing here."
- Keyboard shortcuts everywhere; visible on hover.
- Lesson: density + restraint + one job done very well per screen.

### Vercel (https://vercel.com)
- Inter again, but with serif (Söhne / Geist) for emphasis on marketing pages.
- Generous spacing on marketing; tight spacing in dashboard. *Same tokens, different scale*.
- Black/white/gray with one accent (electric blue / purple per product).
- Monospace (Geist Mono) used semantically — code, IDs, technical chips.
- Lesson: type-pairing earns its keep when used consistently across density modes.

### Stripe (https://stripe.com)
- Grids over cards. The dashboard is a tabular workspace.
- Inter + custom display face for marketing.
- Color used to encode meaning (green for revenue, red for failures, gray for archived).
- Hover states reveal context without taking up screen space.
- Lesson: when data is the product, get out of the data's way.

### Raycast (https://raycast.com)
- Dark-first; light is the alternate.
- Exquisite focus states — tab order is a visible feature.
- 4px / 6px borders pretending to be 1px through bg contrast.
- Lesson: keyboard-first interfaces force you to design *every* state, not just the lucky path.

### Arc Browser (https://arc.net) — historical reference (sunset 2024)
- Spaces > tabs as a primary metaphor. Reframed an old UX.
- Bold color use, but each space is monochromatic — palette restraint within an exuberant overall design.
- Lesson: bold isn't loud; it's confidence in restraint.

### Notion (https://notion.so)
- Inter, modest scale (1–4 levels max).
- Empty states *teach* (the page that explains how to use the page).
- Slash-command surface — the entire UI is keyboard-summonable.
- Lesson: progressive disclosure done right looks like simplicity, not hiddenness.

### Cron / Notion Calendar (https://cron.com)
- Pixel-perfect typography in a calendar context.
- Color-coding by calendar source, not by event type.
- Lesson: when every screen is roughly the same shape (a calendar grid), tiny details carry the experience.

## What they share

- **One font family per product** (rarely more than two — and the second is for code or display).
- **Tight color palette** — neutrals + one brand + system-state colors (success/warn/error). Not seven gradients.
- **Spacing scale ≤ 12 values** across the entire app, not per-component improvisation.
- **Visible focus states.** Always.
- **Empty / loading / error states designed first**, not retrofitted.
- **Density variants** for novice vs. expert (dashboard vs. marketing).

## What to do when in doubt

When the frontend-designer can't decide: pick the choice that makes the design *more like one of these references* and *less like a generic AI default*. Document *which reference* informed the choice in the design notes (so a successor can preserve the lineage).

## What NOT to do

- Don't pixel-copy. These references' visual identity is theirs; we're learning the *principles*.
- Don't mix references on a single screen (Linear's density + Vercel's headline scale + Stripe's color encoding = chaos).
- Don't aim for "all of the above." Pick one as the dominant influence; the rest are secondary references.

## Cross-reference

- Principles: `principles.md`
- Anti-patterns: `anti-patterns.md`
- Slash commands: `skill/commands/design-audit.md` + `skill/commands/impeccable-craft.md`
