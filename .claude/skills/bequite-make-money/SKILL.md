---
name: bequite-make-money
description: Earning opportunity discovery + verification. 10 tracks (highest-payout / easiest-start / fastest-first-dollar / AI-assisted / no-calls / remote / local / beginner / skilled / long-term). Local + global + hidden platforms. Strict safety (no fraud / scams / VPN misrepresentation / upfront-fee). Invoked by /bq-make-money.
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Write
---

# bequite-make-money — earning opportunity discovery

## Purpose

Be the BeQuite expert on **legitimate** earning opportunities — country-specific, language-specific, AI-assisted, task-based, hidden, and worldwide. Apply track-based filtering. Live web research at runtime. Strict safety rules.

Invoked by `/bq-make-money`.

---

## The 10 tracks

| Track | Code | Optimization |
|---|---|---|
| Highest payout | `highest-payout` | $/hour or $/task — top of range |
| Easiest start | `easiest-start` | No portfolio, instant signup, fast verify |
| Fastest first dollar | `fastest-first-payout` | Get paid this week |
| Long-term stable | `long-term-stable` | Recurring monthly income, not one-offs |
| AI-assisted | `ai-assisted` | Use user's AI tools as multiplier |
| No client calls | `no-calls` | Async-only, text-based |
| Remote global | `remote-global` | Works regardless of user's location |
| Local country only | `local-only` | Tied to country + language |
| Beginner-friendly | `beginner` | No prior experience needed |
| Skilled work | `skilled` | Premium rate; expertise required |

---

## Platform categories

### AI training + data labeling
Outlier, Mercor, Data Annotation, Surge AI, Mindrift, Scale AI, Labelbox, Toloka, Appen, Clickworker, Microworkers
- **Trust:** generally high for the named platforms
- **Payout:** $5-40/hour depending on skill match
- **Eligibility:** varies; some require US/EU residency
- **Track fit:** ai-assisted, beginner-friendly to skilled

### Microtask
Amazon MTurk (US restricted), Premise, Field Agent, Streetbees (location-based, legitimate)
- **Trust:** high for established names; verify newer
- **Payout:** $0.10-5 per task
- **Track fit:** easiest-start, fastest-first-payout

### Research panels (well-paid)
Prolific, User Interviews, Respondent, dscout, Wynter
- **Trust:** high; reputable academic / UX research
- **Payout:** $15-100+ per study; quality > quantity
- **Track fit:** highest-payout, easiest-start, no-calls (mostly)

### Testing
UserTesting, UserBrain, Userlytics, Lookback, PlaybookUX, TryMyUI
- **Trust:** high (established)
- **Payout:** $5-60 per test
- **Track fit:** easiest-start, ai-assisted (talk-aloud good for AI users)

### Freelance
Upwork, Fiverr, Toptal (high-bar), Contra, Freelancer.com, PeoplePerHour
- **Trust:** platform-dependent; verify per-client
- **Payout:** $5-100+/hour
- **Track fit:** skilled, long-term-stable, remote-global

### AI-assisted services (sell to clients)
- AI image editing (Photoshop + Midjourney + Topaz)
- AI video editing (Runway, CapCut + AI)
- AI content writing (with human review)
- AI automation (n8n / Make / Zapier for SMBs — per tool neutrality)
- AI research / market reports
- **Track fit:** ai-assisted, skilled, highest-payout

### Country-specific
Per user's country — search live.
- Egypt: Wuzzuf, Forsa, Shoghlonline
- India: Naukri, Internshala
- LatAm: Worki, GetonBoard
- Europe: StepStone, Welcome-to-the-Jungle

### Translation / localization
Gengo, ProZ, OneHourTranslation, Unbabel, MotionSpot
- **Trust:** generally high
- **Payout:** $0.03-0.10 per word (varies by pair)
- **Track fit:** ai-assisted, remote-global, skilled (per language pair)

### Content + creator economy
- Substack / Beehiiv (newsletters with subscriptions)
- YouTube + AdSense + sponsorships (long-term)
- Selling templates: Gumroad, Etsy, Creative Market
- Stock content: Adobe Stock, Shutterstock, iStock
- **Track fit:** long-term-stable, skilled, ai-assisted

### Local business automation (AI services)
- Booking automation (clinics, salons, gyms)
- Lead generation (per country regulations)
- Social media management
- Ad creative generation
- **Track fit:** ai-assisted, skilled, local-only

### Hidden / overlooked (`worldwide_hidden=true`)
- Country-specific microtask platforms (Yandex Toloka, Allegro-PL, Subito-IT)
- Regional freelance (Witmart-CN, MEEM-AR, Bourhane-MA)
- Niche platforms by skill (search live)
- Small companies hiring globally (Wellfound, RemoteRocketship)
- AI training task platforms (some restricted; verify)

---

## Research methodology — Claude does the search work

⚠ **The user does NOT search.** Claude runs the full discovery loop using whichever research tools are available in the active host.

**Tool tiers (in order of preference):**

1. **WebFetch + WebSearch** (built-in) — default; fast; works on any host
2. **Chrome MCP** (`mcp__claude-in-chrome__*`) — JS-rendered pages, scroll-to-load, DOM inspection. Auto-detected if loaded.
3. **Computer Use MCP** (`mcp__computer-use__*`) — last resort for native interactions / anti-bot sites. Requires user `request_access` permission.

The user invokes the command + answers intake. Claude:

1. **Reads** `MONEY_PROFILE.md` + track preference
2. **Queries** the chosen research tools per track + country + languages
3. **Cross-references** Reddit / Trustpilot / payout-proof communities
4. **Verifies** per trust-check criteria below
5. **Ranks** by 10 categories + Hidden Gems if `worldwide_hidden=true`
6. **Writes** `OPPORTUNITIES.md`, `TRUST_CHECKS.md`, `ACTION_PLAN.md`

**Failure handling:**

- Rate-limited → degrade gracefully; mark items "needs manual verification"
- Captcha walls → **never** solve; flag + skip
- Login walls → ask user; never auto-login
- ToS conflicts → respect platform terms
- All tiers fail for a platform → write what we have + flag for manual verification

## Trust check criteria

Per opportunity:

- Legitimacy (Trustpilot, Reddit, payout-proof communities)
- Country eligibility
- Required documents (passport, tax ID)
- Payout methods (PayPal / Payoneer / Wise / bank / crypto / mobile money)
- VPN policy
- ID verification requirement
- Upfront payment (red flag if yes)
- Payout complaints (search "<platform> payout problems")
- Scam reports (search "<platform> scam")
- Realistic pay range (vs. marketed)
- Time to first payout
- Required skills + language
- For hidden: why hidden / overlooked

Save trust check to `TRUST_CHECKS.md` per platform.

---

## Safety rules (strict)

❌ NO fraud / fake accounts / fake reviews / fake engagement
❌ NO CAPTCHA bypass / CAPTCHA farms
❌ NO spam / mass cold outreach
❌ NO platform terms violations
❌ NO VPN to misrepresent location
❌ NO identity misuse
❌ NO upfront-fee scams
❌ NO unrealistic income promises
❌ NO crypto pump-and-dump
❌ NO MLM
❌ NO adult / NSFW unless user explicitly opts in
❌ Mark **uncertainty** clearly — never claim payout guarantees

When in doubt, exclude + log to `TRUST_CHECKS.md` with reason.

---

## Worldwide hidden mode

(Same protocol as `bequite-job-finder` skill §"Worldwide hidden mode".)

When `worldwide_hidden=true`:
- Expand beyond user's country / language
- Search multilingual (Portuguese / Spanish / German / French / Italian / Turkish / Polish / Romanian / Indonesian / Hindi / Arabic / English)
- Surface Hidden Gems with full trust check
- Look for overlooked country-specific platforms, regional boards, niche communities

---

## Repeat-search behavior

If `OPPORTUNITIES.md` exists from previous run:

- Read previous results
- Mark each in new list: 🆕 / ✅ / ❌ / ⚠ / ⬆ / 🔍
- Append `## Changes since <last date>` section
- Update `TRUST_CHECKS.md` with new scam reports / payout complaints
- Refresh `ACTION_PLAN.md` if priorities shifted

---

## 7-day action plan philosophy

A good action plan:

- 1-3 platform signups in Day 1-2 (no more — overload causes inaction)
- First payout target in Day 3-7
- Concrete deliverables (not "work on profile" — "complete profile, take 3 sample tasks")
- Realistic expected payout per platform
- Per-platform acceptance criteria

Refresh weekly on repeat searches.

---

## Anti-patterns

- ❌ Recommending too many opportunities (overload + no action)
- ❌ Recommending platforms with payout complaints
- ❌ Hidden gems without trust check (defeats the point)
- ❌ Suggesting CAPTCHA farms / fake review services (banned)
- ❌ Optimistic income claims without uncertainty markers
- ❌ Ignoring repeat-search comparison
- ❌ Recommending a platform that requires the user to bypass its terms

---

## What this skill does NOT do

- Sign up the user on platforms (out of scope)
- Apply to gigs for the user (out of scope)
- Generate fake accounts / fake reviews / fake engagement (refused)
- Provide financial / tax advice (out of scope — recommend consulting an accountant)
- Replace `/bq-job-finder` (that's primary jobs; this is earning ops)

---

## See also

- `.claude/commands/bq-make-money.md` — the command spec
- `.bequite/money/` — memory templates
- `bequite-job-finder` skill — overlapping but jobs-focused
- `bequite-researcher` skill — applies the same evidence rigor
- `.bequite/principles/TOOL_NEUTRALITY.md` — platforms named here are candidates, not endorsements

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
