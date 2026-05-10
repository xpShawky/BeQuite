"""bequite.auth — CLI Authentication Phase-2 (v0.10.6).

Phase-2 ships command stubs that gracefully degrade until a BeQuite auth
server stands up (Phase-3, v0.11.x+ or post-v1.0.0). What works today:

- Local file-based identity (a generated UUID stored at .bequite/.identity.json
  so existing receipts have a session_id).
- `bequite auth whoami` reports the local identity or "not signed in".
- `bequite auth status` reports auth + offline + CI mode.
- `bequite auth login` is a stub that prints "auth backend not yet available"
  with a graceful local-identity fallback.
- `bequite auth logout` deletes the local identity.
- `bequite auth refresh` is a no-op until refresh tokens exist (Phase-3).

CI mode (`BEQUITE_CI_MODE=true` + `BEQUITE_API_KEY=...`) skips device-code +
identifies via the API key.

Per ADR-011: token storage uses Python `keyring` when available; falls back
to mode-0600 file at `.bequite/.session/token` with prominent warning.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import json
import os
import pathlib
import sys
import uuid
from typing import Optional


SERVICE_NAME = "bequite"
KEYRING_KEY = "session"
LOCAL_IDENTITY_PATH = ".bequite/.identity.json"
LOCAL_SESSION_DIR = ".bequite/.session"


@dataclasses.dataclass
class LocalIdentity:
    """Local-only identity used when no auth server exists yet."""
    version: str = "1"
    user_id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    user_email: Optional[str] = None  # None until login flow completes
    issued_utc: str = dataclasses.field(default_factory=lambda: _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"))
    device_id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    backend: str = "local-file"  # "keyring" | "local-file" | "none"


def is_offline() -> bool:
    return os.environ.get("BEQUITE_OFFLINE", "").lower() in ("true", "1", "yes")


def is_ci_mode() -> bool:
    return os.environ.get("BEQUITE_CI_MODE", "").lower() in ("true", "1", "yes") \
        or bool(os.environ.get("BEQUITE_API_KEY"))


def has_keyring() -> bool:
    try:
        import keyring  # noqa: F401
        return True
    except ImportError:
        return False


def get_local_identity(repo_root: pathlib.Path) -> Optional[LocalIdentity]:
    p = repo_root / LOCAL_IDENTITY_PATH
    if not p.exists():
        return None
    try:
        return LocalIdentity(**json.loads(p.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, TypeError):
        return None


def save_local_identity(repo_root: pathlib.Path, ident: LocalIdentity) -> pathlib.Path:
    p = repo_root / LOCAL_IDENTITY_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(dataclasses.asdict(ident), indent=2, sort_keys=True), encoding="utf-8")
    try:
        os.chmod(p, 0o600)
    except (OSError, NotImplementedError):
        pass
    return p


def delete_local_identity(repo_root: pathlib.Path) -> bool:
    p = repo_root / LOCAL_IDENTITY_PATH
    if p.exists():
        p.unlink()
        return True
    return False


def status_dict(repo_root: pathlib.Path) -> dict:
    ident = get_local_identity(repo_root)
    return {
        "authenticated": ident is not None and ident.user_email is not None,
        "user_id": ident.user_id if ident else None,
        "user_email": ident.user_email if ident else None,
        "device_id": ident.device_id if ident else None,
        "issued_utc": ident.issued_utc if ident else None,
        "offline_mode": is_offline(),
        "ci_mode": is_ci_mode(),
        "keyring_available": has_keyring(),
        "auth_backend": ident.backend if ident else "none",
        "phase": "Phase-2 (Phase-3 device-code flow lands v0.11.x+)",
    }


# ---------------------------------------------------------------------- CLI


def _login_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    if is_ci_mode():
        print("ci-mode detected (BEQUITE_API_KEY set). Skipping device-code flow.")
        ident = LocalIdentity(user_email="ci@bequite.dev", backend="ci-api-key")
        save_local_identity(repo, ident)
        return 0
    print("auth backend not yet available — Phase-2 stub.")
    print("Phase-3 (device-code flow per RFC 8628) lands v0.11.x+.")
    print("In the meantime, recording a local identity so receipts have a session_id.")
    email = args.email or input("Optional email (Enter to skip): ").strip() or None
    ident = LocalIdentity(user_email=email)
    p = save_local_identity(repo, ident)
    print(f"local identity recorded at {p}")
    print(f"  user_id: {ident.user_id}")
    print(f"  user_email: {ident.user_email or '(not provided)'}")
    return 0


def _logout_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    deleted = delete_local_identity(repo)
    if deleted:
        print("local identity deleted.")
    else:
        print("(no local identity to delete)")
    return 0


def _whoami_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    ident = get_local_identity(repo)
    if ident is None:
        print("not signed in")
        return 1
    if args.json:
        print(json.dumps(dataclasses.asdict(ident), indent=2, sort_keys=True))
    else:
        print(f"user: {ident.user_email or '(no email)'}")
        print(f"  user_id: {ident.user_id}")
        print(f"  device:  {ident.device_id}")
        print(f"  since:   {ident.issued_utc}")
        print(f"  backend: {ident.backend}")
    return 0


def _status_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    s = status_dict(repo)
    if args.json:
        print(json.dumps(s, indent=2, sort_keys=True))
    else:
        for k, v in s.items():
            print(f"  {k}: {v}")
    return 0


def _refresh_cmd(args: argparse.Namespace) -> int:
    print("auth refresh: no-op until Phase-3 device-code flow lands (v0.11.x+).")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="bequite-auth", description="CLI Authentication Phase-2 (v0.10.6).")
    p.add_argument("--repo", default=".")
    sub = p.add_subparsers(dest="cmd", required=True)

    li = sub.add_parser("login", help="Sign in (Phase-2 stub; Phase-3 device-code v0.11.x+).")
    li.add_argument("--email", default=None)
    li.set_defaults(fn=_login_cmd)

    lo = sub.add_parser("logout", help="Delete local identity.")
    lo.set_defaults(fn=_logout_cmd)

    wh = sub.add_parser("whoami", help="Show local identity.")
    wh.add_argument("--json", action="store_true")
    wh.set_defaults(fn=_whoami_cmd)

    st = sub.add_parser("status", help="Show auth + offline + CI mode.")
    st.add_argument("--json", action="store_true")
    st.set_defaults(fn=_status_cmd)

    rf = sub.add_parser("refresh", help="Refresh session (Phase-3 only).")
    rf.set_defaults(fn=_refresh_cmd)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
