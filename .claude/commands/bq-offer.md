---
description: "The business pack's one command for selling work honestly. Modes - offer (default: a productized offer pack), proposal (a tailored proposal for one client or job post), local-business (a minimum digital system for an offline business), pain-radar (public pain in a niche turned into opportunities), business-system / agency / service-business. No invented demand, no income promises, no overpromising."
---

# /bq-offer: from a need to an honest, sellable offer

<!-- bq:contract -->
> **Every run follows the contract** (`.claude/bequite/docs/architecture/COMMAND_EXECUTION_CONTRACT.md`):
> 1. **Up to date:** first run `bash .claude/bequite/bin/bq-update.sh` (hourly; it updates BeQuite when a newer version is published, backs up first, never touches `.bequite/` memory, never blocks) and say its one line.
> 2. **Skills first:** announce the `Skill Selection:` block before any plan, edit or tool call for the task.
> 3. **Resolve the work:** read `.bequite/ACTIVE.md`; use `.bequite/work/<id>/`, or create the next work folder if this is new work (`/bq-work`).
> 4. **Gates:** project gates in `.bequite/state/WORKFLOW_GATES.md`, work gates in `work/<id>/gates.md`. Refuse and name the missing gate.
> 5. **Plan first:** non-trivial work gets a plan the user approves before output. Hard human gates always wait for a yes.
> 6. **Evidence:** every check goes to `work/<id>/evidence.md` (command + exit code + output) or is marked `UNVERIFIED:`.
> 7. **Write back:** `work/<id>/log.md`, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, and `.bequite/state/MISTAKE_MEMORY.md` when a lesson surfaced.
> 8. **Finish** with the Next Command Recommendations block.
<!-- /bq:contract -->

The monetization chain in one place: `pain-radar` finds problems, `/bq-make-money` finds earning tracks, `offer` packages the standing product, `proposal` pitches it to one client, `/bq-productize` turns finished work into an asset. Each mode's full spec lives in `.claude/bequite/docs/specs/`.

## Syntax and modes

```
/bq-offer "<skill / service / product / course idea / niche / pain>" [lang=ar|en]   offer pack (default)
/bq-offer refine "<which part>"                                                    iterate on an offer pack
/bq-offer proposal "<job post / RFP text or path>" [pricing=fixed|milestone|retainer] [tone=<voice>]
/bq-offer local-business "<business type + place>"
/bq-offer pain-radar "<niche>" [country=<market>] [language=<lang>]
/bq-offer pain-radar from-exports "<path to exports or screenshots the user provides>"
/bq-offer business-system | agency | service-business "<idea>"
```

| Mode | Produces | Spec | Writes |
|---|---|---|---|
| offer (default), refine | target client, pain and outcome, deliverables with exclusions, 2-3 price tiers, a guarantee the seller controls, onboarding questions, outreach message, demo idea, proof checklist, proposal angle | `OFFER_ENGINE.md` | `.bequite/offers/` |
| proposal | a proposal for one client: their problem in their words, real proof from memory, milestones, pricing options, a confidence forecast | `PROPOSAL_BUILDER.md` | `.bequite/proposals/` |
| local-business | business profile, pain map, digital-opportunity map, the minimum system (booking, WhatsApp/Telegram flows, listings), a 30-day rollout | `LOCAL_BUSINESS.md` | `.bequite/local-business/` |
| pain-radar | public pains with links, grouped and scored, turned into MVP, service, automation, bot and course ideas, each with source and confidence | `PAIN_RADAR.md` | `.bequite/pain-radar/` |
| business-system / agency / service-business | the offer chain for a whole service business: business model, offer stack, delivery system, client acquisition, proof engine, operations, risks | `OFFER_ENGINE.md` (business-system section) | `.bequite/offers/` |

## Honesty rules (refusal-grade, every mode)

- No invented demand: a demand claim traces to pain-radar output, the user's facts or live research, else it is marked `UNVERIFIED ASSUMPTION`.
- No income claims without evidence; never guaranteed revenue. The promise names the outcome pursued; the guarantee covers only what the seller controls (refund terms, redo, response times).
- No claimed experience that is not in memory or the user's input; proof gaps are listed, not hidden.
- No legal advice: contract or guarantee wording is flagged for a professional.
- pain-radar reads public sources only, politely, and never logs in or scrapes behind a login; user-provided exports are the route for private groups.
- Sending, posting or submitting anything is the user's act; BeQuite drafts.

## Steps (any mode)

1. **Intake.** Vague request: ask three to five questions (who it is for, what they pay for now, delivery capacity, price comfort, proof already owned) or draft with every assumption marked. Read prior context: `.bequite/pain-radar/`, `.bequite/money/`, `.bequite/offers/`, `.bequite/proposals/`, proof packs.
2. **Run the mode's spec** step by step; one specific painful problem beats a broad theme.
3. **Price with reasons** (tiers, anchoring, fixed vs retainer, local purchasing power for MENA markets) and state the pricing confidence.
4. **Check every claim** (anti-hallucination) and run the human-taste tell sweep on any text a person will read.
5. **Route** with the Next Command Recommendations block.

## Skills

product-strategist (offer, price) · make-money (verification, payout channels) · writing-dna and human-taste (any outward text) · researcher (market claims) · anti-hallucination · localization-rtl (Arabic and MENA) · automation (local-business systems, bots) · presentation-builder (a pitch deck) · frontend-design-system (a landing page).

## Language

Output follows the request: Arabic asked means an Arabic pack (localization-rtl attaches, MENA pricing and payment context applies); English asked means English.

## Next Command Recommendations (typical)

- No niche yet: run `/bq-offer pain-radar` or `/bq-make-money` first.
- Offer built and a client in view: `/bq-offer proposal`.
- Finished work to sell: `/bq-productize`.
- Marketing assets: `/bq-content script` (posts) · `/bq-release announce` (publishing is a hard human gate).
- Do not build the offered product before one real buyer signal (MVP first).
