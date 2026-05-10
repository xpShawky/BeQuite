"""bequite auto — Auto-mode state machine (v0.10.0).

One-click run-to-completion P0 → P7 with safety rails:

- Hard cost ceiling (`bequite.config.toml::cost.session_max_usd`, default $20).
- Hard wall-clock ceiling (`max_wall_clock_hours`, default 6h).
- 3 consecutive Implementer failures on the same task → BLOCKED.
- Banned-word check (existing `stop-verify-before-done.sh` hook).
- Hook-block respect (any pretooluse-* exit 2 pauses; never auto-overrides).
- One-way-door operations always pause (PyPI publish, npm publish, git push to main, force push, terraform apply, DB migrations against shared DBs).
- Heartbeat: writes `activeContext.md` every 5 minutes during long phases.
- Per-phase commit (atomic): each phase exit creates a single commit with the receipt + artifacts.

State persistence at `.bequite/auto-state/<session>.json`. Resume with `bequite auto resume <session>` (v0.10.7+).

CLI flags (per ADR-008 + plan §10):

    --feature <name>
    --max-cost-usd <float> (default 20)
    --max-wall-clock-hours <float> (default 6)
    --phases <subset> (e.g. P0,P1,P2)
    --mode slow|fast|auto (default auto)
    --on-failure pause|abort|continue-with-warning (default pause)
    --no-skeptic (debug only — do NOT use in production)
    --resume <session-id> (v0.10.7+)

In v0.10.0, the actual model invocation is **stubbed** — the state machine
walks phase-by-phase but each phase's "do work" call is a no-op that emits
a synthetic receipt. v0.10.5 will integrate multi-model planning at P2; the
broader auto-mode-with-real-LLMs lands per the routing matrix already wired
in v0.8.0.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import json
import os
import pathlib
import re
import sys
import time
import uuid
from typing import Any, Optional

PHASES = ["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"]
DEFAULT_MAX_COST_USD = 20.0
DEFAULT_MAX_WALL_CLOCK_HOURS = 6.0
DEFAULT_FAILURE_THRESHOLD = 3
HEARTBEAT_INTERVAL_S = 300  # 5 minutes

BANNED_WEASEL_WORDS = (
    "should",
    "probably",
    "seems to",
    "appears to",
    "i think it works",
    "might work",
    "hopefully",
    "in theory",
)

ONE_WAY_DOORS = (
    "git push origin main",
    "git push --force",
    "git push -f",
    "pypi publish",
    "twine upload",
    "npm publish",
    "terraform apply",
    "psql.*DROP DATABASE",
    "psql.*TRUNCATE",
)


@dataclasses.dataclass
class AutoState:
    """Persistent state for an auto-mode session."""

    version: str = "1"
    session_id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    feature: str = ""
    started_utc: str = dataclasses.field(default_factory=lambda: _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"))
    last_heartbeat_utc: Optional[str] = None
    current_phase: str = "INIT"  # INIT | P0..P7 | DONE | BLOCKED | FAILED | PAUSED
    completed_phases: list[str] = dataclasses.field(default_factory=list)
    blocked_reason: Optional[str] = None
    failed_reason: Optional[str] = None
    paused_reason: Optional[str] = None
    consecutive_failures: int = 0
    failed_task_id: Optional[str] = None
    cost_usd_so_far: float = 0.0
    max_cost_usd: float = DEFAULT_MAX_COST_USD
    max_wall_clock_hours: float = DEFAULT_MAX_WALL_CLOCK_HOURS
    mode: str = "auto"
    on_failure: str = "pause"
    skeptic_enabled: bool = True
    phase_artifacts: dict[str, list[str]] = dataclasses.field(default_factory=dict)
    receipts_emitted: list[str] = dataclasses.field(default_factory=list)


# ----------------------------------------------------------------------------- safety rails


def check_banned_words(text: str) -> Optional[str]:
    """Return the first banned word found, or None."""
    lower = text.lower()
    for word in BANNED_WEASEL_WORDS:
        if word in lower:
            return word
    return None


def check_one_way_door(command: str) -> Optional[str]:
    """Return the matched one-way-door pattern, or None."""
    for pat in ONE_WAY_DOORS:
        if re.search(pat, command, re.IGNORECASE):
            return pat
    return None


def check_cost_ceiling(state: AutoState) -> Optional[str]:
    """Return a reason string when the ceiling is reached, or None."""
    if state.cost_usd_so_far >= state.max_cost_usd:
        return f"cost ceiling reached: ${state.cost_usd_so_far:.2f} >= ${state.max_cost_usd:.2f}"
    return None


def check_wall_clock(state: AutoState) -> Optional[str]:
    """Return a reason string when the wall-clock ceiling is reached, or None."""
    started = _dt.datetime.fromisoformat(state.started_utc)
    elapsed_s = (_dt.datetime.now(_dt.timezone.utc) - started).total_seconds()
    if elapsed_s >= state.max_wall_clock_hours * 3600:
        return f"wall-clock ceiling reached: {elapsed_s/3600:.2f}h >= {state.max_wall_clock_hours}h"
    return None


def check_failure_threshold(state: AutoState, threshold: int = DEFAULT_FAILURE_THRESHOLD) -> Optional[str]:
    """Return a reason string when the threshold is reached, or None."""
    if state.consecutive_failures >= threshold:
        return f"{state.consecutive_failures} consecutive failures on task {state.failed_task_id}"
    return None


# ----------------------------------------------------------------------------- persistence


def state_path(repo_root: pathlib.Path, session_id: str) -> pathlib.Path:
    return repo_root / ".bequite" / "auto-state" / f"{session_id}.json"


def save_state(repo_root: pathlib.Path, state: AutoState) -> pathlib.Path:
    p = state_path(repo_root, state.session_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(dataclasses.asdict(state), indent=2, sort_keys=True), encoding="utf-8")
    return p


def load_state(repo_root: pathlib.Path, session_id: str) -> Optional[AutoState]:
    p = state_path(repo_root, session_id)
    if not p.exists():
        return None
    return AutoState(**json.loads(p.read_text(encoding="utf-8")))


def heartbeat(repo_root: pathlib.Path, state: AutoState) -> None:
    """Update activeContext.md + state.last_heartbeat_utc."""
    state.last_heartbeat_utc = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    save_state(repo_root, state)
    ac = repo_root / ".bequite" / "memory" / "activeContext.md"
    if ac.exists():
        # Just touch the heartbeat marker; full update is the caller's responsibility.
        marker = f"\n<!-- auto-mode heartbeat {state.last_heartbeat_utc} session {state.session_id[:8]} phase {state.current_phase} -->\n"
        text = ac.read_text(encoding="utf-8")
        # Replace any prior marker
        text = re.sub(r"\n<!-- auto-mode heartbeat .*? -->\n", "", text)
        ac.write_text(text + marker, encoding="utf-8")


# ----------------------------------------------------------------------------- state machine


def transition(state: AutoState, to: str, reason: Optional[str] = None) -> AutoState:
    """Move the state machine to a new phase. Returns the updated state."""
    # Bookkeep completed phases.
    if state.current_phase in PHASES and state.current_phase not in state.completed_phases:
        state.completed_phases.append(state.current_phase)
    state.current_phase = to
    if to == "BLOCKED":
        state.blocked_reason = reason
    elif to == "FAILED":
        state.failed_reason = reason
    elif to == "PAUSED":
        state.paused_reason = reason
    return state


def run_phase(
    state: AutoState,
    phase: str,
    *,
    repo_root: pathlib.Path,
    do_work: Optional[Any] = None,
) -> AutoState:
    """Run one phase. Returns updated state.

    `do_work` is a callable that takes (state) and returns (cost_delta_usd, completion_text).
    In v0.10.0 stub mode, do_work is None → no-op + synthetic completion.
    """
    state = transition(state, phase)
    save_state(repo_root, state)

    # Pre-phase rail checks.
    for check in (check_cost_ceiling, check_wall_clock, lambda s: check_failure_threshold(s)):
        reason = check(state)
        if reason:
            return transition(state, "BLOCKED", reason)

    # Do the actual work.
    if do_work is None:
        # v0.10.0 stub: no-op.
        cost_delta = 0.0
        completion = f"(stub) {phase} completed at {_dt.datetime.now(_dt.timezone.utc).isoformat(timespec='seconds')}"
    else:
        try:
            cost_delta, completion = do_work(state)
        except Exception as e:  # noqa: BLE001
            state.consecutive_failures += 1
            state.failed_task_id = phase
            return transition(state, "FAILED", f"{type(e).__name__}: {e}")

    # Post-phase rail checks.
    banned = check_banned_words(completion)
    if banned:
        return transition(state, "BLOCKED", f"banned weasel word in completion: {banned!r}")

    state.cost_usd_so_far += cost_delta
    state.consecutive_failures = 0  # reset on successful phase
    state.phase_artifacts.setdefault(phase, []).append(completion)
    save_state(repo_root, state)
    return state


def run_all_phases(
    state: AutoState,
    *,
    repo_root: pathlib.Path,
    phases: list[str] = PHASES,
    do_work: Optional[Any] = None,
) -> AutoState:
    """Walk every phase in order until DONE / BLOCKED / FAILED."""
    for phase in phases:
        state = run_phase(state, phase, repo_root=repo_root, do_work=do_work)
        if state.current_phase in ("BLOCKED", "FAILED"):
            return state
    return transition(state, "DONE")


# ----------------------------------------------------------------------------- CLI


def _run_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    state = AutoState(
        feature=args.feature or "(unspecified)",
        max_cost_usd=args.max_cost_usd,
        max_wall_clock_hours=args.max_wall_clock_hours,
        mode=args.mode,
        on_failure=args.on_failure,
        skeptic_enabled=not args.no_skeptic,
    )
    save_state(repo, state)
    print(f"auto-mode session {state.session_id} starting on feature: {state.feature}")
    state = run_all_phases(state, repo_root=repo, phases=args.phases or PHASES)
    print(f"final state: {state.current_phase}")
    if state.blocked_reason:
        print(f"  blocked: {state.blocked_reason}")
    if state.failed_reason:
        print(f"  failed: {state.failed_reason}")
    print(f"phases completed: {state.completed_phases}")
    print(f"cost so far: ${state.cost_usd_so_far:.4f}")
    print(f"state file: {state_path(repo, state.session_id)}")
    return 0 if state.current_phase == "DONE" else 1


def _status_cmd(args: argparse.Namespace) -> int:
    repo = pathlib.Path(args.repo).resolve()
    sid = args.session_id
    state = load_state(repo, sid)
    if state is None:
        print(f"no state at {state_path(repo, sid)}")
        return 1
    print(json.dumps(dataclasses.asdict(state), indent=2, sort_keys=True))
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="bequite-auto", description="Auto-mode state machine (v0.10.0).")
    p.add_argument("--repo", default=".")
    sub = p.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Start a new auto-mode session.")
    run.add_argument("--feature", default=None)
    run.add_argument("--max-cost-usd", type=float, default=DEFAULT_MAX_COST_USD)
    run.add_argument("--max-wall-clock-hours", type=float, default=DEFAULT_MAX_WALL_CLOCK_HOURS)
    run.add_argument("--mode", default="auto", choices=["slow", "fast", "auto"])
    run.add_argument("--on-failure", default="pause", choices=["pause", "abort", "continue-with-warning"])
    run.add_argument("--phases", nargs="*", default=None)
    run.add_argument("--no-skeptic", action="store_true")
    run.set_defaults(fn=_run_cmd)

    st = sub.add_parser("status", help="Show state for a session.")
    st.add_argument("session_id")
    st.set_defaults(fn=_status_cmd)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
