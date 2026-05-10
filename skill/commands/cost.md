---
name: bequite.cost
description: Token + dollar receipts roll-up. BeQuite-unique. Reads .bequite/receipts/ (v0.7.0+); produces per-phase, per-persona, per-day, per-feature, per-session breakdowns. Cross-references state/project.yaml::safety_rails.cost_ceiling_usd. Token-economist persona owns this.
phase: any
persona: token-economist
implementation: cli/bequite/cost.py (lands with v0.7.0 receipts)
---

# /bequite.cost [scope] [flags]

When invoked (or `bequite cost [args]`):

## Scope arguments

- `--session` (default) — current session.
- `--feature <slug>` — by feature.
- `--phase P5` — by phase.
- `--persona software-architect` — by persona.
- `--day` / `--week` / `--month` / `--all-time` — time windows.
- `--since <tag>` — from a release tag forward.
- `--vs-budget` — show consumption against `safety_rails.cost_ceiling_usd`.

## Step 1 — Read receipts

Walk `.bequite/receipts/*.json` (v0.7.0+). Each receipt carries:

```json
{
  "cost": {
    "input_tokens": ...,
    "output_tokens": ...,
    "cache_read_input_tokens": ...,
    "usd": ...
  },
  "model": { "name": "claude-opus-4-7", "reasoning_effort": "high" },
  "phase": "P5",
  "persona": "backend-engineer",
  "feature": "lead-routing",
  "task_id": "TASK-007",
  "timestamp_utc": "..."
}
```

## Step 2 — Aggregate

For the requested scope, produce:

```
PHASE        | PERSONA              | TOKENS (in)   | TOKENS (out) | CACHE READ  | USD     | RUNS
-------------|----------------------|---------------|--------------|-------------|---------|------
P0 Research  | research-analyst     | 124,512       | 18,432       | 87,231      | $1.43   | 3
P1 Stack     | software-architect   | 89,310        | 12,890       | 54,120      | $1.12   | 2
P5 Implement | backend-engineer     | 312,540       | 41,890       | 198,120     | $3.21   | 11
P5 Implement | frontend-designer    | 198,420       | 28,140       | 122,310     | $2.04   | 8
P5 Review    | reviewer (architect) | 45,230        | 6,820        | 31,210      | $0.58   | 4
P5 Skeptic   | skeptic              | 18,310        | 4,210        | 12,840      | $0.24   | 5
P6 Verify    | qa-engineer          | 156,210       | 22,430       | 98,540      | $1.81   | 1
-------------|----------------------|---------------|--------------|-------------|---------|------
TOTAL        |                      | 944,532       | 134,812      | 604,371     | $10.43  | 34

Cost ceiling: $20.00  (safety_rails.cost_ceiling_usd)
Consumed:     $10.43  (52%)
Remaining:    $9.57   (48%)
```

## Step 3 — Anomalies

- Per-persona cost > 2× routing.json estimate → flag (token-economist routing matrix may need re-tuning).
- Per-day cost > 1.5× rolling-7-day average → flag (cost runaway?).
- Cache-hit ratio < 50% on long sessions → flag (prompt compression opportunity).

## Step 4 — Roll-up to observability (optional)

If `state/project.yaml::telemetry.mode == "receipts_only"`: emit aggregated metrics (no prompt content) to the configured backend. Default: off.

## Step 5 — Save

`evidence/_cost/cost-<scope>-<YYYY-MM-DD>.md`. Update `state/evidence_index.json`.

## Stop condition

- Aggregation rendered.
- Anomalies surfaced (if any).
- For `--vs-budget`: exit 0 if under ceiling; exit 1 if 80%+; exit 2 if 100%+ without override.

## Anti-patterns

- Reading receipts without verifying chain integrity (sloppy; use `/bequite.evidence` first).
- Reporting only totals without per-persona breakdown (hides where the money went).
- Surfacing cost without recommending mitigations (token-economist persona's job).

## Related

- Token-economist persona at `skill/agents/token-economist.md`.
- `stop-cost-budget.sh` — Stop hook that enforces ceiling.
- `routing.json` — model choices that drive cost.
- `/bequite.audit` — separate concern (rule violations) but cross-references when over-budget runs accumulate.
