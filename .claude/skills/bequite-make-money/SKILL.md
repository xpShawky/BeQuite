---
name: bequite-make-money
description: Use when someone asks how to earn money from their skills, time, AI tools or audience, in their country, through /bq-make-money or in plain words ("how can I make money from X", "which platform pays in Egypt"). Finds legitimate routes, checks each one on the platform's own pages for that country (eligibility, payout method, fees, minimums), and turns the best two or three into a seven-day plan. Refuses scams and terms violations.
last_verified: 2026-11-21
sources:
  - https://support.upwork.com/hc/en-us/articles/211062538-Learn-about-the-Freelancer-Service-Fee
  - https://help.fiverr.com/hc/en-us/articles/360010530058-Withdrawing-your-earnings-managing-payout-methods
  - https://support.mostaql.com/how-to-withdraw-profits
  - https://support.khamsat.com/withdraw-profits
  - https://support.google.com/youtube/answer/7101720
  - https://support.google.com/youtube/answer/72851
  - https://www.paypal.com/eg/digital-wallet/paypal-consumer-fees
  - https://core.telegram.org/api/revenue
  - https://gumroad.com/pricing
  - https://consumer.ftc.gov/articles/job-scams
---

# bequite-make-money

Legitimate income routes, checked for the user's country on the platform's own pages today. A route that cannot pay the user out is not a route.

## When to use

- `/bq-make-money`, and any "how do I earn from ..." request.
- Before recommending any platform, programme or marketplace to a user in a specific country.

Not for: jobs with an employer (`bequite-job-finder`); packaging one offer (`/bq-offer`); turning finished work into a product (`/bq-productize`, proposed for v1); tax or legal advice (say so and suggest an accountant).

## Inputs (from `.bequite/money/MONEY_PROFILE.md`, else ask once)

Country of residence · languages · skills and tools (including AI tools they already pay for) · hours per week · devices · payout methods they already have (bank, PayPal, Payoneer, wallet) · risk tolerance · track. Tracks: `highest-payout`, `easiest-start`, `fastest-first-payout`, `long-term-stable`, `ai-assisted`, `no-calls`, `remote-global`, `local-only`, `beginner`, `skilled`.

## Procedure

1. **Shortlist by track** from the families in `references/route-families.md` (freelance marketplaces, Arab freelance platforms, creator programmes, digital products, AI training and data work, research and testing panels, local services). Pick 6 to 10 candidates, not 50.
2. **Verify each candidate for this country** (`bequite-researcher` ladder; open help pages in the browser when they refuse scripts). Record in `TRUST_CHECKS.md`, one row per platform:
   - accepts residents of the country (eligibility list, not a forum);
   - payout path that ends in money the user can use (method, minimum, fee, days);
   - the platform's fee or commission;
   - ID and tax documents required; VPN or location rules;
   - scam and payout complaints (search "<platform> payout problem", read the dates);
   - realistic first payout date.
   Every cell carries the URL and date read, or `UNVERIFIED:`.
3. **Exclude** anything that fails a safety rule (below) or has no verified payout path for the country. Log the reason.
4. **Rank** the rest for the track: time to first payout, pay range reported by the platform itself, fit with skills, risk. Hidden gems (`worldwide_hidden=true`): search in the user's languages plus regional boards; each gem gets the same full check and a line on why it is overlooked.
5. **Write** `OPPORTUNITIES.md` (ranked, each with its check row), and `ACTION_PLAN.md`: at most three sign-ups on days 1 and 2, a concrete deliverable per day ("publish one gig with three portfolio samples", not "work on profile"), a first-payout target by day 7, and the acceptance test for each day.
6. **Repeat runs:** compare with the previous `OPPORTUNITIES.md`; mark new, still active, expired, risk increased, better alternative, needs manual check; append "Changes since <date>".

## Safety rules (refuse, and say why)

No fraud, fake accounts, fake reviews or bought engagement · no CAPTCHA farms or bypassing · no VPN or false location to pass eligibility · no account renting or someone else's identity · no upfront fee to get work (the FTC's first scam sign) · no MLM, pump-and-dump or "guaranteed income" · no mass unsolicited outreach · no adult content unless the user opted in · no income promise: give the platform's own figures and say they are not a guarantee.

## Worked example (verified 2026-11-21, user in Egypt, track `fastest-first-payout`, skills: Arabic writing + AI tools)

| Route | Verified for Egypt | Payout | Verdict |
|---|---|---|---|
| Khamsat (Arabic micro-services) | Bank withdrawal lists Egypt | Bank from $250, up to 14 working days, Khamsat pays the fee; PayPal from $25 within 48 h; 14-working-day hold | Rank 1 for Arabic services |
| Mostaql (Arabic projects) | Bank withdrawal lists Egypt | Same thresholds; commission 15% or 20% by membership | Rank 2 |
| Fiverr | Payout via PayPal, or bank via Payoneer | PayPal $1 min, Payoneer bank $1 fee, $20 min | Rank 3; PayPal withdrawal from Egypt is `UNVERIFIED:` (the Egypt fee page says bank withdrawal "may not be possible in all markets") |
| YouTube Partner Program | Egypt in the availability list | 1,000 subs + 4,000 watch hours (12 months) or 10M Shorts views (90 days) | Long-term track, not week one |
| TikTok Creator Rewards | Not in any list found; official page did not load | - | `UNVERIFIED:` check TikTok Studio in the app |
| Lemon Squeezy | Egypt in payout list | - | Excluded: closed to new sign-ups, shuts down 31 March 2027 |

Day 1 to 2: Khamsat profile and three services with real samples. Day 3: Mostaql profile and five proposals. Day 7 target: first delivered order (the 14-day hold means cash arrives after the week; the plan says so).

## Quality gate

- Each recommended route has a verified payout path for the user's country, with URL and date.
- No pay figure without the platform's own source; others are `UNVERIFIED:`.
- At most three sign-ups in the plan; each day has a deliverable and a test.
- Excluded routes are listed with the reason.

## Boundaries

BeQuite does not sign up, apply, accept terms or move money for the user. Platform names are candidates, not endorsements. Country facts age fast: re-check anything older than 30 days before advising.
