---
name: bequite-human-taste
description: Use before producing any creative output (writing, a web page, a film, a post, an image) and before delivering it. Makes the work start from studied human references and pass the human test, so it does not read as machine-made. Owns the REFERENCES_STUDIED and HUMAN_TEST_PASSED gates.
last_verified: 2026-11-21
sources:
  - https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing  # tells by family, ineffective indicators, signs of human writing (read 2026-11-21)
  - https://github.com/blader/humanizer  # removing patterns is half the job; match the sample's own rates (read 2026-11-21)
  - https://arxiv.org/abs/2505.23276  # Arabic machine text: repetition, length, detection weakest on social media (read 2026-11-21)
  - https://ai.google.dev/gemini-api/docs/video-understanding  # 1 FPS sampling: why video references are checked on frames (read 2026-11-21)
  - .claude/bequite/docs/architecture/REFERENCE_FIRST.md  # the doctrine this skill enforces
  - .claude/skills/bequite-writing-dna/references/tells-ar.md  # Arabic tells measured on 47 human vs 12 model posts (2026-11-21)
---

# bequite-human-taste

This file is the model for every v1 skill: a trigger-style description, a dated source list, a short procedure, one worked example, a quality gate, and nothing the agent already knows.

## When to use

- Any command that produces something a person will read, watch or look at: `/bq-content`, `/bq-motion`, `/bq-presentation`, `/bq-writing-dna`, `/bq-uiux-variants`, `/bq-live-edit`, and frontend work in `/bq-feature`.
- Before delivery of that output.

Not for: code with no visible surface, logs, internal notes.

## Procedure

1. **Check the gate.** Open `work/<id>/gates.md`. If `REFERENCES_STUDIED` is not ticked, do steps 2 to 4 before anything else.
2. **Collect.** Use the owner's references if given. Otherwise pick sources from the table in `REFERENCE_FIRST.md` section 3 for the domain, open them in the browser, and gather 3 to 10 (30 to 50 posts for a voice). Show the owner the set in one message and wait for a yes or a swap.
3. **Measure.** Write `work/<id>/references.md`: one block per reference with numbers and facts only. For a live site, read the real values from the page (computed font family and size, colours, the scripts that drive the motion). For a video, use `bequite-video-intel` (route G or the ladder; check what you use on frames). For a voice, `bequite-writing-dna` (`voice_stats.py`).
4. **Extract.** Write the DNA: rules, one example per rule, and the never-list. Tick `REFERENCES_STUDIED`.
5. **Produce** with the DNA open. Write down any deliberate deviation.
6. **Test** (`REFERENCE_FIRST.md` section 5): side by side, tell sweep, blind pick for writing, phone check for visuals. Record each step in `evidence.md`.
7. **Deliver** to the owner with the side-by-side. Tick `HUMAN_TEST_PASSED` only after the owner's verdict. Turn each correction into a DNA rule.

## Worked example

Task: "Posts for a football fan page, like the big Egyptian ones."

- Collect: 40 posts from two pages the owner names, copied with date and reaction counts.
- Measure: median post 14 words; no full stops; one emoji in 60% of posts, at the end; colloquial Egyptian throughout; 7 of the top 10 posts tease the rival club in the first five words.
- DNA: "Open on the tease." Example: one real post. Never-list: formal Arabic, hashtags, more than two lines.
- Produce 10 posts. Tell sweep finds two with a comma after every clause; rewritten.
- Blind pick (`bequite-writing-dna/references/blind-pick.md`): a fresh subagent marks one of three generated posts. Its reason ("too balanced") becomes a rule.
- Owner: approves 8, rewrites 2. The two rewrites are added to the exemplars.

## Quality gate

- `references.md` holds numbers, not adjectives. A block with no number is redone.
- The side-by-side exists as a file or an image, not as a sentence.
- No claim that the output "looks human". The evidence is the test record and the owner's verdict.

## Boundaries

Learn a manner; never copy posts, pose as a real page or person, or promise to pass AI detectors. Collected posts and screenshots stay in the work folder and are never committed.
