---
description: Write the implementation plan for the active work - options board built from what this machine has, the chosen option as architecture, stack, file map, phases, tasks, tests, risks, security, deployment, acceptance criteria and rollback. No code. Waits for the user's approval. Arguments - from-issues, migration.
---

# /bq-plan: options, then one plan the user approves

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Stages 4, 5 and 6 of `PIPELINE.md`. Markdown only: no code is written here. Skills: `bequite-project-architect` always; `bequite-backend-architect`, `bequite-database-architect`, `bequite-ux-ui-designer`, `bequite-frontend-quality` when the work has those parts; `bequite-security-reviewer`, `bequite-devops-cloud`, `bequite-testing-gate`; `bequite-delegation` when the build will be split between models.

## Syntax

```
/bq-plan [from-issues "<source>" | migration "<from -> to>"]
```

`from-issues` turns issues, feedback or feature requests into a Now / Next / Later roadmap (`.bequite/plans/ROADMAP.md`), each item with its source link and a stated reason for its priority. `migration` writes an upgrade blueprint: dependency diff, breaking-change map, phased plan, rollback.

## Gates

Needs `BEQUITE_INITIALIZED` and `MODE_SELECTED`. `SCOPE_LOCKED` is expected (a plan without a scope plans the wrong thing); `CLARIFY_ANSWERED` and `RESEARCH_COMPLETE` are recommended, and anything the plan assumes without them is listed as unverified. Sets `PLAN_APPROVED` only after the user's yes.

## Steps

1. **Read:** `work/<id>/brief.md`, `spec.md`, `research.md`; `.bequite/state/DECISIONS.md`, `OPEN_QUESTIONS.md`, `PROJECT_DNA.md`, `CAPABILITIES.md` (run `/bq-doctor` if it is empty); `.bequite/audits/DISCOVERY_REPORT.md`.
2. **Options board.** Two to four real options built from `CAPABILITIES.md`, never from defaults:

   | Option | Uses (from CAPABILITIES) | Cost (money, credits, time) | Risk | Cannot do | Verdict |
   |---|---|---|---|---|---|

   Each option answers the ten decision questions (`.bequite/principles/TOOL_NEUTRALITY.md`). Recommend one and say why the others lost. Every package named was checked in its registry this session.
3. **Write `work/<id>/plan.md`** for the chosen option:
   - Vision in two sentences, current context, non-goals.
   - Architecture and stack decision, with the scale tier and the reason.
   - **File-responsibility map:** each file, its one responsibility, which way it may import, its covering tests, and an explicit "do not touch" list. `/bq-assign` refuses to write tasks without it.
   - Phase plan and task plan. Every task has one acceptance criterion; a task without one is too vague.
   - For each phase: the skills it needs, the model role (strong, balanced, fast per `MODEL_ROLES.md`; BeQuite recommends, it never switches), effort, and a confidence with its evidence level.
   - Test plan, risks with mitigations, security considerations, deployment and operations, acceptance criteria for shipping, rollback, open questions.
4. **System Design Risk Check.** When the work touches payments, inventory, bookings, auth, permissions or tenancy, database writes, concurrency, queues, external APIs, webhooks, uploads, admin actions or production, include the block from `.claude/bequite/docs/architecture/SYSTEM_DESIGN_REASONING_STANDARD.md`. The canonical test: one item in stock, two simultaneous buyers. A risk without a named test is an unfinished plan; a blocking unknown stops the build. Outside those domains write "Not applicable" and the reason.
5. **Present and wait.** Show the options board and the plan summary. The user approves, asks for changes, or asks for a second opinion (`/bq-multi-plan`). Record the answer in `work/<id>/log.md` and `DECISIONS.md`; only then set `PLAN_APPROVED`.

## Output

```
Plan: .bequite/work/<id>/plan.md    option chosen: <A/B/C> (<one-line reason>)
Phases: <n>   Tasks: <n>   Open questions: <n>   Confidence: <NN%> (<evidence level>)
Waiting for approval. Next after a yes: /bq-assign
```

## Quality gate

No placeholder sections; every task has an acceptance criterion; unresolved items sit in open questions rather than being papered over; no banned weasel words; the user's approval is recorded before any code.

## Next Command Recommendations (typical)

`/bq-assign` after approval · `/bq-multi-plan` for a high-stakes second opinion · `/bq-red-team` to attack the plan before building.
