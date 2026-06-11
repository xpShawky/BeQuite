---
name: bequite-writing-dna
description: Writing DNA discipline — extract an explicit style profile (genre, audience, tone, rhythm, vocabulary, citation style, forbidden patterns) from user samples, then generate or rewrite content constrained by it. Human-quality, source-faithful, ethical. Invoked by /bq-writing-dna; consumed by /bq-presentation speaker notes.
allowed-tools: Read, Glob, Grep, Edit, Write, WebFetch, WebSearch
---

# bequite-writing-dna — voice as an explicit artifact

## Purpose

Generic AI text is median text. This skill replaces "write like a human" prompting with the pattern that actually works: **corpus analysis → explicit profile → constrained generation → review against profile**. The profile (`WRITING_DNA.md`) is a durable artifact — built once, reused everywhere, corrected over time.

## Ethical boundary (binding)

Improve clarity / rhythm / specificity / fidelity / voice. **Never:** fabricate sources, invent citations, assist academic dishonesty, promise AI-detector evasion. When sources are strict, no unsupported claims — `UNVERIFIED:` marks gaps honestly.

## The WRITING_DNA.md profile shape

| Section | Captures | Evidence rule |
|---|---|---|
| Genre + audience | what kind of writing, for whom, assumed knowledge | from intake |
| Tone register | formal↔casual, warm↔neutral, confident↔hedged — as a POSITION, not adjectives | quote 2+ sample lines per claim |
| Sentence rhythm | length distribution (short/medium/long %), fragment tolerance, question use, opener variety | measured from samples |
| Paragraph architecture | typical length, topic-sentence habit, transition style | measured |
| Vocabulary | level, signature words/phrases, words this voice NEVER uses | listed with sample evidence |
| Citation style | APA/MLA/Chicago/Vancouver/none + in-text vs footnote habits | academic only |
| Structural habits | headings? lists? anecdote openers? callback endings? | from samples |
| Forbidden patterns | generic-AI tells + user bans + anti-patterns this voice never produces | → FORBIDDEN_PATTERNS.md |

**Profile rule:** every inference cites sample evidence ("samples average 14-word sentences with 30% under 8 words — see STYLE_SAMPLES §2"). No evidence → mark `[Provisional]`.

## Default forbidden patterns (apply to every profile)

"delve / tapestry / landscape (metaphorical) / navigate (metaphorical)" · "in today's fast-paced world" · "it's important to note that" · furthermore/moreover/additionally chains · uniform sentence lengths (the metronome tell) · triple-adjective stacks · hedging stacks ("could potentially perhaps") · every-paragraph-summarizes endings · rhetorical-question openers used more than once · exclamation marks in formal registers · em-dash density >1 per ~80 words

## Generation discipline

1. Load DNA before drafting; the profile is a CONSTRAINT SET, not inspiration
2. Strict mode → Pattern 4 (PROMPT_PATTERNS.md): claims trace to sources, no additions
3. Draft → self-review against the profile table row by row → fix → grep output for forbidden patterns → only then deliver
4. Rewrites preserve meaning exactly; flag any place where applying the voice would change a claim
5. Multiple profiles supported: name them (`WRITING_DNA.md` holds the active one; archived profiles at `WRITING_DNA-<name>.md`)

## Genre quick-guides

- **Academic:** citation fidelity is the prime constraint; hedge only where evidence hedges; methodology = precise + reproducible; discussion = claims ranked by evidence strength. Help users improve THEIR work — never produce work to be misrepresented as theirs.
- **Brand/marketing:** voice consistency beats cleverness; one idea per piece; CTA matches funnel stage.
- **Lecture/teaching:** spoken rhythm (shorter sentences than prose), signposting, one concept per beat — pairs with `/bq-presentation` speaker notes.
- **Scripts (YouTube):** hook in first 2 lines; written for the EAR; pattern interrupts every ~45s of speech.
- **Email:** subject = the ask; first line = context; ≤150 words unless justified.

## When NOT to use this skill

- Repo conventions for code/docs (PROJECT_DNA) · slide visual design (presentation-builder) · one-line tweaks · any detector-evasion or dishonesty framing (refuse)

## Quality gate

- [ ] WRITING_DNA inferences carry sample evidence (or `[Provisional]`)
- [ ] Output greps clean against FORBIDDEN_PATTERNS.md
- [ ] Strict mode: zero invented citations; `UNVERIFIED:` marks present where sources were silent
- [ ] OUTPUT_REVIEW.md written for non-trivial pieces
- [ ] No banned weasel words in completion claims; memory writeback done (LAST_RUN / AGENT_LOG)

## Common mistakes

Adjective-soup profiles ("witty yet professional") instead of measured constraints · applying blog DNA to academic work because it's the active profile (genre-check first) · "humanizing" by adding errors (the goal is QUALITY, not noise) · letting the rewrite drift meaning · building the profile from ONE sample (ask for 3+ or mark Provisional)

## Failure handling

No samples → provisional profile from intake, labeled · samples in conflicting voices → ask which voice wins, or build named profiles · request crosses ethics line → refuse that part + offer the legitimate adjacent help · profile contradicts an explicit user instruction → user instruction wins, log to WRITING_RULES
