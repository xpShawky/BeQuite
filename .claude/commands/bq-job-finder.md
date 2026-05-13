---
description: Find real work opportunities — full-time / part-time / remote / freelance / tasks / AI-assisted gigs — based on country, skills, languages, AI tools, payment methods, and availability. Supports worldwide_hidden mode for overlooked opportunities. Live research at runtime; safety-first; no scams.
---

# /bq-job-finder — real work opportunity finder

## Purpose

Help the user find **legitimate** work opportunities. Build a job-search profile, research local + global + hidden platforms, classify by fit, surface application links + suggested pitches, track applications.

**Safety-first.** No scams. No fake reviews. No platform abuse. No VPN misrepresentation. No CAPTCHA farms.

## Syntax

```
/bq-job-finder
/bq-job-finder "<situation or filter>"
/bq-job-finder worldwide_hidden=true
/bq-job-finder worldwide_hidden=true "Find overlooked remote tasks and AI-assisted work opportunities"
```

Modes:
- **Default** — uses user's country + language as primary filter
- **`worldwide_hidden=true`** — searches beyond user's region and famous platforms; finds overlooked legitimate opportunities (see §10)

## When to use it

- You want a job or freelance work
- You want to expand into international / remote work
- You want AI-assisted gigs (image edit, video, content, research, automation)
- You want hidden opportunities your usual searches miss

## When NOT to use it

- You already have a job and want to make extra income → use `/bq-make-money` (overlaps but different intake)
- You want to build a SaaS / product → use `/bq-new` + `/bq-spec`
- You want immediate paid microtasks only — `/bq-make-money` (lighter intake, faster path)

## Preconditions

- `BEQUITE_INITIALIZED`

## Required previous gates

- `BEQUITE_INITIALIZED`

## Files to read

- `.bequite/jobs/JOB_PROFILE.md` (if exists from prior run)
- `.bequite/jobs/JOB_SEARCH_LOG.md` (if exists — for repeat-search comparison)
- `.bequite/jobs/OPPORTUNITIES.md` (if exists — to compare new vs. old)
- `.bequite/jobs/APPLICATION_TRACKER.md` (if exists)
- `.bequite/state/PROJECT_STATE.md`

## Files to write

- `.bequite/jobs/JOB_PROFILE.md` — user's intake answers
- `.bequite/jobs/JOB_SEARCH_LOG.md` — append-only log per search
- `.bequite/jobs/OPPORTUNITIES.md` — current ranked list
- `.bequite/jobs/APPLICATION_TRACKER.md` — user-maintained later
- `.bequite/jobs/PITCH_TEMPLATES.md` — suggested pitches per opportunity type
- `.bequite/logs/AGENT_LOG.md`

## Workflow

### Step 1 — Intake (skip if `JOB_PROFILE.md` exists and is < 30 days old)

Ask the user (concise; one batch):

1. Name or nickname (optional)
2. Country
3. City / timezone
4. Languages (native + fluent)
5. Age range (only if relevant — some platforms have minimums)
6. Work type wanted (one or many): task / freelance / part-time / full-time / remote
7. Skills (list — coding, design, video, writing, etc.)
8. Tools you use (Photoshop, Figma, Excel, etc.)
9. AI tools you use (ChatGPT, Claude, Midjourney, Runway, etc.)
10. Portfolio links (GitHub, LinkedIn, Behance, personal site)
11. Expected income range (per month, or per hour, or per task)
12. Hours per week available
13. Preferred industries (or "open")
14. Things you cannot or will not do (e.g. "no calls", "no sales", "no NSFW")
15. Payment methods you can use (PayPal, Payoneer, Wise, bank transfer, crypto, mobile wallet)
16. Can you work with international clients? (yes / no / depends)

If `JOB_PROFILE.md` is recent → ask the user "Use existing profile? (y/N)" and skip re-intake if yes.

### Step 2 — Build JOB_PROFILE.md

Write the user's answers to `.bequite/jobs/JOB_PROFILE.md` with timestamps.

### Step 3 — Research opportunities (Claude searches for you)

⚠ **Claude does the search work — not the user.** When you invoke this command, Claude uses whichever research tools are available in the active host:

| Tier | Tool | When to use |
|---|---|---|
| 1 | **WebFetch + WebSearch** (built-in) | Default for public, fetchable pages |
| 2 | **Chrome MCP** (`mcp__claude-in-chrome__*`) | When a page needs JS rendering, scroll-to-load, DOM inspection, or interactive search forms. Auto-used if loaded |
| 3 | **Computer Use MCP** (`mcp__computer-use__*`) | Last resort — for native interactions or sites that block headless browsers. Requires explicit user `request_access` permission |

You sit back. Claude reports the findings. You decide which to act on.

**Failure paths:**
- Rate-limited / blocked → degrade to known platforms by region; mark items "needs manual verification"
- Captcha walls → **never** solve; flag platform as gated and skip
- Login walls → ask user if they want to share access (never auto-login)
- ToS conflicts → respect platform terms; don't scrape where forbidden
- Suspicious link from observed content → verify URL before navigating (per the link-safety rules baked into computer use / Chrome MCP)

Search across:

- **Local country platforms** (per user's country — e.g. for Egypt: Forsa, Wuzzuf, ShoghlOnline; for India: Naukri, Internshala)
- **International platforms** (LinkedIn, Indeed, Glassdoor)
- **Remote job boards** (Remote.co, We Work Remotely, RemoteOK, Working Nomads, Himalayas)
- **Freelance platforms** (Upwork, Fiverr, Toptal, Contra, Freelancer.com)
- **AI gig platforms** (Outlier, Data Annotation, Surge AI, Scale AI, Mercor)
- **Niche-by-skill platforms** (Stack Overflow Jobs for dev; Dribbble Jobs for design; ProBlogger for writing)
- **Company career pages** (top companies hiring user's skill mix)
- **Startup communities** (Y Combinator Work at a Startup, Wellfound/AngelList)
- **Task-based platforms** (Clickworker, Microworkers, Amazon MTurk)
- **Public LinkedIn posts** with hashtags like `#hiring`, `#remoteok`
- **Public Facebook job groups** (per user's language / region)
- **Discord / Slack communities** (where the user can opt to join)
- **Indie Hackers**, **Polywork**, **read.cv** for indie/remote work

Search in **local language + English** + any other user-listed language.

### Step 4 — `worldwide_hidden=true` extra research

If `worldwide_hidden=true`, expand search to include:

- European country-specific platforms (e.g. Stepstone-DE, Welcome-to-the-Jungle-FR, Lavorare-IT)
- Latin American platforms (Get on Board, Computrabajo, LovelyJobs-BR)
- Asian platforms (LiNGOL-JP, Wantedly-JP, JobStreet, JobsDB)
- African platforms (Brighter Monday-NG, Pnet-ZA)
- Russian / Eastern European platforms (when language fits)
- Translation gig boards (Gengo, ProZ, OneHourTranslation)
- AI training task platforms (Outlier, Mercor, Data Annotation, Surge, Mindrift)
- Data labeling platforms (Scale, Labelbox, Toloka, Appen, Clickworker)
- Research panels (User Interviews, Respondent, dscout, Wynter)
- Browser/search testing panels (UserTesting, UserBrain, Lookback, PlaybookUX)
- App-based earning programs (Premise, Field Agent, Streetbees)
- Niche platforms by region (varies — research live)
- Remote-first startup boards (RemoteHabits, JustRemote, FlexJobs)

Search in **multiple languages**: Portuguese, Spanish, German, French, Italian, Turkish, Polish, Romanian, Indonesian, Hindi, Arabic, English — pick the ones that match user's language list + opportunity region.

### Step 5 — Verify each opportunity (trust check)

For every shortlisted opportunity, check:

- **Legitimacy** — Trustpilot reviews, Reddit threads, payout proof, BBB if US
- **Still active?** — recent posts, careers page activity
- **Country eligibility** — does it allow the user's country?
- **Residency requirement?** — some require local bank / tax ID
- **Payout methods** — PayPal / Payoneer / Wise / bank / crypto / mobile money
- **VPN policy** — allowed / forbidden / detected
- **Identity verification required?** — passport / ID / selfie
- **Upfront payment required?** — usually a red flag
- **Payout complaints?** — search "<platform name> payout problems"
- **Scam reports?** — search "<platform name> scam"
- **Realistic pay range** — what real users report
- **Time to first payout** — minimum threshold + processing time
- **Required skills + language**
- **Why hidden / overlooked?** (for `worldwide_hidden=true`)

### Step 6 — Classify

Each opportunity gets a category:

- **Best fit** — high match with profile
- **Easy start** — low barrier (no portfolio, instant signup)
- **High pay** — top of range
- **Fast application** — apply in < 5 min
- **Needs portfolio** — apply only with samples
- **Needs learning first** — recommend learning before applying
- **Risky or unclear** — verify before applying
- **Not recommended** — fails safety checks → flag + exclude

For `worldwide_hidden=true`, add: **Hidden Gem** category.

### Step 7 — Rank + output

Output (write to `OPPORTUNITIES.md` + print in chat):

```markdown
# Job opportunities — <date>

**Profile:** <country> · <languages> · <skills>
**Mode:** <default | worldwide_hidden>
**Search depth:** <local | regional | worldwide>

## Best fit (top 5-10)

### 1. <Platform / Company name>

- **Type:** full-time / part-time / freelance / task / AI gig
- **Country:** <region> | **Language:** <language>
- **Why it fits:** <one-line>
- **Requirements:** <list>
- **Application link:** <URL>
- **Suggested pitch:** <template — saved to PITCH_TEMPLATES.md>
- **Estimated difficulty:** easy / medium / hard
- **Estimated pay:** <range if available>
- **Trust level:** verified / decent / unverified / flagged
- **Payout methods:** <list>
- **Time to first payout:** <estimate>
- **Next action:** <click apply, build portfolio item, etc.>

(repeat per opportunity)

## Easy start

(...)

## High pay

(...)

## Hidden Gems (only if worldwide_hidden=true)

(...)

## Risky or unclear

(...)

## Not recommended (with reason)

- <Platform> — <why excluded; saved here so user doesn't waste time>
```

### Step 8 — Repeat-search behavior

If `OPPORTUNITIES.md` already exists from a previous run:

- Compare new findings to previous
- Mark each opportunity:
  - 🆕 **New** — wasn't in last search
  - ✅ **Still active** — found again
  - ❌ **Expired** — was active, now gone
  - ⚠ **Risk increased** — new scam reports or payout complaints
  - ⬆ **Better alternative found** — a related opportunity with better terms
  - 🔍 **Needs manual verification** — couldn't fully verify this run

Append a `## Changes since <last date>` section.

### Step 9 — Save pitch templates

For each opportunity-type, save a reusable pitch template to `.bequite/jobs/PITCH_TEMPLATES.md`:

- AI gig task application
- Freelance proposal (Upwork-style)
- Remote full-time application
- LinkedIn cold outreach
- Local-language application

Each template ≤ 200 words. User fills in name + portfolio links.

### Step 10 — Final report

```
✓ Job finder complete

Profile: .bequite/jobs/JOB_PROFILE.md
Log:     .bequite/jobs/JOB_SEARCH_LOG.md
Results: .bequite/jobs/OPPORTUNITIES.md
Pitches: .bequite/jobs/PITCH_TEMPLATES.md

Opportunities found: <N>
  Best fit:    <count>
  Easy start:  <count>
  High pay:    <count>
  Hidden Gems: <count> (if worldwide_hidden)
  Risky:       <count>
  Excluded:    <count>

Next:
  - Open OPPORTUNITIES.md
  - Pick 2-3 to apply this week
  - Track applications in APPLICATION_TRACKER.md
  - Re-run /bq-job-finder weekly for fresh results
```

## Safety and trust rules

Per `bequite-job-finder` skill — strict NEVER list:

- ❌ Scammy jobs (upfront payment, fake reviews, "make $$$ from home with no skills")
- ❌ Illegal work (jurisdiction-dependent — flag explicitly per region)
- ❌ Account renting / identity-for-rent schemes
- ❌ Bypassing platform rules (multi-accounting, fake locations)
- ❌ CAPTCHA-solving farms — likely abuse + low pay
- ❌ VPN to misrepresent eligibility
- ❌ Identity misuse / document forgery
- ❌ Jobs requiring upfront payment unless verifiably legitimate (rare)
- ❌ "Earn while you sleep" passive-income MLM
- ❌ Crypto pump-and-dump groups
- ❌ Adult / NSFW unless user explicitly opted in
- ❌ Anything that fails the trust check

Always check: payout proof, platform reputation, region eligibility, fees, withdrawal methods.

## Output format

Structured markdown to `OPPORTUNITIES.md` + chat summary.

## Quality gate

- Profile saved to `JOB_PROFILE.md`
- At least 5 verified opportunities surfaced (or honest "couldn't find more than N legitimate matches")
- Every opportunity has trust check + payout method + eligibility
- Pitches saved as reusable templates
- No banned weasel words
- No scam-pattern opportunities included

## Failure behavior

- Live web research unavailable → degrade gracefully; surface known platforms by region from skill knowledge + flag as "verify yourself before applying"
- User refuses to share country / skills → run with anonymized profile; warn that results will be less targeted
- All search sources return blocked / rate-limited → write what we have; suggest retry in 24h

## Memory updates

- `JOB_PROFILE.md` — created or refreshed
- `JOB_SEARCH_LOG.md` — append entry
- `OPPORTUNITIES.md` — overwrite or merge per repeat-search behavior
- `PITCH_TEMPLATES.md` — append new templates
- `APPLICATION_TRACKER.md` — user-maintained going forward

## Log updates

- `AGENT_LOG.md` — entry per search run

## Tool neutrality (global rule)

The platforms listed (LinkedIn, Upwork, Outlier, Wuzzuf, etc.) are **examples** — not endorsements or exclusive recommendations. The 10 decision questions apply:

1. Project type? (the user's earning situation)
2. Actual problem? (need income / want career)
3. Scale? (one task vs. full-time)
4. Constraints? (country, language, payout)
5. Existing stack? (skills, AI tools)
6. UX needed? (calls or no calls)
7. Failure risks? (scams, non-payment)
8. Proven tools? (platforms with payout proof)
9. Overkill? (don't recommend Toptal if user has no portfolio)
10. Best output / least complexity?

The agent researches at runtime and reports findings honestly. User decides which platforms to actually engage.

See `.bequite/principles/TOOL_NEUTRALITY.md`.

## Standardized command fields (alpha.8)

**Phase:** Any (lifestyle / career command; not part of P0-P5 workflow)
**When NOT to use:** product-development tasks (use other commands); scammy "fast money" goals (refused)
**Preconditions:** `BEQUITE_INITIALIZED`
**Required previous gates:** `BEQUITE_INITIALIZED`
**Quality gate:** profile saved; ≥5 verified opportunities or honest under-count; trust check per item; pitches saved; safety rules enforced
**Failure behavior:** web research blocked → degrade with known platforms + verify-yourself caveat; all blocked → write what we have, suggest 24h retry
**Memory updates:** `.bequite/jobs/` 5 files
**Log updates:** `AGENT_LOG.md`

## Usual next command

- Open `OPPORTUNITIES.md` and pick 2-3 to apply to
- Track applications in `APPLICATION_TRACKER.md` (user-maintained)
- Re-run `/bq-job-finder` weekly for fresh results
- `/bq-make-money` if user wants supplementary income alongside main job search
