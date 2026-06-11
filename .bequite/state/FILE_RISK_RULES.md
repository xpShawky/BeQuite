# File Risk Rules (project-tunable)

> Per-project overrides for `docs/architecture/FILE_RISK_CLASSIFICATION.md`. The pack-wide tiers (R3 CONFIRM / R2 ANNOUNCE / R1 NORMAL) apply by default; this file adds project-specific paths or lowers tiers for paths the user has explicitly cleared.

**Read by:** every command at execution-contract step 7, before any Edit/Write.

---

## Project-specific R3 additions (CONFIRM)

| Path / pattern | Why |
|---|---|
| (none yet) | |

## Project-specific R2 additions (ANNOUNCE)

| Path / pattern | Why |
|---|---|
| (none yet) | |

## User-approved tier reductions

> Only the USER adds rows here (or explicitly asks the agent to). Each row needs a date + reason.

| Path / pattern | Default tier | Reduced to | Date | Reason |
|---|---|---|---|---|
| (none yet) | | | | |

---

## For the BeQuite repo itself

| Path | Tier | Note |
|---|---|---|
| `.claude/hooks/*` | R3 | hook scripts are an RCE vector — review-before-enable model |
| `.claude/settings*.json*` | R3 | wires hooks into the harness |
| `scripts/install-bequite.*` | R2 | runs on user machines at install |
| `.bequite/state/WORKFLOW_GATES.md` | R2 | machine-tracked ledger |
| everything else | R1 | |
