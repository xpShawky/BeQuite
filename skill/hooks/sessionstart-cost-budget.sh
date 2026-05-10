#!/usr/bin/env bash
# skill/hooks/sessionstart-cost-budget.sh
#
# SessionStart hook: load the cost ceiling + wall-clock ceiling from
# state/project.yaml::safety_rails into stderr so the token-economist
# persona can enforce.
#
# Non-blocking. Exit 0 always.

set -uo pipefail

if [[ -f "state/project.yaml" ]]; then
  COST_USD=$(grep -E '^[[:space:]]*cost_ceiling_usd[[:space:]]*=' state/project.yaml | head -1 | sed 's/.*=[[:space:]]*//' | tr -d '\r' || echo "20")
  WALL_HOURS=$(grep -E '^[[:space:]]*wall_clock_ceiling_hours[[:space:]]*=' state/project.yaml | head -1 | sed 's/.*=[[:space:]]*//' | tr -d '\r' || echo "6")
  FAIL_THRESH=$(grep -E '^[[:space:]]*consecutive_failure_threshold[[:space:]]*=' state/project.yaml | head -1 | sed 's/.*=[[:space:]]*//' | tr -d '\r' || echo "3")
else
  COST_USD="20"
  WALL_HOURS="6"
  FAIL_THRESH="3"
fi

cat >&2 <<EOF
[bequite hook: sessionstart-cost-budget] Active safety rails for this session:

Cost ceiling:        \$${COST_USD} USD
Wall-clock ceiling:  ${WALL_HOURS} hours
Failure threshold:   ${FAIL_THRESH} consecutive failures on a single task

When 80% of either ceiling is reached, the token-economist persona writes
a soft warning to state/recovery.md::heartbeat. At 100%, the Stop hook
fires and pauses for explicit human approval to continue.

To override (per session): export BEQUITE_COST_CEILING_USD=<value>
                           export BEQUITE_WALL_CLOCK_HOURS=<value>

Override rationale must be recorded in the session's receipt or in
.bequite/memory/decisions/ as an ADR amendment.
EOF

exit 0
