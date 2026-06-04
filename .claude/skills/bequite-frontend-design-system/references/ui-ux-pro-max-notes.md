# UI UX Pro Max — researched reference notes

**Source:** nextlevelbuilder — https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (MIT). Verified against `.claude/skills/ui-ux-pro-max/SKILL.md`, `core.py`, `design_system.py`, and the `ui-reasoning.csv` / `colors.csv` / `typography.csv` / `styles.csv` data (alpha.17 research pass).

> Reference, not a dependency. BeQuite ports the *product-type-first* idea as a lightweight Markdown table (`product-type-rules.md`), NOT the Python/CSV engine.

## What it is

A data-driven design-intelligence skill: a searchable CSV knowledge base + a Python BM25 reasoning engine. A plain request ("landing page for my beauty spa") → a complete, product-appropriate design system. Core data: `ui-reasoning.csv` (~161 industry reasoning rules — the brain), `styles.csv` (67 styles with `Best For` / `Do Not Use For`), `colors.csv` (161 semantic palettes), `typography.csv` (57 mood-keyed pairings).

## The pipeline (what BeQuite mirrors, minus the engine)

1. **Detect product category FIRST.** 2. Look up the category's reasoning rule. 3. Multi-domain search (style/color/type) biased by the rule's priority keywords. 4. Pick best style (checked against its `Do Not Use For`). 5. Assemble: pattern + style + colors + typography + key effects + **anti-patterns** + checklist. Persists a `MASTER.md` + per-page override files.

`ui-reasoning.csv` columns: `UI_Category, Recommended_Pattern, Style_Priority, Color_Mood, Typography_Mood, Key_Effects, Decision_Rules, Anti_Patterns, Severity` → these became the columns of BeQuite's `product-type-rules.md`.

## The headline insight (highest-value port)

Trust domains — **banking, fintech, healthcare, government, legal, B2B** — explicitly list **"AI purple/pink gradients" as a forbidden anti-pattern**. Trust-first beats trendy. `Decision_Rules` encode conditional branches ("switch to liquid-glass if luxury", "dark-mode if dashboard"); `Severity` ranks how hard each rule is.

## Other ported rules

- **`Best For` / `Do Not Use For` gating on every style** — never propose a style without checking it against the product type (Claymorphism ✗ finance/medical/legal; Brutalism ✗ corporate; Motion-driven/Liquid-glass ✗ data dashboards).
- **Semantic color roles with pre-paired `On *` foregrounds** — shadcn-style (Primary/On-Primary, Secondary, Accent, Background, Foreground, Card, Muted, Border, Destructive, Ring) so contrast pairs ship together. (→ DNA §6)
- **Dedicated dashboard/admin doctrine** — Data-Dense: minimal padding, KPI cards, virtualize large lists, data-export, dark + high-contrast default; charts need legends/tooltips/pattern-textures.
- **Mood-keyed typography pairings with ready CSS/Tailwind** — counters "Inter-by-default" (e.g. Playfair+Inter luxury; Space Grotesk+DM Sans tech; EB Garamond+Lato legal; Figtree+Noto Sans medical; Lora+Raleway wellness).
- **Accessibility:** 4.5:1 normal / 3:1 secondary in BOTH themes; WCAG-AAA for gov/healthcare; 44×44pt targets + 8px gaps; color never the sole signal; reduced-motion; modal scrim 40–60%.
- **Mobile/multi-platform:** mobile-first; breakpoints 375/768/1024/1440; bottom nav ≤5 items; transform-only 150–300ms motion.

## Top principles BeQuite encodes

1. **Detect product type first, then derive design** → kills "everything is a cinematic SaaS landing." (DNA §1 + `product-type-rules.md`)
2. Compact product-category → design-rule table (Markdown, no Python).
3. Per-category anti-pattern guardrails, esp. "no AI purple/pink gradients" for trust domains → into `frontend-quality`'s slop detection.
4. `Best For` / `Do Not Use For` style gating.
5. Semantic color roles with paired on-colors → `tokens.css` correct by construction.
6. Decision-rule branching (if luxury → X; if dashboard → dark).
7. Dedicated dashboard/admin doctrine separate from marketing pages.
8. Mood-based typography pairings keyed to product type.

**UNVERIFIED:** the repo's data does NOT contain an explicit 60-30-10 rule or "tinted neutrals" instruction (those come from Impeccable). Don't attribute them here.
