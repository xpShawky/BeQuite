# Course Engine — `/bq-course` (C5) — alpha.22

A serious Course Engine — not an outline generator. Runs validation → persona → promise → offer → curriculum → lessons → assessment → production → marketing → launch.

## Reference policy (honesty note)

The user-supplied course-building PDF is **ONE reference among several**. **The PDF file was not accessible in the authoring session** (repo-wide search found no PDF); its framework is used via the user's summary — 12 topics: market gap validation · ideal persona · irresistible offer · lean curriculum · practical tasks · delivery model · personal branding · content engine · sales funnel · objections/closing · gamification · MVP launch. When the user attaches the actual PDF, `/bq-course` reads it directly and records fidelity in `SOURCE_FIDELITY.md`. Additional references (researched at runtime, never from memory alone): cohort-based courses, YouTube education, Udemy/Coursera structure, technical training, academic teaching, crash courses, project-based learning, adult learning principles, course marketing, completion psychology, gamification, Arabic/MENA delivery.

## Course types handled

YouTube course · crash course · full course · live / recorded / hybrid · university lecture series · technical tutorial · paid course · free lead magnet · Arabic/MENA + RTL. (Examples: BeQuite beginner YouTube course · AI automation for restaurants · chess 1200→1600 in a month · pharmacology lecture series.)

## High-value questions ONLY (ask what's missing, skip the obvious)

learner? · transformation? · pain solved? · free or paid? · crash or full? · practical or theoretical? · platform? · language? · duration? · existing source materials? · strict source fidelity? · output needed now?

## Outputs — `.bequite/courses/`

COURSE_BRIEF · MARKET_GAP · LEARNER_PERSONA · COURSE_PROMISE · OFFER · CURRICULUM_MAP · LESSON_PLAN · EXERCISES · QUIZZES · SLIDE_BRIEFS · RECORDING_PLAN · MARKETING_ANGLE · LAUNCH_PLAN · SOURCE_FIDELITY (created per scope on first run).

## Auto-selected skills (Skill Router)

researcher (always) · writing-dna (scripts/narration) · presentation-builder (slides → C1) · localization-rtl (Arabic/MENA/RTL signals) · product-strategist (paid course) · anti-hallucination (academic/scientific/technical content) · frontend-design-system (HTML deck or course site requested). Knowledge: run `C4 /bq-knowledge build` first when source documents exist.

## Quality rules

Curriculum before slides, always. Every lesson states: outcome, practical task, proof of learning. Completion psychology designed in (quick wins early, momentum loops, gamification where it serves learning — not points-for-points). Paid courses get offer + objections + funnel sections; free courses get lead-magnet positioning. Strict mode = full source fidelity (no invented facts, citations preserved); ethics rules of Writing DNA apply (no fabricated citations, no academic dishonesty).
