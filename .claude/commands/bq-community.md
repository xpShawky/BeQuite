---
description: Community Pack (C15). Plan a community for a course, brand, content creator, or product launch — platform decision, member persona, onboarding flow, content/event calendar, engagement loops, moderation rules, roles/permissions, growth plan, health metrics, risks. Practical structure, not motivational fluff. Serves /bq-course, /bq-release launches, and /bq-brand-kit.
---

# /bq-community — community strategy & structure (C15)

Full spec: `docs/specs/COMMUNITY_PACK.md`. Follows the 12-step contract. Skills: product-strategist + writing-dna (tone/prompts) + localization-rtl (Arabic/MENA groups). Shared capability used by course/launch/brand workflows.

## Syntax

```
/bq-community "<who it's for + purpose>"
```
Examples: course cohort accountability · content-creator audience · product-launch community · brand membership · learner study group.

## Steps (after contract steps 1–7)

1. **Strategy + member** — `COMMUNITY_STRATEGY.md` (why it exists, the one job it does) + `MEMBER_PERSONA.md`.
2. **Platform** — `PLATFORM_DECISION.md`: Discord / Telegram / WhatsApp / Facebook group / forum / website / course-platform community — chosen by where the members already are + moderation needs + MENA habits (WhatsApp-first is common). Trade-offs stated.
3. **Onboarding + rhythm** — `ONBOARDING_FLOW.md` · `CONTENT_AND_EVENT_CALENDAR.md` (weekly rhythm, prompts, events) · `ENGAGEMENT_LOOPS.md` (what brings members back; accountability).
4. **Safety + roles** — `MODERATION_RULES.md` (spam prevention, conduct) · `ROLES_AND_PERMISSIONS.md` (who can do what) · `RISKS.md` (spam, toxicity, dead-community, over-moderation).
5. **Growth + health** — `GROWTH_PLAN.md` + community health metrics (active members, not vanity counts) + `NEXT_STEPS.md`.

## Writes

`.bequite/community/{COMMUNITY_STRATEGY,MEMBER_PERSONA,PLATFORM_DECISION,ONBOARDING_FLOW,CONTENT_AND_EVENT_CALENDAR,ENGAGEMENT_LOOPS,MODERATION_RULES,ROLES_AND_PERMISSIONS,GROWTH_PLAN,RISKS,NEXT_STEPS}.md` (first run) + AGENT_LOG + LAST_RUN.

## Next Command Recommendations (typical)

Required next: depends on parent — after C5 course → community supports the cohort; after a launch → W4.2 `/bq-release`. Set: C2 `/bq-writing-dna` (prompts/tone) · C12 `/bq-automation` (onboarding/reminder bot — bot safety applies) · C17 `/bq-start`. Do not run yet: building a custom community platform when an existing one (Discord/Telegram/WhatsApp) fits — don't over-engineer.
