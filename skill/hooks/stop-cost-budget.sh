#!/usr/bin/env bash
# skill/hooks/stop-cost-budget.sh
#
# Stop hook: enforce the cost ceiling. Reads accumulated session cost from
# .bequite/cache/cost-ledger.json (token-economist writes; v0.7.0+).
# If 80% of ceiling reached, warn. If 100% reached, block stop until human
# approval logged to .bequite/cache/cost-override.json.
#
# Non-blocking until v0.7.0 ships the receipt system; before that, this hook
# exits 0 without inspection.

set -uo pipefail

LEDGER="${BEQUITE_COST_LEDGER:-.bequite/cache/cost-ledger.json}"

if [[ ! -f "$LEDGER" ]]; then
  exit 0   # No ledger yet; receipts not shipped. No-op.
fi

# Load ceiling from project.yaml (default $20).
COST_USD=$(grep -E '^[[:space:]]*cost_ceiling_usd[[:space:]]*=' state/project.yaml 2>/dev/null | head -1 | sed 's/.*=[[:space:]]*//' | tr -d '\r' || echo "20")

# Load current session cost.
SESSION_USD=$(jq -r '.session_total_usd // 0' "$LEDGER" 2>/dev/null || echo "0")

# Compare (bash float comparison via awk).
PCT=$(awk -v s="$SESSION_USD" -v c="$COST_USD" 'BEGIN{ if (c==0) print 0; else printf "%.0f", (s/c)*100 }')

OVERRIDE_FILE=".bequite/cache/cost-override.json"

if (( PCT >= 100 )); then
  if [[ -f "$OVERRIDE_FILE" ]]; then
    echo "[bequite hook: stop-cost-budget] WARN — 100% cost ceiling reached, but human override is active at $OVERRIDE_FILE. Allowing stop." >&2
    exit 0
  fi
  cat >&2 <<EOF
[bequite hook: stop-cost-budget] BLOCKED — session cost ceiling reached.

Session total:    \$${SESSION_USD} USD
Configured limit: \$${COST_USD} USD  (state/project.yaml::safety_rails.cost_ceiling_usd)

To proceed:
1. Review the work done so far. Was it worth the spend?
2. Decide: bump the ceiling (record in ADR) OR stop and resume next session.
3. If continuing: write {"approved_by":"<owner>","new_ceiling_usd":<n>,"reason":"<why>","approved_at":"<iso>"} to $OVERRIDE_FILE
4. Re-attempt the stop.

Auto-mode never auto-overrides this (Constitution v1.0.1 Article IV +
state/project.yaml::safety_rails.pause_on includes cost_ceiling_reached).
EOF
  exit 2
elif (( PCT >= 80 )); then
  echo "[bequite hook: stop-cost-budget] WARN — \${SESSION_USD}/${COST_USD} USD (${PCT}%) of cost ceiling consumed." >&2
fi

exit 0
