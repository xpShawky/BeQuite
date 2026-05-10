#!/usr/bin/env bash
# skill/hooks/pretooluse-block-destructive.sh
#
# PreToolUse hook: blocks Bash commands that match destructive patterns
# without an explicit ADR-approved override (Tier-3 per Constitution v1.0.1).
#
# Wired in template/.claude/settings.json under PreToolUse for Bash.
# Reads tool call JSON from stdin.
# Exit 0 = allow. Exit 2 = block.

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // ""')

# Only inspect Bash calls.
if [[ "$TOOL_NAME" != "Bash" ]]; then
  exit 0
fi

CMD=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // ""')

# Tier-3 dangerous patterns — never auto-allow.
# Based on master §19.4 + Constitution Article IV v1.0.1.
DESTRUCTIVE_PATTERNS=(
  # Filesystem
  'rm[[:space:]]+-rf?[[:space:]]+/(?!tmp|var/tmp)'         # rm -rf outside /tmp
  'rm[[:space:]]+-rf?[[:space:]]+~'                       # rm -rf ~
  'rm[[:space:]]+-rf?[[:space:]]+\$HOME'                  # rm -rf $HOME
  'rm[[:space:]]+-rf?[[:space:]]+\.\$'                    # rm -rf .
  'rm[[:space:]]+-rf?[[:space:]]+\*'                      # rm -rf *
  # Git destructive
  'git[[:space:]]+push[[:space:]]+(--force|-f)([[:space:]]|$)'
  'git[[:space:]]+push[[:space:]]+.*[[:space:]]+(--force|-f)([[:space:]]|$)'
  'git[[:space:]]+reset[[:space:]]+--hard'
  'git[[:space:]]+clean[[:space:]]+-[a-z]*[fFdx]'
  'git[[:space:]]+branch[[:space:]]+-D[[:space:]]+(main|master|production|prod)'
  'git[[:space:]]+filter-branch'
  'git[[:space:]]+update-ref[[:space:]]+-d'
  # Database
  'DROP[[:space:]]+(DATABASE|SCHEMA|TABLE)'
  'TRUNCATE[[:space:]]+TABLE'
  'DELETE[[:space:]]+FROM[[:space:]]+[a-zA-Z_]+([[:space:]]*;|[[:space:]]*$)'  # DELETE without WHERE
  # Infrastructure
  'terraform[[:space:]]+(destroy|apply.*-auto-approve)'
  'pulumi[[:space:]]+destroy'
  'kubectl[[:space:]]+delete[[:space:]]+(namespace|ns|node|cluster)'
  'docker[[:space:]]+system[[:space:]]+prune[[:space:]]+--all.*--force'
  'docker[[:space:]]+rm[[:space:]]+-f[[:space:]]+\$\(docker[[:space:]]+ps'
  # Permissions
  'chmod[[:space:]]+777'
  'chown[[:space:]]+root'
  # Disable security
  'iptables[[:space:]]+-F'
  'ufw[[:space:]]+disable'
  # System destruction
  ':\(\)\{[[:space:]]*:\|:[[:space:]]*&[[:space:]]*\};:'   # fork bomb
  'mkfs\.'
  'dd[[:space:]]+.*of=/dev/sd'
)

for pattern in "${DESTRUCTIVE_PATTERNS[@]}"; do
  if printf '%s' "$CMD" | grep -qE "$pattern"; then
    cat >&2 <<EOF
[bequite hook: pretooluse-block-destructive] BLOCKED — destructive command detected.

Constitution v1.0.1 Article IV + master §19.4 Tier-3 classification:
"Dangerous commands must never run automatically."

Pattern matched: $pattern
Command: $CMD

Tier-3 commands require:
- An explicit ADR at .bequite/memory/decisions/ authorising this operation
  for this project, OR
- Explicit per-invocation human approval recorded in the receipt.

To proceed:
- For one-off operations: have a human run the command directly outside
  the agent loop, then resume the session.
- For recurring needs: write an ADR amendment + receipt and re-invoke.

Auto-mode never auto-overrides this hook (Constitution v1.0.1 Article IV).
EOF
    exit 2
  fi
done

# Allowed.
exit 0
