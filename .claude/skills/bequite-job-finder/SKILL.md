---
name: bequite-job-finder
description: Real work opportunity discovery + verification. Local + global + hidden platforms. Classifies by fit (best / easy / high pay / fast apply / risky). Strict safety (no scams / fake reviews / VPN misrepresentation / upfront-fee / identity misuse). Invoked by /bq-job-finder.
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

## Research methodology — Claude does the search work

⚠ **The user does NOT search.** Claude runs the full discovery loop using whichever research tools are available in the active host (Claude Code, Claude Desktop, API, etc.):

**Tool tiers (in order of preference):**

1. **WebFetch + WebSearch** (built-in) — default; fast; works on any host
2. **Chrome MCP** (`mcp__claude-in-chrome__*`) — JS-rendered pages, scroll-to-load, DOM inspection. Auto-detected if the MCP is loaded.
3. **Computer Use MCP** (`mcp__computer-use__*`) — last resort for native-interaction sites. Requires explicit user `request_access` permission (tier-3 full desktop).

The user invokes the command, answers the intake form (or accepts existing profile), and waits. Claude:

1. **Reads** `JOB_PROFILE.md` to know user's constraints (country, language, skills, payout)
2. **Queries** the chosen research tools with profile-specific search strings (local language + English + skill keywords)
3. **Cross-references** Reddit, Trustpilot, payout-proof communities per platform candidate
4. **Filters** — excludes anything failing safety rules
5. **Ranks** — by match score (profile fit × trust × payout)
6. **Documents** — every claim has source URL + date accessed (`bequite-researcher` rigor)

**Failure handling per tier:**

| Failure | Tier 1 recovery | Tier 2 recovery | Tier 3 recovery |
|---|---|---|---|
| Page blocks WebFetch | Try search engine result | Open in Chrome MCP, parse DOM | Open in real desktop browser |
| JS-only content | Skip; flag | Use Chrome MCP `read_page` | Same |
| Captcha | Skip; flag platform | Skip | Skip — **never solve** |
| Login wall | Skip; ask user | Same | Same |
| Rate limit | Wait; retry once; then degrade | Try Chrome MCP if WebFetch limited | Try computer-use last |
| ToS violation | Respect; skip | Same | Same |
| Suspicious link | Verify URL first; flag user | Same | Same — link safety rules apply |

If ALL tiers fail for a platform → mark "needs manual verification" in `OPPORTUNITIES.md` and recommend user verify directly.

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

---

## When NOT to use this skill (alpha.15)

- The task at hand doesn't touch this skill's domain — defer to the right specialist skill
- A faster / simpler skill covers the same need — pick the simpler one and document why
- The skill's core invariants don't apply to the current project (e.g. regulated-mode rules on a prototype)
- The command that would activate this skill is already running with another specialist that fits better

If unsure, surface the trade-off in the command's output and let the user decide.

## Quality gate (alpha.15)

Before claiming this skill's work complete:

- [ ] Artifacts produced match the skill's expected outputs
- [ ] All discipline rules in this skill were respected (not just glanced at)
- [ ] No banned weasel words in any completion claim — `should`, `probably`, `seems to`, `appears to`, `might`, `hopefully`, `in theory`
- [ ] Any tool / library / framework added during this run has a decision section per `.bequite/principles/TOOL_NEUTRALITY.md`
- [ ] Acceptance criteria for the invoking command's task are met (or honestly reported as PARTIAL / FAIL)
- [ ] `.bequite/state/MISTAKE_MEMORY.md` updated when a project-specific lesson surfaced
- [ ] `.bequite/logs/AGENT_LOG.md` entry appended for the run
- [ ] Memory state files (LAST_RUN, WORKFLOW_GATES, CURRENT_PHASE) updated when gate state changed

If any item fails, do not claim done — report PARTIAL with the specific gap.
