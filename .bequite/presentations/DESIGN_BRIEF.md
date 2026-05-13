# Design brief

> Written by `/bq-presentation`. Visual decisions BEFORE any slide is built. Named, deliberate choices — no defaulting to "Inter" without reason.

## Audience-driven design context

- **Audience:**
- **Viewing distance:** `<laptop | projector | cinema | mixed>`
- **Tone:** `<academic | business | cinematic | editorial | minimal | brand-led>`
- **Light vs dark:** `<light | dark | both per slide>`
- **Brand identity:** `<brand-led | neutral>` (cross-ref `PRESENTATION_BRIEF.md::brand`)

## Color palette (3–5 colors)

| Role | Hex | Usage |
|---|---|---|
| Primary | `#______` | (brand-defining; headers, accents) |
| Secondary | `#______` | (support; sub-headings, highlights) |
| Accent | `#______` | (callouts, links) |
| Background | `#______` | (canvas) |
| Text | `#______` | (body, captions) |

**Contrast check:** all text-on-background pairs meet WCAG AA (4.5:1 normal, 3:1 large). For projector / cinematic decks, prefer AAA on large text.

## Typography

- **Heading face:** `<font name — be specific, not "Inter">` — reason: (one sentence)
- **Body face:** `<font name>` — reason
- **Display face (if separate):** `<font name>` — reason
- **Mono face (for code, if any):** `<font name>`

### Size tier

| Element | Projector | Laptop | Cinematic |
|---|---|---|---|
| Title | 60–80pt | 48–64pt | 80–120pt |
| Headline | 36–48pt | 32–40pt | 48–60pt |
| Body | 24–32pt | 20–28pt | 24–32pt |
| Caption | 18–22pt | 16–20pt | 18–22pt |

> **Never:** body text below 18pt. AI-slop tell.

## Layout grid

- **Columns:** `<1 / 2 / 3 / 12-grid>`
- **Margins:** top / bottom / sides (pt or %)
- **Safe area:** account for projector edge crop
- **Vertical rhythm:** baseline grid (pt)
- **Visual rhythm rule:** (one paragraph — e.g. "every 3rd slide is a section-break full-bleed image to reset the eye")

## Layout templates per slide type

- Title (open)
- Section divider
- Content-with-bullets
- Hero image
- Quote
- Chart / data
- Comparison split
- Image grid
- Code (only if dev / technical)
- Close + action

## Icon style

- **Style:** `<outline | filled | duotone | illustrated | none>`
- **Source:** `<bundled set | brand kit | none — text-only>`
- **Stroke weight / shape consistency:** specified

## Imagery direction

- **Photo style:** `<editorial | documentary | studio | abstract | none>`
- **Illustration style:** `<flat | textured | 3D | line | none>`
- **Charts:** `<minimal | brand-coloured | data-dense | sparkline-style>`

## AI-slop reject list (don't ship if any present)

- [ ] No purple → blue gradients on section dividers
- [ ] No stock-icon soup (8 different icon styles)
- [ ] No decorative icons that don't add meaning
- [ ] No cropped people-photo headers from generic stock libraries
- [ ] No quote marks the size of titles (unless deliberate brand choice)
- [ ] No synergy / leverage / ecosystem boilerplate
- [ ] No body text below 18pt
- [ ] No gray-on-color text below WCAG AA
- [ ] No nested cards
- [ ] No "lorem ipsum" left anywhere
- [ ] No generic slide titles ("Introduction", "Overview", "Conclusion") — be specific

## Brand asset extraction (when `brand=` provided)

- **Palette extracted:**
- **Typography mood:** `<geometric sans | humanist serif | condensed display | mono | ...>`
- **Layout mood:** `<dense | airy | editorial | minimal>`
- **Icon style:**
- **Verified against actual assets:** yes/no (no hallucinated logos)

---

*Once this brief is signed off, `SLIDE_PLAN.md` populates per these decisions. Motion lives in `MOTION_PLAN.md`.*
