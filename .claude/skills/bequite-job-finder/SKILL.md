---
name: bequite-job-finder
description: Use when someone is looking for a job, contract, freelance client or remote role, through /bq-job-finder or in plain words ("find me remote work as X", "jobs in Egypt for Y"). Searches local, regional, remote and freelance sources in the user's languages, checks every listing for scam signs and country fit, classifies by fit, and writes short pitches. Never applies for the user.
last_verified: 2026-11-21
sources:
  - https://consumer.ftc.gov/articles/job-scams
  - https://wuzzuf.net/
  - https://remoteok.com/
  - https://support.upwork.com/hc/en-us/articles/211062538-Learn-about-the-Freelancer-Service-Fee
  - https://support.mostaql.com/how-to-withdraw-profits
  - https://support.khamsat.com/withdraw-profits
  - https://help.fiverr.com/hc/en-us/articles/360010530058-Withdrawing-your-earnings-managing-payout-methods
---

# bequite-job-finder

Real openings the user can actually take from where they live, each checked before it is shown.

## When to use

- `/bq-job-finder`, and any request to find work, clients or roles.

Not for: earning routes without an employer or client (`bequite-make-money`); writing a CV from nothing (the user's facts only; never invent experience).

## Inputs (from `.bequite/jobs/JOB_PROFILE.md`, else ask once)

Country and city · languages and level · role and seniority · skills with one proof each (link, repo, portfolio) · full-time, part-time, contract or freelance · remote, hybrid or on-site · minimum pay and currency · payout methods available · time zone limits.

## Where to look (verify each live)

| Kind | Start with | Note |
|---|---|---|
| Local and regional boards | Wuzzuf (Egypt-focused; 5,073 open jobs on 2026-11-21, also lists Riyadh, Dubai, Amman) and the country's own boards | Search in Arabic and English |
| Professional network | LinkedIn job search and posts with "hiring" in the user's languages | Read in the user's own browser only with their OK; never message or apply |
| Remote boards | Remote OK (region filter has Worldwide, Middle East, Africa), We Work Remotely, Himalayas, Working Nomads | "Remote" often means "remote within one country": check the location line |
| Freelance marketplaces | Upwork (fee 0-15% per contract), Fiverr, Mostaql, Khamsat | Payout path for the country first (`bequite-make-money` table) |
| Startup boards | Wellfound, YC Work at a Startup | Visa and contractor rules |
| Niche boards by skill | Design, writing, data, dev communities | Find live; many niche boards close |

`worldwide_hidden=true`: also search regional boards and non-English sites in the user's languages; each hidden gem gets the full check and a line on why it is overlooked.

## Procedure

1. Build search strings from the profile in each language (role synonyms, seniority, "remote" variants).
2. Collect 15 to 30 raw listings; keep URL, company, date posted, location rule, pay if stated.
3. **Check each** and write the result in `TRUST_CHECKS.md`:
   - the company exists outside the post (site, registry, people who work there);
   - the post is on the company's own careers page or a reputable board;
   - no fee to apply, train or be "placed"; no cheque to deposit and forward; no reshipping (FTC signs);
   - the location rule admits the user's country; contractor vs employee; how they pay;
   - posted in the last 30 days.
4. **Classify:** best fit · easy start · high pay · fast apply (under 5 minutes) · needs portfolio first · needs learning first · risky or unclear · not recommended (failed a check; say which) · hidden gem.
5. Write `OPPORTUNITIES.md` (top 10 to 15 with their check rows) and `PITCH_TEMPLATES.md` (one per opening type, under 200 words, built from the user's real proof: deliverable first, then the proof link, then availability).
6. Repeat runs: mark new, still open, expired, risk increased, better alternative, and append "Changes since <date>".

## Worked example (2026-11-21)

Profile: Cairo, Arabic and English, AI automation and n8n, wants remote contract work paid in USD.

- Wuzzuf "automation" search, in Arabic and English: local openings with Cairo or Giza locations; classified by fit.
- Remote OK, region Worldwide or Middle East: listings with "US only" location lines moved to "not recommended: location".
- LinkedIn posts (past month, read only): Egyptian specialists already work remotely for Saudi and Gulf agencies; demand is for bilingual Arabic and English AI work. Several "recognition" posts end with a WhatsApp number to buy a feature: classified as a red flag, not an opportunity.
- Freelance fallback: Mostaql and Khamsat pay out to Egyptian banks (from $250) or PayPal (from $25).

## Quality gate

- Every listing shown has URL, date posted, location rule and its check row.
- Nothing that asks the candidate for money is shown except as a warning.
- Pitches use only the user's real facts and links.
- Listings are in the user's languages, not English only.

## Boundaries

BeQuite does not apply, message recruiters, accept terms or fill forms. No fake CVs, no false location or VPN to meet a requirement, no illegal work. Board names are starting points, not endorsements.
