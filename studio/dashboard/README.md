# BeQuite Dashboard (placeholder — full impl v0.18.0+)

> The Studio operations console. Visual layout target: `../brand/raw/06-studio-dashboard-mock.png`.

## Information architecture (per the mock)

```
┌─ Top bar ──────────────────────────────────────────────────┐
│ [BeQuite ⚡] Workspace · Project Name              [agent]│
├──────┬─────────────────────────────────────┬───────────────┤
│Phases│   COMMAND CONSOLE                    │ AGENT ONLINE  │
│      │   $ bequite init                     │  [astronaut]  │
│ P0 ✓ │   $ bequite plan                     │  Hi there.    │
│ P1 ✓ │   ...                                │  Ready when   │
│ P2 ✓ │                                      │  you are.     │
│ P3 ✓ │                                      │               │
│ P4 ⏳│                                      │               │
│ P5   │                                      │               │
│ P6   ├─────────────────────────────────────┤               │
│      │ PLAN  │ TASKS  │ TESTS                │               │
│ DEV  │       │        │                       │               │
│ STATUS│ ...  │ ...    │ ...                  │               │
│ READY│       │        │                       │               │
│      │       │        │                       │               │
│ DEPLOY│      │        │                       │               │
└──────┴─────────────────────────────────────┴───────────────┘
```

## Stack (planned for v0.18.0+)

- Next.js 15 (App Router) — same framework as marketing.
- TanStack Query v5 — server state from `../api/`.
- Zustand — minimal client state.
- Framer Motion — phase-board transitions.
- xterm.js — live terminal preview when signed in.
- Three.js (optional) — 3D astronaut peek per the mock.

## Reads from BeQuite-managed projects

The dashboard reads (read-only by default):

- `<project>/.bequite/memory/` — Memory Bank + decisions.
- `<project>/state/{recovery,current_phase,project,task_index,decision_index,evidence_index}.{md,json,yaml}` — operational state.
- `<project>/.bequite/receipts/` — chain-hashed JSON receipts.
- `<project>/.bequite/cache/cost-ledger.json` — session cost.
- `<project>/specs/<feature>/{spec,plan,phases,tasks}.md` — planning artifacts.

Write actions (when authenticated, post-v0.10.6 device-code auth):
- Update `state/recovery.md`, `activeContext.md`, `progress.md` on user-driven phase transitions.
- Trigger CLI commands via `../api/`.

## Status

**v0.16.0 ships this README + the directory structure only.** The actual Next.js implementation lands per the v0.18.0 row in the master roadmap.

## Cross-references

- Visual target: `../brand/raw/06-studio-dashboard-mock.png`
- Marketing app (sister): `../marketing/`
- API (back-end): `../api/`
- ADR-013: `../../.bequite/memory/decisions/ADR-013-studio-v2-architecture.md`
