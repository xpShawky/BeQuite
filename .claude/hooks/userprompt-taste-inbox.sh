#!/usr/bin/env bash
# BeQuite hook - UserPromptSubmit - log the user's corrections to .bequite/state/TASTE_INBOX.md for /bq-taste.
# A correction is a prompt that starts with no / not like that / wrong / don't / لا / لأ / مش كده / غلط.
# Never blocks and adds no context: it only appends one row. Fails soft on anything unexpected.
# Plugin installs run it from ${CLAUDE_PLUGIN_ROOT}; script installs enable it through /bq-hooks.
set -u
INPUT=""; [ -t 0 ] || INPUT="$(cat 2>/dev/null || true)"   # run by hand in a terminal: no input
PROJECT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
[ -d "$PROJECT/.bequite/state" ] || exit 0

RAW="$(printf '%s' "$INPUT" | grep -oE '"prompt"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"' | head -n 1)"
[ -z "$RAW" ] && exit 0
TEXT="$(printf '%s' "$RAW" | sed -e 's/^"prompt"[[:space:]]*:[[:space:]]*"//' -e 's/"$//' -e 's/\\n/ /g' -e 's/\\t/ /g' -e 's/\\"/"/g' -e 's/\\\\/\\/g' | tr -s ' ' | sed 's/^ *//')"

printf '%s' "$TEXT" | grep -Eiq '^(no\b|nope\b|not like (this|that)|that.?s (wrong|not (it|right))|wrong\b|don.?t\b|لا[ ،,.]|لا$|لأ|مش كده|مش كدا|غلط)' || exit 0
# polite "no" that is not a correction
printf '%s' "$TEXT" | grep -Eiq '^(no (problem|worries|need)|لا مشكلة|لا بأس|لا شكرا)' && exit 0

INBOX="$PROJECT/.bequite/state/TASTE_INBOX.md"
if [ ! -f "$INBOX" ]; then
  {
    echo "# Taste inbox"
    echo
    echo "Corrections waiting for \`/bq-taste review\` (appended by the UserPromptSubmit hook)."
    echo
    echo "| # | Date | Work | The user's words | What it corrected | Status |"
    echo "|---|---|---|---|---|---|"
  } > "$INBOX"
fi
N="$(grep -c '^| [0-9]' "$INBOX" 2>/dev/null)"   # grep -c prints 0 on no match (and exits 1): no "|| echo 0"
case "$N" in ''|*[!0-9]*) N=0 ;; esac
N=$(( N + 1 ))
WORK="$(sed -n 's/^\*\*Id:\*\* *//p' "$PROJECT/.bequite/ACTIVE.md" 2>/dev/null | head -n 1 | tr -d '\r')"
SHORT="$(printf '%s' "$TEXT" | tr '|' '/' | cut -c1-300)"
printf '| %s | %s | %s | %s | (fill at review) | new |\n' "$N" "$(date +%Y-%m-%d)" "${WORK:-none}" "$SHORT" >> "$INBOX"
exit 0
