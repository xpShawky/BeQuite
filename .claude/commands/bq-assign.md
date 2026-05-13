---
description: Break the implementation plan into atomic tasks with IDs, priorities, dependencies, acceptance criteria. Writes .bequite/tasks/TASK_LIST.md.
---

# /bq-assign — break plan into atomic tasks

You convert `.bequite/plans/IMPLEMENTATION_PLAN.md` into a list of **atomic tasks** the agent can pick off one at a time.

## Step 1 — Read context

- `.bequite/plans/IMPLEMENTATION_PLAN.md`
- `.bequite/plans/SCOPE.md`
- `.bequite/state/DECISIONS.md`

If IMPLEMENTATION_PLAN.md is missing, suggest `/bq-plan` first and exit.

## Step 2 — Break the plan into tasks

For each phase in the plan, expand each item into one or more **atomic tasks**:

**Atomic** = ≤5 minutes of focused implementer work + one specific acceptance criterion + one or two file changes.

Bad: "Build the auth system" (multi-day)
Good: "T-2.1: Create `lib/auth.ts` exporting `auth` from `better-auth` with email-password provider"

## Step 3 — Order tasks

- Topological order respecting dependencies
- Group by phase (P1, P2, P3, ...)
- Number within phase (T-1.1, T-1.2, T-2.1, ...)
- Mark parallel-safe tasks with `parallel: true` (per AkitaOnRails 2026: only when applying the same change to many files, OR generating similar CRUD endpoints — N > 5 threshold)

## Step 4 — Write TASK_LIST.md

`.bequite/tasks/TASK_LIST.md`:

```markdown
# Task list

**Generated:** <date>
**From plan:** .bequite/plans/IMPLEMENTATION_PLAN.md
**Total tasks:** <count>

## Status legend

- [ ] pending — not yet started
- [~] in-progress — being worked on now
- [x] done — acceptance criterion met
- [!] blocked — see notes
- [-] skipped — see notes

---

## Phase 1 — Scaffold

- [ ] T-1.1 — Init Next.js 15 app
  - Files: `package.json`, `next.config.ts`, `tsconfig.json`
  - Depends on: none
  - Acceptance: `npm run dev` boots; `curl http://localhost:3000` returns HTTP 200
  - Estimated: 5min

- [ ] T-1.2 — Set up Drizzle + Supabase client
  - Files: `lib/db.ts`, `drizzle.config.ts`, `.env.example`
  - Depends on: T-1.1
  - Acceptance: `npm run db:migrate` succeeds against Supabase
  - Estimated: 10min

## Phase 2 — Auth

- [ ] T-2.1 — Install + init Better-Auth
  - Files: `lib/auth.ts`, `app/api/auth/[...all]/route.ts`
  - Depends on: T-1.2
  - Acceptance: `GET /api/auth/session` returns 200
  - Estimated: 5min

- [ ] T-2.2 — Sign-up page
  - Files: `app/(auth)/signup/page.tsx`, `components/SignupForm.tsx`
  - Depends on: T-2.1
  - Acceptance: form submission creates a user row; redirect to /dashboard
  - Estimated: 10min

(... full list ...)

## Parallel-safe groups

- T-3.1, T-3.2, T-3.3, T-3.4 (booking CRUD endpoints) can run in parallel — N=4 below threshold; recommend serial.
- T-4.1, T-4.2, ..., T-4.6 (six similar admin-table cells) — parallel: true (N=6, above threshold)

## Next safe task

T-1.1 — Init Next.js 15 app
```

## Step 5 — Update state

- `.bequite/state/CURRENT_PHASE.md` → "Phase 2 — Build → tasks assigned"
- `.bequite/state/LAST_RUN.md` updated
- `.bequite/logs/AGENT_LOG.md` appended

## Step 6 — Report back

```
✓ Tasks assigned

Phases:   <count>
Tasks:    <count> total
Parallel: <count> tasks marked parallel-safe

Task list: .bequite/tasks/TASK_LIST.md

Next: /bq-implement — pick off T-1.1
```

## Rules

- **Atomic ≤5 min per task.** If a task feels bigger, split it.
- **Every task must have an acceptance criterion.**
- **Mark dependencies explicitly.** "T-2.2 depends on T-2.1" is part of the task entry.
- **Only mark parallel: true when N > 5 + truly independent.** Otherwise, serial is safer (AkitaOnRails 2026).

## Standardized command fields (alpha.6)

**Phase:** P2 — Planning and Build
**When NOT to use:** no plan exists yet (run `/bq-plan` first); or you're in Add Feature / Fix Problem mode (use `/bq-feature` / `/bq-fix` instead — those are self-contained).
**Preconditions:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `PLAN_APPROVED`
**Required previous gates:** `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `PLAN_APPROVED`
**Quality gate:**
- `TASK_LIST.md` exists
- Every task is ≤5 minutes of focused work
- Every task has ONE acceptance criterion
- Tasks are dependency-ordered
- Marks `ASSIGN_DONE ✅`
**Failure behavior:**
- Plan is too vague to extract atomic tasks → return to `/bq-plan` for clarification; do not advance
- Tasks accumulate dependencies (T-2.1 needs T-1.3 needs T-2.7) → flag circular dep; re-order or split
**Memory updates:** Sets `ASSIGN_DONE ✅`. Writes `TASK_LIST.md`.
**Log updates:** `AGENT_LOG.md`.

## Memory files this command reads

- `.bequite/plans/IMPLEMENTATION_PLAN.md`
- `.bequite/plans/SCOPE.md`
- `.bequite/state/DECISIONS.md`

## Memory files this command writes

- `.bequite/tasks/TASK_LIST.md` (new)
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

`/bq-implement` — pick off the first task
