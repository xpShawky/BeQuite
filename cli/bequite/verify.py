"""bequite verify — Phase 6 validation mesh orchestrator.

Runs the per-Mode gate matrix (per Constitution v1.0.1):

    Format / Lint / Typecheck / Unit / Integration / API / DB-migration /
    Seed / E2E (Playwright) / Accessibility / Build / Docker Compose /
    Security scan / bequite audit / bequite freshness / Restore-drill (Enterprise)

For each gate that's appropriate to `state/project.yaml::mode`, run the
relevant command and capture exit code + stdout hash + duration. Emit a
roll-up to `evidence/P6/verify-<timestamp>.md` and (when v0.7.0+ receipts
ship) a signed receipt at `.bequite/receipts/<sha>-P6-verify.json`.

This v0.6.0 implementation ships the orchestrator + per-gate command
contract. The Playwright planner→generator→healer loop ships in v0.6.1
alongside the Impeccable bundle (frontend Doctrine integration).

Pre-CLI usage:
    python -m cli.bequite.verify [--gate <name>] [--mode fast|safe|enterprise]
                                  [--no-color] [--json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

# tomllib in Python 3.11+ stdlib
try:
    import tomllib  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[import-not-found,no-redef]


# ----------------------------------------------------------------------------
# Domain
# ----------------------------------------------------------------------------


@dataclass
class GateResult:
    name: str
    command: str | None
    skipped: bool
    exit_code: int | None
    duration_seconds: float
    stdout_hash: str | None
    stderr_tail: str | None
    note: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class VerifyConfig:
    repo_root: Path
    mode: str = "safe"
    active_doctrines: list[str] = field(default_factory=list)
    gate_filter: str | None = None
    web_server_command: str | None = None
    base_url: str = "http://localhost:3000"


GATE_REQUIRED_BY_MODE: dict[str, dict[str, set[str]]] = {
    # gate_name: { mode: {"required" | "optional" | "skipped"} }
    "format": {"fast": "required", "safe": "required", "enterprise": "required"},
    "lint": {"fast": "required", "safe": "required", "enterprise": "required"},
    "typecheck": {"fast": "required", "safe": "required", "enterprise": "required"},
    "unit": {"fast": "required", "safe": "required", "enterprise": "required"},
    "integration": {"fast": "optional", "safe": "required", "enterprise": "required"},
    "api": {"fast": "optional", "safe": "required", "enterprise": "required"},
    "db-migration": {"fast": "optional", "safe": "required", "enterprise": "required"},
    "seed": {"fast": "optional", "safe": "required", "enterprise": "required"},
    "e2e": {"fast": "optional", "safe": "required", "enterprise": "required"},
    "accessibility": {"fast": "optional", "safe": "required", "enterprise": "required"},
    "build": {"fast": "required", "safe": "required", "enterprise": "required"},
    "docker-compose": {"fast": "optional", "safe": "optional", "enterprise": "required"},
    "security-scan": {"fast": "optional", "safe": "required", "enterprise": "required"},
    "audit": {"fast": "required", "safe": "required", "enterprise": "required"},
    "freshness": {"fast": "optional", "safe": "required", "enterprise": "required"},
    "self-walk": {"fast": "optional", "safe": "required", "enterprise": "required"},
    "smoke": {"fast": "required", "safe": "required", "enterprise": "required"},
    "restore-drill": {"fast": "skipped", "safe": "skipped", "enterprise": "required"},
}


# ----------------------------------------------------------------------------
# Detection — which command runs each gate (per stack)
# ----------------------------------------------------------------------------


def detect_command(gate: str, config: VerifyConfig) -> str | None:
    """Best-effort: pick the right command for this gate based on what's in the repo."""
    repo = config.repo_root

    # Read package.json scripts when present.
    pkg_json = repo / "package.json"
    pkg_scripts: dict[str, str] = {}
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(encoding="utf-8"))
            pkg_scripts = data.get("scripts", {}) or {}
        except (OSError, json.JSONDecodeError):
            pass

    pkg_manager = "pnpm" if (repo / "pnpm-lock.yaml").exists() else "npm"

    py_toml = repo / "pyproject.toml"
    has_py = py_toml.exists()

    cargo = repo / "Cargo.toml"
    has_rust = cargo.exists()

    match gate:
        case "format":
            if pkg_scripts.get("format"):
                return f"{pkg_manager} run format"
            if has_py:
                return "ruff format --check ."
            if has_rust:
                return "cargo fmt --check"
            return None
        case "lint":
            if pkg_scripts.get("lint"):
                return f"{pkg_manager} run lint"
            if has_py:
                return "ruff check ."
            if has_rust:
                return "cargo clippy --all-targets -- -D warnings"
            return None
        case "typecheck":
            if pkg_scripts.get("typecheck"):
                return f"{pkg_manager} run typecheck"
            if has_py:
                return "mypy ."
            if has_rust:
                return "cargo check"
            return None
        case "unit":
            if pkg_scripts.get("test:unit") or pkg_scripts.get("test"):
                return f"{pkg_manager} run {('test:unit' if 'test:unit' in pkg_scripts else 'test')}"
            if has_py:
                return "pytest tests/unit/ -q"
            if has_rust:
                return "cargo test --lib"
            return None
        case "integration":
            if pkg_scripts.get("test:integration"):
                return f"{pkg_manager} run test:integration"
            if has_py:
                return "pytest tests/integration/ -q"
            return None
        case "api":
            if pkg_scripts.get("test:api"):
                return f"{pkg_manager} run test:api"
            return None
        case "db-migration":
            if pkg_scripts.get("db:migrate"):
                return f"{pkg_manager} run db:migrate"
            if (repo / "prisma/schema.prisma").exists():
                return "npx prisma migrate dev --name verify-test"
            return None
        case "seed":
            if pkg_scripts.get("db:seed"):
                return f"{pkg_manager} run db:seed"
            return None
        case "e2e":
            if (repo / "playwright.config.ts").exists() or (repo / "playwright.config.js").exists():
                return "npx playwright test"
            if pkg_scripts.get("test:e2e"):
                return f"{pkg_manager} run test:e2e"
            return None
        case "accessibility":
            if pkg_scripts.get("test:a11y"):
                return f"{pkg_manager} run test:a11y"
            return None
        case "build":
            if pkg_scripts.get("build"):
                return f"{pkg_manager} run build"
            if has_py:
                return "python -m build" if (repo / "pyproject.toml").exists() else None
            if has_rust:
                return "cargo build --release"
            return None
        case "docker-compose":
            if (repo / "docker-compose.yml").exists() or (repo / "compose.yaml").exists():
                return "docker compose up -d --wait"
            return None
        case "security-scan":
            commands = []
            if (repo / "package.json").exists():
                commands.append("npx osv-scanner --recursive .")
            if has_py:
                commands.append("pip-audit")
            commands.append("trivy fs --severity HIGH,CRITICAL --exit-code 1 .")
            return " && ".join(commands)
        case "audit":
            return "python -m cli.bequite.audit --ci"
        case "freshness":
            return "python -m cli.bequite.freshness --all"
        case "self-walk":
            sw = repo / "scripts" / "self-walk.sh"
            if sw.exists():
                return f"bash {sw}"
            return None
        case "smoke":
            sk = repo / "scripts" / "smoke.sh"
            if sk.exists():
                return f"bash {sk}"
            return None
        case "restore-drill":
            sk = repo / "scripts" / "restore-drill.sh"
            if sk.exists():
                return f"bash {sk}"
            return None
    return None


# ----------------------------------------------------------------------------
# Runner
# ----------------------------------------------------------------------------


def run_gate(gate: str, command: str | None, config: VerifyConfig) -> GateResult:
    if command is None:
        return GateResult(
            name=gate,
            command=None,
            skipped=True,
            exit_code=None,
            duration_seconds=0.0,
            stdout_hash=None,
            stderr_tail=None,
            note="(no command configured for this gate in this stack)",
        )

    start = time.time()
    try:
        completed = subprocess.run(
            shlex.split(command) if not command.startswith("bash ") else ["bash", "-c", command[5:]],
            cwd=config.repo_root,
            capture_output=True,
            text=True,
            timeout=600,
        )
    except subprocess.TimeoutExpired:
        return GateResult(
            name=gate,
            command=command,
            skipped=False,
            exit_code=124,
            duration_seconds=time.time() - start,
            stdout_hash=None,
            stderr_tail="(timed out)",
            note="600s timeout",
        )
    except FileNotFoundError as e:
        return GateResult(
            name=gate,
            command=command,
            skipped=False,
            exit_code=127,
            duration_seconds=time.time() - start,
            stdout_hash=None,
            stderr_tail=str(e),
            note="command not on PATH",
        )

    duration = time.time() - start
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    stdout_hash = "sha256:" + hashlib.sha256(stdout.encode("utf-8")).hexdigest()
    stderr_tail = "\n".join(stderr.splitlines()[-20:]) if stderr else None

    return GateResult(
        name=gate,
        command=command,
        skipped=False,
        exit_code=completed.returncode,
        duration_seconds=duration,
        stdout_hash=stdout_hash,
        stderr_tail=stderr_tail,
    )


# ----------------------------------------------------------------------------
# Config loader
# ----------------------------------------------------------------------------


def load_verify_config(repo_root: Path, args: argparse.Namespace) -> VerifyConfig:
    mode = args.mode or "safe"
    active_doctrines: list[str] = []

    project_yaml = repo_root / "state" / "project.yaml"
    if project_yaml.exists():
        text = project_yaml.read_text(encoding="utf-8", errors="replace")
        import re
        m = re.search(r"^\s*mode\s*:\s*(\S+)", text, re.MULTILINE)
        if m:
            mode = m.group(1).strip()
        m = re.search(r"^\s*active_doctrines\s*:\s*((?:\n\s+-\s+\S+)+)", text, re.MULTILINE)
        if m:
            active_doctrines = re.findall(r"-\s+(\S+)", m.group(1))

    return VerifyConfig(
        repo_root=repo_root,
        mode=mode.lower(),
        active_doctrines=active_doctrines,
        gate_filter=args.gate,
        base_url=os.environ.get("BASE_URL", "http://localhost:3000"),
    )


# ----------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------


def render_console(results: list[GateResult], config: VerifyConfig) -> str:
    lines = [f"[bequite verify] mode={config.mode}, doctrines={config.active_doctrines or '(none)'}\n"]
    for r in results:
        if r.skipped:
            lines.append(f"  [skip] {r.name}  — {r.note}")
        elif r.exit_code == 0:
            lines.append(f"  [PASS] {r.name}  ({r.duration_seconds:.1f}s)")
        else:
            lines.append(f"  [FAIL] {r.name}  exit={r.exit_code}  ({r.duration_seconds:.1f}s)")
            if r.stderr_tail:
                lines.append("         " + r.stderr_tail.replace("\n", "\n         "))

    failed = [r for r in results if not r.skipped and r.exit_code != 0]
    if failed:
        lines.append(f"\n  {len(failed)} gate(s) FAILED. Phase 6 cannot exit until resolved.")
    else:
        lines.append("\n  All non-skipped gates PASSED.")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bequite verify",
        description=(
            "Phase 6 validation mesh — runs the per-Mode gate matrix and "
            "emits an evidence roll-up. Wires Playwright + smoke + audit + "
            "freshness in one command."
        ),
    )
    parser.add_argument("--repo", default=".", help="repo root (default: cwd)")
    parser.add_argument("--mode", default=None, choices=["fast", "safe", "enterprise"], help="override active Mode")
    parser.add_argument("--gate", default=None, help="run only one gate (e.g. e2e, audit)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--no-color", action="store_true", help="disable color output")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo).resolve()
    config = load_verify_config(repo_root, args)

    # Build the gate list per active mode.
    gates: list[str] = []
    for gate, mode_map in GATE_REQUIRED_BY_MODE.items():
        if mode_map.get(config.mode, "skipped") in {"required", "optional"}:
            if config.gate_filter and config.gate_filter != gate:
                continue
            gates.append(gate)

    results: list[GateResult] = []
    for gate in gates:
        cmd = detect_command(gate, config)
        result = run_gate(gate, cmd, config)
        results.append(result)
        # Stop early on a "required" failure so user fixes one thing at a time.
        if (
            not result.skipped
            and result.exit_code != 0
            and GATE_REQUIRED_BY_MODE[gate].get(config.mode) == "required"
        ):
            break

    # Save evidence.
    evidence_dir = repo_root / "evidence" / "P6"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime())
    (evidence_dir / f"verify-{timestamp}.json").write_text(
        json.dumps({"mode": config.mode, "doctrines": config.active_doctrines, "results": [r.to_dict() for r in results]}, indent=2),
        encoding="utf-8",
    )

    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2))
    else:
        print(render_console(results, config))

    failed = [r for r in results if not r.skipped and r.exit_code != 0]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
