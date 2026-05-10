#!/usr/bin/env bash
# Bring the BeQuite Studio stack up via Docker Compose (macOS / Linux).
#
# Usage:
#   ./scripts/docker-up.sh                # build + up (foreground)
#   ./scripts/docker-up.sh --detach       # build + up in background
#   ./scripts/docker-up.sh --down         # stop + remove containers
#   ./scripts/docker-up.sh --no-build     # skip rebuild

set -uo pipefail

DETACH=false
DOWN=false
NO_BUILD=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --detach|-d)   DETACH=true; shift ;;
    --down)        DOWN=true; shift ;;
    --no-build)    NO_BUILD=true; shift ;;
    -h|--help)
      head -n 9 "$0" | tail -n 8
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

yellow() { printf '\033[33m%s\033[0m' "$*"; }
green()  { printf '\033[32m%s\033[0m' "$*"; }
red()    { printf '\033[31m%s\033[0m' "$*"; }
cyan()   { printf '\033[36m%s\033[0m' "$*"; }
section() { echo; echo "$(yellow "==> $1")"; }

# --- Prereq ---

section "Checking Docker"

if ! command -v docker >/dev/null 2>&1; then
  echo
  echo "$(red "Docker is not installed.")"
  echo "  Install:  $(cyan "https://www.docker.com/products/docker-desktop/")"
  echo
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo
  echo "$(red "Docker daemon is not running.")"
  echo "  Start Docker Desktop, then re-run this script."
  echo "  (Linux: sudo systemctl start docker)"
  echo
  exit 1
fi

echo "  Docker daemon: OK"

# --- Down path ---

if $DOWN; then
  section "Stopping BeQuite Studio stack"
  docker compose down
  echo
  echo "  $(green "Containers removed. Images preserved.")"
  echo "  Run 'docker image prune' to free disk."
  exit 0
fi

# --- Port check ---

section "Checking ports 3000 / 3001 / 3002"
for port in 3000 3001 3002; do
  if lsof -i ":$port" >/dev/null 2>&1 || ss -tln 2>/dev/null | grep -q ":$port "; then
    echo "  $(yellow "Port $port") is already in use."
    echo "    Stop any local dev servers first."
  else
    echo "  Port $port: free"
  fi
done

# --- Up ---

section "Bringing the stack up"

ARGS=("compose" "up")
if ! $NO_BUILD; then ARGS+=("--build"); fi
if   $DETACH;     then ARGS+=("-d"); fi

echo "  Running: $(cyan "docker ${ARGS[*]}")"
echo

docker "${ARGS[@]}"
EXIT=$?

if $DETACH && [[ $EXIT -eq 0 ]]; then
  echo
  echo "  $(green "┌─────────────────────────────────────────────────────────┐")"
  echo "  $(green "│")                                                         $(green "│")"
  echo "  $(green "│")   BeQuite Studio is running in the background!          $(green "│")"
  echo "  $(green "│")                                                         $(green "│")"
  echo "  $(green "│")     http://localhost:3000     marketing site            $(green "│")"
  echo "  $(green "│")     http://localhost:3000/docs   vibecoder tutorials    $(green "│")"
  echo "  $(green "│")     http://localhost:3001     dashboard                 $(green "│")"
  echo "  $(green "│")     http://localhost:3002/healthz   API health          $(green "│")"
  echo "  $(green "│")                                                         $(green "│")"
  echo "  $(green "│")   Follow logs:    docker compose logs -f                $(green "│")"
  echo "  $(green "│")   Stop:           ./scripts/docker-up.sh --down         $(green "│")"
  echo "  $(green "│")                                                         $(green "│")"
  echo "  $(green "└─────────────────────────────────────────────────────────┘")"
  echo
fi

exit $EXIT
