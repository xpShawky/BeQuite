#!/usr/bin/env bash
# Vibecoder-friendly one-line install for BeQuite on macOS / Linux.
#
# Run with:
#   curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.sh | bash
#
# Or with --studio for the full Studio surface:
#   curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.sh | bash -s -- --studio
#
# What it does:
#   1. Checks for python3 + git. Prints a clear install hint if missing.
#   2. Clones https://github.com/xpShawky/BeQuite into ./BeQuite/.
#   3. Runs scripts/install.sh from inside the clone.
#   4. Prints next-step commands.

set -uo pipefail
# (no -e — we want to give the user clean error messages, not die on first
# stderr-as-error from a non-critical native command)

STUDIO=false
INSTALL_DIR="./BeQuite"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --studio)      STUDIO=true; shift ;;
    --install-dir) INSTALL_DIR="$2"; shift 2 ;;
    -h|--help)
      head -n 17 "$0" | tail -n 16
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

bold()   { printf '\033[1m%s\033[0m' "$*"; }
red()    { printf '\033[31m%s\033[0m' "$*"; }
yellow() { printf '\033[33m%s\033[0m' "$*"; }
green()  { printf '\033[32m%s\033[0m' "$*"; }
cyan()   { printf '\033[36m%s\033[0m' "$*"; }

section() { echo; echo "$(yellow "==> $1")"; }
have() { command -v "$1" >/dev/null 2>&1; }

# --- Banner ---------------------------------------------------------------

echo
echo "  $(yellow "┌─────────────────────────────────────────────┐")"
echo "  $(yellow "│")  $(bold "BeQuite — one-command installer")           $(yellow "│")"
echo "  $(yellow "│")   Build it right the first time.            $(yellow "│")"
echo "  $(yellow "└─────────────────────────────────────────────┘")"
echo

# --- 1. Prereq checks -----------------------------------------------------

section "Checking prerequisites"

MISSING=()

if have python3; then
  echo "  $(green "[OK]") Python: $(python3 --version)"
elif have python; then
  echo "  $(green "[OK]") Python: $(python --version)"
else
  MISSING+=("Python 3.11+ — needed to run bequite CLI")
fi

if have git; then
  echo "  $(green "[OK]") Git:    $(git --version)"
else
  MISSING+=("Git — needed to clone the BeQuite repository")
fi

if $STUDIO; then
  if have node; then
    echo "  $(green "[OK]") Node:   $(node --version)"
  else
    MISSING+=("Node.js 20+ — needed for Studio dashboard + marketing")
  fi
  if have bun; then
    echo "  $(green "[OK]") Bun:    $(bun --version)"
  else
    echo "  $(yellow "[WARN]") Bun:    not installed (needed for Studio API only)"
    echo "         Install with:  curl -fsSL https://bun.sh/install | bash"
  fi
fi

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo
  echo "$(red "MISSING PREREQUISITES — install these first, then re-run the bootstrap:")"
  echo
  for m in "${MISSING[@]}"; do
    echo "  $(red "·") $m"
  done
  echo
  echo "Install hints:"
  echo "  $(cyan "macOS:")    brew install python3 node git"
  echo "  $(cyan "Ubuntu:")   sudo apt install python3 python3-venv nodejs npm git"
  echo "  $(cyan "Bun:")      curl -fsSL https://bun.sh/install | bash"
  echo
  echo "Then re-run:"
  echo "  $(cyan "curl -fsSL https://raw.githubusercontent.com/xpShawky/BeQuite/main/scripts/bootstrap.sh | bash")"
  echo
  exit 1
fi

# --- 2. Clone -------------------------------------------------------------

section "Cloning BeQuite into $INSTALL_DIR"

if [[ -d "$INSTALL_DIR" ]]; then
  echo "  Directory already exists at: $(realpath "$INSTALL_DIR" 2>/dev/null || echo "$INSTALL_DIR")"
  echo "  Skipping clone. To start fresh, delete it first:"
  echo "    rm -rf \"$INSTALL_DIR\""
else
  if ! git clone https://github.com/xpShawky/BeQuite.git "$INSTALL_DIR"; then
    echo "$(red "FATAL: git clone failed.")" >&2
    exit 1
  fi
fi

# --- 3. Run install.sh from inside the clone ------------------------------

cd "$INSTALL_DIR"

if [[ ! -f "./scripts/install.sh" ]]; then
  echo "$(red "FATAL: scripts/install.sh not found inside the clone.")" >&2
  exit 1
fi

chmod +x ./scripts/install.sh

section "Running install.sh"

if $STUDIO; then
  ./scripts/install.sh --studio
else
  ./scripts/install.sh
fi

INSTALL_EXIT=$?
if [[ $INSTALL_EXIT -ne 0 ]]; then
  echo "$(red "FATAL: install.sh exited with code $INSTALL_EXIT")" >&2
  exit $INSTALL_EXIT
fi

# --- 4. Bonus next-step nudge ---------------------------------------------

echo
echo "  $(green "┌─────────────────────────────────────────────────────────────┐")"
echo "  $(green "│                                                             │")"
echo "  $(green "│")   $(bold "Bootstrap complete!")                                       $(green "│")"
echo "  $(green "│                                                             │")"
echo "  $(green "│")   Next:                                                     $(green "│")"
echo "  $(green "│                                                             │")"
echo "  $(green "│")     cd BeQuite                                              $(green "│")"
echo "  $(green "│")     source ./.venv/bin/activate                             $(green "│")"
echo "  $(green "│")     bequite quickstart                                      $(green "│")"
echo "  $(green "│                                                             │")"
echo "  $(green "└─────────────────────────────────────────────────────────────┘")"
echo
