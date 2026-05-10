---
name: impeccable
version: 1.0.0
description: Bundled design-craft sub-skill. 23 commands (craft/teach/document/extract/shape/critique/audit/polish/bolder/quieter/distill/harden/onboard/animate/colorize/typeset/layout/delight/overdrive/clarify/adapt/optimize/live) for the frontend-designer persona. Vendored from pbakaus/impeccable (MIT, attributed). Loaded with frontend Doctrines.
allowed-tools: [Read, Edit, Write, Glob, Grep, Bash, mcp__Claude_Preview__preview_screenshot, mcp__Claude_Preview__preview_eval]
loaded_by: [default-web-saas, mena-bilingual+frontend, fintech-pci+web, healthcare-hipaa+web, gov-fedramp+web, eu-gdpr+web]
---

# Impeccable bundled skill

> Loaded by the **frontend-designer** persona when a frontend Doctrine is active. Provides 23 design commands plus the principles + anti-pattern catalog that drive the `design-audit` and `impeccable-craft` slash commands.

## Loading order

1. BeQuite SKILL.md routes a P5/P6 frontend task to `frontend-designer`.
2. `frontend-designer` checks `state/project.yaml::active_doctrines`. If a frontend Doctrine is loaded, this Impeccable bundle attaches.
3. The user invokes `bequite design <command>` (or `/bequite.impeccable-craft <command>`); the bundle's `commands/<command>.md` is loaded into context for dispatch.

## Hard rules this bundle enforces (BeQuite-flavored, not upstream Impeccable's)

These are layered on top of upstream Impeccable's philosophy to align with BeQuite's Iron Laws + Doctrines:

1. **Tokens-only outputs.** Every emitted CSS / Tailwind class must reference `tokens.css` / `tokens.json`. No hardcoded hex / rgb / px (except shadow + radius edge cases declared in tokens). Enforces `default-web-saas` Rule 1.
2. **Recorded font choice.** Every typography change requires a one-line comment in `tokens.css` explaining *why this font fits this product*. Enforces Doctrine Rule 2.
3. **No bounce / elastic.** Motion uses linear / ease-out / cubic-bezier — never bounce / elastic / back. Enforces Doctrine Rule 6.
4. **WCAG AA.** axe-core runs after every command; failures block the commit (the `posttooluse-audit.sh` hook gates this). Enforces Doctrine Rule 5+8.
5. **Mobile + desktop parity.** Every command captures evidence at viewport 360 + 1440 (and `ar-*` locale RTL when mena-bilingual is loaded). Enforces Doctrine Rule 7.
6. **No screenshots = no commit.** Before/after screenshots in `evidence/<phase>/<task>/screenshots/` are mandatory. The `impeccable-craft` slash command refuses without them.

## How a command flows

```
bequite design craft <file>
  → load skill/skills-bundled/impeccable/commands/craft.md
  → before-screenshot saved to evidence/<phase>/<task>/screenshots/before/
  → frontend-designer applies craft per the command's contract
  → after-screenshot saved
  → bequite design audit (lightweight) confirms anti-pattern reduction
  → posttooluse-audit.sh runs axe-core + tokens-only check
  → if green: commit suggested with conventional-commit prefix style:
  → if red: BLOCKED; show findings; recommend remediation command
```

## Cross-references

- BeQuite agent: `skill/agents/frontend-designer.md`
- BeQuite slash: `skill/commands/design-audit.md`, `skill/commands/impeccable-craft.md`
- BeQuite Doctrine: `skill/doctrines/default-web-saas.md`
- BeQuite reference: `skill/references/frontend-stack.md` (May-2026 verified frontend libraries)
- Upstream Impeccable: https://github.com/pbakaus/impeccable
- Pinned commit: `.pinned-commit` in this directory
- Attribution: `ATTRIBUTION.md` in this directory

## Versioning

- v1.0.0 (this snapshot) — vendored 2026-05-10, BeQuite v0.6.1 release.
- Future bumps follow upstream's release cadence; ADR required for breaking changes; otherwise PR + `.pinned-commit` update.
