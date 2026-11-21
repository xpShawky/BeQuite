#!/usr/bin/env bash
# BeQuite hook - Stop - refuse a completion claim that has no evidence, or that uses a banned weasel word.
# Reads the last assistant message from the hook input (no jq, no transcript parsing needed).
# exit 2 blocks the stop; stderr tells Claude what to fix. Fails soft: any doubt -> exit 0.
# Loop guard: exits 0 when stop_hook_active is true (Claude Code also overrides after 8 blocks in a row).
# Plugin installs run it from ${CLAUDE_PLUGIN_ROOT}; script installs enable it through /bq-hooks.
set -u
INPUT="$(cat 2>/dev/null || true)"
[ -z "$INPUT" ] && exit 0
printf '%s' "$INPUT" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true' && exit 0
PROJECT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
[ -d "$PROJECT/.bequite" ] || exit 0

# the last assistant message as a JSON string (escapes kept; enough for word matching)
MSG="$(printf '%s' "$INPUT" | grep -oE '"last_assistant_message"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -n 1)"
[ -z "$MSG" ] && exit 0

# only completion claims are checked
printf '%s' "$MSG" | grep -Eiq '(\b(done|completed?|finished|fixed|implemented|shipped|all (tests|checks) pass(ed)?|ready to (ship|merge|release))\b|خلصت|تم الانتهاء|اتعمل|جاهز)' || exit 0

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
