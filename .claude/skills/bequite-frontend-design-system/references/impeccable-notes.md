# Impeccable — researched reference notes

**Source:** Paul Bakaus — https://github.com/pbakaus/impeccable (Apache-2.0). Tagline: *"The vocabulary you didn't know you needed. 1 skill, 23 commands, and curated anti-patterns for impeccable frontend design."* Verified against README, `skill/SKILL.src.md`, and the `skill/reference/*.md` command files (alpha.17 research pass).

> Reference, not a dependency. BeQuite studies Impeccable and ports principles — it does not install or copy it.

## What it is

A design skill pack for AI coding assistants that reduces AI-generated "tells." Structure: one skill compiled from `SKILL.src.md`, per-command reference files read before executing a command, a deterministic detector script (`detect.mjs`, exit 0 clean / 2 findings), and a palette generator. Project context persists to `PRODUCT.md` / `DESIGN.md`; critique snapshots to `.impeccable/critique/`. Key idea: a **register split** — `brand.md` (design *is* the product) vs `product.md` (design *serves* the product); rules differ (fluid type for brand, fixed scales for product).

## The vocabulary (23 verbs — what BeQuite borrows conceptually)

`craft · shape · init · document · extract · critique · audit · polish · bolder · quieter · distill · harden · onboard · animate · colorize · typeset · layout · delight · overdrive · clarify · adapt · optimize · live`.

The lifecycle analog to "audit → critique → polish → harden → live": `init → shape (plan before code) → craft (build) → refine (typeset/colorize/layout/animate/adapt/clarify) → critique (heuristics + detector) → audit (a11y/perf/responsive) → harden (errors/i18n/edge) → polish → live (variants)`.

Distinctive named concepts BeQuite adopts:
- **Scene sentence** — who/where/light/mood → drives theme + color from context, not category reflex. (→ DNA §5)
- **Color strategy commitment** — Restrained / Committed / Full palette / Drenched.
- **AI Slop Test (two altitudes)** — (1) guessable from category alone? (2) guessable aesthetic family from category + anti-refs? Both must be "no."
- **`critique` loop** — two independent assessments, human-style FIRST then deterministic detector (so the detector doesn't anchor judgment); P0–P3 severity; persisted snapshots.

## Anti-patterns (match-and-refuse) — ported into the continuity checklist

Side-stripe borders (`border-left/right >1px` colored) · gradient text (`background-clip:text`) · glassmorphism-by-default · hero-metric template · identical card grids · **eyebrow kicker on every section** · numbered `01/02/03` markers by default · text overflow (long word + big clamp + narrow grid) · ghost-card (`border:1px` + `box-shadow ≥16px`) · over-rounded corners (`radius ≥32px` on cards) · sketchy SVG / `feTurbulence` · repeating-linear-gradient stripes · "X theater" copy.

## Domain rules ported

- **Type:** 5-size system, scale ratio ≥1.25, body ≥16px, measure 45–75ch, line-height 1.1–1.2 headings / 1.5–1.7 body, ≤3 families, hierarchy = size+weight+color+space, all-caps only ≤4-word labels at 0.05–0.12em, `text-wrap: balance` on h1–h3.
- **Color:** OKLCH; contrast floors (body 4.5:1, large/UI 3:1, placeholder also 4.5:1); palette roles (primary/neutral 9–11/semantic/surface); 60-30-10 by visual weight; tinted neutrals toward brand hue; no cream-default; gray-on-color banned; dark-mode = vary lightness not invert.
- **Space:** 4pt scale; rhythm by contrast (8–12 within, 48–96 between, never uniform); 3:1 hierarchy ratio; flex for 1D / grid for 2D; cards are lazy, nested cards always wrong; semantic z-index scale.
- **Motion:** 100/300/500 timing, exit ≈75% of entrance; exponential ease-out, no bounce/elastic; animate transform+opacity only; stagger ≤500ms total; reveal-safety; mandatory reduced-motion; never animate `img` on hover.
- **Responsive:** mobile-first; content-driven breakpoints (640/768/1024); `clamp()`; pointer/hover queries; touch ≥44px; safe-area insets.
- **UX writing:** buttons = verb+object; error = what/why/how + example; empty = acknowledge→value→action; no em-dashes; no buzzwords (streamline/empower/seamless/world-class); term consistency.

## Top principles BeQuite encodes (drift-fighting)

1. Deterministic match-and-refuse anti-patterns as grep rules → run a detector pass **after each section**. (`design-continuity-checklist.md`)
2. "No identical card grid / no nested cards" as a hard gate.
3. Rhythm-by-contrast spacing + squint test as acceptance criteria.
4. Tinted-neutral + OKLCH + contrast floors (placeholder 4.5:1).
5. AI Slop Test + scene sentence before color. (DNA §5)
6. Section-by-section critique with persisted snapshots + P0–P3 severity → the Design Continuity Report.
7. Reveal-safety + reduced-motion + no-image-hover.
8. Banned-word + "every word earns its place" copy gate.
