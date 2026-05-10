# BeQuite Dashboard

> The Studio operations console. Visual layout matches `../brand/raw/06-studio-dashboard-mock.png`. Reads `.bequite/` from any BeQuite-managed project.
>
> **v0.18.0 = working app** (filesystem-backed; reads receipts + state + Memory Bank). **v0.19.0** swaps filesystem for HTTP calls to `../api/` for multi-user / cloud operation.

## Run

```bash
cd studio/dashboard
pnpm install
pnpm dev          # → http://localhost:3001
```

By default the dashboard targets `../..` (the BeQuite repo itself) — perfect for dogfooding.

## Information architecture (matches image 6)

```
┌─ TopBar ────────────────────────────────────────────────────┐
│ [BeQuite] · workspace · project           AGENT ONLINE     │
├──────────┬─────────────────────────────────┬─────────────────┤
│ Phases   │ Command Console                  │  Agent panel   │
│ P0 ✓     │  $ bequite init                  │  [astronaut]   │
│ P1 ✓     │  $ bequite plan                  │   online       │
│ P2 ✓     │  $ bequite verify ✓              │   Hi. Memory   │
│ P3 ✓     │                                  │   loaded.      │
│ P4 ✓     │                                  │   Ready.       │
│ P5       │                                  │                │
│ P6       │                                  │                │
│ P7       │                                  │                │
│          │                                  │                │
│ Dev      │  Plan | Tasks | Tests panels    │                │
│ Status   │                                  │                │
│ READY    │                                  │                │
│          │  Receipts list                   │                │
│ [DEPLOY] │                                  │                │
└──────────┴─────────────────────────────────┴─────────────────┘
       v0.18.0 footer: Constitution v1.3.0 · Doctrines · Last green tag
```

## What it reads (v0.18.0 filesystem-mode)

- `<project>/.bequite/memory/constitution.md` — Constitution version
- `<project>/.bequite/memory/projectbrief.md` — project name
- `<project>/.bequite/memory/activeContext.md` — active context summary
- `<project>/.bequite/receipts/*.json` — last 10 receipts (with signature check)
- `<project>/.bequite/cache/cost-ledger.json` — session cost rollup
- `<project>/state/current_phase.md` — current phase
- `<project>/state/recovery.md` — last green tag + summary

All reads are **server-component synchronous** — `lib/projects.ts::loadProject(rootDir)` is called from `app/page.tsx`. No client-side JS for data loading in v0.18.0.

## Stack

- Next.js 15 (App Router)
- React 19
- Tailwind v4 (brand tokens from `../brand/tokens.css`)
- Framer Motion 11
- Lucide React icons
- TanStack Query 5 (wired but not yet used; activates v0.19.0)
- `gray-matter` for frontmatter parsing

## File map

```
studio/dashboard/
├── app/
│   ├── layout.tsx         ← root + metadata
│   ├── page.tsx           ← composes TopBar + PhasesSidebar + main + AgentPanel
│   └── globals.css        ← imports brand tokens
├── components/
│   ├── TopBar.tsx         ← logo + workspace/project + agent online indicator
│   ├── PhasesSidebar.tsx  ← P0..P7 with status icons + DEV STATUS + DEPLOY
│   ├── CommandConsole.tsx ← terminal-mock with prompt + ✓ output styling
│   ├── PlanTasksTests.tsx ← 3-column panel grid
│   ├── AgentPanel.tsx     ← right-side astronaut + status message
│   └── ReceiptsList.tsx   ← signed-receipt rows from .bequite/receipts/
├── lib/
│   └── projects.ts        ← filesystem loader (loadProject + listKnownProjects)
└── public/brand/          ← astronaut + logo
```

## What's still missing (lands v0.18.5+ / v0.19.0)

- **Live terminal stream (xterm.js)** when authenticated.
- **HTTP to `../api/`** instead of filesystem (so the dashboard can read remote projects, not just local).
- **WebSocket heartbeat** for auto-mode live updates.
- **Project picker** (currently hardcoded to `../..`).
- **Authenticated views** (per ADR-011 Phase-3 device-code auth).
- **3D astronaut** in the AgentPanel (post-Blender pipeline; see `../marketing/components/three/AgentCharacter3D.tsx`).

## Cross-references

- Visual target: `../brand/raw/06-studio-dashboard-mock.png`
- Marketing app (sister): `../marketing/`
- API (back-end, v0.19.0+): `../api/`
- ADR-013: `../../.bequite/memory/decisions/ADR-013-studio-v2-architecture.md`
- Doctrine `default-web-saas`: `../../skill/doctrines/default-web-saas.md`
