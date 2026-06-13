---
description: Local Business Digitizer (C13). Turn an offline/low-tech local business (restaurant, clinic, pharmacy, store, teacher) into a practical minimum digital system — business profile, pain map, digital-opportunity map, minimum viable digital system, automation ideas, local-market notes, implementation roadmap, compliance, offer angle. MENA/Arabic-aware (WhatsApp, cash-vs-online, phone-first, low-tech staff). Practical, not enterprise.
---

# /bq-local-business — offline business → practical digital system (C13)

Full spec: `docs/specs/LOCAL_BUSINESS.md`. Follows the 12-step contract. Skills: automation-engineer + product-strategist + localization-rtl (MENA) + make-money (offer angle). Reuses C6 pain-radar + C11 offer + C12 automation rather than duplicating them.

## Syntax

```
/bq-local-business "<business type + location/context>"
```
Examples: restaurant (menu · WhatsApp ordering · booking · reminders · reviews) · clinic (booking · intake · reminders · follow-up) · pharmacy (inventory · orders · delivery · WhatsApp) · furniture store (catalog · offers · lead capture) · course teacher (landing · enrollment · community · payments · delivery).

## Steps (after contract steps 1–7)

1. **Profile** — `BUSINESS_PROFILE.md`: what they sell, how they operate today, staff tech level, current tools (often just phone + WhatsApp + paper), budget reality.
2. **Pain + opportunity** — `PAIN_MAP.md` (where they lose time/money/customers) → `DIGITAL_OPPORTUNITY_MAP.md` (ranked digital fixes by impact/effort).
3. **Minimum system** — `MINIMUM_DIGITAL_SYSTEM.md`: the smallest set that delivers value (often: simple menu/catalog page + WhatsApp ordering + booking/reminders) — NOT an enterprise build. `AUTOMATION_IDEAS.md` (reminders, follow-ups, order routing — tool-neutral, official-API-first).
4. **Local context** — `LOCAL_MARKET_NOTES.md`: WhatsApp behavior, cash-vs-online payments, Instagram/Facebook habits, phone-first workflows, Arabic/RTL, trust/proof needs, simple admin UX for low-tech staff.
5. **Plan + risk + offer** — `IMPLEMENTATION_ROADMAP.md` (phased) · `RISK_AND_COMPLIANCE.md` (data/privacy, PDPL/MENA where relevant) · `OFFER_ANGLE.md` (how to sell this as a service — feeds C11) · `NEXT_STEPS.md`.

## Writes

`.bequite/local-business/{BUSINESS_PROFILE,PAIN_MAP,DIGITAL_OPPORTUNITY_MAP,MINIMUM_DIGITAL_SYSTEM,AUTOMATION_IDEAS,LOCAL_MARKET_NOTES,IMPLEMENTATION_ROADMAP,RISK_AND_COMPLIANCE,OFFER_ANGLE,NEXT_STEPS}.md` (first run) + AGENT_LOG + LAST_RUN.

## Next Command Recommendations (typical)

Required next: **C11 `/bq-offer`** (package it as a sellable service) or **W2.3 `/bq-feature`** (build the minimum system). Set: C12 `/bq-automation` (reminders/ordering) · C3 `/bq-reference` (menu/catalog design) · W4.2 `/bq-release proof` (case study after delivery). Do not run yet: enterprise/multi-tenant build before the minimum system is validated with the owner.
