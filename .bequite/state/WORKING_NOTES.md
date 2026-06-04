# Working Notes

Generic per-task scratchpad. **Every** workflow (frontend / backend / db / security / devops / testing) appends here in the **same shape** so progress survives context resets — this is BeQuite's structured note-taking / external memory (Anthropic *effective-harnesses*).

**This is what the agent re-reads after `/compact` or in a new session to continue without re-deriving.** Read the top entry first; it is the current state of work.

- **Append-only. Newest entry at the TOP.** Never delete history below; prune by compacting (see Rules).
- **Machine state lives elsewhere.** Gates / phase / mode / pass-fail status live in the JSON/markdown ledgers (`WORKFLOW_GATES.md`, `CURRENT_PHASE.md`, `CURRENT_MODE.md`, `PROJECT_STATE.md`). **This file is human narrative** — the "why / what I tried / what's next" that ledgers cannot hold.

---

## Rules

| Rule | Why |
|---|---|
| **One task in focus at a time.** | Parallel half-finished tasks lose the thread across a reset. |
| **The PENDING list is the source of truth — not chat memory.** | After `/compact`, chat memory is gone; PENDING is what survives. |
| **Keep the TOP entry current.** Update it as the task moves; don't wait until done. | A stale top entry mis-routes the next session. |
| **Prune / compact when the file grows.** | Collapse resolved tasks into a one-line summary; archive the detail. Long context buries the middle (*effective-context-engineering*). |
| **Every claim of progress carries a proof command + its last result.** | No weasel words; verification over assertion (*reduce-hallucinations*). |
| **Cite file:line for what you learned.** | The next session must locate the evidence without re-searching. |

---

## Entry template

Copy this block to the TOP for each new working session on a task.

```
### <UTC timestamp> — <task in one line>
- **domain:** fe | be | db | sec | devops | test
- **what I tried:** <action(s) taken this session>
- **what I learned:** <finding> (evidence: <path>:<line>)
- **PENDING (next action):** <the single concrete next step>
- **RE-READ before continuing:** <files / sections / ledgers to load first>
- **confidence:** high | med | low — **biggest unknown:** <the one thing still unverified>
- **proof:** `<exact command>` → last result: <output / pass / fail / not-run>
```

---

## Entries

### 2026-06-03T14:20Z — Wire WORKING_NOTES re-read into /bq-recover
- **domain:** devops
- **what I tried:** Added a "read WORKING_NOTES.md top entry" step to the recover sequence; checked the ledger reads were already present.
- **what I learned:** `/bq-recover` reads state ledgers but not this narrative file (evidence: `.claude/commands/bq-recover.md`:31). Re-read step belongs after the green-checkpoint scan so PENDING overrides a stale checkpoint.
- **PENDING (next action):** Insert the re-read step at `bq-recover.md`:33, then update `docs/architecture/MEMORY_FIRST_BEHAVIOR.md` to list this file in core memory.
- **RE-READ before continuing:** `.claude/commands/bq-recover.md` (steps 30-40), `docs/architecture/MEMORY_FIRST_BEHAVIOR.md` § core-memory list.
- **confidence:** med — **biggest unknown:** whether `/bq-recover` should write back a checkpoint entry here or stay read-only.
- **proof:** `grep -n "WORKING_NOTES" .claude/commands/bq-recover.md` → last result: 0 matches (not yet wired).
