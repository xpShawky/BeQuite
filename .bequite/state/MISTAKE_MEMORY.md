# Mistake Memory

Project-specific lessons. When BeQuite or the agent makes a mistake, hits an error, fixes a repeated issue, or learns a project-specific lesson, it stores the entry here. Re-read on every session start so the same mistake isn't repeated.

**Updated by:** `/bq-fix`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`, `/bq-auto`, `/bq-live-edit`

---

## Entry template

```markdown
## <ISO 8601 UTC> — <one-line summary>

**Context:** <where this came up — file, feature, phase, session>
**Mistake:** <what went wrong>
**Root cause:** <one sentence; the actual cause, not the symptom>
**Fix:** <file:line + what changed>
**Prevention rule:** <how to avoid this in future work>
**Related files:** <list>
**Related command:** <which BeQuite command surfaced this>
**How to detect next time:** <pattern to grep for; test to add; check to run>
```

---

## How this file is used

1. **On session start** — agent reads this file (top 10-20 entries) into context. Recent mistakes inform decisions.
2. **During `/bq-fix`** — after the fix lands, append an entry. Future bug attempts check here first.
3. **During `/bq-audit`** — entries inform what areas to scrutinize.
4. **During `/bq-review`** — diffs that touch the "Related files" trigger extra care.
5. **During `/bq-red-team`** — entries become attack-angle inputs.
6. **During `/bq-verify`** — if a "Prevention rule" hasn't been verified, add to verify checklist.
7. **During `/bq-auto`** — surfaces relevant entries before each phase based on the task.
8. **During `/bq-live-edit`** — entries tagged with frontend / responsive / contrast / spacing inform every edit.

---

## Entries (newest at top)

<!--
  Examples of good entries:

  ## 2026-05-12T14:30Z — Hidden text on mobile cards due to gray-on-color
  **Context:** /bq-fix run on the dashboard's PricingCards section at 360px viewport
  **Mistake:** initial fix applied `--color-fg-muted` to the card title; failed contrast on the highlighted card's brand-color background
  **Root cause:** muted gray reuses the same value across light and dark sections; doesn't pass WCAG AA on colored backgrounds
  **Fix:** components/PricingCards.tsx:42 — switched to `--color-fg` on the highlighted card; left muted on the neutral cards
  **Prevention rule:** never apply muted text on a colored card background; use the body text token instead
  **Related files:** components/PricingCards.tsx, components/Cards.tsx, tokens.css
  **Related command:** /bq-fix (15-type: frontend bug — visual/state)
  **How to detect next time:** axe-core check on cards with backgrounds != base bg; manual grayscale check during /bq-live-edit
-->

> **Seeded frontend prevention rules (alpha.17).** The entries below are the design-drift lessons the Design Continuity upgrade was built to prevent. They are universal patterns — keep them, add project-specific instances above them as they occur. Tag: `[fe][design]`.

## seed — [fe][design] Hero polished but middle/body sections go generic
**Context:** the headline failure — frontends look great at the hero, then middle sections become bland card grids
**Mistake:** quality dropped as the page got longer; the original direction was forgotten mid-build
**Root cause:** LLM distributional convergence — without a persisted, re-read Design DNA, the model samples the generic statistical center once the hero scrolls out of live context
**Prevention rule:** persist `DESIGN_DNA.md` before coding; build section-by-section, re-reading `FRONTEND_CONTEXT_SUMMARY.md` each section; run the Design Continuity Gate comparing every section to the strongest one
**Related files:** `.bequite/design/DESIGN_DNA.md`, `.bequite/design/DESIGN_CONTINUITY_REPORT.md`, `.bequite/state/FRONTEND_CONTEXT_SUMMARY.md`
**Related command:** `/bq-feature`, `/bq-auto frontend`, `/bq-audit`
**How to detect next time:** quality-cliff check in the Design Continuity Gate (weakest vs. strongest section); visual QA of each middle section

## seed — [fe][design] Text becomes ALL-CAPS / letter-spacing too wide
**Context:** middle-section typography drift
**Mistake:** section headings rendered in all-caps with 0.15–0.2em tracking for no recorded reason
**Root cause:** "eyebrow kicker on every section" AI grammar; caps used as a decorative reflex
**Prevention rule:** all-caps only on ≤4-word labels/badges at 0.05–0.12em tracking; never caps body; never positive tracking on body; record any caps use in DNA §7
**Related files:** `tokens.css`, section components
**Related command:** `/bq-live-edit`, `/bq-review`
**How to detect next time:** grep `text-transform:\s*uppercase` and `letter-spacing` > 0.12em outside label tokens; continuity checklist typography block

## seed — [fe][design] Text overflows / escapes its container
**Context:** cards and hero headings at narrow widths
**Mistake:** long words + large `clamp()` + narrow grid → text spills out of the card
**Root cause:** no min-width / overflow handling; type scale max too large for the container
**Prevention rule:** cap hero `clamp()` max ≤ ~2.5× min; `text-wrap: balance` on h1–h3; test at 360px; `min-width: 0` on flex children
**Related files:** section components, `tokens.css`
**Related command:** `/bq-fix` (visual), `/bq-live-edit`
**How to detect next time:** responsive check at 360px in Visual QA; continuity checklist "text overflow" item

## seed — [fe][design] Gray text on colored background fails contrast / hides
**Context:** highlighted cards, dark sections
**Mistake:** muted-gray foreground token applied on a brand-colored or dark background → washed out, fails 4.5:1
**Root cause:** one muted-gray reused across all surfaces; gray-on-color never passes AA
**Prevention rule:** never apply muted/gray text on a colored or dark background; use a darker shade of the bg hue or the on-color token; muted FG must still hit 4.5:1
**Related files:** `tokens.css`, card components
**Related command:** `/bq-fix`, `/bq-audit`
**How to detect next time:** axe-core; manual grayscale pass; continuity checklist contrast block

## seed — [fe][design] Button looks active but isn't clickable
**Context:** styled CTAs with no handler
**Mistake:** button rendered with primary styling but no `onClick`/`href`/handler — a dead click
**Root cause:** visual-first generation without wiring the action
**Prevention rule:** every styled button has a real handler or is explicitly disabled with a reason; verb+object label
**Related files:** interactive components
**Related command:** `/bq-red-team` (UX angle), `/bq-verify`
**How to detect next time:** Visual QA "all important buttons clickable"; grep for buttons without handlers

## seed — [fe][design] Mobile layout broken (overflow / tiny targets)
**Context:** desktop-first build
**Mistake:** horizontal scroll on body at 360px; touch targets < 44px; nav doesn't collapse
**Root cause:** designed desktop-first, mobile treated as afterthought
**Prevention rule:** mobile-first (`min-width` queries); touch targets ≥44×44pt; no body h-scroll; thumb-zone primary actions
**Related files:** layout + nav components
**Related command:** `/bq-live-edit`, `/bq-fix`
**How to detect next time:** Visual QA 360px row; `references/mobile-app-ui-checklist.md`

## seed — [fe][design] Cards nested inside cards
**Context:** pricing / feature sections
**Mistake:** a card placed inside another card → excess depth, visual noise
**Root cause:** "cards are lazy" default; nested cards are always wrong
**Prevention rule:** one card depth max; group with space + hairline, not nested elevated surfaces
**Related files:** card components
**Related command:** `/bq-audit`, `/bq-review`
**How to detect next time:** continuity checklist "nested cards"; grep card class within card class

## seed — [fe][design] Motion too noisy
**Context:** scroll-reveal + hover effects everywhere
**Mistake:** whole-section fade-on-scroll, bounce easing, image scale on hover, no reduced-motion fallback
**Root cause:** scattered animations instead of one orchestrated experience; dated easing
**Prevention rule:** exponential ease-out only (no bounce/elastic); animate transform+opacity; never image-on-hover transform; mandatory `prefers-reduced-motion: reduce`; reveal-safety (content visible if animation fails)
**Related files:** motion config, section components
**Related command:** `/bq-live-edit`, `/bq-red-team`
**How to detect next time:** `references/cinematic-ui-checklist.md`; grep bounce/elastic easing + `:hover` transform on `img`

## seed — [fe][design] Typography inconsistent across sections
**Context:** multi-section page
**Mistake:** font sizes too close together (flat hierarchy); section 3 uses a different scale than section 1
**Root cause:** type scale not enforced; hierarchy by size alone
**Prevention rule:** fixed type scale (ratio ≥1.2); hierarchy = size + weight + color + space; sizes clearly spaced (not 14/15/16); same scale every section
**Related files:** `tokens.css`, headings
**Related command:** `/bq-audit`, `/bq-review`
**How to detect next time:** continuity checklist typography; compare heading sizes across sections

## seed — [fe][design] Random gradients / generic "AI-looking" UI
**Context:** hero + section backgrounds
**Mistake:** purple→blue / purple→pink gradient on a non-purple brand; gradient text; the "could-guess-from-category" generic look
**Root cause:** the single most recognizable AI-slop tell; category-reflex color
**Prevention rule:** no decorative AI gradients unless brand is genuinely that hue; write a scene sentence to drive color from context; pass the two-altitude slop test
**Related files:** `tokens.css`, hero/section backgrounds
**Related command:** `/bq-audit`, `/bq-uiux-variants`
**How to detect next time:** `frontend-quality` 15-tell scan; continuity checklist color block; grep `linear-gradient` on text/large surfaces

---

## Categories to organize entries (use tags in the summary)

- `[fe]` — frontend / UI
- `[be]` — backend / API
- `[db]` — database / schema / query
- `[auth]` — authentication / permissions
- `[build]` — build / compile / TS
- `[test]` — testing
- `[deploy]` — deployment / CI / env
- `[perf]` — performance
- `[sec]` — security
- `[dep]` — dependency / package
- `[config]` — configuration / env vars
- `[net]` — network / integration
- `[mem]` — memory leak / resource
- `[race]` — race condition / async
- `[xbrowser]` — cross-browser / platform
- `[design]` — design system / token / AI-slop

Examples:
```
## 2026-05-12T14:30Z — [fe][design] Hidden text on mobile cards (gray-on-color contrast)
## 2026-05-15T10:00Z — [build][dep] PhantomRaven package alert: typo-squatted dep
## 2026-05-20T16:00Z — [be][race] Missing await on email send caused dropped notifications
```

---

## Rules for good entries

- **One mistake per entry.** Don't pile unrelated lessons into one.
- **Prevention rule must be concrete.** "Be careful with X" is not concrete. "Always run axe-core before merging UI changes" is.
- **Cite file:line whenever possible.** "The pricing component is broken" is not useful. "components/PricingCards.tsx:42 — gray-on-color fails AA" is.
- **Pattern over instance.** If the root cause is "missing await on async DB call", record the pattern, not just this one instance.
- **Use tags.** They make grep + filtering work.

---

## Pruning

This file grows. To prevent bloat:
- Every 3 months: review entries; archive resolved/permanent-fixed patterns to `.bequite/state/MISTAKE_MEMORY-archive-<date>.md`
- Keep the live file under 200 entries
- The agent prefers recent + tag-matching entries; archived entries are still readable on demand
