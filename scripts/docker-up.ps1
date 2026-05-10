<#
.SYNOPSIS
  Bring the BeQuite Studio stack up via Docker Compose (Windows).

.DESCRIPTION
  Equivalent to running `docker compose up --build`, with a couple of
  beginner-friendly checks:
    1. Docker Desktop is running (daemon reachable).
    2. Ports 3000/3001/3002 aren't already in use (warns if so).
    3. Prints the three URLs after `up` succeeds.

.EXAMPLE
  .\scripts\docker-up.ps1                # build + up (foreground)

.EXAMPLE
  .\scripts\docker-up.ps1 -Detach        # build + up in background

.EXAMPLE
  .\scripts\docker-up.ps1 -Down          # stop + remove containers
#>
[CmdletBinding()]
param(
  [switch]$Detach = $false,
  [switch]$Down = $false,
  [switch]$NoBuild = $false
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

# --- Prereq checks ---

Write-Section "Checking Docker"

if (-not (Test-Command docker)) {
  Write-Host ""
  Write-Host "Docker is not on PATH. Install Docker Desktop:" -ForegroundColor Red
  Write-Host "  https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
  Write-Host "  Or via winget: winget install Docker.DockerDesktop" -ForegroundColor Yellow
  Write-Host ""
  exit 1
}

$dockerInfo = (docker info 2>&1) | Out-String
if ($dockerInfo -match "Cannot connect|failed to connect|daemon not running") {
  Write-Host ""
  Write-Host "Docker Desktop is installed but the daemon isn't running." -ForegroundColor Red
  Write-Host "Start Docker Desktop from the Start Menu and wait for the whale icon" -ForegroundColor Yellow
  Write-Host "in the taskbar to show 'Engine running', then re-run this script." -ForegroundColor Yellow
  Write-Host ""
  exit 1
}

Write-Host "  Docker daemon: OK"

# --- Down path ---

if ($Down) {
  Write-Section "Stopping BeQuite Studio stack"
  docker compose down
  Write-Section "Done"
  Write-Host "  Containers removed. Images preserved (use 'docker image prune' to clean)." -ForegroundColor Green
  exit 0
}

# --- Port check ---

Write-Section "Checking ports 3000 / 3001 / 3002"
foreach ($port in 3000, 3001, 3002) {
  $inUse = (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue).Count -gt 0
  if ($inUse) {
    Write-Host "  Port $port is already in use." -ForegroundColor Yellow
    Write-Host "    If it's a previous BeQuite dev server, stop it first." -ForegroundColor Yellow
    Write-Host "    The Docker container will FAIL to bind." -ForegroundColor Yellow
  } else {
    Write-Host "  Port ${port}: free"
  }
}

# --- Up ---

Write-Section "Bringing the stack up"

$composeArgs = @("compose", "up")
if (-not $NoBuild) { $composeArgs += "--build" }
if ($Detach)       { $composeArgs += "-d" }

Write-Host "  Running: docker $($composeArgs -join ' ')" -ForegroundColor Cyan
Write-Host ""

& docker @composeArgs

if ($Detach -and $LASTEXITCODE -eq 0) {
  Write-Host ""
  Write-Host "  ┌─────────────────────────────────────────────────────────┐" -ForegroundColor Green
  Write-Host "  │                                                         │" -ForegroundColor Green
  Write-Host "  │   BeQuite Studio is running in the background!          │" -ForegroundColor Green
  Write-Host "  │                                                         │" -ForegroundColor Green
  Write-Host "  │     http://localhost:3000     marketing site            │" -ForegroundColor Green
  Write-Host "  │     http://localhost:3000/docs   vibecoder tutorials    │" -ForegroundColor Green
  Write-Host "  │     http://localhost:3001     dashboard                 │" -ForegroundColor Green
  Write-Host "  │     http://localhost:3002/healthz   API health          │" -ForegroundColor Green
  Write-Host "  │                                                         │" -ForegroundColor Green
  Write-Host "  │   Follow logs:    docker compose logs -f                │" -ForegroundColor Green
  Write-Host "  │   Stop:           .\scripts\docker-up.ps1 -Down         │" -ForegroundColor Green
  Write-Host "  │                                                         │" -ForegroundColor Green
  Write-Host "  └─────────────────────────────────────────────────────────┘" -ForegroundColor Green
  Write-Host ""
}
