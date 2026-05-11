# Current mode

**Mode:** `(none selected yet — run /bq-mode)`

## Allowed modes

| Mode | When to use | Entry command |
|---|---|---|
| **New Project** | Starting from scratch in an empty folder | `/bq-mode` then `/bq-new` |
| **Existing Project Audit** | Working with an existing repo; want to understand + clean it | `/bq-mode` then `/bq-existing` |
| **Add Feature** | Existing repo; adding one feature | `/bq-feature "<feature title>"` |
| **Fix Problem** | Something is broken | `/bq-fix "<symptom>"` |
| **Research Only** | Pre-planning research; no implementation | `/bq-mode → research` |
| **Release Readiness** | Built; now need to verify + ship | `/bq-mode → release` |

## Mode-specific workflows

Each mode has a recommended sequence (defined in `docs/architecture/FEATURE_AND_FIX_WORKFLOWS.md`).

The `WORKFLOW_GATES.md` enforces the right gates per mode (some modes skip irrelevant phases).

## Selecting / changing mode

Run `/bq-mode` to interactively select. Run `/bq-mode <name>` to set directly.

Mode change after work is started:
- Allowed but warns user
- Logs the change to `.bequite/state/DECISIONS.md` for traceability
- Does NOT reset memory or gates — those track the actual state regardless of mode

## Reading this file

- `/bequite` reads it to recommend next commands.
- `/bq-auto` reads it to determine the autonomous workflow path.
- Phase orchestrators (`/bq-p0`–`/bq-p5`) skip irrelevant gates per the selected mode.
