---
description: Course Engine (C5). Build a complete course from idea to launch — validation, learner persona, promise, offer, curriculum, lessons, exercises, quizzes, slide briefs, recording plan, marketing, launch. Handles YouTube/crash/full/live/recorded/hybrid/academic/paid/free and Arabic/MENA courses. Curriculum before slides, always.
---

# /bq-course — the Course Engine (C5)

Full spec: `docs/specs/COURSE_ENGINE.md`. Follows the 12-step execution contract including skill routing, Confidence Forecast, and the step-12 router block. Reference policy: the user's course-building PDF framework is ONE reference (12 topics: gap validation → persona → offer → lean curriculum → practical tasks → delivery → branding → content engine → funnel → objections → gamification → MVP launch) alongside runtime research on cohort courses, YouTube education, Udemy/Coursera structure, adult learning, completion psychology, and Arabic/MENA delivery.

## Syntax

```
/bq-course "<course idea>"                      ← full engine
/bq-course validate "<idea>"                    ← market gap + persona + promise only
/bq-course curriculum "<validated idea>"        ← curriculum + lessons + assessment
/bq-course launch "<built course>"              ← marketing angle + launch plan
```

## Preconditions / gates

`BEQUITE_INITIALIZED`. Paid-course pricing/funnel work pauses at the normal hard gates (no paid-service activation, no publishing).

## Steps (after contract steps 1–7)

1. **High-value questions only** (skip anything already known from memory/request): learner? transformation? pain? free/paid? crash/full? practical/theoretical? platform? language? duration? source materials? strict fidelity? output now?
2. **Validation** — MARKET_GAP (researched, cited) + LEARNER_PERSONA + COURSE_PROMISE (the transformation, falsifiable) + OFFER (paid courses: pricing logic, objections, funnel sketch).
3. **Curriculum architecture** — CURRICULUM_MAP (modules → outcomes), then LESSON_PLAN: every lesson = outcome + practical task + proof-of-learning. EXERCISES + QUIZZES designed for completion psychology (early wins, momentum loops; gamification only where it serves learning).
4. **Production** — SLIDE_BRIEFS (handoff to C1 `/bq-presentation`) + RECORDING_PLAN (per delivery model). Strict mode: full source fidelity, Writing-DNA ethics (no fabricated citations, no academic dishonesty).
5. **Go-to-market** — MARKETING_ANGLE + LAUNCH_PLAN (MVP launch first). SOURCE_FIDELITY records what came from which source.

## Writes

`.bequite/courses/{COURSE_BRIEF,MARKET_GAP,LEARNER_PERSONA,COURSE_PROMISE,OFFER,CURRICULUM_MAP,LESSON_PLAN,EXERCISES,QUIZZES,SLIDE_BRIEFS,RECORDING_PLAN,MARKETING_ANGLE,LAUNCH_PLAN,SOURCE_FIDELITY}.md` (per scope) + AGENT_LOG + LAST_RUN.

## Skill routing (auto)

researcher (always) · writing-dna (scripts) · presentation-builder (slides) · localization-rtl (Arabic/MENA) · product-strategist (paid) · anti-hallucination (academic/scientific/technical) · frontend-design-system (HTML deck / course site). Source docs exist ⇒ recommend C4 `/bq-knowledge build` first.

## Next Command Recommendations (typical)

Required next after curriculum: **C1 `/bq-presentation`** when slides are needed — can auto-run: yes. Set: C4 knowledge build (docs exist) · C2 writing-dna (narration voice) · W4.2 `release announce` for launch content (publishing = hard human gate). Do not run yet: slides before CURRICULUM_MAP approval — slides-first course building is the failure mode this engine exists to prevent.
