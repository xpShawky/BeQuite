# Impeccable design principles (BeQuite-vendored)

> The design-language philosophy distilled from upstream Impeccable, layered with BeQuite's Iron Laws. Every command in `commands/` operates within these principles.

## 1. Hierarchy is non-negotiable

Every screen has exactly one primary action. Every section has exactly one heading. Every list has exactly one starting point. If an interface has "two equally important things" it has actually has zero — the user picks neither and bounces.

**Mechanic:** weight (font-size + font-weight + color contrast) is reserved for the primary. Secondary elements are *visibly secondary* (lower contrast, smaller, less saturated).

## 2. Typography is a recorded choice, not a default

Inter is fine. Geist is fine. SF Pro is fine. **What's not fine is "the AI chose Inter."** The font stack must come from a sentence the team can defend: *"We picked Inter because we want Linear/Vercel-style cleanliness in a developer-tooling context"* — that's defensible. *"It looks neutral"* — that's not.

**Mechanic:** `tokens.css` carries a one-line comment above the `--font-sans` declaration explaining the choice. The `bequite audit` rule pack flags missing comments.

## 3. Color is a system, not a palette

Three-color systems beat seven-color systems. A primary, a neutral scale, an accent. Anything more is decoration. If the brand needs more, they belong in *brand assets*, not interface chrome.

**Mechanic:** `tokens.css` ships with a deliberately minimal token set; expansion requires Doctrine override or ADR.

## 4. Spacing comes from a scale

4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128. That's it. Anything else is a code smell or a deliberate exception (e.g. negative-space hero with 200px). Random spacings (13px, 27px, 41px) mean the developer eyeballed it.

**Mechanic:** Tailwind's `spacing` extension exposes only the scale; arbitrary values like `mt-[27px]` are flagged by `bequite audit`.

## 5. Motion is restraint

Linear ease, ease-out, custom cubic-bezier. *Never* bounce, elastic, back. Motion serves causality (this came from there) — it doesn't entertain. Anything bouncy looks like a 2014 toolkit demo.

**Mechanic:** Doctrine `default-web-saas` Rule 6 blocks bounce/elastic/back at audit time.

## 6. Empty / loading / error states are real, not placeholder

"Nothing to show" is not an empty state — it's a sign that the designer didn't think about empty. A real empty state has: a one-line explanation of *why* it's empty, a clear next-action CTA, and an illustration *only* if the brand has illustration assets. Loading uses skeletons matched to the future content's shape (not generic spinners). Errors carry the actual error + a recovery action + a way to see logs / retry.

**Mechanic:** `harden` command enforces this; `design-audit` flags bare placeholders.

## 7. Mobile-first, RTL-aware, keyboard-accessible

Every component renders correctly at viewport 360 (one-handed-thumb zone) and viewport 1440 (laptop). Touch targets ≥ 44 × 44 px (Apple HIG, Google Material). When `mena-bilingual` is active: layout flips, font swaps to Arabic-friendly stack, mirrored icons. Every interactive element is keyboard-reachable in tab-order; focus states are visible.

**Mechanic:** Playwright walks at viewport 360 + 1440 + (when active) `ar-*` locale.

## 8. Information density matches user proficiency

Marketing pages want air. Admin dashboards want density. The *same* design system serves both — the tokens are the same; the spacing scale is applied differently. A novice user wants 32-spacing; an expert running their tenth daily report wants 8-spacing.

**Mechanic:** `adapt` command surfaces density variants. Don't try to make a marketing page out of admin spacing or vice versa.

## 9. Consistency beats cleverness

The third icon-and-tile in a row should match the first two. The fourth heading should be sized like the third. "Variation for variation's sake" is amateur-hour. Variation should signal a meaningful difference (this section is more important / less important / different in kind).

**Mechanic:** `extract` command pulls one-off patterns into a reusable token / variant / component.

## 10. Skeptic kill-shot per change

Before committing a design change, the frontend-designer must answer: *"What would a skeptic look at this and say is wrong?"* If there's a real answer, fix it before commit. If there isn't, ship.

**Mechanic:** Constitution Article II + Skeptic gate at every phase boundary.

## Cross-reference

- Anti-pattern catalog: `anti-patterns.md`
- Aesthetic targets to study: `aesthetic-targets.md`
- Doctrine that operationalizes these: `skill/doctrines/default-web-saas.md`
- Slash commands that dispatch them: `skill/commands/design-audit.md`, `skill/commands/impeccable-craft.md`
