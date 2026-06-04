#!/usr/bin/env bash
# BeQuite hook — PreToolUse (matcher: Write|Edit) — block secret-shaped strings before they hit disk.
# OPT-IN. Review before enabling. See docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md
#
# Protocol: stdin JSON; exit 2 blocks (stderr -> Claude); exit 0 allows.
# Only HIGH-CONFIDENCE patterns block (near-zero false positives). The generic
# KEY=<long-value> pattern is intentionally left commented out to avoid blocking
# legitimate base64 test fixtures — enable it per project if you accept the trade-off.
set -uo pipefail
INPUT="$(cat)"

if command -v jq >/dev/null 2>&1; then
  CONTENT="$(printf '%s' "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // empty' 2>/dev/null || true)"
  FILE="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // "the edit"' 2>/dev/null || echo "the edit")"
  HAY="${CONTENT:-$INPUT}"
else
  HAY="$INPUT"; FILE="the edit"
fi

block() {
  echo "BeQuite hook blocked a secret-shaped string in ${FILE}: $1" >&2
  echo "Move it to .env / an OS keychain / a secret manager, gitignore the file, and use a placeholder in code." >&2
  exit 2
}

printf '%s' "$HAY" | grep -Eq 'AKIA[0-9A-Z]{16}'                         && block "AWS access key id"
printf '%s' "$HAY" | grep -Eq 'gh[pousr]_[A-Za-z0-9_]{36,}'             && block "GitHub token"
printf '%s' "$HAY" | grep -Eq 'sk-ant-[A-Za-z0-9_-]{20,}'              && block "Anthropic API key"
printf '%s' "$HAY" | grep -Eq 'sk-[A-Za-z0-9]{32,}'                    && block "OpenAI-style API key"
printf '%s' "$HAY" | grep -Eq -- '-----BEGIN [A-Z ]*PRIVATE KEY-----'  && block "private key block"
printf '%s' "$HAY" | grep -Eq 'xox[baprs]-[A-Za-z0-9-]{10,}'           && block "Slack token"

# OPTIONAL (false-positive prone — enable per project):
# printf '%s' "$HAY" | grep -Eiq '(api|secret|password|token)[a-z_]*[[:space:]]*[:=][[:space:]]*.{0,2}[A-Za-z0-9+/_-]{20,}' && block "hardcoded credential assignment"

exit 0
