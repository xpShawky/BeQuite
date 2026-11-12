# Context Compaction Rules (operational card)

Strategy: `.claude/bequite/docs/architecture/CONTEXT_COMPACTION_STRATEGY.md` · primitives: `CONTEXT_ENGINEERING.md` + `bequite-context-engineer`.

| Pressure | Do |
|---|---|
| ~40% | write/refresh compact summary → `CONTEXT_SUMMARY.md` |
| ~60% | externalize: decisions→`DECISIONS.md` · assumptions→`ASSUMPTIONS.md` · file map + active work→`WORKING_NOTES.md` · task→`.bequite/tasks/CURRENT_TASK.md` |
| ~75% | stop starting new tasks; finish current writeback |
| ~85% | write handoff (Context Compact block + LAST_RUN); ask user for fresh session |

**Laws:** critical facts never live only in chat · check pressure at every task boundary · `/bq-recover` reads CONTEXT_SUMMARY first.

```
Context Compact:
- User goal:            - Decisions made:
- Current phase:        - Open questions:
- Current command:      - Current task:
- Selected skills:      - Next action:
- Files inspected:      - Risks:
- Files changed:        - Confidence:
                        - Evidence logged:
```
