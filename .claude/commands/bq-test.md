---
description: Run tests AND write missing ones. Detects test framework from the repo (vitest, jest, pytest, cargo test, etc.) and identifies coverage gaps.
---

# /bq-test — test discipline

You run the project's tests AND write any missing tests for recently-changed code.

## Step 1 — Detect test framework

From `.bequite/audits/DISCOVERY_REPORT.md` or `package.json::"scripts.test"` / `pyproject.toml` / `Cargo.toml`:

| Stack | Test command | File pattern |
|---|---|---|
| Node + vitest | `npm test` or `npx vitest run` | `*.test.{ts,tsx,js}` |
| Node + jest | `npm test` or `npx jest` | `*.test.{ts,tsx,js}` |
| Node + playwright (e2e) | `npx playwright test` | `tests/e2e/*.spec.ts` |
| Python pytest | `python -m pytest` | `test_*.py`, `*_test.py` |
| Rust | `cargo test` | inline `#[test]` |
| Go | `go test ./...` | `*_test.go` |

If no test framework detected: tell the user to pick one + propose the lightest option (vitest for Node, pytest for Python). Stop until they confirm.

## Step 2 — Run the tests

Use Bash with the detected command. Capture full stdout + stderr + exit code.

## Step 3 — Classify results

**Green (exit 0):** All tests pass.
- Report counts. Suggest moving on.

**Red (exit nonzero):** At least one failure.
- Read the failure output
- For each failure: identify the test name + file:line + the assertion that failed
- Group by file

**Crashed (exit code odd; test framework itself errored):**
- Config issue (missing tsconfig, broken import, etc.)
- This is a `/bq-fix` situation, not a test failure

## Step 4 — Coverage gap scan

Look at recently changed source files (git status; recent commits):

- For each modified source file, is there a matching test file?
- For each new function / route / component, does at least one test exercise it?

List gaps:

```
Coverage gaps:
- src/lib/csv.ts → no test file
- src/api/booking/route.ts → no integration test for POST
- components/SignupForm.tsx → no test
```

## Step 5 — Write missing tests (if user wants)

Ask:
> "Found <count> coverage gaps. Write tests for them? (y/N)"

If yes:
- For each gap, write a SMALL test:
  - Round-trip / happy-path case
  - One edge case
  - Don't try for 100% coverage — aim for "exercised at least once"
- Add to the same naming convention the repo uses
- Run the new tests + confirm green

## Step 6 — Write VERIFY_REPORT.md updates

Don't write a standalone `TEST_REPORT.md` — that level of detail is in `/bq-verify`. Just update state.

## Step 7 — Update state + log

- `.bequite/state/LAST_RUN.md` → `/bq-test` + outcome
- `.bequite/logs/AGENT_LOG.md` appended

## Step 8 — Report back

```
✓ Tests run

Framework:       <name>
Existing tests:  <count> · pass: <count> · fail: <count>
New tests added: <count>
Coverage gaps:   <count> (after fixes)

Next: /bq-review (if some still failing) or /bq-implement (if all green and tasks remain)
```

## Rules

- **Run all tests, not a subset** — unless the test runner is slow + user opted into `--changed` mode.
- **Failures are not "should be ok".** Either pass or fail; no maybes.
- **New tests for new code.** Every `/bq-implement` or `/bq-add-feature` that doesn't write a test is incomplete.
- See `.claude/skills/bequite-testing-gate/SKILL.md` for the deeper test-discipline procedures (test pyramid, contract tests, snapshot rules, etc.).

## Standardized command fields (alpha.6)

**Phase:** P3 — Quality and Review
**When NOT to use:** no code changed since last test run (waste of cycles); or no test framework exists yet (use `/bq-feature testing` to set one up — never auto-install).
**Preconditions:** `BEQUITE_INITIALIZED`
**Required previous gates:** `BEQUITE_INITIALIZED`
**Quality gate:**
- All tests run (none silently skipped)
- All tests pass — green
- Coverage gap report written for changed files
- Marks `TEST_DONE ✅`
**Failure behavior:**
- Tests red → write specific failure to `ERROR_LOG.md`; recommend `/bq-fix`
- No test framework detected → don't auto-install (tool neutrality); recommend `/bq-feature testing`
- Flaky test (pass on retry) → log to `MISTAKE_MEMORY.md`; flag for stabilization
**Memory updates:** Sets `TEST_DONE ✅` when all green. May write new test files.
**Log updates:** `AGENT_LOG.md`. `MISTAKE_MEMORY.md` for flaky-test patterns.

## Memory files this command reads

- `.bequite/audits/DISCOVERY_REPORT.md`
- `package.json` / equivalent test config
- Source files (to find coverage gaps)

## Memory files this command writes

- New test files (when gaps were filled)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

- All green + tasks remain → `/bq-implement` (next task)
- Some failing → `/bq-fix`
- Coverage gaps still open → `/bq-review`

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
