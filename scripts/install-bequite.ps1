<#
.SYNOPSIS
  Install BeQuite (lightweight skill pack) into the current project.

.DESCRIPTION
  Copies the BeQuite slash commands, skills, principles, memory scaffold,
  and command reference into your project directory. No heavy dependencies.
  No Docker. No database. No frontend. No localhost app. Just markdown files.

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
$BEQUITE_VERSION = "v3.0.0-alpha.13"

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
Write-Host "  BeQuite installer ($BEQUITE_VERSION — lightweight skill pack)" -ForegroundColor Yellow
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

Write-Section "Installing .claude/commands/ (44 slash commands)"
$SRC_CMD = Join-Path $SOURCE ".claude\commands"
if (-not (Test-Path $SRC_CMD)) {
  Exit-Fatal "Source missing $SRC_CMD — is this a valid BeQuite repo?"
}
New-Item -ItemType Directory -Path ".\.claude\commands" -Force | Out-Null
Copy-Item -Path "$SRC_CMD\*" -Destination ".\.claude\commands\" -Recurse -Force
$count = (Get-ChildItem .\.claude\commands\*.md).Count
Write-Host "  $count slash commands installed" -ForegroundColor Green

# --- 4. Copy .claude/skills/bequite-* (15 specialist skills) ---

Write-Section "Installing .claude/skills/bequite-* (21 specialist skills)"
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

# --- 5. Create .bequite/ scaffold (alpha.5-alpha.8: principles + uiux + jobs + money + new state files) ---

Write-Section "Scaffolding .bequite/ memory (alpha.5-13: principles, uiux, jobs, money, mistake memory, assumptions, delegate, presentations)"

$SCAFFOLD = @(
  ".bequite\state",
  ".bequite\logs",
  ".bequite\prompts\user_prompts",
  ".bequite\prompts\generated_prompts",
  ".bequite\prompts\model_outputs",
  ".bequite\audits",
  ".bequite\plans",
  ".bequite\tasks",
  ".bequite\principles",
  ".bequite\decisions",
  ".bequite\uiux\screenshots",
  ".bequite\uiux\archive",
  ".bequite\jobs",
  ".bequite\money",
  ".bequite\backups",
  ".bequite\presentations\assets",
  ".bequite\presentations\outputs"
)
foreach ($dir in $SCAFFOLD) {
  if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
  }
}
Write-Host "  directory scaffold ready"

# Copy alpha.5–alpha.8 template files into target project (preserves existing)
$TEMPLATES = @{
  # alpha.3 principles
  ".bequite\principles\TOOL_NEUTRALITY.md" = ".bequite\principles\TOOL_NEUTRALITY.md"
  # alpha.5 mistake memory + assumptions
  ".bequite\state\MISTAKE_MEMORY.md"      = ".bequite\state\MISTAKE_MEMORY.md"
  ".bequite\state\ASSUMPTIONS.md"          = ".bequite\state\ASSUMPTIONS.md"
  # alpha.4 UI/UX
  ".bequite\uiux\SECTION_MAP.md"          = ".bequite\uiux\SECTION_MAP.md"
  ".bequite\uiux\LIVE_EDIT_LOG.md"        = ".bequite\uiux\LIVE_EDIT_LOG.md"
  ".bequite\uiux\UIUX_VARIANTS_REPORT.md" = ".bequite\uiux\UIUX_VARIANTS_REPORT.md"
  ".bequite\uiux\selected-variant.md"     = ".bequite\uiux\selected-variant.md"
  # alpha.8 jobs
  ".bequite\jobs\JOB_PROFILE.md"          = ".bequite\jobs\JOB_PROFILE.md"
  ".bequite\jobs\JOB_SEARCH_LOG.md"       = ".bequite\jobs\JOB_SEARCH_LOG.md"
  ".bequite\jobs\OPPORTUNITIES.md"        = ".bequite\jobs\OPPORTUNITIES.md"
  ".bequite\jobs\APPLICATION_TRACKER.md"  = ".bequite\jobs\APPLICATION_TRACKER.md"
  ".bequite\jobs\PITCH_TEMPLATES.md"      = ".bequite\jobs\PITCH_TEMPLATES.md"
  # alpha.8 money
  ".bequite\money\MONEY_PROFILE.md"       = ".bequite\money\MONEY_PROFILE.md"
  ".bequite\money\MONEY_SEARCH_LOG.md"    = ".bequite\money\MONEY_SEARCH_LOG.md"
  ".bequite\money\OPPORTUNITIES.md"       = ".bequite\money\OPPORTUNITIES.md"
  ".bequite\money\TRUST_CHECKS.md"        = ".bequite\money\TRUST_CHECKS.md"
  ".bequite\money\ACTION_PLAN.md"         = ".bequite\money\ACTION_PLAN.md"
  # alpha.10 deep-intelligence templates (jobs)
  ".bequite\jobs\HIDDEN_GEMS.md"          = ".bequite\jobs\HIDDEN_GEMS.md"
  ".bequite\jobs\COMMUNITY_SIGNALS.md"    = ".bequite\jobs\COMMUNITY_SIGNALS.md"
  ".bequite\jobs\AI_ASSISTED_WORK.md"     = ".bequite\jobs\AI_ASSISTED_WORK.md"
  # alpha.10 deep-intelligence templates (money)
  ".bequite\money\HIDDEN_GEMS.md"         = ".bequite\money\HIDDEN_GEMS.md"
  ".bequite\money\COMMUNITY_SIGNALS.md"   = ".bequite\money\COMMUNITY_SIGNALS.md"
  ".bequite\money\AI_ASSISTED_PATHS.md"   = ".bequite\money\AI_ASSISTED_PATHS.md"
  # alpha.10 version + update tracking
  ".bequite\state\BEQUITE_VERSION.md"     = ".bequite\state\BEQUITE_VERSION.md"
  ".bequite\state\UPDATE_SOURCE.md"       = ".bequite\state\UPDATE_SOURCE.md"
  ".bequite\logs\UPDATE_LOG.md"           = ".bequite\logs\UPDATE_LOG.md"
  # alpha.12 delegate task pack + mode history
  ".bequite\state\MODE_HISTORY.md"                    = ".bequite\state\MODE_HISTORY.md"
  ".bequite\tasks\DELEGATE_TASKS.md"                  = ".bequite\tasks\DELEGATE_TASKS.md"
  ".bequite\tasks\DELEGATE_INSTRUCTIONS.md"           = ".bequite\tasks\DELEGATE_INSTRUCTIONS.md"
  ".bequite\tasks\DELEGATE_ACCEPTANCE_CRITERIA.md"    = ".bequite\tasks\DELEGATE_ACCEPTANCE_CRITERIA.md"
  ".bequite\tasks\DELEGATE_TEST_PLAN.md"              = ".bequite\tasks\DELEGATE_TEST_PLAN.md"
  ".bequite\audits\DELEGATE_REVIEW_REPORT.md"         = ".bequite\audits\DELEGATE_REVIEW_REPORT.md"
  # alpha.13 presentation builder
  ".bequite\presentations\PRESENTATION_BRIEF.md"            = ".bequite\presentations\PRESENTATION_BRIEF.md"
  ".bequite\presentations\CONTENT_OUTLINE.md"               = ".bequite\presentations\CONTENT_OUTLINE.md"
  ".bequite\presentations\SLIDE_PLAN.md"                    = ".bequite\presentations\SLIDE_PLAN.md"
  ".bequite\presentations\DESIGN_BRIEF.md"                  = ".bequite\presentations\DESIGN_BRIEF.md"
  ".bequite\presentations\MOTION_PLAN.md"                   = ".bequite\presentations\MOTION_PLAN.md"
  ".bequite\presentations\SPEAKER_NOTES.md"                 = ".bequite\presentations\SPEAKER_NOTES.md"
  ".bequite\presentations\REFERENCES.md"                    = ".bequite\presentations\REFERENCES.md"
  ".bequite\presentations\PRESENTATION_VARIANTS_REPORT.md"  = ".bequite\presentations\PRESENTATION_VARIANTS_REPORT.md"
  ".bequite\presentations\EXPORT_LOG.md"                    = ".bequite\presentations\EXPORT_LOG.md"
}
foreach ($pair in $TEMPLATES.GetEnumerator()) {
  $src = Join-Path $SOURCE $pair.Key
  $dst = ".\$($pair.Value)"
  if ((Test-Path $src) -and (-not (Test-Path $dst))) {
    Copy-Item -Path $src -Destination $dst -Force
    Write-Host "  + $($pair.Value)"
  }
}

# Copy commands.md at repo root (top-level reference)
$CMDS_MD_SRC = Join-Path $SOURCE "commands.md"
if ((Test-Path $CMDS_MD_SRC) -and (-not (Test-Path ".\commands.md"))) {
  Copy-Item -Path $CMDS_MD_SRC -Destination ".\commands.md" -Force
  Write-Host "  + commands.md (full command reference at repo root)"
}

# --- 6. Append BeQuite section to CLAUDE.md if missing ---

Write-Section "Updating CLAUDE.md"

$CLAUDE_MD = ".\CLAUDE.md"
$BQ_MARKER = "<!-- BEQUITE -->"

if (-not (Test-Path $CLAUDE_MD)) {
  Set-Content -Path $CLAUDE_MD -Encoding utf8 -Value @"
# CLAUDE.md

This project uses **BeQuite $BEQUITE_VERSION** — a lightweight Claude Code skill pack.

$BQ_MARKER

## How to use BeQuite here

- Run ``/bequite`` to see the gate-aware menu.
- Run ``/bq-now`` for one-line orientation (faster than ``/bequite``).
- Run ``/bq-help`` for the full command reference (or open ``commands.md``).
- ``/bq-init`` to formally initialize (creates baseline state files).
- ``/bq-auto [intent] "task"`` for scoped autonomous mode (17 intents).
- ``/bq-suggest "<situation>"`` for workflow advice — recommends commands + mode.
- ``/bq-job-finder`` or ``/bq-make-money`` for opportunity discovery (Claude searches; deep intelligence + ``worldwide_hidden=true``).
- ``/bq-update`` to safely refresh BeQuite itself when a new alpha ships.
- BeQuite memory lives in ``.bequite/`` (state / logs / plans / tasks / audits / principles / uiux / jobs / money / backups).
- BeQuite commands live in ``.claude/commands/bequite.md`` + ``.claude/commands/bq-*.md``.
- BeQuite skills live in ``.claude/skills/bequite-*/``.

## Core operating rules (BeQuite)

1. **Tool neutrality** — named tools are EXAMPLES, not commands. See ``.bequite/principles/TOOL_NEUTRALITY.md``.
2. Never claim a task is "done" unless ``/bq-verify`` passes.
3. Always update ``.bequite/logs/AGENT_LOG.md`` when you take a real action.
4. Always update ``.bequite/state/WORKFLOW_GATES.md`` when a gate is met.
5. Banned weasel words: should, probably, seems to, appears to, I think it works, might, hopefully, in theory.
6. No out-of-order commands — gate system blocks them.

<!-- /BEQUITE -->
"@
  Write-Host "  created CLAUDE.md"
} else {
  $existing = Get-Content $CLAUDE_MD -Raw
  if ($existing -notmatch [regex]::Escape($BQ_MARKER)) {
    Add-Content -Path $CLAUDE_MD -Value @"

---

$BQ_MARKER

# BeQuite $BEQUITE_VERSION

This project uses **BeQuite** — a lightweight Claude Code skill pack.

- ``/bequite`` — gate-aware menu
- ``/bq-now`` — one-line status
- ``/bq-help`` — full reference (also at ``commands.md``)
- ``/bq-auto [intent] "task"`` — scoped autonomous mode
- ``/bq-suggest "<situation>"`` — workflow advisor
- ``/bq-job-finder`` / ``/bq-make-money`` — opportunity discovery with deep intelligence + ``worldwide_hidden=true``
- ``/bq-update`` — safe BeQuite self-update (backups + non-destructive)

See ``.bequite/`` for memory + state. Named tools are EXAMPLES — see ``.bequite/principles/TOOL_NEUTRALITY.md``.
Memory-first principle: see ``docs/architecture/MEMORY_FIRST_BEHAVIOR.md``.

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

Write-Section "BeQuite $BEQUITE_VERSION installed"
Write-Host ""
Write-Host "  Run inside Claude Code:" -ForegroundColor Cyan
Write-Host "    /bequite              gate-aware menu + next 3 recommendations" -ForegroundColor White
Write-Host "    /bq-now               one-line orientation (faster than /bequite)" -ForegroundColor White
Write-Host "    /bq-help              full command reference" -ForegroundColor White
Write-Host "    /bq-init              formally initialize this project" -ForegroundColor White
Write-Host "    /bq-discover          inspect this repo" -ForegroundColor White
Write-Host "    /bq-doctor            environment health" -ForegroundColor White
Write-Host ""
Write-Host "  Autonomous:" -ForegroundColor Cyan
Write-Host "    /bq-auto new ""..""    full P0->P5 lifecycle" -ForegroundColor White
Write-Host "    /bq-auto fix ""..""    scoped fix mini-cycle" -ForegroundColor White
Write-Host "    /bq-auto uiux variants=5 ""..""   generate 5 UI directions" -ForegroundColor White
Write-Host "    /bq-live-edit ""..""              section-by-section frontend edits" -ForegroundColor White
Write-Host ""
Write-Host "  Opportunity and Workflows (alpha.8 + deep intelligence alpha.10):" -ForegroundColor Cyan
Write-Host "    /bq-suggest ""<situation>""       workflow advisor + mode recommendation" -ForegroundColor White
Write-Host "    /bq-job-finder                   real work opportunities (Claude searches)" -ForegroundColor White
Write-Host "    /bq-make-money                   earning opportunities + 10 tracks" -ForegroundColor White
Write-Host "      worldwide_hidden=true          search beyond famous English platforms" -ForegroundColor Gray
Write-Host "      trending_now=true              last-30-days surge" -ForegroundColor Gray
Write-Host "      community_discovered=true      Reddit / IH / HN / X / forum signals" -ForegroundColor Gray
Write-Host "      AI_assisted=true               surface AI-multiplier work paths" -ForegroundColor Gray
Write-Host ""
Write-Host "  Maintenance (alpha.10):" -ForegroundColor Cyan
Write-Host "    /bq-update                       safe BeQuite self-update (backups + no overwrites)" -ForegroundColor White
Write-Host "    /bq-update check                 preview what would change" -ForegroundColor White
Write-Host ""
Write-Host "  Operating modes (alpha.12 — composable):" -ForegroundColor Cyan
Write-Host "    /bq-auto deep ""..""              full 11-dim research + red-team for quality-critical work" -ForegroundColor White
Write-Host "    /bq-auto fast ""..""              short discovery; still tests + verifies" -ForegroundColor White
Write-Host "    /bq-auto token-saver ""..""       (alias: lean) low context cost; reuse cached research" -ForegroundColor White
Write-Host "    /bq-auto delegate ""..""          strong model architects + cheap model implements + strong model reviews" -ForegroundColor White
Write-Host ""
Write-Host "  Creative + Content Workflows (alpha.13):" -ForegroundColor Cyan
Write-Host "    /bq-presentation Create a lecture about X       natural language; quotes optional" -ForegroundColor White
Write-Host "    /bq-presentation format=pptx variants=3 ...     PPTX with 3 design directions" -ForegroundColor White
Write-Host "    /bq-presentation format=html ...                cinematic browser slides" -ForegroundColor White
Write-Host "    /bq-presentation format=both ...                same content, two renders" -ForegroundColor White
Write-Host "    /bq-presentation strict=true source=...         preserve source (PDF / Word / scientific)" -ForegroundColor White
Write-Host "    /bq-presentation creative=true ...              topic-only; add hooks + story" -ForegroundColor White
Write-Host ""
Write-Host "  Memory:        .bequite/ (state / logs / plans / tasks / audits / uiux / jobs / money / presentations / backups)" -ForegroundColor Gray
Write-Host "  Commands:      .claude/commands/" -ForegroundColor Gray
Write-Host "  Skills:        .claude/skills/" -ForegroundColor Gray
Write-Host "  Reference:     commands.md (repo root) — full command catalog" -ForegroundColor Gray
Write-Host "  Tool rule:     .bequite/principles/TOOL_NEUTRALITY.md" -ForegroundColor Gray
Write-Host ""
