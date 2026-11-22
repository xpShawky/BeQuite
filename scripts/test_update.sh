#!/usr/bin/env bash
# Behaviour test for the automatic update path (bq-update.sh + install-bequite.sh). Offline; CI runs it.
#   bash scripts/test_update.sh
# Builds, in a temp folder, a BeQuite "source" git clone and a project installed from this checkout,
# then runs the update against them: a version with "/" in it, uncommitted files in the source,
# a source inside the project, a non-official repo, a pinned tag, the lock, a failing installer,
# a CLAUDE.md that lost its closing marker, and the Auto update switch.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "${T:?}"' EXIT
SRC="$T/src"; PROJ="$T/proj"
pass=0; fail=0
ok()   { pass=$((pass + 1)); echo "  PASS  $1"; }
bad()  { fail=$((fail + 1)); echo "  FAIL  $1"; [ -n "${2:-}" ] && echo "        got: $2"; }
has()  { case "$2" in *"$3"*) ok "$1" ;; *) bad "$1" "$2" ;; esac; }
hasnt(){ case "$2" in *"$3"*) bad "$1" "$2" ;; *) ok "$1" ;; esac; }
setv() { printf '%s\n' "$1" > "$SRC/VERSION"; git -C "$SRC" add -A >/dev/null; git -C "$SRC" -c user.name=t -c user.email=t@t commit -qm "v$1"; }
setfield() {  # file field value
  BQ_F="$2" BQ_V="$3" awk 'BEGIN{f="**" ENVIRON["BQ_F"] ":**"} index($0, f)==1 {print f " " ENVIRON["BQ_V"]; next} {print}' "$1" > "$1.t" && mv "$1.t" "$1"
}
upd() { (cd "$PROJ" && bash .claude/bequite/bin/bq-update.sh --now "$@" 2>&1); }
ver() { sed -n 's/^\*\*Version:\*\* *//p' "$PROJ/.bequite/state/BEQUITE_VERSION.md" | head -n 1 | tr -d '\r'; }

echo "BeQuite update path test (temp: $T)"
# --- the source clone: this checkout's pack, committed ---
mkdir -p "$SRC/.claude"
for p in templates scripts agents hooks .claude-plugin commands.md VERSION; do [ -e "$REPO/$p" ] && cp -R "$REPO/$p" "$SRC/"; done
for p in commands skills bequite hooks settings.json.example settings.windows.json.example; do [ -e "$REPO/.claude/$p" ] && cp -R "$REPO/.claude/$p" "$SRC/.claude/"; done
git -C "$SRC" -c core.autocrlf=false init -q && git -C "$SRC" config core.autocrlf false && setv 9.9.1
echo "uncommitted" > "$SRC/.claude/commands/zz-uncommitted.md"

# --- the project: installed from this checkout, then pointed at the source clone ---
mkdir -p "$PROJ" && (cd "$PROJ" && bash "$REPO/scripts/install-bequite.sh" --from-local "$REPO" >/dev/null 2>&1)
[ -f "$PROJ/.claude/bequite/bin/bq-update.sh" ] && ok "fresh install has the update script" || bad "fresh install has the update script"
S="$PROJ/.bequite/state/UPDATE_SOURCE.md"
setfield "$S" "Repo URL or local path" "$SRC"
setfield "$PROJ/.bequite/state/BEQUITE_VERSION.md" "Version" "v1.0.0 - test install (model/effort/confidence)"

out="$(upd --check)"; has "--check reports the new version" "$out" "v9.9.1 is available"
out="$(upd)";         has "auto installs it" "$out" "updated to v9.9.1"
[ "$(ver)" = "v9.9.1" ] && ok "version line rewritten even with '/' in the old value" || bad "version line rewritten" "$(ver)"
grep -q '^\*\*Previous version:\*\* v1.0.0 - test install (model/effort/confidence)' "$PROJ/.bequite/state/BEQUITE_VERSION.md" && ok "previous version kept verbatim" || bad "previous version kept verbatim"
[ ! -e "$PROJ/.claude/commands/zz-uncommitted.md" ] && ok "uncommitted source files are not installed" || bad "uncommitted source files are not installed"
b="$(ls -d "$PROJ"/.bequite/backups/*-v1.0.0 2>/dev/null | head -n 1)"
[ -f "$b/.claude/skills/bequite-orchestrator/SKILL.md" ] && ok "backup keeps each skill in its own folder" || bad "backup keeps each skill in its own folder" "$b"
out="$(upd)";         has "second run: current" "$out" "is the latest"
grep -q '^\*\*Source type:\*\* local' "$S" && grep -qF "$SRC" "$S" && ok "update did not repoint the source at its temp copy" || bad "update did not repoint the source"

# --- lock: a second session waits ---
setv 9.9.2
mkdir "$PROJ/.bequite/state/update.lock"
out="$(upd)";         has "lock held: no second install" "$out" "Another BeQuite session"
rmdir "$PROJ/.bequite/state/update.lock"
out="$(upd)";         has "lock free: installs" "$out" "updated to v9.9.2"

# --- a failing installer: previous files come back ---
printf '#!/usr/bin/env bash\necho broken; exit 1\n' > "$SRC/scripts/install-bequite.sh"; setv 9.9.3
out="$(upd)";         has "failed install is reported" "$out" "previous files were put back"
[ "$(ver)" = "v9.9.2" ] && ok "version unchanged after a failed install" || bad "version unchanged after a failed install" "$(ver)"
out="$(cd "$PROJ" && bash .claude/bequite/bin/bq-update.sh 2>&1)"; has "a failure is not retried within the day" "$out" "retried tomorrow"
git -C "$SRC" checkout -q HEAD~1 -- scripts/install-bequite.sh && setv 9.9.4

# --- sources that must never run ---
mkdir -p "$PROJ/.bequite/evil/templates/bequite" "$PROJ/.bequite/evil/scripts"
setfield "$S" "Repo URL or local path" "$PROJ/.bequite/evil"
out="$(upd)";         has "a source inside the project is refused" "$out" "inside this project"
setfield "$S" "Repo URL or local path" "relative/path"
out="$(upd)";         has "a relative local path is refused" "$out" "not an existing absolute path"
setfield "$S" "Source type" "github"; setfield "$S" "Repo URL or local path" "https://github.com/attacker/BeQuite.git"; setfield "$S" "Pinned tag" "v9.9.9"
out="$(upd)";         has "another repo is reported, not installed" "$out" "only from github.com/xpShawky/BeQuite"
setfield "$S" "Repo URL or local path" 'x;touch /tmp/pwn'
out="$(upd)";         has "a malformed repo is refused" "$out" "not a GitHub owner/name"
[ "$(ver)" = "v9.9.2" ] && ok "nothing was installed by the refused sources" || bad "nothing was installed by the refused sources" "$(ver)"

# --- CLAUDE.md without its closing marker keeps the user's sections ---
printf '# CLAUDE.md\n\n<!-- BEQUITE -->\nold block\n\n## My own section\nkeep me\n' > "$PROJ/CLAUDE.md"
(cd "$PROJ" && bash "$REPO/scripts/install-bequite.sh" --from-local "$REPO" --force >/dev/null 2>&1)
grep -q "keep me" "$PROJ/CLAUDE.md" && ok "CLAUDE.md sections after a broken block survive" || bad "CLAUDE.md sections after a broken block survive"

# --- the Auto update switch is added where an old memory file lacks it ---
grep -v '^\*\*Auto update:\*\*' "$S" > "$S.t" && mv "$S.t" "$S"
(cd "$PROJ" && bash "$REPO/scripts/install-bequite.sh" --from-local "$REPO" --force >/dev/null 2>&1)
grep -q '^\*\*Auto update:\*\* on' "$S" && ok "Auto update switch added to an old memory file" || bad "Auto update switch added"

echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
