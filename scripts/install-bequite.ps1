<#
.SYNOPSIS
  Install BeQuite (lightweight skill pack) into the current project.

.DESCRIPTION
  Copies the BeQuite slash commands, skills, and memory scaffold into your
  current project directory. No heavy dependencies. No Docker. No database.
  No frontend. No localhost app. Just files.

  By default, this script downloads from the BeQuite GitHub repo. If you've
  already cloned BeQuite locally, pass -FromLocal <path> to copy from there.

.PARAMETER FromLocal
  Path to a local BeQuite clone. If omitted, downloads from GitHub.

.PARAMETER Force
  Overwrite existing .bequite/, .claude/commands/, .claude/skills/. Without
  this flag, refuses to overwrite — you'd lose memory.

.EXAMPLE
  # From inside the target project directory
  irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex

.EXAMPLE
  # Or, with a local BeQuite clone
  & C:\dev\BeQuite\scripts\install-bequite.ps1 -FromLocal C:\dev\BeQuite
#>
[CmdletBinding()]
param(
  [string]$FromLocal = "",
  [switch]$Force = $false
)

$ErrorActionPreference = "Continue"

function Write-Section($text) {
  Write-Host ""
  Write-Host "==> $text" -ForegroundColor Yellow
}

function Exit-Fatal($msg) {
  Write-Host ""
  Write-Host "FATAL: $msg" -ForegroundColor Red
  Write-Host ""
  exit 1
}

$REPO_URL = "https://github.com/xpShawky/BeQuite.git"
$TARGET = (Get-Location).Path

Write-Host ""
Write-Host "  BeQuite installer (lightweight skill pack)" -ForegroundColor Yellow
Write-Host "  Target: $TARGET"
Write-Host ""

# --- 1. Refuse to overwrite without --Force ---

$EXISTING = @()
if (Test-Path ".\.bequite") { $EXISTING += ".bequite/" }
if (Test-Path ".\.claude\commands\bequite.md") { $EXISTING += ".claude/commands/bequite.md" }
if (Test-Path ".\.claude\skills\bequite-project-architect") { $EXISTING += ".claude/skills/bequite-*" }

if ($EXISTING.Count -gt 0 -and -not $Force) {
  Write-Host "BeQuite appears to already be installed here:" -ForegroundColor Yellow
  foreach ($e in $EXISTING) { Write-Host "  $e" }
  Write-Host ""
  Write-Host "Re-running install would overwrite your .bequite/ memory." -ForegroundColor Red
  Write-Host "If you want to proceed, re-run with -Force."
  exit 1
}

# --- 2. Get the source ---

$SOURCE = $null

if ($FromLocal -ne "") {
  if (Test-Path $FromLocal) {
    $SOURCE = (Resolve-Path $FromLocal).Path
    Write-Section "Using local BeQuite clone at $SOURCE"
  } else {
    Exit-Fatal "Path '$FromLocal' doesn't exist."
  }
} else {
  # Clone or download
  Write-Section "Downloading BeQuite from $REPO_URL"

  $TMP = Join-Path $env:TEMP "bequite-installer-$(Get-Random)"
  New-Item -ItemType Directory -Path $TMP -Force | Out-Null

  if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "  Cloning shallow..."
    git clone --depth 1 $REPO_URL $TMP 2>&1 | ForEach-Object { Write-Host "  $_" }
    if ($LASTEXITCODE -ne 0) { Exit-Fatal "git clone failed." }
    $SOURCE = $TMP
  } else {
    Exit-Fatal "git is not on PATH. Install git or use -FromLocal <path-to-cloned-BeQuite>."
  }
}

# --- 3. Copy .claude/commands/ ---

Write-Section "Installing .claude/commands/"
$SRC_CMD = Join-Path $SOURCE ".claude\commands"
if (-not (Test-Path $SRC_CMD)) {
  Exit-Fatal "Source missing $SRC_CMD — is this a valid BeQuite repo?"
}
New-Item -ItemType Directory -Path ".\.claude\commands" -Force | Out-Null
Copy-Item -Path "$SRC_CMD\*" -Destination ".\.claude\commands\" -Recurse -Force
$count = (Get-ChildItem .\.claude\commands\*.md).Count
Write-Host "  $count slash commands installed" -ForegroundColor Green

# --- 4. Copy .claude/skills/bequite-* ---

Write-Section "Installing .claude/skills/bequite-*"
$SRC_SKILLS = Join-Path $SOURCE ".claude\skills"
if (-not (Test-Path $SRC_SKILLS)) {
  Exit-Fatal "Source missing $SRC_SKILLS"
}
New-Item -ItemType Directory -Path ".\.claude\skills" -Force | Out-Null
Get-ChildItem $SRC_SKILLS -Directory -Filter "bequite-*" | ForEach-Object {
  $skillName = $_.Name
  Copy-Item -Path $_.FullName -Destination ".\.claude\skills\$skillName" -Recurse -Force
  Write-Host "  + $skillName"
}

# --- 5. Create .bequite/ scaffold (only if not already present, even with --Force we preserve memory) ---

Write-Section "Scaffolding .bequite/ memory"

$SCAFFOLD = @(
  ".bequite\state",
  ".bequite\logs",
  ".bequite\prompts\user_prompts",
  ".bequite\prompts\generated_prompts",
  ".bequite\prompts\model_outputs",
  ".bequite\audits",
  ".bequite\plans",
  ".bequite\tasks"
)
foreach ($dir in $SCAFFOLD) {
  if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
  }
}
Write-Host "  scaffold ready"

# --- 6. Append BeQuite section to CLAUDE.md if missing ---

Write-Section "Updating CLAUDE.md"

$CLAUDE_MD = ".\CLAUDE.md"
$BQ_MARKER = "<!-- BEQUITE -->"

if (-not (Test-Path $CLAUDE_MD)) {
  Set-Content -Path $CLAUDE_MD -Encoding utf8 -Value @"
# CLAUDE.md

This project uses **BeQuite** — a lightweight Claude Code skill pack.

$BQ_MARKER

## How to use BeQuite here

- Run ``/bequite`` to see the menu.
- Run ``/bq-help`` for the full command reference.
- ``/bq-init`` to formally initialize (creates baseline state files).
- BeQuite memory lives in ``.bequite/``.
- BeQuite commands live in ``.claude/commands/bequite.md`` + ``.claude/commands/bq-*.md``.
- BeQuite skills live in ``.claude/skills/bequite-*/``.

## Core operating rules (BeQuite)

- Never claim a task is "done" unless ``/bq-verify`` passes.
- Always update ``.bequite/logs/AGENT_LOG.md`` when you take a real action.
- Banned weasel words in completion reports: should, probably, seems to, appears to, I think it works, might, hopefully, in theory.

<!-- /BEQUITE -->
"@
  Write-Host "  created CLAUDE.md"
} else {
  $existing = Get-Content $CLAUDE_MD -Raw
  if ($existing -notmatch [regex]::Escape($BQ_MARKER)) {
    Add-Content -Path $CLAUDE_MD -Value @"

---

$BQ_MARKER

# BeQuite

This project uses **BeQuite** — a lightweight Claude Code skill pack.

Run ``/bequite`` to see the menu. See ``.bequite/`` for memory + state.

<!-- /BEQUITE -->
"@
    Write-Host "  appended BeQuite section"
  } else {
    Write-Host "  BeQuite section already present; skipped"
  }
}

# --- 7. Cleanup ---

if ($FromLocal -eq "" -and $TMP -and (Test-Path $TMP)) {
  Remove-Item -Recurse -Force $TMP -ErrorAction SilentlyContinue
}

# --- 8. Done ---

Write-Section "BeQuite installed"
Write-Host ""
Write-Host "  Run inside Claude Code:" -ForegroundColor Cyan
Write-Host "    /bequite        the menu" -ForegroundColor White
Write-Host "    /bq-help        full command reference" -ForegroundColor White
Write-Host "    /bq-init        formally initialize this project" -ForegroundColor White
Write-Host "    /bq-discover    inspect this repo" -ForegroundColor White
Write-Host "    /bq-doctor      environment health" -ForegroundColor White
Write-Host ""
Write-Host "  Memory:        .bequite/" -ForegroundColor Gray
Write-Host "  Commands:      .claude/commands/" -ForegroundColor Gray
Write-Host "  Skills:        .claude/skills/" -ForegroundColor Gray
Write-Host ""
