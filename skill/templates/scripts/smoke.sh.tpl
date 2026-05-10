#!/usr/bin/env bash
# template/scripts/smoke.sh — curl every public endpoint declared in the
# project's openapi.yaml or routes.json. Asserts each returns the expected
# 200 / 401 / 403 per the spec. Article II / II — verification before
# completion.
#
# Used by `bequite verify` (Phase 6) as the API-level smoke pass alongside
# Playwright walks.
#
# Output: evidence/P6/smoke-<timestamp>.log

set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:3000}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H-%M-%SZ")
LOG_DIR="evidence/P6"
LOG="$LOG_DIR/smoke-${TIMESTAMP}.log"

mkdir -p "$LOG_DIR"

echo "[smoke] base_url=$BASE_URL timestamp=$TIMESTAMP" | tee "$LOG"

# Per-endpoint expected status (configurable in tests/smoke-routes.json):
# {
#   "/api/health":       { "method": "GET",  "expect": 200, "auth": false },
#   "/api/users/me":     { "method": "GET",  "expect": 401, "auth": false },
#   "/api/admin/users":  { "method": "GET",  "expect": 401, "auth": false },
#   "/api/sign-in":      { "method": "POST", "expect": 400, "auth": false, "body": {} }
# }

ROUTES_FILE="${SMOKE_ROUTES_FILE:-tests/smoke-routes.json}"

if [[ ! -f "$ROUTES_FILE" ]]; then
  echo "[smoke] WARN — no smoke-routes.json at $ROUTES_FILE; using common defaults" | tee -a "$LOG"
  cat <<EOF > /tmp/smoke-routes-default.json
{
  "/api/health":   { "method": "GET", "expect": 200, "auth": false }
}
EOF
  ROUTES_FILE=/tmp/smoke-routes-default.json
fi

ANY_FAILED=0
ENDPOINTS=$(jq -r 'to_entries[] | "\(.key)|\(.value.method)|\(.value.expect)|\(.value.auth // false)"' "$ROUTES_FILE")

while IFS='|' read -r path method expected auth; do
  [[ -z "$path" ]] && continue

  if [[ "$auth" == "true" ]]; then
    if [[ -z "${SMOKE_AUTH_TOKEN:-}" ]]; then
      echo "[smoke]   SKIP $method $path (auth required but SMOKE_AUTH_TOKEN unset)" | tee -a "$LOG"
      continue
    fi
    AUTH_HEADER=(-H "Authorization: Bearer $SMOKE_AUTH_TOKEN")
  else
    AUTH_HEADER=()
  fi

  STATUS=$(curl -s -o /dev/null -w '%{http_code}' \
    -X "$method" \
    "${AUTH_HEADER[@]}" \
    "$BASE_URL$path" \
    || echo '000')

  if [[ "$STATUS" == "$expected" ]]; then
    echo "[smoke]   $method $path → $STATUS  (expected $expected)  ✓" | tee -a "$LOG"
  else
    ANY_FAILED=1
    echo "[smoke]   $method $path → $STATUS  (expected $expected)  ✗" | tee -a "$LOG"
  fi
done <<< "$ENDPOINTS"

if (( ANY_FAILED == 0 )); then
  echo "[smoke] PASS" | tee -a "$LOG"
  exit 0
else
  echo "[smoke] FAIL — at least one endpoint returned the wrong status" | tee -a "$LOG"
  exit 1
fi
