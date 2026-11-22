#!/usr/bin/env bash
# BeQuite update check. Every BeQuite command runs it first (step 1 of the command contract).
#   bash .claude/bequite/bin/bq-update.sh           check (at most once an hour) and install a new release
#   bash .claude/bequite/bin/bq-update.sh --check   report only; never changes a file
#   bash .claude/bequite/bin/bq-update.sh --now     ignore the cache
# Prints one line. Never blocks work: offline or on any error it says "skipped" or "failed" and exits 0.
#
# What it installs by itself, and nothing else:
#   - the latest published GitHub Release of the official repo (xpShawky/BeQuite). A release exists only
#     after the owner pushes a v* tag and the strict self-check passes (.github/workflows/release.yml),
#     so a push to main never reaches anyone by itself;
#   - the tag in "Pinned tag", when one is set (official repo only);
#   - for "Source type: local", the last commit of a BeQuite clone outside this project (never its
#     uncommitted files).
# Any other repo, a path inside this project, or a value that fails validation is reported, never run.
# The version check and the install read the same commit (one clone or one git archive).
# Settings: .bequite/state/UPDATE_SOURCE.md (Source type, Repo URL or local path, Pinned tag, Auto update).
# "New" means: the published VERSION differs from the installed one (a version can go 4.0.0 -> 1.0.0).
# The whole body sits in main(): bash reads it completely before running, so the update may replace this file.

main() {
  official="xpShawky/BeQuite"
  verre='^[0-9]+\.[0-9]+\.[0-9]+([.+-][0-9A-Za-z.-]+)?$'
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
  clean() { printf '%s' "$1" | tr -cd 'A-Za-z0-9._:/@+ -' | cut -c1-100; }   # values from memory files are printed only after this

  installed="$(word "$(field "$ver_md" "Version")")"; installed="${installed#v}"
  printf '%s' "$installed" | grep -Eq "$verre" || installed="unknown"
  source_type="$(word "$(field "$src_md" "Source type")")"; [ -n "$source_type" ] || source_type="github"
  location="$(field "$src_md" "Repo URL or local path" | tr '\\' '/')"
  auto="$(word "$(field "$src_md" "Auto update")")"; [ -n "$auto" ] || auto="on"
  pinned="$(word "$(field "$src_md" "Pinned tag")")"
  case "$pinned" in [0-9]*) pinned="v$pinned" ;; v[0-9]*) ;; *) pinned="" ;; esac
  if [ -n "$pinned" ] && ! printf '%s' "${pinned#v}" | grep -Eq "$verre"; then pinned=""; fi
  now="$(date +%s)"

  # --- 1. where the next version comes from ----------------------------------------------------
  kind="github"; where=""; key=""; report=""; tag=""; loc_abs=""
  case "$source_type" in
    local*)
      kind="local"
      case "$location" in /*|[A-Za-z]:/*) [ -d "$location" ] && loc_abs="$(cd "$location" && pwd)" ;; esac
      where="local $(clean "$location")"
      if [ -z "$loc_abs" ]; then
        echo "BeQuite update check skipped: the local source $(clean "$location") is not an existing absolute path ($src_md). Continuing with v$installed."; return 0
      fi
      case "$loc_abs/" in "$root/"*)
        echo "BeQuite update check skipped: the local source is inside this project; BeQuite never installs from there ($src_md). Continuing with v$installed."; return 0 ;;
      esac
      if ! git -C "$loc_abs" rev-parse --is-inside-work-tree >/dev/null 2>&1 || [ ! -f "$loc_abs/scripts/install-bequite.sh" ] || [ ! -d "$loc_abs/templates/bequite" ]; then
        echo "BeQuite update check skipped: $(clean "$loc_abs") is not a BeQuite git clone. Continuing with v$installed."; return 0
      fi
      key="local|$loc_abs" ;;
    *)
      slug="$(printf '%s' "${location:-https://github.com/$official.git}" | sed -e 's#^https://github.com/##' -e 's#^git@github.com:##' -e 's#\.git$##' -e 's#/$##')"
      if ! printf '%s' "$slug" | grep -Eq '^[A-Za-z0-9-]+/[A-Za-z0-9._-]+$'; then
        echo "BeQuite update check skipped: the repo in $src_md is not a GitHub owner/name. Continuing with v$installed."; return 0
      fi
      where="github.com/$slug"
      lower_slug="$(printf '%s' "$slug" | tr 'A-Z' 'a-z')"; lower_official="$(printf '%s' "$official" | tr 'A-Z' 'a-z')"
      [ "$lower_slug" = "$lower_official" ] || report="updates install by themselves only from github.com/$official; run /bq-update for $where"
      [ -n "$pinned" ] && where="$where@$pinned"
      key="github|$slug|$pinned" ;;
  esac
  key="$key|v$installed"

  write_check() {  # result published
    {
      echo "# BeQuite update check"
      echo
      echo "Written by \`.claude/bequite/bin/bq-update.sh\` at the start of BeQuite commands. Safe to delete."
      echo
      echo "**Last check:** $(date -u +%Y-%m-%dT%H:%M:%SZ)"
      echo "**Last check epoch:** $now"
      echo "**Result:** $1"
      echo "**Installed:** v$installed"
      echo "**Published:** ${2:+v$2}"
      echo "**Source:** $where"
      echo "**Key:** $key"
    } > "$chk_md"
  }

  # --- 2. checked recently for the same source and version: repeat that answer ---------------------
  last="$(field "$chk_md" "Last check epoch")"; result="$(word "$(field "$chk_md" "Result")")"
  cached_pub="$(clean "$(field "$chk_md" "Published")")"; cached_key="$(field "$chk_md" "Key")"
  if [ "$force_now" = false ] && [ "$mode" = "auto" ] && [ "$cached_key" = "$key" ] && [ -n "$last" ] && [ "$last" -eq "$last" ] 2>/dev/null; then
    age=$(( (now - last) / 60 ))
    limit=60; [ "$result" = "failed" ] && limit=1440   # a failed install is retried once a day, not every hour
    if [ "$age" -lt "$limit" ] && [ "$age" -ge 0 ]; then
      case "$result" in
        current|updated) echo "BeQuite v$installed is current (checked $age min ago)."; return 0 ;;
        skipped) echo "BeQuite update check skipped $age min ago (no release reachable). Continuing with v$installed."; return 0 ;;
        available) echo "BeQuite $cached_pub is available (installed: v$installed; checked $age min ago). Run /bq-update."; return 0 ;;
        failed) echo "The last BeQuite update failed $age min ago (see .bequite/logs/UPDATE_LOG.md); it is retried tomorrow. Continuing with v$installed."; return 0 ;;
      esac
    fi
  fi

  # --- 3. the published version ----------------------------------------------------------------
  published=""
  if [ "$kind" = "local" ]; then
    published="$(git -C "$loc_abs" show HEAD:VERSION 2>/dev/null | tr -d ' \r\n')"
  elif [ -n "$pinned" ]; then
    tag="$pinned"; published="$pinned"
  elif command -v curl >/dev/null 2>&1; then
    tag="$(curl -fsSL --proto '=https' --max-time 8 -H 'Accept: application/vnd.github+json' "https://api.github.com/repos/$slug/releases/latest" 2>/dev/null \
      | grep -oE '"tag_name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n 1 | sed 's/.*"\([^"]*\)"$/\1/')"
    published="$tag"
  fi
  published="${published#v}"
  if ! printf '%s' "$published" | grep -Eq "$verre"; then
    write_check "skipped" ""
    echo "BeQuite update check skipped: no release found at $where (offline, or nothing released yet). Continuing with v$installed."
    return 0
  fi

  # --- 4. same version: done -------------------------------------------------------------------
  if [ "$published" = "$installed" ]; then
    write_check "current" "$published"
    echo "BeQuite v$installed is the latest ($where)."
    return 0
  fi

  # --- 5. a different version: report, or install it -------------------------------------------
  [ "$mode" = "check" ] && report="report only (--check)"
  [ "$auto" != "on" ] && report="Auto update is $(clean "$auto") in $src_md"
  if [ -n "$report" ]; then
    write_check "available" "$published"
    echo "BeQuite v$published is available (installed: v$installed; $report). Run /bq-update to install it."
    return 0
  fi
  command -v git >/dev/null 2>&1 || { write_check "skipped" "$published"; echo "BeQuite v$published is available but git is missing, so it cannot install. Continuing with v$installed."; return 0; }

  lock=".bequite/state/update.lock"
  if ! mkdir "$lock" 2>/dev/null; then
    if [ -n "$(find "$lock" -maxdepth 0 -mmin +10 2>/dev/null)" ] && rmdir "$lock" 2>/dev/null && mkdir "$lock" 2>/dev/null; then :; else
      echo "Another BeQuite session is updating this project right now. Continuing with v$installed."; return 0
    fi
  fi
  tmp="$(mktemp -d 2>/dev/null || true)"
  [ -n "$tmp" ] && [ -d "$tmp" ] || { rmdir "$lock" 2>/dev/null; echo "BeQuite update skipped: no temp folder. Continuing with v$installed."; return 0; }
  trap 'rm -rf "${tmp:?}"; rmdir "$lock" 2>/dev/null' EXIT

  stamp="$(date +%Y%m%d-%H%M%S)-$$"; backup=".bequite/backups/$stamp-v$installed"; log=".bequite/logs/UPDATE_LOG.md"
  mkdir -p "$backup/.claude/skills" "$backup/.bequite/state" .bequite/logs || { echo "BeQuite update skipped: could not create $backup. Continuing with v$installed."; return 0; }
  [ -d .claude/commands ] && cp -R .claude/commands "$backup/.claude/commands"
  for d in .claude/skills/bequite-*/; do [ -d "$d" ] && cp -R "${d%/}" "$backup/.claude/skills/"; done
  [ -d .claude/bequite ] && cp -R .claude/bequite "$backup/.claude/bequite"
  for x in hooks agents; do [ -d ".claude/$x" ] && cp -R ".claude/$x" "$backup/.claude/$x"; done
  for f in CLAUDE.md commands.md; do [ -f "$f" ] && cp "$f" "$backup/$f"; done
  [ -f "$ver_md" ] && cp "$ver_md" "$backup/$ver_md"
  { echo; echo "## $(date -u +%Y-%m-%dT%H:%M:%SZ) automatic update v$installed -> v$published ($where)"; echo; echo "Backup: $backup"; echo; echo '```'; } >> "$log"

  ok=1; mkdir -p "$tmp/src"
  if [ "$kind" = "local" ]; then
    git -c core.autocrlf=false -C "$loc_abs" archive --format=tar HEAD 2>>"$log" | tar -x -C "$tmp/src" 2>>"$log" || ok=0
  else
    GIT_TERMINAL_PROMPT=0 GIT_HTTP_LOW_SPEED_LIMIT=1000 GIT_HTTP_LOW_SPEED_TIME=20 \
      git -c advice.detachedHead=false -c core.autocrlf=false clone --quiet --depth 1 --branch "$tag" "https://github.com/$official.git" "$tmp/src" >>"$log" 2>&1 || ok=0
  fi
  got="$(tr -d ' \r\n' < "$tmp/src/VERSION" 2>/dev/null)"; got="${got#v}"
  if [ "$ok" = 1 ] && [ "$got" != "$published" ]; then echo "VERSION in the downloaded source is '$got', expected $published: not installed." >> "$log"; ok=0; fi
  if [ "$ok" = 1 ]; then
    BEQUITE_INSTALLED_FROM="$where" bash "$tmp/src/scripts/install-bequite.sh" --from-local "$tmp/src" --force >> "$log" 2>&1 || ok=0
  fi
  echo '```' >> "$log"
  now_ver="$(word "$(field "$ver_md" "Version")")"; now_ver="${now_ver#v}"
  if [ "$ok" = 1 ] && [ "$now_ver" = "$published" ] && [ -f .claude/bequite/bin/bq-update.sh ] && [ -f .claude/commands/bequite.md ]; then
    installed="$published"; key="${key%|v*}|v$published"
    write_check "updated" "$published"
    echo "BeQuite updated to v$published from $where (backup: $backup). The new commands load from the next command on; carry on with the task."
  else
    # put the previous files back (copy over; nothing is deleted)
    [ -d "$backup/.claude" ] && cp -R "$backup/.claude/." .claude/ 2>/dev/null
    for f in CLAUDE.md commands.md "$ver_md"; do [ -f "$backup/$f" ] && cp "$backup/$f" "$f"; done
    echo "Restored the previous files from $backup." >> "$log"
    write_check "failed" "$published"
    echo "BeQuite update to v$published did not finish and the previous files were put back (log: $log). Carry on with the task and tell the user."
  fi
  return 0
}

main "$@"
exit 0
