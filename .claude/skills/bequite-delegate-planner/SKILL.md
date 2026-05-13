---
name: bequite-delegate-planner
description: Delegate Mode workflow — strong model architects + writes implementation task packs that a cheaper / smaller model can implement safely, then strong model reviews. Cost-saving without quality loss. Invoked by /bq-auto delegate, /bq-plan delegate, /bq-assign delegate, /bq-review delegate. Cross-session: planner writes a task pack the implementer reads in a separate Claude session.
allowed-tools: Read, Glob, Grep, Edit, Write
---

# bequite-delegate-planner — strong model plans, cheaper model implements

## Purpose

Encode the **Delegate Mode** workflow:

1. **Strong model** (Opus, GPT-5, similar) does architecture, research, splits work into atomic tasks with exact instructions, acceptance criteria, and test commands.
2. **Cheaper model** (Sonnet, Haiku, or a smaller open model) implements **exactly** from the task pack — no architectural decisions, no guessing.
3. **Strong model** reviews the implementation diff. Fixes or asks for fixes. Final verify runs.

The intent: **cost savings** without **quality loss**. The strong model's expensive tokens are concentrated on the thinking parts; the cheap model's tokens carry the mechanical work.

Invoked by `/bq-auto delegate`, `/bq-plan delegate`, `/bq-assign delegate`, `/bq-review delegate`.

---

## When to use this skill

- A feature is large enough that the cost of running the strong model end-to-end is high
- The work has a **clear architectural shape** but lots of mechanical implementation
- You're willing to do a **two-session handoff** (Plan → switch model → Implement → switch back → Review)
- You can articulate acceptance criteria precisely enough that a weaker model can execute

## When NOT to use this skill

- Tiny tasks (just use `/bq-fix fast` — overhead isn't worth it)
- Exploratory / research-heavy work (the cheap model can't make discovery decisions)
- Anything requiring real-time judgment (UX iteration, design taste, security trade-offs)
- One-shot urgent fixes (handoff overhead delays)
- Highly regulated work where every line needs senior eyes (just use `--mode deep`)

---

## The three phases

### Phase 1 — Architect (strong model)

Inputs: project memory + user task description.

Strong model produces a **task pack** at `.bequite/tasks/`:

| File | Contents |
|---|---|
| `DELEGATE_TASKS.md` | Atomic task list with IDs (T-D-1, T-D-2, ...). Each task ≤5min for the cheap model. |
| `DELEGATE_INSTRUCTIONS.md` | Per-task: goal, files to inspect, files to edit, files NOT to touch, exact implementation steps, edge cases, common mistakes, rollback notes |
| `DELEGATE_ACCEPTANCE_CRITERIA.md` | Per-task: observable success conditions (testable) |
| `DELEGATE_TEST_PLAN.md` | Per-task: exact test command(s) to run + expected output |

Strong model also:
- Identifies hard human gates (destructive ops, secret handling, prod touches) and marks tasks that touch them — cheap model MUST pause at those tasks
- Notes tool-neutrality decisions already made (cheap model uses chosen tools, doesn't re-decide)
- Provides 2-3 example task completions in the task pack so cheap model has a pattern to follow

Strong model exits + writes to `LAST_RUN.md`:
> "Delegate task pack ready. Switch to implementer model + run `/bq-implement delegate` to start T-D-1."

### Phase 2 — Implement (cheaper model)

User switches Claude model (Sonnet → Haiku, or different host/account).

Cheaper model runs `/bq-implement delegate` (mode flag triggers delegate-implementer behavior):
- Reads task pack
- Picks next `[ ] pending` task
- Reads ONLY the files in "Files to inspect" + "Files to edit"
- Applies the exact implementation steps
- Runs the exact test command
- Marks task `[x]` if test passes
- Stops on:
  - Test fails after 2 retries → mark `[!]` blocked, log
  - Banned weasel word in own output
  - File not listed in "Files to edit" needs changing → mark `[?]` clarification needed
  - Hard human gate hit → pause for user

Cheaper model DOES NOT:
- Make architectural decisions
- Install new dependencies (already decided in Phase 1)
- Edit files not listed in task instructions
- Refactor "while in here"
- Skip tests

### Phase 3 — Review (strong model)

User switches back to strong model.

Strong model runs `/bq-review delegate`:
- Reads `git diff` since Phase 2 start
- Cross-references with `DELEGATE_INSTRUCTIONS.md` per task
- Checks: file placement / function design / naming / integration / tests / security / regressions / UX (if relevant) / docs+log updates / weasel words
- Writes `.bequite/audits/DELEGATE_REVIEW_REPORT.md`:
  - Per task: ✅ approved / ⚠ approved-with-comments / ❌ rejected
  - Per rejection: specific fix instructions
  - Overall verdict

If rejections exist:
- User decides: strong model fixes inline, OR sends back to cheaper model with corrections appended to instructions
- Re-run cycle until verdict is "approved"

After approval: run `/bq-verify` for full gate matrix.

---

## Task pack format (what strong model writes)

### `DELEGATE_TASKS.md`

```markdown
# Delegate Tasks — <feature name>

**Generated:** <ISO 8601 UTC>
**Strong model:** <e.g. Claude Opus 4.7>
**Recommended implementer:** Claude Sonnet 4.5 or similar
**Total tasks:** <N>
**Estimated cheap-model tokens:** <range>

## Task list

- [ ] T-D-1 — <one-line goal>
  - File: <primary file>
  - Acceptance: <one criterion>
  - Hard gate: <none | name>
  - Est. cheap-model time: <minutes>

- [ ] T-D-2 — ...
```

### `DELEGATE_INSTRUCTIONS.md`

```markdown
# Delegate Instructions

For the implementer model. Read this file before each task. Read ONLY the files listed per task. Follow steps exactly. Don't refactor. Don't decide architecture. Don't install deps.

---

## T-D-1: <one-line goal>

**Why this task exists:** <one sentence>

**Files to inspect (read-only):**
- `<path>` — to understand context

**Files to edit:**
- `<path>` — see steps below

**Files NOT to touch:**
- (default: everything else)
- specifically guarded: <list>

**Implementation steps:**
1. Open `<file>`; find the section "<anchor>"
2. Add `<code snippet>` after line containing `<text>`
3. Make sure imports include `<import>`
4. Save.

**Edge cases:**
- If `<edge case>`, handle by `<approach>`
- If `<other edge case>`, mark task `[?]` and exit

**Common mistakes (from MISTAKE_MEMORY.md):**
- <pattern> — avoid by <rule>

**Rollback if it goes wrong:**
- `git checkout -- <file>`

---

## T-D-2: ...
```

### `DELEGATE_ACCEPTANCE_CRITERIA.md`

```markdown
# Delegate Acceptance Criteria

Observable, testable success conditions per task.

## T-D-1
- [ ] `<test command>` exits 0
- [ ] File `<path>` contains `<expected content>`
- [ ] No banned weasel words in commit message
- [ ] No new dependencies added

## T-D-2
- ...
```

### `DELEGATE_TEST_PLAN.md`

```markdown
# Delegate Test Plan

Run after EACH task. The implementer doesn't move to the next task until the current one passes.

## T-D-1
```bash
npm test -- --testNamePattern="<specific test>"
```
Expected: 1 test passed, 0 failed.

## T-D-2
```bash
<command>
```
Expected: <output>
```

### `.bequite/audits/DELEGATE_REVIEW_REPORT.md` (Phase 3)

```markdown
# Delegate Review Report

**Generated:** <ISO 8601 UTC>
**Reviewer (strong model):** <e.g. Claude Opus 4.7>
**Implementer:** <e.g. Claude Sonnet 4.5>
**Tasks reviewed:** <N>

## Verdict
**Overall: APPROVED | APPROVED-WITH-COMMENTS | REJECTED**

## Per-task review

### T-D-1: ✅ APPROVED
- file placement: ✓
- function design: ✓
- naming: ✓
- integration: ✓
- tests: ✓ (1 pass)
- security: ✓
- regressions: none detected
- docs/log updates: ✓

### T-D-2: ⚠ APPROVED-WITH-COMMENTS
- naming: function name `handleStuff` is too generic → recommend `handleBookingExport`
- tests: pass but missing edge case for empty result → add follow-up test

### T-D-3: ❌ REJECTED
- **Reason:** modified `app/api/auth/route.ts` — was NOT in "Files to edit" list
- **Fix instructions:** revert that change; the auth route isn't part of this feature
- **Re-run:** `/bq-implement delegate T-D-3` after fix

## Action items
1. Revert app/api/auth/route.ts → original state
2. Add follow-up test for T-D-2 empty case
3. Rename `handleStuff` → `handleBookingExport`

## Final verify recommendation
Run `/bq-verify` after action items above are complete.
```

---

## Mode composition

Delegate mode composes with other modes:

| Combination | Behavior |
|---|---|
| `delegate` alone | Standard delegate (balanced research depth in Phase 1) |
| `deep delegate` | **Strongly recommended** for new features — strong model does 11-dim research + writes the task pack |
| `fast delegate` | Phase 1 uses Fast Mode shallow research; suitable for well-understood features |
| `token-saver delegate` | Phase 1 reuses cached research / discovery; suitable for follow-up tasks |
| `delegate uiux` | Delegate works for UI tasks too — strong model writes section-mapped instructions; cheap model edits per section |

---

## Hard human gates inside delegate workflow

Hard gates from `/bq-auto`'s 17-gate list still apply at the IMPLEMENTATION phase. If a delegate task involves:
- Destructive deletion / DB migration / production change / VPS-Nginx-SSL / paid service / secret handling / auth model / architecture / etc.

The strong model MUST flag the task in `DELEGATE_INSTRUCTIONS.md` with:

```markdown
**⏸ HARD GATE:** This task touches <gate type>. Implementer model MUST pause + wait for user confirmation before executing.
```

Cheaper model honors the pause. Strong model's review at Phase 3 verifies the gate was respected.

---

## Common mistakes to avoid

- ❌ Cheap model makes architectural decisions ("I think we should restructure this") — refuse; flag task `[?]`
- ❌ Cheap model installs deps not in task instructions — refuse
- ❌ Cheap model edits files not in "Files to edit" list — refuse; flag task `[?]`
- ❌ Strong model skips Phase 3 review — final verify alone isn't enough
- ❌ Strong model writes vague instructions that require cheap-model judgment — re-write tighter
- ❌ User runs `/bq-auto delegate` with NO research yet — strong model should run discovery first
- ❌ Implementer model claims "looks good" without running the test command — review will catch + reject

---

## Failure handling

| Failure | Recovery |
|---|---|
| Cheap model marks 3+ tasks `[?]` | Task pack is too vague; strong model re-writes those instructions tighter |
| Cheap model marks task `[!]` blocked | User decides: strong model fixes, OR strong model rewrites task |
| Phase 3 review finds architectural drift | REJECTED; revert + re-instruct; consider re-running with `deep delegate` if drift was caused by ambiguity |
| Strong model task pack > 20 tasks | Split into sub-features; deliver one feature pack at a time |
| Tests pass but review finds quality issues | APPROVED-WITH-COMMENTS; user decides if cheap model should fix or strong model handles |

---

## Memory updates

- `.bequite/tasks/DELEGATE_TASKS.md` (Phase 1)
- `.bequite/tasks/DELEGATE_INSTRUCTIONS.md` (Phase 1)
- `.bequite/tasks/DELEGATE_ACCEPTANCE_CRITERIA.md` (Phase 1)
- `.bequite/tasks/DELEGATE_TEST_PLAN.md` (Phase 1)
- `.bequite/audits/DELEGATE_REVIEW_REPORT.md` (Phase 3)
- `.bequite/state/MODE_HISTORY.md` (per-run; tracks what mode was used + outcome)
- `.bequite/state/LAST_RUN.md` (after each phase)
- `.bequite/logs/AGENT_LOG.md` (each phase entry)

---

## Cost discipline

Strong model should produce a **cost estimate** at Phase 1 end:

```
Phase 1 (this session, strong model): ~<X> tokens, ~$<Y>
Phase 2 (separate session, cheap model): ~<Z> tokens, ~$<W>  estimated
Phase 3 (this session continued, strong model review): ~<A> tokens, ~$<B>

Total estimated: ~$<sum>
vs. running strong model end-to-end: ~$<comparison>
Savings: ~<%>
```

If savings < 30%, recommend NOT using delegate (overhead isn't worth it).

---

## What this skill does NOT do

- Replace `/bq-multi-plan` (that's two strong models cross-checking each other; this is one strong + one cheap)
- Solve every multi-model workflow (only the strong-plans-cheap-implements pattern)
- Provide judgment for design taste, security trade-offs, UX feel — those stay with the strong model
- Auto-switch models (the user manually switches Claude models between phases)

---

## See also

- `docs/architecture/AUTO_MODE_STRATEGY.md` §"Mode flags" + §"Mode composition"
- `bequite-multi-model-planning` skill — related but different (two strong models thinking independently)
- `bequite-workflow-advisor` skill — recommends when delegate mode fits
- `.claude/commands/bq-auto.md` — the entry point for `delegate` mode
