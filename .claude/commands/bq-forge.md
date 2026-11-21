---
description: When a work closes, find the procedure that worked and propose it as a new skill or an improvement to an existing one. A candidate lives in .bequite/skills/forge/ with a use counter; it is promoted into the pack only after three evidenced uses and the user's yes. Modes - propose, use, status, promote.
---

# /bq-forge: the pack learns from the owner's own work, with proof

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks).
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Skills written from imagination rot; skills distilled from work that passed its checks do not. This command reads a closing work's `evidence.md` and `log.md`, finds a procedure that worked (and the lessons that shaped it), and drafts it to the v1 skill rubric. Nothing reaches `.claude/skills/` until it has worked three times. Skills: `bequite-skill-auditor` (rubric, overlap), `bequite-orchestrator` (does a skill or command already cover it?).

## Syntax

```
/bq-forge propose [<work-id>]          draft candidates from a closing work (default: the active work)
/bq-forge use <candidate> <work-id>    record one more evidenced use (link to the evidence entry)
/bq-forge status                       candidates, their uses (n/3), last use
/bq-forge promote <candidate>          after 3 uses and the user's yes: install into .claude/skills/, update the registries
```

## Steps (propose)

1. Read the work's evidence and log. List procedures that ran more than once or that ended a struggle (three failures then a fix that held).
2. For each, check the pack first: an existing skill that should gain a step is an **improvement** proposal (a diff), not a new skill. Duplicates are refused.
3. Draft the candidate in `.bequite/skills/forge/<name>/SKILL.md` to the v1 rubric (trigger-style description, numbered procedure, one worked example with the real values from this work, quality gate, boundaries) plus `forge.md`: `uses: 1/3`, the evidence link, the date, what would make it fail.
4. Show the user the candidate list; nothing else changes.

## Promotion rule

Three uses, each with an evidence link from a different work or a different day, and the user's yes. Promotion follows `CLAUDE.md` rule 6 for a new skill (registry, router, orchestration map, README, CHANGELOG in the same commit) and `bq_check.py` must stay green.

## Quality gate

Every candidate cites the evidence it came from; no candidate duplicates an existing skill; promotion never skips the three uses.

## Next Command Recommendations (typical)

`/bq-work close` after `propose` · `/bq-skill-audit` after `promote`.
