#!/usr/bin/env bash
# Install BeQuite (lightweight Claude Code workflow pack) into the current project.
#
# Usage (run inside the project you want to enhance):
#   curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash
# From a local clone:
#   /path/to/BeQuite/scripts/install-bequite.sh --from-local /path/to/BeQuite [--force]
#
# --force re-installs commands and skills over an existing install.
# Project memory in .bequite/ is NEVER overwritten (missing files are added).

set -uo pipefail

BEQUITE_VERSION="v3.0.0-alpha.25"
REPO_URL="https://github.com/xpShawky/BeQuite.git"
TARGET="$(pwd)"
FROM_LOCAL=""
FORCE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from-local) FROM_LOCAL="${2:-}"; shift 2 ;;
    --force) FORCE=true; shift ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

yellow() { printf '\033[33m%s\033[0m' "$*"; }
green()  { printf '\033[32m%s\033[0m' "$*"; }
red()    { printf '\033[31m%s\033[0m' "$*"; }
section() { echo; echo "$(yellow "==> $1")"; }

echo
echo "  $(yellow "BeQuite installer ($BEQUITE_VERSION)")"
echo "  Target: $TARGET"

# --- 1. Existing install? ---------------------------------------------------
if [[ -f "./.claude/commands/bequite.md" && "$FORCE" != true ]]; then
  echo
  echo "$(yellow "BeQuite is already installed here.")"
  echo "Re-run with --force to refresh commands and skills. Your .bequite/ memory is never overwritten."
  exit 1
fi

# --- 2. Source ----------------------------------------------------------------
TMP=""
cleanup() { [[ -n "$TMP" && -d "$TMP" ]] && rm -rf "$TMP"; }
trap cleanup EXIT

if [[ -n "$FROM_LOCAL" ]]; then
  [[ -d "$FROM_LOCAL" ]] || { echo "$(red "FATAL:") '$FROM_LOCAL' does not exist." >&2; exit 1; }
  SOURCE="$(cd "$FROM_LOCAL" && pwd)"
  section "Using local BeQuite source at $SOURCE"
else
  command -v git >/dev/null 2>&1 || { echo "$(red "FATAL:") git not found. Install git or use --from-local <path>." >&2; exit 1; }
  section "Downloading BeQuite from $REPO_URL"
  TMP="$(mktemp -d -t bequite-installer-XXXXXX)"
  git clone --quiet --depth 1 "$REPO_URL" "$TMP" || { echo "$(red "FATAL:") clone failed." >&2; exit 1; }
  SOURCE="$TMP"
fi
[[ -d "$SOURCE/templates/bequite" ]] || { echo "$(red "FATAL:") $SOURCE has no templates/bequite (old or wrong source)." >&2; exit 1; }

# --- 3. Commands, skills, hooks ---------------------------------------------
section "Installing commands and skills"
mkdir -p ./.claude/commands ./.claude/skills
cp -r "$SOURCE/.claude/commands/"*.md ./.claude/commands/
for skill in "$SOURCE"/.claude/skills/bequite-*/; do
  name="$(basename "$skill")"
  rm -rf "./.claude/skills/$name"
  cp -r "$skill" "./.claude/skills/$name"
done
echo "  $(green "$(ls -1 ./.claude/commands/*.md | wc -l | tr -d ' ') commands, $(ls -d ./.claude/skills/bequite-*/ | wc -l | tr -d ' ') skills")"

if [[ -d "$SOURCE/.claude/hooks" ]]; then
  mkdir -p ./.claude/hooks
  cp -r "$SOURCE/.claude/hooks/"* ./.claude/hooks/ 2>/dev/null || true
  for ex in settings.json.example settings.windows.json.example; do
    [[ -f "$SOURCE/.claude/$ex" ]] && cp "$SOURCE/.claude/$ex" "./.claude/$ex"
  done
  echo "  safety hooks copied but NOT active (opt-in: run /bq-hooks status)"
fi

# --- 4. Memory scaffold (never overwrites) ----------------------------------
section "Preparing .bequite/ memory"
added=0
while IFS= read -r -d '' src; do
  rel="${src#"$SOURCE/templates/bequite/"}"
  dst="./.bequite/$rel"
  if [[ ! -e "$dst" ]]; then
    mkdir -p "$(dirname "$dst")"
    sed "s/{{VERSION}}/$BEQUITE_VERSION/g" "$src" > "$dst"
    added=$((added + 1))
  fi
done < <(find "$SOURCE/templates/bequite" -type f -print0)
echo "  $added files added (existing memory left untouched)"

if [[ -f "$SOURCE/commands.md" ]]; then cp "$SOURCE/commands.md" ./commands.md; fi

# --- 5. CLAUDE.md -------------------------------------------------------------
section "Updating CLAUDE.md"
block="$(sed "s/{{VERSION}}/$BEQUITE_VERSION/g" "$SOURCE/templates/CLAUDE.bequite.md")"
if [[ ! -f ./CLAUDE.md ]]; then
  printf '# CLAUDE.md\n\n%s\n' "$block" > ./CLAUDE.md
  echo "  created CLAUDE.md"
elif grep -q "<!-- BEQUITE -->" ./CLAUDE.md; then
  BQ_BLOCK="$block" awk '
    /<!-- BEQUITE -->/ {print ENVIRON["BQ_BLOCK"]; skip=1; next}
    /<!-- \/BEQUITE -->/ {skip=0; next}
    !skip {print}
  ' ./CLAUDE.md > ./CLAUDE.md.bqtmp && mv ./CLAUDE.md.bqtmp ./CLAUDE.md
  echo "  refreshed the BeQuite section"
else
  printf '\n---\n\n%s\n' "$block" >> ./CLAUDE.md
  echo "  appended the BeQuite section"
fi

# --- 6. Done ------------------------------------------------------------------
section "BeQuite $BEQUITE_VERSION installed"
echo
echo "  In Claude Code, start with:"
echo "    /bequite        menu: project state + next recommended commands"
echo "    /bq-help        full command reference (also commands.md)"
echo "    /bq-auto \"..\"   autonomous runner; stops only at hard gates"
echo
