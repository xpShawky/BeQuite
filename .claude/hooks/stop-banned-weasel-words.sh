#!/usr/bin/env bash
# BeQuite hook - Stop - refuse a completion claim that has no evidence, or that uses a banned weasel word.
# Reads the last assistant message from the hook input (no jq, no transcript parsing needed).
# exit 2 blocks the stop; stderr tells Claude what to fix. Fails soft: any doubt -> exit 0.
# Loop guard: exits 0 when stop_hook_active is true (Claude Code also overrides after 8 blocks in a row).
# Plugin installs run it from ${CLAUDE_PLUGIN_ROOT}; script installs enable it through /bq-hooks.
set -u
INPUT=""; [ -t 0 ] || INPUT="$(cat 2>/dev/null || true)"   # run by hand in a terminal: no input, exit quietly
[ -z "$INPUT" ] && exit 0
printf '%s' "$INPUT" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true' && exit 0
PROJECT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
[ -d "$PROJECT/.bequite" ] || exit 0

# the last assistant message as a JSON string (escapes kept; enough for word matching)
MSG="$(printf '%s' "$INPUT" | grep -oE '"last_assistant_message"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -n 1)"
[ -z "$MSG" ] && exit 0

# Only completion claims are checked: a sentence that says the work is finished, not any use of the word
# "done" (an explanation such as "it returns when the loop is finished" must pass).
CLAIM_EN='\b((all|it is|it.?s|this is|that is|that.?s|everything is|work is|task is|tasks? are|now) (done|complete|completed|finished|fixed)|(i|we)( have|.?ve)? (just |now )?(fixed|implemented|completed|finished|resolved|shipped)|(is|are|has been|have been|was|were) (now )?(fixed|implemented|resolved|shipped)|all (tests|checks) pass(ed)?|ready to (ship|merge|release))\b'
CLAIM_LINE='(\\n|: ?")[^a-z\\]{0,4}(done|fixed|completed|finished|implemented)\b'
CLAIM_AR='(خلصت|خلصنا|تم الانتهاء|تم التنفيذ|تم الإصلاح|اتصلح)'
printf '%s' "$MSG" | grep -Eiq "$CLAIM_EN|$CLAIM_LINE|$CLAIM_AR" || exit 0

if printf '%s' "$MSG" | grep -Eiq '\b(should (work|be fixed|pass|be fine)|probably (works|correct|fixed|fine)|seems to (work|be fixed)|appears to (work|be fixed)|i think it works|i believe it works|might (work|fix)|hopefully|in (theory|principle))\b'; then
  echo "BeQuite Stop hook: this reply claims the work is done but uses a banned weasel word." >&2
  echo "Replace it with the evidence (the command, its exit code and the decisive output) or write UNVERIFIED: with the reason, then finish." >&2
  exit 2
fi

if ! printf '%s' "$MSG" | grep -Eiq '(exit( code)? ?[0-9]|exit [0-9]|UNVERIFIED|evidence\.md|[0-9]+ ?/ ?[0-9]+ (checks|tests)|checks passed|tests? passed|PASS\b|FAIL\b|bq_check|\bok\b.*[0-9])'; then
  echo "BeQuite Stop hook: this reply claims the work is done without evidence." >&2
  echo "Add the evidence (command + exit code + decisive output, also written to work/<id>/evidence.md) or say UNVERIFIED: and why, then finish." >&2
  exit 2
fi
exit 0
