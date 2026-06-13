---
description: Starting Path Advisor (C17). Help a user choose HOW to start — personal profile vs new page/account, personal name vs brand, which platforms, one niche vs content pillars, content/course/offer sequence, or career/freelance positioning. Neutral and practical — gives a concrete recommendation with tradeoffs, a 7-day start plan and 30-day experiment, not generic motivational advice. Uses the user's actual assets; does not just agree.
---

# /bq-start — choose the best starting path (C17)

Full spec: `docs/specs/STARTING_PATH_ADVISOR.md`. Follows the 12-step contract. Skills: product-strategist + make-money + job-finder (career) + writing-dna (tone) + researcher (platform behavior) + localization-rtl (MENA). The "I don't know how to start / which path" command — most people fail at starting, not building.

## Syntax

```
/bq-start "<what you want to start + your current assets>"
```
Examples: "start content but I have a personal FB with 1000 friends/family — profile or new page?" · "YouTube under my name or a brand name?" · "make courses — free content first or paid course directly?" · "work at a company or freelance — what do I optimize first?" · "I want to talk about AI + automation + pharmacy — mix or separate?"

## Steps (after contract steps 1–7)

1. **Context** — `START_CONTEXT.md`: goal, current assets (followers, accounts, skills, proof), constraints, fears (judgment/unfollow/privacy). Use the user's ACTUAL assets — never ignore them.
2. **Options + analysis** — `OPTION_MAP.md` · `AUDIENCE_AND_PLATFORM_ANALYSIS.md` (existing reach vs relevance — warm-but-unqualified followers are signal-testers, not the final audience) · `ACCOUNT_STRATEGY.md` (personal profile vs page vs new account, with roles) · `PERSONAL_BRAND_VS_BRAND_DECISION.md` (is the user the product? should it survive beyond them?).
3. **Positioning** — `CONTENT_POSITIONING.md` (one niche / umbrella + pillars / separate accounts / phased — using audience-overlap + monetization + confusion-risk, NOT a blind narrow niche) · `PLATFORM_PROFILE_SETUP.md` (per relevant platform: best use, setup, format, risks, first action).
4. **Plan** — `FIRST_30_DAYS_PLAN.md` (7-day start + 30-day experiment) · `EXPERIMENT_PLAN.md` (what to measure — saves/DMs/comments, not just likes; when to pivot) · `RISKS_AND_TRADEOFFS.md`.
5. **Decide** — `FINAL_RECOMMENDATION.md`: recommended option · why · what NOT to do · profile setup checklist · content pillars · first 10 post/video ideas · metrics to watch · pivot trigger · `NEXT_STEPS.md`.

## Concrete-not-generic rule

Output concrete decisions ("use personal profile for 2 weeks of low-frequency validation, then create a page if signal appears"; "one umbrella brand if topics share an audience, split only on clear intent difference"; "LinkedIn for credibility + X for build-in-public + YouTube for durable education"), NOT "be consistent / post value / know your audience." Be neutral — disagree with the user when the evidence says so. Always end with a recommendation + next action.

## Hard rules

Don't push many accounts without a clear reason · don't force personal-brand if brand-led is safer (or vice-versa) · don't pretend platform strategy is universal · don't ignore the user's assets / audience mismatch / privacy pressure · no theory-only output.

## Writes

`.bequite/start/{START_CONTEXT,OPTION_MAP,AUDIENCE_AND_PLATFORM_ANALYSIS,ACCOUNT_STRATEGY,CONTENT_POSITIONING,PERSONAL_BRAND_VS_BRAND_DECISION,PLATFORM_PROFILE_SETUP,FIRST_30_DAYS_PLAN,EXPERIMENT_PLAN,RISKS_AND_TRADEOFFS,FINAL_RECOMMENDATION,NEXT_STEPS}.md` (first run) + AGENT_LOG + LAST_RUN.

## Next Command Recommendations (typical, route by chosen direction)

- Content/brand → **C14 `/bq-brand-kit`** (identity) + C2 `/bq-writing-dna` (tone).
- Course → **C5 `/bq-course`** (+ C15 `/bq-community`).
- Service/business → **C11 `/bq-offer`** (+ C6 `/bq-pain-radar`).
- Career/freelance → **C9 `/bq-job-finder`** + C8 `/bq-proposal` (+ C10 `/bq-make-money`).
Do not run yet: building anything before the account/positioning decision is made — starting wrong is the failure this command prevents.
