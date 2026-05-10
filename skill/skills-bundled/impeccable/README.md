# skill/skills-bundled/impeccable/

> Bundled expert sub-skill for BeQuite. Loaded automatically when a frontend Doctrine is active (e.g. `default-web-saas`). Provides the **frontend-designer** persona with Impeccable's design-language toolkit.
>
> Vendored from upstream (https://github.com/pbakaus/impeccable), MIT-licensed, attributed to Paul Bakaus. Pinned commit recorded at `.pinned-commit`. Update via PR with diff review per the protocol there.

## What this skill provides

- **23 design commands** in `commands/` (one Markdown stub per Impeccable command). The `frontend-designer` persona dispatches via `bequite design <command>` (or `/bequite.impeccable-craft <command>`).
- **Design principles** in `references/principles.md` — the philosophy + decisioning rubric that powers the commands.
- **Anti-pattern catalog** in `references/anti-patterns.md` — 15 AI-slop tells the `design-audit` command walks against, cross-referenced from `default-web-saas` Doctrine Rules 1+4+5+6+7.
- **The "look" worth aspiring to** in `references/aesthetic-targets.md` — Linear, Vercel, Stripe, Raycast, Arc — what they share and how to inherit it tastefully.

## When this skill loads

Loaded when `state/project.yaml::active_doctrines` contains any of:
- `default-web-saas` (and forks)
- `mena-bilingual` (when stacked with a frontend doctrine; adds RTL + Arabic-friendly typography to the Impeccable command output)
- explicit `--load-skill impeccable` flag on the BeQuite CLI

Not loaded for: `cli-tool`, `library-package`, `ml-pipeline`, `gov-fedramp` (without a UI subprofile), or pure backend Doctrines.

## How the frontend-designer uses it

The `frontend-designer` persona at `skill/agents/frontend-designer.md` references this bundled skill when:

- Designing a new UI section (P5 — invokes `craft`, `shape`, `colorize`, `typeset`, `layout`).
- Auditing an existing page (P5/P6 — `audit`, `critique`).
- Iterating on contrast / spacing / weight (`polish`, `bolder`, `quieter`).
- Adding empty / loading / error states (`harden`).
- Onboarding flow (`onboard`).
- Performance pass (`optimize`).
- Live preview / playground (`live`).

The `design-audit` slash command at `skill/commands/design-audit.md` walks all 23 commands' criteria as a finding catalog.

The `impeccable-craft` slash command at `skill/commands/impeccable-craft.md` invokes a specific Impeccable command on a target file with before/after screenshots saved to `evidence/<phase>/<task>/screenshots/`.

## Layering with other skills

- **mena-bilingual** — when both load, Impeccable's `typeset` command picks Arabic-friendly fonts (Tajawal, Cairo, Readex Pro) and `layout` flips for RTL.
- **ai-automation** — when the project has an automation-admin UI, Impeccable governs the UI layer; ai-automation governs the flow layer. Each owns its own evidence trail.
- **mcp-shadcn / mcp-magic / mcp-context7** — Impeccable orchestrates *what* to build; these MCPs supply *the components* (shadcn) / *the variants* (Magic) / *the docs* (context7).

## What this skill does NOT do

- Does not replace Tailwind / shadcn / vanilla CSS — it operates *on* them.
- Does not generate code blindly — it requires the BeQuite-flavored evidence trail (before/after screenshots, design-audit pre-and-post deltas).
- Does not bypass the Doctrine's Rule 1 (tokens-only). Even Impeccable's outputs go through `tokens.css`.
- Does not inject upstream Impeccable prompts verbatim — the bundled commands are BeQuite-flavored documentation that shows *what* each command does so the frontend-designer can dispatch via Skill mechanics. Upstream IP stays upstream.

## Versioning

This bundled skill versions independently. Update via PR + `.pinned-commit` bump + ADR (for breaking changes only).

- **Bundle version:** 1.0.0 (matches BeQuite v0.6.1)
- **Upstream pin:** see `.pinned-commit`

## License

- The bundled stubs in `commands/`, `references/`, and this `README.md` are MIT-licensed by BeQuite (Ahmed Shawky / xpShawky).
- The upstream Impeccable project is MIT-licensed by Paul Bakaus.
- Attribution: see `ATTRIBUTION.md`.

## Quick command reference

| Command | One-liner |
|---|---|
| `craft` | Apply Impeccable's design language to a section. |
| `teach` | Explain why the current state is or isn't good. |
| `document` | Produce design notes for a component. |
| `extract` | Pull a pattern from one component into a reusable token / variant. |
| `shape` | Adjust shape language (border radius, corner profiles). |
| `critique` | Point out issues without fixing. |
| `audit` | Comprehensive scan. |
| `polish` | Small refinements (contrast, spacing, alignment). |
| `bolder` | Increase visual weight. |
| `quieter` | Reduce visual weight. |
| `distill` | Simplify a noisy component. |
| `harden` | Add edge-case states (loading, error, empty, disabled). |
| `onboard` | First-time-user / onboarding flow refinement. |
| `animate` | Motion design (eased, never bounce/elastic). |
| `colorize` | Colour palette pass. |
| `typeset` | Typography pass. |
| `layout` | Grid / flex / responsive pass. |
| `delight` | Small interactive flourishes. |
| `overdrive` | Push a component to its emphasised extreme. |
| `clarify` | Wording / labels / microcopy. |
| `adapt` | Responsive variants (mobile / tablet / desktop). |
| `optimize` | Performance (bundle size, render). |
| `live` | Interactive preview / playground for a component. |

Detailed dispatch contract for each: `commands/<name>.md`.
