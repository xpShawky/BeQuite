---
description: One-line orientation. Shows current phase + last command + suggested next. Faster than /bequite (full menu). Read-only.
---

# /bq-now — quick orientation

## Purpose

Print the project's current state and the **single** suggested next command in one line. For daily-driver use when you don't want a full menu.

## When to use it

- Returning to a project mid-cycle and want to know where you left off
- Between commands; quick sanity check
- Faster than `/bequite` (which prints the full menu)
- Inside `/bq-auto` loops to verify progress

## When NOT to use it

- First-time setup (use `/bequite` for the full menu)
- When you need the recommendation rationale (use `/bequite`)
- When you need to choose between options (use `/bequite`)

## Syntax

```
/bq-now
```

No arguments.

## Preconditions

- `BEQUITE_INITIALIZED`

## Required previous gates

- None (read-only diagnostic)

## Files to read

- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/state/WORKFLOW_GATES.md`
- `.bequite/state/OPEN_QUESTIONS.md`

## Files to write

None. `/bq-now` is strictly read-only.

## Steps

### 1. Read state

Read the 5 files above. Identify:
- Current phase (`P0` … `P5` or `Cycle complete`)
- Current mode (one of 6, or `Not selected`)
- Last command + verdict (from `LAST_RUN.md`)
- Next unmet gate (first `❌ pending` in `WORKFLOW_GATES.md` for the current mode)
- Blockers (`[!]` entries in gates or open questions)

### 2. Compute next command

Apply the gate-aware recommendation logic from `/bequite`:
- If `BEQUITE_INITIALIZED` is `❌`: next = `/bq-init`
- If `MODE_SELECTED` is `❌`: next = `/bq-mode`
- Otherwise: next = first command that satisfies the next pending gate for the current mode

### 3. Print one line

Normal case:
```
P2 build · mode: Add Feature · last: /bq-implement T-2.3 ✓ · next: /bq-test
```

Blocker case:
```
⏸ blocker: PLAN_APPROVED ❌ pending · run /bq-plan
```

Fresh-install case:
```
BeQuite not initialized · run /bq-init
```

Cycle-complete case:
```
P5 done · mode: Add Feature · last: /bq-handoff ✓ · cycle complete · start new: /bq-feature "<title>"
```

## Output format

**A single line.** No menus. No tables. No verbose state dump.

If the user wants a full menu, they run `/bequite`.

## Quality gate

- Output is exactly one line (or a one-line blocker notice plus the resolve hint)
- Reflects actual state (re-read every invocation, no caching)
- Recommendation is gate-aware (matches `/bequite`'s recommendation logic)
- No banned weasel words

## Failure behavior

- BeQuite not initialized → `BeQuite not initialized · run /bq-init`
- State files unreadable → `State unreadable · run /bq-recover`
- Conflicting state (mode says X, phase says Y, mismatched) → `Inconsistent state · run /bq-recover`

## Memory updates

None. `/bq-now` is read-only.

## Log updates

None. `/bq-now` doesn't write to `AGENT_LOG.md` (it's a navigational helper, not an action).

## Usual next command

The command in the `next: ` field of the output.

## Tool neutrality (global rule)

This command makes no tool picks. Read-only. Nothing to install. See `.bequite/principles/TOOL_NEUTRALITY.md` for the global rule.
