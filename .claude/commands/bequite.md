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

Command map (52 active commands + 1 deprecated alias — catalog IDs per .bequite/commands/COMMAND_ID_MAP.md):

  W0 — Setup and Discovery
    W0.1 /bequite       this menu
    W0.2 /bq-init       initialize BeQuite in this repo
    W0.3 /bq-discover   inspect repo → DISCOVERY_REPORT.md
    W0.4 /bq-doctor     environment health → DOCTOR_REPORT.md
    W0.5 /bq-mode       select / show the workflow mode
    W0.6 /bq-new        begin a New Project workflow
    W0.7 /bq-existing   begin an Existing Project Audit workflow

  W1 — Product Framing and Research
    W1.1 /bq-clarify    3-5 high-value clarifying questions
    W1.2 /bq-research   11-dimension verified evidence
    W1.3 /bq-scope      lock IN / OUT / NON-GOALS (+ from-interview)
    W1.4 /bq-plan       IMPLEMENTATION_PLAN.md, no code yet (+ from-issues, migration)
    W1.5 /bq-spec       one-page Spec Kit-compatible spec
    W1.6 /bq-multi-plan unbiased multi-model planning (manual paste)

  W2 — Planning and Build
    W2.1 /bq-assign     break plan into atomic tasks
    W2.2 /bq-implement  implement one approved task at a time
    W2.3 /bq-feature    add feature workflow with 12-type router
    W2.4 /bq-fix        fix workflow with 15-type router (+ regression ledger)
    W2.5 /bq-uiux-variants  1-10 isolated UI directions (+ style=3d)
    W2.6 /bq-live-edit  section-by-section frontend edits

  W3 — Quality and Review
    W3.1 /bq-test       run + write tests (+ from-spec, fixtures)
    W3.2 /bq-audit      full project audit (+ client, a11y)
    W3.3 /bq-review     review current changes (+ Guard Pass on AI diffs)
    W3.4 /bq-red-team   adversarial review (Skeptic mode)

  W4 — Release
    W4.1 /bq-verify     full local verification (+ regressions, drift)
    W4.2 /bq-release    release prep; user pushes (+ readiness, announce, proof, demo-video)
    W4.3 /bq-changelog  categorize commits into CHANGELOG

  W5 — Memory and Handoff
    W5.1 /bq-memory     read / write BeQuite memory snapshots
    W5.2 /bq-recover    resume after a session break
    W5.3 /bq-handoff    generate HANDOFF.md (+ client bundle)

  N — Navigation
    N1 /bq-now          one-line status (faster than this menu)
    N2 /bq-help         full command reference (with IDs)
    N3 /bq-explain      plain-English explainer
    N4 /bq-suggest      MAIN NAVIGATION ASSISTANT — commands + skills + mode + gates + confidence

  O — Orchestrators
    O1-O6 /bq-p0../bq-p5  walk one phase in order
    O7 /bq-auto         scoped autonomous runner (reports "Internal workflow executed: <IDs>")

  C — Capability commands
    C1 /bq-presentation premium PPTX or HTML decks (variants, strict/creative, motion)
    C2 /bq-writing-dna  reusable writing profile → writing in YOUR voice (ethics-bound)
    C3 /bq-reference    screenshot/URL/flow → design extraction + clone-safe rebuild blueprint
    C4 /bq-knowledge    docs → knowledge pack / FAQ / RAG blueprint (build/ask/rag-plan/export)
    C5 /bq-course       Course Engine — validation → curriculum → launch (Arabic/MENA aware)
    C6 /bq-pain-radar   public pain mining → MVP/service/course/automation ideas (ethical sources only)
    C7 /bq-integrate    API docs → integration blueprint (UNVERIFIED markings, invents nothing)
    C8 /bq-proposal     job post → honest tailored proposal (Writing DNA, no overpromising)
    C9 /bq-job-finder   find real work opportunities (+ hidden gems)
    C10 /bq-make-money  legitimate earning tracks (10 tracks + hidden gems)

  M — Maintenance
    M1 /bq-update       update BeQuite itself (safe + non-destructive)
    M2 /bq-skill-audit  structural quality loop over all skills (+ command-router drift checks)

Automatic skill routing (alpha.20): you describe the goal — BeQuite selects the
right expert skills itself. You never need to name skills manually.
Command Router (alpha.22): every non-trivial command ends with Next Command
Recommendations (required next + 2-6 set + accelerators + do-not-run-yet).
Confidence Forecast (alpha.21): plans and tasks carry calibrated success
percentages with evidence levels — confidence is a report, not a feeling.

Operating modes (alpha.12 — composable, set per command):
  deep                  quality matters most · full 11-dim research · full red-team
  fast                  small scoped work · memory-first · 3 dims · still tests + verifies
  token-saver (lean)    long sessions · reuse cached research + targeted reads (NOT token-free)
  delegate              strong model architects → cheap model implements → strong model reviews

Mode examples:
  /bq-auto deep "your project idea"
  /bq-auto fast "your small fix"
  /bq-auto token-saver "your scoped task"     (alias: /bq-auto lean "...")
  /bq-auto delegate "prepare work for cheaper model"
  /bq-auto deep delegate "research deeply, then produce delegated tasks"

Modes adjust depth + cost + speed, NOT safety. All 17 hard human gates apply regardless of mode.
Active mode: .bequite/state/CURRENT_MODE.md · History: MODE_HISTORY.md

Frontend design continuity (alpha.17 — the quality promise):
  Hero quality is not enough — every visible section must meet the Design DNA.
  Master skill: bequite-frontend-design-system (coordinates ux-ui-designer / frontend-quality / live-edit)
  Design DNA: .bequite/design/DESIGN_DNA.md · Gate spec: docs/architecture/DESIGN_CONTINUITY_GATE.md
  Runs inside: /bq-feature /bq-fix /bq-auto /bq-uiux-variants /bq-live-edit /bq-audit /bq-review /bq-red-team /bq-verify

Reliability & hooks (alpha.18):
  Opt-in Claude Code hooks machine-enforce the safety subset (destructive ops · secrets · weasel-word "done" claims) — review before enabling, NOT active by default.
  bequite-context-engineer (PROJECT_DNA + WORKING_NOTES, all workflows) · bequite-anti-hallucination (evidence over claims · citation-or-strike).
  Docs: docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md · CONTEXT_ENGINEERING.md · HARNESS_AND_PROMPT_QUALITY.md

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

## Orchestrator reference (alpha.22 orchestration update)

This command consults the global orchestration brain: `bequite-orchestrator` skill + `.bequite/state/ORCHESTRATION_MAP.md` — the source of truth when commands/skills conflict, workflows seem duplicated, the next step is unclear, or a task matches no existing capability (Missing Capability protocol).
