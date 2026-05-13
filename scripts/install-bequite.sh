#!/usr/bin/env bash
# Install BeQuite (lightweight skill pack) into the current project.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash
#
# Or from a local clone:
#   /path/to/BeQuite/scripts/install-bequite.sh --from-local /path/to/BeQuite

set -uo pipefail

BEQUITE_VERSION="v3.0.0-alpha.10"
REPO_URL="https://github.com/xpShawky/BeQuite.git"
TARGET="$(pwd)"
FROM_LOCAL=""
FORCE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from-local) FROM_LOCAL="$2"; shift 2 ;;
    --force) FORCE=true; shift ;;
    -h|--help)
      head -n 9 "$0" | tail -n 8
      exit 0
      ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

yellow() { printf '\033[33m%s\033[0m' "$*"; }
green()  { printf '\033[32m%s\033[0m' "$*"; }
red()    { printf '\033[31m%s\033[0m' "$*"; }
cyan()   { printf '\033[36m%s\033[0m' "$*"; }
section() { echo; echo "$(yellow "==> $1")"; }

echo
echo "  $(yellow "BeQuite installer ($BEQUITE_VERSION — lightweight skill pack)")"
echo "  Target: $TARGET"
echo

# --- 1. Refuse to overwrite without --force ---

EXISTING=()
[[ -d "./.bequite" ]] && EXISTING+=(".bequite/")
[[ -f "./.claude/commands/bequite.md" ]] && EXISTING+=(".claude/commands/bequite.md")
[[ -d "./.claude/skills/bequite-project-architect" ]] && EXISTING+=(".claude/skills/bequite-*")

if [[ ${#EXISTING[@]} -gt 0 && "$FORCE" != true ]]; then
  echo "$(yellow "BeQuite appears to already be installed here:")"
  for e in "${EXISTING[@]}"; do echo "  $e"; done
  echo
  echo "$(red "Re-running install would overwrite your .bequite/ memory.")"
  echo "If you want to proceed, re-run with --force."
  exit 1
fi

# --- 2. Source ---

SOURCE=""
TMP=""

if [[ -n "$FROM_LOCAL" ]]; then
  if [[ -d "$FROM_LOCAL" ]]; then
    SOURCE="$(cd "$FROM_LOCAL" && pwd)"
    section "Using local BeQuite clone at $SOURCE"
  else
    echo "$(red "FATAL:") path '$FROM_LOCAL' doesn't exist." >&2
    exit 1
  fi
else
  section "Downloading BeQuite from $REPO_URL"
  TMP="$(mktemp -d -t bequite-installer-XXXXXX)"
  if ! command -v git >/dev/null 2>&1; then
    echo "$(red "FATAL:") git not on PATH. Install git or use --from-local <path>." >&2
    exit 1
  fi
  git clone --depth 1 "$REPO_URL" "$TMP"
  SOURCE="$TMP"
fi

# --- 3. .claude/commands/ (37 slash commands) ---

section "Installing .claude/commands/ (43 slash commands)"
mkdir -p "./.claude/commands"
cp -r "$SOURCE/.claude/commands/"* "./.claude/commands/"
count=$(ls -1 ./.claude/commands/*.md 2>/dev/null | wc -l)
echo "  $(green "$count slash commands installed")"

# --- 4. .claude/skills/bequite-* (15 specialist skills) ---

section "Installing .claude/skills/bequite-* (19 specialist skills)"
mkdir -p "./.claude/skills"
for skill in "$SOURCE"/.claude/skills/bequite-*/; do
  if [[ -d "$skill" ]]; then
    name="$(basename "$skill")"
    cp -r "$skill" "./.claude/skills/$name"
    echo "  + $name"
  fi
done

# --- 5. .bequite/ scaffold (alpha.5: principles + uiux + new state files) ---

section "Scaffolding .bequite/ memory (alpha.5-8: principles, uiux, jobs, money, mistake memory, assumptions)"
mkdir -p ./.bequite/{state,logs,prompts/user_prompts,prompts/generated_prompts,prompts/model_outputs,audits,plans,tasks,principles,decisions,uiux/screenshots,uiux/archive,jobs,money,backups}
echo "  directory scaffold ready"

# Copy alpha.5 templates into target project (preserve existing if present)
copy_template() {
  local src_rel="$1"
  local dst_rel="$2"
  if [[ -f "$SOURCE/$src_rel" && ! -f "./$dst_rel" ]]; then
    cp "$SOURCE/$src_rel" "./$dst_rel"
    echo "  + $dst_rel"
  fi
}

# alpha.3 — tool neutrality
copy_template ".bequite/principles/TOOL_NEUTRALITY.md" ".bequite/principles/TOOL_NEUTRALITY.md"

# alpha.5 — mistake memory + assumptions
copy_template ".bequite/state/MISTAKE_MEMORY.md"      ".bequite/state/MISTAKE_MEMORY.md"
copy_template ".bequite/state/ASSUMPTIONS.md"          ".bequite/state/ASSUMPTIONS.md"

# alpha.4 — UI/UX
copy_template ".bequite/uiux/SECTION_MAP.md"          ".bequite/uiux/SECTION_MAP.md"
copy_template ".bequite/uiux/LIVE_EDIT_LOG.md"        ".bequite/uiux/LIVE_EDIT_LOG.md"
copy_template ".bequite/uiux/UIUX_VARIANTS_REPORT.md" ".bequite/uiux/UIUX_VARIANTS_REPORT.md"
copy_template ".bequite/uiux/selected-variant.md"      ".bequite/uiux/selected-variant.md"

# alpha.8 — jobs
copy_template ".bequite/jobs/JOB_PROFILE.md"          ".bequite/jobs/JOB_PROFILE.md"
copy_template ".bequite/jobs/JOB_SEARCH_LOG.md"       ".bequite/jobs/JOB_SEARCH_LOG.md"
copy_template ".bequite/jobs/OPPORTUNITIES.md"        ".bequite/jobs/OPPORTUNITIES.md"
copy_template ".bequite/jobs/APPLICATION_TRACKER.md"  ".bequite/jobs/APPLICATION_TRACKER.md"
copy_template ".bequite/jobs/PITCH_TEMPLATES.md"      ".bequite/jobs/PITCH_TEMPLATES.md"

# alpha.8 — money
copy_template ".bequite/money/MONEY_PROFILE.md"       ".bequite/money/MONEY_PROFILE.md"
copy_template ".bequite/money/MONEY_SEARCH_LOG.md"    ".bequite/money/MONEY_SEARCH_LOG.md"
copy_template ".bequite/money/OPPORTUNITIES.md"       ".bequite/money/OPPORTUNITIES.md"
copy_template ".bequite/money/TRUST_CHECKS.md"        ".bequite/money/TRUST_CHECKS.md"
copy_template ".bequite/money/ACTION_PLAN.md"         ".bequite/money/ACTION_PLAN.md"

# alpha.10 — deep-intelligence templates (jobs)
copy_template ".bequite/jobs/HIDDEN_GEMS.md"          ".bequite/jobs/HIDDEN_GEMS.md"
copy_template ".bequite/jobs/COMMUNITY_SIGNALS.md"    ".bequite/jobs/COMMUNITY_SIGNALS.md"
copy_template ".bequite/jobs/AI_ASSISTED_WORK.md"     ".bequite/jobs/AI_ASSISTED_WORK.md"

# alpha.10 — deep-intelligence templates (money)
copy_template ".bequite/money/HIDDEN_GEMS.md"         ".bequite/money/HIDDEN_GEMS.md"
copy_template ".bequite/money/COMMUNITY_SIGNALS.md"   ".bequite/money/COMMUNITY_SIGNALS.md"
copy_template ".bequite/money/AI_ASSISTED_PATHS.md"   ".bequite/money/AI_ASSISTED_PATHS.md"

# alpha.10 — version + update tracking
copy_template ".bequite/state/BEQUITE_VERSION.md"     ".bequite/state/BEQUITE_VERSION.md"
copy_template ".bequite/state/UPDATE_SOURCE.md"       ".bequite/state/UPDATE_SOURCE.md"
copy_template ".bequite/logs/UPDATE_LOG.md"           ".bequite/logs/UPDATE_LOG.md"

# Copy commands.md at repo root (top-level reference)
if [[ -f "$SOURCE/commands.md" && ! -f "./commands.md" ]]; then
  cp "$SOURCE/commands.md" "./commands.md"
  echo "  + commands.md (full command reference at repo root)"
fi

# --- 6. CLAUDE.md ---

section "Updating CLAUDE.md"

BQ_MARKER="<!-- BEQUITE -->"

if [[ ! -f "./CLAUDE.md" ]]; then
  cat > ./CLAUDE.md <<EOF
# CLAUDE.md

This project uses **BeQuite $BEQUITE_VERSION** — a lightweight Claude Code skill pack.

$BQ_MARKER

## How to use BeQuite here

- Run \`/bequite\` to see the gate-aware menu.
- Run \`/bq-now\` for one-line orientation (faster than \`/bequite\`).
- Run \`/bq-help\` for the full command reference (or open \`commands.md\`).
- \`/bq-init\` to formally initialize (creates baseline state files).
- \`/bq-auto [intent] "task"\` for scoped autonomous mode (17 intents).
- \`/bq-suggest "<situation>"\` for workflow advice — recommends commands + mode.
- \`/bq-job-finder\` or \`/bq-make-money\` for opportunity discovery (Claude searches; deep intelligence + \`worldwide_hidden=true\`).
- \`/bq-update\` to safely refresh BeQuite itself when a new alpha ships.
- BeQuite memory lives in \`.bequite/\` (state / logs / plans / tasks / audits / principles / uiux / jobs / money / backups).
- BeQuite commands live in \`.claude/commands/bequite.md\` + \`.claude/commands/bq-*.md\`.
- BeQuite skills live in \`.claude/skills/bequite-*/\`.

## Core operating rules (BeQuite)

1. **Tool neutrality** — named tools are EXAMPLES, not commands. See \`.bequite/principles/TOOL_NEUTRALITY.md\`.
2. Never claim a task is "done" unless \`/bq-verify\` passes.
3. Always update \`.bequite/logs/AGENT_LOG.md\` when you take a real action.
4. Always update \`.bequite/state/WORKFLOW_GATES.md\` when a gate is met.
5. Banned weasel words: should, probably, seems to, appears to, I think it works, might, hopefully, in theory.
6. No out-of-order commands — gate system blocks them.

<!-- /BEQUITE -->
EOF
  echo "  created CLAUDE.md"
else
  if ! grep -q "$BQ_MARKER" ./CLAUDE.md; then
    cat >> ./CLAUDE.md <<EOF

---

$BQ_MARKER

# BeQuite $BEQUITE_VERSION

This project uses **BeQuite** — a lightweight Claude Code skill pack.

- \`/bequite\` — gate-aware menu
- \`/bq-now\` — one-line status
- \`/bq-help\` — full reference (also at \`commands.md\`)
- \`/bq-auto [intent] "task"\` — scoped autonomous mode
- \`/bq-suggest "<situation>"\` — workflow advisor
- \`/bq-job-finder\` / \`/bq-make-money\` — opportunity discovery with deep intelligence + \`worldwide_hidden=true\`
- \`/bq-update\` — safe BeQuite self-update (backups + non-destructive)

See \`.bequite/\` for memory + state. Named tools are EXAMPLES — see \`.bequite/principles/TOOL_NEUTRALITY.md\`.
Memory-first principle: see \`docs/architecture/MEMORY_FIRST_BEHAVIOR.md\`.

<!-- /BEQUITE -->
EOF
    echo "  appended BeQuite section"
  else
    echo "  BeQuite section already present; skipped"
  fi
fi

# --- 7. Cleanup ---

if [[ -n "${TMP:-}" && -d "$TMP" ]]; then
  rm -rf "$TMP"
fi

# --- 8. Done ---

section "BeQuite $BEQUITE_VERSION installed"
echo
echo "  $(cyan "Run inside Claude Code:")"
echo "    /bequite              gate-aware menu + next 3 recommendations"
echo "    /bq-now               one-line orientation (faster than /bequite)"
echo "    /bq-help              full command reference"
echo "    /bq-init              formally initialize this project"
echo "    /bq-discover          inspect this repo"
echo "    /bq-doctor            environment health"
echo
echo "  $(cyan "Autonomous:")"
echo "    /bq-auto new \"..\"     full P0->P5 lifecycle"
echo "    /bq-auto fix \"..\"     scoped fix mini-cycle"
echo "    /bq-auto uiux variants=5 \"..\"   generate 5 UI directions"
echo "    /bq-live-edit \"..\"               section-by-section frontend edits"
echo
echo "  $(cyan "Opportunity and Workflows (alpha.8 + deep intelligence alpha.10):")"
echo "    /bq-suggest \"<situation>\"        workflow advisor + mode recommendation"
echo "    /bq-job-finder                   real work opportunities (Claude searches)"
echo "    /bq-make-money                   earning opportunities + 10 tracks"
echo "      worldwide_hidden=true          search beyond famous English platforms"
echo "      trending_now=true              last-30-days surge"
echo "      community_discovered=true      Reddit / IH / HN / X / forum signals"
echo "      AI_assisted=true               surface AI-multiplier work paths"
echo
echo "  $(cyan "Maintenance (alpha.10):")"
echo "    /bq-update                       safe BeQuite self-update (backups + no overwrites)"
echo "    /bq-update check                 preview what would change"
echo
echo "  Memory:        .bequite/ (state / logs / plans / tasks / audits / uiux / jobs / money / backups)"
echo "  Commands:      .claude/commands/"
echo "  Skills:        .claude/skills/"
echo "  Reference:     commands.md (repo root) — full command catalog"
echo "  Tool rule:     .bequite/principles/TOOL_NEUTRALITY.md"
echo
