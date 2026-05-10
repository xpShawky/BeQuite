# Active Context: {{PROJECT_NAME}}

> The most-edited file in `.bequite/memory/`. Captures what is happening **right now**: which feature, which phase, which task, what's blocked, what's next.
>
> **Update at the end of every task** (Article III). At the end of every phase, append-snapshot to `.bequite/memory/prompts/v<N>/`.

---

## Now (last edited: {{TIMESTAMP_UTC}})

- **Active feature:** `{{ACTIVE_FEATURE}}`
- **Active phase:** `{{ACTIVE_PHASE}}`  (P0 Research / P1 Stack / P2 Plan / P3 Phases / P4 Tasks / P5 Implement / P6 Verify / P7 Handoff)
- **Active task ID:** `{{ACTIVE_TASK}}`
- **Active mode:** `{{ACTIVE_MODE}}`  (slow / fast / auto)
- **Skeptic gate state:** `{{SKEPTIC_STATE}}`  (pending / open-questions / cleared)
- **Last green sub-version:** `{{LAST_GREEN_VERSION}}`
- **Cost-ceiling status:** `{{COST_USED}} / {{COST_CEILING}} USD`
- **Wall-clock-ceiling status:** `{{WALLCLOCK_USED}} / {{WALLCLOCK_CEILING}} h`

## What I'm doing right now (one paragraph)

{{NARRATIVE}}

## Open questions (need answers before I can continue)

- [ ] {{QUESTION_1}}
- [ ] {{QUESTION_2}}

## Blockers

| Blocker | Why it blocks | Owner | Mitigation |
|---|---|---|---|
| | | | |

## Next 3 things I'll do

1. {{NEXT_1}}
2. {{NEXT_2}}
3. {{NEXT_3}}

## Heartbeat (auto-mode only)

In auto-mode, this section refreshes every 5 minutes during long phases.

- Last heartbeat: `{{LAST_HEARTBEAT}}`
- Last receipt: `{{LAST_RECEIPT}}`
- Last commit: `{{LAST_COMMIT}}`

## Recent decisions (last 5)

A rolling window. For full history see `.bequite/memory/decisions/` and `.bequite/memory/prompts/v<N>/`.

```
{{RECENT_DECISIONS}}
```
