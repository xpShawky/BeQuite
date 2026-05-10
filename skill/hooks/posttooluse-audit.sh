#!/usr/bin/env bash
# skill/hooks/posttooluse-audit.sh
#
# PostToolUse hook: run a lightweight subset of `bequite audit` rules on the
# just-edited file. Surface findings to stderr; warn-only (the full audit
# runs in CI + on demand via `bequite audit`).
#
# Wired in v0.4.2+ once the audit rules engine ships.

set -uo pipefail

INPUT=$(cat)
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // ""')

case "$TOOL_NAME" in
  Edit|Write) ;;
  *) exit 0 ;;
esac

FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // ""')

# Light checks. The full audit lives at cli/bequite/audit.py (v0.4.2).

# 1. Doctrine `default-web-saas` Rule 2: hardcoded `font-family: Inter` outside tokens.
case "$FILE_PATH" in
  *.css|*.scss|*.tsx|*.jsx|*.vue|*.svelte)
    if [[ "$FILE_PATH" != *"tokens"* ]] && [[ "$FILE_PATH" != *"theme"* ]]; then
      if grep -qE "font-family[[:space:]]*:[[:space:]]*['\"]?Inter" "$FILE_PATH" 2>/dev/null; then
        echo "[bequite hook: posttooluse-audit] WARN — hardcoded 'font-family: Inter' outside tokens.css ($FILE_PATH). Doctrine default-web-saas Rule 2: recorded design choice required." >&2
      fi
    fi
    ;;
esac

# 2. Iron Law IV: code reading `.env*` files.
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs|*.py|*.rs|*.go)
    if grep -qE "(read.*\.env|open\([^)]*\.env|fs\.read.*\.env)" "$FILE_PATH" 2>/dev/null; then
      echo "[bequite hook: posttooluse-audit] WARN — code reads .env file in $FILE_PATH. Iron Law IV: never read .env directly; use the framework's env loader." >&2
    fi
    ;;
esac

# 3. Doctrine `library-package` Rule 7: telemetry endpoints not behind config gate.
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs)
    if grep -qE "fetch\([^)]*['\"]https?://[^)]*(telemetry|analytics|track|metrics)" "$FILE_PATH" 2>/dev/null; then
      echo "[bequite hook: posttooluse-audit] WARN — telemetry-shaped fetch in $FILE_PATH. Doctrine library-package Rule 7: telemetry must be opt-in only." >&2
    fi
    ;;
esac

exit 0
