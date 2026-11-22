---
description: Full verification before shipping. Runs every gate the project has (install, lint, typecheck, tests, build, smoke, frontend and visual checks, secret scan), converges the work's acceptance criteria against its evidence, and writes an honest PASS or FAIL to work/<id>/verify.md. Arguments - regressions, drift, --strict.
---

# /bq-verify: prove it the way a user would

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Stage 9 of `PIPELINE.md`: the only place "done" is earned. Procedure: `bequite-release-gate` (CI parity, ship or not), `bequite-testing-gate` (evidence format), `bequite-anti-hallucination`. For an independent run, hand the checks to the `bq-verifier` subagent, which did not build the work.

## Syntax

```
/bq-verify [--strict] [regressions | drift]
```

`--strict` stops at the first red gate. `regressions` re-runs only the guard records in `.bequite/state/REGRESSION_LEDGER.md`. `drift` only compares the counts and paths the docs claim with the files that exist.

## Gates

Needs `BEQUITE_INITIALIZED`, `TESTS_PASS`, `REVIEW_APPROVED`. Sets `VERIFY_PASSED` and `CONVERGED` on PASS only.

## Steps

1. **Find the real commands** in the manifest and `.bequite/audits/DISCOVERY_REPORT.md`; never guess a script name.
2. **Build the gate matrix** from what the project has, and run each gate:

| Gate | When | Run |
|---|---|---|
| Clean install | always | the lockfile install (`npm ci`, `pnpm install --frozen-lockfile`, `pip install -e .`) |
| Lint, typecheck | configured | the project's own scripts |
| Unit and integration tests | tests exist | the project's test command |
| Build | a build script exists | the project's build |
| Smoke | a server, API or CLI | start it and call it (`curl` the health route, `<cli> --version`) |
| Frontend e2e | Playwright or similar is installed | the e2e command |
| Design continuity | a frontend with more than one section | `.bequite/design/DESIGN_CONTINUITY_REPORT.md` with no BLOCKER or HIGH drift (`DESIGN_CONTINUITY_PASS`) |
| Visual QA | a frontend | a real browser at desktop and phone width into `.bequite/audits/VISUAL_QA_REPORT.md` (`VISUAL_QA_DONE`); without a browser tool, say so and mark it `UNVERIFIED:` |
| Web performance | motion, video or 3D on the page | the budget in `.claude/skills/bequite-frontend-design-system/references/web-motion.md` (`PERF_BUDGET_PASS`) |
| Human test | creative work | the tell sweep and the blind pick from `bequite-human-taste` (`HUMAN_TEST_PASSED`) |
| Secret scan | always | search the diff and the tree for key patterns; never print a value |
| Lockfile sanity | a manifest exists | exactly one lockfile |
| Regressions | the ledger exists | every guard record still passes |
| Risk tests | the plan has a System Design Risk Check | each named risk has a test that ran |

3. **Record each gate** in `work/<id>/evidence.md`: the command, the exit code, the decisive output lines. A gate that could not run is `UNVERIFIED:` with the reason, never green.
4. **Definition of done:** runnable, typecheck and tests green, no stub, TODO or placeholder in changed files, docs and memory updated.
5. **Converge:** compare `spec.md` acceptance criteria and `tasks.md` with `evidence.md`. Every criterion without evidence becomes a new task, and the verdict is FAIL until it has one.
6. **Write `work/<id>/verify.md`:** date, mode, the matrix with status and one-line output per gate, failures, warnings, verdict. State a confidence with its evidence level (`CONFIDENCE_CALIBRATION_STRATEGY.md`).

## Output

```
Verify: PASS | FAIL    gates: <green> ok, <yellow> warn, <red> failed, <n> skipped, <n> UNVERIFIED
Report: .bequite/work/<id>/verify.md
Next: /bq-release (PASS) or /bq-fix "<first failing gate>" (FAIL)
```

## Quality gate

Every status has a command and an exit code behind it; skipped gates say why; a required gate that is red or unverified means FAIL; a previously fixed bug that returns is FAIL plus a `MISTAKE_MEMORY.md` entry; a difference between CI and local results is fixed in the script, not waved through.

## Next Command Recommendations (typical)

PASS: `/bq-changelog` then `/bq-release`. FAIL: `/bq-fix` with the failing evidence.
