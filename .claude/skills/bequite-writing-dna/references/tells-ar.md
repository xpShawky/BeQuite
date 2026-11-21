# Arabic tells (tested 2026-11-21; re-test per voice)

A tell is a habit the samples do not have. Rates are per 100 words unless stated. The test that matters is your own: `.claude/skills/bequite-writing-dna/scripts/voice_stats.py samples.json --vs drafts.json`.

## How the starting list was tested

47 top Arabic AI posts on X (Nov 1-21, 2026, 100+ likes, read in a browser) against 12 posts on the same topics from a fresh fast model with no style guidance.

| measure | human posts | default model |
|---|---|---|
| words per post, median / SD | 40 / 13.3 | 30.5 / 4.6 |
| sentence length mean; share under 8 words | 8.0; 53% | 11.0; 38% |
| Arabic comma ، | 2.52 | 5.67 |
| full stop | 3.44 | 7.93 |
| colon | 0.97 | 2.55 |
| exclamation | 1.26 | 0.28 |
| ellipsis (… or ..) | 1.38 | 0 |
| line breaks per post (median) | 4 | 0 |
| posts with emoji / opening with emoji | 49% / 30% | 0% / 0% |
| posts ending in a call (احفظ، تابع، جرب، 👇) | 17% | 42% |
| particles (يعني، بقى، كده، اللي، عشان، مش، وش، مو، زي، يا ...) | 2.24 | 2.83 |
| dialect markers Egyptian / Gulf / MSA | 32 / 45 / 23% | 89 / 0 / 11% |

Caveat: in an AI niche many top posts are themselves templated or machine-assisted (🚨 opener, "تخيّل", "والأقوى؟", "01." lists). Prefer a page whose voice is personal, and posts from before November 2022 when you can get them.

## The list

**Confirmed by measurement**
1. A comma after every clause, and a full stop after every sentence (about 2x the human rate).
2. One unbroken paragraph where the genre breaks lines.
3. Even lengths: every post about the same size, few very short sentences.
4. A closing moral or summary line ("والمستقبل بيقرب أكتر", "ودي بداية مرحلة جديدة"); a call to action on most posts.
5. Label-and-colon openers ("سؤال لمتابعيني:", "شرح كامل:", "خبر حلو للمبرمجين:").
6. No emoji, ellipsis or exclamation in a genre that uses them.
7. Inline ordinal enumeration "أولاً، ... ثانياً، ... ثالثاً،".

**Kept from the doctrine, scoped**
8. A dialect that does not match the page (the default model wrote Egyptian unprompted; the niche itself mixes Gulf, Egyptian and MSA). Match the page's mix.
9. Perfect spelling where the samples have habits (هذي، لسى، اللي، ـــ elongation, "ماحبيت" joined). Not yet measured; check against the page.
10. Translated English idioms and calques ("في نهاية اليوم", "يلعب دوراً محورياً"). Not yet measured.

**Dropped as a tell**
- "No particles": the model used them at the human rate. Check which particles and where, not whether.
- Formal Arabic in itself: fine where the page writes formally; many human tech posts are MSA with emoji.

## From the research (for longer or formal Arabic)

- Machine Arabic repeats its most frequent words more and uses a narrower vocabulary (Al-Shaibani & Ahmed, arXiv 2505.23276: top words over 3,000 occurrences vs under 2,000 in human abstracts).
- On social media, machine posts ran 25-72% of human length in that study; ours were 76% of the human median.
- Detectors trained on one genre fail on others (ALHD, arXiv 2510.03502): no detector score replaces the blind pick.
