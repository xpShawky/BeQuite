---
description: Fix a broken behavior. 15-type problem router. Reproduce first → identify type → activate matching specialist skills → root cause → smallest patch → add test → verify symptom is gone → log to ERROR_LOG.md.
---

# /bq-fix — diagnose + repair, with type router

## Purpose

Fix **one specific broken behavior**. The command classifies the problem into one of 15 types and activates the matching specialist skills. Reproduce-first discipline. Smallest safe patch. Always a regression test.

## When to use it

- Anything broken: error, wrong output, performance regression, security issue, UX regression
- A test went red and you don't know why
- Production incident (with `bequite-problem-solver` skill in heavy mode)

## Preconditions

- `BEQUITE_INITIALIZED ✅`
- Code exists (the bug has to be in something)

## Required previous gates

- `BEQUITE_INITIALIZED`
- `MODE_SELECTED` (Fix Problem mode — or any mode mid-cycle)

## Files to read

- `.bequite/logs/ERROR_LOG.md` (prior entries for context)
- recent `git log`
- the failing code + tests

## Files to write

- The fix (source file)
- A new or updated regression test
- `.bequite/logs/ERROR_LOG.md` (appended)
- `.bequite/logs/CHANGELOG.md` (appended if user-visible)
- `.bequite/audits/FIX_<slug>.md` (mini-spec for the fix)
- `.bequite/tasks/CURRENT_TASK.md`
- `.bequite/state/WORKFLOW_GATES.md` (`FIX_DONE ✅`)
- `.bequite/logs/AGENT_LOG.md`
- `.bequite/state/LAST_RUN.md`

## Steps

### 1. Get the bug

If user typed `/bq-fix` alone:
> "What's broken? Paste the error message, command, or describe the symptom."

If `/bq-fix "login button does nothing on Safari"` — use that.

### 2. Classify the problem (15 types)

Ask the model (silently) to classify into one of:

| # | Type | Activates skill(s) |
|---|---|---|
| 1 | **Frontend bug (visual / state)** | `bequite-frontend-quality`, `bequite-problem-solver` |
| 2 | **Backend bug (API / logic)** | `bequite-backend-architect`, `bequite-problem-solver` |
| 3 | **Database bug (query / data)** | `bequite-database-architect`, `bequite-problem-solver` |
| 4 | **Auth bug (login / permissions)** | `bequite-security-reviewer`, `bequite-backend-architect` |
| 5 | **Build / compile error** | `bequite-problem-solver`, `bequite-testing-gate` |
| 6 | **Test failure** | `bequite-testing-gate`, `bequite-problem-solver` |
| 7 | **Deployment / CI bug** | `bequite-devops-cloud`, `bequite-problem-solver` |
| 8 | **Performance regression** | `bequite-problem-solver`, `bequite-backend-architect` |
| 9 | **Security vulnerability** | `bequite-security-reviewer` |
| 10 | **Dependency / package issue** | `bequite-problem-solver`, `bequite-project-architect` |
| 11 | **Configuration / env bug** | `bequite-devops-cloud`, `bequite-problem-solver` |
| 12 | **Network / integration bug** | `bequite-backend-architect`, `bequite-problem-solver` |
| 13 | **Memory leak / resource issue** | `bequite-problem-solver`, `bequite-backend-architect` |
| 14 | **Race condition / async bug** | `bequite-problem-solver`, `bequite-backend-architect` |
| 15 | **Cross-browser / platform bug** | `bequite-frontend-quality`, `bequite-problem-solver` |

Print the classification + which skills will be active. Ask: "Correct? (y/N + correction)"

### 3. Reproduce

**Before changing anything**, reproduce the bug:

- Code-level error: run the failing command yourself
- UI bug: navigate to the page yourself
- Test failure: run the failing test in isolation
- Env / config issue: re-run the setup
- Performance: run a benchmark with the regression visible

If you can't reproduce, ask the user for:
- Exact command run
- Exact error output
- OS / browser / runtime version
- Steps to reproduce

**Do NOT proceed without reproduction.** "I think I know what's wrong" is wrong — you've been wrong before.

### 4. Capture the exact error

Save verbatim error output + reproduction steps to `ERROR_LOG.md`:

```markdown
## <ISO 8601 UTC> — <one-line symptom>

**Type:** <1 of 15>
**Reproduced via:** <command or steps>
**Error output:**

```
<verbatim stderr or stack trace>
```

**Affected component:** <file or system>
**Activated skills:** <list>
```

### 5. Write the fix mini-spec

Save to `.bequite/audits/FIX_<slug>.md`:

```markdown
# Fix: <symptom>

**Generated:** <date>
**Type:** <classification>
**Active skills:** <list>

## Symptom

(one paragraph)

## Reproduction

(steps + expected vs actual)

## Hypothesis

(2-3 possible causes, ranked by likelihood)

## Files this fix will touch

| File | Why |
|---|---|

## Test plan

- The reproduction (currently fails) will pass
- New regression test: <name>
- Suite: no new failures

## Rollback

(if fix is wrong, how to revert in one step)
```

### 6. Find the root cause

Walk back from the error:

1. **What was the LAST thing that changed?** (`git log`)
2. **Where in the code does this error originate?** (Read the stack trace; open the file at the offending line)
3. **What does that code DO?** (Read function + neighborhood; understand intent)
4. **What's wrong?** (the actual cause — not the symptom)

The root cause is the **smallest change** that makes the symptom disappear.

**Common root-cause patterns per type:**

- Frontend: stale prop, missing useEffect dep, CSS specificity, hydration mismatch
- Backend: missing await, wrong env var, type coercion, missing null check
- Database: missing index, wrong join, N+1, transaction isolation
- Auth: cookie not set, CORS, redirect URL mismatch, expired token
- Build: peer dep mismatch, missing types, wrong path alias
- Test: order-dependent test, leaky fixture, time-dependent
- Deployment: env var missing, wrong region, build cache stale
- Performance: missing index, sync I/O in hot path, no caching
- Security: input not sanitized, exposed secret, OWASP-Top-10 hit
- Dependency: transitive CVE, version pin missing, AGPL leak
- Config: typo in env var name, path separator (Windows vs Unix), permissions
- Network: timeout, retry not configured, certificate
- Memory: closure holding ref, unbounded array, missing cleanup
- Race: missing lock, await order, fire-and-forget
- Cross-browser: vendor prefix, polyfill missing, BOM differences

### 7. Fix the smallest cause

Make the smallest safe change that addresses the root cause. NOT a refactor. NOT "while I'm here...".

Read the file. Edit only what needs editing.

### 8. Add or update a regression test

Every fix gets a test that **reproduces the bug**:

- Fails BEFORE the fix
- Passes AFTER the fix
- Has a name that describes the bug (`it("renders login button on Safari", ...)`)

If a test for this behavior already existed and was passing → it was missing a case. Add the case.

### 9. Verify

Run the failing reproduction + the new test:

- Original symptom gone? (the reproduction now succeeds)
- New test passes?
- Other tests still pass? (no regressions in full suite)

### 10. Log the fix

Append to ERROR_LOG.md below the original entry:

```markdown
**Root cause:** <one sentence>
**Fix:** <file:line + summary; ~3 lines of diff if helpful>
**Verification:**
- Reproduction now: passes
- New test: passes (`<test name>`)
- Full suite: <count pass / count total>
**Resolved:** <date>
```

### 11. Update CHANGELOG (if user-visible)

If the bug was user-visible, append to `CHANGELOG.md` under `[Unreleased]`:

```markdown
### Fixed
- <one-line symptom + brief cause>
```

### 12. Update state + report

- Mark `FIX_DONE ✅` in `WORKFLOW_GATES.md`
- `LAST_RUN.md` updated
- `AGENT_LOG.md` appended

Print to chat:

```
✓ Fixed — <symptom>

Type:         <classification>
Active skills:<list>
Root cause:   <one-liner>
Fix:          <file:line>
Test added:   <test name>
Suite:        <pass> / <total>

Logged: .bequite/logs/ERROR_LOG.md
        .bequite/audits/FIX_<slug>.md
```

## Output format

Narrate each step. Highlight the classification + activated skills early so user can correct.

## Quality gate

- Reproduction confirmed BEFORE any code change
- Type classified (1 of 15)
- Root cause stated in one sentence
- Smallest patch (no refactor, no "while I'm here")
- Regression test added (fails before, passes after)
- Full suite green (no new failures)
- ERROR_LOG.md entry complete
- No banned weasel words

## Failure behavior

- Can't reproduce → log the symptom, ask user for more details, exit
- Root cause unclear after 30 minutes → pause, ask user, consider `/bq-research` for the specific tech
- Fix breaks other tests → roll back, log, retry with a different approach
- Type classification wrong → user corrects, re-route to different skills

## Rules

- **Reproduce first.** No fix without reproduction.
- **Smallest cause, smallest patch.** No refactors.
- **Always add a test.** A bug that escaped means the test was missing.
- **No "should fix" claims.** Verify the original symptom is actually gone.
- **One bug per /bq-fix.** Multiple bugs = multiple invocations.

## Skills activated

Per the 15-type table above. Always plus `bequite-problem-solver` (the reproduce-first discipline core).

## Usual next command

- `/bq-test` — full suite to confirm no regressions
- `/bq-implement` — continue task list if mid-implementation when bug hit
- `/bq-fix` — if another bug surfaced during the fix
- `/bq-changelog` — if you fixed a user-visible bug and want to sharpen the entry

---

## Tool neutrality (global rule)

⚠ **A fix should rarely introduce a new tool. If it does, the fix mini-spec must include a decision section before the patch lands.**

The smallest-cause / smallest-patch discipline means most fixes use existing project tooling. If a fix tempts you to "let's add library X to handle this properly" — pause. Either the existing stack solves it, or the fix is larger than a fix (becomes a feature).

**Do not write in the FIX mini-spec:** "Add Zod for validation."
**Write:** "Zod is one candidate to address the validation gap. Compared against [alternatives]; chosen because [reasons]; risk [X]; rollback [Y]."

The 10 decision questions every new dep introduced during a fix must answer:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

**Default for fixes:** use what's already installed. Adding a dep during a fix is a flag — re-scope as a feature if the dep is structural.

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.
