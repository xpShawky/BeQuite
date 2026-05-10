# BeQuite API (placeholder — full impl v0.19.0+)

> Hono-on-Bun API serving both `studio/marketing/` (CMS-ish content) and `studio/dashboard/` (project + receipt + state data).

## Stack (planned for v0.19.0+)

- **Hono on Bun** — smallest TS edge backend (Doctrine Rule).
- **Zod** for input validation everywhere (Doctrine Rule 11).
- **Better-Auth** for authentication (per ADR-011).
- **Postgres (Supabase)** for project metadata + receipt mirrors when v2.0.0 cloud features stand up.
- **Drizzle ORM** with deny-by-default RLS.

## Endpoint surface (planned)

```
GET  /healthz                           — liveness
GET  /api/v1/me                         — current user (authenticated)
GET  /api/v1/projects                   — projects user can access
GET  /api/v1/projects/:id               — project metadata
GET  /api/v1/projects/:id/state         — operational state (state/recovery.md, etc.)
GET  /api/v1/projects/:id/memory/*      — Memory Bank files
GET  /api/v1/projects/:id/receipts      — receipt list
GET  /api/v1/projects/:id/receipts/:sha — single receipt JSON
GET  /api/v1/projects/:id/cost          — session-cost roll-up
POST /api/v1/projects/:id/cli/:command  — invoke CLI command (auth + RoE-bound)
WS   /api/v1/projects/:id/stream        — live xterm.js stream + heartbeat
```

## Status

**v0.16.0 ships this README + directory only.** Real API lands per the v0.19.0 row in the master roadmap.

## Cross-references

- Marketing: `../marketing/`
- Dashboard: `../dashboard/`
- ADR-011 (Auth): `../../.bequite/memory/decisions/ADR-011-cli-authentication.md`
- ADR-013 (Studio architecture): `../../.bequite/memory/decisions/ADR-013-studio-v2-architecture.md`
- Doctrine `default-web-saas`: `../../skill/doctrines/default-web-saas.md`
