# Delegate Tasks

Atomic task list for the implementer model. Written by the strong model in Phase 1 of Delegate Mode.

---

**Generated:** <ISO 8601 UTC>
**Feature:** <name>
**Strong model (planner):** <e.g. Claude Opus 4.7>
**Recommended implementer model:** <e.g. Claude Sonnet 4.5>
**Total tasks:** <N>
**Estimated cheap-model tokens:** <range>
**Estimated total cost (Phase 1 + 2 + 3):** $<estimate>
**Estimated savings vs. strong-model-end-to-end:** <%>

---

## Task list

<!--
  Template per task:

  - [ ] T-D-<n> — <one-line goal>
    - File: <primary file path>
    - Acceptance: <one observable criterion>
    - Hard gate: <none | name from /bq-auto's 17 hard gates>
    - Est. cheap-model time: <minutes>
-->

(populated by `/bq-auto delegate` or `/bq-plan delegate` Phase 1)

---

## Status markers (used by implementer model)

- `[ ]` — pending
- `[x]` — complete (test passed)
- `[!]` — blocked (3 failures or hard gate hit; needs user/strong-model attention)
- `[?]` — clarification needed (instructions too vague; strong model needs to re-write)

---

## Implementer model rules

1. Read this file + `DELEGATE_INSTRUCTIONS.md` per task. Read ONLY the files listed per task.
2. Apply implementation steps EXACTLY. Don't refactor. Don't decide architecture.
3. Run the test command from `DELEGATE_TEST_PLAN.md` after each task.
4. Mark task `[x]` only if test passes.
5. Don't install new dependencies (already decided in Phase 1).
6. Don't edit files not listed in "Files to edit".
7. Stop on hard gate; mark `[!]`; wait for user.
8. No banned weasel words in commit messages.
