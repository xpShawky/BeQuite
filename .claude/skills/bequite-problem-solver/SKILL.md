---
name: bequite-problem-solver
description: Use when something is broken and the cause is not obvious, such as a failing test, an error or crash, "works locally but not in CI", a regression, flaky or intermittent behaviour, or a fix that did not hold. Reproduce first, narrow with evidence (logs, bisect, pickaxe, minimal input), fix the root cause with the smallest change, and prove it with a regression test.
last_verified: 2026-11-21
sources:
  - https://git-scm.com/docs/git-bisect (read 2026-11-21) bisect run exit codes, custom terms
  - https://git-scm.com/docs/git-log (read 2026-11-21) pickaxe -S and -G
  - https://code.claude.com/docs/en/best-practices (read 2026-11-21) give the agent a pass-or-fail check
  - https://sre.google/sre-book/effective-troubleshooting/ (read 2026-11-21) triage, examine, diagnose, test; pitfalls
  - https://www.debuggingbook.org/html/DeltaDebugger.html (read 2026-11-21) shrinking a failing input
  - https://sre.google/workbook/postmortem-culture/ (read 2026-11-21) blameless follow-up
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# bequite-problem-solver

Guessing at fixes creates new bugs. This skill turns a symptom into a reproduction, the reproduction into a root cause, and the cause into a one-line fix plus a test, with every step written down so nobody repeats it.

## When to use

- `/bq-fix` when the cause is not visible in the first read; `/bq-implement` when a task hits an unexpected failure.
- A test that used to pass now fails; CI and local disagree; a bug comes back.
- `/bq-live-edit` when the request is a fix ("cards overflow on mobile"): reproduce before editing.

Not for: new features, refactors, or performance tuning without a symptom.

## Procedure

1. **Triage.** If users are hurt now, stop the bleeding first (revert, feature flag, the owner's call on production), then debug.
2. **Reproduce.** Get the exact command, input, environment and commit. Run it and paste the verbatim output and exit code into `.bequite/work/<id>/log.md`. No reproduction, no fix: collect more facts (versions, OS, env diff, logs) or ask for them.
3. **Expected vs actual**, one line each.
4. **Shrink.** Remove input, code and config until the failure is as small as it gets while still failing (delta debugging by hand: halve, test, keep the failing half).
5. **Locate in time.** If it used to work: `git log -S'<string>'` or `-G'<regex>'` when the symptom has a searchable string; otherwise `git bisect run <script>` (exit 0 good, 1-127 bad, 125 skip).
6. **Locate in space.** Read the code path end to end before editing: caller, handler, config, types. Check the layer that differs between the passing and failing environment first (`references/patterns.md`). Use a debugger (`breakpoint()`, browser DevTools) or targeted logs, not guesses.
7. **Name the root cause** in one sentence: the thing which, if changed, makes the symptom impossible. Ask "why" until you reach something the team controls (a process gap counts).
8. **Smallest fix.** One change aimed at the cause. No drive-by refactors, no touching unrelated files, no `catch` that hides the error.
9. **Regression test** (`bequite-testing-gate`): fails on the old code, passes on the fix, named after the bug.
10. **Verify**: re-run the original reproduction and the full suite; paste both. Symptom gone = done. Still there = back to step 6 with the new facts.
11. **Write back**: the log entry (verbatim error, root cause sentence, fix as file:line, proof), and a MISTAKE_MEMORY lesson when the trap is likely to recur. Three failed fix attempts in a row: stop and report to the user.

Wide reading (many logs, a large codebase, several hypotheses at once) can go to a subagent that returns only findings with file:line, so the main context stays on the fix.

## Worked example (real run on this repo, 2026-11-21)

Symptom: `python scripts/bq_check.py` exits 1 in a fresh worktree; the author's checkout exits 0.

```
repro (fresh worktree):  $ python scripts/bq_check.py   -> exit 1, "FAIL references_exist (1) .claude/commands/bq-motion.md:33: missing path `motion-library/inbox/New`"
expected / actual:       a clean clone passes the self-check / it fails
locate in time:          $ git log -S "motion-library/inbox/New" --oneline -- .claude/commands/bq-motion.md   -> 5259275
locate in space:         $ git check-ignore -v motion-library/inbox/New   -> .gitignore:117:motion-library/inbox/*
```

Root cause: the check tests paths against the working tree, and the cited folder is gitignored media. On the author's disk the untracked folder exists, so the check passes there and fails on every clean clone (CI included). Why it was not caught: nobody ran the check from a clean clone after 5259275. Fix, owned by the track that owns the file: cite the folder outside backticks, or make the check ignore gitignored paths. Process fix: run the self-check in a fresh worktree before merging.

## Quality gate

- The log holds the verbatim error, the reproduction command and its exit code.
- The root cause is one sentence and explains both the failing and the passing environment.
- The fix touches only what the cause needs; the diff is shown.
- A regression test failed before and passes after; the full suite is green; output pasted.
- No "should be fixed now". The symptom was re-run and is gone, or the report says PARTIAL.

## Boundaries

- Never change production, shared databases or servers to test a hypothesis; reproduce on a copy.
- Never delete or rewrite tests to make a failure disappear.
- A fix in a file owned by another track or person is handed over with the repro, not made in place.

## References (load on demand)

- `references/patterns.md`: symptom to likely cause table, environment-difference checklist, bisect script template, pitfalls from the SRE troubleshooting chapter.
