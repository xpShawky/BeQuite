# install-bequite.ps1 - install BeQuite (lightweight Claude Code workflow pack) into the current project.
#
# Primary use (run inside the project you want to enhance):
#   irm https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.ps1 | iex
# File execution with options:
#   & C:\dev\BeQuite\scripts\install-bequite.ps1 -FromLocal C:\dev\BeQuite -Force
# Options through iex: set $env:BEQUITE_FROM_LOCAL / $env:BEQUITE_FORCE before the irm line.
#
# -Force re-installs commands and skills over an existing install.
# -Packs core,studio,business (or $env:BEQUITE_PACKS) picks the packs; core is always installed; default: all three,
#   or the choice saved in .bequite\state\PACKS.md by an earlier install, so updates keep the same packs.
# Project memory in .bequite\ is NEVER overwritten (missing files are added).
#
# Rules for this file (checked by scripts/bq_check.py): pure ASCII, no BOM, no param()/CmdletBinding
# block (Invoke-Expression cannot run one), and no `exit` (it would close the user's shell under iex).

$BqFromLocal = if ($env:BEQUITE_FROM_LOCAL) { $env:BEQUITE_FROM_LOCAL } else { "" }
$BqForce = [bool]($env:BEQUITE_FORCE)
$BqPacks = if ($env:BEQUITE_PACKS) { $env:BEQUITE_PACKS } else { "" }
for ($i = 0; $i -lt $args.Count; $i++) {
  switch -regex ("$($args[$i])") {
    '^-+[Ff]rom[Ll]ocal$' { if ($i + 1 -lt $args.Count) { $i++; $BqFromLocal = "$($args[$i])" } }
    '^-+[Ff]orce$'        { $BqForce = $true }
    '^-+[Pp]acks$'        { if ($i + 1 -lt $args.Count) { $i++; $BqPacks = "$($args[$i])" } }
  }
}

function Install-BeQuite([string]$FromLocal, [bool]$Force, [string]$Packs) {
  $ErrorActionPreference = "Stop"
  $Version = "v1.0.0"
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
  # the source's VERSION file is the version being installed (the constant above is only the fallback)
  $VerFile = Join-Path $Source "VERSION"
  if (Test-Path $VerFile) { $Version = "v" + [System.IO.File]::ReadAllText($VerFile).Trim().TrimStart('v') }
  $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  # packs: the argument, else the choice saved by an earlier install, else all three; core is always in
  if ($Packs -eq "" -and (Test-Path ".\.bequite\state\PACKS.md")) {
    $pm = [regex]::Match([System.IO.File]::ReadAllText((Join-Path $Target ".bequite\state\PACKS.md")), '(?m)^\*\*Packs:\*\* *([^\r\n]*)')
    if ($pm.Success) { $Packs = $pm.Groups[1].Value }
  }
  if ($Packs -eq "") { $Packs = "core,studio,business" }
  $packList = @("core") + @($Packs.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" -and $_ -ne "core" })
  $Packs = ($packList | Select-Object -Unique) -join ","
  $excluded = @{}
  $packsFile = Join-Path $Source ".claude\bequite\PACKS.txt"
  if (Test-Path $packsFile) {
    foreach ($line in [System.IO.File]::ReadAllLines($packsFile)) {
      $parts = $line.Trim() -split '\s+', 2
      if ($parts.Count -lt 2 -or $parts[0].StartsWith("#")) { continue }
      if (-not ($packList -contains $parts[0])) { $excluded[$parts[1]] = $true }
    }
  }

  try {
    # --- 3. Commands, skills, hooks ----------------------------------------
    Section "Installing commands and skills"
    New-Item -ItemType Directory -Force ".\.claude\commands", ".\.claude\skills" | Out-Null
    Get-ChildItem (Join-Path $Source ".claude\commands") -Filter "*.md" | ForEach-Object {
      if (-not $excluded.ContainsKey("commands/" + $_.Name)) { Copy-Item $_.FullName ".\.claude\commands\" -Force }
    }
    Get-ChildItem (Join-Path $Source ".claude\skills") -Directory -Filter "bequite-*" | ForEach-Object {
      if ($excluded.ContainsKey("skills/" + $_.Name)) { return }
      $dst = Join-Path ".\.claude\skills" $_.Name
      if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
      Copy-Item -Path $_.FullName -Destination $dst -Recurse -Force
    }
    if (Test-Path ".\.claude\bequite") { Remove-Item ".\.claude\bequite" -Recurse -Force }
    Copy-Item -Path (Join-Path $Source ".claude\bequite") -Destination ".\.claude\bequite" -Recurse -Force
    # files a newer version removed: move them aside, never delete
    $moved = 0
    $removedList = Join-Path $Source ".claude\bequite\REMOVED.txt"
    if (Test-Path $removedList) {
      foreach ($line in [System.IO.File]::ReadAllLines($removedList)) {
        $p = $line.Trim()
        if ($p -eq "" -or $p.StartsWith("#") -or $p.Contains("..")) { continue }
        $old = Join-Path ".\.claude" $p
        if ($p.StartsWith("hooks/")) {
          $usedBy = @(".\.claude\settings.json", ".\.claude\settings.local.json") | Where-Object { (Test-Path $_) -and ([System.IO.File]::ReadAllText((Resolve-Path $_).Path).Contains($p)) }
          if ($usedBy) { Write-Host "  kept .claude\$p : your Claude Code settings still run it (remove it from the settings, then delete the file)"; continue }
        }
        if (Test-Path $old) {
          $dst = Join-Path ".\.bequite\backups\$Stamp-removed\.claude" $p
          New-Item -ItemType Directory -Force (Split-Path $dst -Parent) | Out-Null
          Move-Item $old $dst -Force
          $moved++
        }
      }
    }
    Get-ChildItem ".\.claude\skills" -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    $agentsSrc = Join-Path $Source "agents"
    if (Test-Path $agentsSrc) {
      New-Item -ItemType Directory -Force ".\.claude\agents" | Out-Null
      Copy-Item -Path (Join-Path $agentsSrc "bq-*.md") -Destination ".\.claude\agents\" -Force
    }
    $nCmd = (Get-ChildItem ".\.claude\commands" -Filter *.md).Count
    $nSkill = (Get-ChildItem ".\.claude\skills" -Directory -Filter "bequite-*").Count
    $nAgent = @(Get-ChildItem ".\.claude\agents" -Filter "bq-*.md" -ErrorAction SilentlyContinue).Count
    Write-Host "  $nCmd commands, $nSkill skills, $nAgent subagents (packs: $Packs)" -ForegroundColor Green
    if ($moved -gt 0) { Write-Host "  $moved removed command or skill file(s) moved to .bequite\backups\$Stamp-removed\" }

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
    $hadSourceMd = Test-Path ".\.bequite\state\UPDATE_SOURCE.md"
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

    # the pack choice is remembered so updates install the same packs
    New-Item -ItemType Directory -Force ".\.bequite\state" | Out-Null
    $packsMd = "# BeQuite packs`n`n**Packs:** $Packs`n`nChange with: set `$env:BEQUITE_PACKS and `$env:BEQUITE_FORCE=1 before the installer line (or --packs with install-bequite.sh).`n"
    [System.IO.File]::WriteAllText((Join-Path $Target ".bequite\state\PACKS.md"), $packsMd, $Utf8NoBom)
    # version metadata is not memory: it always says what is installed now
    $vf = Join-Path $Target ".bequite\state\BEQUITE_VERSION.md"
    if (Test-Path $vf) {
      $vt = [System.IO.File]::ReadAllText($vf)
      $m = [regex]::Match($vt, '(?m)^\*\*Version:\*\* *([^\r\n]*)')
      $oldV = if ($m.Success) { $m.Groups[1].Value.Trim() } else { "" }
      if ($oldV -ne $Version) {
        # '$' in a replacement string is a .NET substitution token, so the values are escaped
        $vt = [regex]::Replace($vt, '(?m)^\*\*Version:\*\*[^\r\n]*', ("**Version:** " + $Version.Replace('$', '$$')))
        $vt = [regex]::Replace($vt, '(?m)^\*\*Previous version:\*\*[^\r\n]*', ("**Previous version:** " + $oldV.Replace('$', '$$')))
        $vt = [regex]::Replace($vt, '(?m)^\(none yet\)\r?\n', "")
        $vt = $vt.TrimEnd() + "`n- " + (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ") + ": $oldV -> $Version`n"
        [System.IO.File]::WriteAllText($vf, $vt, $Utf8NoBom)
        Write-Host "  version metadata: $oldV -> $Version"
      }
    }
    # a first install from a local clone keeps updating from that clone (change it in UPDATE_SOURCE.md)
    $sf = Join-Path $Target ".bequite\state\UPDATE_SOURCE.md"
    if (-not $hadSourceMd -and $FromLocal -ne "" -and -not $env:BEQUITE_INSTALLED_FROM -and (Test-Path $sf)) {
      $st = [System.IO.File]::ReadAllText($sf)
      $st = [regex]::Replace($st, '(?m)^\*\*Source type:\*\*[^\r\n]*', "**Source type:** local")
      $st = [regex]::Replace($st, '(?m)^\*\*Repo URL or local path:\*\*[^\r\n]*', ("**Repo URL or local path:** " + $Source.Replace('\', '/').Replace('$', '$$')))
      [System.IO.File]::WriteAllText($sf, $st, $Utf8NoBom)
      Write-Host "  updates will come from $Source (UPDATE_SOURCE.md)"
    }
    # the automatic update switch is always visible (older memory files have no such line)
    if (Test-Path $sf) {
      $st = [System.IO.File]::ReadAllText($sf)
      if (-not [regex]::IsMatch($st, '(?m)^\*\*Auto update:\*\*')) {
        [System.IO.File]::WriteAllText($sf, $st.TrimEnd() + "`n`n**Auto update:** on (BeQuite installs new official releases by itself; set to off to be told instead)`n", $Utf8NoBom)
        Write-Host "  added the Auto update switch to UPDATE_SOURCE.md (on)"
      }
    }

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
    Write-Host "  Every BeQuite command first checks for a new official release and installs it (off switch: .bequite\state\UPDATE_SOURCE.md)."
    Write-Host ""
  } finally {
    if ($Tmp -and (Test-Path $Tmp)) { Remove-Item $Tmp -Recurse -Force -ErrorAction SilentlyContinue }
  }
}

Install-BeQuite -FromLocal $BqFromLocal -Force $BqForce -Packs $BqPacks
