#!/usr/bin/env bash
# skill/hooks/posttooluse-lint.sh
#
# PostToolUse hook: run linter on the file just edited/written. Warn-only;
# never blocks (lint blocking belongs in CI / `bequite verify`, not here).
#
# Output: collected to stderr so Claude can read and respond.

set -uo pipefail

INPUT=$(cat)
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // ""')

case "$TOOL_NAME" in
  Edit|Write) ;;
  *) exit 0 ;;
esac

FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // ""')

if [[ -z "$FILE_PATH" || ! -f "$FILE_PATH" ]]; then
  exit 0
fi

LINT_OUTPUT=""

case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs)
    if command -v biome >/dev/null 2>&1; then
      LINT_OUTPUT=$(biome lint "$FILE_PATH" 2>&1 || true)
    elif command -v eslint >/dev/null 2>&1; then
      LINT_OUTPUT=$(eslint "$FILE_PATH" 2>&1 || true)
    fi
    ;;
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      LINT_OUTPUT=$(ruff check "$FILE_PATH" 2>&1 || true)
    fi
    ;;
  *.rs)
    if command -v cargo >/dev/null 2>&1 && [[ -f "Cargo.toml" ]]; then
      LINT_OUTPUT=$(cargo clippy --no-deps --quiet 2>&1 || true)
    fi
    ;;
  *.go)
    if command -v go >/dev/null 2>&1; then
      LINT_OUTPUT=$(go vet "./..." 2>&1 || true)
    fi
    ;;
esac

# Surface lint output if any.
if [[ -n "$LINT_OUTPUT" ]]; then
  echo "[bequite hook: posttooluse-lint] WARN — lint findings on $FILE_PATH:" >&2
  echo "$LINT_OUTPUT" >&2
fi

exit 0   # never block; this is advisory.
