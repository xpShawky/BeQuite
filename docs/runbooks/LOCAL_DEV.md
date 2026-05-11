# BeQuite — Local Development Runbook

> The minimum-friction guide for running BeQuite locally. Three install paths, three run modes. Pick what fits.

---

## TL;DR (90 seconds)

```bash
git clone https://github.com/xpShawky/BeQuite.git
cd BeQuite
docker compose up --build
```

Wait ~60-90s for first build, then open:

| URL | What you'll see |
|---|---|
| http://localhost:3000 | Cinematic marketing landing |
| http://localhost:3000/docs | 6 vibecoder tutorial cards |
| http://localhost:3001 | Operations dashboard (HTTP mode, LiveIndicator green) |
| http://localhost:3002/healthz | `{"status":"ok",...}` |

Stop with `docker compose down`.

---

## Install paths (pick one)

### Path A — Docker (recommended for vibecoders)

```bash
git clone https://github.com/xpShawky/BeQuite.git
cd BeQuite
docker compose up --build
```

**Requires:** Docker Desktop running. https://www.docker.com/products/docker-desktop/

**What it does:** Builds three images (API on Bun, dashboard + marketing on Node 20) and brings them up wired together. First build ~60-90s. Subsequent runs use cache (~10s).

**Convenience helper:**

```powershell
# Windows
.\scripts\docker-up.ps1            # foreground
.\scripts\docker-up.ps1 -Detach    # background
.\scripts\docker-up.ps1 -Down      # stop
```

```bash
# macOS / Linux
./scripts/docker-up.sh             # foreground
./scripts/docker-up.sh --detach    # background
./scripts/docker-up.sh --down      # stop
```

### Path B — Bootstrap (CLI only, native)

For users who only want the `bequite` Python CLI and don't need the visual surface:

```powershell
# Windows
irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.ps1 | iex
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.sh | bash
```

**Requires:** Python 3.11+ and git. Script prints install hints if either is missing.

### Path C — Manual (full control, for contributors)

```bash
git clone https://github.com/xpShawky/BeQuite.git
cd BeQuite

# CLI
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# Unix:    source .venv/bin/activate
pip install -e ./cli
bequite --version            # → 1.0.3+

# Studio API (Bun, port 3002)
cd studio/api
bun install
bun run src/index.ts &

# Studio dashboard (Node, port 3001)
cd ../dashboard
npm install
BEQUITE_DASHBOARD_MODE=http npm run dev &

# Studio marketing (Node, port 3000)
cd ../marketing
npm install
npm run dev &
```

---

## Daily-driver commands

After install, every new terminal needs venv activation (Path B or C):

```bash
# Windows
.\.venv\Scripts\Activate.ps1

# Unix
source ./.venv/bin/activate
```

Then:

```bash
bequite quickstart                              # friendly onboarding
bequite doctor                                  # environment + scaffolding check
bequite init my-app --doctrine default-web-saas # scaffold a new project
cd my-app
bequite auto --feature "add health endpoint"   # full 7-phase workflow
```

---

## Service map

| Service | Path | Port | Purpose |
|---|---|---|---|
| **marketing** | `studio/marketing/` | 3000 | Cinematic landing + 6 MDX vibecoder tutorials at `/docs` |
| **dashboard** | `studio/dashboard/` | 3001 | Operations console — phases sidebar + plan/tasks/tests + xterm terminal + LiveIndicator |
| **api** | `studio/api/` | 3002 | Hono on Bun back-end — auth + reads + writes + SSE streams + terminal exec |
| **CLI** | `cli/` | n/a | Python `bequite` + `bq` console scripts |

---

## Mode chart

| Where you are | Dashboard reads from | LiveIndicator | Terminal works? |
|---|---|---|---|
| Docker compose (default) | API container | LIVE | Yes |
| Native, all 3 apps running | API @ localhost:3002 | LIVE | Yes |
| Native, only dashboard | filesystem (`.bequite/` on host) | FS | No (no remote process to spawn) |
| Native, API down | API unreachable | OFFLINE | No |

---

## Verification — is it really working?

After install, run these in order. If any step fails, see Troubleshooting below.

### CLI check

```bash
bequite --version                # → bequite, version 1.0.3+
bequite --help                   # → command list (no UnicodeError on Windows)
bequite doctor                   # → tabular environment check
```

### Browser checks (when Docker compose or all-three is running)

| URL | Expected |
|---|---|
| http://localhost:3002/healthz | `{"status":"ok","service":"bequite-api","version":"0.20.5",...}` |
| http://localhost:3002/api/v1/auth/status | `{"mode":"local-dev",...}` |
| http://localhost:3000 | Gold logo top-left, "Plan it. Build it. Be quiet." hero with gold "Be quiet." gradient |
| http://localhost:3000/docs | 6 cards: quickstart, from-scratch, retrofit, multi-model-planning, auto-mode, troubleshooting |
| http://localhost:3001 | TopBar with `LIVE` pill (green) + `HTTP` chip in footer + xterm Terminal in CommandConsole position |

### Curl checks (no browser needed)

```bash
curl http://localhost:3002/healthz
curl http://localhost:3002/api/v1/projects
curl http://localhost:3002/api/v1/projects/snapshot
curl -I http://localhost:3000
curl -I http://localhost:3001
```

All should return HTTP 200.

---

## Troubleshooting

### Docker

| Symptom | Cause | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop not running | Start Docker Desktop; wait for the whale icon to say "Engine running" |
| `dependency failed to start: container bequite-api is unhealthy` (and you're on alpha.5 or earlier) | Stale healthcheck cached in image | Run `docker compose down && docker compose build --no-cache && docker compose up -d`. Permanent fix shipped in v2.0.0-alpha.6+. |
| `Port 3000 / 3001 / 3002 is already in use` | A local dev server is still running | Stop the local one: `pnpm exit` or `Stop-Process -Id <pid>`. Or stop existing containers: `docker compose down` |
| Dashboard shows `OFFLINE` chip | API container is down | `docker logs bequite-api` to see why; `docker compose restart api` |

### Native install (Path B / C)

| Symptom | Cause | Fix |
|---|---|---|
| `ERROR: .\cli is not a valid editable requirement` | You're not inside the BeQuite/ directory | `cd BeQuite` first |
| `bequite: command not found` | Venv not activated | `.\.venv\Scripts\Activate.ps1` (Win) or `source .venv/bin/activate` (Unix) |
| `UnicodeEncodeError: 'charmap' codec can't encode character '→'` | Pre-1.0.1 install | `pip install -e ./cli --force-reinstall` (v1.0.1+ fixes this) |
| `npm install` in marketing fails with ERESOLVE React 19 conflict | Pre-v2.0.0-alpha.2 lockfile | `git pull origin main` then `rm -rf node_modules package-lock.json && npm install` |
| Dashboard or marketing crashes with `TurbopackInternalError` | Pre-v2.0.0-alpha.3 globals.css | `git pull origin main` then restart `npm run dev` |

### PowerShell-specific gotchas

| Symptom | Fix |
|---|---|
| `The token '&&' is not a valid statement separator` | You're on PowerShell 5.1 (default Windows). Use `;` or two separate lines instead of `&&` |
| `running scripts is disabled on this system` | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `bun: command not found` after install | Close and reopen PowerShell to refresh PATH |

---

## Environment variables

See [`.env.example`](../../.env.example) at the repo root for the full list.

**You don't need any env vars for local-dev mode.** All defaults work.

If you want to switch to **token-mode auth**:

```bash
# In one terminal — start API in local-dev to bootstrap
BEQUITE_AUTH_MODE=local-dev bun run src/index.ts

# In another — mint a token
curl -X POST http://localhost:3002/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"label":"dashboard-local"}'
# → save the token from the response

# Restart API in token mode
BEQUITE_AUTH_MODE=token bun run src/index.ts

# Restart dashboard with token
NEXT_PUBLIC_BEQUITE_API_TOKEN=<token> npm run dev
```

---

## Tearing down

### Docker

```bash
docker compose down                  # stop + remove containers, keep images
docker compose down --rmi all        # also remove the bequite-* images
docker image prune                   # remove unused dangling images
```

### Native

```bash
# Each terminal: Ctrl+C to stop its dev server.
# Then deactivate the venv:
deactivate
```

### Reset to a clean clone

```bash
cd ..
rm -rf BeQuite                       # nuke everything
git clone https://github.com/xpShawky/BeQuite.git
cd BeQuite
docker compose up --build            # or your preferred install path
```

---

## What's next

- **CLI users:** `bequite quickstart` for the friendly first-time guide.
- **Studio users:** http://localhost:3000/docs for the 6 deep tutorials.
- **Contributors:** see `docs/RELEASES/v1.0.0.md` for what's stable + `docs/audits/` for the latest audit reports.

For the architectural overview, see [`docs/HOW-IT-WORKS.md`](../HOW-IT-WORKS.md). For the install paths in more detail, see [`docs/INSTALL.md`](../INSTALL.md).
