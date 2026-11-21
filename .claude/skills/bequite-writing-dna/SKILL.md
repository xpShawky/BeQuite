---
name: bequite-writing-dna
description: Use before writing or rewriting anything a person will read as someone's voice (posts, captions, scripts, emails, a page's copy, the owner's own posts), when the user asks to "write like me / like this page", and when output reads as machine-made. Learns a voice from 30-50 real samples, measures it, writes in it, and proves it with a tell sweep and a blind pick. Owns WRITING_DNA.md. Used by /bq-writing-dna, /bq-presentation speaker notes, the content studio's script step and the human-taste gate.
last_verified: 2026-11-21
sources:
  - https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing  # tells by family; word lists drift per model generation (mid-2026: shorter sentences in an 8-20 word band); "ineffective indicators"; signs of human writing (read 2026-11-21)
  - https://github.com/blader/humanizer/blob/main/SKILL.md  # 26 patterns in 6 families; structure outlasts vocabulary; match a sample's own rates, even for dashes (MIT, 71,920 stars, read 2026-11-21)
  - https://arxiv.org/abs/2505.23276  # The Arabic AI Fingerprint: LLM Arabic repeats top words more, narrower vocabulary; social-media posts 25-72% of human length; detection weakest on social media (read 2026-11-21)
  - https://arxiv.org/abs/2510.03502  # ALHD: 400K Arabic human/LLM samples, news + social + reviews, MSA and dialects; detectors fail to generalise across genres (abstract read 2026-11-21)
  - https://arxiv.org/abs/2412.11385  # Juzek & Ward, COLING 2025: 21 overused focal words; RLHF a likely cause, so word lists drift (abstract read 2026-11-21)
  - .claude/bequite/docs/architecture/REFERENCE_FIRST.md  # doctrine: collect, measure, extract, produce, human test, learn
  - references/tells-ar.md  # 47 human vs 12 default-model Arabic posts, measured 2026-11-21
---

# bequite-writing-dna

A voice is a set of measurable habits: how long, how punctuated, which dialect, which openers, what it never does. This skill learns those habits from real samples, writes inside them, and tests the result against the samples. It never "makes text sound human" by adjectives.

## When to use

- A new voice: the owner's, a client's, a genre ("Egyptian football fan pages"), a page the user names.
- Any writing in an existing voice: load `WRITING_DNA.md` first.
- A rewrite of text that reads as machine-made.

Not for: code docs (repo conventions), slide layout (`bequite-presentation-builder`), anything meant to pass as a real person or to beat AI detectors (refuse).

## Procedure

1. **Collect** 30-50 posts (or 3-5 long texts) from the named source, with date and reactions. In the user's browser only with their yes, read only. Save to `work/<id>/research/voice/<source>.json` (private, never committed). A post that looks templated (same opener, same emoji, numbered lists every time) is marked; in AI niches many top posts are machine-assisted.
2. **Measure** with `.claude/skills/bequite-writing-dna/scripts/voice_stats.py <posts.json>`: length and its spread, sentence length, punctuation per 100 words, line breaks, emoji, links, lists, calls to action, particles, dialect mix, digits, openers. Read the numbers next to the posts.
3. **Extract** `WRITING_DNA.md` with `references/voice-dna-template.md`: each rule carries its number and one real example; ten exemplar posts (the top by reactions plus typical ones); the never-list (what the samples never do).
4. **Write** with the DNA open. Match rates, not just words: if the samples break lines four times a post and use one emoji, so does the draft. A deliberate deviation is written down.
5. **Tell sweep**: `references/tells-ar.md` or `references/tells-en.md`. Fix every hit or justify it in one line. Then `voice_stats.py samples.json --vs drafts.json` (same script): any measure more than 2x off the samples is a fix.
6. **Blind pick** (`references/blind-pick.md`): 3 drafts mixed with 7 real posts; a fresh fast-model subagent with no context picks the generated ones and says why. Pass: it finds one or none. Its reasons become rules.
7. **Owner's verdict**, logged. Each correction becomes a DNA rule with its example.

## Worked example (2026-11-21, Arabic AI posts, real numbers)

- Collected 47 top Arabic AI posts on X (Nov 1-21, 100+ likes). Asked a fresh fast model for 12 posts on the same topics, no style guidance.
- Measured: the model used 2.25x the Arabic commas (5.67 vs 2.52 per 100 words) and 2.3x the full stops, no line breaks (human median 4), no emoji (humans: 49% of posts), a post-length spread 2.9x narrower, and ended 42% of posts on a call or moral (humans 17%).
- Not a tell here: formal Arabic (the model chose Egyptian colloquial on its own) and missing particles (same rate as humans).
- Rules written: break lines like the samples; commas only where the samples put them; no closing moral; open on the claim, not on a "label:".

## Quality gate

- `WRITING_DNA.md` has numbers for every rule and ten real exemplars; a rule with no evidence is marked `[provisional]`.
- `voice_stats.py --vs` table is in `evidence.md`, with no measure more than 2x off unless justified.
- Blind-pick record (picks, reasons, pass or fail) is in `evidence.md`.
- No claim that a text "sounds human": the evidence is the measurements, the blind pick and the owner's verdict.

## Boundaries

- Learn a manner; never copy posts, pose as a real page or person, or promise to pass AI detectors.
- Collected posts and screenshots stay in the work folder and never enter git. The owner's own voice: no limit beyond the owner's approval.
- Strict-source writing (academic, legal, news): no claim without its source; gaps are `UNVERIFIED:`.
