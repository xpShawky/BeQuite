# BeQuite — Full Project Audit (v2.0.0-alpha.5)

**Date:** 2026-05-11
**Auditor:** Claude (Opus 4.7 xhigh) acting as senior product / QA / DevOps engineer
**Scope:** Repo structure · install path · runtime · frontend UX · API · CLI · tests · release gate
**Methodology:** Read-only inspection of every manifest, component, route, doc, and script. Live verification deferred to Phase 2–7.

---

## 1. Executive summary

BeQuite is in pre-release `v2.0.0-alpha.5` with a Layer-1 CLI tagged `v1.0.3` (Production/Stable) and a Layer-2 Studio (marketing + dashboard + API) in alpha. **The product runs** — both Next.js apps render at HTTP 200 from a fresh clone (verified `v2.0.0-alpha.3`); the CLI installs cleanly via bootstrap (verified `v1.0.3`); Docker compose YAML validates clean.

**Where it falls short:**
- **Frontend UX**: at least 6 dead clicks / hardcoded panels / missing-anchor links. The dashboard's DEPLOY button does nothing; the marketing Nav's "How it works" link scrolls to an anchor that doesn't exist; the PlanTasksTests + AgentPanel "recent activity" are hardcoded mock data instead of pulling from real state.
- **One-command dev**: no root `package.json`, no `Makefile`, no `bequite dev`. Currently a user must `cd` into three directories and run three commands or fall back on `docker compose up`.
- **Test coverage**: Python integration suite is strong (125+ tests across 12 modules). Frontend has **zero** Playwright tests. API has no smoke tests outside the Python suite.
- **Honest gaps**: `bequite doctor` exists but doesn't check Node/Bun/Docker; the install scripts have shipped 5 bugs in 24 hours, each caught by fresh-clone testing — a clear signal that release attestation has been weak.
- **Tailwind v4 token leak**: motion + typography tokens declared in `:root` but not in `@theme {}`; many `duration-cinematic`, `text-mega` classes silently no-op. Apps render but less "cinematic" than designed.

**Repair plan**: 8 phases per the user's audit brief. Phase 2 fresh-clone simulation + Phase 3 frontend QA + Phase 5 CLI repair are the highest-impact next moves.

---

## 2. Repo inventory

### 2.1 Top-level structure

```
BeQuite/
├── README.md                         [shipped; 14k]  one-command install + 7-phase pitch
├── CHANGELOG.md                      [shipped; 148k] every release through alpha.5
├── CLAUDE.md                         Claude Code orientation
├── AGENTS.md                         Universal AI-agent orientation
├── LICENSE                           MIT
├── BEQUITE_BOOTSTRAP_BRIEF.md        Original brief (preserved verbatim)
├── BeQuite_MASTER_PROJECT.md         Expanded master file
├── docker-compose.yml                Three-service Docker stack (api/dashboard/marketing)
├── .dockerignore                     Root-level build-context filter
├── .gitignore                        Standard + .bequite/.keys + .bequite/.auth
├── .github/                          ci.yml + release.yml + commitlint
├── .bequite/                         Project's own Memory Bank + receipts + state
├── cli/                              Python CLI (bequite + bq commands)
├── studio/
│   ├── api/                          Hono on Bun (port 3002)
│   ├── dashboard/                    Next.js 15 ops console (port 3001)
│   ├── marketing/                    Next.js 15 cinematic landing (port 3000)
│   └── brand/                        Source-of-truth design tokens
├── skill/                            SKILL.md + agents + commands + hooks + templates
├── template/                         Repo template for `bequite init`
├── examples/                         Three example projects (bookings-saas, ai-tool-wrapper, tauri-note-app)
├── docs/                             Documentation (this audit lives here)
├── scripts/                          install + bootstrap + docker-up scripts
├── tests/integration/                Python integration suite (12 modules, 125+ tests)
├── evidence/                         Filesystem-level audit artifacts
├── prompts/                          Reusable prompt packs
└── state/                            Current operational state (recovery, current_phase, project.yaml)
```

### 2.2 Apps detected

| App | Path | Stack | Port | Purpose | Status |
|---|---|---|---|---|---|
| **CLI** | `cli/` | Python 3.11+ / click / pydantic / rich | n/a | The Harness (Layer 1) — 19+ subcommands | Production/Stable v1.0.3 |
| **API** | `studio/api/` | Hono 4 + Zod + Bun runtime | 3002 | Reads/writes `.bequite/` over HTTP; SSE event streams; terminal exec | alpha.5 |
| **Dashboard** | `studio/dashboard/` | Next.js 15 + Tailwind v4 + Framer Motion + xterm.js | 3001 | Operations console — phase board, receipts, live terminal | alpha.5 |
| **Marketing** | `studio/marketing/` | Next.js 15 + Tailwind v4 + Framer Motion 11 + R3F 9 + drei 10 + Three.js 0.171 | 3000 | Cinematic landing + 6 MDX vibecoder tutorials | alpha.5 |

### 2.3 Tracked manifests

| File | What | Issue (if any) |
|---|---|---|
| `cli/pyproject.toml` | hatchling build; deps; entry points | None — fixed v1.0.1 |
| `studio/api/package.json` | hono ^4.6; zod ^3.23; gray-matter ^4 | None |
| `studio/dashboard/package.json` | next 15.5; react 19; tailwind v4 beta.3; xterm | None — fixed v2.0.0-alpha.2 |
| `studio/marketing/package.json` | next 15.5; react 19; tailwind v4 beta.3; R3F 9; drei 10; three 0.171 | None — fixed v2.0.0-alpha.2 |
| **Root `package.json`** | n/a | **MISSING** — no `npm run dev` / `npm run verify` at repo root |
| **Root `Makefile`** | n/a | **MISSING** — no Unix one-command |
| **Root `.env.example`** | n/a | **MISSING** — operators don't know what env vars exist |

### 2.4 Ports allocation

| Port | Service | Notes |
|---|---|---|
| 3000 | marketing | Static Next.js |
| 3001 | dashboard | Next.js with SSE + xterm |
| 3002 | API | Hono on Bun |
| (none) | CLI | terminal-only |

**Note:** The user's audit brief mentioned port 3200 for the API. The actual code uses **3002**. This is a typo in the brief, not a real conflict — all documentation, Dockerfiles, and runtime config use 3002.

### 2.5 Install paths

| Method | Entry point | Status |
|---|---|---|
| Docker compose | `docker compose up --build` (repo root) | Works; first build hit README COPY bug at alpha.4, fixed in alpha.5 |
| Bootstrap (Windows) | `irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.ps1 \| iex` | Verified live in v1.0.3 |
| Bootstrap (Unix) | `curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.sh \| bash` | Logic mirrors PS; not live-tested in-session |
| Manual (`pip install -e ./cli`) | After `cd BeQuite` + venv activation | Verified live in v1.0.1 |
| `pip install bequite` from PyPI | n/a | **Not yet published** — one-way door; Ahmed-gated |

---

## 3. Doc inventory — what's referenced vs what exists

### 3.1 Existing docs

```
docs/
├── README.md                         (navigation entry)
├── QUICKSTART.md                     (5-minute path; drafted v0.14.0)
├── INSTALL.md                        (three-path install; drafted v1.0.1, updated v2.0.0-alpha.4)
├── HOW-IT-WORKS.md                   (architecture overview)
├── DOCTRINE-AUTHORING.md             (how to fork doctrines)
├── HOSTS.md                          (per-host install)
├── AUTONOMOUS-MODE.md                (auto-mode safety rails)
├── SECURITY.md                       (threat model + OWASP map)
├── MAINTAINER.md                     (release process)
├── RELEASES/
│   ├── v1.0.0.md
│   └── v2.0.0-alpha.1.md
├── architecture/
│   ├── CLI_AUTHENTICATION_STRATEGY.md  (ADR-011)
│   └── MULTI_MODEL_PLANNING_STRATEGY.md (ADR-012)
├── specs/                            (requirement docs)
├── merge/                            (master-file merge audit)
├── planning_runs/                    (multi-model planning artifacts)
├── audits/                           (THIS AUDIT lives here)
├── runbooks/                         (NEW; will be populated in Phase 6)
└── changelogs/                       (NEW; AGENT_LOG.md goes here in Phase 8)
```

### 3.2 References in code/docs that point at non-existent docs

| Referenced | Exists? | Action |
|---|---|---|
| `docs/INSTALL.md` | ✅ | none |
| `docs/QUICKSTART.md` | ✅ | none |
| `docs/RELEASES/v1.0.0.md` | ✅ | none |
| `docs/RELEASES/v2.0.0-alpha.1.md` | ✅ | none |
| **`docs/runbooks/LOCAL_DEV.md`** | ❌ | **Create in Phase 2** |
| **`docs/changelogs/AGENT_LOG.md`** | ❌ | **Create in Phase 8** |
| **`docs/audits/*.md`** (this set) | ❌ | **Creating now** |

---

## 4. Frontend UX issues (Phase 1 spot-check; Phase 3 confirms via Playwright)

These were found by **static-only inspection** of components. Each will be re-verified in Phase 3 with Playwright + screenshots.

### 4.1 Critical (dead clicks / broken navigation)

| # | Location | Issue | Fix |
|---|---|---|---|
| F-1 | `studio/marketing/components/Nav.tsx:42` | "How it works" link → `/#how-it-works` — **no component has `id="how-it-works"`**. Dead anchor. | Add `id="how-it-works"` to `PhasesScroll.tsx` (it's the spiritual target). |
| F-2 | `studio/marketing/components/Hero.tsx:105` | Same dead anchor `#how-it-works` on the secondary CTA button | Same fix as F-1 applies (one source of truth) |
| F-3 | `studio/dashboard/components/PhasesSidebar.tsx:52-58` | `<button>DEPLOY</button>` has **no `onClick` handler**. Looks fully functional. | Either remove the button or add a real handler that calls `POST /api/v1/terminal/exec` with `bequite handoff`. For now: add `disabled` + tooltip "Deploy lands v2.0.0-beta.1" to set expectations honestly. |

### 4.2 High (hardcoded mock data masquerading as live state)

| # | Location | Issue | Fix |
|---|---|---|---|
| F-4 | `studio/dashboard/components/PlanTasksTests.tsx:11-37` | `planItems`, `taskItems`, `testItems` are **hardcoded literals**. The component receives `snapshot: ProjectSnapshot` but only uses `snapshot.doctrineList[0]`. Looks like real project data; isn't. | Derive from `snapshot.phases`, parse `specs/<feature>/tasks.md` server-side, or display "(no plan loaded — run `bequite plan`)" honestly. |
| F-5 | `studio/dashboard/components/AgentPanel.tsx:63-67` | "Recent activity" list is hardcoded: `bequite verify ✓`, `bequite plan ✓`, `bequite freshness ✓`. Doesn't reflect actual receipts. | Replace with `snapshot.recentReceipts.slice(0, 3).map(...)` showing the actual last 3 phase commands from receipts. |
| F-6 | `studio/dashboard/components/CommandConsole.tsx:11-20` | Static-mode CommandConsole shows `DEFAULT_LINES` (hardcoded). This is the **filesystem-mode** terminal — HTTP mode swaps for the live `Terminal` component. **Make this honest:** add a header "Demo only — filesystem mode" so users don't think it's a live shell. | Add `<p>Demo • static</p>` banner OR replace filesystem-mode with a "Switch to HTTP mode for live terminal" CTA. |

### 4.3 Medium (visual + animation)

| # | Location | Issue | Fix |
|---|---|---|---|
| F-7 | `studio/marketing/components/Hero.tsx:61` | References `@keyframes glint` animation but **`@keyframes glint` is never defined**. The gold-bright star particles never animate. | Add `@keyframes glint { 0%, 100% { opacity: 0.2 } 50% { opacity: 0.7 } }` to `globals.css`. |
| F-8 | both apps' `globals.css` | Motion + typography tokens (`--ease-cinematic`, `--text-mega`, `--font-display`) declared in `:root` but **not in `@theme {}`** — Tailwind v4 doesn't pick them up. Classes `duration-cinematic`, `ease-cinematic`, `text-mega`, `font-display`, `tracking-mega` all silently no-op. | Mirror motion + type tokens into `@theme {}` blocks (add `--animate-cinematic`, `--font-display`, `--text-mega` etc. in v4-native naming). |
| F-9 | `studio/dashboard/components/CommandConsole.tsx:56` | `t.includes("⏳") ? "" : ""` — both branches return empty string. Dead conditional. | Either render the ⏳ glyph when present, or remove the dead conditional. |

### 4.4 Low (info / housekeeping)

| # | Location | Issue | Fix |
|---|---|---|---|
| F-10 | `studio/dashboard/components/TopBar.tsx:22` | `signedInUser = "(not signed in)"` hardcoded default; no real auth UI hooks up the value. | Acceptable for alpha — flag in audit; address with Better-Auth in v2.0.0-alpha.3 (per ADR-015). |
| F-11 | `studio/dashboard/tailwind.config.ts` | This v3-style file ships alongside `app/globals.css` v4 `@theme` block. Tailwind v4 ignores v3 configs by default. Dead file. | Either delete it or convert to a `@config` directive in CSS. |

---

## 5. API issues (Phase 1 static-only; Phase 4 confirms live)

The API has 8 modules under `src/lib/`, 7 routes under `src/routes/`, and a clean Hono entrypoint. From static inspection:

### 5.1 Strengths
- ✅ Path-traversal guard on every endpoint that takes `?path=`
- ✅ Iron Law X attestation helper used on every write endpoint
- ✅ Three-mode auth selectable by env (no hardcoded "always auth")
- ✅ Append-only writes (no DELETE/PUT — Article IV)
- ✅ Hardcoded exec allow-list (`bequite`, `bq`) per ADR-016
- ✅ SSE heartbeat + clean teardown on client abort
- ✅ Zod validation on every body

### 5.2 Issues to verify live (Phase 4)

| # | Location | Issue | Verification needed |
|---|---|---|---|
| A-1 | `studio/api/src/index.ts:14-28` | CORS: dev allows `http://localhost:*` + `http://127.0.0.1:*`, returns `null` for prod origins. Production allow-list deferred to v0.20.x+. | Browser preflight from dashboard works? |
| A-2 | `studio/api/src/index.ts:24` | `credentials: true` set; with `origin: callback` returning the requested origin, cookies *can* travel. No cookies are actually set today, but the config is forward-compatible. | Confirm no preflight error for non-cookie requests. |
| A-3 | `studio/api/src/routes/health.ts` | Returns `{ status, service, version, workspace_root, uptime_s }`. No error path tested. | Curl works (already verified Phase 0 of this session). Verify when workspace mount missing. |
| A-4 | `studio/api/src/routes/streams.ts` | EventSource auth uses `?token=` fallback. The query-param token is logged in some access-log scenarios (URL in HTTP request line). | Document this in SECURITY.md or move to a header-style approach. Acceptable for alpha; flag for beta. |
| A-5 | `studio/api/src/lib/exec-session.ts:230-240` | `kill()` on Windows: Node's `child.kill('SIGTERM')` is *advisory* on Windows — `taskkill /F /PID` is the reliable path. Current code may leave zombies on Windows. | Live-test on Windows: kick off a long `bequite auto` simulation, click Cancel, watch for exit_reason. |

---

## 6. CLI issues

### 6.1 Strengths
- ✅ 21 working subcommands wired via Click
- ✅ `bequite doctor` exists and produces a tabular diagnostic
- ✅ `bequite quickstart` shipped in v1.0.3 (friendly onboarding)
- ✅ UTF-8 stdout/stderr reconfigure (fixed v1.0.1)
- ✅ Per-project ed25519 keypair (signed receipts)
- ✅ 125+ Python integration tests pass

### 6.2 Issues

| # | Symptom | Root cause | Fix |
|---|---|---|---|
| C-1 | `bequite doctor` doesn't check Node, Bun, Docker availability | Doctor only checks Python + git + jq + scaffolding. Doesn't surface "the dashboard needs Node/Bun" gaps. | Extend `commands.run_doctor()` to add a "Studio runtime" section: node ≥20, pnpm ≥9, bun ≥1.1, docker daemon. |
| C-2 | No `bequite dev` command to bring up the whole stack | The dev experience currently requires three terminals OR `docker compose up`. CLI is unaware of the Studio. | Add `bequite dev` subcommand: detects docker → runs `docker compose up`; falls back to `concurrently`-style three-terminal launch. |
| C-3 | No `bequite status` shorthand for "is the API + dashboard reachable?" | Closest is `bequite doctor` but that's local-only checks. | Add `bequite status` that GETs `http://localhost:3002/healthz` + `:3001` + `:3000` and reports each. |
| C-4 | First-run hint is buried | `bequite quickstart` exists, but on `bequite init` success there's no "next: run `bequite quickstart`" nudge. | Add to `init` success handler. |
| C-5 | Errors are stack traces by default | Most subcommands let exceptions bubble. A vibecoder sees a Python traceback. | Wrap every subcommand body in a top-level try/except that prints a friendly `rich`-formatted error + the underlying message. Keep `--debug` flag for raw traces. |
| C-6 | No "spider" subcommand referenced in audit brief | The brief mentions `bequite spider` (probably means `scraping-engineer` from Article VIII). The CLI exposes `freshness` and `audit` but no top-level "spider" / scraping invocation. | Decide: either alias `bequite spider → bequite scrape` (new) OR document that scraping is a Doctrine-driven persona, not a CLI command. v1.0.3 docs say the latter. |

### 6.3 Install-path bugs caught in fresh-clone testing (last 24h)

| Tag | Bug | Verified end-to-end? |
|---|---|---|
| `v1.0.1` | `cli/README.md` missing — broke `pip install -e ./cli` | ✅ clean venv |
| `v1.0.2` | PowerShell `\"` parse bug — install.ps1 -Studio broke | ⚠️ logic-only |
| `v2.0.0-alpha.2` | R3F 8.x React 18 peer-dep — npm install marketing broke | ✅ 525 pkgs + tsc clean |
| `v1.0.3` | pip stderr halted install script | ✅ live iex test |
| `v2.0.0-alpha.3` | Turbopack cross-package CSS + `.js` extensions | ✅ both apps HTTP 200 |
| `v2.0.0-alpha.4` | Docker support | ⚠️ compose validate; live build deferred |
| `v2.0.0-alpha.5` | README COPY missing + wget healthcheck | ⚠️ structural; live deferred |

**Pattern:** 7 install-path bugs in 36 hours, all caught by **fresh-clone testing rather than developer-disk testing**. This audit's Phase 2 will run a single canonical "fresh-clone simulation" against all four install paths to catch any remaining issues before they bite a new user.

---

## 7. Test gaps

| Area | Coverage | Gap |
|---|---|---|
| Python CLI | **125+ tests across 12 modules** (receipts, signing, router, pricing, auth, auto-state, multi-model, exporters, skill-install, e2e/seven-phase-walk, e2e/doctrine-loading) — all green on Python 3.14 | Could be stronger: real CLI invocation tests (currently mostly module-level). |
| API HTTP | **None** | Need smoke tests against running API: `GET /healthz`, `GET /api/v1/projects`, `POST /api/v1/receipts` (with body), `GET /api/v1/streams/all` (SSE), `POST /api/v1/terminal/exec` (with RoE-Ack). Author in Phase 4. |
| Dashboard | **None** | Playwright smoke: page loads, LiveIndicator shows correct state, Terminal renders, footer mode chip displays correctly. Author in Phase 3. |
| Marketing | **None** | Playwright smoke: page loads, nav links scroll to real anchors (catches F-1, F-2), `/docs` and `/docs/quickstart` render. Author in Phase 3. |
| Lint / typecheck | API + dashboard + marketing all pass `tsc --noEmit` | No `eslint` or `biome` run in CI. |
| Build | `next build` per app works (Docker confirms) | No `npm run build` in CI yet (the `.github/workflows/ci.yml` covers Python only). |
| Full system | **None** | No e2e test that exercises CLI → API → dashboard together. |

---

## 8. Release blockers

For **v2.0.0-stable** (currently `v2.0.0-alpha.5`):

| # | Blocker | Severity | Fix in |
|---|---|---|---|
| B-1 | Frontend dead clicks (F-1, F-2, F-3) | High — affects every visitor | Phase 3 |
| B-2 | Hardcoded "live" panels (F-4, F-5) — dishonest UX | High — Article VI violation | Phase 3 |
| B-3 | No one-command dev (`npm run dev`, `make dev`, `bequite dev`) | Medium — friction for new contributors | Phase 6 |
| B-4 | Zero Playwright tests | Medium — every release ships without UI smoke | Phase 3 + 7 |
| B-5 | Live `docker compose up` not yet verified end-to-end in-session | Medium — alpha.5 was patched but never live-booted by me | Phase 7 |
| B-6 | Better-Auth integration deferred to alpha.3 (per ADR-015) | Medium for v2.0.0-beta.1 | Out of scope (deferred) |
| B-7 | Postgres mirror deferred to beta.1 | Low for alpha line | Out of scope |
| B-8 | PyPI publish not yet done | Low — Ahmed-gated one-way door | Out of scope |

---

## 9. Quick fixes (this audit ships these in Phase 2–7)

- ✅ Add `id="how-it-works"` to PhasesScroll (fixes F-1, F-2)
- ✅ Mark DEPLOY button as disabled with tooltip OR add real handler (fixes F-3)
- ✅ Replace hardcoded panel data with real `snapshot` fields (fixes F-4, F-5)
- ✅ Add CommandConsole "Demo only" banner in filesystem mode (fixes F-6)
- ✅ Add `@keyframes glint` to marketing globals.css (fixes F-7)
- ✅ Migrate motion/typography tokens into Tailwind v4 `@theme` blocks (fixes F-8)
- ✅ Remove dead conditional in CommandConsole (fixes F-9)
- ✅ Delete dead `tailwind.config.ts` from dashboard (fixes F-11)
- ✅ Extend `bequite doctor` with Node/Bun/Docker checks (fixes C-1)
- ✅ Add `bequite dev` + `bequite status` (fixes C-2, C-3)
- ✅ Wrap CLI commands in friendly error handler (fixes C-5)
- ✅ Author `.env.example` at repo root
- ✅ Author root `package.json` + `Makefile` (fixes B-3)
- ✅ Add Playwright smoke suite (fixes B-4)
- ✅ Live-verify `docker compose up` end-to-end (fixes B-5)

## 10. Larger fixes (deferred past this audit)

- DEPLOY button real implementation — needs ADR for "what does deploy mean in alpha"
- Project picker UI — currently hardcoded to `../..`
- Better-Auth wiring (per ADR-015 — v2.0.0-alpha.3+ on the existing roadmap)
- Postgres mirror (v2.0.0-beta.1)
- Multi-user / cloud auth-server (v2.0.0-beta.2)
- PyPI publish

---

## 11. Risky dependencies

| Dep | Version | Risk |
|---|---|---|
| `tailwindcss@^4.0.0-beta.3` | beta | Frequent breaking changes between betas. **Pin exact** before stable. |
| `@tailwindcss/postcss@^4.0.0-beta.3` | beta | Same. |
| `@xterm/xterm@^5.5.0` | stable | None known. |
| `@react-three/fiber@^9.0.0` | stable | Major bump from v8; we use stable subset only. |
| `@react-three/drei@^10.0.0` | stable | Some v9 helpers dropped (e.g. `ScrollControls` legacy mode). We don't use those. |
| `three@^0.171.0` | stable | None known. |
| `framer-motion@^11.11.0` | stable | None known. |
| `next@^15.0.0` | stable | Turbopack still maturing — be ready for surprises. |
| `react@^19.0.0` | stable | New; widely deployed by 2026. |
| `hono@^4.6.0` | stable | None known. |
| `bun@1.1` (Docker base) | stable | Pin to a specific minor in production. |
| `anthropic@^0.40.0` (Python) | stable | SDK actively maintained. |
| `cryptography@^42.0.0` (Python) | stable | None known. |

---

## 12. What this audit is NOT

- Not a code-style review (deferred to a separate review pass — Phase 8 will run `/review`)
- Not a security pentest (relies on Article IX + Doctrine `vibe-defense` which were authored separately)
- Not a load test (alpha scope is single-user dev)
- Not a multi-OS matrix run (this audit's live verification is Windows + Bash-on-Windows only; Linux/macOS CI runs the Python suite)

---

## 13. Phase 1 conclusion

The product **works** in the happy path but has identified UX + tooling gaps that this 8-phase audit will close. Phase 2 (fresh-clone simulation) starts next: actually run the install scripts + Docker path + per-app dev servers from a clean state and capture exit codes, response bodies, and any errors.

**No new env vars required.** Local-dev mode works out of the box.

**Next:** Phase 2 — fresh-clone simulation → `FRESH_INSTALL_AUDIT.md` + `.env.example` + `runbooks/LOCAL_DEV.md`.
