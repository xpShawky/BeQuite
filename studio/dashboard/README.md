# BeQuite Dashboard

> The Studio operations console. Visual layout matches `../brand/raw/06-studio-dashboard-mock.png`. Reads `.bequite/` from any BeQuite-managed project.
>
> **v0.18.0** = filesystem-mode (direct reads). **v2.0.0-alpha.1 candidate** = dual-mode dispatcher — filesystem OR HTTP via `BEQUITE_DASHBOARD_MODE` env. Server-component callers see the same `ProjectSnapshot` shape either way. **v0.20.0** adds live SSE updates via the `LiveIndicator` (HTTP mode only).

## Run

```bash
cd studio/dashboard
pnpm install      # or: npm install
pnpm dev          # → http://localhost:3001
```

By default the dashboard targets `../..` (the BeQuite repo itself) — perfect for dogfooding.

## Loader modes (v2.0.0-alpha.1 candidate)

| Env | Default | Behavior |
|---|---|---|
| `BEQUITE_DASHBOARD_MODE=filesystem` | yes | Server components read `.bequite/` directly from disk. Single-machine dev. |
| `BEQUITE_DASHBOARD_MODE=http` | no | Server components fetch from `BEQUITE_API_BASE` (default `http://localhost:3002`). Required for multi-user/cloud. |
| `BEQUITE_API_BASE=http://...` | `http://localhost:3002` | Base URL when in HTTP mode. |
| `BEQUITE_API_TOKEN=<hex>` | (none) | Bearer token when the API runs with `BEQUITE_AUTH_MODE=token`. Omit in local-dev mode. |

The footer shows the active mode as a chip (`FS` or `HTTP`) so you always know what the page rendered against.

### HTTP-mode quickstart

```bash
# Terminal 1 — start the API
cd studio/api
bun install && bun run src/index.ts   # → http://localhost:3002 (local-dev auth)

# Terminal 2 — start the dashboard in HTTP mode
cd studio/dashboard
BEQUITE_DASHBOARD_MODE=http pnpm dev  # → http://localhost:3001 talks to :3002
```

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

## What it reads

### Filesystem mode (`BEQUITE_DASHBOARD_MODE=filesystem`, default)

- `<project>/.bequite/memory/constitution.md` — Constitution version
- `<project>/.bequite/memory/projectbrief.md` — project name
- `<project>/.bequite/memory/activeContext.md` — active context summary
- `<project>/.bequite/receipts/*.json` — last 10 receipts (with signature check)
- `<project>/.bequite/cache/cost-ledger.json` — session cost rollup
- `<project>/state/current_phase.md` — current phase
- `<project>/state/recovery.md` — last green tag + summary

### HTTP mode (`BEQUITE_DASHBOARD_MODE=http`)

The dashboard hits these endpoints on `studio/api/`:

- `GET /healthz` — reachability probe
- `GET /api/v1/auth/status` — auth mode badge
- `GET /api/v1/projects/snapshot?path=<workspace>` — full `ProjectSnapshot`
- `GET /api/v1/projects` — project list
- `GET /api/v1/receipts?path=<workspace>` — receipt list (delivered as part of the snapshot today; separate call lands when receipts pagination ships)

Server components `await loadProject()` in either mode — the return shape is identical. The HTTP loader degrades gracefully on API unreachability (returns a sentinel snapshot with `recoveryPreview` describing the failure rather than throwing into the render path).

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
│   ├── projects.ts             ← dual-mode dispatcher (await loadProject())
│   ├── projects-types.ts       ← shared ProjectSnapshot types
│   ├── projects-filesystem.ts  ← filesystem reader
│   ├── projects-http.ts        ← HTTP reader (fetch via api-client)
│   └── api-client.ts           ← StudioApiClient (Bearer auth, reachability probe)
└── public/brand/          ← astronaut + logo
```

## Live updates (v0.20.0)

The dashboard subscribes to SSE streams from `studio/api/` when running in HTTP mode. The `LiveIndicator` component (top-right of the TopBar) shows the current stream status:

| Pill | Meaning |
|---|---|
| ● LIVE | SSE connected; heartbeat fresh (≤60s old) |
| ○ CONNECTING | Initial connection in progress / reconnecting |
| ◐ STALE | No heartbeat received in 60s; may have lost the stream |
| ✕ OFFLINE | Transport error / API unreachable / closed |
| — FS | Filesystem mode — no stream to subscribe to |

When a `receipt` / `cost` / `phase` / `active_context` event arrives, the indicator triggers a throttled `router.refresh()` (default: 2s throttle) so the server-component re-render shows the new state without a manual page reload. This is the "operationally complete" piece for the dashboard side — Iron Law X step 7 ("did the user need to refresh?") is answered "no" by construction.

**For token-mode APIs:** set `NEXT_PUBLIC_BEQUITE_API_TOKEN` in the dashboard's `.env.local` before running `pnpm dev`. The token is sent as `?token=<hex>` in the SSE URL (browser EventSource can't send custom headers; the API auth middleware accepts the query-param fallback only on `/api/v1/streams/*`).

## What's still missing (lands v0.20.5 / v2.0.0)

- **Bidirectional WebSocket terminal stream (xterm.js)** for auto-mode (v0.20.5; needs node-pty + RoE gates per Article IV).
- **Project picker** (currently hardcoded to `../..`) (v2.0.0).
- **Authenticated views** with per-project ACL (per ADR-011 Phase-3 + ADR-015) (v0.20.x+).
- **3D astronaut** in the AgentPanel (post-Blender pipeline; see `../marketing/components/three/AgentCharacter3D.tsx`).

## Cross-references

- Visual target: `../brand/raw/06-studio-dashboard-mock.png`
- Marketing app (sister): `../marketing/`
- API (back-end, v0.19.0+): `../api/`
- ADR-013: `../../.bequite/memory/decisions/ADR-013-studio-v2-architecture.md`
- Doctrine `default-web-saas`: `../../skill/doctrines/default-web-saas.md`
