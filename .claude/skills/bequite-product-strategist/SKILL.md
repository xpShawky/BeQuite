---
name: bequite-product-strategist
description: Senior-product-thinking procedures — Jobs To Be Done, persona definition, MVP scoping, scope-creep defense, differentiation tests, pricing assumptions, north-star metric. Loaded by /bq-clarify, /bq-scope, /bq-plan. Forces decisions before code.
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch
---

# bequite-product-strategist — think like a senior PM, not a coder

## Why this skill exists

The most expensive bug is shipping the wrong thing. Code is cheap; user attention is not. This skill encodes the questions a senior PM would force you to answer before a single line of code.

If the user can't answer these, the project isn't ready for `/bq-plan`. Push back.

---

## The 5 questions every project must answer

### Q1 — What's the Job To Be Done?

Frame: "When [situation], I want to [motivation], so I can [expected outcome]."

Examples:
- ✗ "We need a CRM" (not a job)
- ✓ "When I prep for a sales call, I want to see the prospect's recent emails + last meeting notes in one place, so I don't ask them to repeat themselves" (concrete job)

If the user can't write this in one sentence, brainstorm with them.

### Q2 — Who is the user (concretely)?

Not "small business owners." Concretely:
- Role (CEO / engineer / accountant)
- Company size + stage
- Daily software they already use
- One named person you've talked to who fits this

If they can't name one real person, flag it. Personas without people are fiction.

### Q3 — What do they do today without this?

Three possibilities:
1. **Workaround** — Excel sheets, manual processes, fragmented tools
2. **Direct competitor** — they pay for X today; you replace X
3. **Nothing** — they live with the pain

If "nothing" — the pain isn't real enough. Be very skeptical of "everyone has this problem".

### Q4 — Why pick us over the workaround / competitor?

The differentiation kill test (from bequite-researcher §11):

Acceptable:
- Concrete capability they lack
- 10x cheaper or faster (quantified)
- Niche fit (specific persona)
- Regional/language fit

Unacceptable:
- "Better UX"
- "Modern stack"
- "AI-powered"
- "Easier" (without quantification)

### Q5 — How do you know it worked?

The north-star metric. ONE number that tells you v1 shipped successfully.

Examples:
- ✓ "50 paid signups in the first 30 days"
- ✓ "Users come back 3 days per week on average"
- ✓ "Time-to-first-value < 5 minutes"
- ✗ "Lots of users love it" (not measurable)
- ✗ "Strong engagement" (vague)

---

## MVP scoping (cut ruthlessly)

The MVP test for every feature:
- **Does removing it kill the product?** No → cut for v1
- **Does it serve the JTBD directly?** No → cut
- **Can the user work around its absence for a week?** Yes → cut, ship later

Common scope-creep traps:
- Admin panel (always cut — use the DB directly for v1)
- Email notifications (cut unless central to JTBD)
- Bulk import / export (cut unless central)
- API for third-parties (cut for solo founders)
- Multi-tenancy (cut unless paid customer demands it)
- Roles / permissions (often cut — "owner only" is fine for v1)

Things you cannot cut:
- The core JTBD path (sign-up → first value)
- Payment if you're selling
- Auth (just use the simplest option — magic link or social)
- Basic error states (broken empty page = canceled customer)

---

## Pricing assumptions (lock them early)

Don't ship without a plan for pricing, even if v1 is free.

The basic table:
- **Free tier** — what do they get?
- **Paid tier(s)** — price, what unlocks?
- **Enterprise** — call us (or not yet)

Verify against:
- 3-5 competitor pricing pages (WebFetch)
- The persona's budget (what would they pay for the workaround?)

Pricing red flags:
- Free forever with no path to revenue — flag for user
- Enterprise-only pricing — limits adoption
- Pricing > 10x cheaper than competitors — verify cost structure can sustain

---

## Scope-creep defense

Mid-build, the user says "while we're at it, can we add X?"

The pushback protocol:
1. Does X serve the v1 JTBD? If no → "Let's add to v2 backlog."
2. Does X delay shipping v1 by > 1 week? If yes → "Cut for v1, add to v2."
3. Does X violate locked SCOPE.md? If yes → "Update SCOPE.md first; otherwise this is scope creep."

Write the answer to OPEN_QUESTIONS.md as a v2 candidate. Move on.

---

## Differentiation framework

For each feature, ask: **why us, not them?**

Categories:
1. **Speed** — we ship X workflow in 1 click; they need 5 clicks
2. **Price** — we cost $0; they cost $20/mo
3. **Niche fit** — we target solo founders; they target enterprises
4. **Region** — we ship in Arabic + Egyptian dialect; they're English-only
5. **Specificity** — we do ONE thing well; they're a 50-feature suite

If the answer is "we have AI" — that's not differentiation in 2026. Push harder.

---

## North-star metric per phase

| Phase | Metric | Threshold |
|---|---|---|
| Launch | Sign-ups in 7 days | ≥ 20 |
| Early traction | Day-7 retention | ≥ 30% |
| Validated | Paid conversions | ≥ 5% of signups |
| Growth | MoM revenue growth | ≥ 10% |

Don't write a v1 plan without a launch-phase metric.

---

## Activate on these commands

- `/bq-clarify` — generate the 3-5 questions that surface JTBD / persona / differentiation
- `/bq-scope` — apply MVP cuts, surface scope creep
- `/bq-plan` — confirm differentiation + metric before locking the plan
- `/bq-audit` (for existing projects) — assess product-market-fit signals
- `/bq-handoff` — write the "what is this product" section

---

## Common failure modes

- User describes a "platform" → ask "what's the FIRST thing a user does in this platform?" Focus on that.
- User wants "everything customizable" → premature. Build the opinionated v1.
- User says "users will love it" → ask "which user? What will they DO with it that they can't do today?"
- User can't articulate the JTBD → pause; brainstorm with `product-management:brainstorm` skill if available; do not advance to plan.

---

## What this skill does NOT do

- Marketing copy (use brand-voice plugin)
- Detailed financial modeling (out of scope; recommend a CFO advisor for serious money)
- Legal / regulatory analysis (recommend a lawyer for fintech/healthcare/gov)
- A/B test design (use a dedicated experimentation tool)

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
