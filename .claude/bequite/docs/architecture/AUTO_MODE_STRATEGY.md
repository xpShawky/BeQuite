# Auto mode strategy

How `/bq-auto` behaves. The intents, modes and phase table are in the command itself (`.claude/commands/bq-auto.md`); the stages are in `PIPELINE.md`. This file holds the rules behind them.

## The principle

Minimum interruption, maximum discipline, scoped to the task. Auto mode runs the pipeline for one intent and keeps going until the work is verified and written back. It does not restart the project lifecycle for a one-section fix, and it does not skip a stage to look fast.

## Continue by default

| After a step | Auto mode |
|---|---|
| it succeeded and no hard gate is next | continues without asking |
| a hard human gate is next | pauses, says which gate, why, what the user must do, and the line that resumes |
| a recoverable failure (a red test, a lint error) | one `/bq-fix` attempt, then retries the step |
| three failures in a row on the same task | pauses and reports what was tried |
| the intent is ambiguous | asks one question, then continues |
| a completion claim would need a banned word | replaces it with the evidence, or marks it `UNVERIFIED:` |

It never asks "should I continue?", "do you approve the plan?" (for safe, scoped, non-creative work) or "want tests?".

## Plan-first exceptions

Creative work is plan-first even in auto mode: films, content, UI variants, presentations, brand work and new products run references, research and options, then stop at the plan. A film stops three times before any build: script, style, and the tool and render plan with prices.

## Hard human gates

Auto mode pauses for an explicit yes before each of these, in every mode:

1. Destructive deletion (tracked code, directories, user data).
2. A migration against a shared or production database.
3. A change on a production server.
4. A VPS, Nginx or SSL change.
5. Activating a paid service or spending paid credits.
6. Handling a secret or key (creating, rotating, moving).
7. Changing the auth or security model.
8. Changing the project's architecture.
9. Deleting an implementation that still has callers.
10. A task that contradicts the locked scope.
11. Anything, when the user asked for manual approval (`--manual-approval`).
12. The cost ceiling (default $20 per session, or the work's `/bq-budget`).
13. The wall-clock ceiling (default 6 hours).
14. A banned word in a completion claim that cannot be replaced by evidence.
15. Three consecutive failures on one task.
16. Picking the winning UI or presentation variant.
17. A release push or tag (always run by the user).
18. For creative work: the script, the style, the render plan, picture lock, the final render and delivery.
19. Anything that leaves the machine in the user's name: a post, a message, an upload, an account, accepted terms.

A mode changes depth, speed and cost. No mode removes a gate.

## Verify before "done"

Every gate the intent needs is set; the tests for the changed surface pass; frontend work covers every in-scope section, the phone layout and the empty, loading and error states (not only a hero), with passing continuity and visual QA reports; creative work passed the human test; the report carries the command, the exit code and the decisive output.

## Resume after a pause

The pause message gives the exact line that resumes (`/bq-auto <same arguments>`). State is in the work folder (`log.md`, `gates.md`, `tasks.md`), so a new session resumes from the last completed step, not from the start.

## What auto mode refuses

- Skipping tests, verification or the write-back to finish sooner.
- Widening the scope ("while I am here") beyond the intent.
- Polishing only the visible first screen of a page.
- Installing a dependency or tool without the ten decision questions.
- Reporting PASS for a check it did not run.

## What it is not

Not a way around approvals, not a background daemon, and not a replacement for the user's judgement on taste, money or anything public.
