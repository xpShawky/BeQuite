---
description: BeQuite root menu — shows project state, current mode, current phase, gate status, last command, blockers, and the next 3 recommended commands. Gate-aware — refuses to recommend commands whose required gates aren't met.
---

# /bequite: where the project stands and what to run next

Read-only. It reads state, shows the menu and recommends; it edits nothing, writes no code and decides nothing for the user. Routing knowledge: `bequite-orchestrator`.

## Step 0: up to date

If `.claude/bequite/bin/bq-update.sh` exists, run `bash .claude/bequite/bin/bq-update.sh` and put its one line at the top of the menu (hourly check; it installs a new official release by itself, never blocks, and says "skipped" offline). Plugin installs have no such file and update through `/plugin`.

## Step 1: read the state (silently)

`.bequite/state/PROJECT_STATE.md`, `CURRENT_MODE.md`, `CURRENT_PHASE.md`, `WORKFLOW_GATES.md`, `LAST_RUN.md`, `OPEN_QUESTIONS.md`, `PACKS.md`; `.bequite/ACTIVE.md` and the active work's `gates.md`; and in the folder: a manifest (existing repo), `.git/`, `.bequite/`. A missing file is a signal, not an error.

## Step 2: show the menu

```
BeQuite v<version> by xpShawky
<the update line>

Status
  Project:        <existing repo | new project | unknown>
  BeQuite:        <not initialized | fresh | initialized | mid-workflow>
  Mode / phase:   <mode or "not selected"> / <P0..P5 or "not set">
  Active work:    <id - title (type), or "none">   open work items: <n>
  Last run:       <from LAST_RUN.md, or "none">
  Open questions: <n>      Blockers: <open gates that block, or "none">
  Packs:          <core, studio, business as installed>

Phase gates
  P0 Setup <done | partial | pending>   P1 Framing <...>   P2 Build <...>
  P3 Quality <...>   P4 Release <...>   P5 Memory <...>

Recommended next
  1. /<command>   <why>
  2. /<command>   <why>
  3. /<command>   <why>

Commands (53; IDs in .bequite/commands/COMMAND_ID_MAP.md, details in /bq-help)
  Setup      /bequite /bq-init /bq-discover /bq-doctor /bq-mode /bq-work
  Framing    /bq-clarify /bq-research /bq-scope /bq-spec /bq-plan /bq-multi-plan
  Build      /bq-assign /bq-implement /bq-feature /bq-fix /bq-uiux-variants /bq-live-edit
  Quality    /bq-test /bq-audit /bq-review /bq-red-team
  Release    /bq-verify /bq-changelog /bq-release
  Memory     /bq-memory /bq-recover /bq-handoff
  Navigate   /bq-help /bq-explain /bq-suggest
  Run it all /bq-auto <intent> "<task>"   (modes: fast, deep, token-saver, delegate)
  Core tools /bq-knowledge /bq-writing-dna /bq-team /bq-operator
  Studio     /bq-motion /bq-presentation /bq-content /bq-watch /bq-dna
  Business   /bq-offer /bq-make-money /bq-job-finder /bq-start /bq-productize
  Maintain   /bq-update /bq-skill-audit /bq-hooks /bq-budget /bq-taste /bq-forge /bq-eval

Describe the goal and BeQuite picks the skills. Not sure where to start: /bq-suggest "<what you want>".
```

Show only the packs that are installed; a pack that is missing gets one line saying how to add it.

## Step 3: recommend three commands, gate-aware

Never recommend a command whose required gate is open; recommend the command that closes the gate.

| State | Recommend |
|---|---|
| No `.bequite/`, or state files missing | `/bq-init`, then `/bq-mode`, then `/bq-auto phase=P0` |
| Mode not selected | `/bq-mode`, `/bq-help` |
| P0 open | the next pending of `/bq-discover`, `/bq-doctor`; or `/bq-auto phase=P0` |
| P1 open | the next pending of `/bq-clarify`, `/bq-research`, `/bq-scope`, `/bq-plan`; `/bq-auto phase=P1`; `/bq-multi-plan` when research left a tie |
| P2 open | `/bq-implement` (new project), `/bq-feature` (add feature) or `/bq-fix` (fix); `/bq-test` after each task; `/bq-auto phase=P2` |
| P3 open | `/bq-test` if not green, `/bq-review`, `/bq-auto phase=P3` |
| P4 open | `/bq-verify`, `/bq-changelog`, `/bq-release` |
| P5 open | `/bq-memory snapshot`, `/bq-handoff` when someone else takes over, `/bq-work close` |
| Back after a break | `/bq-recover` first |
| Corrupted or contradictory state | `/bq-recover` |

If `LAST_RUN.md` shows a command that was refused for an open gate, say so above the recommendations: which command, which gate, and what closes it.

## `/bequite short`: one line

Same reads, same logic, exactly one line and nothing else:

```
P2 build · work 0007 launch-film (motion) · last: /bq-motion M5 done · next: /bq-motion M6
blocked: PLAN_APPROVED pending (work 0007) · run /bq-plan
BeQuite not initialized · run /bq-init
```

## Quality gate

The status, the phase gates and three recommendations are shown; every recommendation is allowed by the gates; nothing was written.
