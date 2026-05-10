#!/usr/bin/env bash
# skill/hooks/posttooluse-format.sh
#
# PostToolUse hook: auto-format the file just edited / written. Detects the
# language by extension. Non-blocking: if the formatter is missing or fails,
# emit a warning to stderr and exit 0 (warn-only).
#
# Wired in template/.claude/settings.json under PostToolUse for Edit + Write.

set -uo pipefail   # NOT -e: we want to continue on formatter failure with warning

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

# Detect language. Run the appropriate formatter. Suppress stdout; show errors.
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs)
    if command -v biome >/dev/null 2>&1; then
      biome format --write "$FILE_PATH" 2>&1 1>/dev/null || echo "[posttooluse-format] biome format warning on $FILE_PATH" >&2
    elif command -v prettier >/dev/null 2>&1; then
      prettier --write "$FILE_PATH" 2>&1 1>/dev/null || echo "[posttooluse-format] prettier warning on $FILE_PATH" >&2
    fi
    ;;
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      ruff format "$FILE_PATH" 2>&1 1>/dev/null || echo "[posttooluse-format] ruff format warning on $FILE_PATH" >&2
    elif command -v black >/dev/null 2>&1; then
      black --quiet "$FILE_PATH" || echo "[posttooluse-format] black warning on $FILE_PATH" >&2
    fi
    ;;
  *.rs)
    if command -v rustfmt >/dev/null 2>&1; then
      rustfmt "$FILE_PATH" 2>&1 1>/dev/null || echo "[posttooluse-format] rustfmt warning on $FILE_PATH" >&2
    fi
    ;;
  *.go)
    if command -v gofmt >/dev/null 2>&1; then
      gofmt -w "$FILE_PATH" || echo "[posttooluse-format] gofmt warning on $FILE_PATH" >&2
    fi
    ;;
  *.json)
    if command -v jq >/dev/null 2>&1; then
      tmp=$(mktemp)
      if jq . "$FILE_PATH" > "$tmp" 2>/dev/null; then mv "$tmp" "$FILE_PATH"; else rm -f "$tmp"; fi
    fi
    ;;
  *.md|*.mdx)
    if command -v prettier >/dev/null 2>&1; then
      prettier --write --parser markdown "$FILE_PATH" 2>&1 1>/dev/null || true
    fi
    ;;
  *.css|*.scss|*.html)
    if command -v prettier >/dev/null 2>&1; then
      prettier --write "$FILE_PATH" 2>&1 1>/dev/null || true
    fi
    ;;
esac

exit 0
