---
description: Offer Engine (C11). Turn a skill, service, automation, product idea, course idea, niche, or pain point into a sellable productized offer — target client, pain/outcome, deliverables + exclusions, pricing tiers, safe guarantee, onboarding questions, outreach message, demo idea, proof checklist, proposal angle. Honest by contract — no invented demand, no fake income claims, no overpromising.
---

# /bq-offer — idea → sellable productized offer (C11)

Full spec: `docs/specs/OFFER_ENGINE.md`. Follows the 12-step execution contract (skill routing, Confidence Forecast, router block). The monetization connector: pain-radar finds problems, make-money finds tracks, **offer packages the standing product**, proposal pitches it per-client.

## Syntax

```
/bq-offer "<skill / service / automation / product / course idea / niche / pain point>"
/bq-offer "<idea>" lang=ar|en        ← output language (defaults to the request's language)
/bq-offer refine "<which part>"      ← iterate on an existing offer pack
```

Examples: `/bq-offer "AI automation for restaurants"` · `/bq-offer "Arabic course about AI automation for small business owners"` · `/bq-offer "Website audit service for clinics"` · `/bq-offer "Workflow automation package for ecommerce stores"`.

## Preconditions / gates

`BEQUITE_INITIALIZED`. **Publishing/sending the offer anywhere is user-performed** — BeQuite drafts.

## Honesty rules (refusal-grade)

**No overpromising. No invented market demand** — demand claims trace to pain-radar output, user-provided facts, or live research (researcher skill), else marked `UNVERIFIED ASSUMPTION`. **No fake income claims** ("make $10k/month" without evidence = banned). **Offer promise ≠ guarantee** — the promise states the outcome pursued; the guarantee states only what the seller can actually control (refund terms, redo work, response times) — never guarantee client results you can't control. **No legal advice** (guarantee/contract wording flagged "have a professional review this"). **No claimed experience** absent from memory or user input. Every section carries confidence; proof gaps are listed, not hidden.

## Steps (after contract steps 1–7)

1. **Intake.** If the niche/idea is vague: ask 3–5 high-value questions (who is it for? what do they currently pay for or struggle with? your deliverable capacity? price range comfort? proof you already have?) — OR produce a draft with every assumption explicitly marked. Pull prior context if present: `.bequite/pain-radar/` (verified pains), `.bequite/money/` (profile), `.bequite/proposals/` (past pitches), `/bq-release proof` packs (evidence).
2. **Target + pain.** `TARGET_CLIENT.md` (specific segment, not "small businesses" — *which* ones, where, with what buying power) + `PAIN_AND_OUTCOME.md` (the painful specific problem; the measurable outcome the offer pursues; what happens if they don't solve it). Reference-A discipline from the Course Engine applies: one painful specific problem beats a broad theme.
3. **Package.** `DELIVERABLES.md` (concrete included items + **explicit exclusions** — scope boundaries are part of the product) + `OFFER.md` (the assembled offer: name, one-line promise, who/pain/outcome, package, differentiator — the 5-element message: promise + price + bonus + guarantee + differentiator).
4. **Price.** `PRICING_TIERS.md` — 2–3 tiers with trade-offs (what each adds/drops), anchoring logic, fixed-vs-retainer recommendation, local purchasing-power note for MENA markets. Pricing confidence stated; product-strategist pricing extension applies.
5. **De-risk.** `GUARANTEE_AND_RISK_REVERSAL.md` — a guarantee the seller can honor (conditional refund tied to *applied* effort, redo clause, response-time SLA), clearly separated from the promise; risk to the seller analyzed too.
6. **Operationalize.** `ONBOARDING_QUESTIONS.md` (what to ask a buyer before starting — feeds `/bq-scope intake`) · `OUTREACH_MESSAGE.md` (hook → pain → offer → CTA; in the user's Writing DNA voice if a profile exists) · `DEMO_IDEA.md` (what to show in 5 minutes that proves capability) · `PROOF_CHECKLIST.md` (what evidence exists vs needed — feeds `/bq-release proof`) · `PROPOSAL_ANGLE.md` (how C8 should pitch this per-client).
7. **Route.** `NEXT_STEPS.md` + the step-12 router block.

## Writes

`.bequite/offers/{OFFER,TARGET_CLIENT,PAIN_AND_OUTCOME,DELIVERABLES,PRICING_TIERS,GUARANTEE_AND_RISK_REVERSAL,ONBOARDING_QUESTIONS,OUTREACH_MESSAGE,DEMO_IDEA,PROOF_CHECKLIST,PROPOSAL_ANGLE,NEXT_STEPS}.md` (one set per offer; created on first run) + AGENT_LOG + LAST_RUN.

## Language rule

Output language follows the user's request: Arabic asked ⇒ Arabic offer pack (localization-rtl auto-attaches; MENA payment/pricing context applies); English asked ⇒ English. Arabic source material + English request ⇒ translate concepts, never awkward literal phrases.

## Skill routing (auto)

product-strategist (offer/pricing) · writing-dna (voice) · make-money (opportunity verification) · anti-hallucination (claims discipline) · researcher (when market claims are made) · localization-rtl (Arabic/MENA/RTL) · presentation-builder (pitch deck requested) · frontend-design-system (landing page requested).

## Next Command Recommendations (typical)

- No niche yet → **do not run this**; Required: C6 `/bq-pain-radar` or C10 `/bq-make-money` first.
- Offer built, wants a client pitch → Required next: **C8 `/bq-proposal`** (uses PROPOSAL_ANGLE) — can auto-run: yes.
- Wants marketing assets → C2 `/bq-writing-dna repurpose` · W4.2 `/bq-release announce` (publishing = hard human gate) · W2.3 `/bq-feature landing`.
- Wants the sales process → W1.3 `/bq-scope intake` → C8 proposal → W4.2 `/bq-release proof`.
- Do not run yet: building the offered service/product before one real buyer signal — MVP-first discipline (Reference A stage 11) applies to offers too.
