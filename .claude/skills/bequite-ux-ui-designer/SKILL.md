---
name: bequite-ux-ui-designer
description: Use when a screen, section, component or design variant needs design decisions, such as type scale, colours, spacing, radii, hierarchy, states, motion or layout, or when tokens are created or changed. Derives every token from measured references and the Design DNA instead of defaults, writes them once in tokens, and designs real states and phone layouts first.
last_verified: 2026-11-21
sources:
  - https://tailwindcss.com/docs/theme (read 2026-11-21) v4.3 @theme variables, OKLCH default palette
  - https://www.w3.org/TR/WCAG22/ (read 2026-11-21) contrast and target-size floors
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion (read 2026-11-21) reduce motion, widely available
  - https://ui.shadcn.com/docs/mcp (read 2026-11-21) registry and MCP server for components
  - https://github.com/pbakaus/impeccable (read 2026-11-21) design vocabulary and anti-patterns
  - https://linear.app, https://stripe.com, https://www.apple.com/airpods-pro/ (measured 2026-11-21) type, weight, radius, colour values
allowed-tools: Read, Glob, Grep, Edit, Write, WebFetch
---

# bequite-ux-ui-designer

Generated interfaces look alike because they are built from the same defaults: one bold weight, one radius, one gradient, grey on everything. This skill replaces each default with a value taken from a measured reference or the project's DNA, and writes the reason next to the token.

## When to use

- Called by `bequite-frontend-design-system` for each section; by `/bq-feature` for a new screen; by `/bq-uiux-variants` for directions; whenever `tokens.css` or the theme changes.

Not for: checking a finished page (`bequite-frontend-quality`), editing a running app (`bequite-live-edit`), brand strategy or illustration.

## Procedure

1. **Read the DNA and the references.** `.bequite/design/DESIGN_DNA.md` and the measured reference table. No DNA yet: run step 1 of `bequite-frontend-design-system` first. Never design from memory of "what modern sites do".
2. **Type.** Families, weights and tracking come from the references (for example display tracking near -2% at 48-64 px, medium weights 500-600, body 400). Set a size scale with a fluid clamp for display sizes; body text at least 16 px on phones; line length 50-75 characters.
3. **Colour.** One brand colour used only for primary actions, active states and key data; a neutral ramp of 4-7 steps with a job per step; status colours. Write colours in OKLCH or hex, check every text and background pair for 4.5:1 (3:1 for large text and UI parts) before saving.
4. **Space and shape.** A spacing scale (4 or 8 based); radius by component size (controls small, cards one value, pills full), shadows only where elevation means something.
5. **Tokens once** (`references/tokens.md`): every value above becomes a token with a one-line source ("from Linear h1 tracking"). Components use tokens only.
6. **Hierarchy per screen.** One primary action; one h1; secondary actions visibly quieter.
7. **Phone first.** Design the 375 px layout, then widen. Targets at least 24 x 24 CSS px (larger for primary touch actions), no horizontal scroll.
8. **States.** Empty, loading, error, success and the 10x-data case for every view; real-looking content in the product's language (Arabic and RTL when the product needs it, with `bequite-localization-rtl`).
9. **Motion with a job.** Durations and easing from the references or `../bequite-frontend-design-system/references/web-motion.md`; every animation respects `prefers-reduced-motion: reduce`.
10. **Hand to the check.** The section goes to `bequite-frontend-quality` for the sweep in the browser; fixes come back here.

### Variants (`/bq-uiux-variants`)

Each direction starts from a different reference set (not a colour swap), lives in its own route or folder, meets the same checks, and is compared side by side at desktop and phone width in `UIUX_VARIANTS_REPORT.md`. The user picks the winner (hard human gate); the others are archived.

## Worked example (real run, 2026-11-21)

Tokens written for the clinic-booking test page from the measured references, then checked in the browser:

```css
:root {
  --font-sans: Inter, system-ui, sans-serif;     /* Linear runs Inter Variable at 400/510/590 */
  --display: clamp(36px, 7vw, 64px);             /* Linear h1 64 px; 36 px keeps the phone h1 to 4 lines */
  --display-weight: 560;                         /* between Linear 510 and Apple 600 */
  --display-tracking: -0.022em;                  /* Linear -1.408 px at 64 px = -2.2% */
  --body-weight: 400;                            /* Linear and Apple body 400 */
  --radius-card: 12px;                           /* Linear cards 12 px; controls 4-8 px */
  --surface: #14141c; --line: #23232e;           /* solid surface + 1 px line instead of glass */
}
```

Measured result at 375 x 812: h1 36 px, -0.792 px, 4 lines, no horizontal scroll; at 1024 px: 64 px, -1.408 px, 2 lines. The tell sweep went from 5 hits to 1 justified hit.

## Quality gate

- Every token has a source line (a reference measurement or a DNA rule).
- Every text and background pair used meets 4.5:1 (or 3:1 where WCAG allows), measured.
- The phone layout was designed and seen at 375 px before the desktop one was finished.
- All states exist for every view; no lorem ipsum.
- No value outside the tokens in component code (grep for raw hex, px radii and font names).

## Boundaries

- Learn from references; never copy another site's assets, copy or exact palette as the brand.
- Fonts, kits and generators are candidates; licences checked; nothing installed without the user's yes.
- Generated images are a last resort after a real photo, a product screenshot or a drawing in code.

## References (load on demand)

- `references/tokens.md`: token contract template with source lines, colour and contrast steps, component rules.
