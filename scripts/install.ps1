<#
.SYNOPSIS
  One-command install for BeQuite on Windows (PowerShell 5.1 and 7+).

.DESCRIPTION
  Vibecoder-friendly. Detects missing prerequisites, prints a clear install
  hint, then continues. Never fatal-errors on benign pip/npm stderr warnings.

  - Verifies prerequisites (Python 3.11+, git).
  - Creates a venv in the current directory.
  - Installs the Layer 1 Harness CLI (bequite + bq) in editable mode.
  - Optionally installs the Layer 2 Studio dependencies (pnpm + bun).

  Run from inside a cloned BeQuite repo. For a truly one-command experience
  that includes cloning, use scripts\bootstrap.ps1 instead (or the README
  one-liner).

.PARAMETER Studio
  Also install Layer 2 Studio dependencies (Bun for api/, pnpm/npm for
  dashboard/ + marketing/). Skipped by default for a quick CLI-only install.

.PARAMETER VenvName
  Name of the venv directory. Default: .venv

.EXAMPLE
  # CLI only (most users)
  .\scripts\install.ps1

.EXAMPLE
  # CLI + Studio surfaces
  .\scripts\install.ps1 -Studio
#>
[CmdletBinding()]
param(
  [switch]$Studio = $false,
  [string]$VenvName = ".venv"
)

# Continue on errors so we can give the user a clean failure message rather
# than letting PowerShell halt on a pip stderr warning. We check
# $LASTEXITCODE explicitly after every critical native command.
$ErrorActionPreference = "Continue"

function Write-Section($text) {
  Write-Host ""
  Write-Host "==> $text" -ForegroundColor Yellow
}

function Test-Command($cmd) {
  $null = Get-Command $cmd -ErrorAction SilentlyContinue
  return $?
}

function Exit-Fatal($msg) {
  Write-Host ""
  Write-Host "FATAL: $msg" -ForegroundColor Red
  Write-Host ""
  exit 1
}

# Run a native command, suppress noise, fail loudly if exit code is non-zero.
function Invoke-Native($description, [scriptblock]$block) {
  & $block
  if ($LASTEXITCODE -ne 0) {
    Exit-Fatal "$description failed (exit $LASTEXITCODE)"
  }
}

# --- 1. Prereq checks -------------------------------------------------------

Write-Section "Checking prerequisites"

if (-not (Test-Command python)) {
  Write-Host ""
  Write-Host "Python is not on PATH. To install:" -ForegroundColor Red
  Write-Host "  Option 1 (easiest):  Install from https://python.org (one-click installer)" -ForegroundColor Yellow
  Write-Host "  Option 2 (winget):   winget install Python.Python.3.12" -ForegroundColor Yellow
  Write-Host "  Option 3 (uv):       irm https://astral.sh/uv/install.ps1 | iex" -ForegroundColor Yellow
  Write-Host ""
  Write-Host "After install, CLOSE + REOPEN PowerShell so Python lands on PATH, then re-run this script." -ForegroundColor Yellow
  exit 1
}
$pyVersion = (python --version) 2>&1 | Out-String
Write-Host "  Python: $($pyVersion.Trim())"

if (-not (Test-Command git)) {
  Write-Host ""
  Write-Host "Git is not on PATH. To install:" -ForegroundColor Red
  Write-Host "  Option 1 (winget):    winget install Git.Git" -ForegroundColor Yellow
  Write-Host "  Option 2 (installer): https://git-scm.com/download/win" -ForegroundColor Yellow
  Write-Host ""
  exit 1
}
Write-Host "  Git:    $((git --version) 2>&1)"

if ($Studio) {
  if (-not (Test-Command node)) {
    Write-Host "  Node:   not on PATH (needed for Studio dashboard + marketing)." -ForegroundColor Yellow
    Write-Host "          Install with: winget install OpenJS.NodeJS.LTS" -ForegroundColor Yellow
    Write-Host "          Or from: https://nodejs.org" -ForegroundColor Yellow
  } else {
    Write-Host "  Node:   $((node --version) 2>&1)"
  }
  if (-not (Test-Command pnpm)) {
    Write-Host "  pnpm:   not on PATH (will fall back to npm install)" -ForegroundColor Yellow
  } else {
    Write-Host "  pnpm:   $((pnpm --version) 2>&1)"
  }
  if (-not (Test-Command bun)) {
    Write-Host '  bun:    not on PATH (needed for Studio API only).' -ForegroundColor Yellow
    Write-Host '          Install with this one-liner (then CLOSE+REOPEN PowerShell):' -ForegroundColor Yellow
    Write-Host '            powershell -c "irm bun.sh/install.ps1 | iex"' -ForegroundColor Yellow
  } else {
    Write-Host "  Bun:    $((bun --version) 2>&1)"
  }
}

# Sanity check we're in a BeQuite repo.
if (-not (Test-Path ".\cli\pyproject.toml")) {
  Exit-Fatal "cli\pyproject.toml not found. Run this script from inside a cloned BeQuite repo (`cd BeQuite`), or use scripts\bootstrap.ps1 for a clone+install in one shot."
}

# --- 2. Venv + CLI install -------------------------------------------------

Write-Section "Creating venv at .\$VenvName"
if (-not (Test-Path ".\$VenvName")) {
  Invoke-Native "venv creation" { python -m venv $VenvName }
} else {
  Write-Host "  (already exists; reusing)"
}

Write-Section "Activating venv"
$activate = Join-Path (Get-Location) "$VenvName\Scripts\Activate.ps1"
if (-not (Test-Path $activate)) {
  Exit-Fatal "venv activation script not found at $activate"
}
. $activate
Write-Host "  active: $env:VIRTUAL_ENV"

Write-Section "Upgrading pip (warnings ignored)"
# pip's cache warnings go to stderr; suppress them so the script doesn't bail.
python -m pip install --upgrade pip --quiet 2>$null
# pip writes nothing meaningful to exit code when --quiet succeeds, so don't
# treat a non-zero exit here as fatal (the install below catches real
# breakage).

Write-Section "Installing bequite CLI (editable)"
pip install -e .\cli 2>&1 | ForEach-Object { Write-Host "  $_" }
if ($LASTEXITCODE -ne 0) {
  Exit-Fatal "pip install -e .\cli failed (exit $LASTEXITCODE). See output above."
}

Write-Section "Verifying bequite CLI"
$version = (bequite --version) 2>&1 | Out-String
$version = $version.Trim()
Write-Host "  $version"
if ($version -notmatch "bequite, version") {
  Exit-Fatal "bequite did not report a version. Got: $version"
}

# --- 3. Optional Studio install --------------------------------------------

if ($Studio) {
  if (Test-Command bun) {
    Write-Section "Installing Studio API dependencies (Bun)"
    Push-Location ".\studio\api"
    bun install 2>&1 | ForEach-Object { Write-Host "  $_" }
    $bunExit = $LASTEXITCODE
    Pop-Location
    if ($bunExit -ne 0) {
      Write-Host "  WARNING: bun install exited $bunExit. The API may not boot." -ForegroundColor Yellow
    }
  } else {
    Write-Section "Skipping Studio API (bun not on PATH)"
    Write-Host "  Install Bun, then re-run with -Studio to install /studio/api/ deps." -ForegroundColor Yellow
  }

  $pkgMgr = if (Test-Command pnpm) { "pnpm" } else { "npm" }

  Write-Section "Installing Studio Dashboard dependencies ($pkgMgr)"
  Push-Location ".\studio\dashboard"
  & $pkgMgr install 2>&1 | ForEach-Object { Write-Host "  $_" }
  $dashExit = $LASTEXITCODE
  Pop-Location
  if ($dashExit -ne 0) {
    Write-Host "  WARNING: $pkgMgr install exited $dashExit in studio\dashboard." -ForegroundColor Yellow
  }

  Write-Section "Installing Studio Marketing dependencies ($pkgMgr)"
  Push-Location ".\studio\marketing"
  & $pkgMgr install 2>&1 | ForEach-Object { Write-Host "  $_" }
  $mktExit = $LASTEXITCODE
  Pop-Location
  if ($mktExit -ne 0) {
    Write-Host "  WARNING: $pkgMgr install exited $mktExit in studio\marketing." -ForegroundColor Yellow
  }
}

# --- 4. Summary -------------------------------------------------------------

Write-Section "Install complete!"
Write-Host ""
Write-Host "  bequite CLI is now installed in the local venv." -ForegroundColor Green
Write-Host ""
Write-Host "  Activate the venv (every new PowerShell window):" -ForegroundColor Cyan
Write-Host "    .\$VenvName\Scripts\Activate.ps1"
Write-Host ""
Write-Host "  Try the CLI:" -ForegroundColor Cyan
Write-Host "    bequite --version"
Write-Host "    bequite quickstart                # interactive quickstart"
Write-Host "    bequite doctor                    # environment diagnostic"
Write-Host "    bequite init my-app --doctrine default-web-saas"
Write-Host ""
if ($Studio) {
  Write-Host "  Run the Studio (three separate PowerShell windows):" -ForegroundColor Cyan
  Write-Host "    [1] cd studio\api"
  Write-Host "        bun run src/index.ts                      # http://localhost:3002"
  Write-Host ""
  Write-Host "    [2] cd studio\dashboard"
  Write-Host "        `$env:BEQUITE_DASHBOARD_MODE = 'http'"
  Write-Host "        npm run dev                                # http://localhost:3001"
  Write-Host ""
  Write-Host "    [3] cd studio\marketing"
  Write-Host "        npm run dev                                # http://localhost:3000"
  Write-Host ""
}
Write-Host "  Full install guide:  docs\INSTALL.md" -ForegroundColor Cyan
Write-Host "  Release notes:       docs\RELEASES\v1.0.0.md" -ForegroundColor Cyan
Write-Host ""
