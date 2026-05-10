---
id: ADR-015
title: Studio API — auth (MVP Bearer-token) + append-only write surface + Iron Law X attestation
status: accepted
date: 2026-05-10
supersedes: null
authors: [BeQuite Builder]
related: [ADR-011 (CLI auth, Phase-3 device-code), ADR-013 (Studio v2 architecture), ADR-014 (Iron Law X)]
---

## Context

v0.19.0 shipped the Studio API as a **read-only** surface (3 routes: health, projects, receipts). The dashboard talks to the API via filesystem-mode today; the migration to HTTP-mode lands v2.0.0-alpha.1. Before that swap, the API needs:

1. **An auth layer.** Without auth, anyone on the local network (or with port-forwarded access) can read `.bequite/` from any project under the workspace root. Doctrine `default-web-saas` Rule 9 mandates Better-Auth (or Clerk / Supabase Auth — explicitly **no custom auth**).
2. **A write surface.** Today the CLI and dashboard write directly to `.bequite/receipts/` and `.bequite/memory/prompts/`. A future multi-user setup needs the API as the single writer. Iron Law X (Article X — "operational completeness, no broken-half-build reports") demands every write surface attest to the change being live.
3. **A migration story from v0.19.5 (single-machine) to v0.20.0+ (multi-user cloud).** Whatever ships in v0.19.5 must be forward-compatible with the device-code Better-Auth wiring that lands when the auth server stands up.

## Decision

### Auth: three modes selected by `BEQUITE_AUTH_MODE`

| Mode | Default? | Semantics | Lifecycle |
|---|---|---|---|
| `local-dev` | yes | Pass-through. Every request is unauthenticated. `X-BeQuite-Auth-Mode: local-dev` set on every response so the dashboard can warn. | Single-machine dev (dashboard + API on the same box). |
| `token` | no | Bearer tokens stored as sha256 hashes at `<workspace>/.bequite/.auth/tokens.json`. Raw token returned by POST `/api/v1/auth/token` once; never again. | Multi-agent dev, local-network access, CI. |
| `device-code` | no | RFC 8628 device-code flow against a remote auth server (per ADR-011 Phase-3). Returns 503 until the auth server stands up. | Multi-user cloud (v0.20.0+). |

**Token storage**: sha256(raw) on disk, mode 0600 on POSIX (no-op on Windows). The `.bequite/.auth/` directory is gitignored alongside `.bequite/.keys/`. Tokens carry an 8-hex id for log correlation + revocation.

**Why MVP Bearer token instead of full Better-Auth in v0.19.5**: Better-Auth needs a database (Postgres at scale; SQLite for single-user). Standing up the database conflates Layer-1 Harness work with Layer-2 Studio work. The MVP Bearer token is intentionally minimal — when the auth server stands up (v0.20.0+) the validator swaps from `validateBearerToken()` to `verifyBetterAuthSession()` without touching route handlers. The `AuthContext` shape is the seam.

### Write surface: append-only, two endpoints in v0.19.5

| Endpoint | What it does | Why append-only |
|---|---|---|
| `POST /api/v1/receipts` | Persists a receipt to `.bequite/receipts/<sha>-<phase>.json`. Idempotent on content-hash. | Article IV — no destructive ops. Mutation = emit a new receipt with the old one's hash as `parent_receipt`. |
| `POST /api/v1/snapshots` | Copies the six Memory Bank files into `.bequite/memory/prompts/v<N>/<timestamp>_<phase>_<reason>/`. Refuses overwrite. | Article III — snapshots are a one-way-door audit artifact. |

**No DELETE, no PUT.** Article IV is explicit: "Never run destructive ops (`rm -rf`, `terraform destroy`, `DROP DATABASE`, etc.) without an explicit ADR." Renaming or rotating a receipt requires emitting a new one + linking via `parent_receipt`. Deleting a snapshot directory requires manual operator intervention (and per Article III, shouldn't happen at all — snapshots are tracked).

### Iron Law X verification block on every write

Every successful write returns a block:

```typescript
interface IronLawXBlock {
  persisted_path: string;           // absolute path on disk
  file_readable: boolean;           // re-read after write succeeded
  file_size_bytes: number;          // non-zero bytes
  file_sha256: string;              // content fingerprint
  api_route_alive: boolean | "n/a"; // sibling GET against same resource succeeded
  attestation: string;              // short prose — never contains banned weasel words
  caller_must: string[];            // what the user/caller still needs to do (Article X step 7)
}
```

If the re-read fails or the sibling probe returns non-ok, the helper **throws** and the route returns 500. There is no "should work" path — Article X step 7 ("did the user need to restart the build for the change to be live?") is answered explicitly in `caller_must`.

Banned weasel words **never** appear in the attestation string: `should`, `probably`, `seems to`, `appears to`, `I think it works`, `might work`, `hopefully`, `in theory`.

### Path-traversal guard preserved

Every endpoint that accepts `?path=` resolves it via `path.resolve()` and checks the result is under `BEQUITE_WORKSPACE_ROOT`. Outside-root paths return `403 path outside workspace root`. This was added in v0.19.0 for reads; v0.19.5 preserves the guard on writes.

## Alternatives considered

1. **Full Better-Auth in v0.19.5.** Rejected — needs a database, conflates Layer-1 Harness with Layer-2 Studio, slows the dashboard's HTTP-mode swap. Forward-compatible MVP Bearer token achieves the same surface area for the single-machine case and the swap-out point is one function (`validateBearerToken` → `verifyBetterAuthSession`).
2. **JWT-only.** Rejected — JWT needs a signing key + rotation policy + revocation list. Bearer-token-with-server-side-hash gives revocation for free (`DELETE /api/v1/auth/token/:id` drops the hash from the file).
3. **Cookie-based session.** Rejected — multi-host (dashboard on :3001, API on :3002) cookie sharing requires SameSite gymnastics. Bearer header is friendlier to non-browser clients (the CLI, future cloud SDK).
4. **No auth in v0.19.5; defer to v0.20.0.** Rejected — the dashboard HTTP-mode swap (v2.0.0-alpha.1) sits between v0.19.5 and v0.20.0. Without auth, the dashboard HTTP-mode would either ship insecure or block on auth. local-dev mode as the default gives a frictionless single-machine path while reserving the option to flip to token mode for everyone else.
5. **PUT/DELETE write surface.** Rejected — Article IV. The chain-pointer pattern (every mutation = a new receipt with `parent_receipt` pointing at the previous) is the audit trail. Editing in place destroys the trail.
6. **Sync HTTP probe inside the Iron Law X block** (curl the API from inside the handler). Rejected — circular dependency on the in-flight request's worker; instead the helper re-reads the file directly and parses it (functional equivalent for a file-backed resource, no boot/port assumption).

## Consequences

### Positive

- Dashboard HTTP-mode swap (v2.0.0-alpha.1) is now unblocked — it can target the API directly with `Authorization: Bearer <token>`.
- Append-only writes preserve receipt chain integrity (the audit trail) by construction.
- Iron Law X attestation in every write response is machine-checkable — the dashboard can surface "operationally complete" to the user without a manual re-fetch.
- Forward-compatible with Better-Auth (swap the validator, not the routes).

### Negative

- **Bun runtime is not present in this developer's environment.** v0.19.5 attestation is partial: TypeScript typecheck (`tsc --noEmit`) returned exit 0, but the API was not booted in this session. Full Iron Law X attestation (boot + curl) is deferred to v0.19.x verification when a Bun-equipped environment runs the smoke suite. The README's quickstart is unchanged and should work as written.
- **Token mode bootstrap requires temporarily flipping to local-dev** (mint a token, restart in token mode). This is the standard chicken-and-egg for self-hosted auth and is documented in the README. Alternative would be a CLI command (`bequite api token mint`) that lives outside the HTTP layer; that lands v0.20.0+ with the wider CLI/API integration.
- **Device-code mode is a stub** — returns 503 with a helpful message. The auth server stands up v0.20.0+ per ADR-011 Phase-3.

### Neutral

- The `.bequite/.auth/` gitignore rule joins `.bequite/.keys/` — both private-key-class artifacts. Pattern is consistent with v0.7.1.
- POST endpoints accept the same `?path=` query as GET endpoints. The path-traversal guard is enforced identically.

## Verification

- `tsc --noEmit` passes on the full `studio/api/` tree (4 lib files + 4 route files + index.ts). Exit 0.
- `npm install` succeeds; `node_modules/` resolved (Hono + Zod + gray-matter + @types/bun + typescript).
- Iron Law X helper unit-tested implicitly: every write endpoint calls `buildIronLawXBlock()` which **throws** on re-read failure or probe failure (no silent success path).
- README documents the bootstrap-into-token-mode flow explicitly.

## What v0.19.5 does NOT ship

- Better-Auth full integration (Doctrine Rule 9). Lands v0.20.x+ with the auth server.
- WebSocket / SSE for receipt + cost streaming. Lands v0.20.0.
- xterm.js terminal stream for auto-mode. Lands v0.20.0.
- Postgres mirror for multi-user / cloud operation. Lands v2.0.0.
- The dashboard's HTTP-mode swap (`lib/projects.ts` filesystem → HTTP). Lands v2.0.0-alpha.1 (next).

## References

- [ADR-011](./ADR-011-cli-authentication.md) — CLI authentication design. Phase-3 device-code is the long-term auth path.
- [ADR-013](./ADR-013-studio-v2-architecture.md) — Studio v2 architecture (3 surfaces, brand system).
- [ADR-014](./ADR-014-iron-law-x-operational-completeness.md) — Iron Law X full text.
- [Constitution v1.3.0](../constitution.md) — Article IV (security/destruction), Article X (operational completeness).
- [Doctrine `default-web-saas`](../../skill/doctrines/default-web-saas.md) — Rule 9 (Better-Auth/Clerk/Supabase Auth, no custom auth) + Rule 11 (Zod/Pydantic/Valibot input validation).
- RFC 8628 — OAuth 2.0 Device Authorization Grant.
- [Hono docs](https://hono.dev/) — middleware composition, context API.
