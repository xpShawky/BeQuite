"""Integration smoke test for cli/bequite/auth.py (BeQuite v0.10.6)."""

from __future__ import annotations

import json
import os
import pathlib
import sys
import tempfile

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))

from bequite.auth import (  # noqa: E402
    LocalIdentity,
    delete_local_identity,
    get_local_identity,
    is_ci_mode,
    is_offline,
    save_local_identity,
    status_dict,
)


def test_local_identity_roundtrips() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        ident = LocalIdentity(user_email="ahmed@example.com")
        p = save_local_identity(repo, ident)
        assert p.exists()
        loaded = get_local_identity(repo)
        assert loaded is not None
        assert loaded.user_email == "ahmed@example.com"
        assert loaded.user_id == ident.user_id


def test_get_local_identity_returns_none_when_absent() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        assert get_local_identity(repo) is None


def test_delete_local_identity() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        ident = LocalIdentity()
        save_local_identity(repo, ident)
        assert delete_local_identity(repo) is True
        assert delete_local_identity(repo) is False  # second call no-op


def test_status_dict_unauthenticated() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        s = status_dict(repo)
        assert s["authenticated"] is False
        assert s["user_email"] is None


def test_status_dict_authenticated() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = pathlib.Path(td)
        ident = LocalIdentity(user_email="x@y.com")
        save_local_identity(repo, ident)
        s = status_dict(repo)
        assert s["authenticated"] is True
        assert s["user_email"] == "x@y.com"


def test_offline_mode_via_env() -> None:
    saved = os.environ.get("BEQUITE_OFFLINE")
    try:
        os.environ["BEQUITE_OFFLINE"] = "true"
        assert is_offline() is True
        os.environ["BEQUITE_OFFLINE"] = "false"
        assert is_offline() is False
    finally:
        if saved is not None:
            os.environ["BEQUITE_OFFLINE"] = saved
        else:
            os.environ.pop("BEQUITE_OFFLINE", None)


def test_ci_mode_via_api_key() -> None:
    saved_key = os.environ.get("BEQUITE_API_KEY")
    saved_ci = os.environ.get("BEQUITE_CI_MODE")
    try:
        os.environ.pop("BEQUITE_API_KEY", None)
        os.environ.pop("BEQUITE_CI_MODE", None)
        assert is_ci_mode() is False
        os.environ["BEQUITE_API_KEY"] = "k"
        assert is_ci_mode() is True
    finally:
        if saved_key is not None:
            os.environ["BEQUITE_API_KEY"] = saved_key
        else:
            os.environ.pop("BEQUITE_API_KEY", None)
        if saved_ci is not None:
            os.environ["BEQUITE_CI_MODE"] = saved_ci
        else:
            os.environ.pop("BEQUITE_CI_MODE", None)


def test_local_identity_has_uuid() -> None:
    ident = LocalIdentity()
    assert len(ident.user_id) > 30  # UUID-shaped
    assert len(ident.device_id) > 30


def _run_all() -> int:
    tests = [
        test_local_identity_roundtrips,
        test_get_local_identity_returns_none_when_absent,
        test_delete_local_identity,
        test_status_dict_unauthenticated,
        test_status_dict_authenticated,
        test_offline_mode_via_env,
        test_ci_mode_via_api_key,
        test_local_identity_has_uuid,
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
