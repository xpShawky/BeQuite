# The BeQuite pipeline (v1)

The one description of how work flows. Every action command is an entry point into this pipeline: `/bq-auto` runs all of it for an intent, `/bq-feature`, `/bq-fix`, `/bq-motion` and `/bq-content` are routes that preset the stages, and the phase commands (`/bq-clarify`, `/bq-plan`, `/bq-implement`, `/bq-verify` ...) run one stage by hand. The short contract block at the top of each command points here; when the plugin's SessionStart hook is on, the state this pipeline needs is injected at the start of every session.

## The stages

| # | Stage | Does | Writes | Sets | Skills (usual) | Skipped when |
|---|---|---|---|---|---|---|
| 0 | **Up to date** | `bash .claude/bequite/bin/bq-update.sh`: hourly check, automatic update when a newer BeQuite is published (backup first, memory untouched, never blocks offline) | `.bequite/state/UPDATE_CHECK.md` | - | updater | never |
| 1 | **Orient** | read `ACTIVE.md`, the work folder, `LAST_RUN.md`, the top `MISTAKE_MEMORY.md` lessons, `CAPABILITIES.md`; decide active work or new work; restate the goal and what done means | `work/<id>/brief.md` (new work) | `BEQUITE_INITIALIZED` if missing | orchestrator, context-engineer | never |
| 2 | **References** (creative work only) | study real human references before any creative output: sites, films, posts, decks; measure them | `work/<id>/research.md` § References | `REFERENCES_STUDIED` | human-taste, video-intel, frontend-design-system | code-only work |
| 3 | **Research** | facts that change (versions, prices, platform rules, competitors) from primary sources, dated; a subagent when the reading is wider than five sources | `work/<id>/research.md` | `RESEARCH_COMPLETE` | researcher (`bq-researcher` subagent) | fast mode on a known stack; the facts are already in memory and under 120 days old |
| 4 | **Options board** | two to four real options built from `CAPABILITIES.md` (what this machine and this user actually have), each with cost, risk and the ten decision questions | `work/<id>/plan.md` § Options | - | project-architect, orchestrator | a one-line fix |
| 5 | **Plan** | the chosen option as a plan: files, steps, tests, rollback, the gates it will need | `work/<id>/plan.md`, `tasks.md` | `PLAN_APPROVED` after stage 6 | project-architect, delegation (large work) | a one-line fix (the plan is the commit message) |
| 6 | **Approval** | the user approves the plan; creative work shows options, script, style and render plan; hard human gates always stop here | the decision in `work/<id>/log.md` | `PLAN_APPROVED` | - | auto mode on safe, scoped, non-creative work (it states the plan and continues) |
| 7 | **Build** | one task at a time, smallest change, tests written with the change | code, assets | `IMPLEMENTATION_DONE` (per work) | the domain specialists | read-only commands |
| 8 | **Guard** | an independent second pass for the failure modes generated work shows | `audits/GUARD_PASS_REPORT.md` or the work's `review.md` | - | guard-pass, security-reviewer (risky domains), `bq-red-team` subagent (high stakes) | read-only commands |
| 9 | **Verify** | re-run every check the way a user would (browser for UI, the real command for a CLI); creative work also passes the human test | `work/<id>/evidence.md`, `verify.md` | `VERIFY_PASSED` (`HUMAN_TEST_PASSED` for creative) | testing-gate, anti-hallucination, `bq-verifier` subagent | never |
| 10 | **Write back** | the work log, `LAST_RUN.md`, `AGENT_LOG.md`, `SKILL_USAGE_LOG.md`, `MISTAKE_MEMORY.md` when a lesson surfaced, `CHANGELOG.md` when behaviour changed; then the next-command recommendations | the files named | - | context-engineer | never |

A later stage never starts while an earlier stage's gate is open; the command names the missing gate and stops. Hard human gates (`CLAUDE.md`) stop any stage.

## How the entry points preset the stages

| Entry point | Stages | Notes |
|---|---|---|
| `/bq-auto <intent>` | 0-10 for the intent's scope | creative intents stop at stage 6; see `/bq-auto` for intents and modes |
| `/bq-feature` | 0, 1, 3 (scoped), 4, 5, 6, 7, 8, 9, 10 | the feature-type router: `FEATURE_AND_FIX_WORKFLOWS.md` |
| `/bq-fix` | 0, 1, reproduce (inside 3), 5 (root cause and the smallest patch), 7, 8, 9 (the regression test fails before, passes after), 10 | the fix-type router: `FEATURE_AND_FIX_WORKFLOWS.md` |
| `/bq-motion` | 0, 1, 2, 3, 4, 5, 6 (script, style, render plan), 7 (animatic, build rounds), 9 (human test, QC), 10 | M-phases in `bequite-motion-director` |
| `/bq-content` | 0, 1, 2 (radar and study), 5 (script), 6 (per post), 7 (produce, package), 9 (human test, package check), 10 | nothing is posted without a yes per post |
| phase commands | the one stage they name, plus 0, 1 and 10 | e.g. `/bq-plan` = 4 + 5, `/bq-verify` = 9 |

## Subagents (when they pay)

Allowed when the reading is wider than five sources, when a check must be independent of the builder, or when the output would flood the main context; otherwise the stage runs inline. Shipped definitions in `.claude/agents/`: `bq-researcher` (stage 3), `bq-red-team` (stage 8), `bq-verifier` (stage 9), `bq-scout` (fast sweeps for stages 2 and 3 on the fast model). Never more readers than distinct questions.

## Modes

`fast` shortens stages 3 and 4; `deep` widens 3 and adds `bq-red-team` at 8; `token-saver` reuses cached research and summaries; `delegate` splits 5 (strong model) from 7 (cheaper model) with a task pack and a strong-model review at 8. Modes never skip 0, 6 (hard gates), 9 or 10.

## Evidence rule

Stage 9 is the only place "done" is earned: the command, its exit code and the decisive output in `evidence.md`, or `UNVERIFIED:` with the reason. Banned in a completion report: should, probably, seems to, appears to, I think it works, might, hopefully, in theory.
