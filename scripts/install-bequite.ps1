# install-bequite.ps1 - install BeQuite (lightweight Claude Code workflow pack) into the current project.
#
# Primary use (run inside the project you want to enhance):
#   irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex
# File execution with options:
#   & C:\dev\BeQuite\scripts\install-bequite.ps1 -FromLocal C:\dev\BeQuite -Force
# Options through iex: set $env:BEQUITE_FROM_LOCAL / $env:BEQUITE_FORCE before the irm line.
#
# -Force re-installs commands and skills over an existing install.
# Project memory in .bequite\ is NEVER overwritten (missing files are added).
#
# Rules for this file (checked by scripts/bq_check.py): pure ASCII, no BOM, no param()/CmdletBinding
# block (Invoke-Expression cannot run one), and no `exit` (it would close the user's shell under iex).

$BqFromLocal = if ($env:BEQUITE_FROM_LOCAL) { $env:BEQUITE_FROM_LOCAL } else { "" }
$BqForce = [bool]($env:BEQUITE_FORCE)
for ($i = 0; $i -lt $args.Count; $i++) {
  switch -regex ("$($args[$i])") {
    '^-+[Ff]rom[Ll]ocal$' { if ($i + 1 -lt $args.Count) { $i++; $BqFromLocal = "$($args[$i])" } }
    '^-+[Ff]orce$'        { $BqForce = $true }
  }
}

function Install-BeQuite([string]$FromLocal, [bool]$Force) {
  $ErrorActionPreference = "Stop"
  $Version = "v4.0.0"
  $RepoUrl = "https://github.com/xpShawky/BeQuite.git"
  $Target = (Get-Location).Path
  $Utf8NoBom = New-Object System.Text.UTF8Encoding $false

  function Section($t) { Write-Host ""; Write-Host "==> $t" -ForegroundColor Yellow }
  function Fail($t) { Write-Host ""; Write-Host "FATAL: $t" -ForegroundColor Red; Write-Host "" }

  Write-Host ""
  Write-Host "  BeQuite installer ($Version)" -ForegroundColor Yellow
  Write-Host "  Target: $Target"

  # --- 1. Existing install? ------------------------------------------------
  if ((Test-Path ".\.claude\commands\bequite.md") -and -not $Force) {
    Write-Host ""
    Write-Host "BeQuite is already installed here." -ForegroundColor Yellow
    Write-Host "Re-run with -Force (or `$env:BEQUITE_FORCE=1) to refresh commands and skills. Your .bequite memory is never overwritten."
    return
  }

  # --- 2. Source ------------------------------------------------------------
  $Tmp = $null
  if ($FromLocal -ne "") {
    if (-not (Test-Path $FromLocal)) { Fail "'$FromLocal' does not exist."; return }
    $Source = (Resolve-Path $FromLocal).Path
    Section "Using local BeQuite source at $Source"
  } else {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Fail "git not found. Install git or set `$env:BEQUITE_FROM_LOCAL."; return }
    Section "Downloading BeQuite from $RepoUrl"
    $Tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("bequite-installer-" + [guid]::NewGuid().ToString("N").Substring(0, 8))
    & git clone --quiet --depth 1 $RepoUrl $Tmp
    if ($LASTEXITCODE -ne 0) { Fail "git clone failed."; return }
    $Source = $Tmp
  }
  $TplRoot = Join-Path $Source "templates\bequite"
  if (-not (Test-Path $TplRoot)) { Fail "$Source has no templates\bequite (old or wrong source)."; return }

  try {
    # --- 3. Commands, skills, hooks ----------------------------------------
    Section "Installing commands and skills"
    New-Item -ItemType Directory -Force ".\.claude\commands", ".\.claude\skills" | Out-Null
    Copy-Item -Path (Join-Path $Source ".claude\commands\*.md") -Destination ".\.claude\commands\" -Force
    Get-ChildItem (Join-Path $Source ".claude\skills") -Directory -Filter "bequite-*" | ForEach-Object {
      $dst = Join-Path ".\.claude\skills" $_.Name
      if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
      Copy-Item -Path $_.FullName -Destination $dst -Recurse -Force
    }
    if (Test-Path ".\.claude\bequite") { Remove-Item ".\.claude\bequite" -Recurse -Force }
    Copy-Item -Path (Join-Path $Source ".claude\bequite") -Destination ".\.claude\bequite" -Recurse -Force
    $nCmd = (Get-ChildItem ".\.claude\commands" -Filter *.md).Count
    $nSkill = (Get-ChildItem ".\.claude\skills" -Directory -Filter "bequite-*").Count
    Write-Host "  $nCmd commands, $nSkill skills, reference docs in .claude\bequite\docs" -ForegroundColor Green

    $hooks = Join-Path $Source ".claude\hooks"
    if (Test-Path $hooks) {
      New-Item -ItemType Directory -Force ".\.claude\hooks" | Out-Null
      Copy-Item -Path (Join-Path $hooks "*") -Destination ".\.claude\hooks\" -Recurse -Force
      foreach ($ex in @("settings.json.example", "settings.windows.json.example")) {
        $src = Join-Path $Source ".claude\$ex"
        if (Test-Path $src) { Copy-Item $src ".\.claude\$ex" -Force }
      }
      Write-Host "  safety hooks copied but NOT active (opt-in: run /bq-hooks status)"
    }

    # --- 4. Memory scaffold (never overwrites) ------------------------------
    Section "Preparing .bequite memory"
    $added = 0
    Get-ChildItem $TplRoot -Recurse -File -Force | ForEach-Object {
      $rel = $_.FullName.Substring($TplRoot.Length).TrimStart('\', '/')
      $dst = Join-Path ".\.bequite" $rel
      if (-not (Test-Path $dst)) {
        $dir = Split-Path $dst -Parent
        if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
        $text = [System.IO.File]::ReadAllText($_.FullName)
        $text = $text.Replace("{{VERSION}}", $Version)
        [System.IO.File]::WriteAllText((Join-Path $Target $dst), $text, $Utf8NoBom)
        $added++
      }
    }
    Write-Host "  $added files added (existing memory left untouched)"

    $cmdRef = Join-Path $Source "commands.md"
    if (Test-Path $cmdRef) { Copy-Item $cmdRef ".\commands.md" -Force }

    # --- 5. CLAUDE.md ---------------------------------------------------------
    Section "Updating CLAUDE.md"
    $block = [System.IO.File]::ReadAllText((Join-Path $Source "templates\CLAUDE.bequite.md")).Replace("{{VERSION}}", $Version).TrimEnd()
    $claude = Join-Path $Target "CLAUDE.md"
    $open = "<!-- BEQUITE -->"
    $close = "<!-- /BEQUITE -->"
    if (-not (Test-Path $claude)) {
      [System.IO.File]::WriteAllText($claude, "# CLAUDE.md`n`n" + $block + "`n", $Utf8NoBom)
      Write-Host "  created CLAUDE.md"
    } else {
      $cur = [System.IO.File]::ReadAllText($claude)
      $a = $cur.IndexOf($open)
      $b = $cur.IndexOf($close)
      if ($a -ge 0 -and $b -gt $a) {
        $new = $cur.Substring(0, $a) + $block + $cur.Substring($b + $close.Length)
        [System.IO.File]::WriteAllText($claude, $new, $Utf8NoBom)
        Write-Host "  refreshed the BeQuite section"
      } else {
        [System.IO.File]::WriteAllText($claude, $cur.TrimEnd() + "`n`n---`n`n" + $block + "`n", $Utf8NoBom)
        Write-Host "  appended the BeQuite section"
      }
    }

    # --- 6. Done --------------------------------------------------------------
    Section "BeQuite $Version installed"
    Write-Host ""
    Write-Host "  In Claude Code, start with:"
    Write-Host "    /bequite        menu: project state + next recommended commands"
    Write-Host "    /bq-help        full command reference (also commands.md)"
    Write-Host "    /bq-auto `"..`"   autonomous runner; stops only at hard gates"
    Write-Host ""
  } finally {
    if ($Tmp -and (Test-Path $Tmp)) { Remove-Item $Tmp -Recurse -Force -ErrorAction SilentlyContinue }
  }
}

Install-BeQuite -FromLocal $BqFromLocal -Force $BqForce
