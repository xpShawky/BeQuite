---
name: bequite-guard-pass
description: Use after code, tests, docs or a creative deliverable are produced and before /bq-verify, /bq-release or any claim that the work is right. A second, independent pass that hunts the failure modes generated work shows (invented APIs, faked success, tests that test nothing, docs that drift). This is the procedure the bq-verifier subagent runs.
last_verified: 2026-11-21
sources:
  - https://github.com/amElnagdy/guard-skills
  - https://code.claude.com/docs/en/sub-agents
  - https://www.anthropic.com/engineering/building-effective-agents
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
---

# bequite-guard-pass

The builder is the worst judge of its own work: long-running agents are known to mark features done without testing them end to end. The guard is a separate reader that sees the result and the acceptance criteria, not the builder's reasoning, and tries to prove the work wrong.

## When to use

- After `/bq-implement`, `/bq-feature`, `/bq-fix`, `/bq-test`; before `/bq-verify` and `/bq-release`; on `/bq-review` of generated diffs.
- Before any "the docs are accurate" claim.

Not for: style while writing (it is reactive); unchanged code; replacing `/bq-review` (review checks the spec, guard hunts failure modes).

## How it runs

- **Independent:** run it in the `bq-verifier` subagent (read-only tools, its own context). Give it the diff (`git diff <base>...HEAD`), the task's acceptance criteria and the commands to run. Not the builder's notes.
- **Severity-gated:** flag only what breaks correctness, the stated requirements, or a hard rule. A guard told to "find problems" invents them.
- **Citation-or-strike:** every finding quotes `path:line`. No quote, no finding.

## The guards

**Code:** imported symbols and methods exist in the installed version (check the package source or docs, not memory) · no hard-coded success (a status or return that cannot fail) · no swallowed errors (`except: pass`, empty `catch`) · no copy-from-sibling bugs (stale names, conditions) · names match behaviour; callers match signatures · no abstraction with one user.

**Tests:** a test fails when the feature is removed (delete or break the line, run, restore) · mocks do not replace the thing under test · assertions check values, not truthiness · skipped or `todo` tests are not counted as passing · every fixed bug has a regression test.

**Docs:** every command, flag, file and function named exists · examples run as written · counts match the tree · the changelog matches the diff · install steps work in an empty folder.

**Creative output:** defer to `bequite-human-taste` (reference-first doctrine): side-by-side with the references exists, the tell sweep for the medium ran, the phone check or blind pick is recorded.

## Procedure

1. Collect the diff, acceptance criteria and run commands; list the files in scope.
2. Run the checks that are commands first (tests, linters, `python scripts/bq_check.py`, the counts below); paste exit codes.
3. Read each changed file against the guard lists. Quote each finding.
4. Write `work/<id>/review.md`: per finding the guard, severity (blocking / fix / note), `path:line` quote, the fix. Verdict PASS, FINDINGS (n) or BLOCKED.
5. Report only; fixes are applied by the builder after the user or the gate allows.

## Worked example (docs guard, run on this repo, 2026-11-21)

```
$ ls .claude/commands/*.md | wc -l        -> 55   (v1: core 45, studio 5, business 5)
$ ls -d .claude/skills/*/ | wc -l          -> 38
$ grep -n -E "[0-9]+ (commands|skills)" CLAUDE.md README.md commands.md   # every count must match `python scripts/bq_check.py counts_match`
CLAUDE.md:13, CLAUDE.md:14, README.md:9, README.md:10, commands.md:3
```

Verdict: PASS for counts. Coverage stated: three files, two counts. The same guard on this track's own draft caught that the old anti-hallucination skill quoted "~22% measured vs ~77% predicted" from a page that has no such number: struck.

## Quality gate

- A PASS states what was checked (files, guards, commands). "No findings" without coverage is itself an unsupported claim.
- Every finding has a quote; every command has an exit code.
- The guard did not edit the work it judged.

## Boundaries

Markdown procedure only: no scripts, network or credentials of its own. Platform-specific guards (WordPress, payments) are added per project when needed.
