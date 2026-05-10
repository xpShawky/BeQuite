#!/usr/bin/env bash
# skill/hooks/stop-verify-before-done.sh
#
# Stop hook: runs when Claude is about to stop. Two checks:
# 1. Banned weasel words in completion message (Constitution v1.0.1 Article II).
# 2. (When in P5+ phase) outstanding test failures or incomplete tasks.
#
# Exit 0 = allow stop. Exit 2 = force continuation with reason on stderr.
#
# Wired in template/.claude/settings.json under Stop.

set -uo pipefail

INPUT=$(cat)
COMPLETION_TEXT=$(printf '%s' "$INPUT" | jq -r '.completion_text // .response // ""' 2>/dev/null || echo "")

# 1. Banned weasel words (Iron Law II — Verification before completion).
# These phrases imply a hedge that is incompatible with "verified done".
BANNED_PHRASES=(
  "should work"
  "should pass"
  "should be"
  "should now"
  "probably"
  "seems to"
  "seems like"
  "appears to"
  "appears that"
  "I think it works"
  "I think it should"
  "might work"
  "hopefully"
  "in theory"
  "in principle"
  "likely works"
)

# Lower-case both for case-insensitive match.
LOWER_TEXT=$(printf '%s' "$COMPLETION_TEXT" | tr '[:upper:]' '[:lower:]')

for phrase in "${BANNED_PHRASES[@]}"; do
  if printf '%s' "$LOWER_TEXT" | grep -qF "$phrase"; then
    cat >&2 <<EOF
[bequite hook: stop-verify-before-done] BLOCKED — banned weasel word in completion message.

Constitution v1.0.1 Article II (Verification before completion):
A task is "done" only after acceptance evidence has been executed in this
session and passed. The agent MUST NOT use:

  $(printf '  %s\n' "${BANNED_PHRASES[@]}")

Detected: "$phrase"

Restate the completion concretely:
- WHAT ran (commands; cite exit codes).
- WHAT passed (tests, gates).
- WHAT failed (with reproducer commands).
- WHAT was not run (and why).
- WHAT is uncertain (and what would resolve the uncertainty).

Then re-attempt the stop.
EOF
    exit 2
  fi
done

# 2. Outstanding state checks (best-effort; refuse to stop with known incomplete).
# Look for an in-flight task in state/task_index.json.
if [[ -f "state/task_index.json" ]]; then
  IN_PROGRESS=$(jq -r '.tasks[] | select(.status == "in_progress") | .id' state/task_index.json 2>/dev/null || echo "")
  if [[ -n "$IN_PROGRESS" ]]; then
    cat >&2 <<EOF
[bequite hook: stop-verify-before-done] BLOCKED — task still marked in_progress.

state/task_index.json shows the following task is in_progress:
$IN_PROGRESS

Per Iron Law III: at the end of every task, update state/recovery.md +
.bequite/memory/activeContext.md + state/task_index.json. The task must be
either:
  - completed (status set, evidence_path populated, completed_at set), or
  - explicitly paused with a documented reason in state/recovery.md.

Do not stop with stale "in_progress" state.
EOF
    exit 2
  fi
fi

# Allowed.
exit 0
