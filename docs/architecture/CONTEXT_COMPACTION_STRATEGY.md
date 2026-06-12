# Context Compaction Strategy

Long tasks die of context rot, not lack of skill. This strategy adds **pressure-triggered compaction** to the alpha.18 context-engineering layer (`CONTEXT_ENGINEERING.md` + `bequite-context-engineer` — still canonical for the primitives; this doc adds the thresholds and the compact format). Operational copy: `.bequite/state/CONTEXT_COMPACTION_RULES.md`.

## 1. Pressure thresholds (approximate — act early, not exactly)

| Pressure | Action |
|---|---|
| **~40%** | create/refresh the compact working summary (`CONTEXT_SUMMARY.md`) |
| **~60%** | externalize decisions → `DECISIONS.md`, assumptions → `ASSUMPTIONS.md`, file map + task state → `WORKING_NOTES.md` + `CURRENT_TASK.md` |
| **~75%** | stop STARTING new tasks; finish current task's writeback |
| **~85%** | write a handoff (compact block below + LAST_RUN) and ask the user to continue in a fresh session |

Auto mode checks pressure at every task boundary (orchestration step 6). Manual commands check before any multi-file task.

## 2. The standing laws

Never rely on chat memory alone for critical project facts. Canonical homes: facts → `.bequite/state/CONTEXT_SUMMARY.md` · active work → `WORKING_NOTES.md` · current task → `.bequite/tasks/CURRENT_TASK.md` (created on first use) · decisions → `DECISIONS.md` · unresolved assumptions → `ASSUMPTIONS.md`. A fact that exists only in conversation is one compaction away from gone.

## 3. Context Compact output format

```
Context Compact:
- User goal:
- Current phase:
- Current command:
- Selected skills:
- Files inspected:
- Files changed:
- Decisions made:
- Open questions:
- Current task:
- Next action:
- Risks:
- Confidence:
- Evidence logged:
```

Written to `CONTEXT_SUMMARY.md` at every threshold crossing and before any planned `/compact` or session end. `/bq-recover` reads it first when resuming.
