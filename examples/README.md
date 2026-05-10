# BeQuite examples

> Three worked examples demonstrating BeQuite across the doctrine spectrum: web SaaS, CLI tool, and desktop app. Each example is a **spec'd scaffold** — full `.bequite/` tree + seven-phase walkthrough document + stack ADR + HANDOFF — so a developer can clone the example, run `bequite verify`, and see what BeQuite expects at each phase.

## What v0.9.0 ships

The three example directories below each contain:

- **`.bequite/memory/`** — initialised Memory Bank (Cline pattern: 6 files + decisions + prompts/v1).
- **`.bequite/memory/decisions/ADR-001-stack.md`** — stack decision per Doctrine.
- **`specs/<feature>/spec.md`** — what the feature is.
- **`specs/<feature>/plan.md`** — implementation plan.
- **`specs/<feature>/phases.md`** — seven-phase decomposition.
- **`specs/<feature>/tasks.md`** — atomic task list.
- **`state/{project.yaml, current_phase.md, recovery.md}`** — operational state.
- **`HANDOFF.md`** — per-engineer + per-vibe-handoff sections.
- **`README.md`** — what was built, how to run, what each phase exercised.

What v0.9.0 does **not** ship: production-quality code for each example. The point of v0.9.0 is to demonstrate that **the BeQuite scaffold is correct + the seven-phase walk is documented + the doctrine choices are defensible**. Full code walkthroughs land in v0.9.1's e2e harness (which drives `bequite auto` on each example) and in post-v1.0.0 example iterations.

This is honest per Iron Law VI — calling out what was built (scaffolds + walkthroughs) vs what remains (production code, screencasts, fully-running apps).

## The three examples

### 1. `01-bookings-saas/` — web SaaS

- **Doctrine:** `default-web-saas`
- **Stack:** Next.js (App Router) + Hono backend + Supabase (DB + auth) + Clerk (auth alt) + Vercel
- **Scale:** 5,000 MAU (small SaaS tier)
- **Audience:** engineer
- **Feature:** Bookings flow with admin + customer roles
- **Phases exercised:** P0–P7 with focus on P5 (impl) + P6 (Playwright walks) + P7 (handoff)

### 2. `02-ai-tool-wrapper/` — CLI tool

- **Doctrine:** `cli-tool`
- **Stack:** Python 3.11+ + Anthropic SDK + click + rich + httpx
- **Scale:** solo (single-user CLI)
- **Audience:** engineer
- **Feature:** Markdown summariser CLI (`mdsum <file>`)
- **Phases exercised:** P0–P7 with focus on P1 (stack ADR), P5 (impl), P7 (handoff via README + `--help`)

### 3. `03-tauri-note-app/` — desktop

- **Doctrine:** `desktop-tauri`
- **Stack:** Tauri v2 + SvelteKit + SQLite + OS keychain (`tauri-plugin-keyring`, NOT deprecated Stronghold)
- **Scale:** local-first (single-user desktop)
- **Audience:** engineer
- **Feature:** Local-first note CRUD with end-to-end encryption (key from OS keychain)
- **Phases exercised:** P0–P7 with focus on P1 (stack ADR including signing chain) + P5 (impl) + P6 (notarytool/AzureSignTool config) + P7 (release-package handoff)

## How to use these examples

For each example:

```bash
# 1. Read the example's README.md.
cat examples/01-bookings-saas/README.md

# 2. Inspect the stack ADR.
cat examples/01-bookings-saas/.bequite/memory/decisions/ADR-001-stack.md

# 3. Inspect the seven-phase walkthrough.
cat examples/01-bookings-saas/specs/bookings-flow/phases.md

# 4. Inspect the HANDOFF.
cat examples/01-bookings-saas/HANDOFF.md

# 5. Optional: run bequite verify against the scaffold (lots of gates will be N/A
#    because there's no actual code yet — that's expected).
cd examples/01-bookings-saas/
python -m cli.bequite.verify   # from repo root with PYTHONPATH=cli/
```

## Cross-references

- BeQuite repo root: `..`
- The Skill (source of truth): `../skill/`
- Doctrines used: `../skill/doctrines/{default-web-saas,cli-tool,desktop-tauri}.md`
- Tokens template: `../skill/templates/tokens.css.tpl` (used by example 1)
- Walkthrough templates: `../skill/templates/tests/walkthroughs/`
- Build plan §9 line items: `../  .bequite/memory/prompts/v1/2026-05-10_initial-plan.md`

## Forking guidance

To create your own example:

1. Pick a Doctrine.
2. Run `python -m cli.bequite init my-example --doctrine <doctrine> --scale <tier>` (from the BeQuite repo root).
3. Walk it through P0 → P7 manually (auto-mode lands v0.10.0 — until then, supervised execution).
4. Archive receipts at `.bequite/receipts/`.
5. Write a HANDOFF.md.
6. PR the example into BeQuite's `examples/` directory.
