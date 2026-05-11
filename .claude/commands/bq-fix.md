---
description: Fix a broken behavior. Reproduce first, identify root cause, fix the smallest cause, add or update test, verify, log to .bequite/logs/ERROR_LOG.md.
---

# /bq-fix — break the broken thing

You are diagnosing + fixing **one specific broken behavior**. Reproduce-first discipline. Smallest safe patch.

## Step 1 — Get the bug

If user typed `/bq-fix` alone, ask:
> "What's broken? Paste the error message, command, or describe the symptom."

If they passed an argument like `/bq-fix "login button does nothing on Safari"`, use that.

## Step 2 — Reproduce

**Before changing anything**, reproduce the bug:

- For a code-level error: run the failing command yourself
- For a UI bug: navigate to the page yourself (or describe what should happen vs what does)
- For a test failure: run the failing test in isolation
- For an env / config issue: re-run the setup

If you can't reproduce, ask the user for:
- Exact command they ran
- Exact error output
- OS / browser / runtime version
- Steps to reproduce

Do NOT proceed without reproduction. "I think I know what's wrong" is wrong — you've been wrong before.

## Step 3 — Capture the exact error

Save the verbatim error output to `.bequite/logs/ERROR_LOG.md`:

```markdown
## <ISO 8601 UTC> — <one-line symptom>

**Reproduced via:** <command or steps>
**Error output:**

```
<verbatim stderr or stack trace>
```

**Affected component:** <file or system>
```

## Step 4 — Find the root cause

Walk back from the error:

1. **What was the LAST thing that changed?** (git log; recent commits)
2. **Where in the code does this error originate?** (Read the stack trace; open the file at the offending line)
3. **What does that code DO?** (Read function + neighborhood; understand intent)
4. **What's wrong?** (the actual cause — not the symptom)

The root cause is the **smallest** change you can revert/fix that makes the symptom disappear.

**Common root-cause patterns:**
- Off-by-one
- Missing null/undefined check
- Wrong env var
- Wrong path (forward vs back slashes; absolute vs relative)
- Type mismatch
- Async race / missing await
- CORS / cross-origin
- Permissions / file system access
- Version mismatch between deps

## Step 5 — Fix the smallest cause

Make the smallest safe change that addresses the root cause. NOT a refactor. NOT "while I'm in here, let me also...". The fix only.

Read the file. Edit only what needs editing.

## Step 6 — Add or update a test

Every fix gets a test that **reproduces the bug**. The test should:

- Fail BEFORE the fix
- Pass AFTER the fix
- Have a name that describes the bug (`it("renders login button on Safari", ...)`)

If a test for this behavior already exists and was passing → it was missing a case. Add the case.

## Step 7 — Verify

Run the failing reproduction + the new test:

- Original symptom gone? (acceptance: the reproduction now succeeds)
- New test passes? (acceptance: green)
- Other tests still pass? (acceptance: no regressions in `npm test`)

## Step 8 — Log the fix to ERROR_LOG.md

Append below the original entry:

```markdown
**Root cause:** <one sentence>
**Fix:** <file:line + summary; ~3 lines of diff if helpful>
**Verification:**
- Reproduction now: passes
- New test: passes
- Full suite: <count pass / count total>
**Resolved:** <date>
```

## Step 9 — Update CHANGELOG (if user-visible)

If the bug was user-visible, append to `.bequite/logs/CHANGELOG.md` under [Unreleased]:

```markdown
### Fixed
- <one-line symptom + brief cause>
```

## Step 10 — Update state + report

- `.bequite/state/LAST_RUN.md` updated
- `.bequite/logs/AGENT_LOG.md` appended

Print to chat:

```
✓ Fixed — <symptom>

Root cause:   <one-liner>
Fix:          <file:line>
Test added:   <test name>
Suite:        <pass / total>

Logged: .bequite/logs/ERROR_LOG.md
```

## Rules

- **Reproduce first.** No fix without reproduction.
- **Smallest cause, smallest patch.** No refactors.
- **Always add a test.** A bug that escaped means the test was missing.
- **No "should fix" claims.** Verify the original symptom is actually gone.
- **One bug per /bq-fix.** Multiple bugs = multiple invocations.

This command pairs with the `bequite-problem-solver` skill — see `.claude/skills/bequite-problem-solver/SKILL.md` for the deeper diagnostic procedures (binary search, git bisect, etc.).

## Memory files this command reads

- The actual failing code + tests
- `.bequite/logs/ERROR_LOG.md` (prior entries for context)
- recent git log

## Memory files this command writes

- The fix (source file)
- A new or updated test
- `.bequite/logs/ERROR_LOG.md` (appended)
- `.bequite/logs/CHANGELOG.md` (appended if user-visible)
- `.bequite/logs/AGENT_LOG.md` (appended)
- `.bequite/state/LAST_RUN.md` (updated)

## Usual next command

- `/bq-test` — full suite to confirm no regressions
- `/bq-implement` — continue task list if you were mid-implementation when the bug hit
- `/bq-fix` — if another bug surfaced during the fix
