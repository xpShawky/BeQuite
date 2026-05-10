---
name: bequite.auto
description: One-click run-to-completion. BeQuite-unique. Runs P0 → P7 sequentially with safety rails (cost ceiling, wall-clock ceiling, 3-failure threshold, banned-word check, hook-block never auto-overridden, one-way doors always pause). State machine with explicit BLOCKED/FAILED/PAUSED states. Per-phase commits make every phase revertable. Implementation lands in v0.10.0 as cli/bequite/auto.py.
phase: orchestrates P0 → P7
persona: orchestrator (this SKILL) + dispatch to phase personas
implementation: cli/bequite/auto.py (v0.10.0)
---

# /bequite.auto --feature <name> [flags]

When invoked (or `bequite auto --feature <name>`):

## CLI flags

- `--feature <slug>` (required) — the feature to drive.
- `--max-cost-usd <n>` — override session ceiling (default 20; from `state/project.yaml::safety_rails.cost_ceiling_usd`).
- `--max-wall-clock-hours <n>` — override (default 6).
- `--phases <comma-list>` — subset (e.g. `--phases P5,P6` to skip discovery / planning when those exist).
- `--mode <slow|fast|auto>` — execution speed (orthogonal to project Mode in `state/project.yaml`; `slow` = pause at every task, `fast` = no pauses below safety rails, `auto` = pauses only at one-way doors and rails).
- `--on-failure <pause|abort|continue-with-warning>` — default `pause`.
- `--no-skeptic` — debug only; refuses without explicit `BEQUITE_DEBUG_SKIP_SKEPTIC=1` env.
- `--auto-sign-stack` — allow stack ADR sign-off without pause (default OFF; one-way door).
- `--resume <session-id>` — resume from `.bequite/auto-state/<session>.json` (v0.10.1).

## State machine

```
INIT → P0_RESEARCH → P1_STACK → P2_PLAN → P3_PHASES → P4_TASKS →
       P5_IMPLEMENT (per-task loop) → P6_VERIFY → P7_HANDOFF → DONE

Any phase can exit to:
  BLOCKED — needs human (Skeptic kill-shot unanswerable; ambiguous spec)
  FAILED  — gate trip (test fails 3× in a row; freshness probe stale-block)
  PAUSED  — rail trip (cost ceiling; wall-clock ceiling; hook block; one-way door)
```

State persisted to `.bequite/auto-state/<session>.json` every 5 minutes (heartbeat).

## Per-phase contract

Each phase exits only when:

1. The phase artefact exists + validates against its schema.
2. Skeptic kill-shot answered in writing (in receipt or in `docs/risks.md` for accepted-risk).
3. Phase gate (Article II verification) passes.
4. Receipt emitted (v0.7.0+) and signed (v0.7.1+).
5. Per-phase commit lands tagged `bequite-auto/<feature>/P<n>` for clean revertability.

## Safety-rail boundaries (auto-mode pauses for owner)

Even in `--mode auto`, **always pause** at:

1. **Cost ceiling reached** — 80% warns; 100% pauses for explicit owner approval logged to `.bequite/cache/cost-override.json`.
2. **Wall-clock ceiling reached** — same.
3. **3 consecutive Implementer failures on the same task** → `BLOCKED`; ask for human input.
4. **Banned-word detected** in completion message → `BLOCKED` (Stop hook + Constitution v1.0.1 Article II).
5. **PreToolUse hook block** (secret-scan / block-destructive / verify-package) — **never** auto-override.
6. **Stack ADR sign-off** (one-way door) — pause unless `--auto-sign-stack`.
7. **First HANDOFF generation** — pause for human review of the engineer-handoff doc.
8. **One-way operations** — never auto-run: PyPI publish, npm publish, git push to main, force push, terraform apply, DB migrations against shared DBs.

## Failure replay

On `BLOCKED` / `FAILED`: capture state to `.bequite/replays/<timestamp>/`:

- Full Memory Bank snapshot.
- Last 10 receipts.
- Last 100 lines of session log.
- Failed gate's command + stdout + stderr.
- The single-command resume: `bequite auto resume <session-id>`.

## Heartbeat

During long phases, every 5 minutes:

- Update `.bequite/memory/activeContext.md::heartbeat`.
- Update `state/recovery.md::heartbeat`.
- Append cost ledger to `.bequite/cache/cost-ledger.json`.
- Check ceilings; warn / pause accordingly.

## Auto-mode does NOT

- Skip Phase 0 (Iron Law III).
- Silently change Doctrines or Mode mid-run.
- Bypass hooks under any flag.
- Generate marketing / press content without pause.
- Run any Tier-3 (Dangerous) command (master §19.4).

## Stop condition

`DONE` only when:

- All declared `--phases` exited successfully.
- All phase commits landed.
- All receipts emitted + chain integrity verified.
- HANDOFF.md hand-runnable (verified by re-running `/bequite.recover` then resuming from the recovery prompt in a fresh session).
- `state/recovery.md::Cost-ceiling status` and `Wall-clock-ceiling status` recorded.
- Final summary printed: phases / tasks completed / total cost / total wall-clock / receipts emitted / known issues.

## Anti-patterns

- Setting `--max-cost-usd 1000` to "just get it done" — defeats the ceiling. Use `state/project.yaml::safety_rails` as the source of truth; flag overrides in receipts.
- Setting `--no-skeptic` outside debugging — refuses without explicit env.
- Setting `--auto-sign-stack` for projects with regulated Doctrines — refuse.

## Related

- `/bequite.recover` — generates the resume prompt for `bequite auto resume`.
- `/bequite.cost` — token + dollar receipts roll-up during / after auto-mode.
- `/bequite.evidence` — surface what auto-mode produced.
