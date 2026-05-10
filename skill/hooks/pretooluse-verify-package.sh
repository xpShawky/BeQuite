#!/usr/bin/env bash
# skill/hooks/pretooluse-verify-package.sh
#
# PreToolUse hook: greps Edit/Write for newly added imports / dependencies
# and verifies the package exists in the relevant registry. Iron Law VII
# (Hallucination defense) + master §19.6 (Supply chain).
#
# Defends against the PhantomRaven attack class (Koi Security 2025, 126
# malicious npm packages exploiting AI-hallucinated names).
#
# Wired in template/.claude/settings.json under PreToolUse for Edit + Write.
# Exit 0 = allow. Exit 2 = block.
#
# Note: this hook performs network calls. In offline mode (BEQUITE_OFFLINE=1),
# skip and emit a warning to stderr. The skip itself is logged.

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // ""')

case "$TOOL_NAME" in
  Edit|Write) ;;
  *) exit 0 ;;
esac

FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // ""')
case "$TOOL_NAME" in
  Edit) CONTENT=$(printf '%s' "$INPUT" | jq -r '.tool_input.new_string // ""') ;;
  Write) CONTENT=$(printf '%s' "$INPUT" | jq -r '.tool_input.content // ""') ;;
esac

# Offline mode escape hatch (logged).
if [[ "${BEQUITE_OFFLINE:-0}" == "1" ]]; then
  echo "[bequite hook: pretooluse-verify-package] OFFLINE mode — skipping registry check (BEQUITE_OFFLINE=1)" >&2
  exit 0
fi

# Bequite allowlist — packages already known-good. Extend at
# skill/references/package-allowlist.md (drafted in v0.4.3).
ALLOWLIST_FILE="${BEQUITE_PACKAGE_ALLOWLIST:-skill/references/package-allowlist.md}"
ALLOWLIST=""
if [[ -f "$ALLOWLIST_FILE" ]]; then
  ALLOWLIST=$(cat "$ALLOWLIST_FILE" 2>/dev/null | grep -Eo '`[^`]+`' | tr -d '`' || true)
fi

is_allowed() {
  local pkg="$1"
  if [[ -z "$ALLOWLIST" ]]; then return 1; fi
  printf '%s\n' "$ALLOWLIST" | grep -Fxq "$pkg"
}

verify_npm() {
  local pkg="$1"
  if is_allowed "$pkg"; then return 0; fi
  if command -v npm >/dev/null 2>&1; then
    if npm view "$pkg" name >/dev/null 2>&1; then return 0; fi
  fi
  if command -v curl >/dev/null 2>&1; then
    if curl -fsSL "https://registry.npmjs.org/$pkg" >/dev/null 2>&1; then return 0; fi
  fi
  return 1
}

verify_pypi() {
  local pkg="$1"
  if is_allowed "$pkg"; then return 0; fi
  if command -v curl >/dev/null 2>&1; then
    if curl -fsSL "https://pypi.org/pypi/$pkg/json" >/dev/null 2>&1; then return 0; fi
  fi
  return 1
}

verify_cargo() {
  local pkg="$1"
  if is_allowed "$pkg"; then return 0; fi
  if command -v curl >/dev/null 2>&1; then
    if curl -fsSL "https://crates.io/api/v1/crates/$pkg" >/dev/null 2>&1; then return 0; fi
  fi
  return 1
}

# Determine ecosystem by file path.
case "$FILE_PATH" in
  *package.json|*pnpm-workspace.yaml)
    # Extract dependency entries from JSON. Match "name": "version"
    PACKAGES=$(printf '%s' "$CONTENT" | jq -r '
      ([.dependencies // {}, .devDependencies // {}, .peerDependencies // {}, .optionalDependencies // {}]
        | map(to_entries) | add | .[]?.key) // empty
    ' 2>/dev/null || true)
    for pkg in $PACKAGES; do
      if ! verify_npm "$pkg"; then
        cat >&2 <<EOF
[bequite hook: pretooluse-verify-package] BLOCKED — npm package not found in registry.

Iron Law VII (Hallucination defense): never import a package without
verifying it exists in this session.

Package: $pkg
Registry: npmjs.com
Ecosystem: npm

Possible causes:
- Hallucinated package name (PhantomRaven attack class).
- Typo (check spelling against npmjs.com search).
- Internal / private registry (configure registry URL or add to allowlist).
- Network issue (set BEQUITE_OFFLINE=1 to skip in offline contexts).

To allowlist a verified package:
  echo '\`$pkg\`' >> $ALLOWLIST_FILE

Reference: PhantomRaven campaign (Koi Security, Aug-Oct 2025) — 126
malicious npm packages exploiting AI-hallucinated names.
EOF
        exit 2
      fi
    done
    ;;
  *requirements.txt|*requirements-*.txt)
    # Extract package names (strip extras, version specifiers).
    while IFS= read -r line; do
      pkg=$(echo "$line" | sed 's/[[:space:]]*#.*$//' | sed 's/\[.*\]//' | sed 's/[<>=!~].*$//' | xargs)
      if [[ -n "$pkg" && "$pkg" != "-r" ]]; then
        if ! verify_pypi "$pkg"; then
          cat >&2 <<EOF
[bequite hook: pretooluse-verify-package] BLOCKED — PyPI package not found.
Package: $pkg
Registry: pypi.org
Ecosystem: PyPI
EOF
          exit 2
        fi
      fi
    done <<< "$CONTENT"
    ;;
  *pyproject.toml)
    # Extract dependency lines (best-effort regex).
    PACKAGES=$(printf '%s' "$CONTENT" | grep -Eo '"[a-zA-Z0-9_.-]+(\[[^]]+\])?[><=!~]' | sed 's/"//' | sed 's/\[.*//' | sed 's/[<>=!~].*//' || true)
    for pkg in $PACKAGES; do
      if [[ -n "$pkg" ]]; then
        if ! verify_pypi "$pkg"; then
          cat >&2 <<EOF
[bequite hook: pretooluse-verify-package] BLOCKED — PyPI package not found.
Package: $pkg
Registry: pypi.org
Ecosystem: PyPI (pyproject.toml)
EOF
          exit 2
        fi
      fi
    done
    ;;
  *Cargo.toml)
    PACKAGES=$(printf '%s' "$CONTENT" | grep -E '^[a-zA-Z0-9_-]+[[:space:]]*=' | grep -v '^\[' | sed 's/[[:space:]]*=.*$//' | tr -d ' ' || true)
    for pkg in $PACKAGES; do
      if [[ -n "$pkg" && "$pkg" != "name" && "$pkg" != "version" && "$pkg" != "edition" && "$pkg" != "authors" ]]; then
        if ! verify_cargo "$pkg"; then
          cat >&2 <<EOF
[bequite hook: pretooluse-verify-package] BLOCKED — crates.io package not found.
Package: $pkg
Registry: crates.io
Ecosystem: Rust
EOF
          exit 2
        fi
      fi
    done
    ;;
  *)
    # Other files — let through.
    exit 0
    ;;
esac

exit 0
