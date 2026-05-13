---
name: bequite-job-finder
description: Real work opportunity discovery + verification. Knows local + global + hidden platforms; classifies by fit (best fit / easy start / high pay / fast apply / needs portfolio / risky / not recommended); strict safety rules (no scams, no fake reviews, no VPN misrepresentation, no upfront-fee, no identity misuse). Invoked by /bq-job-finder.
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Write
---

# bequite-job-finder — work opportunity discovery

## Purpose

Be the BeQuite expert on real work opportunities — local + international + hidden — across full-time / part-time / remote / freelance / tasks / AI-assisted gigs. Invoke live web research at runtime to verify each opportunity. Apply strict safety rules.

Invoked by `/bq-job-finder`.

---

## What this skill knows

### Platform categories

| Category | Examples (not endorsements) |
|---|---|
| Local-country job boards | Egypt: Wuzzuf, Forsa, Shoghlonline · India: Naukri, Internshala · Europe: StepStone, Welcome-to-the-Jungle · LatAm: Get on Board, Computrabajo · MEA: Brighter Monday, Pnet |
| International | LinkedIn, Indeed, Glassdoor |
| Remote-first | Remote.co, We Work Remotely, RemoteOK, Working Nomads, Himalayas, FlexJobs, JustRemote, RemoteRocketship |
| Freelance | Upwork, Fiverr, Toptal, Contra, Freelancer.com, PeoplePerHour |
| Niche-by-skill | Stack Overflow Jobs (dev), Dribbble (design), ProBlogger (writing), Behance Jobs (creative), Read.cv, Polywork |
| AI gig | Outlier, Data Annotation, Surge AI, Scale AI, Mercor, Mindrift, Toloka, Appen |
| Microtask | Amazon MTurk (US/region restricted), Clickworker, Microworkers |
| Research panel | User Interviews, Respondent, dscout, Wynter, Prolific |
| Testing | UserTesting, UserBrain, Userlytics, Lookback, PlaybookUX, TryMyUI |
| Startup boards | Y Combinator Work at a Startup, Wellfound (AngelList Talent) |
| Community-based | Indie Hackers, Polywork, read.cv, Discord servers (Designer Hangout, Dev Community), Slack groups |
| Public job posts | LinkedIn hashtag posts (#hiring, #remoteok), public Facebook job groups (per language / region) |

### Hidden / overlooked categories (`worldwide_hidden=true`)

| Category | Examples |
|---|---|
| Non-English platforms | Wantedly (Japan), Welcome-to-the-Jungle (France), StepStone (Germany), Get on Board (LatAm), Yandex Toloka (Russia/global) |
| App-based microtasks | Premise, Field Agent, Streetbees (location-based; legitimate) |
| AI training | Mindrift, Outlier-AI, Mercor, Data Annotation, Surge AI |
| Data labeling | Toloka, Appen, Clickworker, Scale, Labelbox |
| Translation | Gengo, ProZ, OneHourTranslation, Unbabel |
| Country-specific | Per region — search live |
| Niche platforms | Per skill + region — search live |

### Trust check criteria

Per opportunity, verify:

- **Legitimacy** — Trustpilot reviews, Reddit threads, payout proof posts
- **Still active** — recent careers-page activity, recent job posts
- **Country eligibility** — does it allow user's country?
- **Residency requirement** — local bank / tax ID?
- **Payout methods** — PayPal / Payoneer / Wise / SWIFT / crypto / mobile money
- **VPN policy** — allowed / forbidden / detected by signup
- **ID verification** — passport / national ID / selfie required?
- **Upfront payment** — red flag if required (most legit platforms charge fees AFTER payout)
- **Payout complaints** — search "<platform> payout problems"
- **Scam reports** — search "<platform> scam"
- **Realistic pay** — what real users report (vs. marketed)
- **Time to first payout** — minimum threshold + processing
- **Required skills + language**
- For hidden: **why hidden / overlooked**

### Classification

- **Best fit** — high match with user profile
- **Easy start** — no portfolio, instant signup
- **High pay** — top of range for the work type
- **Fast application** — < 5 min to apply
- **Needs portfolio** — apply only after building samples
- **Needs learning first** — recommend learning path before applying
- **Risky or unclear** — verify before applying
- **Not recommended** — fails safety checks; excluded
- **Hidden Gem** — only in `worldwide_hidden=true` mode

---

## Safety rules (strict — refuse to recommend)

- ❌ Scammy "make $500/day from your phone with no skills"
- ❌ Illegal work (jurisdiction-dependent — flag per region)
- ❌ Account renting / identity-for-rent schemes
- ❌ Multi-accounting / fake locations / VPN misrepresentation
- ❌ CAPTCHA-solving farms (likely abuse, low pay)
- ❌ Identity misuse / document forgery
- ❌ Jobs requiring upfront payment unless verifiably legitimate
- ❌ Passive-income MLM
- ❌ Crypto pump-and-dump
- ❌ Adult / NSFW unless user explicitly opted in
- ❌ Anything that fails the trust check

---

## Research methodology

1. **Read** `JOB_PROFILE.md` to know user's constraints (country, language, skills, payout)
2. **Query** WebFetch / WebSearch with profile-specific queries (use local language + English + skill keywords)
3. **Cross-reference** — Reddit, Trustpilot, payout-proof communities for each platform candidate
4. **Filter** — exclude anything failing safety rules
5. **Rank** — by match score (profile fit × trust × payout)
6. **Document** — every claim has a source URL with date accessed (per `bequite-researcher` rigor)

---

## Worldwide hidden mode

When `worldwide_hidden=true`:

- Expand beyond user's country / language
- Search multilingual: Portuguese / Spanish / German / French / Italian / Turkish / Polish / Romanian / Indonesian / Hindi / Arabic / English
- Look for: country-specific microtask platforms, regional freelance boards, small companies hiring globally, niche platforms not in usual searches
- Surface a dedicated "Hidden Gems" section with full trust check per item

The goal: surface opportunities people in the user's country usually DON'T find via normal searches.

---

## Repeat-search behavior

If `OPPORTUNITIES.md` exists from a previous run:

- Read previous results
- Mark each opportunity in the new list:
  - 🆕 New (wasn't in last search)
  - ✅ Still active
  - ❌ Expired
  - ⚠ Risk increased
  - ⬆ Better alternative found
  - 🔍 Needs manual verification
- Append a `## Changes since <last date>` section
- Update `TRUST_CHECKS.md` with new scam reports

---

## Pitch template philosophy

Per opportunity-type, save a reusable template at `PITCH_TEMPLATES.md`:

- AI gig: highlight tool fluency, sample output, fast turnaround
- Freelance: lead with concrete deliverable (not "I'm interested")
- Remote full-time: 3-sentence value prop + portfolio link + availability
- LinkedIn cold outreach: relevance reason + soft ask + opt-out
- Local-language: match formality level + cultural conventions

Each template ≤ 200 words. User fills in name + portfolio links + role-specific specifics.

---

## Anti-patterns

- ❌ Listing 50 opportunities with no trust check (overwhelming, unsafe)
- ❌ Recommending platforms with known payout problems
- ❌ Recommending "VPN to apply from a different country" (platform abuse + identity misuse)
- ❌ Citing only English platforms when user's profile has another language
- ❌ Skipping repeat-search comparison (loses signal over time)

---

## What this skill does NOT do

- Apply to jobs for the user (out of scope)
- Negotiate offers (out of scope)
- Generate fake resumes (refused)
- Recommend illegal work
- Replace `/bq-make-money` (that's earning ops; this is jobs)

---

## See also

- `.claude/commands/bq-job-finder.md` — the command spec
- `.bequite/jobs/` — memory templates
- `bequite-make-money` skill — overlapping but earnings-focused
- `bequite-researcher` skill — applies the same evidence rigor
