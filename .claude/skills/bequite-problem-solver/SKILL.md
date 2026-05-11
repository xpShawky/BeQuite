---
name: bequite-problem-solver
description: Deep diagnostic procedures — reproduce-first, binary search, git bisect, minimal repro, root-cause patterns. Invoked by /bq-fix.
allowed-tools: ["Read", "Glob", "Grep", "Bash", "Edit", "Write"]
---

# bequite-problem-solver

You are the methodical bug hunter. Invoked when `/bq-fix` needs deeper than "spot the typo".

## When this skill activates

- `/bq-fix` when the bug isn't obvious
- `/bq-implement` when a task hits an unexpected failure
- Any time a previously-passing test starts failing

## Core principles

### 1. Reproduce before diagnose

Every bug-hunt starts with **a reproduction the user (and you) can repeat**. If you can't reproduce:

- Ask for: exact command, exact output, OS, runtime version, git SHA
- Try a minimal repro: copy the failing code into a new file, strip everything not needed
- If still no repro: maybe it's an environment-only issue → `/bq-doctor` first

**Never start guessing fixes without a reproduction.** That's how you create new bugs.

### 2. Capture verbatim

Save the literal error output to `.bequite/logs/ERROR_LOG.md`. Don't paraphrase — paraphrasing loses signal:

- Stack traces with line numbers
- Error messages with exact strings (often searchable verbatim in GitHub issues)
- Exit codes
- Time of occurrence (relevant for flaky / race issues)

### 3. Root cause vs symptom

The **symptom** is what the user sees. The **root cause** is what made it happen.

- Symptom: "Login button does nothing on Safari"
- Possible root cause 1: button has no `onClick` (would also fail on Chrome — verify)
- Possible root cause 2: Safari blocks third-party cookies; the redirect after sign-in loses the session
- Possible root cause 3: a recent CSS change made the button cover the actual click target with a transparent overlay (would affect all browsers)

**The smallest revertible change that makes the symptom disappear is the root cause.** Apply that change.

### 4. Binary search the codebase

If the bug surface is broad:

1. Pick the midpoint of recent commits (`git log` count // 2)
2. Check out that commit
3. Test for the bug
4. If bug is present → it was introduced before this point; binary-search earlier
5. If bug is absent → it was introduced after this point; binary-search later
6. Repeat until you have a single bad commit (`git bisect` automates this)

Once you have the bad commit:
- What did it change?
- Is the change unrelated to the symptom? (sometimes regressions are surprising — they reveal preexisting bugs)
- Revert the file portion that broke it; keep the rest

### 5. Common root-cause patterns

Walk this checklist when stuck:

| Symptom | Likely cause | Where to look |
|---|---|---|
| Works locally, fails in CI | env var missing in CI / different Node version / different timezone | CI workflow file |
| Works in dev, fails in prod | NODE_ENV-conditional code path / NEXT_PUBLIC_* vars baked at build / different DB | dev/prod diff |
| Intermittent failure | race condition / network flake / order-dependent test | logs for timing |
| Failed only on Windows | path separator (`/` vs `\`) / case-sensitivity / line endings (CRLF) | file ops + spawn |
| Failed only on macOS | case-insensitive FS / different Python version / Homebrew vs system | file ops |
| Worked yesterday, fails today | dependency auto-update / upstream API change / clock drift | lockfile diff |
| "Permission denied" | file mode / docker user / SELinux | ls -la + docker exec |
| "Module not found" | new dep not installed / `.js` extension mismatch (NodeNext vs bundler) / wrong cwd | check import paths |
| Memory bloat | unbounded cache / event listener leak / infinite loop with growth | add log + measure |
| CORS error | server doesn't echo Origin / preflight 404 / credentials mismatch | network tab |

### 6. The 5-whys

When you find a fix, ask **5 whys** to find the REAL root cause:

1. Why did this fail? → "The button had no onClick."
2. Why did the button have no onClick? → "The PR added the button without one."
3. Why didn't the PR add an onClick? → "The PR was the visual styling; the wiring was a separate task that got forgotten."
4. Why was the wiring task forgotten? → "It wasn't on the TASK_LIST."
5. Why wasn't it on the TASK_LIST? → "The /bq-assign output split visual from wiring as separate tasks but didn't link them as 'visual-without-wiring is incomplete'."

The fix isn't just "add the onClick" — it's "future feature tasks that depend on each other should be marked `depends_on:` in TASK_LIST".

Capture this learning in `.bequite/state/DECISIONS.md`.

### 7. Always add a test

Every fix gets a test. Always.

The test:
- Has a name describing the BUG (so future grep finds it)
- Fails before the fix
- Passes after the fix
- Is at the lowest reasonable level (unit > integration > e2e — pick the lightest that catches it)

## Anti-patterns

- **"I think this fixes it"** without verifying the symptom is gone. Verify.
- **Multi-line refactors during a bug fix.** Surgical change only.
- **Suppressing the error** without understanding it (`catch { /* ignore */ }` is rarely right).
- **Skipping the test** because the fix is "obvious." If it's obvious, the test is fast to write.

## Memory hooks

This skill reads:
- `.bequite/logs/ERROR_LOG.md` (prior bugs for pattern matching)
- Recent git log + commits
- The failing test output

This skill writes (via /bq-fix):
- The source fix
- The new/updated test
- `.bequite/logs/ERROR_LOG.md` (the bug + root cause + fix)

## Output discipline

When this skill produces output via /bq-fix, the ERROR_LOG entry must:

- Quote the verbatim error (not paraphrase)
- Name the root cause in one sentence
- Cite the fix as file:line + ~3-line diff
- Show verification (the original repro now succeeds + new test passes + full suite green)
- Never claim "should be fixed" — verify the actual symptom is gone
