# Impeccable command catalog (23 commands)

> The 23 design commands the bundled Impeccable skill exposes. Loaded by the **frontend-designer** persona. Dispatched via `bequite design <command>` (CLI) or `/bequite.impeccable-craft <command>` (slash). See `commands/<name>.md` for detailed dispatch contracts on the marquee commands (`craft`, `audit`, `harden`, `polish`); the rest follow the same pattern.

## How dispatch works

```
bequite design <command> [target-files-or-current-feature]
   → frontend-designer loads
   → before-screenshot saved (viewport 360 + 1440, plus ar-* if mena-bilingual loaded)
   → command applied per its contract below
   → after-screenshot saved
   → bequite design audit (lightweight) confirms anti-pattern reduction (or nothing-broken)
   → posttooluse-audit.sh runs axe-core + tokens-only check
   → on green: suggested commit (style: type prefix)
   → on red: BLOCKED with findings + recommended remediation
```

## The 23

| # | Command | One-liner | Primary effect | Detailed file |
|---|---|---|---|---|
| 1 | `craft` | Apply Impeccable's design language to a section. | Section-scoped pass: hierarchy, spacing, typography, color in one go. | `craft.md` |
| 2 | `teach` | Explain why the current state is or isn't good. | Generates design-rationale Markdown for the target. No edits. | (this file) |
| 3 | `document` | Produce design notes for a component. | Generates `<Component>.design.md` capturing decisions + rationales. | (this file) |
| 4 | `extract` | Pull a one-off pattern into a reusable token / variant. | Refactors duplicated patterns into `tokens.css` or a shared component. | (this file) |
| 5 | `shape` | Adjust shape language (border radius, corner profiles). | Normalises `border-radius` to a chosen scale; documents the choice. | (this file) |
| 6 | `critique` | Point out issues without fixing. | Writes a critique to `docs/critique-<YYYY-MM-DD>.md`. | (this file) |
| 7 | `audit` | Comprehensive scan. | Walks the 15 anti-patterns; emits findings report. | `audit.md` |
| 8 | `polish` | Small refinements (contrast, spacing, alignment). | Surface-level fix-ups, minimal-risk. | `polish.md` |
| 9 | `bolder` | Increase visual weight. | Bumps font-weight, contrast, size selectively. | (this file) |
| 10 | `quieter` | Reduce visual weight. | The inverse of `bolder` — recede less-important elements. | (this file) |
| 11 | `distill` | Simplify a noisy component. | Removes decoration; keeps function. | (this file) |
| 12 | `harden` | Add edge-case states (loading / error / empty / disabled). | Materializes the four canonical states. | `harden.md` |
| 13 | `onboard` | First-time-user / onboarding flow refinement. | Authors empty-state-as-onboarding patterns. | (this file) |
| 14 | `animate` | Motion design (eased, never bounce/elastic). | Adds restrained motion to specific transitions. | (this file) |
| 15 | `colorize` | Colour palette pass. | Re-balances color usage; never expands beyond Doctrine token set. | (this file) |
| 16 | `typeset` | Typography pass. | Pairs / stacks / weights per `principles.md`. | (this file) |
| 17 | `layout` | Grid / flex / responsive pass. | Reflows; doesn't restyle. | (this file) |
| 18 | `delight` | Small interactive flourishes. | Hover / micro-interaction additions; restraint required. | (this file) |
| 19 | `overdrive` | Push a component to its emphasised extreme. | The "hero CTA" treatment, applied to a single element. | (this file) |
| 20 | `clarify` | Wording / labels / microcopy. | Verb-noun CTAs; explicit error copy; named pages. | (this file) |
| 21 | `adapt` | Responsive variants (mobile / tablet / desktop). | Per-breakpoint adjustments; honours touch-target floor. | (this file) |
| 22 | `optimize` | Performance (bundle size, render). | Removes unused CSS; lazy-loads; defers. | (this file) |
| 23 | `live` | Interactive preview / playground for a component. | Generates a Storybook-shaped preview file. | (this file) |

## Common contract (all 23)

Every command:

1. **Refuses without a frontend Doctrine loaded** (no UI to operate on).
2. **Refuses without `tokens.css` present** (no design tokens to reference).
3. **Refuses without before/after screenshot capability** (no proof of effect).
4. **Logs evidence** to `evidence/<phase>/<task>/screenshots/` and `evidence/<phase>/<task>/summary.md`.
5. **Updates `state/recovery.md`** if it touches a tracked feature.
6. **Honors the Iron Laws** — even Impeccable can't bypass Article IV (security) or Article VI (honest reporting).

## Conventions for the BeQuite-flavored stubs

The marquee commands each have their own file in this directory with a more detailed dispatch contract. The other 19 follow the same shape; for those, the row above + `principles.md` + `anti-patterns.md` + the persona at `skill/agents/frontend-designer.md` are sufficient.

If a command's behavior is ambiguous in a specific project context, the frontend-designer escalates to the **Skeptic** for an adversarial reading before applying.

## Do not

- Apply more than one command per invocation. The diff must be attributable to a single command.
- Auto-commit. UI changes are visible; the user must confirm.
- Bypass the screenshot capture. "I forgot" is not honest reporting (Article VI).
- Run on a feature without an acceptance trail. Impeccable improves; it doesn't *replace* spec compliance.
