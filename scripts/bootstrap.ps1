<#
.SYNOPSIS
  Vibecoder-friendly one-line install for BeQuite on Windows.

.DESCRIPTION
  Run this from any PowerShell prompt (in any directory you want BeQuite
  installed under). It will:

    1. Check for Python and Git. Print a clear install hint if missing
       (does NOT auto-install — those tools need a one-time user click).
    2. Clone https://github.com/xpShawky/BeQuite into a new BeQuite/ subdir.
    3. Create a venv inside the clone (.venv/).
    4. Install the bequite CLI in editable mode.
    5. Optionally install the Studio (-Studio flag).
    6. Print next-step commands.

  This is what the one-line README installer runs:
    irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.ps1 | iex

.PARAMETER Studio
  Also install Layer 2 Studio dependencies. Default: false.

.PARAMETER InstallDir
  Where to clone. Default: .\BeQuite (current dir + BeQuite subdir).

.EXAMPLE
  # CLI only — easiest possible install
  irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.ps1 | iex

.EXAMPLE
  # CLI + Studio
  & ([scriptblock]::Create((irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.ps1))) -Studio
#>
[CmdletBinding()]
param(
  [switch]$Studio = $false,
  [string]$InstallDir = ".\BeQuite"
)

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

# --- Banner ----------------------------------------------------------------

Write-Host ""
Write-Host "  ┌─────────────────────────────────────────────┐" -ForegroundColor DarkYellow
Write-Host "  │                                             │" -ForegroundColor DarkYellow
Write-Host "  │   BeQuite — one-command installer           │" -ForegroundColor Yellow
Write-Host "  │   Build it right the first time.            │" -ForegroundColor DarkYellow
Write-Host "  │                                             │" -ForegroundColor DarkYellow
Write-Host "  └─────────────────────────────────────────────┘" -ForegroundColor DarkYellow
Write-Host ""

# --- 1. Prereq checks (with helpful guidance, not auto-install) ------------

Write-Section "Checking prerequisites"

$missing = @()

if (-not (Test-Command python)) {
  $missing += @{
    name = "Python 3.11+"
    why = "needed to run the bequite CLI"
    fix1 = "Install from https://python.org (one-click, easiest)"
    fix2 = "winget install Python.Python.3.12"
  }
} else {
  Write-Host "  [OK] Python: $((python --version) 2>&1)"
}

if (-not (Test-Command git)) {
  $missing += @{
    name = "Git"
    why = "needed to clone the BeQuite repository"
    fix1 = "winget install Git.Git"
    fix2 = "https://git-scm.com/download/win"
  }
} else {
  Write-Host "  [OK] Git:    $((git --version) 2>&1)"
}

if ($Studio) {
  if (-not (Test-Command node)) {
    $missing += @{
      name = "Node.js 20+"
      why = "needed for the Studio dashboard + marketing site"
      fix1 = "winget install OpenJS.NodeJS.LTS"
      fix2 = "https://nodejs.org"
    }
  } else {
    Write-Host "  [OK] Node:   $((node --version) 2>&1)"
  }
  if (-not (Test-Command bun)) {
    Write-Host "  [WARN] Bun:    not on PATH (needed for Studio API; dashboard + marketing work without it)" -ForegroundColor Yellow
    Write-Host "         Install with: powershell -c `"irm bun.sh/install.ps1 | iex`"" -ForegroundColor Yellow
  } else {
    Write-Host "  [OK] Bun:    $((bun --version) 2>&1)"
  }
}

if ($missing.Count -gt 0) {
  Write-Host ""
  Write-Host "MISSING PREREQUISITES — install these first, then re-run the bootstrap:" -ForegroundColor Red
  Write-Host ""
  foreach ($m in $missing) {
    Write-Host "  $($m.name)  ($($m.why))" -ForegroundColor Red
    Write-Host "    Option 1:  $($m.fix1)" -ForegroundColor Yellow
    Write-Host "    Option 2:  $($m.fix2)" -ForegroundColor Yellow
    Write-Host ""
  }
  Write-Host "After installing, CLOSE + REOPEN PowerShell so the new tools land on PATH, then re-run:" -ForegroundColor Cyan
  Write-Host "  irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.ps1 | iex" -ForegroundColor Cyan
  Write-Host ""
  exit 1
}

# --- 2. Clone -------------------------------------------------------------

Write-Section "Cloning BeQuite into $InstallDir"

if (Test-Path $InstallDir) {
  $resolved = (Resolve-Path $InstallDir).Path
  Write-Host "  Directory already exists at: $resolved" -ForegroundColor Yellow
  Write-Host "  Skipping clone. If you want a fresh install, delete it first:" -ForegroundColor Yellow
  Write-Host "    Remove-Item -Recurse -Force '$resolved'" -ForegroundColor Yellow
} else {
  git clone https://github.com/xpShawky/BeQuite.git $InstallDir 2>&1 | ForEach-Object { Write-Host "  $_" }
  if ($LASTEXITCODE -ne 0) {
    Exit-Fatal "git clone failed (exit $LASTEXITCODE)"
  }
}

# --- 3. Run install.ps1 from inside the clone -----------------------------

Set-Location $InstallDir

$installScript = ".\scripts\install.ps1"
if (-not (Test-Path $installScript)) {
  Exit-Fatal "scripts\install.ps1 not found inside the clone. Did the clone succeed?"
}

Write-Section "Running install.ps1"

if ($Studio) {
  & $installScript -Studio
} else {
  & $installScript
}

if ($LASTEXITCODE -ne 0) {
  Exit-Fatal "install.ps1 exited with code $LASTEXITCODE"
}

# --- 4. Bonus next-step nudge ---------------------------------------------

Write-Host ""
Write-Host "  ┌─────────────────────────────────────────────────────────────┐" -ForegroundColor Green
Write-Host "  │                                                             │" -ForegroundColor Green
Write-Host "  │   Bootstrap complete!                                       │" -ForegroundColor Green
Write-Host "  │                                                             │" -ForegroundColor Green
Write-Host "  │   Next:                                                     │" -ForegroundColor Green
Write-Host "  │                                                             │" -ForegroundColor Green
Write-Host "  │     cd BeQuite                                              │" -ForegroundColor Green
Write-Host "  │     .\.venv\Scripts\Activate.ps1                            │" -ForegroundColor Green
Write-Host "  │     bequite quickstart                                      │" -ForegroundColor Green
Write-Host "  │                                                             │" -ForegroundColor Green
Write-Host "  └─────────────────────────────────────────────────────────────┘" -ForegroundColor Green
Write-Host ""
