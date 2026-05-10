#!/usr/bin/env bash
# skill/hooks/pretooluse-secret-scan.sh
#
# PreToolUse hook: blocks Edit/Write/Bash that contains secret-shaped strings.
# Iron Law IV (Constitution v1.0.1) — never write secrets to disk.
#
# Wired in template/.claude/settings.json under PreToolUse for Edit + Write.
# Reads tool call JSON from stdin (Claude Code hook protocol).
# Exit 0 = allow. Exit 2 = block (with reason on stderr).

set -euo pipefail

# Read the tool-call JSON from stdin.
INPUT=$(cat)

# Extract tool name and args. jq is required (`brew install jq` / `apt install jq`).
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // ""')
TOOL_INPUT=$(printf '%s' "$INPUT" | jq -r '.tool_input // {}')

# Patterns that indicate a likely secret. Expand carefully (false-positive cost
# is low; false-negative cost is a leaked secret).
SECRET_PATTERNS=(
  # AWS access key (AKIA…)
  '(^|[^A-Z0-9])AKIA[0-9A-Z]{16}([^A-Z0-9]|$)'
  # AWS secret key (40 chars base64-ish, often quoted)
  '"[A-Za-z0-9/+=]{40}"'
  # Generic API keys (sk_live_, pk_live_, sk-, ghp_, gho_, ghu_, ghs_, ghr_)
  '\b(sk|pk)_(live|test)_[A-Za-z0-9]{24,}\b'
  '\bsk-[A-Za-z0-9]{32,}\b'
  '\bgh[posru]_[A-Za-z0-9]{36,}\b'
  # Anthropic API key (sk-ant-)
  '\bsk-ant-[A-Za-z0-9_-]{50,}\b'
  # OpenAI key (sk-proj-)
  '\bsk-proj-[A-Za-z0-9_-]{40,}\b'
  # Google API key (AIza…)
  '\bAIza[0-9A-Za-z_-]{35}\b'
  # JWT (header.payload.signature; eyJ… is common base64 prefix)
  '\beyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b'
  # Slack tokens
  '\bxox[bopsa]-[0-9]+-[0-9]+-[A-Za-z0-9]+\b'
  # Stripe restricted keys
  '\brk_(live|test)_[A-Za-z0-9]{24,}\b'
  # Generic high-entropy tokens of common shape (40+ chars)
  '"(api[_-]?key|access[_-]?token|secret[_-]?key|auth[_-]?token)"\s*[:=]\s*"[A-Za-z0-9_/+=-]{20,}"'
  # Private SSH keys
  '-----BEGIN (RSA|OPENSSH|DSA|EC|PGP) PRIVATE KEY-----'
)

# Concatenate args fields where secrets could plausibly appear.
SCAN_TARGET=""
case "$TOOL_NAME" in
  Edit)
    SCAN_TARGET=$(printf '%s' "$TOOL_INPUT" | jq -r '.new_string // ""')
    ;;
  Write)
    SCAN_TARGET=$(printf '%s' "$TOOL_INPUT" | jq -r '.content // ""')
    ;;
  Bash)
    SCAN_TARGET=$(printf '%s' "$TOOL_INPUT" | jq -r '.command // ""')
    ;;
  *)
    # Other tools — let through.
    exit 0
    ;;
esac

# Scan.
for pattern in "${SECRET_PATTERNS[@]}"; do
  if printf '%s' "$SCAN_TARGET" | grep -qE "$pattern"; then
    cat >&2 <<EOF
[bequite hook: pretooluse-secret-scan] BLOCKED — secret-shaped string detected.

Iron Law IV (Constitution v1.0.1): never write secrets to disk; never commit
keys, tokens, JWTs, or AWS access patterns.

Tool: $TOOL_NAME
Pattern matched: $pattern

To proceed safely:
- Use environment variables (\$ENV_VAR) and reference them in code.
- Use the platform's secret manager (Doppler / Vault / AWS Secrets Manager / 1Password Connect).
- Never paste a real key. Use a placeholder like "REPLACE_ME_WITH_ENV_VAR".

If this is a false positive (the string genuinely is not a secret), document
why in an ADR at .bequite/memory/decisions/ and override locally.
This hook does not auto-override.
EOF
    exit 2
  fi
done

# Allowed.
exit 0
