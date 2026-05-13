# Delegate Test Plan

Exact test commands to run after each task. The implementer model runs the command, checks output matches "Expected", and only then marks the task `[x]`.

---

<!--
  Template per task:

  ## T-D-<n>

  ```bash
  <exact command — copy-paste-runnable>
  ```

  **Expected output (or pattern):**
  ```
  <expected stdout/stderr snippet>
  ```

  **Exit code:** 0

  **If test fails:**
  - First retry: re-run the same command (transient failures happen)
  - Second retry: re-run + check the changed file matches "Files to edit"
  - Third failure: mark task `[!]` blocked, log to ERROR_LOG.md, exit
-->

(populated by `/bq-auto delegate` or `/bq-plan delegate` Phase 1)

---

## Notes

- Each test command must be **deterministic** — no flaky / time-dependent / order-dependent tests
- Each command should run in **< 30 seconds** for the cheap model to iterate quickly
- If a task needs a longer-running test (e.g. full e2e), defer that to Phase 3 verify, not per-task
- Tests must be **already passing on main** before Phase 1; the implementer's job is to add new passing tests, not fix pre-existing ones
