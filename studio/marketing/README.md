# BeQuite Marketing Site

> Apple-grade cinematic landing for vibecoders. Layer 2 Studio Edition. Showcases the power of BeQuite + walks beginners through every workflow.

## Stack

- **Next.js 15** (App Router) — RSC for SEO + client-component islands for Framer Motion.
- **Tailwind CSS v4** — config from `../brand/tokens.css` (single source of truth).
- **Framer Motion 11+** — scroll-driven animations, `useScroll`, `useTransform`, layout animations.
- **Three.js + React Three Fiber + drei** — 3D-ready scaffold; loads GLB on demand (post-Blender).
- **MDX** — content/tutorials for vibecoders.
- **shadcn/ui v3** — component sourcing per Doctrine `default-web-saas` Rule 3.

## Run locally

```bash
cd studio/marketing
pnpm install      # or: bun install / npm install
pnpm dev          # http://localhost:3000
```

## Build

```bash
pnpm typecheck
pnpm lint
pnpm build
pnpm start
```

## Architecture

```
studio/marketing/
├── app/
│   ├── layout.tsx              ← root layout, metadata, fonts
│   ├── page.tsx                ← home (Hero + Phases + Features + Demo + CTA)
│   ├── globals.css             ← imports brand tokens + Tailwind v4 theme
│   └── (docs)/                 ← MDX docs subroute (lands v0.17.0+)
├── components/
│   ├── Nav.tsx                 ← scroll-aware nav with backdrop blur
│   ├── Hero.tsx                ← pinned cinematic hero (Apple-style)
│   ├── PhasesScroll.tsx        ← 7-phase scroll-driven reveal
│   ├── Features.tsx            ← 6-card feature grid with hover glints
│   ├── Demo.tsx                ← terminal-mock CLI walkthrough
│   ├── CTA.tsx                 ← final call-to-action
│   ├── Footer.tsx              ← three-column footer
│   ├── AgentCharacter.tsx      ← brand astronaut (2D today; 3D-ready)
│   └── three/                  ← R3F components (lands v0.17.0+)
├── content/                    ← MDX tutorials (lands v0.17.0+)
│   └── docs/
│       ├── quickstart.mdx
│       ├── from-scratch.mdx    ← workflow for greenfield projects
│       └── retrofit.mdx        ← workflow for installing into existing projects
├── public/
│   └── brand/                  ← copied from ../brand/raw/ for Next.js Image
└── tailwind.config.ts          ← extends ../brand/tokens.css
```

## Brand consistency

All colors / fonts / motion tokens flow from `studio/brand/tokens.css`. **Never** hardcode hex / rgb / px in components. If a token is missing, propose it in `studio/brand/tokens.css` first, then use it.

## Honest scope (Article VI)

### What v0.16.0 ships (in this commit)

- ✅ Full Next.js 15 + Tailwind v4 + Framer Motion scaffold (boots locally).
- ✅ Hero section with pinned scroll + headline + character + scroll cue.
- ✅ Seven-phase scroll-driven reveal section.
- ✅ Six-feature card grid with hover glints.
- ✅ Terminal-mock demo section.
- ✅ CTA section + Footer.
- ✅ Brand tokens wired (gold + black + Apple-style cinematic motion).
- ✅ Astronaut character with breathing-idle animation.
- ✅ Three.js + R3F dependencies installed (3D-ready).

### What v0.17.0+ ships (subsequent commits)

- 🔲 Frame-by-frame video reveal in hero (apple.com/macbook-pro pattern).
- 🔲 GLB-loaded 3D astronaut character (post-Blender).
- 🔲 Particle starfield via R3F.
- 🔲 MDX vibecoder tutorials in `content/docs/`.
- 🔲 Auto-generated docs from CLI `--help` outputs.
- 🔲 Live demo embedding (xterm.js streaming a real CLI session).
- 🔲 Search.
- 🔲 Theme toggle (dark/light — though brand is dark-first).
- 🔲 Lighthouse 95+ pass + axe-core gate green.

## Cross-references

- ADR-013 (Studio architecture): `../../.bequite/memory/decisions/ADR-013-studio-v2-architecture.md`
- Brand system: `../brand/`
- Doctrine: `../../skill/doctrines/default-web-saas.md`
- Parent BeQuite repo: `../..`
