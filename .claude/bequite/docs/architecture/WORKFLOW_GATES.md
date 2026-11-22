# Workflow gates

Decision record: ADR-002. The list of gates lives in one place per level: project gates in `.bequite/state/WORKFLOW_GATES.md`, per-work gates in `.bequite/work/<id>/gates.md` (in the BeQuite repo: `templates/bequite/state/WORKFLOW_GATES.md` and `templates/bequite/work/_template/gates.md`).

## What a gate is

A named condition that says whether a command may run. Each gate has one state:

| State | Meaning |
|---|---|
| done | met, with the evidence (a file or a command) recorded next to it |
| pending | not met yet |
| n/a - reason | does not apply to this work; the reason is written |
| blocked | cannot be met until something named is resolved |

## How gates work

- Every command names the gates it **needs** and the gates it **sets** (its "Gates" section).
- A command whose needed gate is not done **refuses** and names the gate and the command that closes it:

  ```
  /bq-implement
  Blocked: PLAN_APPROVED is pending for work 0007. Run /bq-plan first.
  ```

- A command sets its gate only when it finished and its evidence exists. A failed command sets nothing.
- Gates are read at the start of every command (the Orient step of the pipeline). `/bq-recover` uses the ledger to find the last good checkpoint.

## One name per gate

A gate has exactly one spelling: the one in the ledger or the work template. `scripts/bq_check.py` fails the pack on any other name. A new gate is added to the ledger or the work template first, then used.

## Which gates each mode needs

| Mode | P0 setup | P1 framing | P2 build | P3 quality | P4 release | P5 memory |
|---|---|---|---|---|---|---|
| New Project | all | all | all | all | all | all |
| Existing Audit | all | clarify, research | none (audit only) | tests, review | none | snapshot |
| Add Feature | initialized, mode | none (the feature cycle carries its own) | `FEATURE_TESTED` | tests, review | optional | snapshot |
| Fix Problem | initialized, mode | none (reproduce first) | `FIX_VERIFIED` | tests, review | optional | snapshot |
| Research Only | initialized, mode | clarify, research | none | none | none | snapshot |
| Release Readiness | initialized, mode | none | none | all, plus audit | all | snapshot |

Creative work adds its own: `REFERENCES_STUDIED` before any creative output, `HUMAN_TEST_PASSED` before delivery, and for films `SCRIPT_APPROVED`, `STYLE_LOCKED`, `RENDER_PLAN_APPROVED`, `PICTURE_LOCKED`, `AUDIO_APPROVED`, `FINAL_QC_PASS`, `DELIVERY_APPROVED`.

## Commands outside the lifecycle

These need only `BEQUITE_INITIALIZED`, set no phase and do not change the mode: `/bequite`, `/bq-help`, `/bq-explain`, `/bq-suggest` (read-only); `/bq-presentation`, `/bq-content`, `/bq-watch`, `/bq-dna`, `/bq-job-finder`, `/bq-make-money`, `/bq-offer`, `/bq-start` (their own memory folders); `/bq-update`, `/bq-hooks`, `/bq-budget`, `/bq-taste`, `/bq-forge`, `/bq-eval`, `/bq-skill-audit` (maintenance). Running one in the middle of a feature leaves the feature's mode and gates as they are.

## Hard human gates

Separate from workflow gates: actions that always wait for the user's explicit yes, in every mode, including `/bq-auto`. The list is in `.claude/bequite/docs/architecture/AUTO_MODE_STRATEGY.md`.

## Not allowed

- Editing a gate to done by hand without running the command that sets it.
- Treating an optional gate as required, or a required one as optional.
- A "force" flag for gates. There is none.
