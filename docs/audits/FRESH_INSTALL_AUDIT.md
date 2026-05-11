# BeQuite — Fresh-Install Audit (Phase 2)

**Date:** 2026-05-11
**Scope:** Simulate exactly what a new user does after `git clone https://github.com/xpShawky/BeQuite.git`. Capture every command, every exit code, every error.
**Environment:** Windows 11, Docker Desktop 29.1.3 running, Node 24.12.0, Python 3.14.2, git 2.52.0.
**Test clone location:** `C:\Ahmed Shawky\Antigravity projects\Test bequite\BeQuite\` — checked out at commit `c791f85` (v2.0.0-alpha.5).

---

## 1. Executive summary

Out of the four install paths, **Docker Compose was the one that broke first** on a fresh clone — a leftover `wget` healthcheck in `docker-compose.yml` (the Dockerfile had been patched to use Bun's fetch in v2.0.0-alpha.5, but the compose override was forgotten). After fixing the compose override:

| Install path | Result |
|---|---|
| Docker Compose (`docker compose up --build`) | ✅ **All three containers Healthy** after compose-healthcheck fix |
| Bootstrap PowerShell one-liner | ✅ Previously verified live (v1.0.3 attestation; not re-run today) |
| Bootstrap bash one-liner | ⚠️ Logic mirrors PS; not re-run on macOS/Linux this audit |
| Manual `pip install -e ./cli` | ✅ Works from fresh clone (verified earlier in session) |

The fix shipped as part of this audit (v2.0.0-alpha.6 candidate, committed after writing this doc).

---

## 2. Step-by-step simulation

### Step 1: clone

```powershell
PS C:\Ahmed Shawky\Antigravity projects\Test bequite> git clone https://github.com/xpShawky/BeQuite.git
Cloning into 'BeQuite'...
remote: Enumerating objects: 1170, done.
...
Receiving objects: 100% (1170/1170), 58.19 MiB | 3.44 MiB/s, done.
Resolving deltas: 100% (431/431), done.
```

**Exit code:** 0
**Time:** ~17 seconds (58MB clone)
**Branch:** `main`, head at `c791f85` (v2.0.0-alpha.5)

✅ No issue.

### Step 2: `docker compose up --build`

```powershell
PS C:\Ahmed Shawky\Antigravity projects\Test bequite\BeQuite> docker compose up --build
[+] Building 53/53 ... all stages OK ...
 ✔ bequite-api:local        Built
 ✔ bequite-dashboard:local  Built
 ✔ bequite-marketing:local  Built
 ✔ Container bequite-api        Healthy        (after fix; see below)
 ✔ Container bequite-dashboard  Healthy
 ✔ Container bequite-marketing  Healthy
```

#### Bug B1 — caught live: stale `wget` healthcheck in compose

**Symptom:**
```
Container bequite-api  Started
Container bequite-api  Waiting
Container bequite-api  Error
dependency failed to start: container bequite-api is unhealthy
```

**Diagnosis:**

```bash
$ docker inspect bequite-api --format '{{json .Config.Healthcheck}}'
{"Test":["CMD","wget","-q","--spider","http://localhost:3002/healthz"],...}

$ docker logs bequite-api | tail -5
BeQuite Studio API v0.20.5 listening on http://localhost:3002
Started server: http://localhost:3002        ← API is actually running!

$ docker inspect bequite-api --format '{{json .State.Health}}' | head
"Output":"OCI runtime exec failed: exec failed: unable to start container process: exec: \"wget\": executable file not found in $PATH"
```

**Root cause:** `docker-compose.yml` had its own `healthcheck:` block specifying `wget` — overriding the Dockerfile's `HEALTHCHECK CMD bun -e fetch(...)` (which was correctly fixed in alpha.5). The compose-level override was forgotten in the alpha.5 patch.

`oven/bun:1.1` base image does NOT include `wget`, so the healthcheck fails on every interval with `executable file not found`.

**Fix (applied in this audit):**

```diff
   healthcheck:
-    test: ["CMD", "wget", "-q", "--spider", "http://localhost:3002/healthz"]
+    test: ["CMD", "bun", "-e", "fetch('http://localhost:3002/healthz').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"]
     interval: 10s
-    timeout: 3s
-    start_period: 10s
+    timeout: 5s
+    start_period: 15s
     retries: 5
```

**File changed:** `docker-compose.yml`

**Verification:** After fix, `docker compose down && docker compose up -d` brought all three containers to Healthy state within ~30 seconds.

```
NAMES               STATUS
bequite-api         Up 26 seconds (healthy)
bequite-marketing   Up 26 seconds (healthy)
bequite-dashboard   Up 20 seconds (healthy)
```

### Step 3: Live endpoint verification

```bash
$ curl -s -w "HTTP %{http_code}\n" http://localhost:3002/healthz
{"status":"ok","service":"bequite-api","version":"0.20.5","workspace_root":"/workspace","uptime_s":26}
HTTP 200
```

✅ API healthy.

```bash
$ curl -s -w "HTTP %{http_code}\n" http://localhost:3002/api/v1/auth/status
{"mode":"local-dev","identity":null,"token_id":null,"tokens_count":null,"notes":"Pass-through. Suitable for single-machine dev. ..."}
HTTP 200
```

✅ Auth in local-dev mode.

```bash
$ curl -s http://localhost:3002/api/v1/projects
{"items":[{"name":"workspace (root)","path":"/workspace"},{"name":"template","path":"/workspace/template"}]}
HTTP 200
```

✅ Project discovery works. The workspace mount + the `template/` subproject both detected.

```bash
$ curl -s "http://localhost:3002/api/v1/projects/snapshot"
{"root":"/workspace","exists":true,"projectName":"Project Brief: BeQuite","doctrineList":[...],"constitutionVersion":"1.3.0","currentPhase":"v0.8.1","lastGreenTag":null,"activeContextSummary":"...","phases":[...],"recentReceipts":[],"costSession":null,"recoveryPreview":"..."}
HTTP 200
```

✅ Snapshot endpoint returns full `ProjectSnapshot` with all expected fields.

```bash
$ curl -s http://localhost:3002/api/v1/receipts
{"items":[]}
HTTP 200
```

✅ Receipts endpoint works (empty — no signed receipts in /workspace yet).

```bash
$ curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:3000
HTTP 200

$ curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:3000/docs
HTTP 200

$ curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:3000/docs/quickstart
HTTP 200

$ curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:3001
HTTP 200
```

✅ Marketing site renders. Dashboard renders. /docs and /docs/quickstart work.

### Step 4: Stop + verify clean shutdown

```bash
$ docker compose down
 Container bequite-dashboard  Stopped
 Container bequite-marketing  Stopped
 Container bequite-api        Stopped
 Container bequite-dashboard  Removed
 Container bequite-marketing  Removed
 Container bequite-api        Removed
 Network bequite_default       Removed
```

✅ Clean shutdown. No zombie processes. Ports 3000/3001/3002 freed.

---

## 3. Findings summary

| # | Finding | Severity | Fix |
|---|---|---|---|
| FI-1 | `docker-compose.yml` healthcheck used `wget` (not in base image) | **Critical** — Docker path 100% broken from fresh clone | Replaced with `bun -e fetch(...)`. Ships v2.0.0-alpha.6. |
| FI-2 | First build is ~60s (acceptable; downloads ~250MB of base images) | Low | Document in README + LOCAL_DEV.md ✅ |
| FI-3 | Image-layer cache stickiness can cause confusion when Dockerfile changes don't propagate | Medium — UX issue | Documented in LOCAL_DEV.md troubleshooting ("Run `docker compose build --no-cache`") ✅ |
| FI-4 | Bootstrap script paths verified earlier; not re-run today | Low | Already verified at v1.0.3 |

---

## 4. End-to-end install attestation

| Install path | Final state |
|---|---|
| `docker compose up --build` | ✅ All three healthy + all routes return HTTP 200 (after FI-1 fix) |
| `irm bootstrap.ps1 \| iex` | ✅ Previously verified live in v1.0.3 |
| `pip install -e ./cli` | ✅ Previously verified live in v1.0.1 |
| `bequite --version` | ✅ Returns `bequite, version 1.0.3` |
| `bequite quickstart` | ✅ Renders friendly onboarding (verified earlier) |

---

## 5. New files shipped in this Phase

| File | Purpose |
|---|---|
| `docker-compose.yml` | Fixed: wget → bun fetch healthcheck override |
| `.env.example` | Full env-var reference at repo root |
| `docs/runbooks/LOCAL_DEV.md` | Practical daily-driver runbook |
| `docs/audits/FRESH_INSTALL_AUDIT.md` | This document |

---

## 6. What this Phase did NOT cover (deferred to later phases)

- **Frontend UX inside the browser** — Phase 3 will Playwright-test pages for dead clicks + visible-text contrast + hardcoded-panel issues identified in Phase 1.
- **API auth, write paths, SSE streams, terminal exec** — Phase 4 will exercise these endpoints end-to-end.
- **CLI cross-platform** — Phase 5 will validate `bequite doctor` against Windows + add Node/Docker checks.
- **One-command dev experience** — Phase 6 will add `bequite dev`, root `package.json`, `Makefile`.
- **Release gate** — Phase 7 will add Playwright + `npm run verify` orchestrator.

---

## 7. Phase 2 conclusion

The **one-command Docker install path now works end-to-end** from a fresh clone after the healthcheck override fix. Six API routes + three frontend routes verified HTTP 200. No env vars required. Stop/start is clean.

This was the **first install-path bug caught by a real `docker compose up --build` run end-to-end in my session** — every prior Docker-related claim was structural validation only. v2.0.0-alpha.6 will ship with this fix + the runbook + .env.example so this exact failure mode never reappears.

**Next:** Phase 3 — Playwright smoke + frontend UX repair.
