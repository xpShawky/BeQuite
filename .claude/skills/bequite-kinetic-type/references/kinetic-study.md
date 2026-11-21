# Kinetic type study: whole words, the push, the following camera (2026-11-21)

Reference: "Typography Motion Graphics Animation in After Effects, Kinetic Typography #4" (tutorial result reel; kept local in the BeQuite repo's `motion-library/inbox/`, never shipped), the 0-13 s showcase, read on a 6 fps contact sheet, 1280x720 at 60 fps. It is the reference the owner chose for the hero film (work 0001, film v14).

## Measured

- **One cycle is 5.2 s and loops** (repeats at 5.33 s and 10.5 s): one sentence of 17 words, "animating text like this can be challenging but this tutorial will help you how to do that".
- **Words land whole**, never letter by letter: each word is readable within 1-2 samples (0.17-0.33 s) of first appearing, arriving from blur and a scale change. 16 arrivals in 4.67 s = **one word every 0.29 s on average (about 3.4 words/s)**, uneven: a fast run of small words ("this / can / be" at 0.83-1.17 s), then a long word alone ("challenging", 1.5 s).
- **The push:** a new word appears beside or under the last one and the block re-centres; small connecting words stack beside a large word ("like" + "this / can / be").
- **Size contrast:** 3-4 type sizes in one block; content words big ("but", "tutorial", "that"), connectors small; the small ones end up 5-8 times smaller than the hero word.
- **Colour:** white plus one accent (green) on chosen words ("text", "challenging", "you", "how", "that"); a dark green-black radial background that never changes.
- **The camera follows the newest word:** it pulls out as the block grows (1.5-2.0 s the whole first block is small), then pushes in hard onto the next hero word ("but" fills the frame at 3.2-3.5 s), panning to keep the newest word near centre.
- **Motion blur on every camera move** (strong directional smears at 3.17, 3.67, 4.67 s); the type itself is sharp when still.
- **The end:** the finished block ("how / to do / that") holds about 0.5 s, then a cut to black and the next cycle.
- **Measurement limits:** `film_study.py` reported 63 "hard cuts" in 13 s; on kinetic type, word arrivals and blur whips read as cuts, so that count is not usable here. Count word arrivals from a 6 fps sheet. `sound_profile.py` on the whole file: tempo unreliable (confidence 0.06).

## The owner's corrections (work 0001, films v9 to v14)

- Whole words that push, not typing.
- The brand word first in the kinetic line.
- Type follows the angle of the light or the edge it sits on (the laptop lid, the light window).
- **Less zoom than the reference.** The reference swings from a wide block to one word filling the frame; the owner asked for moderate zoom. Working range used by the BeQuite engine: 0.95-1.25 (`DIRECTOR_PACK` spec). This is a chosen deviation from the reference, written down.
- Every step verified against the shot (does the line fit the frame at its size?).

## Rules for a new piece (from the above)

1. Words land whole in 0.1-0.3 s, from blur + a small scale settle; never letter by letter unless the content is typing.
2. Vary the spacing: runs of small words, then one big word alone; identical spacing is a tell.
3. One accent colour for the words that carry the meaning; at most 3-4 sizes.
4. The camera follows the newest word with motion blur on the move; zoom stays moderate (0.95-1.25) unless the owner chooses otherwise.
5. Hold the finished block before leaving it (about 0.5 s in the reference).
6. Check it on a contact sheet sampled per scene (first word, half built, finished block), not evenly spaced: an even 12-frame sheet missed a hero word between samples in work 0002 (`.bequite/state/MISTAKE_MEMORY.md`, 2026-11-21).

Engine: the After Effects kinetic engine and its director grammar are built in work 0002 task B9 (track A installs them); this page is the study it rests on.
