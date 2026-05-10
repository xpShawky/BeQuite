"""bequite receipts signing — ed25519 (v0.7.1).

Layered on top of the v0.7.0 receipts module. Generates a per-project keypair
on `bequite init`, signs each emitted receipt at write-time, and validates
signatures via `bequite verify-receipts`.

Key storage:
- Private key: `<project>/.bequite/.keys/private.pem`  — gitignored, mode 0600.
- Public key:  `<project>/.bequite/keys/public.pem`     — committed, world-readable.

Both PEM-encoded (PKCS8 / SubjectPublicKeyInfo). Per Article IV, the private
key never leaves the local project; per Iron Law III, the public key is
committed so any agent / human can validate receipts written by past runs.

Signature placement:
- Optional `signature` field on each Receipt. When present, value is base64-
  encoded ed25519 signature over the receipt's canonical-JSON encoding
  computed *with the signature field absent or null*.
- `sign_receipt(receipt, private_key)` returns a NEW Receipt-like dict with
  the `signature` field added.
- `verify_receipt(receipt, public_key)` recovers the signature, recomputes
  the canonical-JSON-without-signature, verifies. Returns (ok, reason).

Strict mode:
- `verify_receipts --strict`: every receipt MUST carry a valid signature.
- Without `--strict`: unsigned receipts pass (legacy v0.7.0 receipts do).

CLI surface (additions to bequite.receipts module):

    python -m bequite.receipts_signing keygen [--project .]
    python -m bequite.receipts_signing sign --in receipt.json --out signed-receipt.json
    python -m bequite.receipts_signing verify [--strict] [--project .]

Wired into the main CLI as:

    bequite init               # calls generate_keypair() if missing
    bequite verify-receipts [--strict]
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import sys
from typing import Any, Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


# Default key paths inside a BeQuite-managed project.
DEFAULT_PRIVATE_KEY = ".bequite/.keys/private.pem"
DEFAULT_PUBLIC_KEY = ".bequite/keys/public.pem"


# --------------------------------------------------------------------- keygen


def generate_keypair(
    project_dir: pathlib.Path,
    overwrite: bool = False,
) -> tuple[pathlib.Path, pathlib.Path]:
    """Generate a per-project ed25519 keypair if not already present.

    Returns (private_path, public_path). Raises FileExistsError if the
    private key file already exists and overwrite=False.

    Side-effects:
    - Creates `<project>/.bequite/.keys/` (mode 0700) and writes private key
      with mode 0600.
    - Creates `<project>/.bequite/keys/` (mode 0755) and writes public key
      with mode 0644.
    - Does NOT touch .gitignore here; caller is responsible (typically
      `bequite init` adds `.bequite/.keys/` to .gitignore on scaffold).

    The private key is PKCS8-encoded PEM, no passphrase. (For projects that
    require passphrase-protected keys, fork the BeQuite Doctrine and override
    this function — most BeQuite usage keeps keys local-only behind project
    permissions, so adding a passphrase mostly trades convenience for marginal
    additional protection.)
    """
    priv_path = project_dir / DEFAULT_PRIVATE_KEY
    pub_path = project_dir / DEFAULT_PUBLIC_KEY

    if priv_path.exists() and not overwrite:
        raise FileExistsError(
            f"Private key already exists at {priv_path}. "
            "Use overwrite=True to regenerate (this WILL invalidate previous receipt signatures)."
        )

    priv_path.parent.mkdir(parents=True, exist_ok=True)
    pub_path.parent.mkdir(parents=True, exist_ok=True)

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    priv_path.write_bytes(priv_pem)
    pub_path.write_bytes(pub_pem)

    # Restrict private-key file permissions on POSIX. On Windows, NTFS perms
    # are inherited from the directory; users running on Windows are advised
    # in BeQuite docs to keep .bequite/.keys/ inside an OS-protected folder.
    try:
        os.chmod(priv_path, 0o600)
        os.chmod(pub_path, 0o644)
    except (OSError, NotImplementedError):
        pass  # Best-effort on Windows.

    return (priv_path, pub_path)


def load_private_key(path: pathlib.Path) -> Ed25519PrivateKey:
    pem = path.read_bytes()
    key = serialization.load_pem_private_key(pem, password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError(f"Expected Ed25519PrivateKey at {path}, got {type(key).__name__}")
    return key


def load_public_key(path: pathlib.Path) -> Ed25519PublicKey:
    pem = path.read_bytes()
    key = serialization.load_pem_public_key(pem)
    if not isinstance(key, Ed25519PublicKey):
        raise TypeError(f"Expected Ed25519PublicKey at {path}, got {type(key).__name__}")
    return key


# --------------------------------------------------------------------- sign / verify


def _canonical_payload_for_signing(receipt_dict: dict[str, Any]) -> bytes:
    """Canonical bytes used for signing — the receipt with `signature` removed.

    Producing the signing payload by stripping the field rather than rebuilding
    the dict ensures any future-additive fields are included. Sorted keys + no
    whitespace.
    """
    d = {k: v for k, v in receipt_dict.items() if k != "signature"}
    return json.dumps(d, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign_dict(receipt_dict: dict[str, Any], private_key: Ed25519PrivateKey) -> dict[str, Any]:
    """Return a copy of receipt_dict with `signature` (base64-ed25519) added."""
    payload = _canonical_payload_for_signing(receipt_dict)
    sig = private_key.sign(payload)
    out = dict(receipt_dict)
    out["signature"] = base64.b64encode(sig).decode("ascii")
    return out


def verify_dict(receipt_dict: dict[str, Any], public_key: Ed25519PublicKey) -> tuple[bool, str]:
    """Verify a signed-receipt dict. Returns (ok, reason)."""
    sig_b64 = receipt_dict.get("signature")
    if not sig_b64:
        return (False, "no signature on receipt")
    try:
        sig = base64.b64decode(sig_b64)
    except (ValueError, TypeError) as e:
        return (False, f"signature is not valid base64: {e}")
    payload = _canonical_payload_for_signing(receipt_dict)
    try:
        public_key.verify(sig, payload)
        return (True, "valid")
    except InvalidSignature:
        return (False, "signature does not match payload (tampered or wrong key)")


# --------------------------------------------------------------------- store walk


def verify_receipts_directory(
    receipts_dir: pathlib.Path,
    public_key: Ed25519PublicKey,
    strict: bool,
) -> tuple[bool, list[str], dict[str, int]]:
    """Walk every receipt JSON in receipts_dir; verify each.

    Returns (ok, issues, counts).
    counts has keys: total, signed_valid, signed_invalid, unsigned.

    In strict mode, unsigned receipts contribute to issues. In non-strict
    mode they're tolerated (counted but not failed).
    """
    issues: list[str] = []
    counts = {"total": 0, "signed_valid": 0, "signed_invalid": 0, "unsigned": 0}

    if not receipts_dir.exists():
        return (True, [f"(no receipts dir at {receipts_dir})"], counts)

    for f in sorted(receipts_dir.glob("*.json")):
        counts["total"] += 1
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            issues.append(f"{f.name}: malformed JSON ({e})")
            counts["signed_invalid"] += 1
            continue

        if "signature" not in d or not d["signature"]:
            counts["unsigned"] += 1
            if strict:
                issues.append(f"{f.name}: unsigned receipt (strict mode)")
            continue

        ok, reason = verify_dict(d, public_key)
        if ok:
            counts["signed_valid"] += 1
        else:
            counts["signed_invalid"] += 1
            issues.append(f"{f.name}: signature INVALID ({reason})")

    return (len(issues) == 0, issues, counts)


# --------------------------------------------------------------------- CLI


def _keygen_cmd(args: argparse.Namespace) -> int:
    project = pathlib.Path(args.project).resolve()
    try:
        priv, pub = generate_keypair(project, overwrite=args.overwrite)
    except FileExistsError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(f"generated keypair:")
    print(f"  private: {priv}  (chmod 0600)")
    print(f"  public:  {pub}   (chmod 0644)")
    print("")
    print("Reminders:")
    print(f"  - Add '.bequite/.keys/' to .gitignore (private key MUST NEVER be committed).")
    print(f"  - Commit '.bequite/keys/public.pem' so receipt signatures can be validated by future agents.")
    return 0


def _sign_cmd(args: argparse.Namespace) -> int:
    in_path = pathlib.Path(args.input)
    out_path = pathlib.Path(args.output) if args.output else in_path
    receipt = json.loads(in_path.read_text(encoding="utf-8"))
    priv = load_private_key(pathlib.Path(args.private_key))
    signed = sign_dict(receipt, priv)
    out_path.write_text(json.dumps(signed, indent=2, sort_keys=True), encoding="utf-8")
    print(f"signed → {out_path}")
    return 0


def _verify_cmd(args: argparse.Namespace) -> int:
    project = pathlib.Path(args.project).resolve()
    receipts_dir = project / ".bequite" / "receipts"
    pub_path = project / DEFAULT_PUBLIC_KEY
    if not pub_path.exists():
        print(f"error: no public key at {pub_path}. Run `bequite init` or `python -m bequite.receipts_signing keygen` first.", file=sys.stderr)
        return 2
    pub = load_public_key(pub_path)
    ok, issues, counts = verify_receipts_directory(receipts_dir, pub, strict=args.strict)
    print(f"receipts verified: total={counts['total']} signed_valid={counts['signed_valid']} signed_invalid={counts['signed_invalid']} unsigned={counts['unsigned']}")
    if issues:
        for i in issues:
            print(f"  ! {i}", file=sys.stderr)
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="bequite-receipts-signing", description="Ed25519 signing for BeQuite receipts (v0.7.1).")
    sub = p.add_subparsers(dest="cmd", required=True)

    kg = sub.add_parser("keygen", help="Generate a per-project ed25519 keypair.")
    kg.add_argument("--project", default=".")
    kg.add_argument("--overwrite", action="store_true", help="Regenerate even if a keypair exists. WILL invalidate previous signatures.")
    kg.set_defaults(fn=_keygen_cmd)

    sg = sub.add_parser("sign", help="Sign a single receipt JSON.")
    sg.add_argument("--input", required=True)
    sg.add_argument("--output", default=None)
    sg.add_argument("--private-key", default=DEFAULT_PRIVATE_KEY)
    sg.set_defaults(fn=_sign_cmd)

    vf = sub.add_parser("verify", help="Verify all receipts in a project.")
    vf.add_argument("--project", default=".")
    vf.add_argument("--strict", action="store_true", help="Fail on unsigned receipts.")
    vf.set_defaults(fn=_verify_cmd)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
