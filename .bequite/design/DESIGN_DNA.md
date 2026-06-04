# Design DNA

**The single source of truth for this project's visual identity.**

> **Read this before any frontend work.** If it's empty/placeholder, fill it BEFORE writing UI code (gate `DESIGN_DNA_LOCKED`). If frontend work changes the visual identity, update it here first. Every section of every page must match this DNA — that is what the Design Continuity Gate checks.

**Project:** `<name>`
**Last updated:** `<ISO 8601 UTC | "template — not yet filled">`
**Status:** `template`  ← set to `locked` once filled + approved
**Owner skill:** `bequite-frontend-design-system`

---

## 1. Product type

`<one of: SaaS landing · SaaS dashboard · admin panel · mobile app · restaurant/food-ordering · marketplace · medical · financial · developer tool · AI product · content platform · internal business tool · automation dashboard · e-commerce · booking app · other>`

> The product type selects the matching row of `references/product-type-rules.md` (in the master skill). It determines the *correct* defaults for density, color mood, trust level, motion, and accessibility level. Do NOT default every project to "cinematic SaaS landing."

## 2. Target users

`<one sentence: who they are, their context, their device, their expertise>`

## 3. Emotional goal

`<what the user should FEEL: e.g. "trust + calm" / "energy + momentum" / "premium + restraint" / "playful + fast">`

## 4. Brand adjectives (3–5)

`<e.g. trustworthy, precise, warm, modern>` — these adjectives are the tie-breaker for every style decision.

## 5. Scene sentence (anti-slop anchor)

`<who is using this, where, in what light, in what mood>` — e.g. "A clinic receptionist, at a bright front desk, mid-morning, needing to book a patient fast without errors."

> The scene sentence drives theme (light/dark) and color from *context*, not category reflex. **Slop test:** if you could guess the whole design from the product category alone, rework this.

## 6. Color palette (semantic roles — ship contrast pairs together)

| Role | Value | On-color (text on it) | Notes |
|---|---|---|---|
| Primary / brand | `<oklch/hex>` | `<on-primary>` | the one brand color; appears on CTA, active nav, links |
| Background | `<bg>` | `<foreground>` | tinted neutral, not pure white/black |
| Surface / card | `<surface>` | `<on-surface>` | 1 elevation level; avoid card-in-card |
| Muted | `<muted>` | `<muted-fg ≥4.5:1>` | muted FG must still hit 4.5:1; never gray-on-color |
| Border | `<border>` | — | hairline; group with space, not heavy borders |
| Accent (optional) | `<accent>` | `<on-accent>` | ≤10% visual weight |
| Success / Warning / Danger | `<g>` / `<a>` / `<r>` | paired | consistent across all screens |

**Rules:** OKLCH preferred (perceptually uniform). Tinted neutrals (0.005–0.015 chroma toward brand hue), not cold gray or cream-default. 60-30-10 by visual weight. **No purple→blue / purple→pink AI gradients** unless the brand is genuinely purple. Dark mode = vary lightness, not invert.

## 7. Typography rules

- **Display font:** `<font + why>` · **Body font:** `<font + why>` · **Mono (if needed):** `<font>`
- **Never default to Inter/Roboto/Open Sans without a recorded reason.** Record the WHY here and in `tokens.css`.
- **Type scale:** ratio `<1.2 / 1.25 / 1.333>`; body **16px min**; sizes clearly spaced (no 14/15/16 mush).
- **Line-height:** headings 1.1–1.2, body 1.5–1.7. **Measure:** 45–75ch.
- **Hierarchy = size + weight + color + space** (never size alone). Weights: 3–4 roles max.
- **All-caps:** only ≤4-word labels/badges, tracking 0.05–0.12em. **No caps body. No wide tracking on body.**
- `text-wrap: balance` on h1–h3; `pretty` on long prose.

## 8. Spacing rules

- **Scale:** 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 (4pt base). Never `padding: 13px`. Always tokens.
- **Rhythm by contrast:** 8–12px within a group; 48–96px between sections. **Never uniform gaps everywhere.**
- Use `gap` for sibling spacing. Squint test: blurred, the hierarchy + groupings still read.

## 9. Border-radius rules

- **Scale:** `<e.g. sm 4 / md 8 / lg 12>`. Pick ≤3 values; reuse them. Cards cap at 12–16px. Full-pill only for tags/buttons. **No `radius ≥ 32px` on cards** (ovoid blob tell).

## 10. Shadow / elevation rules

- One consistent shadow scale for depth. **Never `border: 1px` + `box-shadow ≥16px` together** (ghost-card tell). Prefer space/surface-lightness over heavy shadow stacks. Dark mode: lightness for depth, not glow.

## 11. Icon style

- One icon family `<e.g. Lucide / Phosphor / custom>`, one weight/size rhythm. **No emoji as structural icons.** Icons supplement labels, never replace them. Same icon ≠ three different meanings on one screen.

## 12. Motion rules

- **Timing:** 100–150ms feedback · 200–300ms state change · 300–500ms layout · exit ≈ 75% of entrance.
- **Easing:** exponential ease-out (`cubic-bezier(0.16,1,0.3,1)` family). **No bounce/elastic.**
- Animate **transform + opacity** only. **No image-on-hover transform.** Dropdowns escape overflow.
- **Reveal safety:** content visible if JS/animation fails — never gate visibility on a transition.
- **`prefers-reduced-motion: reduce`** alternative is mandatory for every animation.

## 13. Component rules

- One button system reused everywhere (same primary across all screens). One card depth (no nesting).
- Inputs: visible label + focus ring + real error state. Tables: legible density per product type.
- Real states required: empty (acknowledge → value → one CTA), loading (skeleton), error (what/why/how-to-fix).
- Buttons = verb + object ("Save changes", not "OK/Submit"). Destructive names the action + count.

## 14. Layout rules

- 1D (rows/navbars/groups) → flexbox; 2D (page/dashboard) → grid. Don't default to grid.
- Responsive grid: `repeat(auto-fit, minmax(<min>, 1fr))`. Container queries for component-level.
- One primary action per screen; secondary de-emphasized; tertiary in menus.

## 15. Mobile rules

- **Mobile-first** (`min-width` queries). Touch targets ≥44×44pt (iOS) / 48×48dp (Android); ≥8px apart.
- Thumb zones: primary actions reachable (bottom/center), not top corners. Safe-area insets.
- No horizontal scroll on body. No hover-only core functionality (`pointer: coarse`).

## 16. Accessibility rules

- WCAG **2.2 AA** baseline: body 4.5:1, large text/UI 3:1, focus indicators 3:1 + visible.
- Regulated types (medical / gov / finance per product-type rules) → **AAA** where required.
- Keyboard-navigable; semantic HTML; color is never the sole signal; respect reduced motion.

## 17. Anti-patterns to AVOID (this project)

- `<list the slop tells that are especially tempting here — e.g. purple-blue gradient, nested cards, all-caps section eyebrows, identical card grids, gray-on-color text, Inter-by-default>`

## 18. Examples of ALLOWED UI patterns

- `<concrete patterns that fit this DNA — e.g. "single accent CTA on tinted-neutral surface; hairline-separated rows; serif display + humanist-sans body">`

## 19. Examples of FORBIDDEN UI patterns

- `<concrete patterns that violate this DNA — e.g. "rainbow gradient hero; card-in-card pricing; ALL-CAPS feature titles with 0.2em tracking; emoji bullets">`

---

## How this file is used

1. **Before any UI work** — read this (or, for cheap reads, `FRONTEND_CONTEXT_SUMMARY.md` which digests it).
2. **Before first UI code** — if `Status: template`, fill it and set `Status: locked` (gate `DESIGN_DNA_LOCKED`).
3. **Design Continuity Gate** — every section is judged against §1–§19 of this file.
4. **On identity change** — update here FIRST, then propagate to `tokens.css` and components.

See `docs/architecture/DESIGN_CONTINUITY_GATE.md`, `docs/architecture/FRONTEND_CONTEXT_ENGINEERING.md`, and `.claude/skills/bequite-frontend-design-system/references/design-dna-template.md`.
