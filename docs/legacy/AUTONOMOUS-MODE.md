# Autonomous mode

> One-click run-to-completion P0 → P7 with safety rails.

## What it does

```bash
bequite auto run \
  --feature "add-health-endpoint" \
  --max-cost-usd 5 \
  --max-wall-clock-hours 2 \
  --mode auto
```

Runs all seven phases in sequence: P0 research → P1 stack → P2 plan → P3 phases → P4 tasks → P5 implement → P6 verify → P7 handoff. State machine persists at `.bequite/auto-state/<session>.json`.

## Per-phase contract

Each phase enters with **memory + receipts + previous-phase-output**, and exits only when:

1. The phase's artifact exists and validates.
2. The Skeptic produces ≥1 kill-shot question and the primary answers it.
3. The phase's gate (Article II verification) passes.
4. The receipt is emitted (and signed since v0.7.1).
5. A commit lands tagged `bequite-auto/<feature>/P<n>`.

## Safety rails

Auto-mode pauses (does NOT auto-override) at:

| Trigger | Effect |
|---|---|
| Cost ceiling reached (`max-cost-usd`) | PAUSED — write `.bequite/cache/cost-override.json` to resume |
| Wall-clock ceiling reached (`max-wall-clock-hours`) | PAUSED |
| 3 consecutive Implementer failures on same task | BLOCKED |
| Banned weasel word in completion | BLOCKED via `stop-verify-before-done.sh` hook |
| PreToolUse hook blocks (exit 2) | BLOCKED — never auto-overrides |
| One-way-door operations | Always pause (PyPI, npm, git push to main, force push, terraform apply, DB migration against shared DB) |
| First HANDOFF generation | PAUSED for human review of engineer-handoff doc |
| Stack ADR sign-off | PAUSED unless `--auto-sign-stack` flag is set |

## State machine

```
INIT → P0_RESEARCH → P1_STACK → P2_PLAN → P3_PHASES → P4_TASKS →
       P5_IMPLEMENT (per-task loop) → P6_VERIFY → P7_HANDOFF → DONE

Any phase can exit to: BLOCKED | FAILED | PAUSED.
```

## CLI flags

| Flag | Default | Meaning |
|---|---|---|
| `--feature <name>` | (required) | Feature being implemented |
| `--max-cost-usd <n>` | 20 | Hard ceiling — PAUSED on hit |
| `--max-wall-clock-hours <n>` | 6 | Hard ceiling — PAUSED on hit |
| `--phases <subset>` | all | Run subset (e.g. `P5,P6`) |
| `--mode <slow|fast|auto>` | auto | Slow = wait for human at every phase; fast = skip optional gates |
| `--on-failure <pause|abort|continue-with-warning>` | pause | What happens on a failure |
| `--no-skeptic` | false | Debug only — disable Skeptic gates |

## Resume

```bash
bequite auto status <session-id>     # show state
# (after fixing whatever blocked / failed)
bequite auto resume <session-id>     # v0.10.7+
```

`resume_session()` clears BLOCKED / PAUSED markers + resets the failure counter + advances to the next phase after the last completed one.

## Heartbeat

During long phases (P5, P6), auto-mode writes a heartbeat marker into `activeContext.md` every 5 minutes:

```
<!-- auto-mode heartbeat 2026-05-10T14:23:01Z session a3f12... phase P5 -->
```

This is mostly for human introspection (`bequite memory show activeContext`) — the state machine uses `state_path(repo, session_id)` for actual persistence.

## Idempotency

- `bequite auto run` for a feature already in flight → detects via `detect_double_commit` and refuses (returns the conflicting session_id).
- Phases already completed in a session don't re-run on resume; `is_phase_idempotent_rerun(state, phase)` returns True.

## Parallel-task fan-out (v0.10.7+)

When ScrumMaster (P4) marks tasks as `parallel: true` in `tasks.md`, `fan_out_parallel()` checks AkitaOnRails 2026 N>5 threshold:

- ≤ 5 parallel-eligible tasks → solo frontier model (no fan-out).
- \> 5 parallel-eligible tasks AND each task is independent → fan out to subagents.

## What auto-mode does NOT do

- Skip Phase 0 research.
- Silently change doctrines mid-run.
- Bypass hooks under any flag.
- Generate publishable press / blog content without a pause.
- Run any one-way-door operation without explicit human approval.

## Recovery from a stuck session

```bash
# 1. Inspect
bequite auto status <session-id>

# 2. Read why it blocked
cat .bequite/auto-state/<session>.json | jq '.blocked_reason'

# 3. Fix the underlying issue (cost ceiling? read current_phase.md and decide)

# 4. Resume
bequite auto resume <session-id>
```

## Cross-references

- Module: `cli/bequite/auto.py` (v0.10.0)
- Hardening: `cli/bequite/auto_state.py` (v0.10.7)
- Tests: `tests/integration/auto/{test_auto_smoke.py,test_auto_state_smoke.py}`
- Build plan §5 + §10: `.bequite/memory/prompts/v1/2026-05-10_initial-plan.md`
