---
description: Resume after a session break. Reads all .bequite/ memory, finds the last green checkpoint, summarizes "what was happening, what's the next safe step", updates state.
---

# /bq-recover — resume after a break

You are restarting work. A new Claude Code session, or after a long pause. Your job: get the user back to productive in 30 seconds.

## Step 1 — Detect available memory

Check existence of:

- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md`
- `.bequite/state/SNAPSHOT-*.md` (any snapshots? show the most recent date)
- `.bequite/tasks/TASK_LIST.md`
- `.bequite/plans/IMPLEMENTATION_PLAN.md`
- `.bequite/logs/AGENT_LOG.md`
- `.bequite/logs/ERROR_LOG.md`

If `.bequite/` doesn't exist at all → tell the user to `/bq-init` first. Exit.

## Step 2 — Restore + read

Read in this order:

1. `LAST_RUN.md` → what was the most recent command?
2. `CURRENT_PHASE.md` → what workflow phase are we in?
3. `TASK_LIST.md` (if present) → what's `[~] in-progress`, what's `[!] blocked`, what's `[ ] next-pending`?
4. `OPEN_QUESTIONS.md` → any unresolved blockers?
5. Last 5 entries of `AGENT_LOG.md` → recent history
6. `ERROR_LOG.md` last 3 entries → recent fixes (in case a regression matters)
7. `IMPLEMENTATION_PLAN.md` (if present) → goal we're working toward

## Step 3 — Detect what's safe to do next

Walk this decision tree:

```
Is there a [~] in-progress task?
├── YES → that's the next thing. Likely the previous session was interrupted mid-implementation.
│         /bq-implement T-<id> (resume)
│
└── NO → check [!] blocked tasks
         ├── Any blocked? → /bq-fix the blocker first, OR /bq-clarify if it's a question
         │
         └── None blocked → look at [ ] pending tasks
                  ├── Any pending? → first pending is the next task. /bq-implement.
                  │
                  └── All [x] done → check verify state
                           ├── Verify passed → /bq-release
                           ├── Verify never run → /bq-verify
                           └── Verify failed → /bq-fix the failing gate

(Also: any unresolved OPEN_QUESTIONS that block forward progress? Surface them.)
```

## Step 4 — Print the recovery summary

```
┌─────────────────────────────────────────────────────────────┐
│  /bq-recover — resuming where you left off                  │
└─────────────────────────────────────────────────────────────┘

Last command:    <e.g. /bq-implement T-2.3 (sign-up form)>
When:            <e.g. 2 days ago>
Phase:           <e.g. Phase 2 — Build>
Result:          <e.g. partial — got UI working, hit a snag on email confirmation>

Task list status:
  [x] done:        12
  [~] in-progress: 1  (T-2.3 sign-up form — partial)
  [!] blocked:     0
  [ ] pending:     7

Recent activity (last 3 entries):
  • <date> /bq-implement T-2.3 → partial; hit blocker on Resend API key
  • <date> /bq-fix bug-router-redirect → fixed in app/(auth)/signin/page.tsx
  • <date> /bq-test → 47/47 passed

Open questions: 1
  Q: "Use Resend or SES for transactional email?" → unresolved

Goal (from plan):
  <one-line summary of vision from IMPLEMENTATION_PLAN.md>

Recommended next step:

  Most likely: /bq-clarify — answer the Resend vs SES question first.
  Alternative: /bq-implement T-2.3 retry (if you've already decided)

Other options:
  /bq-memory show tasks   to see the full task list
  /bq-memory show state.decisions   to see what's locked
  /bequite   to see the full command menu
```

## Step 5 — Update state + log

- `.bequite/state/LAST_RUN.md` → `/bq-recover resumed`
- `.bequite/logs/AGENT_LOG.md` appended:

```markdown
## <ISO 8601 UTC>
**Command:** /bq-recover
**Resumed from:** <previous LAST_RUN.md value>
**Recommendation:** <whatever we suggested>
```

## Rules

- **Don't auto-run the next command.** Just recommend it; user types it.
- **Show recent context concisely.** If the user wants more detail, they'll ask via `/bq-memory show`.
- **Be honest if the trail is cold.** "No memory found — run `/bq-init` first" is fine.

## Standardized command fields (alpha.6)

**Phase:** P5 — Memory and Handoff (or anytime resuming)
**When NOT to use:** fresh session in a fresh repo where you remember context (run `/bq-now` for one-line orientation instead).
**Preconditions:** `BEQUITE_INITIALIZED`
**Required previous gates:** `BEQUITE_INITIALIZED`
**Quality gate:**
- All `.bequite/` files read
- Last green checkpoint identified
- Recovery summary printed: what was happening / next safe step
- `LAST_RUN.md` updated with recovery context
**Failure behavior:**
- State files corrupted / inconsistent → write `RECOVERY_REPORT.md`; print what's recoverable + what's lost; suggest manual review
- Last green checkpoint > 30 days old → flag as stale; suggest user verify the project hasn't drifted
**Memory updates:** Updates `LAST_RUN.md` with recovery summary. Does NOT mutate other state.
**Log updates:** `AGENT_LOG.md` entry "recovery completed".

## Memory files this command reads

- All `.bequite/state/*.md`
- All `.bequite/logs/*.md` (recent entries)
- `.bequite/tasks/TASK_LIST.md`
- `.bequite/plans/IMPLEMENTATION_PLAN.md`

## Memory files this command writes

- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

Depends on the recovery tree — usually `/bq-implement <task>` or `/bq-clarify` or `/bq-fix <issue>`.

---

## Gate check + memory preflight (alpha.15)

Before doing any work:

1. **Gate check.** Read `.bequite/state/WORKFLOW_GATES.md`. If this command's required gates aren't `✅`, refuse:
   > "You're trying to run this command, but `<required-gate>` is pending. Run `<prerequisite-command>` first."

   Don't proceed when a required gate is missing. Recommend the prerequisite + how to resume.

2. **Memory preflight.** Read these files first (per `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`):

   - `.bequite/state/PROJECT_STATE.md`
   - `.bequite/state/CURRENT_MODE.md`
   - `.bequite/state/CURRENT_PHASE.md`
   - `.bequite/state/LAST_RUN.md`
   - `.bequite/state/MISTAKE_MEMORY.md` — top 10–20 entries (skip mistakes already learned)
   - Other state files only when relevant to this command's scope (`DECISIONS.md` for architectural questions, `OPEN_QUESTIONS.md` for phase transitions, `MODE_HISTORY.md` when invoked via `/bq-auto`-style flows)

   **Use focused reads.** Don't load all of `.bequite/` every command.

## Memory writeback (alpha.15)

After successful completion:

- `.bequite/state/LAST_RUN.md` — this command + outcome
- `.bequite/state/WORKFLOW_GATES.md` — set this command's gate to `✅` if applicable
- `.bequite/state/CURRENT_PHASE.md` — advance if phase transitioned
- `.bequite/logs/AGENT_LOG.md` — append entry
- `.bequite/logs/CHANGELOG.md` `[Unreleased]` — only when material files changed (skip for read-only commands)
- `.bequite/state/MISTAKE_MEMORY.md` — append when a project-specific lesson surfaced
- `.bequite/state/MODE_HISTORY.md` — append mode + outcome (when invoked via `/bq-auto`-style mode)

**Failure behavior:** don't claim `✅ done` if any of the above wasn't completed. Report PARTIAL with the specific gap.
