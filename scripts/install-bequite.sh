#!/usr/bin/env bash
# Install BeQuite (lightweight skill pack) into the current project.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash
#
# Or from a local clone:
#   /path/to/BeQuite/scripts/install-bequite.sh --from-local /path/to/BeQuite

set -uo pipefail

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
echo "  $(yellow "BeQuite installer (lightweight skill pack)")"
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

# --- 3. .claude/commands/ ---

section "Installing .claude/commands/"
mkdir -p "./.claude/commands"
cp -r "$SOURCE/.claude/commands/"* "./.claude/commands/"
count=$(ls -1 ./.claude/commands/*.md 2>/dev/null | wc -l)
echo "  $(green "$count slash commands installed")"

# --- 4. .claude/skills/bequite-* ---

section "Installing .claude/skills/bequite-*"
mkdir -p "./.claude/skills"
for skill in "$SOURCE"/.claude/skills/bequite-*/; do
  if [[ -d "$skill" ]]; then
    name="$(basename "$skill")"
    cp -r "$skill" "./.claude/skills/$name"
    echo "  + $name"
  fi
done

# --- 5. .bequite/ scaffold ---

section "Scaffolding .bequite/ memory"
mkdir -p ./.bequite/{state,logs,prompts/user_prompts,prompts/generated_prompts,prompts/model_outputs,audits,plans,tasks}
echo "  scaffold ready"

# --- 6. CLAUDE.md ---

section "Updating CLAUDE.md"

BQ_MARKER="<!-- BEQUITE -->"

if [[ ! -f "./CLAUDE.md" ]]; then
  cat > ./CLAUDE.md <<EOF
# CLAUDE.md

This project uses **BeQuite** — a lightweight Claude Code skill pack.

$BQ_MARKER

## How to use BeQuite here

- Run \`/bequite\` to see the menu.
- Run \`/bq-help\` for the full command reference.
- \`/bq-init\` to formally initialize (creates baseline state files).
- BeQuite memory lives in \`.bequite/\`.
- BeQuite commands live in \`.claude/commands/bequite.md\` + \`.claude/commands/bq-*.md\`.
- BeQuite skills live in \`.claude/skills/bequite-*/\`.

## Core operating rules (BeQuite)

- Never claim a task is "done" unless \`/bq-verify\` passes.
- Always update \`.bequite/logs/AGENT_LOG.md\` when you take a real action.
- Banned weasel words: should, probably, seems to, appears to, I think it works, might, hopefully, in theory.

<!-- /BEQUITE -->
EOF
  echo "  created CLAUDE.md"
else
  if ! grep -q "$BQ_MARKER" ./CLAUDE.md; then
    cat >> ./CLAUDE.md <<EOF

---

$BQ_MARKER

# BeQuite

This project uses **BeQuite** — a lightweight Claude Code skill pack.

Run \`/bequite\` to see the menu. See \`.bequite/\` for memory + state.

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

section "BeQuite installed"
echo
echo "  $(cyan "Run inside Claude Code:")"
echo "    /bequite        the menu"
echo "    /bq-help        full command reference"
echo "    /bq-init        formally initialize this project"
echo "    /bq-discover    inspect this repo"
echo "    /bq-doctor      environment health"
echo
echo "  Memory:        .bequite/"
echo "  Commands:      .claude/commands/"
echo "  Skills:        .claude/skills/"
echo
