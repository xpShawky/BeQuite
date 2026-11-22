#!/usr/bin/env bash
# Install BeQuite (lightweight Claude Code workflow pack) into the current project.
#
# Usage (run inside the project you want to enhance):
#   curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/install-bequite.sh | bash
# From a local clone:
#   /path/to/BeQuite/scripts/install-bequite.sh --from-local /path/to/BeQuite [--force]
#
# --force re-installs commands and skills over an existing install.
# --packs core,studio,business picks the packs (core is always installed; default: all three, or the
#   choice saved in .bequite/state/PACKS.md by an earlier install, so updates keep the same packs).
# Project memory in .bequite/ is NEVER overwritten (missing files are added).

set -uo pipefail

BEQUITE_VERSION="v1.0.0"
REPO_URL="https://github.com/xpShawky/BeQuite.git"
TARGET="$(pwd)"
FROM_LOCAL=""
FORCE=false
PACKS=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from-local) FROM_LOCAL="${2:-}"; shift 2 ;;
    --force) FORCE=true; shift ;;
    --packs) PACKS="${2:-}"; shift 2 ;;
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
# the source's VERSION file is the version being installed (the constant above is only the fallback)
if [[ -f "$SOURCE/VERSION" ]]; then BEQUITE_VERSION="v$(tr -d ' \r\n' < "$SOURCE/VERSION" | sed 's/^v//')"; fi
STAMP="$(date +%Y%m%d-%H%M%S)"
# packs: the flag, else the choice saved by an earlier install, else all three; core is always in
if [[ -z "$PACKS" && -f ./.bequite/state/PACKS.md ]]; then PACKS="$(sed -n 's/^\*\*Packs:\*\* *//p' ./.bequite/state/PACKS.md | head -n 1 | tr -d '\r ')"; fi
[[ -z "$PACKS" ]] && PACKS="core,studio,business"
PACKS="core,$(printf '%s' "$PACKS" | tr -d ' ' | sed 's/core,\{0,1\}//g; s/,$//')"; PACKS="${PACKS%,}"
EXCLUDE=""
if [[ -f "$SOURCE/.claude/bequite/PACKS.txt" ]]; then
  while read -r pk path || [[ -n "$pk" ]]; do
    pk="$(printf '%s' "$pk" | tr -d '\r')"; path="$(printf '%s' "$path" | tr -d '\r')"
    [[ -z "$pk" || "$pk" == \#* ]] && continue
    case ",$PACKS," in *",$pk,"*) ;; *) EXCLUDE="$EXCLUDE|$path|" ;; esac
  done < "$SOURCE/.claude/bequite/PACKS.txt"
fi
excluded() { case "$EXCLUDE" in *"|$1|"*) return 0 ;; esac; return 1; }

# --- 3. Commands, skills, hooks ---------------------------------------------
section "Installing commands and skills"
mkdir -p ./.claude/commands ./.claude/skills
for cmd in "$SOURCE"/.claude/commands/*.md; do
  excluded "commands/$(basename "$cmd")" || cp "$cmd" ./.claude/commands/
done
for skill in "$SOURCE"/.claude/skills/bequite-*/; do
  name="$(basename "$skill")"
  excluded "skills/$name" && continue
  rm -rf "./.claude/skills/$name"
  cp -r "$skill" "./.claude/skills/$name"
done
find ./.claude/skills -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
if [[ -d "$SOURCE/agents" ]]; then mkdir -p ./.claude/agents && cp "$SOURCE"/agents/bq-*.md ./.claude/agents/ 2>/dev/null || true; fi
rm -rf ./.claude/bequite
cp -r "$SOURCE/.claude/bequite" ./.claude/bequite
# files a newer version removed: move them aside, never delete
moved=0
if [[ -f "$SOURCE/.claude/bequite/REMOVED.txt" ]]; then
  while IFS= read -r p || [[ -n "$p" ]]; do
    p="$(printf '%s' "$p" | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    [[ -z "$p" || "$p" == \#* || "$p" == *..* ]] && continue
    if [[ "$p" == hooks/* ]] && grep -qsF "$p" ./.claude/settings.json ./.claude/settings.local.json; then
      echo "  kept .claude/$p: your Claude Code settings still run it (remove it from the settings, then delete the file)"
      continue
    fi
    if [[ -e "./.claude/$p" ]]; then
      mkdir -p "$(dirname "./.bequite/backups/$STAMP-removed/.claude/$p")"
      mv "./.claude/$p" "./.bequite/backups/$STAMP-removed/.claude/$p" && moved=$((moved + 1))
    fi
  done < "$SOURCE/.claude/bequite/REMOVED.txt"
fi
echo "  $(green "$(ls -1 ./.claude/commands/*.md | wc -l | tr -d ' ') commands, $(ls -d ./.claude/skills/bequite-*/ | wc -l | tr -d ' ') skills, $(ls -1 ./.claude/agents/bq-*.md 2>/dev/null | wc -l | tr -d ' ') subagents (packs: $PACKS)")"
[[ $moved -gt 0 ]] && echo "  $moved removed command or skill file(s) moved to .bequite/backups/$STAMP-removed/"

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
had_source_md=false; [[ -f ./.bequite/state/UPDATE_SOURCE.md ]] && had_source_md=true
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

# the pack choice is remembered so updates install the same packs
mkdir -p ./.bequite/state
printf '# BeQuite packs

**Packs:** %s

Change with: install-bequite.sh --force --packs core,studio,business (or $env:BEQUITE_PACKS on Windows).
' "$PACKS" > ./.bequite/state/PACKS.md
# version metadata is not memory: it always says what is installed now
vf=./.bequite/state/BEQUITE_VERSION.md
if [[ -f "$vf" ]]; then
  old_v="$(sed -n 's/^\*\*Version:\*\* *//p' "$vf" | head -n 1 | tr -d '\r' | sed 's/[[:space:]]*$//')"
  if [[ "$old_v" != "$BEQUITE_VERSION" ]]; then
    # awk takes the values from the environment, so no program is ever built from file contents
    if BQ_NEW="$BEQUITE_VERSION" BQ_OLD="$old_v" awk '
         /^\*\*Version:\*\*/ {print "**Version:** " ENVIRON["BQ_NEW"]; next}
         /^\*\*Previous version:\*\*/ {print "**Previous version:** " ENVIRON["BQ_OLD"]; next}
         /^\(none yet\)/ {next}
         {print}
       ' "$vf" > "$vf.bqtmp.$$" && mv "$vf.bqtmp.$$" "$vf"; then
      printf -- '- %s: %s -> %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$old_v" "$BEQUITE_VERSION" >> "$vf"
      echo "  version metadata: $old_v -> $BEQUITE_VERSION"
    else
      rm -f "$vf.bqtmp.$$"; echo "  $(red "could not rewrite") $vf" >&2; exit 1
    fi
  fi
fi
# a first install from a local clone keeps updating from that clone (change it in UPDATE_SOURCE.md)
sf=./.bequite/state/UPDATE_SOURCE.md
# (not when the automatic update runs this installer from its own temporary copy)
if [[ "$had_source_md" == false && -n "$FROM_LOCAL" && -z "${BEQUITE_INSTALLED_FROM:-}" && -f "$sf" ]]; then
  BQ_SRC="$SOURCE" awk '
    /^\*\*Source type:\*\*/ {print "**Source type:** local"; next}
    /^\*\*Repo URL or local path:\*\*/ {print "**Repo URL or local path:** " ENVIRON["BQ_SRC"]; next}
    {print}
  ' "$sf" > "$sf.bqtmp.$$" && mv "$sf.bqtmp.$$" "$sf"
  echo "  updates will come from $SOURCE (UPDATE_SOURCE.md)"
fi
# the automatic update switch is always visible (older memory files have no such line)
if [[ -f "$sf" ]] && ! grep -q '^\*\*Auto update:\*\*' "$sf"; then
  printf '\n**Auto update:** on (BeQuite installs new official releases by itself; set to off to be told instead)\n' >> "$sf"
  echo "  added the Auto update switch to UPDATE_SOURCE.md (on)"
fi

if [[ -f "$SOURCE/commands.md" ]]; then cp "$SOURCE/commands.md" ./commands.md; fi

# --- 5. CLAUDE.md -------------------------------------------------------------
section "Updating CLAUDE.md"
block="$(sed "s/{{VERSION}}/$BEQUITE_VERSION/g" "$SOURCE/templates/CLAUDE.bequite.md")"
if [[ ! -f ./CLAUDE.md ]]; then
  printf '# CLAUDE.md\n\n%s\n' "$block" > ./CLAUDE.md
  echo "  created CLAUDE.md"
elif grep -q "<!-- BEQUITE -->" ./CLAUDE.md && grep -q "<!-- /BEQUITE -->" ./CLAUDE.md; then
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
echo "  Every BeQuite command first checks for a new official release and installs it (off switch: .bequite/state/UPDATE_SOURCE.md)."
echo
