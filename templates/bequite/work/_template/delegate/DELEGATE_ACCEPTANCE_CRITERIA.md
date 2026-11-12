# Delegate Acceptance Criteria

Observable, testable success conditions per task. The implementer model can only mark a task `[x]` if all criteria are met.

---

<!--
  Template per task:

  ## T-D-<n>

  - [ ] `<test command>` exits 0
  - [ ] File `<path>` contains `<expected text or pattern>`
  - [ ] No banned weasel words in commit message
  - [ ] No new dependencies added
  - [ ] No files outside "Files to edit" list modified
  - [ ] (additional task-specific criteria)
-->

(populated by `/bq-auto delegate` or `/bq-plan delegate` Phase 1)

---

## Universal criteria (apply to every task)

1. **Test passes** — the test command in `DELEGATE_TEST_PLAN.md` exits 0
2. **No weasel words** — no "should", "probably", "seems to", "appears to", "might", "hopefully", "in theory" in commit message
3. **No scope creep** — only files in "Files to edit" changed (verify via `git diff --name-only`)
4. **No new deps** — no `package.json` / `requirements.txt` / `Cargo.toml` edits unless explicitly allowed
5. **Logged** — `AGENT_LOG.md` entry per task

If any criterion fails: mark task `[!]` blocked; do NOT mark `[x]`.
