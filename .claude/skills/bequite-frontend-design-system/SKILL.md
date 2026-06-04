---
name: bequite-frontend-design-system
description: Use when building, redesigning, auditing, or editing any frontend/UI/UX across more than one section — keeps design identity consistent from hero to footer. Master skill; coordinates ux-ui-designer (design), frontend-quality (slop detection), live-edit (section edits). Owns Design DNA, the section-by-section loop, the Design Continuity Gate, visual QA, and product-type rules.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, WebFetch, WebSearch
---

# bequite-frontend-design-system — keep the whole page as good as the hero

## Why this skill exists

AI frontends start strong (hero) and **drift in the middle** — generic cards, all-caps misuse, wide letter-spacing, gray-on-color text, text overflow, lost identity, "code-looking" sections. Root cause: the design intent lives only in chat and decays as the page gets longer, so the model falls back to the generic statistical average. This skill fixes that **structurally**: persist the Design DNA, build section-by-section, and gate every section against the DNA.

**Quality promise:** Hero quality is not enough. Every visible section must meet the Design DNA. No section may look like filler. No UI is complete without a Design Continuity pass and a Visual QA pass.

## This is the master skill — it coordinates, it doesn't duplicate

| Need | Call |
|---|---|
| Generate design / palette / type / tokens | `bequite-ux-ui-designer` (owns the 10 principles + token contract) |
| Detect AI-slop in code | `bequite-frontend-quality` (owns the 15 slop tells + sourcing order) |
| Edit one section of a running app + browser screenshots | `bequite-live-edit` (owns the 3-tier inspection + rollback) |

Full map: `.bequite/design/FRONTEND_SKILL_MAP.md`. Do not create new scattered FE skills — extend `references/` here instead.

## The non-negotiable loop (never "build the whole page and hope")

1. **DNA** — read/create `.bequite/design/DESIGN_DNA.md`. If missing/placeholder, fill + lock it BEFORE any UI code (`DESIGN_DNA_LOCKED`). Pick the product type → apply `references/product-type-rules.md`.
2. **Structure** — decide page sections.
3. **Section map** — write `.bequite/uiux/SECTION_MAP.md`, each section with acceptance criteria.
4. **Build section 1 → check section 1** against the DNA.
5. **Build section 2 → check section 2** against the DNA *and* section 1.
6. …continue section by section, re-reading `.bequite/state/FRONTEND_CONTEXT_SUMMARY.md` each time (cheap context).
7. **Full-page continuity audit** → `references/design-continuity-checklist.md` → write `.bequite/design/DESIGN_CONTINUITY_REPORT.md`.
8. **Responsive audit** — 360 / 768 / 1440 + named breakpoints.
9. **Accessibility / contrast audit** — WCAG 2.2 AA (AAA for regulated product types).
10. **Final polish** — pull the weakest section up to the strongest. Write `.bequite/audits/VISUAL_QA_REPORT.md`.

The check-after-each-section is the whole point: drift is caught while it's cheap to fix, not at the end.

## Context engineering (why this works)

Persist design, don't remember it. Before any frontend task, read `FRONTEND_CONTEXT_SUMMARY.md` (1-screen digest); escalate to the full DNA / section map only when needed. Never continue from vague memory — if you can't state the font, primary color, spacing scale, and product type, re-read the DNA. After each section, update the summary. Full rules: `docs/architecture/FRONTEND_CONTEXT_ENGINEERING.md`.

## The Design Continuity Gate

Run it on **every** surface (not a 3-screen sample): hero · every middle section · final sections · nav · footer · cards · forms · modals · dashboards · tables · empty/loading/error/hover/focus states · all breakpoints. It catches: text overflow, all-caps misuse, wide tracking, inconsistent sizes/radius, random gradients, weak contrast, gray-on-color, pure-black-vs-tinted-neutral, nested cards, cliché SaaS layouts, broken hierarchy, mixed icon styles, dead buttons, unfinished/off-DNA sections, generic AI UI. Detection heuristics: `references/design-continuity-checklist.md`. Gate spec: `docs/architecture/DESIGN_CONTINUITY_GATE.md`. Gate name: `DESIGN_CONTINUITY_PASS`.

## Visual QA (render it — don't trust code inspection)

If a frontend exists, render it. Use the highest available browser tier (Playwright MCP → project Playwright → code inspection + user screenshots; Claude Code bundled run/verify if present). **Never auto-install Playwright.** Check: route loads, no console/network errors, buttons clickable, text visible, no overflow, each middle section, mobile view, breakpoints, dark/light contrast, real states. Write `.bequite/audits/VISUAL_QA_REPORT.md` (`VISUAL_QA_DONE`). Checklist: `references/visual-qa-checklist.md`.

## Product-type awareness (not everything is a cinematic SaaS landing)

Read the product type from the DNA and apply the matching row of `references/product-type-rules.md` — it adapts layout, navigation, density, typography, color mood, trust level, motion, CTA style, dashboard patterns, mobile needs, and accessibility level. A dense dark finance dashboard and an airy wellness app are *both correct* for their type; judge continuity against the type, not a universal template.

## Cinematic / 3D / animated (only when the product needs it)

Don't force motion. When the product genuinely calls for cinematic/3D, gate it on: performance, mobile fallback, reduced-motion, load time, accessibility, readability, business fit, distraction risk, conversion impact, progressive enhancement, fallback states. Checklist: `references/cinematic-ui-checklist.md`. Mobile-app specifics: `references/mobile-app-ui-checklist.md`.

## Effort awareness (`${CLAUDE_EFFORT}` / Ultracode)

- **low / medium** — compact: run the grep heuristics + spot-check the weakest middle sections.
- **high** — full: every section + component + state vs the DNA; full continuity report.
- **xhigh / max / Ultracode** — senior-design-review mode: per-section critique with snapshots, full responsive + a11y sweep, browser visual QA, final polish.

If effort is unavailable, infer from operating mode: `deep`→high+, `fast`→compact, `token-saver`→compact + cached DNA, `delegate`→strong model writes the DNA + criteria, cheap model self-checks, strong model verifies.

## References (load on demand — do NOT inline all of these)

- `references/design-continuity-checklist.md` — the gate's drift detection (grep + visual)
- `references/visual-qa-checklist.md` · `references/mobile-app-ui-checklist.md` · `references/cinematic-ui-checklist.md`
- `references/product-type-rules.md` — product-category → design rules
- `references/design-dna-template.md` — how to fill a DNA
- `references/impeccable-notes.md` · `references/ui-ux-pro-max-notes.md` · `references/superpowers-notes.md` — researched principles
- `examples/` — worked DNA / section map / visual QA report

## Tool neutrality (global rule)

Every tool/library/font/framework named in this skill or its references (Playwright, axe-core, shadcn/ui, OKLCH tooling, specific fonts, Three.js, etc.) is an **example, not a default**. The principles (DNA, continuity, contrast floors, section loop) are universal; the tools are candidates to evaluate per project. Don't auto-install. Write a decision section before adopting. See `.bequite/principles/TOOL_NEUTRALITY.md`.

## When NOT to use this skill (alpha.15)

- The task is a single isolated tweak with no cross-section risk → `bequite-live-edit` directly.
- No frontend in the project → skill stays dormant.
- Pure design *generation* with no continuity concern → `bequite-ux-ui-designer`.
- A simpler supporting skill fully covers the need → use it and note why.

## Quality gate (alpha.15)

Before claiming this skill's work complete:

- [ ] `DESIGN_DNA.md` exists + locked; product type chosen
- [ ] `SECTION_MAP.md` covers every built section with acceptance criteria
- [ ] Section-by-section loop run (not "whole page at once")
- [ ] `DESIGN_CONTINUITY_REPORT.md` written; no BLOCKER/HIGH drift open
- [ ] `VISUAL_QA_REPORT.md` written (browser tier or honest tier-3 note)
- [ ] `FRONTEND_CONTEXT_SUMMARY.md` updated
- [ ] `MISTAKE_MEMORY.md` updated for any `[fe][design]` lesson
- [ ] No banned weasel words; no auto-installed dependency
- [ ] `AGENT_LOG.md` + state files updated

If any item fails, report PARTIAL with the specific gap — do not claim done.
