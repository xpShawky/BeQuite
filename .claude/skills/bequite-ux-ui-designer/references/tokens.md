# Token contract (2026-11-21)

One file owns every visual value (`tokens.css`, or the theme block of the project's CSS framework; Tailwind v4 uses `@theme` variables, which also generate utilities, and ships its default palette in OKLCH). Each token carries a source line.

## Template

```css
:root {
  /* Type: families and weights from the references (name each) */
  --font-sans: <family>, system-ui, sans-serif;      /* source: <reference + measured value> */
  --font-mono: <family>, ui-monospace, monospace;
  --weight-body: 400;                                /* source: */
  --weight-strong: <500-600>;                        /* source: */
  --text-xs: 12px; --text-sm: 14px; --text-base: 16px; --text-lg: 18px;
  --text-xl: 24px; --text-2xl: 32px;
  --display: clamp(<phone px>, <vw>, <desktop px>);  /* source: */
  --display-tracking: <-0.01em to -0.03em>;          /* source: */
  --leading-body: 1.5; --leading-display: 1.05;

  /* Colour: brand + neutral ramp + status */
  --brand: <oklch() or hex>;                         /* used for: primary action, active nav, key data */
  --n-0: ; --n-1: ; --n-2: ; --n-3: ; --n-4: ; --n-5: ; --n-6: ;   /* bg -> fg, one job per step */
  --success: ; --warning: ; --danger: ;

  /* Space and shape */
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-6: 24px; --space-8: 32px; --space-12: 48px; --space-16: 64px;
  --radius-control: <4-8px>; --radius-card: <one value>; --radius-pill: 9999px;   /* source: */

  /* Motion */
  --ease-out: <curve from references>; --dur-fast: <ms>; --dur-base: <ms>;
}
@media (prefers-reduced-motion: reduce) {
  :root { --dur-fast: 0ms; --dur-base: 0ms; }
}
```

## Colour steps

1. Pick the brand colour from the brand or the DNA; never a default purple.
2. Build the neutral ramp in one hue family (warm or cool), 4 to 7 steps; name each step's job (page, surface, line, muted text, body text, heading).
3. Check every text/background pair actually used: 4.5:1 for body text, 3:1 for large text (24 px, or 18.66 px bold) and for UI parts and focus rings. Record the ratio next to the pair.
4. Dark mode is its own ramp, not an inversion; check it again.

## Component rules

- Buttons: one primary per screen; the primary is the only filled brand surface in its area.
- Cards: one depth (no card in a card); separation by space or a 1 px line before shadows.
- Icons: one set, one stroke width; an icon never replaces a label for a primary action.
- Forms: visible labels, error text under the field, focus ring from a token.
- Lists and tables: empty, loading, error states designed with the list.

## Raw-value grep (run before calling a section done)

```bash
grep -rnE "#[0-9a-fA-F]{3,8}\b|border-radius:\s*[0-9]+px|font-family:" src/components | grep -v tokens
```

Each hit is moved to a token or justified in a comment.
