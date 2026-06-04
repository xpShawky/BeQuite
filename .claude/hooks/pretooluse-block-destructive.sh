#!/usr/bin/env bash
# BeQuite hook — PreToolUse — block destructive operations.
# OPT-IN. Review this script before enabling it. See docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md
#
# Protocol (verified vs code.claude.com/docs/en/hooks):
#   stdin  = JSON {tool_name, tool_input:{command|file_path|...}, ...}
#   exit 0 = allow the tool call
#   exit 2 = BLOCK the tool call; stderr is fed back to Claude as the reason
#   (exit 1 does NOT block — only exit 2)
# A PreToolUse block fires before any permission-mode check (even bypassPermissions),
# so this can tighten safety but can never loosen it.
set -uo pipefail
INPUT="$(cat)"

# Prefer the command/path field; fall back to the whole payload (safe over-match for a blocker).
if command -v jq >/dev/null 2>&1; then
  FIELD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // .tool_input.file_path // empty' 2>/dev/null || true)"
  HAY="${FIELD:-$INPUT}"
else
  HAY="$INPUT"
fi

block() {
  echo "BeQuite hook blocked a destructive operation: $1" >&2
  echo "This is a hard human gate (per /bq-auto). Re-run only with explicit user confirmation, or choose a safer alternative." >&2
  exit 2
}

# rm -rf / rm -fr / rm -r ... -f  (allow only clearly inside /tmp or node_modules)
if printf '%s' "$HAY" | grep -Eiq 'rm[[:space:]]+-[a-z]*r[a-z]*f|rm[[:space:]]+-[a-z]*f[a-z]*r|rm[[:space:]]+-r[a-z]*[[:space:]]+-f|rm[[:space:]]+--recursive.*--force'; then
  printf '%s' "$HAY" | grep -Eq '/tmp/|node_modules' || block "recursive force-delete (rm -rf) on tracked files"
fi
# protect BeQuite / Claude project memory specifically
printf '%s' "$HAY" | grep -Eiq 'rm[[:space:]]+-[a-z]*[rf].*\.(bequite|claude)\b' && block "deletion of .bequite/ or .claude/ (project memory)"
# force-push to a protected branch
if printf '%s' "$HAY" | grep -Eiq 'git[[:space:]]+push[[:space:]].*(--force([[:space:]]|=)|--force$|-f([[:space:]]|$))'; then
  printf '%s' "$HAY" | grep -Eiq '\b(main|master|prod|production|release)\b' && block "git push --force to a protected branch"
fi
printf '%s' "$HAY" | grep -Eiq 'git[[:space:]]+reset[[:space:]]+--hard' && block "git reset --hard (discards work)"
printf '%s' "$HAY" | grep -Eiq 'terraform[[:space:]]+destroy' && block "terraform destroy"
printf '%s' "$HAY" | grep -Eiq 'DROP[[:space:]]+(TABLE|DATABASE|SCHEMA)\b' && block "SQL DROP TABLE/DATABASE/SCHEMA"

exit 0
