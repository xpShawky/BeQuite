"""Invoke skill/hooks/*.sh from non-Claude hosts.

Claude Code wires hooks via `.claude/settings.json`. For Cursor / Codex /
Gemini / Windsurf / Cline / Kilo / Continue / Aider, the BeQuite CLI exposes
the same hooks so they can be invoked manually or via per-host integration.

Pre-CLI usage:
    bequite hook run pretooluse-secret-scan --input-file path/to/tool-call.json
    bequite hook list
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HOOK_NAMES = [
    "pretooluse-secret-scan.sh",
    "pretooluse-block-destructive.sh",
    "pretooluse-verify-package.sh",
    "posttooluse-format.sh",
    "posttooluse-lint.sh",
    "posttooluse-audit.sh",
    "stop-verify-before-done.sh",
    "stop-cost-budget.sh",
    "sessionstart-load-memory.sh",
    "sessionstart-cost-budget.sh",
]


def find_hooks_dir(repo_root: Path) -> Path | None:
    candidates = [
        repo_root / "skill" / "hooks",
        repo_root / ".claude" / "skills" / "bequite" / "hooks",
        repo_root / ".cursor" / "skills" / "bequite" / "hooks",
    ]
    for c in candidates:
        if c.is_dir() and any(c.glob("*.sh")):
            return c
    return None


def list_hooks(repo_root: Path) -> int:
    hooks_dir = find_hooks_dir(repo_root)
    if not hooks_dir:
        print("(no hooks directory found)", file=sys.stderr)
        return 1
    for h in sorted(hooks_dir.glob("*.sh")):
        print(h.name)
    return 0


def run_hook(repo_root: Path, hook_name: str, input_path: Path | None = None) -> int:
    hooks_dir = find_hooks_dir(repo_root)
    if not hooks_dir:
        print("(no hooks directory found)", file=sys.stderr)
        return 2
    hook_path = hooks_dir / hook_name
    if not hook_path.exists():
        print(f"hook not found: {hook_name}", file=sys.stderr)
        return 2

    bash = shutil.which("bash") or shutil.which("sh")
    if not bash:
        print("bash/sh not found on PATH (Windows: install Git Bash)", file=sys.stderr)
        return 2

    if input_path:
        with input_path.open("rb") as f:
            stdin_data = f.read()
    else:
        stdin_data = b""

    try:
        result = subprocess.run(
            [bash, str(hook_path)],
            input=stdin_data,
            cwd=str(repo_root),
            timeout=60,
        )
        return result.returncode
    except subprocess.TimeoutExpired:
        print("(hook timed out)", file=sys.stderr)
        return 124
