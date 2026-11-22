---
description: Explain a file / function / decision / concept in plain English. Useful for onboarding, vibe-handoff prep, understanding inherited code, or learning what BeQuite did during /bq-auto. Read-only.
---

# /bq-explain: plain-English explainer

Read-only: it writes no file and sets no gate. Needs only a target.

## Syntax

```
/bq-explain "<target>"
```

The target can be a file path, a function ("`computeMonthlyTotal` in `lib/billing.ts`"), a concept ("how auth works in this project"), a decision ("why Drizzle and not Prisma", "ADR-002"), a BeQuite artifact (a work's `plan.md` or `research.md`), or a run ("what /bq-auto changed last time").

Not for changing anything (`/bq-fix`, `/bq-feature`), for a whole-project assessment (`/bq-audit`), or for choosing the next command (`/bq-suggest`).

## Steps

1. **Parse the target** and find it: the file, the symbol (Grep), the decision (`.bequite/state/DECISIONS.md`, the ADRs), the run (`LAST_RUN.md`, `AGENT_LOG.md`, the work's `log.md`, `git log`).
2. **Read the target and its neighbours:** callers, callees, the tests that cover it, the decision that explains it. Read enough to be right, not the whole repo.
3. **Explain in four parts:**
   - **What it is:** one or two sentences a new person would understand.
   - **What it does:** the flow, step by step, with `file:line` where it helps.
   - **Why it matters:** what depends on it and what would break without it (not "it does X" again).
   - **Things to be careful of:** side effects, hidden coupling, known issues, what must not be changed casually.
   Then the related files worth reading next.
4. **Match the reader.** For a non-technical owner, drop the jargon or define it inline and use an analogy; for an engineer, keep the precise terms.
5. **Suggest** one or two follow-ups (another target, or a command if the explanation surfaced a concern).

## Rules

- Say "I could not determine this" for any part that is unclear; never bluff.
- Every claim about the code comes from reading it in this session.
- No banned weasel words about behaviour: read it, or say it is unverified.

## Next Command Recommendations (typical)

`/bq-explain "<another target>"` · `/bq-handoff` when preparing a handoff · `/bq-audit` when the explanation surfaced concerns.
