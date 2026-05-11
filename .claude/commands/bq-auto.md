---
description: Autonomous workflow runner. Walks all phases (P0 → P5) end-to-end, executing each command in order. Stops at hard human gates (mode selection, scope approval, plan approval, implementation approval, release approval, destructive ops, DB migrations, server/VPS changes). Honest pause + clear resume prompt at each gate.
---

# /bq-auto — Autonomous full-cycle runner

## Purpose

Run the BeQuite workflow end-to-end with **minimum interruption**, **maximum discipline**. The agent walks P0 → P5 in order, runs each phase's commands, and pauses **only** at hard human gates where the wrong answer is irreversible or expensive.

Not "fire and forget" — it is "drive the steering wheel and let me handle the pedals for the cliff edges."

## When to use it

- You have a clear-enough goal and want BeQuite to drive
- You're tired of running 18 commands in sequence by hand
- You accept that the agent will stop and ask you ~6-10 times across a full cycle
- You're NOT in a regulated context where every step needs a human sign-off (use the manual phase commands instead)

## Preconditions

- `BEQUITE_INITIALIZED` (run `/bq-init` first if not)

## Required previous gates

- `BEQUITE_INITIALIZED`

## Files to read

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/WORKFLOW_GATES.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md`

## Files to write

- Every artifact each underlying command writes
- `.bequite/state/WORKFLOW_GATES.md` (gates ticked as they pass)
- `.bequite/state/CURRENT_PHASE.md` (advances as each phase completes)
- `.bequite/state/LAST_RUN.md` (after every command)
- `.bequite/logs/AGENT_LOG.md` (one entry per command + one entry per gate pause)

## Hard human gates (the only places /bq-auto pauses)

Auto-mode **MUST** stop and wait for explicit user confirmation at each of these. No exceptions.

| # | Gate | Why it pauses |
|---|---|---|
| 1 | **Mode selection** | The choice of mode (New / Existing / Feature / Fix / Research / Release) shapes everything downstream. Wrong mode = wasted hours. |
| 2 | **Clarify answers** | The agent asked 3-5 questions; the user must answer (or accept defaults explicitly). |
| 3 | **Scope approval** | IN / OUT / NON-GOALS lock the project. Locking the wrong scope ships the wrong thing. |
| 4 | **Multi-model planning decision** | "Do you want a second-opinion plan?" Yes = paste flow. No = proceed. Either way, user picks. |
| 5 | **Implementation plan approval** | The plan is the contract. Approve before code. |
| 6 | **Release approval** | Tagging + publishing is one-way; user runs `git push` and `git tag` themselves. |
| 7 | **Destructive operations** | `rm -rf`, `git push --force`, `terraform destroy`, `DROP TABLE` — agent refuses without explicit user confirmation. |
| 8 | **Database migrations against shared DBs** | Even reversible migrations need a human OK in /bq-auto. |
| 9 | **Server / VPS configuration changes** | Touching production or a shared dev server pauses for user. |
| 10 | **Cost ceiling reached** | Default $20/session. If session token cost roll-up exceeds ceiling → pause. |
| 11 | **Banned-weasel-word trip** | If a completion message would contain `should / probably / seems to / appears to / I think it works / might / hopefully / in theory`, the agent rewrites with a concrete claim — and if it cannot, pauses. |
| 12 | **3 consecutive task failures on the same task** | Don't burn through the wallet on a stuck loop. Pause for human guidance. |

## Steps

### 1. Read state + decide mode

If `.bequite/state/CURRENT_MODE.md` says `Not selected`:
- Pause at **Gate #1: Mode selection**
- Print the 6 options + recommendation based on `PROJECT_STATE.md`
- Wait for user's choice
- Write the mode + resume

### 2. Run P0 — Setup and Discovery

Per mode:

| Mode | P0 commands |
|---|---|
| New Project | `/bq-init new` → `/bq-doctor` |
| Existing Audit | `/bq-init` → `/bq-discover` → `/bq-doctor` |
| Add Feature | `/bq-init` (if not) → `/bq-discover` (if stale) |
| Fix Problem | `/bq-init` (if not) → `/bq-doctor` |
| Research Only | `/bq-init` (if not) |
| Release Readiness | `/bq-init` (if not) → `/bq-doctor` |

After each command, mark the corresponding gate in `WORKFLOW_GATES.md`.

### 3. Run P1 — Product Framing and Research

| Mode | P1 commands |
|---|---|
| New Project | `/bq-clarify` → **Gate #2** → `/bq-research` → `/bq-scope` → **Gate #3** → `/bq-plan` → **Gate #5** → (optional `/bq-multi-plan` at **Gate #4**) |
| Existing Audit | `/bq-clarify` → **Gate #2** → `/bq-research` (focused on gaps) |
| Add Feature | (skip — feature workflow is self-contained) |
| Fix Problem | (skip — fix workflow is reproduction-driven) |
| Research Only | `/bq-clarify` → **Gate #2** → `/bq-research` → STOP (mode complete) |
| Release Readiness | (skip) |

### 4. Run P2 — Planning and Build

| Mode | P2 commands |
|---|---|
| New Project | `/bq-assign` → `/bq-implement` (loop until TASK_LIST empty) |
| Existing Audit | (no build phase; audit is read-only) |
| Add Feature | `/bq-feature "<title>"` (mini-cycle) |
| Fix Problem | `/bq-fix` (reproduce → root cause → patch → test) |
| Research Only | (skip) |
| Release Readiness | (skip — no new code) |

Per task, if 3 consecutive failures → **Gate #12** pause.

### 5. Run P3 — Quality and Review

All modes that produced code:

`/bq-test` → `/bq-audit` (if requested or release path) → `/bq-review` → (optional `/bq-red-team`)

### 6. Run P4 — Release

| Mode | P4 commands |
|---|---|
| New Project | `/bq-verify` → if PASS, `/bq-changelog` → **Gate #6** → print `/bq-release` instructions |
| Existing Audit | (no release; audit writes report only) |
| Add Feature | `/bq-verify` (subset) → `/bq-changelog` entry |
| Fix Problem | `/bq-verify` (subset) → `/bq-changelog` entry under Fixed |
| Research Only | (skip) |
| Release Readiness | `/bq-verify` (full) → `/bq-changelog` → **Gate #6** |

### 7. Run P5 — Memory and Handoff

All modes:

`/bq-memory snapshot` → (optional `/bq-handoff` if user wants a HANDOFF.md)

### 8. Final report

Print a single summary:

```
✓ /bq-auto cycle complete

Mode:           <mode>
Phases run:     P0 P1 P2 P3 P4 P5
Commands run:   <N>
Gates passed:   <count> / <total>
Gates paused at:<list>
Files written:  <count>
Tests:          <pass> / <total>
Cost (tokens):  <approx>
Cost (USD):     <approx>

Next: review the changes (git diff) and confirm /bq-release if applicable.
```

## Output format

The agent narrates each phase transition + each gate pause **clearly** so the user can intervene. Example:

```
[P0 → P1] Setup complete. Moving to product framing.
[P1 Gate #2] I have 4 questions for you. Answer below, or say "all defaults".
...
[P1 → P2] Plan approved. Starting build.
[P2 task T-1.3] Failed twice. Trying once more with a different approach.
[P2 task T-1.3] Failed 3x. Pausing — Gate #12.
```

## Quality gate

- Every phase's required gates marked `✅ done` in `WORKFLOW_GATES.md`
- Every command's `LAST_RUN.md` + `AGENT_LOG.md` entry written
- No banned weasel words in any completion report
- No destructive op executed without explicit user OK
- Cost ceiling respected (or user re-authorized continuation)

## Failure behavior

- Hard gate → pause, print clear resume hint, do NOT continue
- Soft failure (test red, lint red) → run the relevant fix command (`/bq-fix`) and retry once, then pause
- Cost ceiling → pause, print spend, ask user to raise the ceiling or stop
- Banned-word trip → rewrite with concrete claim, or pause asking the user to clarify the actual state

## Usual next command

- After auto-mode completes: `/bq-handoff` (if shipping to another engineer) or done
- After auto-mode pauses at a gate: resolve the gate, then run `/bq-auto` again (it resumes from `LAST_RUN.md`)
