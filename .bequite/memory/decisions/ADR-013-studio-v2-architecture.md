---
adr_id: ADR-013-studio-v2-architecture
title: Studio v2.0.0 architecture — three surfaces (marketing + dashboard + api) + brand system + 3D-ready scaffold
status: accepted
date: 2026-05-10
deciders: [Ahmed Shawky (xpShawky), Claude Code Opus 4.7 (architect)]
supersedes: null
constitution_version: 1.2.0   # bumps to 1.3.0 alongside ADR-014
related_articles: [I, II, III, VI]
implementation_target: v0.16.0 Phase-1 docs + brand + marketing scaffold / v0.17.0+ marketing cinematic chapters / v0.18.0+ dashboard real impl / v0.19.0+ api / v2.0.0 Studio Edition release
---

# ADR-013: Studio v2.0.0 Architecture

> Status: **accepted (Phase-1: docs + brand system + scaffold lands v0.16.0)** · Date: 2026-05-10

## Context

ADR-008 established the two-layer architecture: **Layer 1 Harness** (the CLI + skill, currently shipping toward v1.0.0) and **Layer 2 Studio** (deferred to v2.0.0+). Ahmed has now greenlit Studio Edition work to begin alongside the v1.0.0 review pause.

The brand assets (6 ranked images at `Assets/1-6.png`) define the visual grammar:
- Gold + black core palette
- Astronaut character (zen-pose + pointing-pose) as personality anchor
- Chat-bubble-with-terminal-prompt mark
- Premium 3D-rendered hero compositions (image 1 + 4)
- A pre-mocked dashboard surface (image 6) that operationalizes the Studio's information architecture

Ahmed asked specifically for:
1. A **marketing/landing site** — Apple-grade cinematic, scroll-driven, frame-by-frame transitions (reference: https://www.apple.com/macbook-pro/), with Framer Motion + 3D-ready architecture (Three.js / R3F) so installing Blender later expands capability without restructuring.
2. **Deep tutorials for vibecoders** — non-engineers walking through workflows from-scratch + retrofitting existing projects.
3. The **Studio dashboard** itself (per ADR-008's deferred scope) — implements image 6's information architecture: phases sidebar / command console / planning + tasks + tests / agent panel / status pillar.

## Decision

Studio v2.0.0 is **three surfaces** sharing one brand system + one design language:

```
bequite/                        ← repo root
├── (Layer 1 Harness — unchanged through v1.0.0)
└── studio/                     ← Layer 2 Studio (v2.0.0+)
    ├── brand/                  ← shared design system + raw assets
    │   ├── raw/                ← ChatGPT-generated source PNGs (6 ranked)
    │   ├── tokens.css          ← gold/black palette, Apple-style type scale
    │   ├── tokens.json         ← machine-readable tokens
    │   ├── ATTRIBUTION.md      ← character + mark + wordmark provenance
    │   └── README.md           ← brand usage rules
    ├── marketing/              ← Next.js 15 landing page (Apple-grade)
    │   ├── app/
    │   ├── components/
    │   ├── content/            ← MDX docs + tutorials for vibecoders
    │   ├── public/
    │   └── package.json
    ├── dashboard/              ← Next.js 15 operations console (per image 6)
    │   ├── app/
    │   ├── components/
    │   ├── lib/                ← reads .bequite/ + state/ + receipts/ from any BeQuite-managed project
    │   └── package.json
    ├── api/                    ← Hono API (NOT NestJS — smaller; matches default-web-saas Doctrine Rule 3)
    │   ├── routes/
    │   ├── lib/
    │   └── package.json
    └── README.md               ← Studio-level overview
```

### Why three apps not one

- **Marketing's audience is vibecoders + decision-makers.** Optimized for SEO, scroll-driven storytelling, sub-second LCP. Public Internet target. CDN-cached. No auth surface.
- **Dashboard's audience is BeQuite-power-users.** Authenticated; reads sensitive receipt + state data; rich interactivity > SEO.
- **API serves both** — minimal surface (read receipts + state from a BeQuite project the dashboard user has access to; serve marketing CMS endpoints if marketing pages need dynamic content later).

### Stack per surface

#### Marketing
- **Next.js 15 (App Router)** — RSC for SEO + client-component islands for Framer Motion.
- **Tailwind v4** — config from `studio/brand/tokens.css`.
- **Framer Motion 11+** — scroll-driven animations, `useScroll`, `useTransform`, layout animations.
- **MDX** for content/tutorials.
- **shadcn/ui v3** — Doctrine `default-web-saas` Rule 3 sourcing order.
- **Three.js + React Three Fiber + drei** — 3D-ready scaffold; loads GLB on demand.
- **Hosting:** Vercel (per Doctrine + scale tier).

#### Dashboard
- **Next.js 15 (App Router)** — same framework as marketing (one codebase / one DevX).
- **TanStack Query v5** — server state from API.
- **Zustand** — minimal client state.
- **Framer Motion** — phase-board transitions, status-pillar pulse.
- **xterm.js** — terminal preview for command-console mock + live streaming if user is signed-in.
- **Three.js (optional) — for "BeQuite agent online" 3D character peeking from right side per image 6.**

#### API
- **Hono on Bun** — smallest TS edge backend (matches Doctrine Rule).
- **Zod** for input validation everywhere (Doctrine Rule 11).
- **Better-Auth** when auth lands (per ADR-011).
- **Postgres (Supabase)** for project metadata + receipt mirrors (when v2.0.0 cloud features stand up).

### 3D / Blender pathway (answering Ahmed's question)

**Today, no Blender required:**
- Three.js + React Three Fiber + drei suffice for: particle systems, scroll-driven 3D, sprite-based animations, primitive 3D constructions, GLB loading from any source (Sketchfab, free-license libraries).
- The astronaut character can ship as a 2D sprite sheet (frame-by-frame from images 2/3 or rendered fresh from new compositions) animated via Framer Motion — no 3D required.

**With Blender (recommended pathway for cinematic upgrades):**
- Model the astronaut character once in Blender → rig + animate (idle / wave / point / zen) → export `.glb` (gLTF binary).
- React Three Fiber loads the `.glb` via `<useGLTF />`. Animations play via `<useAnimations />`.
- Scroll position drives `useTransform` → animation timeline scrub. Apple's macbook-pro page does exactly this.
- The Blender + R3F pipeline is 1-2 days of art + 1-2 days of integration.

**Architecture is 3D-ready from v0.16.0:**
- `studio/marketing/components/three/` directory with R3F + drei pre-installed.
- `studio/marketing/public/3d/` for GLB asset drops (placeholder while Blender output pending).
- Hero + features sections built with **fallback-first**: 2D Framer Motion scenes that the 3D version replaces drop-in.

### Apple-style cinematic scroll pattern

Per Ahmed's reference (https://www.apple.com/macbook-pro/), the pattern is:
- **Pinned hero** — scroll inside a viewport-tall section reveals frame-by-frame video / 3D / SVG.
- **Stage transitions** — every ~600vh of scroll = one chapter; smooth cross-fade or 3D camera-cut.
- **Ribbon / sticky context** — phase indicator on the side updates as user scrolls.
- **Final CTA chapter** — after all chapters, the install CTA dominates.

Implementation pattern in this scaffold:
- Each chapter is a `<Chapter />` component.
- Uses `useScroll({ target, offset })` per chapter to drive its own progress.
- Frame-by-frame reveal via `useTransform(scroll, [0, 1], [frame0, frameN])` + image-sequence preloading.
- 3D version (post-Blender) swaps the image-sequence with a `<useGLTF />` mount + animation scrubber.

### Brand color palette (locked)

From the assets:
```
--gold-primary:   #E5B547   /* primary brand gold (logo/character accents) */
--gold-bright:    #F2C76A   /* highlights / glints / call-to-action active */
--gold-deep:      #B8861E   /* hover / pressed states */
--black-pure:     #000000   /* primary background */
--black-stage:    #0A0A0A   /* lifted surfaces (cards, panels) */
--black-velvet:   #141414   /* hover surfaces */
--silver:         #D4D4D4   /* "BeQuite" wordmark / secondary text */
--silver-soft:    #A3A3A3   /* tertiary text / dividers */
--white-pure:     #FFFFFF   /* hero text / contrast peaks */
```

Type scale (Apple-inspired, not copied):
```
--font-display:   "Soehne"|"Inter Display"|"Geist", system-ui, sans-serif
--font-sans:      "Inter", "Geist", system-ui, sans-serif
--font-mono:      "Geist Mono", "JetBrains Mono", monospace
--text-hero:      clamp(3rem, 8vw, 7rem)        /* hero ~96-112px */
--text-display:   clamp(2.25rem, 5vw, 4.5rem)   /* section title */
--text-h1:        clamp(1.75rem, 3.5vw, 2.75rem)
--text-h2:        clamp(1.375rem, 2.5vw, 2rem)
--text-body:      clamp(1rem, 1.2vw, 1.125rem)
```

Motion tokens (eased, never bouncy — per Doctrine Rule 6):
```
--ease-cinematic: cubic-bezier(0.16, 1, 0.3, 1)   /* Apple-flavored ease-out */
--ease-soft-in:   cubic-bezier(0.4, 0, 0.6, 1)
--dur-quick:      200ms
--dur-base:       400ms
--dur-cinematic:  900ms
--dur-stage:      1600ms
```

## What v0.16.0 Phase-1 ships

1. **`studio/brand/`** — tokens.css + tokens.json + ATTRIBUTION + README + the 6 ranked source PNGs at `studio/brand/raw/`.
2. **`studio/README.md`** — Studio-level overview.
3. **`studio/marketing/`** — Next.js 15 + Tailwind v4 + Framer Motion + R3F-ready scaffold:
   - `app/layout.tsx` + `app/page.tsx` with brand-tokens wired
   - `components/Hero.tsx` — pinned hero with Framer Motion (placeholder for 3D)
   - `components/PhasesScroll.tsx` — scroll-driven 7-phase reveal
   - `components/AgentCharacter.tsx` — character art with breathing/blinking idle motion
   - `components/Footer.tsx`
   - `package.json` + `tsconfig.json` + `next.config.ts` + `tailwind.config.ts`
   - boots locally: `cd studio/marketing && bun install && bun dev`
4. **`studio/dashboard/`** — directory + README + placeholder scaffold (full implementation v0.18.0+).
5. **`studio/api/`** — directory + README + Hono boilerplate (full implementation v0.19.0+).
6. **`docs/architecture/STUDIO_V2_OVERVIEW.md`** — non-engineer-friendly overview.

## What v0.16.0 explicitly does NOT ship

Per Article VI honest reporting:
- **Apple-grade frame-by-frame cinematic scroll** — chapters skeleton present, but the actual frame sequences + 3D scenes are subsequent commits (v0.17.0+).
- **Live dashboard UI from image 6** — visual layout matches but no live-data wiring (v0.18.0+).
- **Backend API serving real data** — Hono boilerplate only; no DB, no auth (v0.19.0+).
- **Vibecoder tutorials (deep walkthroughs)** — content scaffold present in `studio/marketing/content/`; chapter MDX bodies subsequent (v0.17.0+).
- **3D Blender pipeline** — R3F infrastructure ready; actual GLB assets pending Ahmed's Blender install + asset creation (v0.17.0+ when assets exist).

## Cross-references

- ADR-008 (two-layer architecture): `.bequite/memory/decisions/ADR-008-master-merge.md`
- ADR-014 (Iron Law X — operational completeness): `.bequite/memory/decisions/ADR-014-iron-law-x-operational-completeness.md`
- Constitution v1.3.0: `.bequite/memory/constitution.md`
- Brand assets: `studio/brand/raw/`
- Doctrine `default-web-saas` (governs marketing + dashboard UI): `skill/doctrines/default-web-saas.md`

## Status: accepted (2026-05-10; Phase-1 lands v0.16.0)
