---
description: Begin a New Project workflow. Sets the mode + skeleton state + recommends the first batch of commands. Use only when starting a project from scratch in an empty folder.
---

# /bq-new — New Project workflow entry

## Purpose

Establish "we are building from scratch in this folder" as the working assumption. Sets state files for an empty-repo workflow + recommends the right next commands.

## When to use it

- Empty (or near-empty) folder where you intend to scaffold a new project
- After `/bq-mode` selected "New Project"
- NOT for adding features to an existing repo (use `/bq-feature` instead)

## Preconditions

- `BEQUITE_INITIALIZED`
- `MODE_SELECTED = New Project` (run `/bq-mode` first if not)

## Required previous gates

- `BEQUITE_INITIALIZED`
- `MODE_SELECTED` = "New Project"

## Files to read

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/CURRENT_MODE.md` (must be "New Project")
- The current directory's top-level (Glob; just to confirm it's empty-ish)

## Files to write

- `.bequite/state/PROJECT_STATE.md` (updated: "type = new project; stack = not yet decided")
- `.bequite/state/CURRENT_PHASE.md` (`P0` set; ready to move to `P1` after discovery)
- `.bequite/state/OPEN_QUESTIONS.md` (queues "What is this project?" + "Who is the user?" + "What's the scale?")
- `.bequite/logs/AGENT_LOG.md`

## Steps

1. Read `.bequite/state/CURRENT_MODE.md`. If not "New Project", refuse + suggest `/bq-mode`.
2. Glob the current directory. If it has substantial source files (package.json, src/, etc.), warn:
   > "This folder doesn't look empty. New Project mode is for fresh scaffolds. Did you mean `/bq-existing`?"
3. Otherwise proceed. Update `PROJECT_STATE.md`:
   - `Project type: new project`
   - `Stack: not yet decided — pending /bq-research + /bq-plan`
   - `Initialized: <date>`
4. Pre-queue three foundational questions in `OPEN_QUESTIONS.md` (with recommended defaults):
   - "What is this project — one sentence?"
   - "Who is the primary user? (engineer / vibecoder / both / enterprise / consumer)"
   - "What's the target scale? (solo / small_saas (~5k MAU) / large_saas (>5k MAU) / regulated)"
5. Print next steps.

## Output format

```
✓ New Project workflow set

Current state:
  Mode:    New Project
  Folder:  <path>
  Stack:   not yet decided
  Phase:   P0 — Setup and Discovery

Pre-queued questions (you'll answer them in /bq-clarify):
  Q1. What is this project — one sentence?
  Q2. Who is the primary user?
  Q3. What's the target scale?

Recommended sequence:
  /bq-discover    (probably says "empty folder" — expected)
  /bq-doctor      (environment health: Node? Python? Git?)
  /bq-clarify     (answer Q1-Q3 above + any new questions)
  /bq-research    (verified evidence — stack picks, product fit, competitors)
  /bq-scope       (lock IN / OUT / NON-GOALS)
  /bq-plan        (the implementation plan)
  /bq-multi-plan  (optional second opinion)
  /bq-assign      (break plan into atomic tasks)
  /bq-implement   (workhorse)

Or run /bq-p0 to walk Phase 0 automatically.
```

## Quality gate

- `CURRENT_MODE.md` = "New Project"
- `PROJECT_STATE.md` updated with new-project context
- 3 questions queued

## Failure behavior

- Folder isn't empty → warn + suggest `/bq-existing`
- Mode is wrong → refuse + suggest `/bq-mode`

## Usual next command

`/bq-discover` (or `/bq-p0` to orchestrate Phase 0)
