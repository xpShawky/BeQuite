# BeQuite Studio (Layer 2)

> v2.0.0+ — the visual surface for BeQuite. Three apps sharing one brand system.

## What's here

```
studio/
├── brand/         ← shared design system + raw assets (gold + black + Geist)
├── marketing/     ← Next.js 15 landing page (Apple-grade cinematic)
├── dashboard/     ← Next.js 15 operations console (image 6 mock; v0.18.0+ impl)
├── api/           ← Hono-on-Bun back-end (v0.19.0+ impl)
└── README.md      ← this file
```

## Status (v0.16.0)

| Surface | Phase | What works today |
|---|---|---|
| `brand/` | ✅ shipped | Tokens (CSS + JSON) + 6 ranked source PNGs + ATTRIBUTION + README. |
| `marketing/` | ✅ scaffold ready (boots locally) | Hero (pinned cinematic) / 7-phase scroll / 6-feature grid / terminal demo / CTA / Footer. Brand wired. Framer Motion + R3F installed. |
| `dashboard/` | 📁 directory + README only | Full Next.js implementation lands v0.18.0+. |
| `api/` | 📁 directory + README only | Hono boilerplate + endpoint surface designed; impl lands v0.19.0+. |

## Run the marketing site

```bash
cd studio/marketing
pnpm install   # or: bun install / npm install
pnpm dev       # http://localhost:3000
```

## Roadmap

| Tag | Surface | Adds |
|---|---|---|
| v0.16.0 (now) | brand + marketing scaffold | Phase-1: tokens + scaffold + boots locally |
| v0.17.0 | marketing | Frame-by-frame cinematic chapters; vibecoder MDX tutorials; R3F particle starfield; Lighthouse 95+ |
| v0.17.5 | marketing + brand | Blender-pipeline 3D astronaut (assumes Ahmed installs Blender) |
| v0.18.0 | dashboard | Real Next.js impl per image 6 mock; reads .bequite/ from any project |
| v0.18.5 | dashboard | xterm.js live terminal stream when signed-in |
| v0.19.0 | api | Hono-on-Bun + Zod + Better-Auth + Postgres + endpoint surface |
| v2.0.0 | all | Studio Edition release |

## Brand-first rule

Every UI value across all three surfaces resolves to `studio/brand/tokens.css`. No hardcoded hex / rgb / px outside the brand folder. Doctrine `default-web-saas` Rule 1.

## Cross-references

- ADR-013 (Studio v2 architecture): `../.bequite/memory/decisions/ADR-013-studio-v2-architecture.md`
- ADR-014 (Iron Law X — operational completeness): `../.bequite/memory/decisions/ADR-014-iron-law-x-operational-completeness.md`
- Constitution v1.3.0: `../.bequite/memory/constitution.md`
- Layer 1 Harness (parent): `..`
