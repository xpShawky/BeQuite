---
name: bequite-format-dna
description: Use before producing short video for a niche (Shorts, Reels, TikTok), when the user asks "how do the winners in my niche make their videos", for /bq-dna and /bq-content study. Picks the niche's outliers by momentum, measures their form (first 3 seconds, speaking rate, cut rate, shot length, captions, sound, ending) and writes a one-page format sheet a producer can follow.
last_verified: 2026-11-21
sources:
  - https://support.google.com/youtube/answer/15424877  # Shorts up to 3 minutes; most songs up to 90 s inside a 3-min Short; longer Shorts may get less Shorts-feed traffic at first (read 2026-11-21)
  - https://github.com/yt-dlp/yt-dlp/blob/master/README.md  # channel tab listings with view counts; sections; -S res (read 2026-11-21)
  - https://ai.google.dev/gemini-api/docs/video-understanding  # 1 FPS sampling misses fast cuts: measure cuts locally (read 2026-11-21)
  - https://github.com/Jakeschincariol/youtube-agent-skill/blob/main/skills/yt-viral/SKILL.md  # outliers = multiple over the channel's own median, 4+ videos (MIT, read 2026-11-21)
  - https://www.socialmediatoday.com/news/instagram-officially-expands-reels-length-to-3-minutes/737766/  # Reels up to 3 minutes (Jan 2025, Mosseri; level 2, no Help Center page found)
  - .claude/skills/bequite-motion-director/scripts/film_study.py  # cut list, shot lengths, loudness, sound at cuts (tested 2026-11-21 on 7 videos)
---

# bequite-format-dna

Topics are cheap; form is what competitors copy last. This skill measures the form of what is winning in a niche right now and turns it into numbers a script and an edit can follow, so production starts from human references, not defaults.

## When to use

- Before the first video in a niche or platform, and again monthly.
- `/bq-dna <niche>`, `/bq-content study`, or "make it look like the ones that work".

Not for: one video's content (`bequite-video-intel`), topic ideas (`bequite-trend-radar`), the edit itself (`bequite-motion-director`).

## Procedure

1. **Pick the five.** From the niche's channels (the radar's watchlist or sweep), rank recent uploads per channel by multiple over that channel's median: `bequite-trend-radar/scripts/radar.py outliers OUT --tab shorts --channel @a --channel @b ...`. Take the top five that are in the niche, from at least three channels. Write why each was chosen.
2. **Measure.** `scripts/dna.py measure OUT <5 URLs> --lang <exact caption code, e.g. ar-orig>`: L0, L1 captions, L3 at 360p + `film_study.py`, a 0-3 s frame strip. Cost is metadata + about 1-3 MB per Short.
3. **Read the frames.** For each video open `first3s.jpg` and `study/shots.jpg`: caption position (% of height), words per caption, case and colours, what is on screen in frame 1, face or no face, layout. Write numbers, not adjectives.
4. **Aggregate.** `scripts/dna.py sheet OUT` gives the medians table; add the visual measurements by hand.
5. **Write the format sheet** (`references/format-sheet-template.md`): one page, every rule with its median and its range across the five, one example timestamp per rule, and a never-list (what none of the five do).
6. **Check with the owner** before production: the sheet is a reference choice (gate `REFERENCES_STUDIED`).
7. **Refresh** monthly or when the radar shows a new format winning.

## Worked example (2026-11-21, AI in Arabic, YouTube Shorts)

- Candidates: 17 Arabic AI channels, last 30 Shorts each, 29 s of listing. Five chosen: Mohamed Ansary 30.9x, JORA TECH 10.4x, Yehia Tech 8.7x, Python Arabic Community 7.0x, Fathy & Abusrea 6.7x.
- The resulting sheet is `BeQuite's v1 work notes, research/format/format-sheet-ai-arabic-shorts.md` (medians across the five, the never-list, a 60-90 s template).

## Quality gate

- Five videos, three or more channels, each chosen by multiple with its number.
- Every rule in the sheet has a median and a range from the five; no rule without a measurement.
- Caption style and hook described from frames with timestamps, not from memory.
- Costs (bytes per video) recorded from the ledger.

## Boundaries

Study only: downloaded videos stay in the work folder and are deleted when the work closes. The sheet copies form (timing, structure, caption grammar), never footage, music, logos or wording.
