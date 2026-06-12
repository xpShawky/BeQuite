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

## Course Source Intake (scanned/OCR PDF handling — alpha.22 stabilization)

Source PDFs may be: text PDFs · scanned/image-based · mixed Arabic/English · OCR-messy · badly ordered · RTL · slides-exported-as-PDF · screenshots-inside-PDF. Intake rules (run before any curriculum work when source files exist):

1. **Probe extractability** — attempt text extraction first; classify each page: `text` / `image-only` / `mixed`.
2. Text-extractable → use direct extraction (no OCR).
3. Scanned/image-based → mark **OCR REQUIRED**; do not silently skip pages.
4. OCR runs **only with tools already present and safe** in the environment (tool-neutral; nothing installed by default).
5. No OCR available → ask the user for extracted text, or offer an explicit OCR pass — never guess page contents.
6. **Preserve page order** even when text streams are jumbled.
7. Reconstruct headings/sections from layout + typography cues.
8. Clean OCR noise (broken words, repeated headers/footers, page numbers in text flow).
9. Detect Arabic/RTL direction problems (reversed runs, broken bidi) — localization-rtl skill attaches automatically.
10. Build a **source map**: page · section · extracted-text summary · extraction confidence.
11. **Never invent missing content.** Gaps are recorded as gaps.
12. Low-confidence OCR sections are marked **NEEDS REVIEW** and excluded from strict-fidelity output until the user confirms.

**Output:** `.bequite/courses/SOURCE_INTAKE_REPORT.md` (the source map + per-page classification + NEEDS REVIEW list). Course outputs are now **15 files** (14 + this report, written whenever source files are ingested). Reminder: any course-building PDF is ONE reference — the engine still researches global best practices when appropriate.
