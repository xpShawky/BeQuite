---
description: Implement ONE approved task at a time. Inspect first, minimal safe changes, run relevant tests, update logs. Stop if a blocker appears.
---

# /bq-implement — the workhorse

You are the implementer. Pick one task from `.bequite/tasks/TASK_LIST.md`, do it cleanly, verify it, log it.

## Step 1 — Pick the next task

Read `.bequite/tasks/TASK_LIST.md`. Find the **first task with status `[ ] pending`** that has all dependencies satisfied (their status is `[x] done`).

If multiple are eligible:
- If the user passed an argument like `/bq-implement T-3.2`, pick that one.
- Otherwise pick the lowest-numbered.

If no eligible task:
- All done? → suggest `/bq-verify` next.
- All blocked? → list the blockers and exit.

## Step 2 — Read context

- The task entry (acceptance + files + dependencies)
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (relevant section)
- `.bequite/state/DECISIONS.md` (any decisions affecting this task)
- The files the task will modify (use Read + Glob — never overwrite without reading first)

## Step 3 — Mark the task in-progress

Update `.bequite/tasks/TASK_LIST.md` — change the task status from `[ ]` to `[~]`.

## Step 4 — Implement minimally

- Make the smallest set of changes that satisfies the acceptance criterion.
- No drive-by refactors. If you notice something else broken, log it to `.bequite/state/OPEN_QUESTIONS.md` or `.bequite/logs/ERROR_LOG.md` — don't fix it here.
- Use existing patterns from the codebase. Look for similar files; mirror their conventions.
- If the task mentions a library you haven't seen used: verify it exists (Read the lockfile) before importing. PhantomRaven defense.

## Step 5 — Run the relevant tests

After your changes, run the test command that covers the touched files. If unsure which tests are relevant, run the whole test suite.

If tests fail:
- Read the failure
- If it's expected (e.g. new behavior; no test yet) → write the test as part of this task
- If it's a regression → fix the regression OR mark task `[!] blocked` and stop

## Step 6 — Verify the acceptance criterion

Re-read the task's acceptance criterion. Run THAT specific check — curl an endpoint, click a button, query the DB.

Do not declare done if the criterion isn't met. Banned weasel: "should work", "probably", "seems to", "appears to", "I think it works", "might", "hopefully", "in theory".

## Step 7 — Update task status

If verified done:
- Change `[~]` → `[x]` in TASK_LIST.md
- Append the test command + its exit code to the task entry

If blocked:
- Change `[~]` → `[!]`
- Add a note explaining the blocker
- Stop the workflow — do not pick another task

## Step 8 — Update state + logs

- `.bequite/state/CURRENT_PHASE.md` — note which task just completed
- `.bequite/state/LAST_RUN.md` updated with the task ID + outcome
- `.bequite/logs/AGENT_LOG.md` appended:

```markdown
## <ISO 8601 UTC>
**Command:** /bq-implement T-2.1
**Task:** Install + init Better-Auth
**Files touched:** lib/auth.ts (new), app/api/auth/[...all]/route.ts (new), package.json (added better-auth)
**Tests run:** `npm test` — 12 passed
**Acceptance:** `curl http://localhost:3000/api/auth/session` → HTTP 200 ✓
**Status:** done
**Next:** T-2.2 (sign-up page)
```

## Step 9 — Report back

```
✓ T-<id> done — <task title>

Files touched: <count>
Tests:         <pass / total>
Acceptance:    <one-line confirmation>

Next: /bq-implement T-<next-id>   (or /bq-test if you want explicit test coverage)
```

If blocked:

```
✗ T-<id> BLOCKED — <task title>

Why: <one-line blocker>
What to try: <suggestion>

Next: /bq-fix or /bq-clarify (or just answer the blocker question yourself, then /bq-implement T-<id> retry)
```

## Rules

- **One task per /bq-implement call.** Multiple tasks = multiple invocations.
- **Inspect files before editing.** Read every file you'll change FIRST. Otherwise the Edit tool errors out anyway.
- **Tests run before declaring done.** No exceptions.
- **No drive-by refactors.** Surface them; don't fix them here.
- **Stop on blocker.** Never skip a blocker silently.
- **Update TASK_LIST.md after every state change.**

## Standardized command fields (alpha.6)

**Phase:** P2 — Planning and Build
**When NOT to use:** no tasks pending (TASK_LIST empty) — use `/bq-feature` or `/bq-fix` for new work. Or you want to do a feature-shaped or bug-shaped task that isn't on the list — use those commands directly.
**Preconditions:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `PLAN_APPROVED`, `ASSIGN_DONE`
**Required previous gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `PLAN_APPROVED`, `ASSIGN_DONE`
**Quality gate:**
- Task marked `[x]` complete
- Acceptance criterion verified
- Test for the change is passing
- No banned weasel words in completion claim
- No destructive op executed
- No new dep installed without decision section (tool neutrality)
**Failure behavior:**
- Test red after change → roll back via `git stash`; log to `ERROR_LOG.md`; retry once; if still red, mark task `[!]` blocked and pause
- 3 consecutive failures on the same task → pause; ask user
- Blocker discovered → mark `[!]` blocked with one-line reason; pick next non-dependent task
**Memory updates:** Updates `TASK_LIST.md` (`[ ]` → `[x]`). Marks `IMPLEMENT_DONE ✅` when list empty. Updates `LAST_RUN.md`.
**Log updates:** `AGENT_LOG.md` entry per task. `CHANGELOG.md` `[Unreleased]` per user-visible change.

## Memory files this command reads

- `.bequite/tasks/TASK_LIST.md`
- `.bequite/plans/IMPLEMENTATION_PLAN.md`
- `.bequite/state/DECISIONS.md`
- The actual source files for the task

## Memory files this command writes

- The source files for the task (the actual implementation)
- `.bequite/tasks/TASK_LIST.md` (task status updated)
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

- `/bq-implement` (next task) — continue the workflow
- `/bq-test` — if you want explicit test coverage check
- `/bq-fix` — if blocked
- `/bq-verify` — if this was the last task

---

## Gate check + memory preflight (alpha.15)

Before doing any work:

1. **Gate check.** Read `.bequite/state/WORKFLOW_GATES.md`. If this command's required gates aren't `✅`, refuse:
   > "You're trying to run this command, but `<required-gate>` is pending. Run `<prerequisite-command>` first."

   Don't proceed when a required gate is missing. Recommend the prerequisite + how to resume.

2. **Memory preflight.** Read these files first (per `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`):

   - `.bequite/state/PROJECT_STATE.md`
   - `.bequite/state/CURRENT_MODE.md`
   - `.bequite/state/CURRENT_PHASE.md`
   - `.bequite/state/LAST_RUN.md`
   - `.bequite/state/MISTAKE_MEMORY.md` — top 10–20 entries (skip mistakes already learned)
   - Other state files only when relevant to this command's scope (`DECISIONS.md` for architectural questions, `OPEN_QUESTIONS.md` for phase transitions, `MODE_HISTORY.md` when invoked via `/bq-auto`-style flows)

   **Use focused reads.** Don't load all of `.bequite/` every command.

## Memory writeback (alpha.15)

After successful completion:

- `.bequite/state/LAST_RUN.md` — this command + outcome
- `.bequite/state/WORKFLOW_GATES.md` — set this command's gate to `✅` if applicable
- `.bequite/state/CURRENT_PHASE.md` — advance if phase transitioned
- `.bequite/logs/AGENT_LOG.md` — append entry
- `.bequite/logs/CHANGELOG.md` `[Unreleased]` — only when material files changed (skip for read-only commands)
- `.bequite/state/MISTAKE_MEMORY.md` — append when a project-specific lesson surfaced
- `.bequite/state/MODE_HISTORY.md` — append mode + outcome (when invoked via `/bq-auto`-style mode)

**Failure behavior:** don't claim `✅ done` if any of the above wasn't completed. Report PARTIAL with the specific gap.
