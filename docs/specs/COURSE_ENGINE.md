# Course Engine — `/bq-course` (C5) — alpha.22

A serious Course Engine — not an outline generator. Runs validation → persona → promise → offer → curriculum → lessons → assessment → production → marketing → launch.

## Reference policy

The course-building PDF ("Executive Task List for Building and Selling Online Courses" — *Your First Million* program, Arabic, 5 pages) is **Reference A — verified directly from the source on 2026-06-12** (text-extractable; no OCR needed; full concept extraction at `.bequite/courses/COURSE_PDF_REFERENCE_NOTES.md`). Its 11-stage framework: market-gap validation (one painful specific "million problem"; 5-competitor offer/price analysis) → ideal persona from pain not guesses (motivations + pre-existing objections + the unified client sentence) → irresistible offer (measurable core promise · bonuses · risk-reversal guarantee · 5-element sales message tested on 5 real people) → lean curriculum (milestones · zero filler · mandatory practical task per module) → delivery model (recorded/live/hybrid + learner-easiest platform with local payment methods) → personal branding (brand statement + tone of voice) → content engine (psychology-anchored; hook→solution→CTA; publish 3 real pieces) → sales funnel (mapped flow + lead magnet) → smart selling (objection scripts + 3 real/simulated conversations) → gamification + micro-chunking (5–10-min lessons; quick wins) → MVP launch (small live cohort first; recordings become v1).

**Reference A is one reference, not the only authority.** The engine augments it at runtime with established practice: outcome-based curriculum, adult learning, project- and cohort-based learning, microlearning, completion psychology, learner transformation, assessment design, case studies, feedback loops, community/accountability, proof/testimonials, launch strategy, positioning, YouTube-free vs paid differences, technical-course vs academic-lecture differences, Arabic/MENA delivery. Outputs must read like a course strategist built them — generic AI filler fails the quality gate.

**Language rule:** framework concepts are documented in English; **course output language follows the user's request** — Arabic course asked = Arabic outputs, English asked = English. The source language of any reference never forces the output language. (localization-rtl auto-attaches for Arabic/MENA outputs.)

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
