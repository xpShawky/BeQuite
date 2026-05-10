"""Integration smoke test for cli/bequite/auto.py (BeQuite v0.10.0)."""

from __future__ import annotations

import pathlib
import sys
import tempfile

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))

from bequite.auto import (  # noqa: E402
    PHASES,
    AutoState,
    check_banned_words,
    check_cost_ceiling,
    check_failure_threshold,
    check_one_way_door,
    check_wall_clock,
    load_state,
    run_all_phases,
    run_phase,
    save_state,
    state_path,
    transition,
)


def test_state_roundtrips() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        s = AutoState(feature="x")
        save_state(repo, s)
        loaded = load_state(repo, s.session_id)
        assert loaded is not None
        assert loaded.feature == "x"
        assert loaded.session_id == s.session_id


def test_banned_word_detected() -> None:
    assert check_banned_words("This should work") == "should"
    assert check_banned_words("It probably runs") == "probably"
    assert check_banned_words("All tests pass; build green; deploy success") is None


def test_one_way_door_detected() -> None:
    assert check_one_way_door("git push origin main") is not None
    assert check_one_way_door("twine upload dist/*") is not None
    assert check_one_way_door("npm publish --access public") is not None
    assert check_one_way_door("git status") is None


def test_cost_ceiling_blocks() -> None:
    s = AutoState(cost_usd_so_far=25.0, max_cost_usd=20.0)
    assert check_cost_ceiling(s) is not None


def test_wall_clock_blocks() -> None:
    import datetime
    s = AutoState(max_wall_clock_hours=0.0001)  # 0.36s
    s.started_utc = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=10)).isoformat(timespec="seconds")
    assert check_wall_clock(s) is not None


def test_failure_threshold_blocks() -> None:
    s = AutoState(consecutive_failures=3)
    assert check_failure_threshold(s) is not None
    s2 = AutoState(consecutive_failures=2)
    assert check_failure_threshold(s2) is None


def test_run_all_phases_done_in_stub_mode() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        s = AutoState(feature="test")
        s = run_all_phases(s, repo_root=repo)
        assert s.current_phase == "DONE"
        assert s.completed_phases == PHASES


def test_run_phase_blocks_on_banned_word() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        s = AutoState(feature="test")
        def do_work_with_weasel(state):
            return (0.0, "This should probably work I think")
        s = run_phase(s, "P0", repo_root=repo, do_work=do_work_with_weasel)
        assert s.current_phase == "BLOCKED"
        assert "should" in s.blocked_reason or "probably" in s.blocked_reason


def test_run_phase_blocks_on_cost_ceiling() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        s = AutoState(feature="test", cost_usd_so_far=21.0, max_cost_usd=20.0)
        s = run_phase(s, "P0", repo_root=repo)
        assert s.current_phase == "BLOCKED"
        assert "cost ceiling" in s.blocked_reason


def test_run_phase_increments_cost_on_success() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        s = AutoState(feature="test")
        def do_work(state):
            return (0.05, "P0 done; tests pass; receipts emit")
        s = run_phase(s, "P0", repo_root=repo, do_work=do_work)
        assert s.current_phase == "P0"
        assert abs(s.cost_usd_so_far - 0.05) < 1e-9


def test_transition_records_completed_phases() -> None:
    s = AutoState(current_phase="P0")
    s = transition(s, "P1")
    assert s.completed_phases == ["P0"]
    s = transition(s, "P2")
    assert s.completed_phases == ["P0", "P1"]


def _run_all() -> int:
    tests = [
        test_state_roundtrips,
        test_banned_word_detected,
        test_one_way_door_detected,
        test_cost_ceiling_blocks,
        test_wall_clock_blocks,
        test_failure_threshold_blocks,
        test_run_all_phases_done_in_stub_mode,
        test_run_phase_blocks_on_banned_word,
        test_run_phase_blocks_on_cost_ceiling,
        test_run_phase_increments_cost_on_success,
        test_transition_records_completed_phases,
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
