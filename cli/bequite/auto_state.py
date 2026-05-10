"""bequite.auto_state — Auto-mode hardening (v0.10.7).

Adds: resume from BLOCKED/PAUSED, parallel-task fan-out (per AkitaOnRails 2026
N>5 rule), idempotent rerun detection.
"""

from __future__ import annotations

import json
import pathlib
from typing import Optional

from bequite.auto import AutoState, load_state, save_state, state_path


def list_sessions(repo_root: pathlib.Path) -> list[dict]:
    """List every session in .bequite/auto-state/."""
    d = repo_root / ".bequite" / "auto-state"
    if not d.exists():
        return []
    out: list[dict] = []
    for p in sorted(d.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            out.append({
                "session_id": data.get("session_id"),
                "feature": data.get("feature"),
                "phase": data.get("current_phase"),
                "completed": data.get("completed_phases", []),
                "started_utc": data.get("started_utc"),
                "cost_usd": data.get("cost_usd_so_far", 0.0),
            })
        except (json.JSONDecodeError, OSError):
            continue
    return out


def can_resume(state: AutoState) -> tuple[bool, Optional[str]]:
    """Determine if a session is resumable. Returns (resumable, reason_if_not)."""
    if state.current_phase == "DONE":
        return (False, "session already DONE")
    if state.current_phase == "FAILED":
        return (False, f"session FAILED: {state.failed_reason or '(no reason recorded)'}")
    if state.current_phase in ("BLOCKED", "PAUSED"):
        return (True, None)
    if state.current_phase in ("INIT", "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"):
        return (True, None)
    return (False, f"unknown state {state.current_phase!r}")


def resume_session(repo_root: pathlib.Path, session_id: str) -> tuple[Optional[AutoState], Optional[str]]:
    """Load a session + clear BLOCKED/PAUSED markers so the next phase can run.
    Returns (state, error_msg). On error, state is None.
    """
    state = load_state(repo_root, session_id)
    if state is None:
        return (None, f"no state found at {state_path(repo_root, session_id)}")
    ok, reason = can_resume(state)
    if not ok:
        return (None, reason)
    # Clear blocking reasons + reset failure counter; the caller will run_phase next.
    state.blocked_reason = None
    state.paused_reason = None
    state.consecutive_failures = 0
    if state.current_phase in ("BLOCKED", "PAUSED"):
        # Resume from the next phase after the last completed.
        state.current_phase = _next_phase_after(state.completed_phases)
    save_state(repo_root, state)
    return (state, None)


def _next_phase_after(completed: list[str]) -> str:
    """Return the phase that follows the last completed one."""
    from bequite.auto import PHASES
    for ph in PHASES:
        if ph not in completed:
            return ph
    return "DONE"


# ----------------------------------------------------------------------- parallel fan-out


def should_split_parallel(num_tasks: int, threshold: int = 5) -> bool:
    """Per AkitaOnRails 2026: split into subagents only when N > threshold (default 5).
    Below threshold, solo frontier wins.
    """
    return num_tasks > threshold


def fan_out_parallel(
    tasks: list[dict],
    *,
    threshold: int = 5,
) -> list[dict]:
    """Mark tasks as parallel-eligible. Adds `parallel_eligible: bool` to each task.

    Rule: a batch of tasks is parallel-eligible only when ALL of:
    1. count > threshold
    2. each task is independent (no `depends_on` declared OR depends only on a completed phase)
    3. each task touches non-overlapping files (best-effort heuristic — caller verifies)
    """
    eligible = should_split_parallel(len(tasks), threshold=threshold)
    annotated: list[dict] = []
    for t in tasks:
        is_indep = not t.get("depends_on") or all(d in t.get("completed_deps", []) for d in t.get("depends_on", []))
        annotated.append({**t, "parallel_eligible": eligible and is_indep})
    return annotated


# ----------------------------------------------------------------------- idempotency


def is_phase_idempotent_rerun(state: AutoState, phase: str) -> bool:
    """Return True when a phase has been completed before for this session.
    Caller can skip the actual work + emit a 'no-op rerun' receipt instead.
    """
    return phase in state.completed_phases


def detect_double_commit(repo_root: pathlib.Path, feature: str) -> Optional[str]:
    """Best-effort: scan .bequite/auto-state/ for another session with the same feature in flight.
    Returns the conflicting session_id, or None.
    """
    for s in list_sessions(repo_root):
        if s.get("feature") == feature and s.get("phase") not in ("DONE", "FAILED"):
            return s.get("session_id")
    return None
