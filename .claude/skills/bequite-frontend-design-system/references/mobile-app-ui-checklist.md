# Mobile App UI Checklist

Mobile-first + native-pattern discipline so mobile layouts don't break and don't get treated as a desktop afterthought.

Sibling references: `touch-targets-accessibility.md`, `responsive-layout-rules.md`, `motion-spec.md`, `typography-rules.md`, `wcag-contrast.md`. This file is mobile-specific; defer to those for full WCAG/motion/type math.

---

## Touch targets

| Rule | Value | Source |
|---|---|---|
| iOS primary control | 44x44 pt minimum | Apple HIG 44pt |
| Android primary control | 48x48 dp minimum | Android Material 48dp |
| Accessibility floor (web/PWA) | 24x24 CSS px minimum | WCAG 2.2 SC 2.5.8 (24px floor) |
| Safer size for primary actions | ~54 dp | field practice; exceeds both platform minimums |
| Spacing between adjacent targets | >=8 dp | Material + WCAG 2.5.8 undersized-exception spacing |

- Pick the larger applicable minimum — never go below it to fit more controls.
- Visual size may be smaller than the hit area; pad the tappable region, not the glyph.
- ClinicFlow staff dashboard: "Confirm appointment" and "Cancel" sit at ~54dp with >=8dp gap so a rushed clinician can't fat-finger the wrong action.

## Thumb zones

- ~49% of usage is one-handed — design for the thumb arc, not the cursor.
- Three reach bands: **natural** (easy, lower-center), **stretch** (upper-center, deliberate), **hard** (top corners, two-handed only).
- Put primary actions in the natural/center-reachable band (bottom or bottom-center).
- Keep destructive or rare actions out of the natural band; do not park primary CTAs in top corners.
- ClinicFlow booking flow: "Book now" pins to a bottom sticky bar; "Back" and account menu live top-left/top-right where mis-taps are low-cost.

## Platform conventions

| Platform | Grid baseline | Density | Target | Source |
|---|---|---|---|---|
| iOS | 8 pt grid | Standard | 44 pt | Apple HIG 44pt |
| Android | 4 dp baseline grid | Denser | 48 dp | Android Material 48dp |

- Match the host OS. Do not port idioms across platforms (no Android-style FAB on iOS, no iOS swipe-back gesture assumptions on Android).
- Use platform-native patterns: iOS tab bar / navigation bar / action sheet; Android bottom nav / app bar / bottom sheet.
- Web/PWA on mobile: honor the underlying OS conventions where detectable; default to the WCAG 24px floor as the universal hard minimum.

## Density per platform + content

- Tune density to platform (iOS roomier, Android denser) AND to content (data-dense ClinicFlow staff list vs. airy marketing landing).
- Never drop below the target-size or >=8dp spacing minimums to gain density.
- Increase tap padding, not font size reduction, when space is tight.

## Safe areas

- Respect notches, home indicators, and rounded corners with `env(safe-area-inset-*)`.
- Pattern: `padding: max(1rem, env(safe-area-inset-bottom));` (same for top/left/right insets).
- Set `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` so insets are available.
- Sticky bottom bars (e.g. ClinicFlow "Book now") add bottom inset so the control clears the home indicator.

## Navigation

- Bottom nav: **<=5 items**; more belongs in a "More" entry or menu.
- Provide predictable back behavior matching the platform (Android system back, iOS edge-swipe + nav-bar back).
- Support deep linking so a shared appointment URL opens the correct screen.

## Layout + media rules

- No horizontal scroll on `body` — content must fit the viewport at the smallest target width.
- No hover-only core functionality. Gate hover affordances behind `@media (pointer: coarse)` / `@media (hover: none)` and provide a tap equivalent.
- Responsive images: use `srcset` + `sizes` or `<picture>` so phones download phone-sized assets.
- Tables collapse to stacked cards at small widths (ClinicFlow appointment table -> one card per appointment on phones).

## Light/dark parity

- Contrast holds in BOTH themes: body 4.5:1, large text 3:1, UI/focus 3:1 (WCAG 2.2 AA). See `wcag-contrast.md`.
- Verify the teal brand color and tinted-neutral backgrounds pass in dark mode, not just light.
- Test focus rings and disabled states in both themes — they regress most often.

## Mobile drift tells to catch

- Overflow / horizontal scroll at 360px width.
- Targets below 44pt / 48dp / 24px.
- Nav that doesn't collapse to mobile pattern (desktop menu bar bleeding onto phone).
- Text clipping, truncation, or ellipsis where the full string is required.
- Hover-revealed content with no tap path.
- Sticky bars overlapping the home indicator (missing safe-area inset).

---

## Per-screen checklist

Run for every screen at 360px and at a large phone width:

- [ ] No horizontal scroll on `body` at 360px.
- [ ] Every interactive target >=44pt (iOS) / >=48dp (Android) / >=24px (WCAG 2.2 floor), with >=8dp spacing.
- [ ] Primary action sits in the natural thumb zone (bottom / bottom-center), not a top corner.
- [ ] Safe-area insets applied (`viewport-fit=cover` + `max(..., env(safe-area-inset-*))`).
- [ ] Bottom nav <=5 items; back is predictable; deep links resolve.
- [ ] No hover-only core function (`pointer: coarse` / `hover: none` fallback present).
- [ ] Images responsive (`srcset`/`sizes`/`<picture>`); tables -> cards at small widths.
- [ ] Contrast passes in light AND dark (4.5:1 body / 3:1 large / 3:1 UI+focus).
- [ ] No text clipping or truncation of required content.
- [ ] Platform-native patterns used; no cross-platform idiom ports.

Sources cited inline above: Apple HIG (44pt), Android Material (48dp), WCAG 2.2 SC 2.5.8 (24px floor / >=8dp spacing).
