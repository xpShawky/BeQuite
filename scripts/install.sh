#!/usr/bin/env bash
# One-command install for BeQuite on macOS / Linux.
#
# - Verifies prerequisites (Python 3.11+, git).
# - Creates a venv in the current directory.
# - Installs the Layer 1 Harness CLI (bequite + bq) in editable mode.
# - Optionally installs Layer 2 Studio dependencies (--studio).
#
# Usage:
#   ./scripts/install.sh                              # CLI only, from inside a cloned repo
#   ./scripts/install.sh --studio                     # CLI + Studio deps
#   ./scripts/install.sh --clone-to /path/to/dir      # clone first, then install
#   ./scripts/install.sh --clone-to /tmp/bq --studio  # clone + Studio
#
set -euo pipefail

CLONE_TO=""
STUDIO=false
VENV_NAME=".venv"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --clone-to)   CLONE_TO="$2"; shift 2 ;;
    --studio)     STUDIO=true; shift ;;
    --venv-name)  VENV_NAME="$2"; shift 2 ;;
    -h|--help)
      head -n 12 "$0" | tail -n 11
      exit 0
      ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

section() { printf '\n\033[33m==> %s\033[0m\n' "$1"; }
have()    { command -v "$1" >/dev/null 2>&1; }

# --- 1. Prereqs ------------------------------------------------------------

section "Checking prerequisites"

if ! have python3 && ! have python; then
  echo "ERROR: python not on PATH. Install Python >= 3.11." >&2
  exit 1
fi
PY="$(command -v python3 || command -v python)"
echo "  Python: $($PY --version)"

if ! have git; then
  echo "ERROR: git not on PATH." >&2
  exit 1
fi
echo "  Git:    $(git --version)"

if $STUDIO; then
  have node && echo "  Node:   $(node --version)" || echo "  Node:   not installed (needed for Studio; https://nodejs.org)"
  have pnpm && echo "  pnpm:   $(pnpm --version)" || echo "  pnpm:   not installed (will fall back to npm)"
  have bun  && echo "  Bun:    $(bun --version)" || echo "  Bun:    not installed (needed for Studio API; curl -fsSL https://bun.sh/install | bash)"
fi

# --- 2. Clone if requested -------------------------------------------------

if [[ -n "$CLONE_TO" ]]; then
  section "Cloning into $CLONE_TO"
  if [[ -d "$CLONE_TO" ]]; then
    echo "  Directory exists; skipping clone."
  else
    git clone https://github.com/xpShawky/BeQuite.git "$CLONE_TO"
  fi
  cd "$CLONE_TO"
fi

if [[ ! -f "./cli/pyproject.toml" ]]; then
  echo "ERROR: cli/pyproject.toml not found. Run from inside a cloned BeQuite repo, or pass --clone-to." >&2
  exit 1
fi

# --- 3. Venv + CLI install -------------------------------------------------

section "Creating venv at ./$VENV_NAME"
[[ -d "$VENV_NAME" ]] || $PY -m venv "$VENV_NAME"

section "Activating venv"
# shellcheck disable=SC1090
source "$VENV_NAME/bin/activate"
echo "  active: ${VIRTUAL_ENV:-?}"

section "Upgrading pip"
python -m pip install --upgrade pip --quiet

section "Installing bequite CLI (editable)"
pip install -e ./cli

section "Verifying bequite CLI"
bequite --version

# --- 4. Optional Studio install --------------------------------------------

if $STUDIO; then
  section "Installing Studio API dependencies (Bun)"
  if have bun; then
    (cd ./studio/api && bun install)
  else
    echo "  Skipped (bun not on PATH)."
  fi

  PKG_MGR="npm"
  have pnpm && PKG_MGR="pnpm"

  section "Installing Studio Dashboard dependencies ($PKG_MGR)"
  (cd ./studio/dashboard && $PKG_MGR install)

  section "Installing Studio Marketing dependencies ($PKG_MGR)"
  (cd ./studio/marketing && $PKG_MGR install)
fi

# --- 5. Summary -------------------------------------------------------------

section "Install complete"
echo
echo "  bequite CLI:"
echo "    Activate venv:    source ./$VENV_NAME/bin/activate"
echo "    Try it:           bequite --version"
echo "    Doctor:           bequite doctor"
echo "    Initialize app:   bequite init my-app --doctrine default-web-saas"
echo
if $STUDIO; then
  echo "  Studio (three separate terminals):"
  echo "    [1] cd studio/api       && bun run src/index.ts                            # :3002"
  echo "    [2] cd studio/dashboard && BEQUITE_DASHBOARD_MODE=http pnpm dev            # :3001"
  echo "    [3] cd studio/marketing && pnpm dev                                        # :3000"
  echo
fi
echo "  Docs:               docs/INSTALL.md  /  README.md"
echo
