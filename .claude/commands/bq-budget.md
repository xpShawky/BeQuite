---
description: A credit budget for one work. Sets a ceiling (tokens or an estimated cost), assigns a model role to each pipeline stage (strong for plans, reviews and red-team; balanced for building; fast for sweeps), logs what each stage spent, warns at 80%, stops at 100% (a hard human gate), and reports cost per deliverable when the work closes. Modes - set, status, log, report.
---

# /bq-budget: what this work may spend, and what it spent

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Credits are the real limit on agent work: one finished post from a six-role team cost about 634,000 tokens in BeQuite's first test (work 0002, 2026-11-21). This command makes the spend visible per work and stops it at a ceiling the user chose. Model roles come from `.claude/bequite/docs/reference/MODEL_ROLES.md`; BeQuite recommends models and never switches them.

## Syntax

```
/bq-budget set <N>k tokens | $<N> [stage=<role> ...]    ceiling for the active work (+ optional role overrides)
/bq-budget status                                        spent / ceiling, per stage, warnings
/bq-budget log <stage> <tokens> ["note"]                 record a spend (a subagent's reported tokens, a team heartbeat, a session's usage)
/bq-budget report                                        cost per deliverable, for the closing report
```

## The file: `work/<id>/budget.md`

```
Ceiling: <N> tokens (≈ $<estimate>, from the plan's model roles)   Warn at: 80%   Stop at: 100%
| Stage | Model role | Planned | Spent | Notes |
| research | fast (sweeps) / balanced (judgment) | ... |
| plan, review, red-team | strong | ... |
| build | balanced | ... |
| verify | balanced; fast for re-runs | ... |
Log: <date> <stage> <tokens> <source of the number> <note>
Deliverables: <name> -> <tokens> (<share>)
```

## Steps

1. **set:** read the plan's stages; propose per-stage numbers from comparable past work (`MODE_HISTORY.md`, earlier `budget.md` files) or say there is no history; the user confirms the ceiling. A dollar figure is an estimate on a subscription: say so.
2. **log:** only numbers with a source (a subagent's usage line, a team ledger's `record --tokens`, the session's usage view). No source: `UNVERIFIED:` and the reason.
3. **status:** spent / ceiling overall and per stage; at 80% a warning in the next command's first line; at 100% every command stops before starting a new stage and asks: raise the ceiling (the user's yes, written in the log) or stop.
4. **report:** each deliverable with its tokens and share; the costliest stage and one way to make it cheaper next time (a cheaper role, a subagent that was not needed, cached research).

## Quality gate

Every logged number names its source; the ceiling is never raised without the user's yes in the log; the closing report has cost per deliverable.

## Next Command Recommendations (typical)

`/bq-auto` or the next stage's command after `set` · `/bq-work close` after `report`.
