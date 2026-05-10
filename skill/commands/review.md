---
name: bequite.review
description: Phase 5 (or pre-merge) — senior code review. Loads the reviewer (= software-architect on review pass) + skeptic + security-reviewer. Walks the 13 review categories per prompts/review_prompt.md. Returns Approved / Approved-with-comments / Blocked.
phase: P5
persona: software-architect (reviewer) + skeptic + security-reviewer
prompt_pack: prompts/review_prompt.md
---

# /bequite.review

When invoked (or `bequite review`):

## Step 1 — Read the diff

Run `git diff <base>..<head>` (or PR diff). Read the task card from `specs/<feature>/phases/<phase>/tasks.md`. Read receipt at `.bequite/receipts/<sha>-P5-<task_id>.json` (v0.7.0+).

## Step 2 — Walk the 13 categories (master §7.6 — adapted)

For every change set:

1. **Requirements match** — diff implements the task card exactly; flag silent additions / omissions.
2. **Type safety** — strict typing throughout; no `any` / `# type: ignore` without recorded reason.
3. **Error handling** — every async has a handled failure mode; timeouts + retries with backoff + jitter; typed errors; logged with traceId.
4. **Security** — no secrets; input validation everywhere; deny-by-default authz; parameterised queries; CSP/HSTS/X-Frame; OWASP coverage.
5. **Accessibility** (frontend) — axe-core green; keyboard; focus states; labels; touch targets ≥44px; empty/loading/error states meaningful.
6. **Performance** — no N+1; no reads in loops; no synchronous blocking in request paths; indexes for new query patterns; bundle size ≤5% growth.
7. **UI quality** (frontend Doctrines) — tokens-only; no nested cards; no gray-on-color; no bounce/elastic; mobile + desktop tested; recorded design choice.
8. **Test coverage** — unit + integration + e2e + migration + negative cases.
9. **Migration safety** — reversible; no production lock for unacceptable duration; backfills batched + idempotent; rollback in task card.
10. **Secrets & config** — no `.env*` reads; new env vars in `.env.example` + `techContext.md`; rotation plan.
11. **Deployment risk** — feature-flagged when user-visible + risky; backwards-compatible; rollback path documented.
12. **Token waste** — no unnecessary skill loading; correct model tier; cost-per-task within budget.
13. **Over-engineering** — simplest thing tried first; no premature abstraction; no speculative generality.

## Step 3 — Skeptic kill-shot

Before approving, Skeptic produces one kill-shot. Implementer / reviewer answers concretely. Unanswerable kill-shots **block** approval.

## Step 4 — Security-reviewer pass

Cross-references OWASP LLM Top 10 (2025) + Web App Top 10. Specifically: prompt-injection paths (Article IV / master §19.5); supply-chain (master §19.6); regulated-data flow; auth/authz boundaries.

## Step 5 — Output

Verdict: **Approved** / **Approved-with-comments** / **Blocked**.

- For Blocked: numbered must-fix list with file:line + category + severity.
- For Approved-with-comments: nice-to-fix list, each becomes a new task in `state/task_index.json`.
- For Approved: one-line confirmation in receipt.

## Stop condition

- Verdict recorded.
- Skeptic kill-shot answered.
- Security-reviewer pass complete.
- `state/task_index.json` updated (and / or new tasks filed).
- Receipt updated with the review block.

## Anti-patterns

- Rewriting the implementer's code in the review (file a new task instead).
- Approving without running the tests yourself (read the receipt; rerun if doubtful).
- Weasel words in the review (Iron Law II).
- Bikeshedding blocking approval (style nits → comment, not block).
