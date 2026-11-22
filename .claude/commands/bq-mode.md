---
description: Select or show the workflow mode (New Project, Existing Project Audit, Add Feature, Fix Problem, Research Only, Release Readiness). The mode decides which gates apply and what the menu recommends. `new` and `existing` also set the project up for that route.
---

# /bq-mode: say what kind of work this is

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

The mode is the workflow (which gates apply). It is separate from the operating modes of `/bq-auto` (`fast`, `deep`, `token-saver`, `delegate`), which set depth and cost.

## Syntax

```
/bq-mode                     show the current mode, or ask which one
/bq-mode new                 New Project: an empty or near-empty folder
/bq-mode existing            Existing Project Audit: a repo that already has code
/bq-mode feature | fix | research | release
```

A sentence works too ("something is broken in checkout"): one question if it is ambiguous.

## Gates

Needs `BEQUITE_INITIALIZED` (run `/bq-init` first). Sets `MODE_SELECTED`.

## Steps

1. **Read** `.bequite/state/CURRENT_MODE.md`, `PROJECT_STATE.md`, `WORKFLOW_GATES.md`. If a mode is already set and no argument was given, show it and ask whether to change it. Changing mode mid-work is allowed; say which artifacts may no longer apply, and log the change.
2. **Offer the six modes** when none was named:

   | Mode | For | Next |
   |---|---|---|
   | New Project | starting from scratch | `/bq-clarify`, or `/bq-auto new "<idea>"` |
   | Existing Project Audit | understanding or improving a repo | `/bq-discover`, `/bq-doctor`, `/bq-audit` |
   | Add Feature | one feature in an existing repo | `/bq-feature "<title>"` |
   | Fix Problem | something is broken | `/bq-fix "<symptom>"` |
   | Research Only | facts before any plan | `/bq-discover`, then `/bq-research` |
   | Release Readiness | built; verify and ship | `/bq-verify` |

3. **Check the folder against the choice.** New Project in a folder with a manifest and source: say it does not look empty and ask whether Existing was meant. Existing in an empty folder: the reverse.
4. **Set the project up for `new` and `existing`:**
   - `PROJECT_STATE.md`: the project type; the stack as "not decided (pending research and plan)" for new, "to be detected by `/bq-discover`" for existing.
   - `CURRENT_PHASE.md`: P0.
   - `OPEN_QUESTIONS.md`, three questions with recommended defaults. New: what is this project in one sentence; who is the primary user; what scale is expected. Existing: what is the goal (understand, fix, improve, add); is it in production; who owns the repo.
5. **Write** the mode with a one-line reason to `CURRENT_MODE.md`, set `MODE_SELECTED` in `WORKFLOW_GATES.md` with the gates this mode skips (table in `.claude/bequite/docs/architecture/WORKFLOW_GATES.md`), and append the decision to `DECISIONS.md`.

## Output

```
Mode: <name>   (<why>)
Folder: <empty | existing code: <stack if known>>   Phase: P0
Queued questions: <n>
Next: <the mode's first command>, or /bq-auto phase=P0
```

## Quality gate

`CURRENT_MODE.md` holds exactly one of the six modes; the gate is set; for `new` and `existing` the project state and the three questions are written.

## Next Command Recommendations (typical)

The mode's "Next" column. `/bq-auto phase=P0` walks the rest of setup in one pass.
