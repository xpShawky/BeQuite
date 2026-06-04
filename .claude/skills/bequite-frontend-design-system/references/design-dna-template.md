# Design DNA — how to fill it

Purpose: how to author `.bequite/design/DESIGN_DNA.md` before any UI code (gate `DESIGN_DNA_LOCKED`).

This file mirrors the section order of `DESIGN_DNA.md` and gives 1-2 lines per field on HOW to choose a good value. Fill every section, then lock. Siblings: the blank `DESIGN_DNA.md` template, `product-type-rules.md` (per-type rules), `continuity-gate.md` (the gate that judges each section against this file), and `slop-checklist.md` (anti-patterns).

Worked example throughout: **ClinicFlow** — a clinic booking platform with a public marketing landing page and an internal staff dashboard. Brand adjectives: trustworthy, calm, efficient.

---

## How to fill each section

### 1 — Product type
Pick the closest row from the product-type list (SaaS landing, SaaS dashboard, marketing site, docs, e-commerce, content/editorial, data-heavy/admin, medical-adjacent, fintech, dev-tool, mobile-first app). This selects the matching row in `product-type-rules.md`, which constrains density, tone, and depth.
- If the product has two surfaces, declare both and fill the divergent fields (color/density/accessibility) per surface.
- ClinicFlow: `SaaS landing (marketing, public)` + `SaaS dashboard / medical-adjacent (staff, internal)`.

### 2 — Target users
Name the real audience, their device, their context, and their expertise. This decides density, reading distance, and default touch-target size.
- ClinicFlow: marketing → prospective clinic owners on desktop+mobile, skim-reading, low patience; dashboard → front-desk staff on shared desktops, repeat all-day use, want speed over delight.

### 3 — Emotional goal
One sentence: how the user should FEEL in the first 5 seconds. Drives contrast level, motion budget, and whitespace.
- ClinicFlow marketing: "I can trust this clinic with my schedule." Dashboard: "I can move fast without making a mistake."

### 4 — Brand adjectives (3-5)
Pick 3-5 adjectives that are specific and ownable, not "modern/clean/sleek". These are the **tie-breaker for every later decision** — when two choices both pass the rules, the one closer to the adjectives wins.
- Drop any adjective you cannot point to in the final UI.
- ClinicFlow: trustworthy, calm, efficient.

### 5 — Scene sentence
Write one sentence describing who is using it, where they are, the quality of light, and the mood. This drives theme + color FROM CONTEXT (not from a trend), which is the strongest anti-slop move.
- Light/place sets light vs dark theme and neutral temperature; mood sets motion and contrast.
- ClinicFlow: "A calm, well-lit clinic reception at mid-morning; unhurried, clean surfaces, soft daylight." → light theme, cool tinted neutrals, low-energy motion.

### 6 — Color palette
List semantic roles, not raw swatches: background, surface, surface-raised, border, text, text-muted, primary, on-primary, secondary, accent, success, warning, danger, and a paired `on-*` for every fill. Use OKLCH so lightness is perceptual and contrast is predictable.
- Tint neutrals slightly toward the brand hue (don't use pure gray) — this is what makes a palette feel designed.
- Apply 60-30-10 by VISUAL WEIGHT: ~60% neutral surface, ~30% secondary/structure, ~10% brand/accent. The brand color is the 10%, not the wallpaper.
- Verify every text/UI pair against section 16 contrast numbers as you choose.
- Do NOT ship a purple→blue or pink AI gradient unless the brand is genuinely that hue.
- ClinicFlow: primary = calm clinical teal (OKLCH), cool tinted-neutral backgrounds, single accent for CTAs, semantic success/warning/danger; no purple/pink gradient.

### 7 — Typography
Name display and body families and **record a reason for each** — never default to Inter (or any font) without a recorded reason. Set a modular scale ratio ≥1.2, a base body size of 16px, and line-height (1.1-1.2 headings / 1.5-1.7 body).
- Pick a display face with character for headings; pick a clean, legible body face; confirm both have the weights and language coverage you need.
- All-caps only on labels ≤4 words at 0.05-0.12em tracking; never on sentences or buttons.
- Constrain body measure to 45-75ch.
- ClinicFlow: humanist sans (display) for warmth + authority; clean sans (body) for legibility on dashboards — reason recorded per family.

### 8 — Spacing
Commit to a 4/8pt scale and define rhythm by contrast: 8-12px WITHIN a group (label↔field, icon↔text), 48-96px BETWEEN major sections. Consistent rhythm is what separates designed from drifted layouts.
- Pick one inner step and one section step and reuse them; resist arbitrary one-off margins.

### 9 — Radius
Choose ≤3 radius values total (e.g. small for inputs, medium for cards, full for pills). Cards land at 12-16px. Never put ≥32px radius on a card — that reads as a toy, not a product.

### 10 — Shadow
Define one elevation ramp (1-3 levels) and pick: borders OR shadows as the primary separation cue, not both heavily. A visible border PLUS a ≥16px box-shadow is the ghost-card slop pattern — avoid it.
- Keep shadows soft, low-spread, single-direction (light from above).

### 11 — Icon style
Lock ONE icon family and one weight/size. Mixing families or weights looks unfinished.
- No emoji as functional UI icons. Decide stroke vs filled once and keep it.

### 12 — Motion
Set the budget: exponential ease-out (cubic-bezier(0.16,1,0.3,1) family), 100-150ms feedback / 200-300ms state / 300-500ms layout, exit ~75% of entrance. NO bounce/elastic.
- Animate transform + opacity only; never animate `img` on hover; never gate content visibility on the animation (reveal-safety — content shows if JS/animation fails).
- A `prefers-reduced-motion: reduce` fallback is mandatory; declare it here.
- ClinicFlow: subtle fades + small translates only; calm, never playful.

### 13 — Component rules
Declare ONE button system (one primary, one secondary, one ghost — defined sizes/states), ONE card depth, and require real states for every interactive element: default, hover, focus-visible, active, disabled, loading, empty, error.
- No dead buttons, no decorative-only controls; if it looks clickable it must do something.

### 14 — Layout
State the grid (columns, max content width, gutter) and the section pattern. Define how the page breathes from hero → middle → footer so middle sections don't drift to generic cards.
- Name the hero pattern and at least 2 distinct middle-section patterns so the page doesn't become a card stack.

### 15 — Mobile
Design mobile-first: define the smallest breakpoint behavior first, then scale up. Touch targets ≥44pt (Apple HIG 44x44pt / Android 48x48dp; WCAG floor 24x24 CSS px) with ≥8dp spacing between targets.
- Decide what collapses, what stacks, and what hides on small screens here, not later.

### 16 — Accessibility
Target WCAG 2.2 AA: body text 4.5:1, large text (18px+ or 14px-bold) 3:1, UI components + focus indicators 3:1. Use AAA (7:1 / 4.5:1) where regulated or for critical actions.
- Require a visible focus indicator, keyboard reachability, and prefers-reduced-motion support.
- ClinicFlow: AA across the marketing site; lean AAA on the dashboard's critical actions (confirm/cancel appointment, delete record).

### 17 — Anti-patterns to avoid
List the slop patterns this project will be checked against (see `slop-checklist.md`): generic 3-card row, all-caps misuse, wide letter-spacing on body, text overflow/clipping, ghost cards, purple/pink AI gradient, identical middle sections, code-looking output, dead buttons, emoji icons.

### 18 — Allowed patterns
List the patterns this project deliberately uses (e.g. tinted-neutral surfaces, single accent CTA, soft single-direction shadow, humanist display headings). This gives the gate a positive baseline, not just a blocklist.

### 19 — Forbidden patterns
List hard NOs specific to this product. For ClinicFlow: no purple/pink gradients, no playful/bouncy motion, no all-caps sentences, no Inter-by-default, no third icon family, no border+heavy-shadow cards.

---

## How it's used

- **Read before any UI work** — every UI command loads this file first.
- **Lock before the first line of UI code** — locking sets the `DESIGN_DNA_LOCKED` gate; UI work is refused until then.
- **The Design Continuity Gate** (`continuity-gate.md`) judges EVERY section of the built UI against these 19 fields. A section that contradicts the locked DNA is a gate failure, not a style preference.
