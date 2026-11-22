---
name: bequite-delegation
description: Use when work is big enough that who thinks and who types matters - a large feature with a clear shape, a high-stakes decision that deserves a second independent plan, or independent tracks that can run in parallel. Routes planning and review to the strong model, mechanical building to a cheaper one, and cross-checks plans from other models without leaking one plan into another. Replaces the former delegate-planner and multi-model-planning skills.
last_verified: 2026-11-21
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://code.claude.com/docs/en/model-config
  - https://code.claude.com/docs/en/agent-teams
  - https://code.claude.com/docs/en/costs
  - https://www.anthropic.com/engineering/building-effective-agents
  - https://www.anthropic.com/engineering/multi-agent-research-system
  - https://arxiv.org/abs/2305.14325
  - .claude/bequite/docs/reference/MODEL_ROLES.md
---

# bequite-delegation

Spend the strong model on judgment and the cheaper one on typing, and get a second opinion only where a wrong plan is expensive. Roles, not model names: see `.claude/bequite/docs/reference/MODEL_ROLES.md`. BeQuite recommends a role; it never switches the user's model.

## When to use

- `/bq-auto delegate`, `/bq-plan delegate`, `/bq-assign delegate`, `/bq-review delegate`, `/bq-multi-plan`.
- A feature with a clear architecture and a lot of mechanical change.
- A decision with two defensible answers (data store, auth model, a one-way door).
- Several tracks that touch different files.

Not for: a small fix (the overhead is larger than the saving); exploratory work where the builder must make discovery calls; taste, security trade-offs or UX feel (those stay with the strong model).

## Pick the shape

| Shape | Use when | How, inside Claude Code |
|---|---|---|
| A. Plan strong, build balanced, review strong | Clear shape, much typing | Plan in plan mode on the strong model (the `opusplan` alias does plan-strong/execute-balanced in one session), or write a task pack and run builder subagents with `model: sonnet` or `haiku`; the strong model reviews the diff |
| B. Independent plans, then merge | High-stakes choice | Same briefing to two or more models (subagents on different models, or the user's other chat apps by manual paste); no plan sees another until all are in |
| C. Parallel tracks | Independent parts, different files | One session or worktree per track (`isolation: worktree` for a subagent); one integrator merges at the end |
| D. Agent team | Parallel work where workers must talk to each other | Experimental, off by default, about 7x the tokens of one session in plan mode; 3 to 5 teammates; only if subagents cannot do it |

## Procedure

1. **Decide whether to delegate.** Estimate the strong-model tokens for doing it all vs planning + reviewing only. House rule (`UNVERIFIED:` not measured): under about 30% saving, do not delegate.
2. **Shape A: write the task pack** in `work/<id>/tasks.md` (format in `references/task-pack.md`): per task the goal, files to read, files to edit, files not to touch, steps, edge cases, the test command and expected output, and any hard gate marked `HARD GATE: pause`. Each task fits in a few minutes for the builder.
3. **Builder rules** (put them in the pack): read only the listed files; no architecture decisions; no new dependencies; no edits outside "files to edit"; run the test; mark `[x]` only on a passing run, `[!]` after two failed tries, `[?]` when the pack is unclear; stop at a hard gate.
4. **Shape B: build one neutral briefing** from the spec, constraints and open questions: no mention of any existing plan or preferred answer. Save the prompt and each answer in `work/<id>/delegation/` (`PROMPT.md`, `ANSWER_<model>.md`). Optional second round (debate): each model reads the others' plans and says what it would change.
5. **Merge (shape B):** a table per decision (`Topic | Plan 1 | Plan 2 | Agree?`). Agreements go in. For each disagreement: a hard rule or the doctrine wins; then the option backed by a source or a reproduction; then ask the user. Never average a binary choice. Record each tie-break in `.bequite/state/DECISIONS.md`.
6. **Review (shapes A and C):** the strong model reads the diff against each task's acceptance criteria and runs the guard pass (`bequite-guard-pass`). Verdict per task: approved, approved with comments, rejected with exact fix steps. A task rejected twice goes back to the planner, not to a third build.
7. **Report the model actually running** for each phase, and the cost per phase if the harness shows it; otherwise `UNVERIFIED:`.

## Worked example (this work, 2026-11-21)

The BeQuite v5 relaunch (work 0002) used shapes A and C. The strong model wrote `plan.md` (29.6 KB) and `tasks.md` (19.4 KB): five tracks with their own evidence, log and question files so no two sessions write the same file, and a rule that only track A edits registries. Balanced-model sessions then ran tracks A, B, C1C2, C345 and D in separate worktrees; each commits per task with the self-check green; track A integrates; the strong model returns for the final end-to-end pass. Shape B is reserved for the one-way door at release (the history choice), where the owner decides.

## Quality gate

- Every task in a pack has files to edit, a test command and expected output.
- No builder output was accepted without its test run pasted.
- Shape B prompts are byte-identical apart from the model label, and no prompt mentions another plan.
- Each merged decision cites its tie-break.
- Hard gates inside delegated tasks were stopped at, and the review checked that they were.

## Boundaries

No provider API keys, no driving a consumer chat app with its session cookies (both vendors' terms forbid it); other vendors' models are reached by the user pasting. The builder never installs a dependency the plan did not approve.
