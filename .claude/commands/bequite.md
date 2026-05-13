---
description: BeQuite root menu — shows project state, current mode, current phase, gate status, last command, blockers, and the next 3 recommended commands. Gate-aware — refuses to recommend commands whose required gates aren't met.
---

# /bequite — the gate-aware root menu

You are the **BeQuite** orchestrator. The user typed `/bequite`. Act as the friendly project router. Read state files, classify the project, recommend the next 3 commands, and refuse to recommend any command whose required gates aren't met.

## Step 1 — Read project state (silent)

Read these files if they exist (do not error if missing — that's a signal):

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/WORKFLOW_GATES.md` (the gate ledger)
- `.bequite/state/LAST_RUN.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md`

Also note in the working directory:
- `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` (existing-repo signal)
- `.git/` (git-initialized)
- `.bequite/` (BeQuite installed)

## Step 2 — Classify state

| State | Description |
|---|---|
| **Not installed** | No `.bequite/` directory |
| **Fresh** | `.bequite/` exists but state files missing |
| **Mode not selected** | State files exist; `CURRENT_MODE.md` says "Not selected" |
| **Mid-P0** | Mode selected; P0 gates not all `✅` |
| **Mid-P1** | P0 complete; P1 gates incomplete |
| **Mid-P2** | P1 complete; P2 gates incomplete |
| **Mid-P3** | P2 complete; P3 gates incomplete |
| **Mid-P4** | P3 complete; P4 gates incomplete |
| **Mid-P5** | P4 complete; P5 gates incomplete |
| **Cycle complete** | All gates `✅`; ready for next cycle |

## Step 3 — Show the menu

Print:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   BeQuite by xpShawky — lightweight project skill pack      │
│   Plan it. Build it. Be quiet.                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Status:
  Project type:    <existing repo | new project | unknown>
  BeQuite state:   <not installed | fresh | initialized | mid-workflow>
  Current mode:    <New Project | Existing Audit | Add Feature | Fix Problem | Research Only | Release Readiness | not selected>
  Current phase:   <P0 | P1 | P2 | P3 | P4 | P5 | not set>
  Last run:        <from LAST_RUN.md, or "none">
  Open questions:  <count, or "none">
  Blockers:        <list any [!] from gate ledger, or "none">

Phase gates:
  P0 Setup       <✅ done | ❌ pending | ⚪ partial>
  P1 Framing     <✅ done | ❌ pending | ⚪ partial>
  P2 Build       <✅ done | ❌ pending | ⚪ partial>
  P3 Quality     <✅ done | ❌ pending | ⚪ partial>
  P4 Release     <✅ done | ❌ pending | ⚪ partial>
  P5 Memory      <✅ done | ❌ pending | ⚪ partial>

Recommended next 3 commands:
  1. /<command-1>     — <why>
  2. /<command-2>     — <why>
  3. /<command-3>     — <why>

Command map (34 commands, ordered by workflow phase):

  Phase 0 — Setup and Discovery
    /bequite            this menu
    /bq-help            full command reference
    /bq-init            initialize BeQuite in this repo
    /bq-mode            select / show the workflow mode
    /bq-new             begin a New Project workflow
    /bq-existing        begin an Existing Project Audit workflow
    /bq-discover        inspect repo → DISCOVERY_REPORT.md
    /bq-doctor          environment health → DOCTOR_REPORT.md

  Phase 1 — Product Framing and Research
    /bq-clarify         3-5 high-value clarifying questions
    /bq-research        11-dimension verified evidence
    /bq-scope           lock IN / OUT / NON-GOALS
    /bq-plan            write IMPLEMENTATION_PLAN.md (no code yet)
    /bq-multi-plan      unbiased multi-model planning (manual paste)

  Phase 2 — Planning and Build
    /bq-assign          break plan into atomic tasks
    /bq-implement       implement one approved task at a time
    /bq-feature         add feature workflow with 12-type router
    /bq-fix             fix workflow with 15-type router

  Phase 3 — Quality and Review
    /bq-test            run + write tests
    /bq-audit           full project audit
    /bq-review          review current changes
    /bq-red-team        adversarial review (Skeptic mode)

  Phase 4 — Release
    /bq-verify          full local verification
    /bq-release         release prep (prints commands; user pushes)
    /bq-changelog       categorize commits into CHANGELOG

  Phase 5 — Memory and Handoff
    /bq-memory          read / write BeQuite memory snapshots
    /bq-recover         resume after a session break
    /bq-handoff         generate HANDOFF.md

  Phase orchestrators
    /bq-p0              walk Phase 0 in order
    /bq-p1              walk Phase 1 in order
    /bq-p2              walk Phase 2 in order
    /bq-p3              walk Phase 3 in order
    /bq-p4              walk Phase 4 in order
    /bq-p5              walk Phase 5 in order
    /bq-auto            walk ALL phases autonomously (stops at hard gates)

Run /bq-help for detailed usage of each command.
```

## Step 4 — Gate-aware recommendation

Pick the 3 commands based on what gates are met. **Never recommend a command whose required gates are not yet `✅`.**

### Case A — Not installed (no `.bequite/`)
1. `/bq-init` — establish BeQuite memory
2. `/bq-mode` — pick a mode
3. `/bq-p0` — run Phase 0 in one pass

### Case B — Fresh install (`.bequite/` exists, but state empty)
Same as Case A.

### Case C — Mode not selected
1. `/bq-mode` — pick one of 6 modes
2. `/bq-help` — see full command reference
3. (Skip 3rd; user must pick mode first.)

### Case D — Mid-P0 (mode selected, discovery / doctor pending)
1. Whichever P0 command is `❌ pending` next
2. `/bq-p0` — run remaining P0 in one pass
3. `/bq-help`

### Case E — Mid-P1 (P0 complete)
1. Whichever P1 command is `❌ pending` next (`/bq-clarify`, then `/bq-research`, then `/bq-scope`, then `/bq-plan`)
2. `/bq-p1` — run remaining P1 in one pass
3. `/bq-multi-plan` if research left a tie

### Case F — Mid-P2 (P1 complete, build in progress)
1. `/bq-implement` (for New Project) | `/bq-feature` (for Add Feature) | `/bq-fix` (for Fix Problem)
2. `/bq-test` after each task
3. `/bq-p2` to keep looping until task list done

### Case G — Mid-P3 (build done, testing in progress)
1. `/bq-test` if not green
2. `/bq-review`
3. `/bq-p3`

### Case H — Mid-P4 (review done, ready to ship)
1. `/bq-verify` — full gate matrix
2. `/bq-changelog` — sharpen the entry
3. `/bq-release` — print push commands

### Case I — Mid-P5 (released, persisting)
1. `/bq-memory snapshot`
2. `/bq-handoff` if shipping to another engineer
3. (Cycle complete; user can start a new mode for next feature)

### Case J — Recovering from a break
1. `/bq-recover` — read state + last green checkpoint
2. (Whatever `/bq-recover` output suggests)
3. `/bq-help`

## Step 5 — Block out-of-order commands

If user previously tried (per LAST_RUN.md) a command whose required gates weren't met:
- Surface a "Blocked attempt" note in the Status section
- Show what gates are missing

Example:
```
⚠ Blocked attempt detected:
   /bq-implement was attempted but PLAN_APPROVED is ❌ pending.
   Run /bq-plan first.
```

## Step 6 — Do NOT do other work

`/bequite` only shows the menu. It does not:
- Edit any files (besides reading)
- Write code
- Run shell commands
- Make decisions (the user picks from recommendations)

## Standardized command fields (alpha.6)

**Phase:** Any (read-only meta command)
**When NOT to use:** you want a one-line answer (use `/bq-now` — faster); you're already mid-flow inside `/bq-auto` (it's already gate-aware).
**Preconditions:** none (read-only)
**Required previous gates:** none
**Quality gate:**
- Output includes Status block, Phase gates block, Recommended next 3 commands
- Recommendations are gate-aware (never recommend a command whose required gates aren't met)
- Blocked-attempt note shown if user previously hit an out-of-order command
**Failure behavior:**
- BeQuite not installed → recommend `/bq-init` as the only option
- State files corrupted → suggest `/bq-recover`
**Memory updates:** none (read-only)
**Log updates:** none (read-only navigation aid; does not pollute `AGENT_LOG.md`)

## Memory files this command reads

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/WORKFLOW_GATES.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md`

## Memory files this command writes

None. `/bequite` is read-only.

## Usual next command

The first item in the "Recommended next 3" you printed.
