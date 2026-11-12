# Work folders (v4)

Every piece of work gets its own folder. One folder per feature, fix, film, course, research question or release, holding its brief, research, spec, plan, tasks, gates, evidence and log. Nothing overwrites another piece of work, and finished work is archived, not deleted.

Borrowed on purpose: Spec Kit's per-feature folder (`specs/NNN-feature/`), OpenSpec's change folders with spec deltas + dated archive, and Spec Kit 1.4's *converge* check (compare the result to the spec, turn gaps into tasks). Adapted to BeQuite's gates, evidence rules and plan-first approval.

## Layout

```
.bequite/
  ACTIVE.md                 the active work id, title, type, phase (one short file)
  specs/                    living truth of the project; finished work merges its spec deltas here
  work/
    _template/              copied for every new work item (do not edit per work)
    0007-launch-film/
      README.md             work card: id · title · type · status · created · links
      brief.md              goal, audience, constraints, clarify Q&A, assumptions
      research.md           research for this work (links shared reports in .bequite/research/)
      spec.md               requirements + acceptance criteria + spec deltas (ADDED / MODIFIED / REMOVED)
      plan.md               plan, file-responsibility map, per-phase execution profile, decisions
      tasks.md              tasks: id · wave · deps · skills · model/effort/confidence · status
      gates.md              this work's gates (start fresh for every work item)
      evidence.md           command + exit code + key output for every check
      review.md             reviews, guard pass, converge results
      verify.md             final verification verdict
      log.md                chronological log of every command run on this work
      delegate/             (delegate mode) task pack for a cheaper model + review report
      assets/ outputs/      (media/web work) references, boards, frames, renders, exports
  archive/
    2026-11-12-0007-launch-film/   finished work, read-only
  state/ logs/ research/ design/ ...   project-wide memory only
```

Work types: `feature` · `fix` · `motion` · `web` · `research` · `course` · `presentation` · `release` · `other`. The type decides which extra gates apply (see `gates.md` in the template).

## Rules

1. **Resolve the work first.** Every action command reads `.bequite/ACTIVE.md` right after memory preflight (contract step 1).
   - The request belongs to the active work → write into that folder.
   - No active work, or the request is clearly a different piece of work → create the next folder (`/bq-work new "<title>"` semantics), switch `ACTIVE.md`, and say so in one line.
   - Unclear → ask one question, or in auto mode pick the likelier option and log the assumption in `brief.md`.
2. **Ids are 4 digits, never reused:** next id = highest existing id across `work/` and `archive/` + 1. Slug = short kebab-case of the title.
3. **Gates are per work.** Project gates (initialized, mode, discovery, doctor, design DNA, project audit, release) stay in `.bequite/state/WORKFLOW_GATES.md`. Everything from clarify to verify is in `work/<id>/gates.md`, so a second feature never inherits the first one's approvals.
4. **Write back to the work.** Each command appends one entry to `work/<id>/log.md` (plus the project-wide `LAST_RUN.md` / `AGENT_LOG.md`). Evidence goes to `evidence.md`, never only to chat.
5. **Shared research is reused, not copied.** Domain research that other work can reuse lives in `.bequite/research/<DOMAIN>_RESEARCH_REPORT.md`; `research.md` links to it and holds only the delta.
6. **Converge before closing.** `/bq-verify` (and `/bq-work close`) compare `spec.md` acceptance criteria and `tasks.md` against `evidence.md`. Every criterion without evidence becomes a new task; the work cannot close until converge is clean.
7. **Close = merge + archive.** On close, the spec deltas in `spec.md` merge into `.bequite/specs/<area>.md`, `README.md` gets the outcome, and the folder moves to `archive/<date>-<id>-<slug>/`. Archived work is read-only history.
8. **Several open items are fine.** `ACTIVE.md` points at one; `/bq-work list` shows all open ones; `/bq-work switch <id>` changes focus.

## Old flat files (before v4)

| Before | Now |
|---|---|
| `.bequite/plans/SCOPE.md`, `.bequite/plans/feature-<slug>.md`, `specs/<slug>/spec.md` | `work/<id>/spec.md` |
| `.bequite/audits/RESEARCH_REPORT.md` | `work/<id>/research.md` (+ reusable domain reports in `.bequite/research/`) |
| `.bequite/plans/IMPLEMENTATION_PLAN.md`, `FILE_RESPONSIBILITY_MAP.md` | `work/<id>/plan.md` |
| `.bequite/tasks/TASK_LIST.md`, `CURRENT_TASK.md`, `TASK_CONFIDENCE.md` | `work/<id>/tasks.md` |
| `.bequite/audits/VERIFY_REPORT.md` | `work/<id>/verify.md` |
| `.bequite/audits/REVIEW_REPORT.md`, `GUARD_PASS_REPORT.md` | `work/<id>/review.md` |
| `.bequite/logs/ERROR_LOG.md` | `work/<id>/log.md` (lessons still go to `MISTAKE_MEMORY.md`) |
| `.bequite/tasks/DELEGATE_*.md`, `audits/DELEGATE_REVIEW_REPORT.md` | `work/<id>/delegate/` |

Migration: when a command finds old flat files and no `work/` folder, it creates `work/0001-<inferred-title>/`, copies the old files into the new names, leaves the originals in place, and records the move in `log.md`.

## Spec Kit interop

`/bq-spec export=speckit` writes the active work's spec to `specs/NNN-<slug>/spec.md` (Spec Kit layout) for teams that also use Spec Kit. BeQuite itself always reads `work/<id>/`.
