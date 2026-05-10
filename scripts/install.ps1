<#
.SYNOPSIS
  One-command install for BeQuite on Windows (PowerShell 5.1 and 7+).

.DESCRIPTION
  - Verifies prerequisites (Python 3.11+, git).
  - Creates a venv in the current directory.
  - Installs the Layer 1 Harness CLI (bequite + bq) in editable mode.
  - Optionally installs the Layer 2 Studio dependencies (pnpm + bun).

  Run from inside a cloned BeQuite repo, OR pass -CloneTo to clone first.

.PARAMETER CloneTo
  Optional directory to clone the repo into. If omitted, assumes the current
  directory IS the BeQuite repo.

.PARAMETER Studio
  Also install Layer 2 Studio dependencies (Bun for api/, pnpm for
  dashboard/ + marketing/). Skipped by default for a quick CLI-only install.

.PARAMETER VenvName
  Name of the venv directory. Default: .venv

.EXAMPLE
  # From inside a cloned BeQuite repo
  .\scripts\install.ps1

.EXAMPLE
  # Clone + install in one shot
  .\install.ps1 -CloneTo C:\dev\BeQuite -Studio
#>
[CmdletBinding()]
param(
  [string]$CloneTo = "",
  [switch]$Studio = $false,
  [string]$VenvName = ".venv"
)

$ErrorActionPreference = "Stop"

function Write-Section($text) {
  Write-Host ""
  Write-Host "==> $text" -ForegroundColor Yellow
}

function Test-Command($cmd) {
  $null = Get-Command $cmd -ErrorAction SilentlyContinue
  return $?
}

# --- 1. Prereq checks -------------------------------------------------------

Write-Section "Checking prerequisites"

if (-not (Test-Command python)) {
  Write-Host "ERROR: python not on PATH. Install Python >= 3.11 from https://python.org or via 'winget install Python.Python.3.12'." -ForegroundColor Red
  exit 1
}
$pyVersionLine = (python --version) 2>&1
Write-Host "  Python: $pyVersionLine"

if (-not (Test-Command git)) {
  Write-Host "ERROR: git not on PATH. Install from https://git-scm.com or 'winget install Git.Git'." -ForegroundColor Red
  exit 1
}
Write-Host "  Git:    $(git --version)"

if ($Studio) {
  if (-not (Test-Command node)) {
    Write-Host "WARNING: node not on PATH (needed for Studio). Install Node.js >= 20 from https://nodejs.org or 'winget install OpenJS.NodeJS.LTS'." -ForegroundColor Yellow
  } else {
    Write-Host "  Node:   $(node --version)"
  }
  if (-not (Test-Command pnpm)) {
    Write-Host "  pnpm:   not on PATH (will install via npm)" -ForegroundColor Yellow
  } else {
    Write-Host "  pnpm:   $(pnpm --version)"
  }
  if (-not (Test-Command bun)) {
    Write-Host "  bun:    not on PATH (needed for Studio API). Install via 'powershell -c \"irm bun.sh/install.ps1 | iex\"'." -ForegroundColor Yellow
  } else {
    Write-Host "  Bun:    $(bun --version)"
  }
}

# --- 2. Clone if requested -------------------------------------------------

if ($CloneTo -ne "") {
  Write-Section "Cloning into $CloneTo"
  if (Test-Path $CloneTo) {
    Write-Host "Directory exists; skipping clone."
  } else {
    git clone https://github.com/xpShawky/BeQuite.git $CloneTo
  }
  Set-Location $CloneTo
}

# Sanity check we're in a BeQuite repo.
if (-not (Test-Path ".\cli\pyproject.toml")) {
  Write-Host "ERROR: cli\pyproject.toml not found. Run this script from inside a cloned BeQuite repo, or pass -CloneTo <dir>." -ForegroundColor Red
  exit 1
}

# --- 3. Venv + CLI install -------------------------------------------------

Write-Section "Creating venv at .\$VenvName"
if (-not (Test-Path ".\$VenvName")) {
  python -m venv $VenvName
}

Write-Section "Activating venv"
$activate = Join-Path (Get-Location) "$VenvName\Scripts\Activate.ps1"
if (-not (Test-Path $activate)) {
  Write-Host "ERROR: venv activation script not found at $activate" -ForegroundColor Red
  exit 1
}
. $activate
Write-Host "  active: $env:VIRTUAL_ENV"

Write-Section "Upgrading pip"
python -m pip install --upgrade pip --quiet

Write-Section "Installing bequite CLI (editable)"
pip install -e .\cli
if (-not $?) {
  Write-Host "ERROR: pip install failed." -ForegroundColor Red
  exit 1
}

Write-Section "Verifying bequite CLI"
$version = bequite --version
Write-Host "  $version"
if ($version -notmatch "bequite, version") {
  Write-Host "ERROR: bequite did not report a version." -ForegroundColor Red
  exit 1
}

# --- 4. Optional Studio install --------------------------------------------

if ($Studio) {
  Write-Section "Installing Studio API dependencies (Bun)"
  if (Test-Command bun) {
    Push-Location ".\studio\api"
    bun install
    Pop-Location
  } else {
    Write-Host "Skipped (bun not on PATH)." -ForegroundColor Yellow
  }

  Write-Section "Installing Studio Dashboard dependencies"
  Push-Location ".\studio\dashboard"
  if (Test-Command pnpm) { pnpm install } else { npm install }
  Pop-Location

  Write-Section "Installing Studio Marketing dependencies"
  Push-Location ".\studio\marketing"
  if (Test-Command pnpm) { pnpm install } else { npm install }
  Pop-Location
}

# --- 5. Summary -------------------------------------------------------------

Write-Section "Install complete"
Write-Host ""
Write-Host "  bequite CLI:" -ForegroundColor Green
Write-Host "    Activate venv:    .\$VenvName\Scripts\Activate.ps1"
Write-Host "    Try it:           bequite --version"
Write-Host "    Doctor:           bequite doctor"
Write-Host "    Initialize app:   bequite init my-app --doctrine default-web-saas"
Write-Host ""
if ($Studio) {
  Write-Host "  Studio (three separate PowerShell windows):" -ForegroundColor Green
  Write-Host "    [1] cd studio\api;       bun run src/index.ts       # http://localhost:3002"
  Write-Host "    [2] cd studio\dashboard;`$env:BEQUITE_DASHBOARD_MODE='http'; pnpm dev   # http://localhost:3001"
  Write-Host "    [3] cd studio\marketing; pnpm dev                  # http://localhost:3000"
  Write-Host ""
}
Write-Host "  Docs:               docs\INSTALL.md  /  README.md"
Write-Host ""
