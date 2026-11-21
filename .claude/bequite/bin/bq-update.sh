#!/usr/bin/env bash
# BeQuite update check. Every BeQuite command runs it first (step 1 of the command contract).
#   bash .claude/bequite/bin/bq-update.sh           check (at most once an hour) and update when a newer BeQuite is published
#   bash .claude/bequite/bin/bq-update.sh --check   report only; never changes a file
#   bash .claude/bequite/bin/bq-update.sh --now     ignore the one-hour cache
# Prints one line. Never blocks work: offline or on any error it says "skipped" and exits 0.
# Settings: .bequite/state/UPDATE_SOURCE.md (Source type, Repo URL or local path, Default branch, Pinned tag, Auto update).
# "Newer" means: the VERSION published at the source differs from the installed one (a version can go 4.0.0 -> 1.0.0).
# The whole body sits in main(): bash reads it completely before running, so the update may replace this file safely.

main() {
  mode="auto"; force_now=false
  for a in "$@"; do
    case "$a" in
      --check) mode="check" ;;
      --now) force_now=true ;;
    esac
  done

  here="$(cd "$(dirname "$0")" && pwd)"
  root="$(cd "$here/../../.." && pwd)"
  cd "$root" || { echo "BeQuite update check skipped: project folder not found."; return 0; }
  src_md=".bequite/state/UPDATE_SOURCE.md"; ver_md=".bequite/state/BEQUITE_VERSION.md"; chk_md=".bequite/state/UPDATE_CHECK.md"
  [ -d .bequite/state ] || { echo "BeQuite update check skipped: no .bequite/state here."; return 0; }
  if [ -d templates/bequite ] && [ -f scripts/install-bequite.sh ]; then echo "BeQuite update check skipped: this is the BeQuite source repo (updates never install over it)."; return 0; fi

  field() { [ -f "$1" ] && sed -n "s/^\*\*$2:\*\* *//p" "$1" | head -n 1 | tr -d '\r' | sed 's/[[:space:]]*$//'; }
  word() { printf '%s' "$1" | awk '{print $1}'; }

  installed="$(field "$ver_md" "Version")"; installed="${installed#v}"
  source_type="$(word "$(field "$src_md" "Source type")")"; [ -n "$source_type" ] || source_type="github"
  location="$(field "$src_md" "Repo URL or local path" | tr '\\' '/')"; [ -n "$location" ] || location="https://github.com/xpShawky/BeQuite.git"
  branch="$(word "$(field "$src_md" "Default branch")")"; [ -n "$branch" ] || branch="main"
  auto="$(word "$(field "$src_md" "Auto update")")"; [ -n "$auto" ] || auto="on"
  pinned="$(word "$(field "$src_md" "Pinned tag")")"
  case "$pinned" in ""|"("*) pinned="" ;; esac
  now="$(date +%s)"

  write_check() {  # result installed published
    {
      echo "# BeQuite update check"
      echo
      echo "Written by \`.claude/bequite/bin/bq-update.sh\` at the start of BeQuite commands. Safe to delete."
      echo
      echo "**Last check:** $(date -u +%Y-%m-%dT%H:%M:%SZ)"
      echo "**Last check epoch:** $now"
      echo "**Result:** $1"
      echo "**Installed:** v$2"
      echo "**Published:** ${3:+v$3}"
      echo "**Source:** $where"
    } > "$chk_md"
  }

  # 1. checked within the hour: repeat that answer (an offline machine must not wait on every command)
  last="$(field "$chk_md" "Last check epoch")"; result="$(word "$(field "$chk_md" "Result")")"
  cached_pub="$(field "$chk_md" "Published")"
  if [ "$force_now" = false ] && [ "$mode" = "auto" ] && [ -n "$last" ] && [ "$last" -eq "$last" ] 2>/dev/null; then
    age=$(( (now - last) / 60 ))
    if [ "$age" -lt 60 ] && [ "$age" -ge 0 ]; then
      case "$result" in
        current|updated) echo "BeQuite v$installed is current (checked $age min ago)."; return 0 ;;
        skipped) echo "BeQuite update check skipped $age min ago (no published version reachable). Continuing with v$installed."; return 0 ;;
        available) echo "BeQuite $cached_pub is available (installed: v$installed; checked $age min ago). Run /bq-update."; return 0 ;;
        failed) echo "The last BeQuite update failed $age min ago (see .bequite/logs/UPDATE_LOG.md). Continuing with v$installed."; return 0 ;;
      esac
    fi
  fi

  # 2. the published version
  published=""; slug=""
  case "$source_type" in
    local*)
      where="$location (local)"
      [ -f "$location/VERSION" ] && published="$(tr -d ' \r\n' < "$location/VERSION")" ;;
    *)
      slug="$(printf '%s' "$location" | sed -e 's#^https://github.com/##' -e 's#^git@github.com:##' -e 's#\.git$##' -e 's#/$##')"
      where="github.com/$slug ($branch)"
      if command -v curl >/dev/null 2>&1; then
        published="$(curl -fsSL --max-time 6 "https://raw.githubusercontent.com/$slug/$branch/VERSION" 2>/dev/null | tr -d ' \r\n')"
      fi ;;
  esac
  published="${published#v}"
  if ! printf '%s' "$published" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+([.+-][0-9A-Za-z.-]+)?$'; then
    write_check "skipped" "$installed" ""
    echo "BeQuite update check skipped: no published version found at $where (offline or nothing released yet). Continuing with v$installed."
    return 0
  fi

  # 3. same version: done
  if [ "$published" = "$installed" ]; then
    write_check "current" "$installed" "$published"
    echo "BeQuite v$installed is the latest ($where)."
    return 0
  fi

  # 4. a different version is published: report, or update
  if [ "$mode" = "check" ] || [ "$auto" != "on" ] || [ -n "$pinned" ]; then
    write_check "available" "$installed" "$published"
    echo "BeQuite v$published is available (installed: v$installed). Run /bq-update, or set Auto update: on in $src_md."
    return 0
  fi

  stamp="$(date +%Y%m%d-%H%M%S)"; backup=".bequite/backups/$stamp-v$installed"; log=".bequite/logs/UPDATE_LOG.md"
  mkdir -p "$backup/.claude/skills" .bequite/logs || { echo "BeQuite update skipped: could not create $backup. Continuing with v$installed."; return 0; }
  [ -d .claude/commands ] && cp -R .claude/commands "$backup/.claude/commands"
  for d in .claude/skills/bequite-*/; do [ -d "$d" ] && cp -R "${d%/}" "$backup/.claude/skills/"; done
  [ -d .claude/bequite ] && cp -R .claude/bequite "$backup/.claude/bequite"
  for x in hooks agents; do [ -d ".claude/$x" ] && cp -R ".claude/$x" "$backup/.claude/$x"; done
  for f in CLAUDE.md commands.md; do [ -f "$f" ] && cp "$f" "$backup/$f"; done
  { echo; echo "## $(date -u +%Y-%m-%dT%H:%M:%SZ) automatic update v$installed -> v$published ($where)"; echo; echo "Backup: $backup"; echo; echo '```'; } >> "$log"
  ok=1
  case "$source_type" in
    local*) bash "$location/scripts/install-bequite.sh" --from-local "$location" --force >> "$log" 2>&1 || ok=0 ;;
    *)
      tmp="$(mktemp 2>/dev/null || echo ".bequite/backups/bq-install-$stamp.sh")"
      if curl -fsSL --max-time 30 "https://raw.githubusercontent.com/$slug/$branch/scripts/install-bequite.sh" -o "$tmp"; then
        bash "$tmp" --force >> "$log" 2>&1 || ok=0
      else ok=0; fi
      rm -f "$tmp" ;;
  esac
  echo '```' >> "$log"
  now_ver="$(field "$ver_md" "Version")"; now_ver="${now_ver#v}"
  if [ "$ok" = 1 ] && [ "$now_ver" = "$published" ]; then
    write_check "updated" "$published" "$published"
    echo "BeQuite updated v$installed -> v$published from $where (backup: $backup). The new commands load from the next command on; carry on with the task."
  else
    write_check "failed" "$installed" "$published"
    echo "BeQuite update to v$published did not finish (log: $log). The previous version is in $backup. Carry on with the task and tell the user."
  fi
  return 0
}

main "$@"
exit 0
