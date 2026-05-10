"""Integration smoke test for cli/bequite/receipts.py (BeQuite v0.7.0).

Runnable two ways:
    1. Direct: `PYTHONIOENCODING=utf-8 python tests/integration/receipts/test_receipts_smoke.py`
    2. Pytest: `PYTHONIOENCODING=utf-8 python -m pytest tests/integration/receipts/`

Both require `cli/` on sys.path (the second ensures it via conftest.py / pytest config).
"""

from __future__ import annotations

import dataclasses
import pathlib
import sys
import tempfile

# Make `bequite` importable from cli/ when run directly.
_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))

from bequite.receipts import (  # noqa: E402
    Receipt,
    ReceiptStore,
    make_receipt,
    replay_check,
    roll_up_by_day,
    roll_up_by_phase,
    roll_up_by_session,
    validate_chain,
)


def _make_test_env(td: pathlib.Path) -> tuple[ReceiptStore, pathlib.Path]:
    """Build a temporary receipt store + memory snapshot directory."""
    store_dir = td / "receipts"
    mem_dir = td / "mem"
    mem_dir.mkdir()
    (mem_dir / "constitution.md").write_text("# Iron Laws v1.2.0", encoding="utf-8")
    (mem_dir / "activeContext.md").write_text("# Active Context", encoding="utf-8")
    return (ReceiptStore(str(store_dir)), mem_dir)


def test_emit_and_list() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        store, mem_dir = _make_test_env(td)

        r = make_receipt(
            phase="P0",
            model_name="claude-opus-4-7",
            reasoning_effort="high",
            prompt="P0 research prompt.",
            memory_snapshot_dir=mem_dir,
            diff_from="HEAD",
            diff_to="HEAD",
            doctrines=["default-web-saas"],
            constitution_version="1.2.0",
            input_tokens=100,
            output_tokens=50,
            usd=0.012,
        )
        target = store.write(r)
        assert target.exists()
        assert target.suffix == ".json"

        receipts = store.list_all()
        assert len(receipts) == 1
        assert receipts[0].content_hash() == r.content_hash()


def test_chain_validation_valid() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        store, mem_dir = _make_test_env(td)

        r1 = make_receipt(
            phase="P0", model_name="m", reasoning_effort="default",
            prompt="p0", memory_snapshot_dir=mem_dir,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
        )
        store.write(r1)
        r2 = make_receipt(
            phase="P1", model_name="m", reasoning_effort="default",
            prompt="p1", memory_snapshot_dir=mem_dir,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
            parent_receipt=r1.content_hash(), session_id=r1.session_id,
        )
        store.write(r2)

        receipts = store.list_all()
        ok, issues = validate_chain(receipts)
        assert ok, f"expected valid chain, got: {issues}"


def test_chain_validation_missing_parent() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        _, mem_dir = _make_test_env(td)

        r1 = make_receipt(
            phase="P0", model_name="m", reasoning_effort="default",
            prompt="p0", memory_snapshot_dir=mem_dir,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
        )
        r2_orphan = make_receipt(
            phase="P1", model_name="m", reasoning_effort="default",
            prompt="p1", memory_snapshot_dir=mem_dir,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
            parent_receipt="sha256:nonexistent", session_id=r1.session_id,
        )
        ok, issues = validate_chain([r1, r2_orphan])
        assert not ok
        assert any("missing parent" in i for i in issues), f"got: {issues}"


def test_replay_check_pass() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        _, mem_dir = _make_test_env(td)
        prompt = "exact-prompt-text"
        r = make_receipt(
            phase="P0", model_name="m", reasoning_effort="default",
            prompt=prompt, memory_snapshot_dir=mem_dir,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
        )
        ok, issues = replay_check(r, prompt, mem_dir)
        assert ok, f"expected replay pass, got: {issues}"


def test_replay_check_tampered_prompt() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        _, mem_dir = _make_test_env(td)
        r = make_receipt(
            phase="P0", model_name="m", reasoning_effort="default",
            prompt="original", memory_snapshot_dir=mem_dir,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
        )
        ok, issues = replay_check(r, "tampered", mem_dir)
        assert not ok
        assert any("prompt_hash mismatch" in i for i in issues), f"got: {issues}"


def test_roll_up_by_session() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        store, mem_dir = _make_test_env(td)
        sid = "test-session-id"
        for i, (phase, usd) in enumerate([("P0", 0.01), ("P1", 0.02), ("P5", 0.03)]):
            r = make_receipt(
                phase=phase, model_name="m", reasoning_effort="default",
                prompt=f"p{i}", memory_snapshot_dir=mem_dir,
                diff_from="HEAD", diff_to="HEAD",
                doctrines=["default-web-saas"], constitution_version="1.2.0",
                input_tokens=100, output_tokens=50, usd=usd, session_id=sid,
            )
            store.write(r)
        receipts = store.list_all()
        rollup = roll_up_by_session(receipts)
        assert sid in rollup
        assert abs(rollup[sid]["usd"] - 0.06) < 1e-9
        assert rollup[sid]["input_tokens"] == 300
        assert rollup[sid]["output_tokens"] == 150


def test_roll_up_by_phase() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        store, mem_dir = _make_test_env(td)
        for i in range(3):
            r = make_receipt(
                phase="P5", model_name="m", reasoning_effort="default",
                prompt=f"p{i}", memory_snapshot_dir=mem_dir,
                diff_from="HEAD", diff_to="HEAD",
                doctrines=[], constitution_version="1.2.0",
                input_tokens=100, output_tokens=50, usd=0.01,
            )
            store.write(r)
        receipts = store.list_all()
        rollup = roll_up_by_phase(receipts)
        assert "P5" in rollup
        assert rollup["P5"]["count"] == 3
        assert abs(rollup[("P5")]["usd"] - 0.03) < 1e-9


def test_roll_up_by_day() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        store, mem_dir = _make_test_env(td)
        r = make_receipt(
            phase="P0", model_name="m", reasoning_effort="default",
            prompt="p", memory_snapshot_dir=mem_dir,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
            usd=0.05,
        )
        store.write(r)
        receipts = store.list_all()
        rollup = roll_up_by_day(receipts)
        assert len(rollup) == 1
        day_key = list(rollup.keys())[0]
        assert abs(rollup[day_key]["usd"] - 0.05) < 1e-9


def test_content_hash_is_deterministic() -> None:
    """The same Receipt object hashed twice yields the same hash."""
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        _, mem_dir = _make_test_env(td)
        r = make_receipt(
            phase="P0", model_name="m", reasoning_effort="default",
            prompt="p", memory_snapshot_dir=mem_dir,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
        )
        h1 = r.content_hash()
        h2 = r.content_hash()
        assert h1 == h2
        assert h1.startswith("sha256:")


def test_round_trip_preserves_receipt() -> None:
    """write -> list_all -> compare gives back an equivalent Receipt."""
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        store, mem_dir = _make_test_env(td)
        r = make_receipt(
            phase="P5", model_name="claude-opus-4-7", reasoning_effort="high",
            prompt="implementation prompt", memory_snapshot_dir=mem_dir,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=["default-web-saas", "vibe-defense"], constitution_version="1.2.0",
            input_tokens=2500, output_tokens=900, usd=0.075,
        )
        store.write(r)
        loaded = store.list_all()[0]
        assert loaded.content_hash() == r.content_hash()
        assert loaded.doctrine == ["default-web-saas", "vibe-defense"]
        assert loaded.cost.usd == 0.075


def _run_all() -> int:
    """Direct-execution runner for environments without pytest."""
    tests = [
        test_emit_and_list,
        test_chain_validation_valid,
        test_chain_validation_missing_parent,
        test_replay_check_pass,
        test_replay_check_tampered_prompt,
        test_roll_up_by_session,
        test_roll_up_by_phase,
        test_roll_up_by_day,
        test_content_hash_is_deterministic,
        test_round_trip_preserves_receipt,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            failures += 1
    print(f"\n{len(tests) - failures}/{len(tests)} tests passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(_run_all())
