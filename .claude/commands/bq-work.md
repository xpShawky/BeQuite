---
description: 'Manage work folders (W0.8). Every feature, fix, film, course or research question gets its own .bequite/work/NNNN-slug/ folder with brief, research, spec, plan, tasks, gates, evidence and log. Subcommands: new, list, switch, status, close (converge + merge specs + archive).'
---

# /bq-work - one folder per piece of work (W0.8)

<!-- bq:contract -->
> **Every run follows the contract** (`.claude/bequite/docs/architecture/COMMAND_EXECUTION_CONTRACT.md`):
> 1. **Skills first:** announce the `Skill Selection:` block before any plan, edit or tool call for the task.
> 2. **Resolve the work:** read `.bequite/ACTIVE.md`; use `.bequite/work/<id>/`, or create the next work folder if this is new work (`/bq-work`).
> 3. **Gates:** project gates in `.bequite/state/WORKFLOW_GATES.md`, work gates in `work/<id>/gates.md`. Refuse and name the missing gate.
> 4. **Plan first:** non-trivial work gets a plan the user approves before output. Hard human gates always wait for a yes.
> 5. **Evidence:** every check goes to `work/<id>/evidence.md` (command + exit code + output) or is marked `UNVERIFIED:`.
> 6. **Write back:** `work/<id>/log.md`, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, and `.bequite/state/MISTAKE_MEMORY.md` when a lesson surfaced.
> 7. **Finish** with the Next Command Recommendations block.
<!-- /bq:contract -->

Spec: `.claude/bequite/docs/architecture/WORK_FOLDERS.md`. Most commands create work automatically; use this command to see, switch or close work by hand.

## Syntax

```
/bq-work new "<title>" [type=feature|fix|motion|web|research|course|presentation|release|other]
/bq-work list                 open work items (id, title, type, phase, gates done/total)
/bq-work switch <id>          make another open item the active one
/bq-work status [<id>]        one screen: brief, phase, gates, open tasks, last log entries
/bq-work close [<id>]         converge -> merge spec deltas -> archive
```

## Skills first

Announce the `Skill Selection:` block before acting. Usually: `bequite-context-engineer` (folder hygiene, state) · `bequite-orchestrator` (deciding whether a request is new work) · `bequite-guard-pass` (close/converge).

## new

1. Read `.bequite/ACTIVE.md`, list `work/` and `archive/`. Next id = highest existing 4-digit id + 1 (never reuse).
2. Slug = short kebab-case of the title (max 5 words). Folder = `.bequite/work/<id>-<slug>/`.
3. Copy `.bequite/work/_template/` into it. Fill `README.md` (`{{ID}}`, `{{TITLE}}`, `{{TYPE}}`, `{{DATE}}`, `{{REQUEST}}`). In `gates.md`, switch the gate groups for this type from `n/a` to `pending` (fix, feature, web, motion).
4. Write `.bequite/ACTIVE.md` (id, title, type, phase = framing, folder).
5. First entry in `log.md`; one line in `.bequite/logs/AGENT_LOG.md`.
6. Say in one line: `Started work <id> - <title> (<type>) at .bequite/work/<id>-<slug>/`.

## list / status

Read only. `list`: a table of open items with id, title, type, phase, gates done/total, last activity; mark the active one. `status`: README + brief summary + gates table + open tasks + last 5 `log.md` entries + next recommended command.

## switch

Refuse unknown or archived ids. Update `ACTIVE.md`; log the switch in both work logs.

## close

1. **Converge:** for every acceptance criterion in `spec.md` and every task in `tasks.md`, find evidence in `evidence.md` / `verify.md`. Missing evidence becomes new tasks in `tasks.md` and the close stops with the list.
2. Require `VERIFY_PASSED` and `CONVERGED` in `gates.md` (or an explicit user override recorded in `README.md`).
3. **Merge specs:** apply the ADDED / MODIFIED / REMOVED deltas from `spec.md` to `.bequite/specs/<area>.md` (create the area file if needed).
4. Fill `README.md` -> Outcome. Move the folder to `.bequite/archive/<YYYY-MM-DD>-<id>-<slug>/`. Clear `ACTIVE.md` (or point it at another open item if the user names one).
5. Append to `.bequite/logs/AGENT_LOG.md` and `.bequite/state/LAST_RUN.md`; add a lesson to `.bequite/state/MISTAKE_MEMORY.md` if the work taught one.

## Migration from flat files (pre-v4 projects)

If `work/` does not exist but old flat files do (`.bequite/plans/SCOPE.md`, `IMPLEMENTATION_PLAN.md`, `.bequite/tasks/TASK_LIST.md`, `.bequite/audits/VERIFY_REPORT.md` ...), `new` first creates `work/0001-<inferred-title>/`, copies the old files into the new names (table in the spec), leaves the originals untouched, and logs it.

## Write back

`work/<id>/log.md` · `.bequite/ACTIVE.md` · `.bequite/logs/AGENT_LOG.md` · `.bequite/state/LAST_RUN.md` · `MISTAKE_MEMORY.md` when a lesson surfaced.

## Next Command Recommendations

After `new`: `/bq-clarify` (or `/bq-motion` / `/bq-feature` / `/bq-fix` for their types). After `close`: `/bq-release` if a release is due, otherwise `/bequite`.
