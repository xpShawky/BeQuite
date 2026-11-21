---
description: Scoped autonomous runner. Parses the intent (new, existing, feature, fix, uiux, frontend, backend, database, security, testing, devops, scraping, automation, deploy, live-edit, variants, release, motion, content), runs the BeQuite pipeline for that scope only, and continues until the work is verified and written back. Pauses only at hard human gates; creative work stops at the plan.
---

# /bq-auto: the pipeline, end to end, for one intent

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks).
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

`/bq-auto` runs the stages of `.claude/bequite/docs/architecture/PIPELINE.md` (up to date, orient, references, research, options board, plan, approval, build, guard, verify, write back) for one intent, with minimum interruption and maximum discipline. It does not stop to ask "should I continue?", "do you approve?" or "want tests?": if the work is safe and scoped, it goes on until verified, tested and logged. Strategy and the full rules: `.claude/bequite/docs/architecture/AUTO_MODE_STRATEGY.md`, `.bequite/state/AUTO_MODE_RULES.md`.

## Syntax

```
/bq-auto [intent] [mode...] [key=value...] "<task>"
/bq-auto phase=P0..P5                     walk exactly one phase of the active work
```

Intent: one keyword below, or inferred from the task (ambiguous: one question, then go on). Modes: `fast`, `deep`, `token-saver` (`lean`), `delegate`; they compose (`deep delegate`). Options: `variants=N`, `max-cost-usd=N`, `--manual-approval`.

## Intents

| Intent | Scope | Route / skills |
|---|---|---|
| `new` | the full lifecycle P0-P5 | project-architect + discovery's specialists |
| `existing` | P0 audit: init, discover, doctor, audit, report | researcher, security-reviewer, frontend-quality |
| `feature` | add-feature cycle | `/bq-feature` (feature-type router) |
| `fix` | fix cycle | `/bq-fix` (fix-type router) + problem-solver |
| `uiux` / `frontend` | UI work only (`variants=N` routes to `/bq-uiux-variants`) | frontend-design-system and its members |
| `backend` / `database` / `security` / `testing` / `devops` | that domain only, scoped audit + fix + verify | the domain's specialist |
| `scraping` / `automation` | blueprint first (`/bq-knowledge automation`), then build | automation (+ backend-architect) |
| `deploy` | verify, plan the deploy, stop at every production touch | devops-cloud, release-gate |
| `live-edit` / `variants` | `/bq-live-edit` / `/bq-uiux-variants` | live-edit / ux-ui-designer |
| `release` | verify, changelog, print the release commands, stop for the user's push and tag | release-gate |
| `motion` | `/bq-motion`: M0 brief and M1 references, then **always stops at the plan** (script, style, render plan each wait for a yes) | motion-director, kinetic-type, sound-voice, render-pipeline |
| `content` | `/bq-content`: radar to a packaged draft; stops at the approval per post | trend-radar, format-dna, hooks-and-copy, publish-prep |

Creative work (motion, content, variants, presentations, brand work, new products) is plan-first even in auto mode: research and options, then the plan waits for approval before output.

## Hard human gates (the only pauses)

Destructive deletion · migrations on shared or production databases · production server, VPS, Nginx or SSL changes · secret or key handling · auth or security-model changes · architecture changes · deleting an implementation with live callers · a scope contradiction · `--manual-approval` · the cost ceiling (default $20 per session) or wall-clock ceiling (default 6 h) · a banned word in a completion claim · three failures in a row on one task · a UI variant winner · release push or tag · paid services or credits · for creative work, the script, style and render plan. The full list and wording: `CLAUDE.md` and `AUTO_MODE_RULES.md`.

## Steps

1. **Parse** the intent, modes, options and task. Name the work: the active work or a new one (`/bq-work new`).
2. **Run the pipeline stages for the scope** (`PIPELINE.md`, "How the entry points preset the stages"). Set `.bequite/state/CURRENT_MODE.md` and `CURRENT_PHASE.md` as phases complete.
3. **Between stages:** success and no gate: continue. A hard gate: pause with the resume hint below. A recoverable failure (a red test): one `/bq-fix` attempt, then retry. Three failures in a row: pause.
4. **Verify before claiming done:** every gate the intent needs is set; the tests for the changed surface pass; frontend work covers every in-scope section and the phone layout (not only a hero) with a passing continuity and visual QA report; creative work passed the human test; no banned words.
5. **Write back** and report.

## Phase mode (`/bq-auto phase=P0..P5`)

| Phase | Walk | Done when |
|---|---|---|
| P0 Setup | `/bq-init` → `/bq-mode` (user picks) → `/bq-discover` → `/bq-doctor` (new project in an empty folder skips discover) | `BEQUITE_INITIALIZED`, `MODE_SELECTED`, `DISCOVERY_COMPLETE` (or n/a), `DOCTOR_COMPLETE` |
| P1 Framing | `/bq-clarify` (answers) → `/bq-research` → `/bq-scope` (approve) → optional `/bq-multi-plan` → `/bq-plan` (approve) | `CLARIFY_ANSWERED`, `RESEARCH_COMPLETE`, `SCOPE_LOCKED`, `PLAN_APPROVED` |
| P2 Build | new project: `/bq-assign` → `/bq-implement` loop · feature: `/bq-feature` · fix: `/bq-fix` | `TASKS_ASSIGNED` + `IMPLEMENTATION_DONE`, or the feature/fix gates |
| P3 Quality | `/bq-test` → `/bq-audit` (when asked or for audits) → `/bq-review` → optional `/bq-red-team` | `TESTS_PASS`, `REVIEW_APPROVED` (+ `RED_TEAM_RESOLVED`) |
| P4 Release | `/bq-verify` (fail: back to P2/P3) → `/bq-changelog` → `/bq-release` (the user pushes and tags) | `VERIFY_PASSED`, `CONVERGED`, `CHANGELOG_UPDATED`, `RELEASE_PREPPED` |
| P5 Memory | `/bq-memory snapshot` → optional `/bq-handoff` → `/bq-work close` | `MEMORY_SNAPSHOT` (+ `HANDOFF_GENERATED`); work archived |

After each phase: set the next phase, print what ran, the gates set and the next phase; a phase with a missing gate stops and names it.

## Modes

| Mode | Optimizes | Behaviour |
|---|---|---|
| balanced (default) | sane defaults | as the pipeline says |
| `fast` | speed | short discovery, three research dimensions, existing stack, no multi-plan or red-team; still tests, verifies and logs |
| `deep` | quality | full research beyond the obvious sources, multi-plan offered, red-team at phase ends, full verify and audit |
| `token-saver` (`lean`) | tokens | core memory only, summaries before files, cached research, compact reports |
| `delegate` | cost | strong model writes the task pack (`bequite-delegation`), a cheaper model implements, the strong model reviews |

Conflicts: `fast` with `deep` asks one question and defaults to deep for new, security, release and deploy work; `delegate` on a tiny task suggests `fast`; `delegate` with no research adds `deep`. Every run appends one line to `.bequite/state/MODE_HISTORY.md` (mode, outcome, rough cost, tests passed/total).

## Final output

```
✓ /bq-auto <intent> — <task>
Done:           <bullets>
Files changed:  <count + paths>
Tests:          <pass / total>   Browser checks: <ran | skipped: reason>
Verification:   PASS | PARTIAL | FAIL     Remaining: <list | none>
State updated:  LAST_RUN.md · WORKFLOW_GATES.md · AGENT_LOG.md · CHANGELOG.md · work/<id>/verify.md
Next:           <command>
```

Paused at a gate:

```
⏸ Paused at hard gate: <gate>   Reason: <one line>
Required action: <what the user does>   Resume: /bq-auto <same args>
```

## Quality gate

Every stage the scope needs ran or is marked `Not applicable — reason:`; no hard gate was crossed without a yes; "done" carries evidence (command, exit code, output); the next command is named.
