---
description: Measure the form of what is winning in a niche (first 3 seconds, speaking rate, cut rate, captions, sound, ending) from its top five outliers and write a one-page format sheet to produce from. Platforms - shorts (default) / reels / tiktok / long.
---

# /bq-dna: the format of what wins, in numbers

<!-- bq:contract -->
> **Every run follows the contract** (`.claude/bequite/docs/architecture/COMMAND_EXECUTION_CONTRACT.md`):
> 1. **Up to date:** first run `bash .claude/bequite/bin/bq-update.sh` (hourly; it updates BeQuite when a newer version is published, backs up first, never touches `.bequite/` memory, never blocks) and say its one line.
> 2. **Skills first:** announce the `Skill Selection:` block before any plan, edit or tool call for the task.
> 3. **Resolve the work:** read `.bequite/ACTIVE.md`; use `.bequite/work/<id>/`, or create the next work folder if this is new work (`/bq-work`).
> 4. **Gates:** project gates in `.bequite/state/WORKFLOW_GATES.md`, work gates in `work/<id>/gates.md`. Refuse and name the missing gate.
> 5. **Plan first:** non-trivial work gets a plan the user approves before output. Hard human gates always wait for a yes.
> 6. **Evidence:** every check goes to `work/<id>/evidence.md` (command + exit code + output) or is marked `UNVERIFIED:`.
> 7. **Write back:** `work/<id>/log.md`, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, and `.bequite/state/MISTAKE_MEMORY.md` when a lesson surfaced.
> 8. **Finish** with the Next Command Recommendations block.
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
