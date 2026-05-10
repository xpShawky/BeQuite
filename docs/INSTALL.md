# Installing BeQuite from a fresh clone

This guide covers installing BeQuite from a clean GitHub clone on Windows, macOS, and Linux. Two layers, pick what you need:

- **Layer 1 — Harness CLI** (`bequite` + `bq`) — Python, ~5MB install, all you need to scaffold + run BeQuite-managed projects from the terminal.
- **Layer 2 — Studio Edition** — three Next.js + Hono apps (marketing site / dashboard / API). Adds a visual surface; optional.

> **Status:** v1.0.1+. Per-PyPI publish (`pip install bequite` from the public registry) is **not yet active** — Ahmed pushes the wheel manually (one-way door per Article IV). Today the canonical install path is "clone + install from source." This doc covers that path; once the wheel is on PyPI the top-level `pip install bequite` will Just Work.

---

## One-command install

We ship two install scripts:

| Platform | Script |
|---|---|
| **Windows** (PowerShell 5.1 or 7+) | `scripts\install.ps1` |
| **macOS / Linux** | `scripts/install.sh` |

### Windows (PowerShell)

```powershell
git clone https://github.com/xpShawky/BeQuite.git
cd BeQuite
.\scripts\install.ps1               # CLI only
# or
.\scripts\install.ps1 -Studio       # CLI + Studio (marketing + dashboard + API)
```

If you get a script-execution policy error:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### macOS / Linux (bash)

```bash
git clone https://github.com/xpShawky/BeQuite.git
cd BeQuite
chmod +x ./scripts/install.sh
./scripts/install.sh                # CLI only
# or
./scripts/install.sh --studio       # CLI + Studio
```

Both scripts:
1. Check prerequisites (Python ≥ 3.11, git).
2. Create a venv at `.venv` in the repo root.
3. Activate it.
4. `pip install -e ./cli` — installs the CLI in editable mode.
5. Verify `bequite --version` succeeds.
6. (With `--Studio` / `--studio`) install `pnpm install` + `bun install` for the three Studio apps.

---

## Prerequisites

### For the CLI (Layer 1) — minimum

| Tool | Min version | Install |
|---|---|---|
| Python | 3.11 | https://python.org · `winget install Python.Python.3.12` · `brew install python@3.12` · `apt install python3.12` |
| git | any | https://git-scm.com |

### For the Studio (Layer 2) — additionally

| Tool | Min version | Install |
|---|---|---|
| Node.js | 20 | https://nodejs.org · `winget install OpenJS.NodeJS.LTS` · `brew install node` |
| pnpm | 9 | `npm install -g pnpm` (or use `npm install` as fallback) |
| Bun | 1.1 | https://bun.sh · `powershell -c "irm bun.sh/install.ps1 \| iex"` (Windows) · `curl -fsSL https://bun.sh/install \| bash` (mac/linux) |

Verify:
```bash
python --version    # ≥ 3.11
node --version      # ≥ 20
pnpm --version      # ≥ 9
bun --version       # ≥ 1.1
git --version       # any
```

---

## Manual install (if the script doesn't fit your flow)

### Layer 1 (CLI)

```bash
# 1. Clone
git clone https://github.com/xpShawky/BeQuite.git
cd BeQuite

# 2. Venv (cleanly isolates from system Python)
python -m venv .venv

# 3. Activate
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows cmd:
.\.venv\Scripts\activate.bat
# macOS / Linux:
source .venv/bin/activate

# 4. Install
pip install -e ./cli

# 5. Verify
bequite --version
bequite --help
bequite doctor
```

> **Common mistake:** running `pip install -e .\cli` from one directory ABOVE the cloned repo. Make sure you `cd BeQuite` first — `cli/` lives inside the clone.

### Layer 2 (Studio)

**Three apps, three terminals.** They don't depend on each other to boot, but the dashboard's HTTP mode + LiveIndicator need the API running.

```bash
# Terminal 1 — API on :3002 (Hono on Bun)
cd studio/api
bun install
bun run src/index.ts

# Terminal 2 — Dashboard on :3001 (Next.js)
cd studio/dashboard
pnpm install
# Or: npm install

# Filesystem mode (single-machine; doesn't need the API):
pnpm dev

# HTTP mode (talks to the API on :3002):
#   Windows PowerShell:
$env:BEQUITE_DASHBOARD_MODE = "http"; pnpm dev
#   macOS / Linux:
BEQUITE_DASHBOARD_MODE=http pnpm dev

# Terminal 3 — Marketing site on :3000 (Next.js)
cd studio/marketing
pnpm install
pnpm dev
```

---

## Verify it all works

| URL | Expected |
|---|---|
| http://localhost:3000 | Cinematic landing (gold-on-black brand) |
| http://localhost:3000/docs | 6 vibecoder tutorial cards |
| http://localhost:3000/docs/quickstart | Full quickstart MDX |
| http://localhost:3001 | Operations dashboard. Mode chip in footer = `FS` or `HTTP`. |
| http://localhost:3002 | API metadata JSON |
| http://localhost:3002/healthz | `{"status":"ok",...,"version":"0.20.5",...}` |
| http://localhost:3002/api/v1/auth/status | `{"mode":"local-dev",...}` |

In the dashboard at `http://localhost:3001` (HTTP mode), the CommandConsole is a live xterm.js Terminal. Type:
```
bequite --version
```
Click **Run**. Output streams within ~250ms. Exit status appears as `[exit 0 · <ms>ms]`. A signed receipt is written to `.bequite/receipts/<sha>-EXEC.json`.

---

## Common errors and fixes

### `pip install bequite` → "No matching distribution found"

The wheel isn't on PyPI yet. Use the from-source path above. Once Ahmed publishes v1.0.x to PyPI, `pip install bequite` / `uvx bequite` / `pipx install bequite` will work.

### `pip install -e ./cli` → "is not a valid editable requirement"

You're not inside the cloned `BeQuite/` directory. `cd BeQuite` first, then re-run.

### `pip install -e ./cli` → "Readme file does not exist: README.md"

Fixed in v1.0.1+. Pull latest main:
```bash
git pull origin main
```

### `bequite --help` on Windows → `UnicodeEncodeError: 'charmap' codec can't encode character '→'`

Fixed in v1.0.1+ (`__main__.py` now reconfigures stdout/stderr to UTF-8 at startup). Pull latest main, reinstall:
```bash
git pull origin main
pip install -e ./cli --force-reinstall
```

### `bequite: command not found` after pip install

You're not in the activated venv, or the venv's Scripts/bin directory isn't on PATH.
```bash
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate
```

Alternative if PATH is a permanent problem: invoke via the module path:
```bash
python -m bequite --version
```

### PowerShell 5.1 → `The token '&&' is not a valid statement separator`

PowerShell 5.1 (the default Windows install) doesn't support `&&`. Replace with `;` (always run) or `; if ($?) {...}` (only-if-success):
```powershell
# Instead of: cmd1 && cmd2
cmd1; if ($?) { cmd2 }
# Or just use two lines.
```

PowerShell 7+ (`pwsh`) supports `&&` natively.

### Bun not found on Windows after install

The install script puts Bun at `%USERPROFILE%\.bun\bin\bun.exe` but doesn't restart your shell. Close + reopen PowerShell, then `bun --version` should work.

### Dashboard LiveIndicator shows `OFFLINE`

The Studio API isn't running on `:3002`. Start it in another terminal:
```bash
cd studio/api && bun run src/index.ts
```

### `pnpm install` on Windows → `EPERM` error

Usually means VS Code or another process is holding a file. Close VS Code, retry. Worst case:
```powershell
Remove-Item -Recurse -Force node_modules
pnpm install
```

---

## Optional: install BeQuite into other hosts

The CLI ships with per-host adapters. After installing:

```bash
# In any BeQuite-managed project:
bequite skill install --host cursor
bequite skill install --host codex
bequite skill install --host cline
# ... or just `bequite skill install` to auto-detect.
```

Supported hosts: `claude-code`, `cursor`, `codex`, `cline`, `kilo`, `continue`, `aider`, `windsurf`, `gemini`.

---

## What's next

- **Read the brand-new tutorials** at http://localhost:3000/docs once the marketing site is running. Six deep ~250-line MDX guides cover quickstart, retrofit, multi-model planning, auto-mode, troubleshooting.
- **Initialize a project** — `bequite init my-app --doctrine default-web-saas --scale small_saas`.
- **Run the full 7-phase workflow** — `bequite auto --feature "your feature" --max-cost-usd 10`.

For per-version detail, see [`CHANGELOG.md`](../CHANGELOG.md). For the v1.0.0 release notes, see [`docs/RELEASES/v1.0.0.md`](RELEASES/v1.0.0.md).
