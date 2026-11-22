---
description: Test the pack's skills and commands with scenarios. Each scenario is an input and what must (and must not) come out; scripted checks run as code, model behaviour runs on the fast model. Results land in evals/results; a regression against the last passing run blocks /bq-release. Modes - run, add, list, compare.
---

# /bq-eval: tested skills, not untested prose

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

A skill is a promise about behaviour. This command checks the promise with scenarios and keeps the results, so a change that makes a skill worse is caught before release. When BeQuite is installed as a plugin and the harness's own `claude plugin eval` is available, scenarios run through it; otherwise this command runs them itself. Skills: `bequite-testing-gate` (fail-first, evidence format), `bequite-skill-auditor`.

## Syntax

```
/bq-eval run [<skill or command> | all]      run the scenarios; scripted first, then model scenarios on the fast model
/bq-eval add <skill> "<scenario name>"       write a new scenario file
/bq-eval list                                scenarios per skill, last result
/bq-eval compare                             this run vs the last passing run; regressions are listed first
```

## Scenario files: `evals/<skill>/<name>.md`

```
kind: script | model
run: <command>                      (script: a test script, a validator, a ledger check)
prompt: <the user's message>        (model: what a user would type)
context: <files the model may read>
must: <observable outputs, each checkable>
must_not: <outputs that fail it>
```

## Steps (run)

1. **Scripted scenarios** (no tokens): the tests shipped with skills (for example `bequite-agent-team/scripts/test_heartbeat.py`, `test_operator_bridge.py`, `bequite-publish-prep/scripts/package_check.py` against a planted broken package), validators and `bq_check.py`. Record command, exit code and the decisive output.
2. **Model scenarios** on the fast model, one fresh subagent per scenario, with only the scenario's context: the routing table of `bequite-orchestrator` ("make me a reel" must route to `/bq-motion`), the team chief dropping a planted instruction in its inbox, the editor rejecting an unsourced number. Check each `must` and `must_not` literally; a model answer that is right for the wrong reason fails.
3. Write `evals/results/<date>.md`: per scenario PASS or FAIL with the evidence; the tokens the run cost.
4. **compare:** any scenario that passed in the last passing run and fails now is a regression; `/bq-release` refuses while one is open.

## Quality gate

Every scenario has at least one `must_not`; a failing scenario is never edited to pass without saying why in the result; the release gate reads the last run.

## Next Command Recommendations (typical)

`/bq-fix` for a regression · `/bq-release` when the run is clean.
