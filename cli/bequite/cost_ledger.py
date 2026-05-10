"""bequite.cost_ledger — feeds .bequite/cache/cost-ledger.json (v0.8.0).

The `stop-cost-budget.sh` hook reads this file to enforce the session
ceiling. Per the hook's contract:

    .bequite/cache/cost-ledger.json:
      {
        "session_total_usd":    <float>,
        "session_total_tokens": <int>,
        "session_started_utc":  <ISO 8601>,
        "last_updated_utc":     <ISO 8601>,
        "calls": [
          {"timestamp_utc": ..., "phase": ..., "persona": ...,
           "provider": ..., "model": ..., "input_tokens": ...,
           "output_tokens": ..., "usd": ...},
          ...
        ]
      }

The ledger is project-local; it resets per session (when `session_started_utc`
diverges from the active session). Receipts are the durable persistence;
the ledger is a fast roll-up cache.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import pathlib
import uuid
from typing import Optional

from bequite.providers import Completion


DEFAULT_LEDGER_PATH = ".bequite/cache/cost-ledger.json"


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def _session_id() -> str:
    """Per-process session id; persists across multiple dispatch() calls in a single CLI run."""
    sid = os.environ.get("BEQUITE_SESSION_ID")
    if sid:
        return sid
    sid = str(uuid.uuid4())
    os.environ["BEQUITE_SESSION_ID"] = sid
    return sid


def update(
    *,
    repo_root: pathlib.Path,
    completion: Completion,
    phase: str,
    persona: str,
    ledger_path: Optional[pathlib.Path] = None,
) -> pathlib.Path:
    """Append a call to the ledger; refresh totals."""
    if ledger_path is None:
        ledger_path = repo_root / DEFAULT_LEDGER_PATH
    ledger_path.parent.mkdir(parents=True, exist_ok=True)

    sid = _session_id()
    now = _now_iso()

    if ledger_path.exists():
        try:
            data = json.loads(ledger_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    # If session id changed, reset session totals (but keep `calls` history).
    current_sid = data.get("session_id")
    if current_sid != sid:
        data["session_id"] = sid
        data["session_started_utc"] = now
        data["session_total_usd"] = 0.0
        data["session_total_tokens"] = 0
        data["calls_this_session"] = 0

    data.setdefault("calls", [])
    data["calls"].append({
        "timestamp_utc": now,
        "session_id": sid,
        "phase": phase,
        "persona": persona,
        "provider": completion.provider,
        "model": completion.model,
        "input_tokens": completion.input_tokens,
        "output_tokens": completion.output_tokens,
        "usd": completion.usd_cost,
        "finish_reason": completion.finish_reason,
        "error": completion.error,
    })

    data["session_total_usd"] = float(data.get("session_total_usd", 0.0)) + float(completion.usd_cost)
    data["session_total_tokens"] = int(data.get("session_total_tokens", 0)) + completion.input_tokens + completion.output_tokens
    data["calls_this_session"] = int(data.get("calls_this_session", 0)) + 1
    data["last_updated_utc"] = now

    ledger_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return ledger_path


def read(repo_root: pathlib.Path, ledger_path: Optional[pathlib.Path] = None) -> dict:
    """Read the current ledger; return empty dict if absent."""
    if ledger_path is None:
        ledger_path = repo_root / DEFAULT_LEDGER_PATH
    if not ledger_path.exists():
        return {}
    try:
        return json.loads(ledger_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def session_summary(repo_root: pathlib.Path, ledger_path: Optional[pathlib.Path] = None) -> dict:
    """One-screen summary of the current session's spend."""
    data = read(repo_root, ledger_path)
    return {
        "session_id": data.get("session_id"),
        "session_started_utc": data.get("session_started_utc"),
        "last_updated_utc": data.get("last_updated_utc"),
        "session_total_usd": data.get("session_total_usd", 0.0),
        "session_total_tokens": data.get("session_total_tokens", 0),
        "calls_this_session": data.get("calls_this_session", 0),
    }


def reset_session(repo_root: pathlib.Path, ledger_path: Optional[pathlib.Path] = None) -> None:
    """Reset just the session totals (keeps `calls` history)."""
    if ledger_path is None:
        ledger_path = repo_root / DEFAULT_LEDGER_PATH
    if not ledger_path.exists():
        return
    try:
        data = json.loads(ledger_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    data["session_id"] = str(uuid.uuid4())
    data["session_started_utc"] = _now_iso()
    data["session_total_usd"] = 0.0
    data["session_total_tokens"] = 0
    data["calls_this_session"] = 0
    ledger_path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
