---
name: bequite-product-strategist
description: Use before planning or scoping a product or feature (/bq-clarify, /bq-scope, /bq-plan, /bq-audit of an existing product), and whenever the user says "build a platform", "everyone needs this", "users will love it", or asks what to charge. Forces the job, the user, the alternative, the differentiation, the success number and the price to be stated before code, and names the cheapest test for the biggest risk.
last_verified: 2026-11-21
sources:
  - https://www.svpg.com/four-big-risks/
  - https://hbr.org/2016/09/know-your-customers-jobs-to-be-done
  - https://stripe.com/guides/atlas/saas-pricing
  - https://amplitude.com/books/north-star
  - https://www.momtestbook.com/
  - https://pmfsurvey.com/
---

# bequite-product-strategist

The most expensive bug is building the wrong thing. This skill makes the product case explicit and testable before `/bq-plan` locks anything.

## When to use

- `/bq-clarify` (generate the questions), `/bq-scope` (cut), `/bq-plan` (confirm the case), `/bq-audit` (product signals), `/bq-handoff` ("what this product is").
- Any pricing question.

Not for: marketing copy (the human-taste skill and the writing DNA); financial models or legal opinions (say so).

## The six answers (write them in `work/<id>/spec.md`)

1. **Job.** "When <situation>, I want to <motivation>, so I can <outcome>." (Jobs to be done, Christensen et al., HBR 2016.) "We need a CRM" is not a job.
2. **User.** Role, context, tools they already use, and one real person who fits. A persona with no person behind it is a guess.
3. **Today's alternative.** Workaround, competitor, or nothing. "Nothing" usually means the pain is not strong enough.
4. **Why us.** A capability they lack, a measured 10x (time or cost), a niche, or a language or region fit (Arabic-first counts when it is real). Not "better UX", "modern stack" or "AI-powered".
5. **Success number.** One metric that shows value to the user and to the business, with its input metrics (North Star idea), a baseline and a target the user picks. No borrowed thresholds.
6. **Price.** A first price and why (below).

## The four risks and the cheapest test (Cagan, SVPG 2017)

| Risk | Question | Cheapest test |
|---|---|---|
| Value (usually the hardest) | Will they buy or choose to use it? | Five conversations about past behaviour, not opinions (The Mom Test); a pre-sale or a waitlist with a price on it |
| Usability | Can they figure it out? | A clickable prototype with three users, watched, no help |
| Feasibility | Can we build it with our time, skills and tools? | A one-day spike on the riskiest part |
| Business viability | Does it work for the business (cost to acquire, payout, legal, support load)? | A one-page unit-economics sketch; check the payment and payout path in the seller's country |

Write the riskiest one first in `spec.md` and run its test before the plan is approved.

## Scope cuts

For each feature: does removing it kill the job? Can the user live without it for a week? If yes, it waits. Usual cuts for a first version: admin panel, bulk import and export, public API, multi-tenancy, roles beyond "owner", notifications that are not the job. Never cut: the path from sign-up to first value, payment if selling, basic error and empty states.

Mid-build "while we are at it": if it does not serve the job, or delays the first version by more than a week, it goes to the backlog; a change to `spec.md` comes first, or it is scope creep.

## Pricing (Stripe Atlas guide, read 2026-11-21)

- Price is the easiest lever; review it every quarter.
- About three plans plus "talk to us"; name plans by who they are for, not Lite, Standard, Premium.
- Charge by a proxy of the value delivered (seats, bookings, documents), anchored to the cost of what it replaces (an hour of an expert, an agency retainer).
- No flat "unlimited" plan; no .99 endings for business buyers.
- Check three to five competitors' live pricing pages before setting a number.

## Worked example (BeQuite itself, 2026-11-21)

- Job: "When I hand a coding agent real work, I want it to follow a plan, prove each step and remember my corrections, so I can trust the result without re-checking everything."
- User: the owner, a solo builder in Egypt using one Claude subscription and Adobe tools.
- Alternative: raw sessions plus personal notes; other skill packs that ship untested prose.
- Why us: evidence gates enforced by hooks, measured-reference creative work, Arabic-first.
- Success number: share of work items closed with every evidence entry present (baseline: work 0001; target set by the owner).
- Riskiest: value. Test: three outside builders run one real task with it and say whether they would keep it.

## Quality gate

- All six answers are in `spec.md`, each specific enough to be wrong.
- The riskiest risk has a test with a date.
- Any number borrowed from elsewhere has its source, or is the user's own target.

## Boundaries

Push back, then let the user decide; log the decision. Price advice is a starting point, not financial advice.
