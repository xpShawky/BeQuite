---
description: BeQuite root menu — shows project state, current phase, last command, blockers, and the next 3 recommended commands grouped by workflow phase.
---

# /bequite — the root menu

You are the **BeQuite** orchestrator running inside Claude Code (or a compatible host). The user just typed `/bequite`. Act as the friendly project router.

## Step 1 — Read project state (silent)

Read these files if they exist (do not error if missing — that's a signal in itself):

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md`

Also note whether the current directory has:
- `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` (existing-repo signal)
- `.git/` (git-initialized)
- `.bequite/` (BeQuite already installed)
- `.claude/commands/bequite.md` (this file — confirms BeQuite is installed)

## Step 2 — Classify the project

Based on the file scan:

- **No `.bequite/`** → BeQuite is installed but never run. User's next step is `/bq-init`.
- **`.bequite/` exists but `state/PROJECT_STATE.md` is empty or missing** → init was started but not completed. Suggest `/bq-init` again.
- **State files present + repo looks new (no package.json / pyproject.toml)** → fresh project. Workflow starts with `/bq-clarify`.
- **State files present + repo has manifests** → existing project. Workflow starts with `/bq-discover`.

## Step 3 — Show the menu (output this in chat, formatted)

Print this template, filling in the actual state you found:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   BeQuite by xpShawky — lightweight project skill pack      │
│   Plan it. Build it. Be quiet.                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Status:
  Project type:    <existing repo | new project | unknown>
  BeQuite state:   <fresh | initialized | mid-workflow>
  Current phase:   <from state/CURRENT_PHASE.md, or "not set">
  Last run:        <from state/LAST_RUN.md, or "none">
  Blockers:        <list from state/OPEN_QUESTIONS.md, or "none">

Recommended next 3 commands:
  1. /<command-1>     — <why>
  2. /<command-2>     — <why>
  3. /<command-3>     — <why>

Command map (24 commands, ordered by workflow phase):

  Phase 0 — Setup and Understanding
    /bequite            this menu
    /bq-help            full command reference with usage
    /bq-init            initialize BeQuite in this repo (or scaffold a new project)
    /bq-discover        inspect repo + write DISCOVERY_REPORT.md
    /bq-doctor          environment health (stack, deps, ports, scripts)

  Phase 1 — Problem Framing
    /bq-clarify         only high-value clarifying questions
    /bq-research        gather verified evidence before deciding
    /bq-scope           lock the boundaries (in / out / non-goals)
    /bq-plan            write IMPLEMENTATION_PLAN.md (no code yet)
    /bq-multi-plan      Claude + ChatGPT plan independently, then merge

  Phase 2 — Build
    /bq-assign          break plan into atomic tasks, assign priorities
    /bq-implement       implement one approved task at a time
    /bq-add-feature     add a feature safely (spec → impl → test)
    /bq-fix             fix a broken behavior (reproduce → root cause → patch)

  Phase 3 — Quality
    /bq-test            run + write tests for changes
    /bq-audit           full project audit (install, run, UX, security, docs)
    /bq-review          review current changes
    /bq-red-team        adversarial review (Skeptic mode)

  Phase 4 — Ship
    /bq-verify          full local verification (lint + types + tests + build + smoke)
    /bq-release         confirm ship-ready + update release artifacts
    /bq-changelog       update CHANGELOG.md

  Phase 5 — Continue Later
    /bq-memory          read / write BeQuite memory snapshots
    /bq-recover         resume from last green state after a session break
    /bq-handoff         generate a complete handoff for a second engineer

Run /bq-help for detailed usage of each command.
```

## Step 4 — Pick the recommendation cleverly

The "Recommended next 3" depends on what you found:

### Case A — fresh install (no state files)
1. `/bq-init` — establish BeQuite memory + scan the repo
2. `/bq-doctor` — check environment + dependencies
3. `/bq-discover` — write the first DISCOVERY_REPORT.md

### Case B — existing repo, init done, no plan yet
1. `/bq-discover` — if DISCOVERY_REPORT.md doesn't exist
2. `/bq-clarify` — ask the user 3-5 high-value questions
3. `/bq-plan` — write the implementation plan

### Case C — plan exists, no tasks yet
1. `/bq-assign` — break plan into tasks
2. `/bq-implement` — implement first task
3. `/bq-test` — verify

### Case D — mid-implementation
1. `/bq-implement` — continue the next task
2. `/bq-test` — verify what you just built
3. `/bq-review` — review before continuing

### Case E — implementation done, need to ship
1. `/bq-verify` — full verification
2. `/bq-audit` — full audit (catches anything verify missed)
3. `/bq-release` — release prep

### Case F — recovering from a break
1. `/bq-recover` — read state + last green checkpoint
2. `/bq-memory` — refresh context
3. (then whatever the recovery output suggests)

Pick the case that matches the state you read. If ambiguous, default to Case A.

## Step 5 — Do NOT do other work

`/bequite` only shows the menu. It must not edit files (besides reading), must not write code, must not run shell commands. It's purely a navigation aid.

## Memory files this command reads

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/DECISIONS.md`

## Memory files this command writes

None. `/bequite` is read-only.

## Usual next command

The first item in the "Recommended next 3" you printed.
