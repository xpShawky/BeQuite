---
description: Add one feature through the pipeline. Classifies it with the 12-type router (frontend UI, backend API, database, auth, automation, scraping, deployment, admin panel, dashboard, CLI, integration, security), loads the matching specialists, writes a mini-spec, builds it task by task, tests and verifies it. Arguments demo-data and landing.
---

# /bq-feature: one feature, end to end

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks).
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

A route into `PIPELINE.md` stages 0, 1, 3 (scoped), 4, 5, 6, 7, 8, 9, 10 for one feature, in its own work folder. The type router and its specialists: `.claude/bequite/docs/architecture/FEATURE_AND_FIX_WORKFLOWS.md` (section "/bq-feature: 12-type router").

## Syntax

```
/bq-feature "<feature title>" [type=<1-12 or name>] [mode]
/bq-feature demo-data "<what to seed>"       realistic, labelled demo data (never shipped as real)
/bq-feature landing "<offer or product>"      a landing page through the frontend-design-system loop
```

## Gates

`BEQUITE_INITIALIZED`; the work's `PLAN_APPROVED` before build (auto mode states the plan and continues for safe, scoped work). UI types (1 frontend UI, 8 admin panel, 9 dashboard) also need `DESIGN_DNA_LOCKED` before build and set `DESIGN_CONTINUITY_PASS` and `VISUAL_QA_DONE` before done. Motion, video or 3D on the web adds `PERF_BUDGET_PASS`.

## Steps

1. **Orient.** New work folder (`/bq-work new "<title>" type=feature`) unless the feature belongs to the active work.
2. **Classify** with the 12-type router; a feature may be two types (say both). Load the router's skills plus `bequite-testing-gate`.
3. **Research, scoped:** only what changes for this feature (a library version, an API rule), dated, in `research.md`.
4. **Options and mini-spec** in `spec.md`: what, why, in scope, out of scope, files it will touch, acceptance criteria, test plan, security notes (security-reviewer for auth, input, secrets), deployment notes when it touches deploys, the implementation order.
5. **Approval:** show the mini-spec and wait (or state it and continue in auto mode on safe, scoped work).
6. **Build** task by task, tests with each task. UI types: section by section against the Design DNA (`bequite-frontend-design-system`), re-reading `FRONTEND_CONTEXT_SUMMARY.md` between sections; pick the product type's rules, never a default "cinematic SaaS landing".
7. **Guard:** `bequite-guard-pass`; `bq-red-team` when the feature touches auth, money or data.
8. **Verify** the way a user would: the browser at desktop and phone width for UI, the real command for a CLI, the endpoint for an API. Evidence in `evidence.md`.
9. **Write back:** work log, `CHANGELOG.md` `[Unreleased]` when users see the change, `LAST_RUN.md`.

## Output

```
✓ /bq-feature "<title>" (type <n>: <name>)
Spec: work/<id>/spec.md · Tasks: <done>/<total> · Tests: <pass>/<total>
Verified: <how: browser / command / endpoint> · Gates set: <list>
Next: /bq-review or /bq-verify
```

## Quality gate

Every acceptance criterion has a test or a recorded check; UI features cover every in-scope section and the phone layout, not only the first section; no hard human gate was crossed without a yes.

## Next Command Recommendations (typical)

`/bq-review` (diff review) · `/bq-verify` (before release) · `/bq-fix` if verification found a bug.
