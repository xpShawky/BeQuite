#!/usr/bin/env bash
# BeQuite hook — Stop — block a completion claim that uses banned weasel words instead of evidence.
# OPT-IN and the MOST EXPERIMENTAL of the three (reads the transcript; fails soft on any uncertainty).
# Review before enabling. See docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md
#
# Protocol (verified vs docs): Stop hook gets {stop_hook_active, transcript_path, ...}.
#   exit 2 = block the turn from ending (forces Claude to keep working); stderr -> Claude.
#   MUST exit 0 when stop_hook_active is true, or you get an infinite loop.
#   Claude Code force-overrides after 8 consecutive blocks regardless.
set -uo pipefail
INPUT="$(cat)"

if ! command -v jq >/dev/null 2>&1; then exit 0; fi   # fail soft without jq
ACTIVE="$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null || echo false)"
[ "$ACTIVE" = "true" ] && exit 0                       # already blocked this cycle -> allow (no infinite loop)
TRANSCRIPT="$(printf '%s' "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null || true)"
[ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ] && exit 0   # can't read transcript -> fail soft

# Last assistant text turn (transcript is JSONL).
LAST="$(jq -rs 'map(select(.type=="assistant")) | last | (.message.content // [])[] | select(.type=="text") | .text' "$TRANSCRIPT" 2>/dev/null || true)"
[ -z "$LAST" ] && exit 0

if printf '%s' "$LAST" | grep -Eiq '\b(should (work|be fixed|pass|be fine)|probably (works|correct|fixed|fine)|seems to (work|be fixed)|appears to (work|be fixed)|i think it works|i believe it works|might (work|fix(es)? (it|the))|hopefully (fixed|works|that)|in (theory|principle))\b'; then
  echo "BeQuite Stop hook: this response makes a completion claim with a banned weasel word." >&2
  echo "Replace it with concrete evidence (the command run + exit code + output), or state an explicit 'UNVERIFIED:' / 'I don't know' — then finish." >&2
  exit 2
fi
exit 0
