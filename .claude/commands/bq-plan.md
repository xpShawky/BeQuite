---
description: Write a complete implementation plan — vision, architecture, stack, file plan, phase plan, task plan, test plan, risks, acceptance criteria, rollback, open questions. Activates senior-engineer / architect / security / devops thinking. No code yet.
---

# /bq-plan — write the definitive plan

## Purpose

Write the **definitive implementation plan** that all downstream work hangs from. No code in this command — markdown only. The plan is the contract; tasks (`/bq-assign`) and implementation (`/bq-implement`) execute against it.

A good plan answers: what are we building, with what stack, in what order, with what tests, what could go wrong, how do we know we shipped.

## When to use it

- After `/bq-research` (and ideally `/bq-scope`)
- Before `/bq-assign` and `/bq-implement`
- Whenever you need a single source of truth other engineers can read

## Preconditions

- `BEQUITE_INITIALIZED ✅`
- `MODE_SELECTED ✅`
- For most modes: `SCOPE_LOCKED ✅` (you have to know what's in/out before planning how to build it)

## Required previous gates

- `BEQUITE_INITIALIZED`
- `MODE_SELECTED`
- `CLARIFY_DONE` (recommended)
- `RESEARCH_DONE` (recommended; for solo prototypes you can skip — write the plan, flag the unverified items)
- `SCOPE_LOCKED` (strongly recommended)

## Files to read

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/audits/RESEARCH_REPORT.md`
- `.bequite/audits/DOCTOR_REPORT.md`
- `.bequite/plans/SCOPE.md`
- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/DECISIONS.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- `.bequite/state/PROJECT_STATE.md`

If any required file is missing, suggest running the prerequisite command and exit early.

## Files to write

- `.bequite/plans/IMPLEMENTATION_PLAN.md` (new — 13 sections)
- `.bequite/state/DECISIONS.md` (plan approval appended)
- `.bequite/state/WORKFLOW_GATES.md` (`PLAN_APPROVED ⚪ pending user`)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Steps

### 1. Activate the right thinking modes

This command consults multiple skills at once:

- `bequite-project-architect` — overall architecture, stack ADR
- `bequite-backend-architect` — server-side design (if applicable)
- `bequite-database-architect` — data model + schema (if applicable)
- `bequite-security-reviewer` — threat model + controls
- `bequite-devops-cloud` — deployment + CI/CD strategy
- `bequite-ux-ui-designer` — page/component plan (if UI)
- `bequite-frontend-quality` — frontend file structure (if frontend)
- `bequite-testing-gate` — test plan + pyramid

Read each skill's SKILL.md as needed during plan authoring.

### 2. Write IMPLEMENTATION_PLAN.md (13 sections)

```markdown
# Implementation Plan

**Generated:** <ISO 8601 UTC>
**Target:** <version, e.g. v1 first ship>
**Mode:** <New Project | Add Feature | ...>

## 1. Vision

(2-3 sentences: what is this product, what problem does it solve, who is it for.)

## 2. Current context

- Stack detected: <from DISCOVERY>
- Decisions locked: <count> (see DECISIONS.md)
- Research dimensions covered: <count> (see RESEARCH_REPORT.md)
- Open questions remaining: <count> (see OPEN_QUESTIONS.md)
- Scope locked: <date in SCOPE.md>

## 3. Non-goals

(List from SCOPE.md NON-GOALS — verbatim. Important to surface here.)

## 4. Architecture

```text
<ASCII or markdown diagram of high-level architecture>
```

(2-4 paragraphs explaining the architecture, data flow, deployment model.)

## 5. Stack decision

| Layer | Choice | Why (from RESEARCH §1) |
|---|---|---|
| Runtime | <e.g. Node 22 + TypeScript 5.6> | <reason> |
| Web framework | <e.g. Next.js 15 App Router> | <reason> |
| Database | <e.g. Postgres via Supabase> | <reason> |
| ORM | <e.g. Drizzle> | <reason> |
| Auth | <e.g. Better-Auth> | <reason> |
| Styling | <e.g. Tailwind v4 + shadcn/ui> | <reason> |
| Test runner | <e.g. Vitest + Playwright> | <reason> |
| Hosting | <e.g. Vercel> | <reason> |
| CI/CD | <e.g. GitHub Actions> | <reason> |
| Monitoring | <e.g. Sentry + Vercel Analytics> | <reason> |

## 6. File plan

```text
<tree of directories + files this version creates / modifies>

app/
├── (auth)/
│   ├── signin/page.tsx                              NEW
│   └── signup/page.tsx                              NEW
├── api/
│   └── auth/[...all]/route.ts                       NEW
├── dashboard/
│   ├── page.tsx                                     NEW
│   └── layout.tsx                                   NEW
lib/
├── auth.ts                                          NEW (Better-Auth init)
├── db.ts                                            NEW (Drizzle client)
└── ...
```

Mark each: NEW / MODIFIED / DELETED.

## 7. Phase plan

| Phase | Outcome | Acceptance evidence | Est. time |
|---|---|---|---|
| P1 | Scaffold + DB up | `npm run dev` boots; migrations succeed | 30m |
| P2 | Auth flow | sign-up + sign-in tested via Playwright | 1h |
| P3 | Domain CRUD | <feature> list + create endpoint pass tests | 2h |
| P4 | Admin panel | /admin route renders today's <feature> | 1h |
| P5 | Email | Resend integration; sign-up sends a real email | 30m |
| P6 | Verify | All Playwright walks + axe + smoke pass | 30m |

## 8. Task plan

Atomic tasks (≤5 min each), dependency-ordered. Each task has ONE acceptance criterion.

| ID | Task | Depends on | Acceptance |
|---|---|---|---|
| T-1.1 | Init Next.js 15 app | none | `npm run dev` boots on :3000 |
| T-1.2 | Set up Drizzle + Supabase client | T-1.1 | `migrations/` exists; `db:migrate` runs |
| T-2.1 | Install Better-Auth | T-1.1 | `lib/auth.ts` exports `auth` |
| T-2.2 | Sign-up page | T-2.1 | Form submits; user appears in DB |
| ... | ... | ... | ... |

## 9. Test plan

| Phase | Test type | Specific tests |
|---|---|---|
| P1 | Smoke | `GET /` → 200 |
| P2 | Integration | Playwright: sign-up creates user; sign-in works |
| P3 | API | `POST /api/<x>` creates row; `GET` returns it |
| ... | ... | ... |

Test pyramid: 70% unit, 20% integration, 10% E2E. Coverage target: 80% on touched files.

## 10. Risks + mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <e.g. Better-Auth v1 migration breaks> | low | medium | pin minor version; lockfile committed |
| <e.g. Supabase free tier hits row limits> | medium | low | document upgrade path |
| ... | ... | ... | ... |

## 11. Security considerations

(from `bequite-security-reviewer` — OWASP Top 10 mapping, threat model, secrets handling, auth flow)

| Area | Controls |
|---|---|
| Auth | Better-Auth + email verification + rate limit |
| Secrets | env vars; no `.env` committed; production via host's secret manager |
| Input validation | Zod schemas at every API boundary |
| OWASP | (mapping per RESEARCH §8) |

## 12. Deployment + DevOps considerations

(from `bequite-devops-cloud`)

| Area | Plan |
|---|---|
| Environments | local / preview / production |
| CI gates | lint, typecheck, unit, integration, build |
| Preview deploys | Vercel preview per PR |
| Production deploy | merge to main → Vercel auto-deploy |
| Rollback | revert commit + redeploy; DB migrations forward-only |
| Monitoring | Sentry errors; Vercel Analytics page-views; uptime check via Better Stack |
| Secrets management | Vercel env vars per environment |

## 13. Acceptance criteria for v1 ship

- All "IN scope" items from SCOPE.md ship
- `/bq-verify` passes (full gate matrix)
- README explains install + run + test in <5 min
- One Playwright walk per user-facing flow
- No banned weasel words in commit messages or completion reports
- Lighthouse / axe baseline met (if UI)
- Security checklist complete (per §11)

## 14. Rollback plan

If v1 needs to roll back:
- Tag `git revert <commit>` and redeploy
- Database: schema is forward-only (no destructive migrations in v1)
- Auth: sessions invalidated on env-var rotation
- Communication: status page update + email to affected users

## 15. Open questions

(Items from OPEN_QUESTIONS.md not yet resolved. Flag prominently — the plan is provisional in those areas.)

| Question | Owner | Blocking? |
|---|---|---|
```

### 3. Present + confirm

Show the user the plan structure. Ask:

> "Plan written. (a) approve and run `/bq-assign` — (b) iterate on a specific section — (c) get a second opinion via `/bq-multi-plan` — your call?"

Wait for explicit user response. **Do not proceed past this point without approval.**

### 4. Update state on approval

If user approves:
- Mark `PLAN_APPROVED ✅` in `WORKFLOW_GATES.md`
- Append "Plan approved on <date>" to `DECISIONS.md`
- `LAST_RUN.md` updated
- `AGENT_LOG.md` appended

If user iterates:
- Apply requested changes, re-present, wait again
- Keep gate as `PLAN_APPROVED ❌ pending user`

If user wants multi-plan:
- Mark `PLAN_APPROVED ❌ pending`
- Suggest `/bq-multi-plan` and exit

### 5. Report back

```
✓ Plan written

Sections: 15
Phases:   <count>
Tasks:    <count>
Risks:    <count>
Open Qs:  <count>

Plan: .bequite/plans/IMPLEMENTATION_PLAN.md

Next: /bq-assign       break plan into actionable tasks
      /bq-multi-plan   get a second opinion before committing
```

## Output format

Print summary + ask for approval. Full plan in the file.

## Quality gate

- All 15 sections written (no "TODO" placeholders in shipped plan)
- Every task has ONE acceptance criterion
- No banned weasel words
- Section §11 (security) coverage matches RESEARCH §8
- Section §12 (devops) matches RESEARCH §10
- Open questions in §15 match unresolved items in OPEN_QUESTIONS.md
- User has explicitly approved (or chosen iterate / multi-plan)

## Failure behavior

- Required upstream file missing → suggest the prerequisite command and exit
- User keeps rejecting → don't auto-iterate past 3 rounds; ask the user to pair-debug the disagreement
- Critical RESEARCH gap (e.g. deprecated central dep) → flag in §10 risks and pause for user decision

## Rules

- **No code in /bq-plan.** Markdown only.
- **Every task has an acceptance criterion.** If you can't think of one, the task is too vague.
- **Mark unresolved questions in §15.** Don't pretend the plan is complete.
- **No banned weasel words** — `should / probably / seems to / appears to / I think it works / might / hopefully / in theory`.

## Skills activated (multi)

- `bequite-project-architect`
- `bequite-backend-architect` (if backend)
- `bequite-database-architect` (if DB)
- `bequite-security-reviewer`
- `bequite-devops-cloud`
- `bequite-ux-ui-designer` (if UI)
- `bequite-frontend-quality` (if frontend)
- `bequite-testing-gate`

## Usual next command

- `/bq-multi-plan` — second opinion (recommended for high-stakes plans)
- `/bq-assign` — break plan into actionable tasks

---

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, design system, or workflow this command names in its stack table is an EXAMPLE, not a mandatory default.**

§5 (Stack decision) of IMPLEMENTATION_PLAN.md must produce **decision sections** for each major pick — not bare names.

**Do not write in the plan:** "Use Next.js 15."
**Write:** "Next.js 15 is one candidate. Compared against alternatives [list]; chosen because [reasons tied to the 10 questions]; risk [X]; rollback plan [Y]."

The 10 decision questions every stack pick must answer:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

For each major pick, embed a decision section (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan) in §5 or §11/§12 of the plan. For large or regulated projects, write a full ADR at `.bequite/decisions/ADR-XXX-<tool>-choice.md` instead.

**Do not auto-install.** The plan declares what tools the project will adopt; `/bq-implement` only installs deps after the decision section is present and approved.

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.
