---
description: 'Write a one-page product or feature spec into the active work (.bequite/work/<id>/spec.md) in a Spec Kit-compatible shape. Optional export=speckit also writes specs/NNN-<slug>/spec.md for teams that use Spec Kit.'
---

# /bq-spec: one page that says what done means

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Part of stage 5 of `PIPELINE.md`. The spec describes the user-visible change; the plan (`/bq-plan`) says how to build it. `/bq-scope` owns the "In scope / Out of scope / Non-goals" section of the same file; this command writes the rest and never overwrites that section. Skills: `bequite-product-strategist`, `bequite-ux-ui-designer` when there is a screen.

## Syntax

```
/bq-spec "<feature or product idea in one sentence>" [export=speckit]
```

No argument: ask for the one sentence. Not for a bug (`/bq-fix`) or a change small enough to describe in a commit message.

## Gates

Needs `BEQUITE_INITIALIZED` (`MODE_SELECTED` recommended). Sets `FEATURE_SPEC_APPROVED` when the user confirms the spec.

## Steps

1. **Read** `work/<id>/brief.md` and `research.md` if they exist, `.bequite/state/DECISIONS.md`, `OPEN_QUESTIONS.md`.
2. **Detect Spec Kit:** a `specs/` or `.specify/` folder at the root. If present, follow its path and naming for the export; if not, offer `export=speckit` only when asked.
3. **Write `work/<id>/spec.md`** with these sections, in plain language and with no stack names:
   - **What** (two or three sentences) and **Why** (the value to the user and the business).
   - **Who:** the primary user as a concrete role, secondary users, stakeholders.
   - **What changes for the user:** before and after, as the user's steps.
   - **Acceptance criteria:** concrete and testable, each one an observable behaviour. These are what `/bq-verify` converges against.
   - **Out of scope** (at least one item), **Constraints** (time, budget, platforms, compliance), **Open questions** (real ones, not "TBD"), **Success metric**, **How** in two or three high-level sentences, **Related** (plan, decisions).
4. **Export** the same content to `specs/NNN-<slug>/spec.md` when `export=speckit` is set, and note the path in the work log. The work spec stays the source of truth.
5. **Confirm with the user**, then append unresolved questions to `OPEN_QUESTIONS.md` and the decision to `DECISIONS.md`.

## Output

```
Spec: .bequite/work/<id>/spec.md  (export: specs/NNN-<slug>/spec.md)
Acceptance criteria: <n>   Open questions: <n>   Status: draft | confirmed
Next: /bq-plan
```

## Quality gate

What, Why, Who and the acceptance criteria are concrete (no weasel words); out of scope is explicit; open questions are real; the user confirmed it.

## Next Command Recommendations (typical)

`/bq-plan` · `/bq-feature "<name>"` when the spec is small · `/bq-clarify` for the open questions.
