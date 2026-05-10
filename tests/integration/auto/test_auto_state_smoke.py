"""Integration smoke test for cli/bequite/auto_state.py (BeQuite v0.10.7)."""

from __future__ import annotations

import pathlib
import sys
import tempfile

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))

from bequite.auto import AutoState, save_state, transition  # noqa: E402
from bequite.auto_state import (  # noqa: E402
    can_resume,
    detect_double_commit,
    fan_out_parallel,
    is_phase_idempotent_rerun,
    list_sessions,
    resume_session,
    should_split_parallel,
)


def test_list_sessions_empty() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        assert list_sessions(repo) == []


def test_list_sessions_returns_saved() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        s1 = AutoState(feature="a")
        s2 = AutoState(feature="b")
        save_state(repo, s1)
        save_state(repo, s2)
        sessions = list_sessions(repo)
        assert len(sessions) == 2
        features = {s["feature"] for s in sessions}
        assert features == {"a", "b"}


def test_can_resume_blocked() -> None:
    s = AutoState(current_phase="BLOCKED", blocked_reason="x")
    ok, reason = can_resume(s)
    assert ok is True


def test_can_resume_done_returns_false() -> None:
    s = AutoState(current_phase="DONE")
    ok, reason = can_resume(s)
    assert ok is False
    assert "DONE" in reason


def test_can_resume_failed_returns_false() -> None:
    s = AutoState(current_phase="FAILED", failed_reason="boom")
    ok, reason = can_resume(s)
    assert ok is False
    assert "boom" in reason


def test_resume_session_clears_blocked_markers() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        s = AutoState(current_phase="BLOCKED", blocked_reason="cost ceiling", consecutive_failures=2)
        s = transition(s, "BLOCKED", "stuck")
        s.completed_phases = ["P0", "P1"]
        save_state(repo, s)
        resumed, err = resume_session(repo, s.session_id)
        assert err is None
        assert resumed is not None
        assert resumed.blocked_reason is None
        assert resumed.consecutive_failures == 0
        assert resumed.current_phase == "P2"  # next after P1


def test_resume_session_unknown_id_returns_error() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        resumed, err = resume_session(repo, "no-such-session")
        assert resumed is None
        assert "no state" in err


def test_should_split_parallel_threshold() -> None:
    assert should_split_parallel(3) is False
    assert should_split_parallel(5) is False
    assert should_split_parallel(6) is True


def test_fan_out_parallel_below_threshold_marks_ineligible() -> None:
    tasks = [{"id": f"t{i}"} for i in range(3)]
    out = fan_out_parallel(tasks)
    assert all(t["parallel_eligible"] is False for t in out)


def test_fan_out_parallel_above_threshold_marks_eligible() -> None:
    tasks = [{"id": f"t{i}"} for i in range(7)]
    out = fan_out_parallel(tasks)
    assert all(t["parallel_eligible"] is True for t in out)


def test_fan_out_parallel_dependency_blocks_eligibility() -> None:
    tasks = [
        {"id": f"t{i}", "depends_on": [f"t{i-1}"] if i > 0 else []}
        for i in range(7)
    ]
    out = fan_out_parallel(tasks)
    # Every task except t0 has an unmet dependency → ineligible.
    assert out[0]["parallel_eligible"] is True
    assert all(out[i]["parallel_eligible"] is False for i in range(1, 7))


def test_is_phase_idempotent_rerun() -> None:
    s = AutoState(completed_phases=["P0", "P1"])
    assert is_phase_idempotent_rerun(s, "P0") is True
    assert is_phase_idempotent_rerun(s, "P1") is True
    assert is_phase_idempotent_rerun(s, "P2") is False


def test_detect_double_commit() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        s1 = AutoState(feature="add-health-endpoint", current_phase="P3")
        save_state(repo, s1)
        # Detect the in-flight session.
        conflict = detect_double_commit(repo, "add-health-endpoint")
        assert conflict == s1.session_id
        # Different feature → no conflict.
        assert detect_double_commit(repo, "different-feature") is None


def _run_all() -> int:
    tests = [
        test_list_sessions_empty,
        test_list_sessions_returns_saved,
        test_can_resume_blocked,
        test_can_resume_done_returns_false,
        test_can_resume_failed_returns_false,
        test_resume_session_clears_blocked_markers,
        test_resume_session_unknown_id_returns_error,
        test_should_split_parallel_threshold,
        test_fan_out_parallel_below_threshold_marks_ineligible,
        test_fan_out_parallel_above_threshold_marks_eligible,
        test_fan_out_parallel_dependency_blocks_eligibility,
        test_is_phase_idempotent_rerun,
        test_detect_double_commit,
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
