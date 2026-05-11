---
description: Write a complete implementation plan — vision, architecture, stack, file plan, phase plan, task plan, test plan, risks, acceptance criteria, rollback. No code yet.
---

# /bq-plan — write the plan

You are writing the **definitive implementation plan** that everything downstream depends on. **No code in this command — planning only.**

## Step 1 — Read all upstream

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/audits/RESEARCH_REPORT.md`
- `.bequite/audits/DOCTOR_REPORT.md`
- `.bequite/plans/SCOPE.md`
- `.bequite/state/DECISIONS.md`
- `.bequite/state/OPEN_QUESTIONS.md` (note: any unresolved must be flagged in the plan)
- `.bequite/state/PROJECT_STATE.md`

If any of the above are missing, suggest running them first and exit early.

## Step 2 — Write IMPLEMENTATION_PLAN.md

`.bequite/plans/IMPLEMENTATION_PLAN.md`:

```markdown
# Implementation Plan

**Generated:** <ISO 8601 UTC>
**Target:** <version, e.g. v1 first ship>
**Author:** BeQuite plan command

## 1. Vision

(2-3 sentences: what is this product, what problem does it solve, who is it for.)

## 2. Current context

- Stack detected: <from DISCOVERY>
- Decisions locked: <count> (see DECISIONS.md)
- Open questions remaining: <count> (see OPEN_QUESTIONS.md)
- Scope locked: <date in SCOPE.md>

## 3. Non-goals

(List from SCOPE.md NON-GOALS — verbatim. Important to surface here so future reviewers don't have to dig.)

## 4. Architecture

```text
<ASCII or markdown diagram of the high-level architecture>
```

(2-4 paragraphs explaining the architecture, data flow, deployment model.)

## 5. Stack decision

| Layer | Choice | Why |
|---|---|---|
| Runtime | <e.g. Node 20 + TypeScript> | <reason from RESEARCH> |
| Web framework | <e.g. Next.js 15 App Router> | <reason> |
| Database | <e.g. Postgres via Supabase> | <reason> |
| Auth | <e.g. Better-Auth> | <reason> |
| ORM | <e.g. Drizzle> | <reason> |
| Styling | <e.g. Tailwind v4> | <reason> |
| Test runner | <e.g. Vitest + Playwright> | <reason> |
| Hosting | <e.g. Vercel> | <reason> |

## 6. File plan

```text
<tree of directories + files that this version creates / modifies>

app/
├── (auth)/
│   ├── signin/page.tsx                          NEW
│   └── signup/page.tsx                          NEW
├── api/
│   └── auth/[...all]/route.ts                   NEW
├── dashboard/
│   ├── page.tsx                                  NEW
│   └── layout.tsx                                NEW
lib/
├── auth.ts                                       NEW (Better-Auth init)
├── db.ts                                         NEW (Drizzle client)
└── ...
```

Mark each: NEW / MODIFIED / DELETED.

## 7. Phase plan

| Phase | Outcome | Acceptance evidence | Est. time |
|---|---|---|---|
| P1 | Scaffold + DB up | `npm run dev` boots; DB migrations succeed | 30m |
| P2 | Auth flow | sign-up + sign-in tested via Playwright | 1h |
| P3 | Booking CRUD | Booking list + create endpoint pass tests | 2h |
| P4 | Admin panel | /admin route renders today's bookings | 1h |
| P5 | Email | Resend integration; sign-up sends a real email | 30m |
| P6 | Verify | All Playwright walks + axe + smoke pass | 30m |

## 8. Task plan

Atomic tasks (≤5 min of focused work each), dependency-ordered. Each task has an acceptance criterion.

| ID | Task | Depends on | Acceptance |
|---|---|---|---|
| T-1.1 | Init Next.js 15 app | none | `npm run dev` boots on :3000 |
| T-1.2 | Set up Drizzle + Supabase client | T-1.1 | `migrations/` dir exists; `npm run db:migrate` runs |
| T-2.1 | Install Better-Auth | T-1.1 | `lib/auth.ts` exports `auth` |
| T-2.2 | Sign-up page | T-2.1 | Form submits; user appears in DB |
| ... | ... | ... | ... |

## 9. Test plan

For each phase, what tests prove it works:

| Phase | Test(s) |
|---|---|
| P1 | `npm run dev` returns 200 on `/` |
| P2 | Playwright: sign-up creates a user; sign-in works |
| P3 | API test: `POST /api/booking` creates a row; `GET` returns it |
| ... | ... |

## 10. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <e.g. Better-Auth v1 has migration breakage> | low | medium | pin minor version; bun.lockb committed |
| <e.g. Supabase free tier hits row limits> | medium | low | document upgrade path |
| ... | ... | ... | ... |

## 11. Acceptance criteria for v1 ship

- All "IN scope" items from SCOPE.md ship
- `/bq-verify` passes
- README explains install + run + test
- One Playwright walk per user-facing flow
- No `should` / `probably` weasel words in commit messages

## 12. Rollback plan

If v1 needs to roll back:
- Tag git revert
- Database: schema is forward-only (no destructive migrations)
- Auth: Better-Auth sessions invalidated on restart; users re-login

## 13. Open questions

(Items from OPEN_QUESTIONS.md not yet resolved. Flag them prominently — the plan is provisional in those areas.)
```

## Step 3 — Present + confirm

Show the user the plan structure. Ask:

> "Plan written. Want to (a) approve and run /bq-assign, (b) iterate on a specific section, or (c) get a second opinion via /bq-multi-plan?"

## Step 4 — Update state

- `.bequite/state/CURRENT_PHASE.md` → "Phase 1 — Problem Framing → plan written"
- Append decision: "Plan approved" (or "Plan in review") to DECISIONS.md
- `.bequite/state/LAST_RUN.md` updated
- `.bequite/logs/AGENT_LOG.md` appended

## Step 5 — Report back

```
✓ Plan written

Phases:   <count>
Tasks:    <count>
Risks:    <count>

Plan: .bequite/plans/IMPLEMENTATION_PLAN.md

Next: /bq-assign       break plan into actionable tasks
      /bq-multi-plan   get a second opinion before committing
```

## Rules

- **No code in /bq-plan.** Source files come in `/bq-implement`. This command writes markdown only.
- **Every task must have an acceptance criterion.** If you can't think of one, the task is too vague.
- **Mark unresolved questions clearly** in §13. Don't pretend the plan is complete if it's not.
- Use the **`bequite-project-architect`** skill for deep architecture procedures (see `.claude/skills/bequite-project-architect/SKILL.md`).

## Memory files this command reads

- All `.bequite/audits/*.md`
- All `.bequite/plans/*.md`
- All `.bequite/state/*.md`

## Memory files this command writes

- `.bequite/plans/IMPLEMENTATION_PLAN.md` (new)
- `.bequite/state/CURRENT_PHASE.md` (updated)
- `.bequite/state/DECISIONS.md` (appended)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

- `/bq-assign` — break the plan into actionable tasks
- `/bq-multi-plan` — get a second opinion before committing
