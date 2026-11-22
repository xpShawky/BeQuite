---
description: Measure the form of what is winning in a niche (first 3 seconds, speaking rate, cut rate, captions, sound, ending) from its top five outliers and write a one-page format sheet to produce from. Platforms - shorts (default) / reels / tiktok / long.
---

# /bq-dna: the format of what wins, in numbers

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

Skills: `bequite-format-dna` (procedure), `bequite-trend-radar` (picking the outliers), `bequite-video-intel` (the ladder). Scripts: `bequite-format-dna/scripts/dna.py`, `bequite-trend-radar/scripts/radar.py`.

## Syntax

```
/bq-dna "<niche>" [shorts|reels|tiktok|long] [--channels @a,@b,...] [--lang ar-orig]
/bq-dna refresh            re-measure the current sheet's niche
```

## Steps

1. Channels: from `--channels`, else the radar watchlist, else a sweep (`radar.py sweep`). Show the list.
2. Outliers: `radar.py outliers OUT --tab shorts --channel ...`; pick five in the niche from three or more channels; show them with their multiples and wait for a yes or a swap.
3. Measure: `dna.py measure OUT <urls> --lang <code>`; read `first3s.jpg` and `study/shots.jpg` for each; write the visual numbers.
4. Sheet: `dna.py sheet OUT`, then `references/format-sheet-template.md` → `work/<id>/research/format/format-sheet-<niche>.md`.
5. Gate: the owner approves the sheet → `REFERENCES_STUDIED` done for the work.

## Output

The one-page sheet, the data table, the five videos with links and multiples, the byte cost.

## Never

Re-use footage, music, logos or wording from the five. Measure private videos.

## Next Command Recommendations

- `/bq-content script` to write in the measured format.
- `/bq-motion` to produce it.
