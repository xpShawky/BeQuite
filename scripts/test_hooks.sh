#!/usr/bin/env bash
# Behaviour test for the three plugin hooks. Offline; CI runs it.
#   bash scripts/test_hooks.sh
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
H="$REPO/.claude/hooks"
T="$(mktemp -d)"; trap 'rm -rf "${T:?}"' EXIT
mkdir -p "$T/proj/.bequite/state" "$T/empty"
pass=0; fail=0
ok()  { pass=$((pass + 1)); echo "  PASS  $1"; }
bad() { fail=$((fail + 1)); echo "  FAIL  $1 (${2:-})"; }
stop() {  # message -> exit code of the Stop hook
  printf '{"hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"%s"}' "$1" \
    | CLAUDE_PROJECT_DIR="$T/proj" bash "$H/stop-banned-weasel-words.sh" >/dev/null 2>&1; echo $?
}
expect() { got="$(stop "$2")"; [ "$got" = "$3" ] && ok "$1" || bad "$1" "exit $got, wanted $3"; }

echo "Stop hook"
expect "an explanation that uses the word finished passes"   "The function returns when the loop is finished, then the caller is done with the handle." 0
expect "a question about done passes"                         "Is the migration done? Not yet: two tables remain." 0
expect "a plain answer passes"                                "Use a Map here; it keeps insertion order." 0
expect "a claim with no evidence is blocked"                  "I fixed the login bug." 2
expect "a claim with evidence passes"                         "I fixed the login bug. npm test: 42/42 tests passed, exit code 0." 0
expect "a claim marked UNVERIFIED passes"                     "The fix is implemented. UNVERIFIED: no browser in this session." 0
expect "a weasel word in a claim is blocked"                  "It is done and should work now. exit code 0" 2
expect "a report line starting with Done is checked"          "Summary\\nDone: the parser handles tabs." 2
expect "an Arabic claim with no evidence is blocked"          "خلصت التعديل على الصفحة." 2
expect "an Arabic claim with evidence passes"                 "خلصت التعديل. الاختبارات: 12/12 tests passed, exit code 0" 0
got="$(printf '{"stop_hook_active":true,"last_assistant_message":"I fixed it."}' | CLAUDE_PROJECT_DIR="$T/proj" bash "$H/stop-banned-weasel-words.sh" >/dev/null 2>&1; echo $?)"
[ "$got" = 0 ] && ok "never blocks twice in a row (stop_hook_active)" || bad "stop_hook_active guard" "exit $got"
got="$(printf '{"last_assistant_message":"I fixed it."}' | CLAUDE_PROJECT_DIR="$T/empty" bash "$H/stop-banned-weasel-words.sh" >/dev/null 2>&1; echo $?)"
[ "$got" = 0 ] && ok "silent outside a BeQuite project" || bad "outside a BeQuite project" "exit $got"

echo "UserPromptSubmit hook"
taste() { printf '{"prompt":"%s"}' "$1" | CLAUDE_PROJECT_DIR="$T/proj" bash "$H/userprompt-taste-inbox.sh" >/dev/null 2>&1; }
rows() { grep -c '^| [0-9]' "$T/proj/.bequite/state/TASTE_INBOX.md" 2>/dev/null || true; }
taste "no, not like that: the heading is too heavy"; [ "$(rows)" = 1 ] && ok "a correction is logged" || bad "a correction is logged" "rows $(rows)"
taste "no problem, carry on";                        [ "$(rows)" = 1 ] && ok "a polite no is not logged" || bad "a polite no is not logged" "rows $(rows)"
taste "add a pricing page";                          [ "$(rows)" = 1 ] && ok "an ordinary request is not logged" || bad "an ordinary request is not logged" "rows $(rows)"
taste "مش كده، الخط تقيل";                           [ "$(rows)" = 2 ] && ok "an Arabic correction is logged" || bad "an Arabic correction is logged" "rows $(rows)"

echo "SessionStart hook"
out="$(echo '{"source":"startup"}' | CLAUDE_PROJECT_DIR="$T/proj" bash "$H/session-start.sh")"
case "$out" in *"BeQuite session context"*) ok "prints context in a BeQuite project" ;; *) bad "prints context in a BeQuite project" ;; esac
[ "${#out}" -le 9000 ] && ok "stays under the context cap" || bad "context cap" "${#out} chars"
out="$(echo '{}' | CLAUDE_PROJECT_DIR="$T/empty" bash "$H/session-start.sh")"
[ -z "$out" ] && ok "silent in a project without BeQuite (script install)" || bad "silent without BeQuite" "$out"
out="$(echo '{}' | CLAUDE_PROJECT_DIR="$T/empty" CLAUDE_PLUGIN_ROOT="$REPO" bash "$H/session-start.sh")"
case "$out" in *"bq-init"*"templates/bequite"*) ok "plugin install, no memory yet: one line pointing at bq-init" ;; *) bad "plugin fresh-project line" "$out" ;; esac

echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
