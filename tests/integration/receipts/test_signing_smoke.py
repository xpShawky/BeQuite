"""Integration smoke test for cli/bequite/receipts_signing.py (BeQuite v0.7.1).

Runnable two ways:
    1. Direct: `PYTHONIOENCODING=utf-8 python tests/integration/receipts/test_signing_smoke.py`
    2. Pytest: `PYTHONIOENCODING=utf-8 python -m pytest tests/integration/receipts/test_signing_smoke.py`

Tests the ed25519 sign + verify primitives, keypair generation, and
the strict-vs-lenient verify modes.
"""

from __future__ import annotations

import json
import pathlib
import sys
import tempfile

# Make `bequite` importable from cli/ when run directly.
_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "cli"))

from bequite.receipts import make_receipt, ReceiptStore  # noqa: E402
from bequite.receipts_signing import (  # noqa: E402
    generate_keypair,
    load_private_key,
    load_public_key,
    sign_dict,
    verify_dict,
    verify_receipts_directory,
)


def _setup_project(td: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    """Build a fake project tree: project / mem / receipts dir."""
    project = td / "demo"
    project.mkdir()
    receipts_dir = project / ".bequite" / "receipts"
    receipts_dir.mkdir(parents=True)
    mem = project / "mem"
    mem.mkdir()
    (mem / "constitution.md").write_text("# Iron Laws v1.2.0", encoding="utf-8")
    return project, mem, receipts_dir


def test_keygen_creates_files() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        project, _, _ = _setup_project(td)
        priv, pub = generate_keypair(project)
        assert priv.exists()
        assert pub.exists()
        assert priv.read_bytes().startswith(b"-----BEGIN PRIVATE KEY-----")
        assert pub.read_bytes().startswith(b"-----BEGIN PUBLIC KEY-----")


def test_keygen_refuses_overwrite_by_default() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        project, _, _ = _setup_project(td)
        generate_keypair(project)
        try:
            generate_keypair(project)
        except FileExistsError:
            return
        raise AssertionError("expected FileExistsError on second keygen without overwrite=True")


def test_keygen_overwrites_when_explicit() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        project, _, _ = _setup_project(td)
        priv1, pub1 = generate_keypair(project)
        first_priv = priv1.read_bytes()
        priv2, pub2 = generate_keypair(project, overwrite=True)
        assert priv2.read_bytes() != first_priv  # New key generated.


def test_sign_and_verify_roundtrip() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        project, mem, _ = _setup_project(td)
        priv_path, pub_path = generate_keypair(project)
        priv = load_private_key(priv_path)
        pub = load_public_key(pub_path)

        r = make_receipt(
            phase="P5", model_name="m", reasoning_effort="high",
            prompt="t", memory_snapshot_dir=mem,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
        )
        d = r.to_canonical_dict()
        signed = sign_dict(d, priv)
        assert "signature" in signed
        ok, reason = verify_dict(signed, pub)
        assert ok, reason


def test_tampered_body_rejected() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        project, mem, _ = _setup_project(td)
        priv_path, pub_path = generate_keypair(project)
        priv = load_private_key(priv_path)
        pub = load_public_key(pub_path)

        r = make_receipt(
            phase="P5", model_name="m", reasoning_effort="high",
            prompt="t", memory_snapshot_dir=mem,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
            input_tokens=100, output_tokens=50, usd=0.01,
        )
        d = r.to_canonical_dict()
        signed = sign_dict(d, priv)
        # Tamper: bump usd from 0.01 to 99.0.
        tampered = dict(signed)
        tampered["cost"] = {"input_tokens": 999, "output_tokens": 99, "usd": 99.0}
        ok, reason = verify_dict(tampered, pub)
        assert not ok
        assert "tampered" in reason.lower() or "does not match" in reason.lower()


def test_unsigned_receipt_strict_mode_fails() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        project, mem, receipts_dir = _setup_project(td)
        priv_path, pub_path = generate_keypair(project)
        pub = load_public_key(pub_path)

        # Write an UNSIGNED receipt directly.
        r = make_receipt(
            phase="P0", model_name="m", reasoning_effort="default",
            prompt="t", memory_snapshot_dir=mem,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
        )
        store = ReceiptStore(str(receipts_dir))
        store.write(r)  # no sign_with → unsigned

        ok, issues, counts = verify_receipts_directory(receipts_dir, pub, strict=True)
        assert not ok
        assert counts["unsigned"] == 1
        assert any("unsigned" in i for i in issues)


def test_unsigned_receipt_lenient_mode_tolerated() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        project, mem, receipts_dir = _setup_project(td)
        _, pub_path = generate_keypair(project)
        pub = load_public_key(pub_path)

        r = make_receipt(
            phase="P0", model_name="m", reasoning_effort="default",
            prompt="t", memory_snapshot_dir=mem,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
        )
        store = ReceiptStore(str(receipts_dir))
        store.write(r)

        ok, issues, counts = verify_receipts_directory(receipts_dir, pub, strict=False)
        assert ok, f"non-strict should tolerate unsigned: {issues}"
        assert counts["unsigned"] == 1


def test_store_write_with_signing_emits_signed_receipt() -> None:
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        project, mem, receipts_dir = _setup_project(td)
        priv_path, pub_path = generate_keypair(project)
        priv = load_private_key(priv_path)
        pub = load_public_key(pub_path)

        r = make_receipt(
            phase="P5", model_name="m", reasoning_effort="high",
            prompt="t", memory_snapshot_dir=mem,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
        )
        store = ReceiptStore(str(receipts_dir))
        target = store.write(r, sign_with=priv)
        # File on disk must include `signature` field.
        d = json.loads(target.read_text(encoding="utf-8"))
        assert "signature" in d
        ok, _ = verify_dict(d, pub)
        assert ok


def test_signature_matches_canonical_payload_excluding_signature() -> None:
    """Sanity: verifying with a signature field that doesn't match the receipt fails."""
    with tempfile.TemporaryDirectory() as td_str:
        td = pathlib.Path(td_str)
        project, mem, _ = _setup_project(td)
        priv_path, pub_path = generate_keypair(project)
        priv = load_private_key(priv_path)
        pub = load_public_key(pub_path)

        r1 = make_receipt(
            phase="P0", model_name="m", reasoning_effort="default",
            prompt="prompt-A", memory_snapshot_dir=mem,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
        )
        r2 = make_receipt(
            phase="P0", model_name="m", reasoning_effort="default",
            prompt="prompt-B", memory_snapshot_dir=mem,
            diff_from="HEAD", diff_to="HEAD",
            doctrines=[], constitution_version="1.2.0",
        )
        d1 = r1.to_canonical_dict()
        d2 = r2.to_canonical_dict()
        signed1 = sign_dict(d1, priv)
        # Cross-paste signature1 onto d2 (mismatch).
        d2["signature"] = signed1["signature"]
        ok, _ = verify_dict(d2, pub)
        assert not ok


def _run_all() -> int:
    tests = [
        test_keygen_creates_files,
        test_keygen_refuses_overwrite_by_default,
        test_keygen_overwrites_when_explicit,
        test_sign_and_verify_roundtrip,
        test_tampered_body_rejected,
        test_unsigned_receipt_strict_mode_fails,
        test_unsigned_receipt_lenient_mode_tolerated,
        test_store_write_with_signing_emits_signed_receipt,
        test_signature_matches_canonical_payload_excluding_signature,
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
