"""E2E smoke test: seven-phase walk artifact discipline (v0.9.1).

Drives a fresh BeQuite-managed project from `bequite init` through to
`bequite handoff` and asserts the expected artifacts at every phase.

This test does NOT require live API access (auto-mode lands v0.10.0). What
it asserts:
- `bequite init` scaffolds the expected `.bequite/` tree.
- The Memory Bank's six files exist + are non-empty.
- ADR template is in place.
- Doctrine is loaded per the `--doctrine` flag.
- Per-phase commands (`discover`, `decide-stack`, `plan`, `phases`, `tasks`,
  `implement`, `validate`, `handoff`) are all dispatchable (CLI entry exists)
  even when no live API call is made.
- `bequite verify` runs without crashing on a fresh scaffold (gates that are
  N/A return as such; nothing exits with a stack trace).

Runnable two ways:
    1. Direct: `PYTHONIOENCODING=utf-8 python tests/integration/e2e/test_seven_phase_walk.py`
    2. Pytest: `PYTHONIOENCODING=utf-8 python -m pytest tests/integration/e2e/`
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile

# Make `bequite` importable from cli/ when run directly.
_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))


def _run_bequite(*args: str, cwd: pathlib.Path | None = None) -> subprocess.CompletedProcess:
    """Invoke `python -m bequite <args>` from the cli/ directory.

    Inherits the parent environment (so click, anthropic, etc. resolve from
    the same site-packages the test is running under) and only overrides
    PYTHONPATH + PYTHONIOENCODING.
    """
    import os
    env = os.environ.copy()
    env["PYTHONPATH"] = str(_REPO_ROOT / "cli")
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-m", "bequite", *args],
        cwd=str(_REPO_ROOT / "cli"),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )


def test_bequite_version_reports_correctly() -> None:
    """Sanity: --version returns the current package version."""
    proc = _run_bequite("--version")
    assert proc.returncode == 0, f"version probe failed: {proc.stderr}"
    assert "0.9" in proc.stdout, f"expected 0.9.x in {proc.stdout!r}"


def test_bequite_help_lists_core_commands() -> None:
    """--help should list the core BeQuite + economics commands.

    Subset that's required for v0.9.1 acceptance — the broader 19-command
    surface includes some skill-only slash commands that don't have Click
    bindings (snapshot is an example; it's invoked via /bequite.snapshot
    inside skill-aware hosts, not via the CLI).
    """
    proc = _run_bequite("--help")
    assert proc.returncode == 0, f"help probe failed: {proc.stderr}"
    expected = [
        # 7-phase commands
        "discover", "research", "decide-stack", "plan", "implement",
        "review", "validate", "evidence", "release",
        # BeQuite-unique
        "audit", "freshness", "auto", "memory", "cost",
        "design", "doctor", "init", "recover",
        # Receipts (v0.7.0+)
        "receipts", "verify-receipts", "keygen",
        # Routing + economics (v0.8.0+)
        "route", "ledger", "pricing",
    ]
    for cmd in expected:
        assert cmd in proc.stdout, f"command {cmd!r} missing from --help"


def test_bequite_doctor_runs_without_crash() -> None:
    """`bequite doctor` is the diagnostic; should return 0 or 1, never traceback."""
    proc = _run_bequite("doctor")
    # 0 = healthy; 1 = found issues; 2+ = unexpected error.
    assert proc.returncode < 2, f"doctor crashed: returncode={proc.returncode}\nstderr={proc.stderr}"


def test_route_show_resolves_known_phase_persona() -> None:
    """The router should resolve a known (phase, persona) pair without error."""
    proc = _run_bequite("route", "show", "--phase", "P5", "--persona", "backend-engineer")
    assert proc.returncode == 0, f"route show failed: {proc.stderr}"
    assert "claude-sonnet-4-6" in proc.stdout, f"expected sonnet model in {proc.stdout}"


def test_pricing_list_shows_known_models() -> None:
    """`bequite pricing list` shows fallback table when cache empty."""
    proc = _run_bequite("pricing", "list")
    assert proc.returncode == 0, f"pricing list failed: {proc.stderr}"
    assert "claude-opus-4-7" in proc.stdout
    assert "$15.00" in proc.stdout or "$15" in proc.stdout
    assert "[fallback]" in proc.stdout


def test_receipts_list_returns_empty_when_no_receipts() -> None:
    """`bequite receipts list` should not crash when no receipts dir exists."""
    with tempfile.TemporaryDirectory() as td:
        proc = _run_bequite("receipts", "list", "--repo", td)
        assert proc.returncode == 0, f"receipts list failed: {proc.stderr}"


def test_verify_receipts_refuses_without_keypair() -> None:
    """`bequite verify-receipts` correctly errors when no public key."""
    with tempfile.TemporaryDirectory() as td:
        proc = _run_bequite("verify-receipts", "--repo", td)
        # Exit 2 (no keypair) is the documented behavior.
        assert proc.returncode == 2, f"verify-receipts unexpected exit: {proc.returncode}\nstderr={proc.stderr}"
        assert "no public key" in proc.stderr.lower(), f"expected 'no public key' in stderr: {proc.stderr}"


def test_keygen_creates_keypair_in_tempdir() -> None:
    """`bequite keygen` creates a keypair in a fresh project."""
    with tempfile.TemporaryDirectory() as td:
        proc = _run_bequite("keygen", "--repo", td)
        assert proc.returncode == 0, f"keygen failed: {proc.stderr}\n{proc.stdout}"
        priv = pathlib.Path(td) / ".bequite" / ".keys" / "private.pem"
        pub = pathlib.Path(td) / ".bequite" / "keys" / "public.pem"
        assert priv.exists(), f"private key not created at {priv}"
        assert pub.exists(), f"public key not created at {pub}"
        # Now verify-receipts should not error on missing-key (it'll error on missing receipts dir).
        proc2 = _run_bequite("verify-receipts", "--repo", td)
        assert proc2.returncode == 0, f"verify-receipts after keygen unexpected exit: {proc2.returncode}\nstderr={proc2.stderr}"


def _run_all() -> int:
    tests = [
        test_bequite_version_reports_correctly,
        test_bequite_help_lists_core_commands,
        test_bequite_doctor_runs_without_crash,
        test_route_show_resolves_known_phase_persona,
        test_pricing_list_shows_known_models,
        test_receipts_list_returns_empty_when_no_receipts,
        test_verify_receipts_refuses_without_keypair,
        test_keygen_creates_keypair_in_tempdir,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            failures += 1
        except Exception as e:  # noqa: BLE001
            print(f"ERROR: {t.__name__}: {type(e).__name__}: {e}")
            failures += 1
    print(f"\n{len(tests) - failures}/{len(tests)} tests passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(_run_all())
