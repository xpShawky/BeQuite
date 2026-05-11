---
description: Phase 1 orchestrator — Product Framing and Research. Walks /bq-clarify → /bq-research → /bq-scope → /bq-plan in order, with optional /bq-multi-plan for high-stakes decisions. Goal: decide what to build before writing code.
---

# /bq-p1 — Phase 1 orchestrator: Product Framing and Research

## Purpose

Run Phase 1 commands in order, in one pass. P1's job is to **decide what to build**. No code yet. The output is an approved IMPLEMENTATION_PLAN.md.

## When to use it

- P0 complete (mode selected, discovery + doctor reports exist)
- You want to think hard before coding
- You're tired of running `/bq-clarify`, `/bq-research`, `/bq-scope`, `/bq-plan` one at a time

## Preconditions

- `BEQUITE_INITIALIZED ✅`
- `MODE_SELECTED ✅`
- Mode is one of: New Project, Existing Audit, Research Only
- (For other modes, P1 is mostly skipped — use `/bq-p2` directly)

## Required previous gates

- `BEQUITE_INITIALIZED`
- `MODE_SELECTED`
- `DISCOVERY_DONE` (or N/A for fresh New Project)

## Files to read

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/CURRENT_MODE.md`
- `.bequite/audits/DISCOVERY_REPORT.md` (if exists)
- `.bequite/audits/DOCTOR_REPORT.md` (if exists)
- `.bequite/state/OPEN_QUESTIONS.md` (any pre-queued questions)

## Files to write

- `.bequite/state/OPEN_QUESTIONS.md` (via `/bq-clarify`)
- `.bequite/audits/RESEARCH_REPORT.md` (via `/bq-research`)
- `.bequite/plans/SCOPE.md` (via `/bq-scope`)
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (via `/bq-plan`)
- `.bequite/plans/MULTI_PLAN_MERGED.md` (optional, via `/bq-multi-plan`)
- `.bequite/state/WORKFLOW_GATES.md` (gates ticked)
- `.bequite/state/CURRENT_PHASE.md` (advances to P2 at end)
- `.bequite/logs/AGENT_LOG.md`

## Steps

### 1. /bq-clarify

Pause for user to answer 3-5 high-value questions (or accept defaults).

**Hard human gate.** Mark `CLARIFY_DONE ✅` once answered.

If mode = **Research Only**, this is the only question phase.

### 2. /bq-research

11-dimension verification (stack, product, competitors, failures, success, user journey, UX/UI, security, scalability, deployment, differentiation). WebFetch for live data — no memory-based claims.

Mark `RESEARCH_DONE ✅`.

If mode = **Research Only** → STOP here. Print the research report path. Phase complete.

### 3. /bq-scope

Force IN / OUT / NON-GOALS commitment. Agent drafts; user approves or moves items.

**Hard human gate.** Mark `SCOPE_LOCKED ✅` once user confirms.

### 4. (Optional) /bq-multi-plan

Ask the user: "Want a second-opinion plan from another model? (y/N)"

If yes → run `/bq-multi-plan` (manual paste flow into ChatGPT or Gemini). Mark `MULTI_PLAN_DONE ⚪ optional ✅`.

If no → skip. Mark `MULTI_PLAN_DONE ⚪ optional skipped`.

### 5. /bq-plan

Write IMPLEMENTATION_PLAN.md. Pure planning, no code. Includes vision, architecture, stack table, file plan, phase plan, task plan, test plan, risks, acceptance criteria, rollback plan.

If multi-plan was run, merge insights.

**Hard human gate.** Print the plan and wait for user approval.

Mark `PLAN_APPROVED ✅`.

### 6. Mark phase complete

If `CLARIFY_DONE`, `RESEARCH_DONE`, `SCOPE_LOCKED`, `PLAN_APPROVED` are all `✅`:
- Set `.bequite/state/CURRENT_PHASE.md` → `P2 — Planning and Build`

### 7. Print summary

```
✓ Phase 1 complete — Product Framing and Research

Mode:           <mode>
Questions:      <answered> / <asked>
Research:       <count> dimensions covered
Scope:          IN: <N>, OUT: <N>, NON-GOALS: <N>
Plan:           .bequite/plans/IMPLEMENTATION_PLAN.md (<line count>)
Multi-plan:     <yes/no>

Next phase: P2 — run /bq-p2 or /bq-assign
```

## Output format

Narrate each step. At the end, print the summary above.

## Quality gate

- `CLARIFY_DONE ✅`
- `RESEARCH_DONE ✅`
- `SCOPE_LOCKED ✅`
- `PLAN_APPROVED ✅`
- Plan contains all 13 required sections (per `/bq-plan` spec)
- No banned weasel words in plan

## Failure behavior

- User refuses to answer clarify questions → use defaults and proceed; log the unanswered questions in OPEN_QUESTIONS.md
- Research finds a blocker (e.g. deprecated library that's central to the plan) → write the finding to `RESEARCH_REPORT.md` and **pause** before scope
- User rejects scope → return to scope drafting; do not advance
- User rejects plan → return to scope or plan; do not advance to P2

## Usual next command

- `/bq-p2` — run Phase 2 (Planning and Build)
- Or `/bq-assign` followed by `/bq-implement` to start atomic-task execution
