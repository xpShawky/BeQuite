# BeQuite Studio API

> Hono-on-Bun HTTP back-end serving `studio/dashboard/`. Reads any BeQuite-managed project's filesystem (Memory Bank + state + receipts + cost ledger) and exposes it over HTTP so the dashboard (and future multi-user clients) can render without direct filesystem access.

**Current version: v0.20.0** (Bearer-token auth + append-only write surface + SSE event streams)

## Quickstart

```bash
cd studio/api
bun install
bun run src/index.ts
# → BeQuite Studio API v0.19.5 listening on http://localhost:3002
```

By default the API reads from `cwd/../..`, which means running from `studio/api/` it dogfoods the BeQuite repo itself.

## Auth modes

The API ships three auth modes, selected via `BEQUITE_AUTH_MODE`:

| Mode | When to use | Header required |
|---|---|---|
| `local-dev` (default) | Dashboard + API on the same machine. | none |
| `token` | Multi-agent dev or local-network access. | `Authorization: Bearer <token>` |
| `device-code` | Multi-user cloud (v0.20.0+). Auth server lands per ADR-011 Phase-3. | (server-issued JWT) |

Every response includes `X-BeQuite-Auth-Mode` so the dashboard can warn the user if it's talking to an unauthenticated local-dev API by accident.

### Bootstrapping into token mode

```bash
# 1. Start in local-dev mode (no auth required)
BEQUITE_AUTH_MODE=local-dev bun run src/index.ts

# 2. Mint a token (in a separate terminal)
curl -X POST http://localhost:3002/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"label":"dashboard-local"}'
# → { "token": "<64-hex>", "id": "<8-hex>", ... }

# 3. Stop the server, restart in token mode
BEQUITE_AUTH_MODE=token bun run src/index.ts

# 4. Subsequent requests require Authorization: Bearer <token>
curl -H "Authorization: Bearer <64-hex>" \
  http://localhost:3002/api/v1/projects
```

Tokens are stored at `<workspace>/.bequite/.auth/tokens.json` as sha256 hashes; the raw token is only returned once by the mint call. The file is gitignored (`.bequite/.auth/` rule) and chmod'd 0600 best-effort.

## Endpoint surface

### Public (no auth required)

```
GET    /                                         — API metadata
GET    /healthz                                  — liveness + uptime
GET    /api/v1/auth/status                       — current mode + token count
POST   /api/v1/auth/token                        — mint a new token (local-dev/token only)
DELETE /api/v1/auth/token/:id                    — revoke a token by 8-char id
GET    /api/v1/auth/tokens                       — list tokens (no hashes)
```

### Authenticated — read

```
GET    /api/v1/projects                          — list discoverable projects under workspace root
GET    /api/v1/projects/snapshot?path=<abs-path> — full ProjectSnapshot
GET    /api/v1/receipts?path=<abs-path>          — receipts summary list
GET    /api/v1/receipts/:sha?path=<abs-path>     — full receipt JSON (sha = 8-64 hex prefix)
GET    /api/v1/snapshots/:version?path=<abs-path> — Memory Bank snapshots under prompts/v<N>/
```

### Authenticated — write (append-only)

```
POST   /api/v1/receipts?path=<abs-path>          — emit a receipt (idempotent on content-hash)
POST   /api/v1/snapshots?path=<abs-path>         — emit a Memory Bank snapshot (refuses overwrite)
```

### Authenticated — event streams (Server-Sent Events; v0.20.0)

```
GET    /api/v1/streams/all?path=<abs-path>       — combined firehose (all events)
GET    /api/v1/streams/receipts?path=<abs-path>  — receipt events only
GET    /api/v1/streams/cost?path=<abs-path>      — cost-ledger events only
GET    /api/v1/streams/phase?path=<abs-path>     — phase + activeContext events
```

Every stream sends a `hello` event on connect (with workspace_root + auth_mode + identity), then state-change events (`receipt` / `cost` / `phase` / `active_context`) as the underlying file watcher fires. Heartbeat every 30 seconds. Watcher errors arrive as `watcher_error` events so the client can surface "stream degraded" rather than silently going dark (Article VI honest reporting).

**EventSource auth.** Browser `EventSource` cannot send custom headers, so on `/api/v1/streams/*` only, the auth middleware also accepts `?token=<hex>` as a fallback to `Authorization: Bearer <hex>`. The query-param path is restricted to stream routes to narrow the URL-leak surface (logs, referrers).

```javascript
// Browser client (in token mode):
const es = new EventSource(
  `http://localhost:3002/api/v1/streams/all?token=${apiToken}`,
);
es.addEventListener("receipt", (e) => console.log("new receipt", e.data));
es.addEventListener("heartbeat", (e) => console.log("alive", e.data));
```

**Reference-counted file watcher.** Streams share one `fs.watch` per workspace under the hood — the first SSE subscriber starts the watcher, the last unsubscriber tears it down. Idle workspaces hold no watcher resources.

Both write endpoints return an `iron_law_x` block (Constitution v1.3.0, Article X) confirming the change is operationally complete:

```json
{
  "ok": true,
  "sha": "...",
  "iron_law_x": {
    "persisted_path": "/abs/path/to/file.json",
    "file_readable": true,
    "file_size_bytes": 1234,
    "file_sha256": "...",
    "api_route_alive": true,
    "attestation": "Operationally complete. ...",
    "caller_must": ["GET /api/v1/receipts/:sha to read back", "no service restart required"]
  }
}
```

No `DELETE` or `PUT` write endpoints. Article IV: "Never run destructive ops without an explicit ADR." Mutation of existing state requires emitting a new receipt with the old one's content-hash as `parent_receipt` (the chain pointer), not editing in place.

## Path-traversal guard

Every endpoint that accepts a `?path=` query validates the resolved path is under `BEQUITE_WORKSPACE_ROOT` (default: two-levels-up from cwd). Paths outside the workspace root return `403 path outside workspace root`.

## Stack

- **Hono on Bun** — smallest TS edge backend (Doctrine `default-web-saas` recommendation).
- **Zod** — input validation on every write + query (Doctrine Rule 11).
- **node:crypto** — sha256 + ed25519 + bearer-token entropy (no external auth lib for the MVP; Better-Auth integration per Doctrine Rule 9 lands when device-code mode stands up).

## Cross-references

- Marketing: `../marketing/`
- Dashboard: `../dashboard/` (consumes this API in HTTP-mode from v2.0.0-alpha.1 onward)
- ADR-011 (CLI Authentication): `../../.bequite/memory/decisions/ADR-011-cli-authentication.md`
- ADR-013 (Studio v2 architecture): `../../.bequite/memory/decisions/ADR-013-studio-v2-architecture.md`
- ADR-014 (Iron Law X — operational completeness): `../../.bequite/memory/decisions/ADR-014-iron-law-x-operational-completeness.md`
- ADR-015 (v0.19.5 auth + write surface): `../../.bequite/memory/decisions/ADR-015-studio-api-auth-and-write-surface.md`
- Doctrine `default-web-saas`: `../../skill/doctrines/default-web-saas.md`

## What's next

- **v0.20.5** — Bidirectional WebSocket terminal stream (xterm.js) for auto-mode. Needs node-pty + RoE gates (per Article IV) since it's the first endpoint that actually executes commands.
- **v0.20.x** — Better-Auth integration (per Doctrine Rule 9 + ADR-011 Phase-3 device-code).
- **v2.0.0-alpha.1** — dashboard `lib/projects.ts` swap from filesystem-mode to HTTP-mode against this API. (CANDIDATE shipped to main at commit `a35dbfc`; awaiting Ahmed's review for the major-version tag.)
- **v2.0.0** — Postgres mirror for multi-user / cloud operation; same endpoint surface.
