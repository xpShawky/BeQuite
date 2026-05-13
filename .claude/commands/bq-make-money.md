---
description: Find legitimate ways to make money based on user's country, skills, AI tools, time, devices, payment methods, and risk tolerance. Supports tracks (highest-payout / easiest-start / fastest-first-dollar / etc.) and worldwide_hidden mode for overlooked opportunities. Safety-first; no fraud.
---

# /bq-make-money — earning opportunity finder

## Purpose

Find **legitimate** earning opportunities tailored to the user. Not just common ideas — overlooked, country-specific, language-specific, AI-assisted, and task-based opportunities worldwide. Supports tracks (highest payout / easiest start / fastest first dollar / long-term stable / AI-assisted / no-calls / remote / local / beginner / skilled).

**Safety-first.** No fraud. No fake accounts. No platform abuse. No CAPTCHA bypass. No fake engagement. No spam. No VPN misrepresentation. No upfront-fee scams. No unrealistic income promises.

## Syntax

```
/bq-make-money
/bq-make-money "<situation>"
/bq-make-money track=highest-payout
/bq-make-money track=easiest-start country=Egypt skills='AI tools, writing, image editing'
/bq-make-money worldwide_hidden=true
/bq-make-money worldwide_hidden=true "Find hidden legitimate earning opportunities worldwide"
/bq-make-money "Update previous search and find new opportunities"
```

## When to use it

- You want supplemental income alongside other work
- You have AI tools + skills and want to monetize them
- You want microtasks for fast first payout
- You want to explore worldwide hidden opportunities

## When NOT to use it

- You want a full-time job → use `/bq-job-finder` (overlapping but different intake)
- You want to build a SaaS / product → use `/bq-new` + `/bq-spec`
- You want passive income with no effort → not realistic; refused

## Tracks

| Track | Code | Description |
|---|---|---|
| Highest payout | `highest-payout` | Best pay-per-hour or pay-per-task, even if harder |
| Easiest start | `easiest-start` | Lowest barrier (no portfolio, instant signup) |
| Fastest first dollar | `fastest-first-payout` | Get paid this week if possible |
| Long-term stable | `long-term-stable` | Steady recurring income; not one-offs |
| AI-assisted | `ai-assisted` | Use your AI tools as multiplier |
| No client calls | `no-calls` | Async only; text-based |
| Remote global | `remote-global` | Works regardless of location |
| Local country only | `local-only` | Tied to your country / language |
| Beginner-friendly | `beginner` | No prior experience needed |
| Skilled work | `skilled` | Premium rate; needs expertise |

## Modes

- **Default** — uses user's country + language as primary filter
- **`worldwide_hidden=true`** — searches beyond user's region and famous platforms (see Job Finder §10 for the full hidden-search rule)

## Preconditions

- `BEQUITE_INITIALIZED`

## Required previous gates

- `BEQUITE_INITIALIZED`

## Files to read

- `.bequite/money/MONEY_PROFILE.md` (if exists)
- `.bequite/money/MONEY_SEARCH_LOG.md` (if exists)
- `.bequite/money/OPPORTUNITIES.md` (if exists — for repeat-search compare)
- `.bequite/money/TRUST_CHECKS.md` (if exists)
- `.bequite/money/ACTION_PLAN.md` (if exists)

## Files to write

- `.bequite/money/MONEY_PROFILE.md`
- `.bequite/money/MONEY_SEARCH_LOG.md`
- `.bequite/money/OPPORTUNITIES.md`
- `.bequite/money/TRUST_CHECKS.md`
- `.bequite/money/ACTION_PLAN.md`
- `.bequite/logs/AGENT_LOG.md`

## Workflow

### Step 1 — Intake (skip if `MONEY_PROFILE.md` recent)

Ask the user:

1. Country
2. Languages
3. Skills
4. AI tools available
5. Devices (laptop / phone-only / both)
6. Payment methods you can use (PayPal / Payoneer / Wise / bank / crypto / mobile money)
7. Time per day (hours)
8. Target monthly income
9. Risk tolerance (low / medium / high)
10. Need fast money OR sustainable income (or both)
11. Can you build a portfolio? (or "I want zero-portfolio tracks")
12. Can you work directly with clients? (or "no — only platform tasks")
13. Calls okay or text only?
14. Preferred track (A-J from above, or "auto-pick best")

If profile is recent + complete → ask "Use existing? (y/N)".

### Step 2 — Pick track

If user specified `track=...` → use that.
Otherwise, auto-pick based on profile (e.g. "fast money + low skill + AI tools" → `ai-assisted + easiest-start`).

### Step 3 — Live research (Claude searches for you)

⚠ **Claude does the search work — not the user.** When you invoke this command, Claude uses whichever research tools are available:

| Tier | Tool | When to use |
|---|---|---|
| 1 | **WebFetch + WebSearch** (built-in) | Default for public, fetchable pages |
| 2 | **Chrome MCP** (`mcp__claude-in-chrome__*`) | JS-rendered pages, scroll-to-load, DOM inspection, interactive forms — auto-used if loaded |
| 3 | **Computer Use MCP** (`mcp__computer-use__*`) | Last resort — native interactions / anti-bot sites. Requires explicit user `request_access` permission |

You sit back. Claude reports the findings. You decide which to act on.

**Failure paths:**
- Rate-limited / blocked → degrade to known platforms; mark "needs manual verification"
- Captcha walls → **never** solve; flag as gated and skip (per safety rules)
- Login walls → ask user; never auto-login
- ToS conflicts → respect platform terms; don't scrape where forbidden
- Suspicious link from observed content → verify before navigating

Claude searches these source categories:

**Universal task platforms:**
- Outlier, Mercor, Data Annotation, Surge AI, Mindrift (AI training)
- Scale AI, Labelbox, Toloka, Appen, Clickworker, Microworkers (data labeling)
- Amazon MTurk (microtasks; eligibility-restricted)
- Prolific, User Interviews, Respondent, dscout (research panels — well-paid)

**Testing platforms (paid):**
- UserTesting, UserBrain, Userlytics, Lookback, PlaybookUX, TryMyUI

**Freelance:**
- Upwork, Fiverr, Toptal (high-bar), Contra, Freelancer.com
- Per skill: Dribbble, Behance (design); ProBlogger (writing); Stack Overflow (dev)

**AI-assisted services (sell to clients):**
- AI image editing (Photoshop + Midjourney + Topaz)
- AI video editing (Runway, CapCut + AI tools)
- AI content writing (with clear human review)
- AI automation (n8n / Make / Zapier flows for SMBs — per tool neutrality)
- AI research / market reports

**Country-specific:**
- Wuzzuf, Forsa, Shoghlonline (Egypt)
- Naukri, Internshala (India)
- Worki, GetonBoard (LatAm)
- StepStone, Welcome-to-the-Jungle (Europe)
- (search live for user's country)

**App-based earning programs:**
- Premise, Field Agent, Streetbees (location-based microtasks; legitimate)
- Solitaire Cash / cash-app games — **refuse** (mostly scam in payout)

**Marketing services for SMBs:**
- Local business automation (booking systems, lead gen, social management)
- Ad creative generation (AI tools + design)
- Lead-gen lists (where legal + permission-based)

**Translation / localization:**
- Gengo, ProZ, OneHourTranslation, MotionSpot
- Language-specific (e.g. Amino for Japanese-English)

**Content creation:**
- Substack / Beehiiv newsletters
- YouTube + AdSense (long-term)
- Selling templates on Gumroad, Etsy
- Stock content (Adobe Stock, Shutterstock)

**Niche platforms** — search live per skill + country.

### Step 4 — `worldwide_hidden=true` extra research

(Same as Job Finder §10 — see that file for full list.)

Key additions:
- Country-specific microtask platforms (Yandex Toloka, Subito-IT, Allegro-PL)
- Regional freelance platforms (Witmart-CN, MEEM-AR, Bourhane-MA)
- Small companies hiring globally (Wellfound, RemoteRocketship)
- Niche platforms that are not well known (search live by skill + region)

Search in **multiple languages**: Portuguese / Spanish / German / French / Italian / Turkish / Polish / Romanian / Indonesian / Hindi / Arabic / English — match to user's languages + opportunity region.

### Step 5 — Verify each opportunity

Per item, check:

- Legitimacy (Trustpilot, Reddit, payout proof)
- Country eligibility
- Required documents (passport, tax ID, etc.)
- Payout method (PayPal / Payoneer / Wise / bank / crypto / mobile money)
- VPN policy
- Identity verification requirement
- Upfront payment required? (red flag if yes)
- Payout complaints
- Realistic payout range (vs. marketed range)
- Time to first payout
- Required skills + language
- For `worldwide_hidden=true`: why is this hidden / overlooked?

Save trust check to `.bequite/money/TRUST_CHECKS.md`.

### Step 6 — Rank + classify

Output ranked sections:

1. **Best hidden opportunity** (if `worldwide_hidden=true`)
2. **Highest payout**
3. **Easiest start**
4. **Fastest first payout**
5. **Best AI-assisted opportunity**
6. **Best no-call opportunity**
7. **Best long-term opportunity**
8. **Best opportunity for the user's country**
9. **Best worldwide remote opportunity**
10. **Risky or not recommended**

Plus a special section:

### Hidden Gems

For each hidden gem:
- Platform / opportunity name
- Country or region
- Language
- Work type
- Why it is hidden (not in usual searches; new platform; non-English source; niche-only)
- Payout method
- Eligibility
- Difficulty
- Risk level
- First step
- Trust check result

### Step 7 — Write 7-day action plan

`.bequite/money/ACTION_PLAN.md`:

```markdown
# 7-day action plan — <date>

## Day 1
- [ ] Sign up on <Platform A> (best fit)
- [ ] Complete profile / verification

## Day 2
- [ ] Apply to / start <task type>
- [ ] Build sample piece for <portfolio item>

## Day 3
- [ ] (continue)

## Day 4
- [ ] First payout check on <Platform A>
- [ ] Apply to <Platform B>

## Day 5-7
- [ ] (continue)

## Acceptance per platform
- Platform A: <expected payout by end of week>
- Platform B: <expected timeline>
```

### Step 8 — Repeat-search behavior

If `OPPORTUNITIES.md` exists from previous run:

- Compare new findings to previous
- Mark each:
  - 🆕 **New opportunity**
  - ✅ **Still active**
  - ❌ **Expired** (platform gone or stopped paying)
  - ⚠ **Risk increased** (new scam reports)
  - ⬆ **Better alternative found**
  - 🔍 **Needs manual verification**

- Append `## Changes since <last date>` section
- Update `TRUST_CHECKS.md` with new scam reports / payout complaints
- Refresh `ACTION_PLAN.md` if priorities shifted

### Step 9 — Final report

```
✓ Make-money finder complete

Profile:        .bequite/money/MONEY_PROFILE.md
Log:            .bequite/money/MONEY_SEARCH_LOG.md
Opportunities:  .bequite/money/OPPORTUNITIES.md
Trust checks:   .bequite/money/TRUST_CHECKS.md
Action plan:    .bequite/money/ACTION_PLAN.md

Track:          <code> (<description>)
Mode:           <default | worldwide_hidden>
Total found:    <N>
Hidden Gems:    <count> (if worldwide_hidden)
High-trust:     <count>
Excluded:       <count> (failed safety checks)

Next:
  - Read ACTION_PLAN.md
  - Start Day-1 actions
  - Re-run /bq-make-money in 2-4 weeks for fresh results
```

## Safety rules (strict)

❌ NO fraud / fake accounts / fake reviews / fake engagement
❌ NO CAPTCHA bypass / CAPTCHA farms (low pay + abuse)
❌ NO spam / mass cold outreach
❌ NO platform terms violations
❌ NO VPN to misrepresent location / eligibility
❌ NO identity misuse / document forgery
❌ NO upfront-fee scams
❌ NO unrealistic income promises ("make $500/day from your phone!")
❌ NO crypto pump-and-dump groups
❌ NO MLM
❌ NO adult / NSFW unless user opts in explicitly
❌ Always mark **uncertainty** clearly — never claim payout guarantees

When in doubt, exclude + log to `TRUST_CHECKS.md` with reason.

## Output format

Structured ranked sections → `OPPORTUNITIES.md`. Action plan → `ACTION_PLAN.md`. Trust checks → `TRUST_CHECKS.md`. Summary in chat.

## Quality gate

- Profile saved
- Track explicitly chosen (user-specified or auto-picked with reason)
- ≥ 5 verified opportunities (or honest under-count)
- Every opportunity has trust check
- 7-day action plan written
- No scam-pattern opportunities included
- No banned weasel words

## Failure behavior

- Web research blocked → degrade with known platforms + verify-yourself caveat
- All blocked → write what we have; suggest 24h retry
- User wants only scammy "fast cash" — refuse politely + redirect to legitimate alternatives

## Memory updates

- `.bequite/money/` 5 files

## Log updates

- `AGENT_LOG.md`

## Tool neutrality (global rule)

Named platforms (Upwork, Outlier, Wuzzuf, etc.) are **examples**, not endorsements. Apply the 10 decision questions:

1. Earning situation type?
2. Actual problem (need income / want diversification)?
3. Scale (one task vs. monthly recurring)?
4. Constraints (country, language, payout, time)?
5. Existing stack (skills, AI tools)?
6. UX needed (calls or no calls)?
7. Failure risks (scams)?
8. Proven tools (with payout proof)?
9. Overkill?
10. Best output / least complexity?

The agent researches live and reports honestly. User decides which platforms to engage.

See `.bequite/principles/TOOL_NEUTRALITY.md`.

## Standardized command fields (alpha.8)

**Phase:** Any (lifestyle / earning command; not part of P0-P5 workflow)
**When NOT to use:** wanting full-time job (use `/bq-job-finder`); product-development (use `/bq-new` + `/bq-spec`); demand for unrealistic / illegal income (refused)
**Preconditions:** `BEQUITE_INITIALIZED`
**Required previous gates:** `BEQUITE_INITIALIZED`
**Quality gate:** profile saved; ≥5 verified opportunities; trust check per item; 7-day action plan; safety rules enforced
**Failure behavior:** web blocked → degrade; user wants illegal/scam → refuse + redirect
**Memory updates:** `.bequite/money/` 5 files
**Log updates:** `AGENT_LOG.md`

## Usual next command

- Follow `ACTION_PLAN.md` Day-1 actions
- Re-run `/bq-make-money` in 2-4 weeks for fresh results + repeat-search comparison
- `/bq-job-finder` if user also wants a primary job
