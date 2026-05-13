# Memory-First Behavior

**Status:** active
**Adopted:** 2026-05-12 (alpha.10)
**Reference:** ADR-002 (workflow gates), TOOL_NEUTRALITY.md, AUTO_MODE_STRATEGY.md

---

## The principle

Every BeQuite command begins by **checking project memory** — unless it's a small static help command. Commands read the relevant memory first, then act. They don't re-derive context the user already paid to write down.

This is what makes BeQuite stateful across sessions: state lives in `.bequite/`. Commands honor it.

---

## Core memory (read on every action-taking command)

These are always read at the start of any non-trivial command:

- `.bequite/state/PROJECT_STATE.md` — project type, stack, summary
- `.bequite/state/CURRENT_MODE.md` — active mode (one of 6)
- `.bequite/state/CURRENT_PHASE.md` — active phase (P0..P5)
- `.bequite/state/WORKFLOW_GATES.md` — gate ledger
- `.bequite/state/LAST_RUN.md` — last command + result
- `.bequite/state/DECISIONS.md` — locked decisions
- `.bequite/state/OPEN_QUESTIONS.md` — unresolved
- `.bequite/state/MISTAKE_MEMORY.md` — project-specific lessons

**Total size:** ~5-15 KB combined — cheap to read in token terms.

## Optional memory (read by specific commands)

- `.bequite/state/ASSUMPTIONS.md` — `/bq-plan`, `/bq-research`, `/bq-clarify`
- `.bequite/audits/DISCOVERY_REPORT.md` — `/bq-clarify`, `/bq-research`, `/bq-plan`, `/bq-audit`
- `.bequite/audits/RESEARCH_REPORT.md` — `/bq-plan`, `/bq-multi-plan`, `/bq-scope`
- `.bequite/plans/IMPLEMENTATION_PLAN.md` — `/bq-assign`, `/bq-implement`, `/bq-review`
- `.bequite/plans/SCOPE.md` — `/bq-plan`, `/bq-feature`, `/bq-implement`
- `.bequite/tasks/TASK_LIST.md` — `/bq-implement`, `/bq-test`, `/bq-review`
- `.bequite/tasks/CURRENT_TASK.md` — `/bq-implement`
- `.bequite/uiux/SECTION_MAP.md` — `/bq-live-edit`, `/bq-uiux-variants`, frontend `/bq-fix`
- `.bequite/uiux/LIVE_EDIT_LOG.md` — `/bq-live-edit`
- `.bequite/uiux/UIUX_VARIANTS_REPORT.md` — `/bq-uiux-variants`
- `.bequite/jobs/JOB_PROFILE.md` — `/bq-job-finder` (re-use if recent)
- `.bequite/money/MONEY_PROFILE.md` — `/bq-make-money` (re-use if recent)
- `.bequite/state/BEQUITE_VERSION.md` — `/bq-update`
- `.bequite/state/UPDATE_SOURCE.md` — `/bq-update`
- `.bequite/principles/TOOL_NEUTRALITY.md` — every command that picks tools
- `.bequite/decisions/` — every command that documents tool / architecture choices

---

## Static commands (read minimal memory)

These commands read only what they need; not all core memory:

| Command | Reads |
|---|---|
| `/bq-help` | Nothing — static reference |
| `/bq-now` | Core memory only — one-line output |
| `/bq-explain` | Target file + 1-2 related files |
| `/bequite` | Core memory + gate state |

---

## Per-command read/write matrix (high-level)

| Command | Reads (besides core) | Writes (besides logs) |
|---|---|---|
| `/bq-init` | Project manifests, README | All `.bequite/state/*` baselines |
| `/bq-discover` | Project files broadly | `DISCOVERY_REPORT.md` |
| `/bq-doctor` | Project manifests, env | `DOCTOR_REPORT.md` |
| `/bq-clarify` | DISCOVERY, ASSUMPTIONS | `OPEN_QUESTIONS.md`, `DECISIONS.md` |
| `/bq-research` | OPEN_QUESTIONS, DISCOVERY | `RESEARCH_REPORT.md` |
| `/bq-scope` | OPEN_QUESTIONS, RESEARCH | `SCOPE.md` |
| `/bq-spec` | SCOPE, PROJECT_STATE | `specs/<slug>/spec.md`, `.bequite/plans/spec-<slug>.md` |
| `/bq-plan` | All P0-P1 outputs | `IMPLEMENTATION_PLAN.md` |
| `/bq-multi-plan` | All P0-P1 outputs | prompts + responses + merged plan |
| `/bq-assign` | IMPLEMENTATION_PLAN | `TASK_LIST.md` |
| `/bq-implement` | TASK_LIST, IMPLEMENTATION_PLAN, code | Source files, tests, `CHANGELOG [Unreleased]` |
| `/bq-feature` | (self-contained) | feature mini-spec, source, tests |
| `/bq-fix` | ERROR_LOG, recent git log, source | source fix, regression test, `ERROR_LOG.md`, `MISTAKE_MEMORY.md` |
| `/bq-test` | (test framework) | new test files |
| `/bq-audit` | Repo broadly | `FULL_PROJECT_AUDIT.md`, `MISTAKE_MEMORY.md` |
| `/bq-review` | Git diff, PLAN | `REVIEW-<ts>.md`, `MISTAKE_MEMORY.md` |
| `/bq-red-team` | Diff, PLAN, RESEARCH | `RED_TEAM-<ts>.md`, `MISTAKE_MEMORY.md` |
| `/bq-verify` | All applicable test runners | `VERIFY_REPORT.md`, `MISTAKE_MEMORY.md` |
| `/bq-release` | VERIFY, CHANGELOG | version bump, CHANGELOG move |
| `/bq-changelog` | git log, feature specs | CHANGELOG |
| `/bq-memory` | All `.bequite/state/*` | `MEMORY_SNAPSHOT_<date>.md` |
| `/bq-recover` | All `.bequite/` | `LAST_RUN.md` |
| `/bq-handoff` | All `.bequite/` | `HANDOFF.md` |
| `/bq-uiux-variants` | DISCOVERY, RESEARCH, tokens.css | variant files, `UIUX_VARIANTS_REPORT.md` |
| `/bq-live-edit` | SECTION_MAP, source | source edits, `LIVE_EDIT_LOG.md` |
| `/bq-auto` | Core + per-intent | per-intent (delegates) |
| `/bq-suggest` | Core memory only | `LAST_RUN.md` |
| `/bq-job-finder` | JOB_PROFILE, JOB_SEARCH_LOG, OPPORTUNITIES | All `.bequite/jobs/*` |
| `/bq-make-money` | MONEY_PROFILE, MONEY_SEARCH_LOG, OPPORTUNITIES | All `.bequite/money/*` |
| `/bq-update` | BEQUITE_VERSION, UPDATE_SOURCE | `BEQUITE_VERSION.md`, `UPDATE_LOG.md`, backups |

---

## Token-saving memory strategy

When the user is on a tight session budget (e.g. `--mode token-saver` on `/bq-auto`):

1. **Read only what's needed for this step.** Don't load the full plan if you're only running one task.
2. **Summarize older log entries.** `AGENT_LOG.md` can be 200 entries deep; load the last 5-10 unless the user is debugging.
3. **Cache research.** If `RESEARCH_REPORT.md` was written this session, don't re-fetch the same WebFetch responses.
4. **Use focused skills.** Don't load all 18 skills every time; only load skills the current task activates.
5. **Avoid loading all docs every session.** `commands.md` (~1500 lines) doesn't need to be in context if the agent already knows the surface from skill descriptions.
6. **Re-derive from snapshots.** If `MEMORY_SNAPSHOT_<date>.md` exists, prefer it over reading 10 source files for the same context.

---

## Auto-mode memory strategy

`/bq-auto` runs many sub-commands. Don't reload all memory between sub-commands. Pattern:

1. **At start:** read core memory once
2. **Pass forward:** keep a session-state object (in `AUTO_STATE_<session>.json`) with key derivations from the initial read
3. **Per sub-command:** read only the **new** files relevant to that sub-command + the session state
4. **Update gates after each phase:** rewrite `WORKFLOW_GATES.md` once per phase, not once per task
5. **Update logs after each major action:** entry per command, not per micro-step
6. **Update MISTAKE_MEMORY only when warranted:** patterns, not one-offs

This makes `/bq-auto` viable for long sessions without burning context on memory re-reads.

---

## Mistake memory strategy

`MISTAKE_MEMORY.md` is the project's evolving rulebook. Read it:

- **Always at session start** (the agent honors prior lessons)
- **Before any fix** (`/bq-fix` — to recognize repeat patterns)
- **Before any review** (`/bq-review`, `/bq-red-team` — to flag known traps)
- **Before any audit** (`/bq-audit` — to inform what to look at)
- **After any failure** (the agent itself triggered a banned-weasel-word check or a 3-failure threshold)

Write to it only when:
- Pattern is **repeating** (same root cause as a previous fix)
- Lesson is **forward-applicable** (a new prevention rule)
- Not a trivial one-off

---

## Recovery behavior

`/bq-recover` reads **all** of `.bequite/` — that's intentional. It's the once-per-session "what was happening" command. The token cost is justified because the alternative is "user manually re-orients across 20+ files".

After recovery, normal commands return to focused-reads.

---

## Memory preflight (for command authors)

Standard preflight template (now baked into every action-taking command):

```
1. Read current project state         (PROJECT_STATE.md)
2. Read current mode                  (CURRENT_MODE.md)
3. Read current phase                 (CURRENT_PHASE.md)
4. Read workflow gates                (WORKFLOW_GATES.md)
5. Read last run                      (LAST_RUN.md)
6. Read mistake memory when relevant  (MISTAKE_MEMORY.md)
7. Read optional memory per command   (see matrix above)
8. Continue only with correct context — if gates not met, refuse + suggest prerequisite
```

## Memory writeback (for command authors)

Standard writeback template:

```
1. Update last run                     (LAST_RUN.md)
2. Update workflow gates if changed    (WORKFLOW_GATES.md)
3. Update current phase if changed     (CURRENT_PHASE.md)
4. Append agent log                    (AGENT_LOG.md)
5. Update changelog if user-visible    (CHANGELOG.md)
6. Update mistake memory if relevant   (MISTAKE_MEMORY.md)
7. Update per-command artifacts        (per file matrix above)
```

---

## Anti-patterns

- ❌ Re-reading all memory on every micro-step (waste of tokens)
- ❌ Skipping `MISTAKE_MEMORY.md` (user paid to write project lessons — honor them)
- ❌ Loading all 18 skills when only 1 is needed
- ❌ Loading the full `commands.md` when the agent already knows commands from skill descriptions
- ❌ Writing to memory files outside the documented matrix (creates drift)
- ❌ Forgetting `LAST_RUN.md` update (next `/bq-now` and `/bequite` lie about state)
- ❌ Updating `WORKFLOW_GATES.md` manually outside command success paths (corrupts gate enforcement)

---

## See also

- `ADR-002-mandatory-workflow-gates.md` — gate system
- `AUTO_MODE_STRATEGY.md` — auto-mode read/write patterns
- `RESEARCH_DEPTH_STRATEGY.md` — when to do live research vs. read cached research
- `commands.md` — per-command reads/writes summarized for the user
