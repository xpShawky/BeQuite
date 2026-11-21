---
name: bequite-testing-gate
description: Use when writing, reviewing or running tests, when a fix needs a regression test, when a feature is marked done, or when tests are flaky, slow or suspiciously green. Picks the test level, proves each new test fails before the fix, and writes evidence in the one format the verifier re-runs.
last_verified: 2026-11-21
sources:
  - https://playwright.dev/docs/best-practices (read 2026-11-21) role locators, web-first assertions, isolation
  - https://playwright.dev/docs/test-agents (read 2026-11-21) planner, generator, healer since 1.56
  - https://testing-library.com/docs/queries/about/ (read 2026-11-21) query priority
  - https://abseil.io/resources/swe-book/html/ch11.html (read 2026-11-21) test sizes, 80/15/5 mix, flakiness
  - https://registry.npmjs.org/vitest (read 2026-11-21) vitest 5.1.1, 2026-11-18
  - https://pypi.org/pypi/pytest/json (read 2026-11-21) pytest 9.2.0, 2026-10-27
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# bequite-testing-gate

A green suite proves nothing if the new test would also pass on the broken code. This skill picks the cheapest test that would catch the bug, shows it failing first, then passing, and records the proof so another agent can run it again.

## When to use

- `/bq-test`, `/bq-feature`, `/bq-fix`, `/bq-verify`, `/bq-implement` when a task adds behaviour.
- A review finds a test that mocks the thing it claims to test, or a suite that only passes with retries.
- UI work: after `/bq-live-edit` or `/bq-uiux-variants`, the build and the page tests.

Not for: choosing what to build, load or penetration testing (name the specialist tool and stop).

## Procedure

1. **Find the existing harness.** Read the test config and one existing test before writing a new one; match its runner, folder layout and naming. If there is no harness, propose one with the ten questions (the stack's own runner first) and wait for the user's yes before installing anything.
2. **Name the behaviour.** One sentence per test, written as the user-visible rule: "rejects a booking that starts in the past", not "test validate()".
3. **Pick the level.** The smallest that can catch it (`references/levels.md`): small (one process, no network, no sleep) for logic; medium (real database or HTTP on localhost) for boundaries; large (browser, deployed stack) for a few key user flows. Rough mix by count: 80 / 15 / 5.
4. **Use real things you own; fake what you do not.** Real objects and a real test database over mocks of your own code. Stub third-party APIs at the network edge. A test that mocks the function under test is deleted.
5. **Write it so it fails first.** Run it against the current (broken, or not-yet-built) code and paste the failure. If it passes, the test is wrong: fix the test, not the code.
6. **Make it pass** with the smallest change, then run the whole suite, not only the new test.
7. **UI tests**: locate by role and label (`getByRole('button', { name: 'Save' })`), assert with retrying web-first assertions, each test with its own storage state, no fixed sleeps. Agent-generated tests (Playwright's planner, generator and healer, or any other) go through step 5 like hand-written ones.
8. **Flaky tests** are bugs: reproduce with repeats (`--repeat-each 20` in Playwright, a loop in other runners), find the race or shared state, fix it. A retry that hides it is reported as a finding.
9. **Write the evidence block** (format below) to `.bequite/work/<id>/evidence.md`. The verifier re-runs exactly these commands.

## Evidence format (shared with the verifier)

```
### <task id> <behaviour> (<date>)
before: $ <command>   -> exit <n>, "<the failing line>"
after:  $ <command>   -> exit 0, "<the passing summary line>"
suite:  $ <full suite command> -> exit 0, "<N passed, M skipped>"
```

## Worked example (real run on this repo, 2026-11-21)

Behaviour: "the self-check fails when a command cites a path that does not exist." Check under test: `references_exist` in `scripts/bq_check.py`.

```
before: $ rmdir motion-library/inbox/New && python scripts/bq_check.py references_exist
        -> exit 1, "FAIL references_exist (1) - .claude/commands/bq-motion.md:33: missing path `motion-library/inbox/New`"
after:  $ mkdir -p motion-library/inbox/New && python scripts/bq_check.py references_exist
        -> exit 0, "1/1 checks passed"
suite:  $ python scripts/bq_check.py -> exit 0, "8/10 checks passed, 2 warning(s)", 0.397 s wall
```

The check catches the regression (it failed when the path vanished), so it can be trusted. The run also exposed a real defect: the cited folder is gitignored, so the check fails on every clean clone; it went to the owner of the command file with this block as the repro.

## Quality gate

- Each new test has a "before" line showing it failed, and an "after" line from the full suite.
- No test mocks the unit it tests; no fixed sleeps; no order dependence (run shuffled where the runner supports it).
- UI tests use role or label locators; test IDs only where no accessible name exists, with a comment.
- Flaky tests are reported with the repeat count that reproduced them, not retried into green.
- Coverage numbers, if shown, come from the tool's output. "Every critical path and every error path has a test" is the target, not a percentage.

## Boundaries

- Never edit a test just to make it pass without saying why the old assertion was wrong.
- Never install a test framework, browser binaries or a coverage service without the user's yes.
- Runner versions in this skill (vitest 5.1.1, pytest 9.2.0, @playwright/test 1.65.1 on 2026-11-21) are for orientation; check the registry before pinning.

## References (load on demand)

- `references/levels.md`: level table, what to test where, contract and snapshot rules, starter tests for vitest, pytest and Playwright.
