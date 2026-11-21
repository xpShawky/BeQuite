# The grammar of this style

Kinetic typography as studied from human-made references (a kinetic-type tutorial's showcase, Apple's 2026 product films, the BeQuite hero film). Each rule has a number you can check.

## 1. Words, not letters

- Words land whole: they appear in about 0.1 s and settle from 118% to 100% in about 0.26 s (a word on a scene's beat 0 is already there on the cut). Letter-by-letter typing is a different style; do not imitate it.
- One word per item. Phrases are built from words landing one after the other.

## 2. Size carries meaning

| Size | Use | Typical count per scene |
|---|---|---|
| XL | the one hero word (brand, payoff, the number) | 0 or 1 |
| L | content words: nouns, verbs, adjectives that matter | 2 to 4 |
| M | secondary content words | 0 to 3 |
| S | connectors in a stack: the, of, a, to, is, with, for, can, be | 0 to 3 |

- At most three sizes in one scene. Everything XL means nothing is.
- A stack of two small words beside a big word is the signature of this style ("the / most" beside "BeQuite"; "this / can be" beside "like").

## 3. The block

- 2 to 4 rows per scene; 1 to 3 items per row.
- Rows of similar width look designed. As a guide, an L word is about 0.5 x its letters x 196 px wide; keep each row's letters within about 30% of the widest row.
- Break lines on meaning, not on width alone: "the most / powerful / AI harness / right now".

## 4. Rhythm (at 120 BPM a beat is 0.5 s)

- Connecting words: half beats or quarter beats, often inside a stack.
- Content words: on beats.
- Before the hero word, leave a breath: one half to one full beat with nothing landing.
- The hero word lands on a strong beat (a whole number, ideally an even one) and may `slam`.
- Two words never land less than a quarter beat apart.
- Vary the spacing between scenes: a fast run (four words in two beats), then a slow one (two words in two beats). Identical spacing in every scene is a tell.
- `hold_beats`: 2 for most scenes, 3 for the last or the most important.

## 5. The camera

- `follow` for building a line word by word: the viewer's eye goes where the newest word is. It is the default and carries the energy.
- `static` for a calm opening or ending, or a list that should be read as one block. Two static scenes in a row start to feel like slides.
- The settle on the whole block happens at the slam; without a slam, right after the last word lands.

## 6. Scenes and transitions

- One idea per scene; 4 to 10 words.
- A 12 to 15 second Reel at 120 BPM is 24 to 30 beats: usually 3 to 4 scenes.
- `whip-up` between scenes that build energy; `cut` when the next scene contrasts; `fade` only at the very end.

## 7. Colour

- One accent colour (the preset decides it). One accented word per scene, the payoff.
- Brand names in two colours through `parts` (for example "Be" in white, "Quite" in gold).

## 8. Checklist before you send

1. Every scene has exactly one hero word (L or XL) and it lands after a breath.
2. Connectors are small and stacked, not full-size words in their own rows.
3. No two scenes have the same rhythm.
4. Beats increase in reading order.
5. The whole film fits the requested length: sum of (last beat + hold_beats) x 60 / bpm, plus `first_beat`.
