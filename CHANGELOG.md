# Changelog

All notable changes to BeQuite are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Conventional Commits](https://www.conventionalcommits.org/). Versioning is [Semantic Versioning](https://semver.org/).

## [Unreleased] — tracking toward v1.0.0 + v2.0.0-alpha.1

v0.20.0 ships the **SSE event-stream layer** — Server-Sent Events for live receipt / cost / phase / activeContext updates from `studio/api/` to `studio/dashboard/`, with reference-counted file watchers, 30-second heartbeats, and a `LiveIndicator` client component that triggers throttled `router.refresh()` on state-change events. The dashboard now reflects state changes without manual page reload (Iron Law X step 7 = "no" by construction).

**v2.0.0-alpha.1 candidate** still on main at `a35dbfc` — dashboard dual-mode loader (filesystem ↔ HTTP). Awaiting Ahmed's explicit go/no-go on the major-version tag.

v0.17.5 (3D astronaut GLB) still parked — Blender MCP unresponsive. v0.20.5 next: bidirectional WebSocket terminal stream for auto-mode (xterm.js + node-pty + RoE gates per Article IV — first endpoint that actually executes commands). Ahmed reviews before tagging v1.0.0 (Layer 1 Harness final) + v2.0.0-alpha.1 (Studio Edition first pre-release).

---

## [0.20.0] — 2026-05-10

### Added — SSE event streams (live dashboard updates)

**API side (`studio/api/`):**

- **`src/lib/event-bus.ts`** — Per-workspace pub/sub with reference counting. First subscribe lazily starts a filesystem watcher; last unsubscribe tears it down. Idle workspaces hold no watcher resources.
- **`src/lib/file-watcher.ts`** — `WorkspaceWatcher` watches four paths and publishes events:
  - `.bequite/receipts/` — new `*.json` file → `receipt` event
  - `.bequite/cache/cost-ledger.json` — content change → `cost` event
  - `.bequite/memory/activeContext.md` — content change → `active_context` event
  - `state/current_phase.md` — content change → `phase` event
  - 250ms coalesce window per channel (Windows fs.watch fires twice per change)
  - Watch errors emit `watcher_error` events so the dashboard can surface "stream degraded" rather than silently going dark (Article VI).
- **`src/routes/streams.ts`** — Four SSE endpoints under `/api/v1/streams/`:
  - `GET /api/v1/streams/all` — combined firehose
  - `GET /api/v1/streams/receipts` — `receipt` events only
  - `GET /api/v1/streams/cost` — `cost` events only
  - `GET /api/v1/streams/phase` — `phase` + `active_context` events
  - All gated by `authMiddleware`; path-traversal guard preserved.
  - 30-second heartbeat keeps proxy connections alive + lets the client detect a dead stream.
  - Initial `hello` event includes workspace_root + auth_mode + identity + filter + server_version.
  - Client disconnect handled via `stream.onAbort` — clean watcher unsubscribe, no orphan watchers.
- **`src/lib/auth.ts`** — Auth middleware extended to accept `?token=<hex>` as a fallback to `Authorization: Bearer <hex>` **only on `/api/v1/streams/*`**. Browser EventSource cannot send custom headers; the query-param path is restricted to stream routes to narrow the URL-leak surface.

**Dashboard side (`studio/dashboard/`):**

- **`lib/streams.ts`** — `openStream()` client wrapper. Reconnects on transient failure (exponential backoff, 1s → 30s cap). Tracks last heartbeat; emits `onStale` when no heartbeat in 60s. Exposes `disconnect()` + `status()`.
- **`components/LiveIndicator.tsx`** — Client component (`"use client"`). Top-right of the TopBar. Shows `LIVE` / `CONNECTING` / `STALE` / `OFFLINE` / `FS` pill. On `receipt` / `cost` / `phase` / `active_context` events, triggers a throttled `router.refresh()` (default: 2s throttle) so the server-component re-render reflects new state. Heartbeat / hello events skipped (they're noise).
- **`components/TopBar.tsx`** — Now accepts `loaderMode`, `apiBase`, `workspacePath` props and renders `<LiveIndicator />` next to the AGENT ONLINE indicator.
- **`app/page.tsx`** — Passes loader config + workspace path through to TopBar.
- **`lib/projects-types.ts`** — Added `StreamEventName` + `BusEvent` types (mirrors API's bus events; kept in sync by convention).

### Changed

- `cli/bequite/__init__.py::__version__` → `0.20.0`. `cli/pyproject.toml::version` → `0.20.0`.
- `studio/api/package.json::version` → `0.20.0`. Description updated.
- `studio/api/src/routes/health.ts::version` → `0.20.0`.
- `studio/api/src/index.ts::version` → `0.20.0`. Endpoint catalog adds `authenticated_streams` group.
- `studio/dashboard/package.json::version` → `0.20.0`.

### Notes

- API + dashboard both **typecheck clean** (`tsc --noEmit` exit 0 on both). Live boot smoke deferred to Ahmed's review (Bun runtime not installed in this developer's env; would need `bun run src/index.ts` + `BEQUITE_DASHBOARD_MODE=http pnpm dev` + a real receipt write to fire the event end-to-end).
- **No new Iron Law.** v0.20.0 implements Article X step 7 ("did the user need to refresh?") at the dashboard layer — answer is now "no, the LiveIndicator triggered router.refresh() automatically."
- **No bidirectional WebSocket in v0.20.0** — that lands v0.20.5. WS for the terminal needs node-pty (running real shells) + RoE gates per Article IV (first endpoint that executes user-supplied commands; explicit ADR required). Not appropriate to fold into the SSE-only release.
- **EventSource auth caveat.** The `?token=<hex>` query-param fallback is restricted to `/api/v1/streams/*` and documented in `studio/api/README.md` § "EventSource auth." Production-grade alternative (signed short-lived cookie + refresh token) lands with Better-Auth integration in v0.20.x+.

### v2.0.0-alpha.1 candidate (still on main, not tagged)

`a35dbfc` — dashboard dual-mode loader (filesystem ↔ HTTP). Per the standing commitment ("Ahmed reviews before tagging v1.0.0 + v2.0.0-alpha.1"), the major-version tag remains explicitly Ahmed's decision. The work integrates cleanly with v0.20.0's LiveIndicator (which only activates in HTTP mode anyway).

---

---

## [0.19.5] — 2026-05-10

### Added — Studio API auth layer + append-only write surface (per ADR-015)

**Auth (three modes selected by `BEQUITE_AUTH_MODE`):**

- `local-dev` (default) — pass-through. `X-BeQuite-Auth-Mode` response header surfaces the mode so the dashboard can warn.
- `token` — Bearer tokens stored as sha256 hashes at `<workspace>/.bequite/.auth/tokens.json` (gitignored; chmod 0600 best-effort). Raw token returned by `POST /api/v1/auth/token` once; never again.
- `device-code` — RFC 8628 stub returning 503 until the auth server stands up v0.20.0+ per ADR-011 Phase-3.

**New auth endpoints:**

- `GET /api/v1/auth/status` — current mode + identity + token count.
- `POST /api/v1/auth/token` — mint a fresh token (returns raw token + 8-char id once).
- `DELETE /api/v1/auth/token/:id` — revoke by 8-char id.
- `GET /api/v1/auth/tokens` — list tokens (no hashes).

**New write endpoints (append-only per Article IV):**

- `POST /api/v1/receipts?path=<abs-path>` — persists a Zod-validated receipt to `.bequite/receipts/<sha>-<phase>.json`. Idempotent on content-hash. Returns `iron_law_x` block.
- `POST /api/v1/snapshots?path=<abs-path>` — copies the six Memory Bank files into `.bequite/memory/prompts/v<N>/<timestamp>_<phase>_<reason>/`. Refuses overwrite (409 with retry-with-bumped-timestamp guidance). Returns `iron_law_x` block.
- `GET /api/v1/snapshots/:version?path=<abs-path>` — list snapshots under that version.

**Iron Law X attestation block (Constitution v1.3.0, Article X):** Every successful write returns:

```typescript
{
  persisted_path: string,        // absolute path
  file_readable: boolean,        // re-read after write
  file_size_bytes: number,
  file_sha256: string,           // content fingerprint
  api_route_alive: boolean | "n/a", // sibling probe
  attestation: string,           // never contains banned weasel words
  caller_must: string[],         // Article X step 7
}
```

If the re-read fails or the sibling probe returns non-ok, the helper **throws** and the route returns 500. No "should work" path.

**Files added in v0.19.5:**

- `studio/api/src/lib/auth.ts` — Hono middleware + token store + sha256 hashing + mint/revoke/list.
- `studio/api/src/lib/iron-law-x.ts` — `buildIronLawXBlock()` verification helper with banned-weasel-word enforcement.
- `studio/api/src/routes/auth.ts` — status + mint + revoke + list endpoints.
- `studio/api/src/routes/snapshots.ts` — POST snapshot + GET list.
- `studio/api/src/routes/receipts.ts` — extended with POST (append-only) on top of v0.19.0 reads.
- `studio/api/src/index.ts` — wires middleware mount at `/api/v1/projects/*`, `/api/v1/receipts/*`, `/api/v1/snapshots/*`. Auth routes mount publicly at `/api/v1/auth/*`. Exposes `X-BeQuite-Auth-Mode` via CORS.
- `studio/api/README.md` — full v0.19.5 surface documented + bootstrap-into-token-mode flow.
- `.bequite/memory/decisions/ADR-015-studio-api-auth-and-write-surface.md` — full decision record.

**Critical Article VI fix shipped in this release:**

The `.gitignore` rule `lib/` (line 27, intended for Python venv install dirs) was over-broad and silently dropped:

- `studio/marketing/lib/docs.ts` from the v0.17.0 commit
- `studio/dashboard/lib/projects.ts` from the v0.18.0 commit
- `studio/api/src/lib/fs-loader.ts` from the v0.19.0 commit

All three published tags shipped Studio apps that would not boot from a fresh clone (Next.js compile error / Hono module-not-found). The CHANGELOG entries falsely claimed "boots locally" — true on the developer's disk where the files were present, false for GitHub clones. The v0.19.5 release:

1. Anchors Python venv install dirs to repo root in `.gitignore` (`lib/` → `/lib/`, `lib64/` → `/lib64/`, `build/` → `/build/`, etc.). Application source dirs named `lib/` are no longer matched.
2. Stages and commits all three previously-silently-ignored files (they exist on disk in their fully-functional shape; recovery is additive).
3. Adds `.bequite/.auth/` to gitignore alongside `.bequite/.keys/`.

v0.19.0 tag was force-updated to include the recovery. v0.17.0 + v0.18.0 tags remain at their historical (broken) commits — main + v0.19.0+ is the recommended pointer.

### Changed

- `cli/bequite/__init__.py::__version__` → `0.19.5`. `cli/pyproject.toml::version` → `0.19.5`.
- `studio/api/package.json::version` → `0.19.5`. Description updated to mention auth + write surface.

### Notes

- API **typechecks clean** in this release (`cd studio/api && npx tsc --noEmit` → exit 0). Full Iron Law X attestation (boot + curl) is deferred to v0.19.x verification — Bun runtime is not installed in this developer's environment, so the live-boot smoke could not be performed in-session. The README's quickstart (`bun install && bun run src/index.ts`) is unchanged.
- **No new Iron Law.** v0.19.5 implements Article X (added in v0.16.0 via Constitution v1.3.0) at the HTTP layer.
- **No Better-Auth in v0.19.5.** Doctrine Rule 9 (Better-Auth / Clerk / Supabase Auth — no custom auth) is forward-compatible: the MVP Bearer validator swaps for Better-Auth session verification without touching route handlers. Full integration lands v0.20.x+.
- v0.20.0 — WebSocket for live receipt + cost stream + xterm.js terminal stream.
- v2.0.0-alpha.1 — swap dashboard `lib/projects.ts` from filesystem-mode to HTTP-mode against `studio/api/`.

---

## [0.19.0] — 2026-05-10

### Added — Studio API back-end (Hono on Bun)

**`studio/api/` is now a working HTTP service** that boots on http://localhost:3002 and reads any BeQuite-managed project at a configurable path. Same loader logic as the dashboard (`studio/dashboard/lib/projects.ts`), but exposed over HTTP so future multi-user / cloud / non-Node clients can read project state without filesystem access.

- **`src/index.ts`** — Hono app with `logger()` + permissive dev CORS (`http://localhost:*` + `http://127.0.0.1:*` allowed in dev; production allow-list lands v0.19.x+) + route registration. Boots via `bun run src/index.ts` on port `process.env.PORT || 3002`.
- **`src/schemas.ts`** — Zod schemas for `PhaseStatus`, `ReceiptSummary`, `ProjectSnapshot`, plus `ProjectQuerySchema` for path-bounded queries. Mirrors the dashboard `ProjectSnapshot` interface so future HTTP-mode swap is type-safe.
- **`src/lib/fs-loader.ts`** — Filesystem-backed `loadProject(rootDir)` + `listProjects()` + `getWorkspaceRoot()`. **Path-traversal guard:** `BEQUITE_WORKSPACE_ROOT` env (defaults to two-levels-up from cwd) is the allow-list root; any `?path=` outside the root returns 403 (`path outside workspace root`). Reads constitution.md, projectbrief.md, activeContext.md, state/current_phase.md, state/recovery.md, `.bequite/receipts/*.json`, `.bequite/cache/cost-ledger.json`.
- **`src/routes/health.ts`** — `GET /healthz` → `{ status, service, version, workspace_root, uptime_s }`.
- **`src/routes/projects.ts`** — `GET /api/v1/projects` (list discoverable projects under workspace root) + `GET /api/v1/projects/snapshot?path=<abs-path>` (full snapshot for a project; Zod-validated query).
- **`src/routes/receipts.ts`** — `GET /api/v1/receipts?path=<abs-path>` (last receipts summary list; sorted newest-first) + `GET /api/v1/receipts/:sha?path=<abs-path>` (full receipt content by 8-64-hex content-hash prefix; Zod-validated sha format).
- **`package.json`** — Hono 4 + Zod 3; runs on Bun (`bun --hot src/index.ts`). TypeScript strict; `tsconfig.json` uses NodeNext modules.
- **`README.md`** — endpoint surface + env vars + dev quickstart.

### Endpoint surface

| Verb | Path | Returns |
|---|---|---|
| `GET` | `/healthz` | `{ status, service, version, workspace_root, uptime_s }` |
| `GET` | `/` | API metadata + endpoint catalog |
| `GET` | `/api/v1/projects` | `{ items: [{ name, path }, ...] }` |
| `GET` | `/api/v1/projects/snapshot?path=<abs-path>` | full `ProjectSnapshot` (constitution version, current phase, last green tag, doctrines, receipts summary, cost session, recovery preview) |
| `GET` | `/api/v1/receipts?path=<abs-path>` | last receipts list per project |
| `GET` | `/api/v1/receipts/:sha?path=<abs-path>` | full receipt JSON for a single sha-prefixed receipt |

### Changed

- `cli/bequite/__init__.py::__version__` → `0.19.0`. `cli/pyproject.toml::version` → `0.19.0`.

### Notes

- API **boots locally**: `cd studio/api && bun install && bun run src/index.ts` → http://localhost:3002. By default `BEQUITE_WORKSPACE_ROOT` is `cwd/../..` so when run from `studio/api/`, the BeQuite repo itself is the readable root.
- v0.19.0 ships **read-only endpoints only**. v0.19.5 adds: auth (Better-Auth per Doctrine Rule 9; ADR-011 Phase-3 device-code flow when standing up the auth server) + write endpoints with RoE gates (per Article IV — no destructive ops without explicit ADR).
- v2.0.0-alpha.1 swaps the dashboard's `lib/projects.ts` from filesystem-mode to HTTP-mode against `studio/api/`. v2.0.0+ adds a Postgres mirror for multi-user / cloud operation.
- WebSocket for live receipt + cost stream + xterm.js terminal stream lands v0.20.0.
- v0.17.5 (3D astronaut GLB via Blender) still parked — `localhost:9876` went from timeout to `Cannot connect`. Scaffold ready (`studio/marketing/public/3d/` + `AgentCharacter3D.tsx` drop-in API); the moment Blender's MCP responds, v0.17.5 is one iteration away.

---

## [0.18.0] — 2026-05-10

### Added — Studio dashboard real implementation (per image 6 mock)

**`studio/dashboard/` is now a working Next.js 15 app** that boots on http://localhost:3001 and reads the BeQuite repo itself (or any BeQuite-managed project at a configurable path):

- **`app/page.tsx`** — composes the full operations console: TopBar + PhasesSidebar + center main + AgentPanel (right). Server-component reads project state via `lib/projects.ts::loadProject()` on every request.
- **`components/TopBar.tsx`** — logo + workspace/project breadcrumbs + AGENT ONLINE indicator with pulsing gold dot.
- **`components/PhasesSidebar.tsx`** — P0..P7 phase list with status icons (Check / Loader / Circle / AlertOctagon) + DEV STATUS block + DEPLOY button.
- **`components/CommandConsole.tsx`** — terminal-mock with gold prompt arrow + ✓ output styling + blinking cursor.
- **`components/PlanTasksTests.tsx`** — 3-panel grid (Plan / Tasks / Tests).
- **`components/AgentPanel.tsx`** — right-side astronaut character + status indicator + activeContext summary + recent activity log.
- **`components/ReceiptsList.tsx`** — last 10 receipts with ed25519 signature badges + cost + timestamp.
- **`lib/projects.ts`** — filesystem-based project loader. Reads `constitution.md`, `projectbrief.md`, `activeContext.md`, `state/current_phase.md`, `state/recovery.md`, `.bequite/receipts/*.json`, `.bequite/cache/cost-ledger.json`. Returns a `ProjectSnapshot`.
- **`package.json`** — Next.js 15 + React 19 + Tailwind v4 + Framer Motion 11 + TanStack Query 5 + gray-matter + Lucide icons.

### Changed

- `cli/bequite/__init__.py::__version__` → `0.18.0`. `cli/pyproject.toml::version` → `0.18.0`.
- `studio/dashboard/README.md` — rewritten from placeholder to working-app docs.

### Notes

- Dashboard **boots locally**: `cd studio/dashboard && pnpm install && pnpm dev` → http://localhost:3001. By default it loads the BeQuite repo from `../..` and shows real receipts, real phases, real Constitution version, real cost ledger.
- v0.17.5 (3D character) still parked — Blender MCP went from timeout to `Cannot connect`.
- v0.18.5 will add live xterm.js terminal streaming.
- v0.19.0 swaps filesystem-mode for HTTP-to-`studio/api/`. v0.19.0+ adds auth (per ADR-011 Phase-3 device-code).

---

## [0.17.0] — 2026-05-10

### Added — Vibecoder tutorials + docs route + cinematic primitives

**6 deep MDX tutorials** at `studio/marketing/content/docs/`:

- **`quickstart.mdx`** (~250 lines) — zero to first verified feature in 10 minutes. No prior CLI experience required. Install → init → multi-model planning → implement → verify → first signed receipt.
- **`from-scratch.mdx`** (~290 lines) — complete worked example (salon-bookings). All seven phases with realistic time + cost expectations + what-you-avoided-by-discipline.
- **`retrofit.mdx`** (~270 lines) — installing BeQuite into an existing project. Survey → init `--retrofit` → audit → freshness → small feature → gradual Doctrine adoption. Common retrofit pain points table.
- **`multi-model-planning.mdx`** (~290 lines) — making Claude + ChatGPT think together via manual-paste mode (ToS-clean). 5 collaboration modes (Parallel / Specialist / Debate / Judge / Red-Team). Cost expectations.
- **`auto-mode.mdx`** (~270 lines) — one-click P0 → P7. 8 safety rails. CLI flags. Heartbeat. Resume. Idempotency. Parallel-task fan-out. Recovery runbook.
- **`troubleshooting.mdx`** (~280 lines) — vibecoder pain points + recovery. "command not found" / hooks blocking / weasel words / Iron Law X failures / verify red gates / undo last change / stuck auto-mode / lost session / multi-model paste fatigue.

**Docs route in Next.js App Router:**

- `studio/marketing/lib/docs.ts` — reads MDX from `content/docs/`, parses frontmatter via `gray-matter`.
- `studio/marketing/app/docs/layout.tsx` — sticky sidebar + content area.
- `studio/marketing/app/docs/page.tsx` — index card grid.
- `studio/marketing/app/docs/[slug]/page.tsx` — per-tutorial page using `<MDXRemote>` with brand-styled components (gold links, ink-stage code blocks, silver text, prev/next navigation footer).
- `studio/marketing/components/DocsSidebar.tsx` — sticky left sidebar with active-link highlight.

**Cinematic primitives:**

- `studio/marketing/components/Chapter.tsx` — pinned-scroll chapter wrapper using `useScroll` + `MotionValue<number>` render-prop pattern (Apple's macbook-pro frame-by-frame style, drop-in 3D-ready).
- `studio/marketing/components/three/Starfield.tsx` — R3F particle starfield (800 gold motes drifting through 3D space). Respects `prefers-reduced-motion: reduce`.

**Nav update:** "Docs" link added; "Get started" CTA → `/docs/quickstart`.

### Changed

- `cli/bequite/__init__.py::__version__` → `0.17.0`. `cli/pyproject.toml::version` → `0.17.0`.
- `studio/marketing/package.json` adds `next-mdx-remote ^5.0.0` + `gray-matter ^4.0.3`.

### Notes

- Marketing site **boots locally** with docs route working: `cd studio/marketing && pnpm install && pnpm dev` → http://localhost:3000/docs.
- v0.17.5 (3D astronaut GLB via Blender pipeline) **deferred** — Blender's MCP add-on at `localhost:9876` is accepting the TCP connection but the Python addon isn't responding (timeout, not refused). The Studio scaffold is 3D-ready (R3F + drei installed; `Chapter` primitive accepts a 3D scene drop-in) — the moment Blender's MCP becomes responsive, v0.17.5 is a single iteration away.
- Combined integration suite still 125/125 (Layer-1 Python tests; the marketing site's own test suite lands v0.17.x+).

---

## [0.16.0] — 2026-05-10

### Added — Studio Edition Phase-1 + Constitution v1.3.0

- **ADR-013** (`.bequite/memory/decisions/ADR-013-studio-v2-architecture.md`) — Studio v2.0.0 architecture: 3 surfaces (`studio/marketing/` Next.js cinematic landing + `studio/dashboard/` Next.js operations console + `studio/api/` Hono-on-Bun back-end) sharing one brand system. 3D-ready scaffold (R3F + drei installed) so Blender pipeline integrates without restructuring.
- **ADR-014** (`.bequite/memory/decisions/ADR-014-iron-law-x-operational-completeness.md`) — **Iron Law X — Operational completeness**. The "restart-the-build" rule. Bumps Constitution to v1.3.0. 7 operational steps every change must satisfy + 6 banned report patterns + mandatory self-attestation block.
- **Constitution v1.3.0** (`.bequite/memory/constitution.md`) — Article X added (full text). Default-model bump documented (Opus 4.7 with `reasoning_effort: xhigh` for orchestrator + Skeptic + multi-model judge + reviewer roles). Specs-numbered-folders convention noted (`specs/001-feature-slug/`, `specs/002-other/`, etc. — Spec-Kit-aligned).
- **`studio/brand/`** — Brand system foundation:
  - `tokens.css` (~180 lines) — gold + black palette (`--gold-primary: #E5B547`, `--gold-bright`, `--gold-deep`, `--black-pure`, `--black-stage`, `--black-velvet`, silver/white scale) + Apple-inspired type scale (Geist + Geist Mono) + cinematic motion easings (never bouncy per Doctrine Rule 6) + reduced-motion handling.
  - `tokens.json` — machine-readable equivalent (Design Tokens Format).
  - `README.md` — usage rules, type, motion, asset table.
  - `ATTRIBUTION.md` — Ahmed's brand assets + third-party (Geist, Inter, Tailwind).
  - `raw/` — 6 ranked source PNGs (hero zen + character zen + character pointing + hero wordmark + horizontal logo + dashboard mock).
- **`studio/marketing/`** — Apple-grade cinematic landing site (Next.js 15 + Tailwind v4 + Framer Motion 11 + R3F-ready):
  - `package.json` + `tsconfig.json` + `next.config.ts` + `postcss.config.mjs` + `tailwind.config.ts`.
  - `app/layout.tsx` (root + metadata + viewport).
  - `app/page.tsx` (composes 6 sections).
  - `app/globals.css` (imports brand tokens + Tailwind v4 theme).
  - `components/Nav.tsx` — scroll-aware nav with backdrop-blur transition.
  - `components/Hero.tsx` — pinned cinematic hero (Apple-style; `useScroll` + `useTransform` driving scale + opacity).
  - `components/PhasesScroll.tsx` — 7-phase scroll-driven reveal (each phase activates as user scrolls; opacity/x/scale transforms per phase index).
  - `components/Features.tsx` — 6-feature card grid with hover gold glints.
  - `components/Demo.tsx` — terminal-mock CLI walkthrough beside the pointing astronaut.
  - `components/CTA.tsx` — final call-to-action with gradient + radial-gold glow.
  - `components/Footer.tsx` — three-column footer.
  - `components/AgentCharacter.tsx` — astronaut with breathing-idle motion (drop-in 3D upgrade-ready).
  - `public/brand/` — 6 brand PNGs copied for Next.js Image.
- **`studio/dashboard/`** — README + directory only (full impl v0.18.0+ per ADR-013). Visual target: image 6 mock.
- **`studio/api/`** — README + directory only (full impl v0.19.0+).
- **`studio/README.md`** — Studio overview + roadmap table.
- **Default model bump** — `skill/routing.json` orchestrator + product-owner reasoning_effort: high → **xhigh** (per Constitution v1.3.0).

### Changed

- Versions bumped to `0.16.0`.
- Constitution v1.2.0 → v1.3.0.

### Notes

- Combined integration suite still 125/125 (v0.16.0 is architecture + brand + marketing scaffold; no new test modules — the marketing app's own test suite lands v0.17.x+).
- The marketing site **boots locally**: `cd studio/marketing && pnpm install && pnpm dev`.
- **Honest scope per Article VI:** v0.16.0 ships the Apple-grade foundation. Frame-by-frame video reveals + GLB-loaded 3D character + R3F particle starfield + MDX vibecoder tutorials all land v0.17.0+ (subsequent commits build cinematic chapters on top of this scaffold).
- Constitution Article X (Iron Law X) is **Iron Law text only** in this commit. Hook extension + posttooluse-operational-check.sh + auto-mode integration land v0.16.x+.

---

## [0.15.0] — 2026-05-10

### Added — Release engineering

- **`.github/workflows/ci.yml`** — five-job pipeline runs on every push + PR + manual: (1) **lint** (ruff + mypy advisory), (2) **test** matrix across Python 3.11/3.12/3.13/3.14 running all 12 integration test files (125+ tests total), (3) **audit** (`bequite audit` + `bequite freshness` self-check; eat-our-own-food), (4) **license-audit** (osv-scanner advisory), (5) **pr-summary** comments PR with status grid.
- **`.github/workflows/release.yml`** — fires on tag `v*.*.*`. Three jobs: (1) **validate** (tag matches `cli/pyproject.toml::version` + full integration suite green), (2) **publish-pypi** via PyPI Trusted Publisher OIDC (no long-lived secrets), (3) **publish-github** (extracts release notes from CHANGELOG between `## [VERSION]` markers; creates GitHub Release with attached LICENSE + CHANGELOG). npm thin shell job present but `if: false` (gated until Ahmed provisions npm account).
- **`.github/workflows/commitlint.yml`** — enforces Conventional Commits on every PR via `@commitlint/config-conventional`.
- **`.commitlintrc.json`** — Conventional Commits rules.

### Changed

- Versions bumped to `0.15.0` (the last sub-version before v1.0.0).

### Notes

- Combined integration suite still 125/125 (v0.15.0 is CI-pipeline only; no new application code).
- Ahmed reviews everything before the final v1.0.0 tag.
- One-way doors that auto-mode never auto-runs (per Constitution Article IV): PyPI publish, npm publish, git push to main, force push, terraform apply, DB migrations against shared DBs. release.yml requires a human-pushed tag to fire.

---

## [0.14.0] — 2026-05-10

### Added — Documentation (8 docs + 2 templates)

- **`docs/README.md`** — navigation for the documentation tree.
- **`docs/QUICKSTART.md`** — 5-minute path from zero to working project.
- **`docs/HOW-IT-WORKS.md`** — architecture overview. Two-layer (Harness + Studio). Seven phases. Iron Laws. 13 Doctrines. 14 hooks. Receipts. Multi-model. CLI auth. Auto-mode.
- **`docs/DOCTRINE-AUTHORING.md`** — fork or write a new Doctrine.
- **`docs/HOSTS.md`** — per-host install + behavior notes for 9 hosts.
- **`docs/AUTONOMOUS-MODE.md`** — auto-mode CLI flags + state machine + 8 safety rails + heartbeat + idempotency + recovery runbook.
- **`docs/SECURITY.md`** — threat model + OWASP Web Top 10 + OWASP LLM Top 10 (2025) coverage + Article IX cybersecurity + Doctrine vibe-defense + vulnerability reporting.
- **`docs/MAINTAINER.md`** — release process + PyPI account ownership + npm thin shell + ed25519 signing keys + license audit + contributor checklist.
- **`template/HANDOFF.md.tpl`** — engineer + non-engineer handoff template.

### Changed

- Versions bumped to `0.14.0`.

### Notes

- Combined integration suite still 125/125 (v0.14.0 is docs-only).

---

## [0.13.0] — 2026-05-10

### Added — Vibe-handoff exporters (spec-kit-zip + claude-code-skill)

- **`cli/bequite/exporters.py`** (~165 lines) — Two export formats: `spec-kit-zip` (specs/ + .bequite/memory/ + AGENTS.md + CLAUDE.md → zip with manifest) and `claude-code-skill` (skill/ + AGENTS.md + CLAUDE.md → zip with manifest). JSON-frontmatter validation for spec.md (feature/version/status) / plan.md (feature/scale_tier/stack_decided) / tasks.md (feature/phase/task_count) / phases.md (feature/phase_count). CLI: `python -m bequite.exporters {validate,spec-kit-zip,claude-skill}`.
- **`tests/integration/exporters/test_exporters_smoke.py`** — 8 tests: frontmatter parsing / validation complete + missing keys + unknown-filename / spec-kit-zip creates valid zip with manifest + included files / claude-skill creates valid zip / required-frontmatter-keys complete. **All 8 pass.**

### Changed

- Versions bumped to `0.13.0`.

### Notes

- Combined integration suite: 117 + 8 = **125/125 tests green** on Python 3.14.

---

## [0.12.0] — 2026-05-10

### Added — Per-host adapters (universal entry + 9 hosts)

- **`template/AGENTS.md.tpl`** — Linux Foundation Agentic AI Foundation universal entry for fresh `bequite init` projects. References Constitution + Memory Bank + state/recovery + active Doctrines + banned weasel words + per-host extension table.
- **`template/.cursor/rules/bequite-constitution.mdc.tpl`** — Cursor-specific rules file with `alwaysApply: true` + Iron Laws summary + required reads.
- **`cli/bequite/skill_install.py`** (~125 lines) — host detection + per-host config installer. 9 supported hosts: `claude-code` (CLAUDE.md), `cursor` (.cursor/rules/), `codex` (.codex/AGENTS.md), `cline` (.clinerules/), `kilo` (.kilocode/), `continue` (.continuerules/), `aider` (.aider/AGENTS.md), `windsurf` (.windsurf/cascades/), `gemini` (.gemini/memory.md). CLI: `python -m bequite.skill_install detect` (probes which hosts are present) + `install [--host <name>]` (writes config; idempotent).
- **`tests/integration/skill_install/test_skill_install_smoke.py`** — 9 tests covering host registry / detect for each host / install creates file / install idempotent / unknown host raises / content includes banned-words. **All 9 pass.**

### Changed

- Versions bumped to `0.12.0`.

### Notes

- Combined integration suite: 108 + 9 = **117/117 tests green** on Python 3.14.

---

## [0.11.0] — 2026-05-10

### Added — MENA bilingual Doctrine + RTL walkthrough

- **`skill/doctrines/mena-bilingual.md`** — Doctrine v1.0.0 with 11 binding rules: locale-binding declared in project.yaml; `dir="rtl"` for ar-* locales; logical properties only (no hardcoded left/right); Arabic-friendly font stack with recorded reason (Tajawal / Cairo / Readex Pro / Noto Sans Arabic / IBM Plex Sans Arabic — all OFL-licensed); slightly-larger body type + more leading for Arabic legibility; bilingual string extraction (no inline ternaries on user-facing strings); Egyptian dialect preserved by default in research outputs (no auto-normalization to Modern Standard); RTL Playwright walks for every UI feature; mirrored icons + arrows; Intl.NumberFormat / DateTimeFormat per locale; Skeptic kill-shot for MENA UX. Stack guidance: i18n libraries (next-intl / i18next / lingui), Arabic font foundries, MENA-specific data sources for Researcher persona.
- **`skill/templates/tests/walkthroughs/rtl-walk.md.tpl`** — 7 RTL flows (locale switch / mirrored navigation / form input at 360 RTL / tabular data + sorting / modal + toast positioning / search + filter chips / empty states + onboarding). Negative paths: mixed-direction text + mixed-language form validation + URL with locale switch.
- **Forking guidance** for `mena-bilingual-saudi` (ar-SA + Hijri default), `mena-bilingual-uae` (ar-AE + DIFC layered), `mena-bilingual-mghreb` (Maghreb + Berber/French).

### Changed

- Versions bumped to `0.11.0`.
- Doctrine count: 12 → 13 (mena-bilingual was previously deferred to v0.11.0; now shipped).
- Tokens template (`skill/templates/tokens.css.tpl`) already shipped `[dir="rtl"]` block since v0.6.1; no change required.

### Notes

- Combined integration suite still 108/108 (v0.11.0 is a Doctrine + walkthrough release; no new code modules).

---

## [0.10.7] — 2026-05-10

### Added — Auto-mode hardening (resume + parallel + idempotent)

- **`cli/bequite/auto_state.py`** (~110 lines) — `list_sessions` / `can_resume` / `resume_session` (clears BLOCKED+PAUSED markers, resets failure counter, advances to next phase). `should_split_parallel` + `fan_out_parallel` (per AkitaOnRails 2026 N>5 threshold; respects `depends_on`). `is_phase_idempotent_rerun` + `detect_double_commit` (same-feature in-flight session detection).
- **`tests/integration/auto/test_auto_state_smoke.py`** — 13 tests covering empty session list / saved sessions / resume valid+invalid states / parallel threshold + dependency-blocking / idempotent rerun / double-commit detection. **All 13 pass.**

### Changed

- Versions bumped to `0.10.7`.

### Notes

- Combined integration suite: 95 + 13 = **108/108 tests green** on Python 3.14.
- Phase-5 (Auto + new feature impls) closes here. Next: phase-6 (MENA + host adapters).

---

## [0.10.6] — 2026-05-10

### Added — CLI Authentication Phase-2 (stubs that gracefully degrade) per ADR-011

- **`cli/bequite/auth.py`** (~190 lines) — LocalIdentity dataclass + get/save/delete + status_dict + offline-mode + ci-mode detection. CLI: `python -m bequite.auth {login,logout,whoami,status,refresh}`. Phase-2 ships local-file identity (UUID at `.bequite/.identity.json`); Phase-3 device-code RFC 8628 flow lands v0.11.x+ when auth server stands up.
- **CI mode** detected via `BEQUITE_API_KEY` or `BEQUITE_CI_MODE=true` — login skips device-code flow.
- **Offline mode** via `BEQUITE_OFFLINE=true` — auth-required commands suppress.
- **`tests/integration/auth/test_auth_smoke.py`** — 8 tests covering identity roundtrip / unauthenticated state / authenticated state / offline + CI mode env handling / UUID generation. **All 8 pass.**

### Changed

- Versions bumped to `0.10.6`.

### Notes

- Combined integration suite: 87 + 8 = **95/95 tests green** on Python 3.14.

---

## [0.10.5] — 2026-05-10

### Added — Multi-Model Planning (manual-paste working) per ADR-012

- **`cli/bequite/multi_model.py`** (~310 lines) — `scaffold_run` (creates `docs/planning_runs/RUN-<datetime>/`), `render_plan_prompt` (per-model role-flavored prompt with brief + doctrines + Constitution version), `render_judge_prompt`, `parse_plan_sections` (coarse keyword-based section extraction), `compare_plans` (per-section agreement / risk / per-model recommendation), `render_comparison_md`, `render_final_plan`. CLI: `python -m bequite.multi_model {scaffold,compare,merge}`.
- **`cli/bequite/providers/manual_paste.py`** — ManualPasteProvider conforming to v0.8.0 AiProvider Protocol. `complete()` writes prompt to file + polls for response (sync) or returns `awaiting_user` (async). `is_available()` always True; cost always $0 (subscription human-cost, not API).
- **`tests/integration/multi_model/test_multi_model_smoke.py`** — 12 tests: prompt rendering / section parsing / agreement detection (all-mention vs all-omitted) / comparison.md generation / final_plan generation with user_decisions / scaffold_run tree / ManualPasteProvider Protocol conformance / async-mode awaiting / judge prompt / token estimation / slug normalization. **All 12 pass.**

### Changed

- `cli/bequite/__init__.py::__version__` → `0.10.5`. `cli/pyproject.toml::version` → `0.10.5`.

### Notes

- v0.10.5 implements ADR-012 §Part 1 (manual-paste MVP). Direct-API mode lands v0.11.x+ (reuses v0.8.0 router).
- Combined integration suite: 75 + 12 = **87/87 tests green** on Python 3.14.

---

## [0.10.0] — 2026-05-10

### Added — Auto-mode state machine + safety rails + heartbeat

- **`cli/bequite/auto.py`** (~270 lines) — state machine with 8 phases (P0..P7) + DONE/BLOCKED/FAILED/PAUSED. State persistence at `.bequite/auto-state/<session>.json`. Per-phase rail checks: cost ceiling, wall-clock ceiling, banned-words, consecutive-failure threshold. One-way-door pattern detection (PyPI/npm/git-push-main/terraform). Heartbeat writes activeContext.md every 5 minutes during long phases. CLI: `python -m bequite.auto run --feature X --max-cost-usd 20 --max-wall-clock-hours 6 --mode auto`.
- **In v0.10.0 the actual model invocation is stubbed** (no-op completing each phase with a synthetic message). v0.10.5 will integrate multi-model planning at P2; v0.11.x+ wires real LLM calls per the v0.8.0 routing matrix.
- **`tests/integration/auto/test_auto_smoke.py`** — 11 tests covering state roundtrip, all 4 rail checks, run_phase / run_all_phases, banned-word blocking, cost-ceiling blocking, transition bookkeeping. **All 11 pass.**

### Changed

- `cli/bequite/__init__.py::__version__` → `0.10.0`. `cli/pyproject.toml::version` → `0.10.0`.

### Notes

- Combined integration suite: 64 + 11 = **75/75 tests green** on Python 3.14.
- Phase-5 (Auto-mode + new feature impls) begins here. Next: v0.10.5 (multi-model manual-paste working).

---

## [0.9.2] — 2026-05-10

### Added — Phase-1 architecture docs for two new feature modules

Per Ahmed's explicit "add two major features to BeQuite" prompt: (1) CLI authentication (browser-based / device-code login, NOT API key as primary), and (2) Multi-Model Planning where models like ChatGPT 5.5 + Claude Opus 4.7 think together before implementation. **Phase-1 (this release) is docs-only** per Ahmed's instruction. Implementation lands v0.10.5+ (multi-model) and v0.10.6+ (CLI auth).

#### Decision records (ADRs)

- **`.bequite/memory/decisions/ADR-011-cli-authentication.md`** — CLI authentication. Recommended MVP: **device-code login (RFC 8628)** because it works headless / SSH / Docker / CI, and supports phone-completion. Browser-OAuth-callback deferred to v0.12.x+ (when BeQuite-cloud auth server stands up). Magic-link rejected as MVP (slowest UX). Token storage via Python `keyring` package (OS keychain on macOS / Windows / Linux). Session refresh / logout / offline-mode / CI-mode (`BEQUITE_API_KEY` separate from human login) all designed. Threat model + 7 failure-state recovery paths documented. **No new Iron Law** — extends Article IV.
- **`.bequite/memory/decisions/ADR-012-multi-model-planning.md`** — Multi-Model Planning. Recommended MVP: **manual-paste mode** (ToS-clean; works with Claude Pro + ChatGPT Plus subscriptions immediately; zero provider auth complexity). Direct-API mode lands v0.11.x+ reusing v0.8.0 provider adapters. **Browser-session reuse of consumer subscriptions explicitly NOT recommended** (Anthropic + OpenAI ToS prohibit driving endpoints from non-API session cookies; brittle to UI changes; rate-limit + detection-fingerprinting risk). 5 collaboration modes (Parallel default + Specialist + Debate + Judge + Red-Team). 12 roles (Lead Architect / Product Strategist / Frontend / Backend / Database / Security Reviewer / Testing / DevOps / UX / Scraping / Cost Optimizer / Final Judge). Conflict resolution: Iron Law beats Doctrine beats freshness beats user-pick. Storage at `docs/planning_runs/RUN-<datetime>/`. **No new Iron Law** — fulfills Articles I + VI + VII.

#### Architecture strategy docs

- **`docs/architecture/CLI_AUTHENTICATION_STRATEGY.md`** (~480 lines) — full operational reference: 3-option comparison table, Mermaid sequence diagram for device-code flow, polling rules with RFC 8628 backoff, secure local token storage strategy (per-OS backend + headless-Linux fallback with mode 0600 file), token shape, read-path code sketch, session refresh strategy, logout (single-device + all-devices), offline-mode rules, CI-mode rules, threat model with 7 mitigations, 6 failure states with recovery paths, test plan, CLI command surface, TUI panel design (color-coded green/yellow/red).
- **`docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md`** (~510 lines) — full operational reference: why multi-model planning exists (3 single-model failure modes), MVP manual-paste workflow with 6-step sequence, future direct-API mode, **explicit non-recommendation of browser-session reuse with reasoning**, ManualPasteProvider Python sketch (conforms to v0.8.0 AiProvider Protocol), 12-role table with default-model assignments, 5 collaboration modes (each with best-for / mode mechanics), plan merge algorithm (8 steps), 5-priority conflict resolution rules, comparison-table schema, model-contribution log shape, token saving strategy, 6 failure scenarios, security/privacy concerns, cost concerns ($0 manual-paste / $0.05-$0.30 direct-API per run), 3 example workflows.

#### Specifications

- **`docs/specs/MULTI_MODEL_PLANNING_REQUIREMENTS.md`** (~370 lines) — F-1 through F-10 functional requirements + NFR-1 through NFR-5 non-functional + CLI surface table + slash-command table + run-directory data model + run-state JSON shape + state-file layout + 13 prompt-template list + acceptance criteria for v0.10.5 ship + 5 deferred questions with default decisions. Defines exactly what v0.10.5 must implement.

#### New personas (3 — total persona count → 20)

- **`skill/agents/multi-model-planning-orchestrator.md`** — owns the per-run lifecycle (scaffold → independent drafting → compare → merge → confirm). 8 hard rules (independence-first / per-model prompts / no silent failures / Iron Law beats / Doctrine beats / freshness beats / user picks final / receipts-per-call). Anti-patterns + Skeptic kill-shot for own behavior.
- **`skill/agents/model-judge.md`** — final synthesizer in Judge mode. 6 hard rules (read all peer plans / explain rejections / never invent / mark user-decision points / Article VI honest reporting / no silent confirmations). Decision-format template with Skeptic kill-shot per topic. **Mandatory self-attestation block** at end of `merge_report.md`.
- **`skill/agents/red-team-reviewer.md`** — adversarial post-plan review. 8 attack angles (security / architecture / testing / deployment / scalability / UX / token-waste / hidden-assumptions). Severity-tagged findings (block / warn / nit). Auto-loaded when Doctrine `vibe-defense` is active.

#### Master-doc updates

- **`CLAUDE.md`** — added 3 new persona names to the "you must act like" list; added 6 new path entries to the quick-reference table.
- **`AGENTS.md`** — added 5 new path entries (multi-model runs / strategy / requirements / CLI auth strategy / both ADRs).
- **`.bequite/memory/constitution.md`** — preamble updated with v0.9.2 line documenting both ADRs accepted Phase-1 docs-only with no new Iron Law (operational frameworks fulfilling existing Articles).
- **`.bequite/memory/activeContext.md`** — modules 12 + 13 added (CLI auth + multi-model planning architectures); persona count 17 → 20; next-actions reshaped.
- **`.bequite/memory/progress.md`** — v0.9.2 row tagged ✅; v0.10.5 + v0.10.6 + v0.10.7 inserted; old v0.10.1 renumbered to v0.10.7; evolution log entry.
- **`state/recovery.md`** — pickup instructions for v0.10.0 (auto-mode unchanged) + v0.10.5 (multi-model) + v0.10.6 (CLI auth) + v0.10.7 (auto-hardening).
- **`state/current_phase.md`** — phase-4 complete + phase-5 upcoming.

### Changed

- `cli/bequite/__init__.py::__version__` → `0.9.2`.
- `cli/pyproject.toml::version` → `0.9.2`.
- Roadmap to v1.0.0: 9 sub-versions remaining (was 7; +v0.10.5 + v0.10.6 for new feature modules).

### Notes

- This release is **Phase-1 docs only** per Ahmed's "Implementation order: Phase 1: Docs and architecture only." instruction. No code changes (other than version bumps).
- Default decisions baked in (Ahmed can amend via ADR later — these don't block):
  - **CLI auth MVP = device-code login** (works in SSH / Docker / CI; phone-completion).
  - **Multi-model MVP = manual-paste mode** (ToS-clean, works with subscriptions today).
  - **Browser-session reuse of consumer subscriptions = NOT recommended** (ToS + brittleness; reasoned in ADR-012 §Part 3 + strategy doc §3).
  - **Default planning mode = Parallel** (independence preserved; Debate + Judge + Red-Team modes available via `--mode`).
  - **Default judge model = Claude Opus 4.7** (configurable per project).
  - **Token storage = Python `keyring` package** (OS keychain on macOS/Windows/Linux; gitignored file fallback for headless Linux).
- Implementation order per Ahmed: Phase 1 (docs — DONE) → Phase 2 (CLI command stubs — v0.10.5/v0.10.6) → Phase 3 (manual-paste workflow working — v0.10.5) → Phase 4 (auth prototype — v0.10.6+) → Phase 5 (direct provider adapters — v0.11.x+).

---

## [0.9.1] — 2026-05-10

### Added — E2E test harness + CI workflow

- **`tests/integration/e2e/test_seven_phase_walk.py`** — 8-test e2e smoke suite that drives the BeQuite CLI surface:
  1. `--version` reports correctly (0.9.x).
  2. `--help` lists the 24 core commands (7-phase + BeQuite-unique + receipts + routing + economics).
  3. `bequite doctor` runs without crash (returncode < 2).
  4. `bequite route show` resolves a known (phase, persona) pair to claude-sonnet-4-6.
  5. `bequite pricing list` shows fallback table.
  6. `bequite receipts list` returns empty when no receipts dir.
  7. `bequite verify-receipts` errors correctly (exit 2) without keypair.
  8. `bequite keygen` creates per-project keypair; subsequent `verify-receipts` succeeds.
  - Subprocess invocations inherit parent env (so click + dependencies resolve from the test runner's site-packages); UTF-8 encoded with `errors="replace"` for Windows compatibility.
- **`tests/integration/e2e/test_doctrine_loading.py`** — 8-test e2e suite for Doctrine structural invariants:
  1. `skill/doctrines/` exists.
  2. All 12 expected Doctrines on disk + non-empty.
  3. Each Doctrine has a YAML frontmatter block (between two `---` markers within first 30 lines).
  4. Each Doctrine declares required fields: `name:`, `version:`, `applies_to:`, `supersedes:`.
  5. Each Doctrine's `name:` matches its filename.
  6. Each Doctrine has a Rules section (tolerant of "Rules" / "Common rules" / "Strict rules" naming).
  7. `default-web-saas` Doctrine is at v1.1.0 (verifies v0.6.1 bump preserved).
  8. Each Doctrine has a Changelog or Status marker.
- **`.github/workflows/examples-e2e.yml`** — three-job GitHub Actions workflow:
  1. **`python-suite`** — runs the full integration suite across Python 3.11 / 3.12 / 3.13 / 3.14 matrix. Six test files = 64 tests total.
  2. **`example-scaffolds`** — verifies each example has README + ADR + (example 1 only) HANDOFF + spec + phases.
  3. **`audit-self`** — runs `bequite audit` against the BeQuite repo (eats its own food); runs `bequite freshness` self-help.
  4. **`pr-comment`** — comments PR-thread with green/red summary on completion.
  - Triggers: every push to main, every PR to main, nightly cron 04:00 UTC, manual workflow_dispatch.

### Combined integration suite

**64/64 tests green on Python 3.14** across 6 modules:
- `test_receipts_smoke.py`: 10 tests
- `test_signing_smoke.py`: 9 tests
- `test_router_smoke.py`: 15 tests
- `test_pricing_smoke.py`: 14 tests
- `test_seven_phase_walk.py`: 8 tests (new)
- `test_doctrine_loading.py`: 8 tests (new)

### Changed

- `cli/bequite/__init__.py::__version__` → `0.9.1`.
- `cli/pyproject.toml::version` → `0.9.1`.

### Notes

- The auto-mode e2e test (`test_auto_mode.test.ts` per the build plan §4 v0.9.1 row) is **deferred to v0.10.0** since auto-mode itself lands there. v0.9.1 ships the parts that don't depend on auto-mode (CLI surface checks + Doctrine structural invariants).
- The plan §4 specified TypeScript test files; honest reality is Python aligns better with the project (CLI is Python). Both paths are acceptable per the plan; we chose Python for consistency.
- Phase-4 (Examples + e2e harness) is now complete: v0.9.0 + v0.9.1 done. Phase-5 (Auto-mode + MENA) begins with v0.10.0.

---

## [0.9.0] — 2026-05-10

### Added — Three example projects (scaffolded + spec'd)

- **`examples/README.md`** — entry point + forking guidance.
- **`examples/01-bookings-saas/`** (Doctrine: `default-web-saas`):
  - `README.md` — what was built / how to run / phases.
  - `.bequite/memory/decisions/ADR-001-stack.md` — full stack ADR (Next.js + Hono + Supabase + Better-Auth + Vercel + Zod + TanStack + Playwright + axe; per-rule Doctrine compliance check).
  - `specs/bookings-flow/spec.md` — 4 flows (sign-up + book / admin availability / admin dashboard / tenant invite); non-goals; constraints; Skeptic kill-shot ("concurrent-booking race condition").
  - `specs/bookings-flow/phases.md` — phase-1 through phase-7 decomposition with exit gates + per-phase Skeptic kill-shots.
  - `HANDOFF.md` — engineer + non-engineer ("vibe-handoff") sections; how to run locally + deploy + add a feature; risk register; cost estimate ($45-90/mo at 5k MAU); Skeptic kill-shot for the handoff itself.
- **`examples/02-ai-tool-wrapper/`** (Doctrine: `cli-tool`):
  - `README.md` — `mdsum` CLI summarizes Markdown via Claude. Stack table + per-phase walkthrough inline + cost-per-invocation analysis.
  - `.bequite/memory/decisions/ADR-001-stack.md` — Python 3.11+ / hatchling / click / rich / httpx / anthropic SDK; reuses BeQuite's `cli/bequite/providers/` adapters; full per-rule Doctrine compliance.
- **`examples/03-tauri-note-app/`** (Doctrine: `desktop-tauri`):
  - `README.md` — `vault-notes` local-first encrypted note app. Tauri v2 + SvelteKit + SQLite + AES-GCM + OS keychain. Per-phase walkthrough inline.
  - `.bequite/memory/decisions/ADR-001-stack.md` — full stack ADR with brief reconciliations baked in (NOT Stronghold; NOT altool; NOT EV cert; NOT relic; per BeQuite v0.1.0 brief verification). Codesigning matrix (notarytool macOS + AzureSignTool Windows). Risk register includes AKV cert 1-yr cap.

### What v0.9.0 explicitly does not ship

Per Article VI honest reporting: production-quality code for each example is **not** in this commit. Each example ships:
- The `.bequite/` tree shape (proves the harness scaffolds correctly).
- A defensible stack ADR per Doctrine.
- A seven-phase walkthrough document.
- A HANDOFF (engineer + vibe-handoff sections, for example 1; README-as-handoff for examples 2 + 3).

The code walkthroughs land via v0.9.1's e2e harness (which drives `bequite auto` on each example) and downstream example iterations post-v1.0.0. **Three full Production apps in one autonomous commit would not be honest.**

### Changed

- `cli/bequite/__init__.py::__version__` → `0.9.0`.
- `cli/pyproject.toml::version` → `0.9.0`.

### Notes

- All three examples cross-reference: parent BeQuite repo, Doctrine, frontend-stack reference (where relevant), and the v0.7.0+v0.7.1 receipts/signing system that they will use post-implementation.
- Phase-4 of the master plan (Examples + e2e harness) begins here; v0.9.1 closes it.

---

## [0.8.1] — 2026-05-10

### Added — Live pricing fetch (best-effort)

- **`cli/bequite/pricing.py`** (~330 lines) — vendor pricing fetch + cache + fallback:
  - **Cache** at `.bequite/cache/pricing.json`; default 24h TTL; canonical-JSON encoded.
  - **`fetch_pricing(provider=None)`** — best-effort GET on each vendor's pricing page (Anthropic / OpenAI / Google / DeepSeek). Returns partial dict on parse failure (rather than raising).
  - **`extract_prices_from_html(html)`** — coarse regex extraction. Pairs nearest model + 2 prices in the same paragraph. Hardly perfect but better than nothing; flags missing extraction so the cache stays incomplete-but-honest rather than silently wrong.
  - **`pricing_for(model)`** — returns `(rates, source)` where source ∈ {"live", "stale", "fallback", "unknown"}. Prefers fresh cache → stale cache (with warning) → vendored hard-coded fallback → unknown.
  - **`estimate_cost_usd(model, input_tokens, output_tokens)`** — one-call helper used by provider adapters. Returns `(usd, source)`.
  - **CLI** at `python -m bequite.pricing {refresh,show,list}`.
- **`skill/references/pricing-table.md`** — vendored May-2026 pricing snapshot covering 5 providers + hosting (Vercel / Cloudflare / Render / Fly / Railway) + auth (Clerk / Auth0 / Better-Auth) + database (Supabase / Neon / Convex). Used as fallback when both cache and live fetch fail. Marked stale on use.
- **Provider adapters updated** (`cli/bequite/providers/{anthropic,openai,google,deepseek}.py`):
  - `estimate_cost_usd()` now consults `pricing.pricing_for()` first; falls back to module-level hard-coded table if pricing module unimportable or model unknown.
  - Soft-import: adapters remain usable without `pricing.py` (graceful degradation per the v0.8.0 contract).
- **CLI surface additions** in `cli/bequite/__main__.py`:
  - `bequite pricing show <model>` — current rate + source for a model.
  - `bequite pricing list` — all known models with cache + fallback rates.
  - `bequite pricing refresh [--provider <p>]` — best-effort live fetch + cache update.
- **14-test integration suite at `tests/integration/pricing/test_pricing_smoke.py`**:
  1. fallback_pricing for 4 known models across 4 providers.
  2. fallback_pricing returns None for unknown.
  3. pricing_for falls back when cache empty.
  4. pricing_for unknown model returns "unknown".
  5. pricing_for uses fresh cache (live source).
  6. pricing_for marks stale when cache > TTL.
  7. pricing_for unknown-in-cache falls back to fallback table.
  8. estimate_cost_usd uses pricing_for (1M opus = $22.50 round-trip).
  9. estimate_cost_usd unknown returns 0.
  10. cache_age_hours missing/invalid returns +inf.
  11. is_cache_fresh under TTL.
  12. is_cache_fresh over TTL.
  13. extract_prices_from_html finds paired model+prices.
  14. AnthropicProvider.estimate_cost_usd consults pricing module.
  - All 14 pass on Python 3.14.
  - **Combined integration suite: 48/48 green** (10 receipts + 9 signing + 15 router + 14 pricing).

### Changed

- `cli/bequite/__init__.py::__version__` → `0.8.1`.
- `cli/pyproject.toml::version` → `0.8.1`.

### Notes

- Live fetch + extract is intentionally conservative. WebFetch + regex extraction is brittle for pricing pages; v0.8.1 ships the **infrastructure** (cache shape, fallback path, adapter wiring). Live extraction degrades gracefully to "fallback (stale)" when a vendor restructures its pricing page.
- The vendored `skill/references/pricing-table.md` is the fallback's fallback. When both cache and live fetch are unavailable, this file is the source of truth — flagged `stale=True`.
- Article VI honest reporting: every cache entry carries `source` so users always know whether they're looking at live, stale, or fallback data.

---

## [0.8.0] — 2026-05-10

### Added — Multi-model routing (cost-aware)

- **`cli/bequite/providers/`** — 5 vendor adapters + Protocol + Completion dataclass:
  - `__init__.py` — `AiProvider` Protocol (`is_available`, `supports_model`, `estimate_cost_usd`, `complete`); `Completion` dataclass (text, input_tokens, output_tokens, finish_reason, model, provider, usd_cost, raw_response, error); `get_provider(name)` factory + `REGISTERED_PROVIDERS` tuple.
  - `anthropic.py` — Claude family via `anthropic` SDK; pricing for `claude-opus-4-7` ($15/$75 per 1M), `claude-sonnet-4-6` ($3/$15), `claude-haiku-4-5` ($0.80/$4); reasoning-effort passed via system-prompt prefix.
  - `openai.py` — GPT-5 / o3 family via `openai` SDK; pricing for `gpt-5` ($12/$50), `gpt-5-mini` ($0.50/$2), `o3` ($10/$40); reusable as base for DeepSeek (OpenAI-compatible API).
  - `google.py` — Gemini via `google-genai` SDK (the `bequite[google]` extra); pricing for `gemini-2.5-pro` ($1.25/$10), `gemini-2.5-flash` ($0.30/$2.50).
  - `deepseek.py` — Subclasses OpenAIProvider; `base_url=https://api.deepseek.com/v1`; pricing for `deepseek-chat`/`deepseek-coder` ($0.27/$1.10), `deepseek-reasoner` ($0.55/$2.19).
  - `ollama.py` — HTTP localhost (`http://localhost:11434`) via `httpx`; **no vendor SDK required**; cost always $0.00 (local compute); availability probed via `/api/tags`.
  - **Graceful degradation:** every adapter is importable WITHOUT its vendor SDK — `is_available()` returns False instead of raising. The router uses this to fall back without crashing.
- **`cli/bequite/router.py`** — selects (provider, model, effort) per (phase, persona):
  - `Route` dataclass (phase, persona, model, reasoning_effort, fallback_model, max_input_tokens, max_output_tokens, provider, used_fallback, note).
  - `_provider_for_model()` heuristic: `claude-*` → anthropic; `gpt-*`/`o3*`/`o4*` → openai; `gemini-*` → google; `deepseek-*` → deepseek; `llama|mistral|qwen|phi|gemma` → ollama; else → ollama.
  - `find_routing_path()` — searches `.bequite/routing-overrides.json` then `skill/routing.json` (project-local override possible).
  - `select_route()` — match priority: exact (phase, persona) → (persona, special-phase: any/any-boundary/always-on/any-mode) → (phase, orchestrator) → orchestrator catch-all.
  - `dispatch()` — runs primary; on unavailable, tries `fallback_model` (auto-resolves provider from model name); calls `cost_ledger.update()` on every call.
- **`cli/bequite/cost_ledger.py`** — feeds `.bequite/cache/cost-ledger.json` so the existing `stop-cost-budget.sh` hook (v0.3.0) actually has data to enforce against:
  - `update()` — appends call to ledger; refreshes `session_total_usd` + `session_total_tokens` + `calls_this_session`. Per-process session_id auto-resets totals on session change.
  - `read()` — full ledger dict.
  - `session_summary()` — one-screen current-session summary.
  - `reset_session()` — clears session totals (keeps call history).
- **CLI surface additions** in `cli/bequite/__main__.py`:
  - `bequite route show --phase <P> --persona <X>` — JSON of resolved route.
  - `bequite route list` — every row in routing.json (table format).
  - `bequite route providers` — availability probe per provider (SDK + API key check).
  - `bequite ledger show` — current session summary.
  - `bequite ledger reset` — reset session totals.
- **15-test integration suite at `tests/integration/router/test_router_smoke.py`**:
  1. provider registry complete (5 providers).
  2. each provider implements Protocol (4 methods).
  3. provider-for-model heuristics (8 model names).
  4. select_route exact match (P5 backend-engineer → claude-sonnet-4-6).
  5. select_route reviewer uses Opus xhigh (Aider architect-mode pattern).
  6. select_route skeptic via any-boundary special phase.
  7. select_route unknown falls back to orchestrator.
  8. anthropic pricing estimates (3 model tiers).
  9. openai pricing estimates.
  10. dispatch with TestProvider returns Completion + Route.
  11. dispatch falls back when primary unavailable.
  12. dispatch returns error when both unavailable.
  13. cost_ledger accumulates across calls (totals + count).
  14. cost_ledger session_summary surface.
  15. dispatch updates ledger when enabled.
  - All 15 pass on Python 3.14.
  - **Total integration suite: 34/34 green** (10 receipts + 9 signing + 15 router).

### Changed

- `cli/bequite/__init__.py::__version__` → `0.8.0`.
- `cli/pyproject.toml::version` → `0.8.0`. Description updated to "multi-model routing (Anthropic + OpenAI + Google + DeepSeek + Ollama with cost-aware fallback)".

### Notes

- The `routing.json` schema in `skill/routing.json` was authored in v0.2.0 with the right shape; v0.8.0 makes it operational by wiring the provider adapters + dispatch path.
- AkitaOnRails 2026 finding (forced multi-model on coupled tasks loses to solo frontier) is preserved: routing routes Skeptic to `any-boundary` and reviewer to Opus-xhigh on Aider architect-mode pattern, but implementation stays single-frontier per-task.
- The `stop-cost-budget.sh` hook (shipped v0.3.0) reads `.bequite/cache/cost-ledger.json::session_total_usd`. Now that the ledger is populated, ceiling enforcement is operational.
- TestProvider injection (`provider_factory` arg on `dispatch()`) keeps the suite hermetic — no network, no API keys required.
- Receipt emission per model invocation is cleanly separable from the dispatch path: the router updates the ledger; receipts (v0.7.0+v0.7.1 schema) get emitted by the auto-mode driver in v0.10.0 when phase boundaries fire.

---

## [0.7.1] — 2026-05-10

### Added — Signed receipts (ed25519)

- **`cli/bequite/receipts_signing.py`** — ed25519 sign-and-verify layer on top of v0.7.0 receipts.
  - **`generate_keypair(project_dir, overwrite=False)`** — creates per-project keypair using `cryptography.hazmat.primitives.asymmetric.ed25519`. Private key at `<project>/.bequite/.keys/private.pem` (mode 0600 best-effort on POSIX; gitignored). Public key at `<project>/.bequite/keys/public.pem` (mode 0644; committed). Refuses to overwrite by default; `overwrite=True` regenerates with explicit warning that previous receipt signatures become invalid.
  - **`load_private_key(path)` / `load_public_key(path)`** — typed PEM loaders. `cryptography` raises if the file isn't actually an Ed25519 key.
  - **`sign_dict(receipt_dict, private_key)`** — returns a copy with `signature` (base64-encoded ed25519) added. Signs over canonical-JSON of receipt *with the signature field absent or null* — sidesteps the chicken-and-egg of "signing a receipt that contains its own signature."
  - **`verify_dict(receipt_dict, public_key)`** — recovers the signature, recomputes canonical-JSON-without-signature, verifies. Returns `(ok, reason)` with helpful error messages.
  - **`verify_receipts_directory(receipts_dir, public_key, strict)`** — walks every `*.json` in `.bequite/receipts/`. Returns `(ok, issues, counts)` where counts has total / signed_valid / signed_invalid / unsigned. In `strict=True`, unsigned receipts contribute to `issues`; in `strict=False`, they're tolerated (legacy v0.7.0 receipts pass).
  - CLI: `python -m bequite.receipts_signing {keygen,sign,verify}`.
- **`Receipt` schema additive bump** — optional `signature: Optional[str] = None` field (last position; backward-compatible). v0.7.0 unsigned receipts still load + emit + roll-up unchanged.
- **`ReceiptStore.write(receipt, sign_with=None)`** — when `sign_with` is an `Ed25519PrivateKey`, the on-disk JSON includes the `signature` field. Filename remains the v0.7.0 deterministic-from-inputs hash so the chain pointer stays stable across re-signings (e.g. after key rotation).
- **`bequite verify-receipts`** Click command (`cli/bequite/__main__.py`):
  - Loads `.bequite/keys/public.pem`; refuses to run if missing (suggests `bequite init` or `bequite keygen`).
  - Verifies signatures via `verify_receipts_directory` with optional `--strict`.
  - Validates chain via existing `validate_chain` (missing-parent + causality + cycles).
  - Exits 0 on full pass, 1 on any failure.
- **`bequite keygen`** Click command — direct keypair generation; explains gitignore + commit obligations.
- **`bequite init` extension** — auto-calls `generate_keypair` (catching FileExistsError for re-init); appends `.bequite/.keys/` patterns to project's `.gitignore` (additive; defends against template drift). Init summary now shows keypair status.
- **9-test integration suite at `tests/integration/receipts/test_signing_smoke.py`** — keygen creates files / refuses overwrite / overwrites when explicit; sign-verify roundtrip; tampered-body rejected; unsigned-strict-fails; unsigned-lenient-tolerated; ReceiptStore.write(sign_with=...) emits signed receipts; cross-paste-signature mismatch detected. All 9 pass on Python 3.14.

### Changed

- `cli/bequite/__init__.py::__version__` → `0.7.1`.
- `cli/pyproject.toml::version` → `0.7.1`. Description updated to "ed25519-signed" (no longer "in v0.7.1+").

### Notes

- The repo's existing root `.gitignore` already had `.bequite/.keys/` from v0.1.0+; the v0.7.1 init code is the belt-and-braces safety net for fresh-template projects.
- ed25519 is fast enough that signing every receipt at emit-time is cost-free; no batching needed.
- Strict-mode unsigned-rejection is opt-in for v0.7.1 to allow gradual adoption; v0.8.0+ may flip the default once auto-mode (v0.10.0) wires emit-with-signing as the only path. Decision deferred until v0.10.0 arrives.
- All 19 receipts+signing tests pass (10 v0.7.0 + 9 v0.7.1).

---

## [0.7.0] — 2026-05-10

### Added — Reproducibility receipts

- **`cli/bequite/receipts.py`** (~510 lines) — Pydantic-style receipt module with stdlib-only runtime dependencies (no pydantic required at receipt-time; module is importable from `python -m bequite.receipts`).
  - **Schema v1** (`Receipt` dataclass): `version` + `session_id` (UUID) + `phase` (P0..P7) + `timestamp_utc` (ISO 8601) + `model{name, reasoning_effort, fallback_model}` + `input{prompt_hash sha256, memory_snapshot_hash sha256}` + `output{diff_hash sha256, files_touched}` + `tools_invoked[{name, args_hash sha256, exit}]` + `tests{command, exit, stdout_hash sha256}` + `cost{input_tokens, output_tokens, usd}` + `doctrine[]` + `constitution_version` + `parent_receipt` (sha256 chain pointer).
  - **`make_receipt()`** — constructor with computed hashes (sha256 of prompt text, sha256-of-files for memory snapshot dir skipping `.git/__pycache__/.venv/node_modules/.pytest_cache/.mypy_cache`, `git diff` for output + files-touched; UUID session_id; UTC timestamp).
  - **`Receipt.content_hash()`** — deterministic sha256 of canonical-JSON encoding (sorted keys, no whitespace, None-stripped). Used as filename + chain pointer.
  - **`ReceiptStore`** — local-filesystem store at `.bequite/receipts/<sha>-<phase>.json`. Methods: `write`, `list_all`, `get`.
  - **`validate_chain()`** — walks parent_receipt links; reports missing-parent + causality (parent timestamp ≤ child) + cycle-detection.
  - **`replay_check()`** — re-hashes prompt + memory snapshot; returns mismatches. Used by tests + future `bequite verify-receipts` (v0.7.1).
  - **`roll_up_by_session/phase/day()`** — token + USD aggregations with first/last timestamps + active doctrines.
  - **CLI surface:** `python -m bequite.receipts {emit,list,show,validate-chain,roll-up}` with full subcommand args (storage-dir, phase, model, prompt-file, diff-from/to, doctrines, constitution-version, input/output tokens, usd, parent-receipt, session-id, fallback-model).
- **`cli/bequite/__main__.py`** — wired `bequite cost` to read local receipts first (Article III; offline-friendly), with skill-dispatch fallback only when no receipts exist. New `bequite receipts {list,show,validate-chain,roll-up}` Click group.
- **`tests/integration/receipts/`** — 10-test integration suite covering: emit + list roundtrip; chain validation valid/invalid; replay pass/tamper-rejection; roll-ups by session/phase/day; content-hash determinism; full Receipt round-trip preservation. Runnable two ways: pytest (`python -m pytest tests/integration/receipts/`) or direct (`python tests/integration/receipts/test_receipts_smoke.py`). All 10 pass on local Python 3.14.
- **`tests/integration/receipts/README.md`** — explains coverage + run modes + future v0.7.1 (signing) coverage path.

### Changed

- `cli/bequite/__init__.py::__version__` → `0.7.0`.
- `cli/pyproject.toml::version` → `0.7.0`. Description updated to mention "reproducibility receipts (chain-hashed JSON; ed25519 signing in v0.7.1+)".

### Notes

- `ReceiptsConfig` (in `cli/bequite/config.py`) was already present from v0.5.0 (the schema slot existed; the emitter ships now).
- Receipts are append-only; superseding requires emitting a NEW receipt with the old as `parent_receipt`. Article III binding.
- ed25519 signing lands v0.7.1 — `verify-receipts` will validate chain + signature against `.bequite/keys/public.pem`.
- Cycle-detection in chain validation is structurally robust: changing any receipt field changes its `content_hash`, so a literal A→B→A cycle is impossible without a hash collision. The test suite verifies missing-parent + tamper-rejection — the realistic failure modes.

---

## [0.6.1] — 2026-05-10

### Added — Frontend Quality Module

- **Bundled Impeccable skill at `skill/skills-bundled/impeccable/`** — vendored snapshot of [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (MIT, attributed Paul Bakaus). Contents:
  - `.pinned-commit` — recorded SHA + verification date + update protocol.
  - `ATTRIBUTION.md` — MIT-license-respecting credit + bundling rationale + delisting protocol.
  - `README.md` — bundle-side docs (when it loads, how the frontend-designer uses it, layering with mena-bilingual / ai-automation / shadcn-MCP).
  - `SKILL.md` — Anthropic-Skills frontmatter (loaded-by Doctrine list, allowed-tools, hard rules layered on upstream's philosophy).
  - `references/principles.md` — 10 design principles (hierarchy, recorded typography, three-color system, 4/8/12/16 spacing scale, eased motion, real states, mobile-first/RTL/keyboard, density variants, consistency-over-cleverness, Skeptic kill-shot).
  - `references/anti-patterns.md` — 15 AI-slop tells with fixes (generic SaaS look, bad spacing, weak typography, purple-blue gradients, card nesting, fake charts, weak empty states, bad mobile, poor contrast, missing focus, repeated icons, poor UX copy, wrong hierarchy, over-rounded, unclear actions).
  - `references/aesthetic-targets.md` — Linear / Vercel / Stripe / Raycast / Arc / Notion / Cron — what they share + how to learn principles without copying.
  - `commands/CATALOG.md` — all 23 commands tabulated.
  - `commands/{craft,audit,harden,polish}.md` — marquee command dispatch contracts (~80–110 lines each: when to use, when not, inputs, steps, outputs, Skeptic kill-shot, stop conditions, anti-patterns).
- **`skill/templates/tokens.css.tpl`** — design-tokens template with deliberate font-choice comment (Doctrine Rule 2), 3-color system (primary + neutral scale + accent + system-state), strict spacing scale (4/8/12/16/24/32/48/64/96/128), restrained radius/shadow tokens, motion tokens (durations + ease curves; never bounce/elastic), breakpoints, z-index scale, light + dark theme overrides, `[dir="rtl"]` overrides for `mena-bilingual` (Tajawal/Cairo/Readex Pro), `prefers-reduced-motion` handling.
- **`skill/references/frontend-stack.md`** — verified May-2026 library reference. Component layer (shadcn/ui v3+, Radix, HeadlessUI, tweakcn, Aceternity, Magic, Origin), framework layer (Next App Router, Remix, Astro, SvelteKit, Nuxt, React+Vite), styling (Tailwind v4+, Panda, CSS Modules), type-safety (Zod, Valibot, TS), data fetching (TanStack Query, SWR, tRPC, Hono RPC), state (Zustand, Jotai), forms (React Hook Form, TanStack Form, Conform), auth (Better-Auth, Clerk, Supabase Auth, Auth0/WorkOS), a11y (axe-core, axe-playwright, eslint-plugin-jsx-a11y, react-aria), i18n (next-intl, i18next, lingui), testing (Playwright, Vitest, Storybook, MSW), perf (Vite, Turbopack, rspack, Lighthouse CI), observability (Sentry — license-flagged BSL/FSL post-2023, PostHog, OTel-JS). License flags called out where commercial closed-source distribution is impacted (Sentry / Aceternity components / SF Pro font).
- **`skill/references/frontend-mcps.md`** — wiring guide for the three frontend MCPs + tweakcn:
  - **shadcn Registry MCP** (built into shadcn CLI v3+; `npx shadcn@latest registry:mcp`; no API key).
  - **21st.dev Magic MCP** (`@21st-dev/magic`; API key `TWENTY_FIRST_API_KEY`; per-prompt-quota cost-conscious).
  - **context7 MCP** (Upstash; `@upstash/context7-mcp`; free tier; version-pinned docs).
  - **tweakcn** (visual theme editor — not an MCP; export to tokens.css).
  - Project-kickoff sequence + custom-component playbook + stack-bump refresh playbook + anti-patterns when wiring.
- **axe-core gate (Doctrine `default-web-saas` Rule 8 wired):**
  - `skill/templates/.github/workflows/axe.yml.tpl` — workflow template; runs on every PR + nightly cron at 03:00 UTC; checks out + builds + boots app + runs `axe-admin` + `axe-user` Playwright projects + uploads HTML/JSON reports + comments on PR if failed.
  - `skill/templates/tests/a11y/admin/axe-admin.spec.ts.tpl` — admin-role axe walks; per-route axe analysis with WCAG 2.0 + 2.1 A + AA tags; results JSON saved to `evidence/P6/axe/admin/`.
  - `skill/templates/tests/a11y/user/axe-user.spec.ts.tpl` — user-role parallel.
  - `skill/templates/playwright.config.ts.tpl` — added `axeProjects` (one per role) so `npx playwright test --project=axe-admin` works out of the box.
- **`skill/doctrines/default-web-saas.md` — bumped `1.0.0` → `1.1.0`** with new section 5 (Frontend Quality Module: subsections 5.1–5.5 cross-referencing the Impeccable bundle / tokens.css.tpl / frontend-stack.md / frontend-mcps.md / axe gate). Sections 6/7/8 renumbered. Rules 1–14 unchanged in behavior — additive-only bump per Article III.

### Changed

- `cli/bequite/__init__.py::__version__` → `0.6.1`.
- `cli/pyproject.toml::version` → `0.6.1`. Description appended: "Frontend Quality Module (Impeccable + tokens.css + axe-core gate)."

### Notes

The `design-audit` slash (`skill/commands/design-audit.md`) and `impeccable-craft` slash (`skill/commands/impeccable-craft.md`) authored in v0.4.0 already referenced the bundled-skill path; v0.6.1 fills in the actual bundle. No slash-command edits required; Doctrine v1.1.0 is the seam.

The Frontend Quality Module respects the existing seven phases — Impeccable is invoked in P5 (during implementation) with before/after evidence, validated in P6 (axe gate runs as part of `bequite verify`). Receipts will record Impeccable command applications when v0.7.0 ships the receipt schema.

---

## [0.6.0] — 2026-05-10

### Added — Verification gates (Playwright walks)

- `skill/templates/tests/walkthroughs/README.md.tpl` — explains the planner → spec writer → generator → healer pattern + per-Mode rigour table + anti-patterns.
- `skill/templates/tests/walkthroughs/admin-walk.md.tpl` + `user-walk.md.tpl` — natural-language walkthroughs per role; mobile + RTL + negative-paths + Skeptic kill-shot + evidence to capture.
- `skill/templates/tests/seed.spec.ts.tpl` — Playwright `setup` project; resets DB, applies migrations, seeds admin + regular users, verifies sign-in via API. Article IV — TEST_*_PASSWORD env vars required.
- `skill/templates/playwright.config.ts.tpl` — projects per `role × viewport × locale`. CI: 2 retries, 1 worker, JUnit + HTML + JSON reporters; output to `evidence/P6/`.
- `skill/templates/scripts/self-walk.sh.tpl` — boots app + curl-sweeps every public route. Cheap-curl complement to Playwright.
- `skill/templates/scripts/smoke.sh.tpl` — API-level smoke; per-endpoint expected status table.
- `skill/references/playwright-walks.md` — canonical reference for the qa-engineer's pattern. Four-step walk + per-Mode rigour matrix + per-Doctrine standard fixtures + example flow + receipt schema (cross-ref v0.7.0) + forking guidance.
- `cli/bequite/verify.py` — Phase 6 validation mesh orchestrator. 17-gate matrix per Constitution v1.0.1 (format / lint / typecheck / unit / integration / api / db-migration / seed / e2e / accessibility / build / docker-compose / security-scan / audit / freshness / self-walk / smoke / restore-drill). Per-stack command detection. Stops on first required-gate failure. Saves JSON to `evidence/P6/verify-<timestamp>.json`. Runnable: `python -m cli.bequite.verify`.
- `cli/bequite/__init__.py::__version__` → `0.6.0`. `cli/pyproject.toml::version` → `0.6.0`.

### Notes

The qa-engineer persona (v0.2.0) prescribed the planner→generator→healer pattern; v0.6.0 ships the templates that pattern operates on + the verify.py orchestrator that wires the gate matrix. Live Playwright planner orchestration (auto-generating .spec.ts via Claude API + MCPs) lands in v0.6.1 alongside the Impeccable bundle.

`tfsec` removed (officially retired into Trivy per repo description).

---

## [0.5.3] — 2026-05-10

### Changed

Repo URL casing fixed across 10 writable files: `xpshawky/bequite` / `xpShawky/bequite` / `xpshawky/BeQuite` → `xpShawky/BeQuite` (matches actual repo at `https://github.com/xpShawky/BeQuite` Ahmed created). `BEQUITE_BOOTSTRAP_BRIEF.md` and `prompts/v1/*` snapshots preserved verbatim (immutable history).

Line-count claims corrected per Article VI (honest reporting): real git counts = 24,132 lines added across 16 commits (now 19+), 153 tracked files. Earlier "30,000+ / 22,000+" estimates were inflated; replaced with git-verified numbers.

README status table refreshed (was stuck showing v0.2.0 as "🟡 committing now"; now reflects all 13 tags through v0.5.2). Doctrine table updated for v0.5.2's three new Doctrines (vibe-defense / mena-pdpl / eu-gdpr).

Quickstart reframed honestly: today vs after-first-push. The `uvx --from git+...` install command works only after the repo is pushed (one-way door; awaits owner authorization). Today's path is `python -m cli.bequite.audit` + `python -m cli.bequite.freshness` from a local checkout.

Remote configured: `origin = https://github.com/xpShawky/BeQuite.git` (fetch + push). NOT pushed.

---

## [0.5.2] — 2026-05-10

### Added

- **Constitution v1.1.0 → v1.2.0**: **Article IX — Cybersecurity & authorized-testing discipline**. Renumbered from brief's "Article XII." Substantive text otherwise verbatim with four senior-architect amendments: (1) **internal red-team carve-out** with 8 hard guardrails for corporate-internal C2/implants/payloads; (2) **cryptojackers** added to forbidden-no-matter-what list; (3) **defensive-validation clause** for known-CVE PoCs against own systems (RoE-self); (4) **plural disclosure frameworks** (Project Zero / CERT/CC / MITRE CNA / FDA / ICS-CERT / NCSC).
- **`ADR-010-article-ix-cybersecurity.md`** captures the bump rationale + four amendments.
- **`skill/references/security-and-pentest.md`** — 25+ verified May-2026 tools with license flags called out (AGPL/GPL = closed-source-blocker; Apache/MIT clean). Lite scanner stack (Trivy + Semgrep + OSV + secret-scan) + full opt-in (Nuclei + ZAP + Wazuh + Falco). Three workflow patterns (scan-and-trigger / harden-on-deploy / incident-response). Selection tree, compliance Doctrine cross-reference.
- **4 new personas:** `security-auditor` (14th, defensive — pairs with existing `security-reviewer`), `pentest-engineer` (15th, RoE-gated offensive), `cve-watcher` (16th, support — daily trickest/cve diff vs SBOM, Haiku), `disclosure-timer` (17th, support — 60/80/90-day SLA tracking, framework-aware).
- **3 new hooks:** `pretooluse-pentest-authorization.sh` (blocks offensive tools without RoE; recognizes lab targets), `pretooluse-no-malware.sh` (blocks 6 forbidden categories — reverse-shell/persistence/cred-exfil/C2/ransomware/cryptojacker — NO override except internal-RT 8-guardrail carve-out), `pretooluse-cve-poc-context.sh` (PoC requires ADR with 3 confirmations).
- **2 templates:** `projects/scan-and-trigger.md` (canonical defensive automation; lite default + `--with-wazuh` opt-in; harden-on-deploy CI gate; incident-response runbook), `roe-template.md` (4 variants — ROE / RoE-RT / RoE-self / RoE-CTF — RoE-RT additions enumerate all 8 hard guardrails).
- **3 new Doctrines:**
  - **`vibe-defense`** — DEFAULT for `audience: vibe-handoff`. 15 extra-strict rules codifying response to Veracode 2025's 45% OWASP-Top-10 hit rate on AI-generated code: HIGH-SAST blocks merge with 90d-expiring-ADR-override, exact-pinned prod deps, RLS deny-by-default, locked-down CSP, secret-scan on every commit, axe-core every deploy, mandatory `bequite audit` clean, input validation everywhere, Better-Auth/Clerk/Supabase no-custom auth, rate limiting on public endpoints, CSRF, Argon2id, hardened cookies, logs exclude PII.
  - **`mena-pdpl`** — Egyptian PDPL (Law 151/2020) + Saudi PDPL (SDAIA enforceable since 2024-09-14, 48+ enforcement decisions by Jan 2026) + UAE Federal PDPL (Decree-Law 45/2021) with **jurisdiction branching** for UAE free zones (DIFC DPL 5/2020, ADGM Data Protection Regs 2021, DHCC). Authoritative URLs verified. Egypt's executive regs flagged as pending.
  - **`eu-gdpr`** — GDPR 2016/679. 12 rules covering Arts. 6/15-22/25/30/32-35/37, ePrivacy cookie consent, Schrems II + SCCs 2021. Stacks with `mena-pdpl` when DIFC/ADGM in scope.
- **`.bequite/memory/prompts/v2/`** — phase snapshot per Article III: Constitution v1.2.0 + ADR-009 + ADR-010 archived.

### Notes — research-driven corrections

The verification research agent surfaced critical corrections applied throughout v0.5.2:

- Crawl4AI canonical URL: `unclecode/crawl4ai` (not `crawl4ai/crawl4ai`).
- n8n MCP: `czlonkowski/n8n-mcp` (community, **not** official `n8n-io`).
- Firecrawl org rename: `mendableai/firecrawl*` → `firecrawl/firecrawl*`.
- License flags throughout: Firecrawl + Shannon + Pentagi + BunkerWeb + THC Hydra are AGPL-3.0; Wazuh + SafeLine + ImHex are GPL-2/3.0; Strix + Trivy + OSV-Scanner + Nuclei + Crawl4AI + Crawlee are Apache-2.0 / MIT (clean).
- tfsec officially retired into Trivy.
- Bug-bounty platform APIs all auth-required; `arkadiyt/bounty-targets-data` for anonymous program-scope reads.
- MENA PDPL: Egypt regs pending; KSA enforceable 2024-09-14; UAE free-zone carve-outs (DIFC/ADGM/DHCC).

### Improvements adopted (per "make it fully loaded" delegation)

I2.1 Internal RT carve-out · I2.2 cve-watcher · I2.3 disclosure-timer · I2.5 vibe-defense Doctrine as default · I2.6 Bug-bounty engagement assistant · I2.7 Findings-to-Jira/Linear · I2.8 Anti-bug-bounty-poaching guard.

---

## [0.5.1] — 2026-05-10

### Added

- **Constitution v1.0.1 → v1.1.0**: **Article VIII — Scraping & automation discipline** added. Renumbered from the brief's "Article XI" to fit BeQuite's 7-Iron-Law structure (we trimmed in v0.1.0). Substantive text otherwise verbatim from the addendum, with four senior-architect amendments: (1) default rate limit `1 req/sec` → `1 req/3 sec` polite-default; (2) stealth requires `legitimate-basis ∈ {own-site, bug-bounty-allows, ToS-explicitly-allows, security-research-with-coordinated-disclosure}` not just "ADR exists"; (3) captcha-solving clause added (CFAA-class concern); (4) watch-budget added (`max_fires_per_week`; 3× exceeded → pause-and-ask).
- **`.bequite/memory/decisions/ADR-009-article-viii-scraping.md`** — captures the Constitution amendment + the four amendments + alternatives considered + consequences + verification.
- **`skill/references/scraping-and-automation.md`** — canonical scraping library list with verified May 2026 URLs + star counts + licenses + last-release dates. Triad (Crawlee / Crawlee-Python / Trafilatura / Firecrawl / Scrapling) + specialists + browser automation + stealth (ADR-gated) + OSINT (RoE-gated). Decision tree, watch-and-trigger pattern, polite-mode preset, anti-bot posture, MCP servers, compliance map (GDPR / CCPA / Egyptian PDPL / Saudi PDPL / UAE PDPL / CFAA / Computer Misuse Act / Robots Exclusion Standard / per-site ToS), forking guidance.
  - **License flags called out**: Firecrawl AGPL-3.0 (commercial closed-source caveat); Crawl4AI Apache-2.0 (cleaner alternative); n8n-mcp is community-maintained (`czlonkowski/n8n-mcp`), not official n8n-io.
  - **Verification footer**: every URL + stars + last-release verified via GitHub REST API on 2026-05-10.
- **`skill/agents/scraping-engineer.md`** — 13th persona. Owns scraping library selection, robots.txt + ToS enforcement, polite-mode defaults, watch-and-trigger pattern, change-detection strategy, anti-bot posture, watch-budget gate, `bequite scrape doctor` command. Cross-pollinates with `automation-architect` (workflow side), `security-reviewer` (legitimate-basis ADRs), `research-analyst` (freshness probes), `token-economist` (scraping cost), `frontend-designer` (admin UI when applicable). Phases P0/P1/P2/P3/P5/P6.
- **`skill/hooks/pretooluse-scraping-respect.sh`** — enforcement hook. Exit 2 (block) when: scraping import without robots.txt path; scraping import without rate-limit + cache config; stealth library without `legitimate-basis` ADR; captcha-solving service without `legitimate-basis` ADR; PII field assignments from scraped data without consent log. Self-exclusion list for the canonical reference + persona + this hook itself + tests.
- **`skill/templates/projects/watch-and-trigger.md`** — canonical scaffold for "watch X, when it changes, trigger Y." Ships n8n + Postgres + Redis in `infra/docker-compose.yml` by default (opt-out via `--no-n8n` swap to `docker-compose.no-n8n.yml`). `polite_mode = true` baked into generated `bequite.config.toml`. Per-target spec + change-detection module + watch-budget enforcement + `bequite scrape doctor` smoke + Phase 6 gates additions.

### Notes

Article VIII is BeQuite's first non-master Iron Law — the brief's "Article XI" name preserved verbatim in the article header but renumbered to VIII for structural consistency. The hook + the polite-mode preset together make Article VIII enforceable, not documentary. Pairs with the existing `ai-automation` Doctrine (v0.2.1) — that Doctrine governs workflow execution; Article VIII governs scraping inputs that feed those workflows.

Three URL corrections caught by parallel verification research: Crawl4AI canonical is `unclecode/crawl4ai` (not `crawl4ai/crawl4ai`); n8n MCP is `czlonkowski/n8n-mcp` (not `n8n-io/n8n-mcp` — community-maintained); `mendableai/firecrawl*` redirects to `firecrawl/firecrawl*` (org rename). License flags surfaced: Firecrawl + Shannon + BunkerWeb are AGPL-3.0 (commercial-closed-source-blocker); Crawl4AI + Strix are Apache-2.0 (clean alternatives).

`tfsec` removed from the canonical list (officially retired into Trivy per repo description; last release May 2025).

---

## [0.5.0] — 2026-05-10

Python CLI thin wrapper. **Eleven sub-versions now tagged this session.** `bequite` + `bq` console scripts; 19 subcommands; Pydantic config; skill loader (v0.5.0 stub for live API dispatch in v0.6.0+); per-host hook runner. See full notes under v0.5.0 commit + the README architecture section.

Key files: `cli/pyproject.toml`, `cli/bequite/__main__.py`, `cli/bequite/commands.py`, `cli/bequite/config.py`, `cli/bequite/skill_loader.py`, `cli/bequite/hooks.py`. All modules import cleanly.

---

## [0.4.3] — 2026-05-10

`cli/bequite/freshness.py` — knowledge probe Python module. npm + PyPI + crates.io + GitHub probes. 24h cache. Verdict logic (fresh / stale-warn / stale-block). Supply-chain incident table. `skill/references/package-allowlist.md` — known-good packages list (~60 entries; ecosystem prefixes).

---

## [0.4.2] — 2026-05-10

`cli/bequite/audit.py` — Constitution + Doctrine drift detector. 7 rule packs (Iron Law IV secrets + env-reads, default-web-saas Rules 2 & 4, library-package Rule 7, ai-automation Rules 1 & 4). Markdown + JSON render. CI workflow at `.github/workflows/audit.yml` (PR + push + manual + quarterly cron; PR comments on blockers; 30d artifacts). `tests/integration/audit/README.md` fixture map.

---

## [0.4.1] — 2026-05-10

### Added

7 BeQuite-unique slash commands at `skill/commands/` (each Markdown with frontmatter + workflow + stop condition + anti-patterns + related-commands):

- `audit.md` — Constitution + Doctrine drift detector. Walks Iron Laws + active Doctrines + ADRs; surfaces violations (block/warn/recommend) with file:line + remediation. Cross-references `posttooluse-audit.sh` (lightweight per-edit subset). Implementation: `cli/bequite/audit.py` (v0.4.2).
- `freshness.md` — knowledge probe. Verifies stack candidates aren't deprecated / EOL'd / replaced / open-CVE'd / pricing-tier-mismatched / supply-chain-incident-flagged. Per-package: last commit < 6mo + fresh release + no unfixed criticals + license unchanged + maintainer status. 24h cache TTL. Wires into `/bequite.decide-stack` pre-sign mandatory checks. Implementation: `cli/bequite/freshness.py` (v0.4.3).
- `auto.md` — one-click run-to-completion P0 → P7. State machine: INIT → P0_RESEARCH → ... → DONE with explicit BLOCKED/FAILED/PAUSED states. Per-phase commits + signed receipts. Safety rails: cost ceiling, wall-clock ceiling, 3-failure threshold, banned-word check, hook block (never auto-overridden), one-way doors always pause. Failure replay to `.bequite/replays/`. Heartbeat every 5 min. Implementation: `cli/bequite/auto.py` (v0.10.0).
- `memory.md` — Memory Bank operations: show / show <file> / show doctrine <name> / show adr <id> / refresh / validate / snapshot / diff. Schema-validates every Memory Bank + state file per the v0.1.0 templates.
- `snapshot.md` — versioned snapshot to `.bequite/memory/prompts/v<N>/<timestamp>_<phase>_<reason>/` per Article III phase-end discipline. Auto-fires at end-of-phase + before one-way doors + on Stop with non-trivial work + on `bequite release`.
- `cost.md` — token + dollar receipts roll-up. Per-phase / per-persona / per-day / per-feature breakdowns. Anomaly detection (>2× routing.json estimate; >1.5× rolling-7-day avg; cache-hit ratio <50%). Wires into `state/project.yaml::safety_rails.cost_ceiling_usd`. Implementation lands with v0.7.0 receipts.
- `skill-install.md` — install BeQuite into a host (Claude Code / Cursor 3.0+ / Codex CLI / Gemini CLI / Windsurf / Cline / Kilo Code / Continue.dev / Aider). Detects host; copies skill content to host's discovery path; merges hooks into `.claude/settings.json` without overwriting user customisation; runs per-host smoke test. Implementation: `cli/bequite/skill_install.py` (v0.12.0).

### Notes

19 commands total surface (12 master-aligned in v0.4.0 + 7 unique in v0.4.1). Five commands have implementations that ship in later sub-versions: `audit` (v0.4.2), `freshness` (v0.4.3), `auto` (v0.10.0), `cost` (v0.7.0+), `skill-install` (v0.12.0). The Markdown specs in v0.4.1 commit to the contract those implementations satisfy.

---

## [0.4.0] — 2026-05-10

### Added

- **12 master-aligned slash commands at `skill/commands/`** (each one Markdown with frontmatter — name, description, phase, persona, prompt-pack reference; body specifies workflow + stop condition + anti-patterns + related commands):
  - `discover.md` — P0 product discovery interview (product-owner; 8 question groups; recommended-defaults; risk register).
  - `research.md` — P0 research scan (research-analyst; source-authority-ranked; 5 output files; cited URLs only).
  - `decide-stack.md` — P1 stack ADR (software-architect; freshness-probe + Skeptic + Doctrine alignment + audit clean as pre-sign mandatory checks; encodes the 12 brief reconciliations).
  - `plan.md` — P2 spec + plan + data-model + contracts (software-architect; analyse adversarial review).
  - `implement.md` — P5 TDD discipline (RED-GREEN-REFACTOR; per-task commit; receipt; dispatches to backend-engineer / frontend-designer / database-architect / automation-architect).
  - `review.md` — P5 senior review (13 review categories per master §7.6; Skeptic + security-reviewer; verdict Approved / Approved-with-comments / Blocked).
  - `validate.md` — P6 validation mesh (per-Mode gate matrix; Playwright walks at viewport 360+1440 and locale en/ar; self-walk + smoke + audit + freshness; phase summary).
  - `recover.md` — generate paste-able recovery prompt for new sessions (master §25; reads state/recovery.md + Memory Bank + receipts; computes 7 answers; chain-integrity check).
  - `design-audit.md` — detect AI-looking UI (15 anti-patterns from master §7.9 + Impeccable cross-reference; report at evidence/<phase>/design-audit-<date>.md).
  - `impeccable-craft.md` — invoke specific Impeccable command (23 commands documented; before/after screenshots; per-task commit).
  - `evidence.md` — surface evidence + cross-reference receipts (chain integrity check).
  - `release.md` — P7 handoff + release prep (master §27 release DoD; HANDOFF.md hand-runnable bar; semver discipline; one-way-door pauses for owner).

### Notes

These 12 commands are dispatch instructions to the relevant persona; they do NOT duplicate persona content. Each command's body fits in ~80-120 lines (concise; the personas + prompt-packs do the heavy lifting). All 12 are ported into `template/.claude/commands/` on `bequite skill install` (v0.12.0+). `bequite.recover` works in any host that loads AGENTS.md.

---

## [0.3.0] — 2026-05-10

### Added

- **10 hook scripts at `skill/hooks/`** (Constitution v1.0.1 Article IV — deterministic gates):
  - `pretooluse-secret-scan.sh` — regex secrets (AWS / GitHub / Anthropic / OpenAI / Stripe / Slack / JWT / SSH private keys / generic API key shapes) in Edit / Write / Bash. Exit 2.
  - `pretooluse-block-destructive.sh` — Tier-3 commands per master §19.4 (`rm -rf` outside `/tmp`, `git push --force`, `git reset --hard`, `DROP DATABASE`, `TRUNCATE`, `DELETE` without WHERE, `terraform destroy`, `pulumi destroy`, `kubectl delete namespace`, fork bombs, `mkfs.*`, `dd of=/dev/sd*`). Exit 2.
  - `pretooluse-verify-package.sh` — diffs new imports / dependencies in `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`. Verifies via `npm view` / `pypi.org` / `crates.io`. PhantomRaven defense. Allowlist at `skill/references/package-allowlist.md` (drafted v0.4.3). `BEQUITE_OFFLINE=1` escape hatch. Exit 2 on hallucinated package.
  - `posttooluse-format.sh` — auto-formats by extension (biome / prettier for TS/JS, ruff/black for Python, rustfmt for Rust, gofmt for Go, jq for JSON, prettier for MD/CSS/HTML). Warn-only.
  - `posttooluse-lint.sh` — biome / eslint / ruff / clippy / `go vet`. Warn-only.
  - `posttooluse-audit.sh` — lightweight subset of `bequite audit`: hardcoded `font-family: Inter` outside tokens (Doctrine `default-web-saas` Rule 2), `.env*` reads in code (Iron Law IV), telemetry-shaped fetch outside opt-in gate (Doctrine `library-package` Rule 7). Warn-only.
  - `stop-verify-before-done.sh` — banned-weasel-words check (`should`, `probably`, `seems to`, `appears to`, `I think it works`, `might work`, `hopefully`, `in theory`, etc. — Constitution v1.0.1 Article II). Plus `state/task_index.json` `in_progress` check. Exit 2.
  - `sessionstart-load-memory.sh` — prints the Memory Bank + ADR + state/ paths the agent must read on session start (Iron Law III).
  - `sessionstart-cost-budget.sh` — prints active safety rails (cost ceiling, wall-clock ceiling, failure threshold) from `state/project.yaml`.
  - `stop-cost-budget.sh` — enforces cost ceiling. Reads `.bequite/cache/cost-ledger.json` (token-economist writes; v0.7.0+). 80% warn; 100% block until human override at `.bequite/cache/cost-override.json`. Exit 2 at 100% without override.
- **`template/.claude/settings.json`** — wires all 10 hooks under their event matchers (PreToolUse / PostToolUse / Stop / SessionStart). Per-hook timeouts. Inline `_comment_bequite` documenting binding Constitution articles.
- **`tests/integration/hooks/README.md`** — fixture layout + smoke-test commands + hook-to-fixture map + v0.3.0 acceptance criteria + v0.6.0 CI integration plan.

### Notes

All hooks read JSON from stdin (Claude Code hook protocol), parse with `jq`, exit 0 / 2 with reason on stderr. Cross-platform — Linux + macOS bash; Windows via Git Bash. Per Constitution v1.0.1 + master §19.4, **no flag bypasses any hook**. Auto-mode never auto-overrides. Override paths are explicit (ADR amendment, allowlist file, ENV escape, human-approved override file) — none are silent.

`bequite freshness` (v0.4.3+) and `bequite audit` (v0.4.2+) ride on top of these hooks once they ship; the hook scripts contain the safety-critical subset.

---

## [0.2.1] — 2026-05-10

### Added

- **`ai-automation` Doctrine** — for projects whose primary deliverable is an automation pipeline (n8n / Make / Zapier / Temporal / Inngest / Trigger.dev / Pipedream / AWS Step Functions). 12 rules covering: workflows-as-versioned-source, idempotency, retry+backoff+jitter+DLQ, secrets via connectors not flow JSON, observability with trace propagation, test fixtures + dry-run, error notification routing, schema validation at the edge, AI-agent budget + circuit breaker, rate-limit awareness, versioned upgrades, daily cost roll-up. Stack guidance per platform, 10-gate verification, forking guidance.
- **`automation-architect` persona** (12th persona) at `skill/agents/automation-architect.md`. Owns workflow design across all named platforms; cross-pollinates with backend-engineer, frontend-designer (admin UIs), security-reviewer (connector secrets, prompt-injection paths), token-economist (LLM-call cost in agent chains).
- **Bundled `ai-automation` skill** at `skill/skills-bundled/ai-automation/`:
  - `README.md` — overview + when this skill loads + layering with Impeccable.
  - `references/n8n.md` — deep n8n expertise (architecture, JSON shape, CI deploy, idempotency, retry+DLQ, observability, AI patterns, self-host docker-compose, 12-rule verification checklist).
  - `references/make.md` — deep Make.com expertise (operations meter as cost killer, scenario JSON shape, error handlers, AI patterns without native agent primitive, 12-rule checklist).
  - `references/zapier.md` — Zapier brief (per-task pricing, Paths, Code by Zapier, 12-rule checklist).
  - `references/temporal.md` — Temporal brief (workflows vs activities, durable execution, replay debugging, signals + queries, AI agent loop pattern, 12-rule checklist).
  - `references/inngest.md` — Inngest brief (TS-first, event-driven, step.run, step.parallel, step.ai.infer, 12-rule checklist) + adjacent (Trigger.dev, Pipedream).
  - `references/patterns.md` — 8 cross-platform patterns: idempotency, retry+backoff+jitter, dead-letter queue, fan-out+fan-in, circuit breaker for AI-agent loops, schema validation at the edge, trace propagation, prompt-injection guardrails. Maps each to per-platform implementations.

### Changed

- **`skill/SKILL.md`** — adds 12th persona (automation-architect); Skeptic kept as 11th (the two BeQuite additions on top of master's 10).
- **`skill/routing.json`** — adds automation-architect routing (Opus 4.7 high; loaded with the bundled `ai-automation` skill when the Doctrine is active).
- **`skill/templates/bequite.config.toml.tpl`** — adds `ai-automation` to the available-Doctrines list; adds `[skills.ai_automation]` block; adds `[ai_automation]` section with cost-alarm thresholds per platform + agent guardrails (max iterations, max cost USD/run, circuit-breaker thresholds).

### Notes

This release is responsive to the user's request to "add AI automation features" with explicit n8n + Make expertise. The Doctrine + persona + bundled skill are decoupled: any project can opt in by adding `ai-automation` to its `doctrines` list. Active automation-architect cross-pollinates with the existing 10 + Skeptic personas (12 total). No conflict with existing Doctrines.

---

## [0.2.0] — 2026-05-10

### Added

- **`skill/SKILL.md`** — the orchestrator. Anthropic Skills frontmatter (name `bequite`, description ≤ 1024 chars, allowed-tools list). Body: orchestrator persona, 7-phase router (P0 Research → P7 Handoff), mode selector (Fast / Safe / Enterprise per Constitution v1.0.1), 19-command surface (master's 12 named + BeQuite's 7 unique extras: `/audit`, `/freshness`, `/auto`, `/memory`, `/snapshot`, `/cost`, `/skill-install`), routing matrix reference, hooks reference, auto-mode reference, banned-weasel-words enforcement.
- **11 persona files at `skill/agents/`:**
  - `product-owner` — owns scope, requirements, phase + task breakdown.
  - `research-analyst` — owns research with cited authority levels, fights AI hallucination of facts.
  - `software-architect` — owns ADRs, system boundaries, second-pass code review.
  - `frontend-designer` — owns UI direction, design system, Impeccable-style flow (12 steps), tokens-only design.
  - `backend-engineer` — owns API, services, error shape, TDD discipline (RED-GREEN-REFACTOR).
  - `database-architect` — owns data model, migrations (reversible), backup-restore drill.
  - `qa-engineer` — owns Playwright planner-generator-healer pattern, validation mesh.
  - `security-reviewer` — owns threat model, OWASP LLM Top 10 + Web Top 10 mapping, supply-chain review.
  - `devops-engineer` — owns Docker, CI, deployment, handoff (P7).
  - `token-economist` — owns cost ceiling, prompt compression, AkitaOnRails 2026 routing rules.
  - `skeptic` — adversarial twin (BeQuite's unique addition; one kill-shot per phase boundary).
- **`skill/routing.json`** — default model routing matrix per phase + persona. Provider abstraction (Anthropic primary; OpenAI / Google / DeepSeek / Ollama fallback). Encodes AkitaOnRails 2026 finding (split-only-when-genuinely-parallel; threshold N>5). Encodes Aider architect-mode pattern (cheap writes + frontier reviews + cheap fixes). Compliance routing for hipaa/pci/fedramp.
- **`skill/templates/bequite.config.toml.tpl`** — per-project config schema. Sections: project metadata, mode, audience, doctrines, scale_tier, compliance, locales, safety_rails (cost + wall-clock + failure threshold + banned-phrase list + auto-mode pause triggers), routing overrides, providers (env-var-only), freshness, receipts, evidence, memory, hosts, skills, telemetry (off by default), mena_bilingual.
- **`template/.claude/skills/bequite/README.md`** — fresh-project skill-install target. Documents the copy-not-symlink decision (Windows + Docker volume compatibility; reproducibility).

### Notes

This release contains no executable code; the CLI ships in v0.5.0. The skill is portable across hosts (Claude Code via `.claude/skills/`, Cursor 3.0+ via `.cursor/skills/`, Codex CLI via `AGENTS.md` discovery, others via the `bequite skill install` v0.12.0 command). Every persona references the Constitution + active Doctrines for binding rules. Skeptic gate now mandatory at every phase boundary.

---

## [0.1.2] — 2026-05-10

### Added

- **Master-file merge audit** at `docs/merge/MASTER_MD_MERGE_AUDIT.md` reconciling `BeQuite_MASTER_PROJECT.md` (introduced mid-session, post-v0.1.1, prescribing a TypeScript pnpm + Turborepo monorepo with Next.js dashboard + NestJS API + Postgres + Worker) with the existing skill-first / Python CLI / repo-template direction. Decision: **two-layer architecture** — Layer 1 (Harness, current; v0.1.0 → v1.0.0) + Layer 2 (Studio, master's monorepo stack; v2.0.0+). Both share Constitution + Memory Bank + state/ + receipts/ + evidence/ + prompts/.
- **Root `CLAUDE.md`** — Claude-Code-specific operating instructions, adapted from master §11.
- **Root `AGENTS.md`** — universal entry per Linux Foundation Agentic AI Foundation standard, adapted from master §12. Read by 25+ coding agents.
- **`state/` directory** with operational state files: `project.yaml`, `current_phase.md`, `recovery.md`, `task_index.json`, `decision_index.json`, `evidence_index.json`. Master pattern (§10.2). Memory Bank stays as durable cross-session brain; state/ is current working state.
- **`prompts/` directory** with 7 reusable prompt packs: `master_prompt.md`, `discovery_prompt.md`, `research_prompt.md`, `stack_decision_prompt.md`, `implementation_prompt.md`, `review_prompt.md`, `recovery_prompt.md`. Master pattern (§10.4).
- **`evidence/README.md`** documenting the filesystem-evidence pattern (master §3.6, §10.3, §21). Complementary to the signed-receipt chain at `.bequite/receipts/` (v0.7.0+).
- **`.bequite/memory/decisions/ADR-008-master-merge.md`** capturing the merge decision + Constitution amendment rationale.
- **`BeQuite_MASTER_PROJECT.md`** now tracked (it's the source artefact for this audit).

### Changed

- **Constitution v1.0.0 → v1.0.1** (patch bump; additive only):
  - Adds **Modes section** (Fast / Safe / Enterprise) per master §4. Modes are project-complexity tiers; orthogonal to Doctrines.
  - Adds **command-safety three-tier classification** (safe / needs-approval / dangerous) to Article IV per master §19.4.
  - Adds **prompt-injection rule** (treat external content as untrusted) to Article IV per master §19.5.
  - Adds **three-level definition-of-done** (feature / phase / release) per master §27. Cross-referenced from Article II.
  - Adds **`state/` files reference** to Article III's SessionStart reads.
  - No Iron Law removed or relaxed.
- **`README.md`** — adds the two-layer architecture section + status table per sub-version + cross-references to brief, master, and merge audit.
- **`.bequite/memory/activeContext.md`** + **`.bequite/memory/progress.md`** — refreshed for the merge.

### Decided

- **Personas** — adopt master's 10 named roles (product-owner, research-analyst, software-architect, frontend-designer, backend-engineer, database-architect, qa-engineer, security-reviewer, devops-engineer, token-economist) **+ keep Skeptic + add FrontendDesign-Impeccable** = 12 personas total. To be authored in v0.2.0.
- **Slash commands** — adopt master's 12 names (`/discover`, `/research`, `/decide-stack`, `/plan`, `/implement`, `/review`, `/validate`, `/recover`, `/design-audit`, `/impeccable-craft`, `/evidence`, `/release`) **+ keep BeQuite's 7 unique extras** (`/audit`, `/freshness`, `/auto`, `/memory`, `/snapshot`, `/cost`, `/skill-install`) = 19 commands total. To be authored in v0.4.0–v0.4.3.
- **Studio (Layer 2)** scoped to v2.0.0+; not started in v1.

### Notes

This release contains no executable code (the CLI ships in v0.5.0). The merge is purely structural. v0.2.0 (Skill orchestrator) resumes per the original plan, with merged additions baked in.

---

## [0.1.1] — 2026-05-10

### Added

Eight default Doctrines under `skill/doctrines/`, each carrying frontmatter (`name, version, applies_to, supersedes, maintainer, ratification_date, license`) + numbered rules (kind: `block` / `warn` / `recommend` + check) + stack guidance + verification gates + examples + forking guidance + changelog:

- `default-web-saas` — UI rules (no AI-default Inter without recorded reason; no purple-blue gradients; no nested cards; no gray-on-color), shadcn/ui ordering, tokens.css required, axe-core gate, Playwright admin+user walks, deny-by-default authz, Zod/Pydantic/Valibot input validation. Stack matrix reflects May 2026 reality (post brief reconciliations).
- `cli-tool` — semver-strict on flags, exit-code discipline (0/1/2/>2), stdout-vs-stderr, NO_COLOR support, completions, man pages, no global state without consent, idempotent operations.
- `ml-pipeline` — reproducible training (seed + dataset version + config), DVC/lakeFS for data, experiment tracking, GPU-cost ceiling, model lineage.json, eval before deploy, no PII in training data, Model Cards.
- `desktop-tauri` — Tauri v2 (Stronghold deprecated → OS keychain), `notarytool` (not altool), AzureSignTool + OV cert (EV no longer privileged since Aug 2024), Keygen recommended for licensing, license validation in Rust not JS, 20 MB bundle discipline.
- `library-package` — semver-strict public API, public-API freeze + private internals, type definitions ship with package, Keep-a-Changelog, Conventional Commits, deprecation runway, no telemetry without opt-in, license clarity, GPL contamination guard, supply-chain hygiene (PhantomRaven defense).
- `fintech-pci` — CDE segmentation, never store SAD post-auth, PAN masking/tokenisation, AES-256 + KMS/HSM, TLS 1.2+, MFA on CDE access, audit log retention 1+ year, FIM, quarterly ASV scans + annual pentest, signed BAAs. Aligned to PCI DSS v4.0.
- `healthcare-hipaa` — PHI inventory + data-flow diagram, FIPS-validated AES-256, TLS 1.2+, unique user IDs, audit controls (6-year retention), minimum-necessary access, BAAs with all BAs, de-identification before analytics/training, breach notification, no PHI in non-prod, no PHI to LLM without BAA + DPIA + de-id + no-data-retention tier.
- `gov-fedramp` — FIPS 199 impact level, SSP maintained, FIPS 140-2/3 *validated* crypto (validated, not merely compliant), FIPS-approved TLS suites, MFA on privileged actions, ConMon (monthly scans + POA&M), immutable audit logs, baseline configs + FIM, SCRM with SBOM, U.S. data residency, authorisation boundary documented. Aligned to NIST 800-53 Rev 5.

`mena-bilingual` Doctrine deferred to v0.11.0 per the approved plan.

### Notes

Each regulated Doctrine carries a disclaimer: starting points, not substitutes for QSA / Security Officer / 3PAO review. No executable code in this release.

---

## [0.1.0] — 2026-05-10

### Added

- Repository skeleton: `README.md`, `LICENSE` (MIT), `.gitignore`, `CHANGELOG.md`.
- **Constitution v1.0.0** — Iron Laws (Articles I–VII): Specification supremacy, Verification before completion, Memory discipline, Security & destruction discipline, Scale honesty, Honest reporting, Hallucination defense.
- **Doctrine schema** — frontmatter + sections for forkable per-project-type rules.
- **ADR template** — semver-versioned, status tracking (proposed / accepted / superseded).
- **Memory Bank templates** — six files (Cline pattern): `projectbrief`, `productContext`, `systemPatterns`, `techContext`, `activeContext`, `progress`.
- **Rendered fresh-project instances** at `template/.bequite/memory/`.
- Plan snapshot archived to `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md`.

### Notes

This release contains no executable code. It establishes the inviolate base layer (Constitution + Memory Bank + ADR + Doctrine schemas) on which every later sub-version depends.

[Unreleased]: https://github.com/xpShawky/BeQuite/compare/v0.20.0...HEAD
[0.20.0]: https://github.com/xpShawky/BeQuite/compare/v0.19.5...v0.20.0
[0.19.5]: https://github.com/xpShawky/BeQuite/compare/v0.19.0...v0.19.5
[0.19.0]: https://github.com/xpShawky/BeQuite/compare/v0.18.0...v0.19.0
[0.18.0]: https://github.com/xpShawky/BeQuite/compare/v0.17.0...v0.18.0
[0.17.0]: https://github.com/xpShawky/BeQuite/compare/v0.16.0...v0.17.0
[0.16.0]: https://github.com/xpShawky/BeQuite/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/xpShawky/BeQuite/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/xpShawky/BeQuite/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/xpShawky/BeQuite/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/xpShawky/BeQuite/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/xpShawky/BeQuite/compare/v0.10.7...v0.11.0
[0.10.7]: https://github.com/xpShawky/BeQuite/compare/v0.10.6...v0.10.7
[0.10.6]: https://github.com/xpShawky/BeQuite/compare/v0.10.5...v0.10.6
[0.10.5]: https://github.com/xpShawky/BeQuite/compare/v0.10.0...v0.10.5
[0.10.0]: https://github.com/xpShawky/BeQuite/compare/v0.9.2...v0.10.0
[0.9.2]: https://github.com/xpShawky/BeQuite/compare/v0.9.1...v0.9.2
[0.9.1]: https://github.com/xpShawky/BeQuite/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/xpShawky/BeQuite/compare/v0.8.1...v0.9.0
[0.8.1]: https://github.com/xpShawky/BeQuite/compare/v0.8.0...v0.8.1
[0.8.0]: https://github.com/xpShawky/BeQuite/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/xpShawky/BeQuite/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/xpShawky/BeQuite/compare/v0.6.1...v0.7.0
[0.6.1]: https://github.com/xpShawky/BeQuite/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/xpShawky/BeQuite/compare/v0.5.3...v0.6.0
[0.5.3]: https://github.com/xpShawky/BeQuite/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/xpShawky/BeQuite/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/xpShawky/BeQuite/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/xpShawky/BeQuite/compare/v0.4.3...v0.5.0
[0.4.3]: https://github.com/xpShawky/BeQuite/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/xpShawky/BeQuite/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/xpShawky/BeQuite/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/xpShawky/BeQuite/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/xpShawky/BeQuite/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/xpShawky/BeQuite/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/xpShawky/BeQuite/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/xpShawky/BeQuite/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/xpShawky/BeQuite/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/xpShawky/BeQuite/releases/tag/v0.1.0
