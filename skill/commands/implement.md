---
name: bequite.implement
description: Phase 5 — implement one task with TDD discipline (RED-GREEN-REFACTOR), per-task commit, signed receipt. Dispatches to backend-engineer / frontend-designer / database-architect / automation-architect based on task scope. Reviewer + Skeptic + security-reviewer gate at task exit.
phase: P5
persona: backend-engineer | frontend-designer | database-architect | automation-architect
prompt_pack: prompts/implementation_prompt.md
---

# /bequite.implement --task <task-id>

When invoked (or `bequite implement --task <id>`):

## Step 1 — Validate

Read `state/task_index.json`. Confirm task is `pending` or `in_progress`. **Refuse** if `completed`. Read the task card from `specs/<feature>/phases/<phase>/tasks.md`.

## Step 2 — Dispatch to right persona

Based on task scope:

- API / service / job → **backend-engineer**
- UI / design / Impeccable flow → **frontend-designer** (Impeccable-loaded)
- Schema / migration / index → **database-architect**
- Workflow / connector / integration → **automation-architect** (when `ai-automation` Doctrine active)

Multi-aspect tasks: orchestrator coordinates; primary persona ships the work; co-personas review.

## Step 3 — TDD loop (Iron Law II + master §3.7)

### RED
Write the failing test. Run it. Confirm it fails for the right reason (assertion, not import error).

### GREEN
Minimum code to pass the new test. Run new + existing test suite. Confirm green.

### REFACTOR
Clean up. Re-run. Confirm green.

Tasks tagged `prototype: true` may skip RED but always emit GREEN.

## Step 4 — Hooks active throughout

- `pretooluse-secret-scan.sh` — blocks secrets.
- `pretooluse-block-destructive.sh` — blocks Tier-3 commands.
- `pretooluse-verify-package.sh` — blocks hallucinated imports.
- `posttooluse-format.sh` — auto-formats.
- `posttooluse-lint.sh` — warns on lint findings.
- `posttooluse-audit.sh` — light Doctrine drift check.

## Step 5 — Skeptic kill-shot

Before claiming done, Skeptic produces ≥1 kill-shot: "What's the failure mode if the upstream API times out mid-stream?" / "Where does this assume the user is authenticated?" / etc.

Primary persona answers in writing — in receipt or in `docs/risks.md` if accepted-risk.

If the answer requires more code → file as a **new task**, not a sneaky addition.

## Step 6 — Per-task commit + receipt

Conventional Commits format: `feat(<task_id>): <subject>` (or `fix:`, `refactor:`, `test:`, `docs:`, `chore:`).

Receipt at `.bequite/receipts/<sha>-P5-<task_id>.json` (v0.7.0+) — captures input prompt hash, model + reasoning effort, system prompt + memory snapshot, lockfile hash, test command + exit code + stdout hash, diff, cost.

Evidence at `evidence/P5/<task_id>/` — test-output.txt, lint-output.txt, typecheck-output.txt, screenshots/ (UI).

## Step 7 — Update state

`state/task_index.json::status` → `completed`, `completed_at`, `evidence_path`.
`state/recovery.md`, `.bequite/memory/activeContext.md`, `.bequite/memory/progress.md`.

## Stop condition

Task `completed` only when:

- Code lands per task card.
- RED-GREEN-REFACTOR captured.
- Lint + typecheck green.
- Per-task commit landed.
- Receipt emitted.
- Skeptic kill-shot answered.
- State updated.

## Anti-patterns

- Multiple unrelated tasks in one commit (master §7.5).
- Modifying files outside scope without writing why.
- Bypassing input validation (Doctrine Rule 11 + OWASP A03).
- Raw SQL string concatenation.
- Adding a dependency without supply-chain review.
- Weasel words in completion message (Iron Law II).
