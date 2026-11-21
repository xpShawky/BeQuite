---
description: "Watch a video (YouTube, Shorts, TikTok, Reels, a file) at the lowest cost that answers the question. Route G (a multimodal model in your browser, if allowed) or the local ladder (metadata, captions, audio + Whisper, storyboards, only the seconds that matter, full low-res study). Every claim used is checked; every step reports its bytes. Modes: breakdown / steps / claims / measure / test."
---

# /bq-watch: give the agent eyes on a video

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

Skill: `bequite-video-intel` (procedure, routes, costs). Scripts: `.claude/skills/bequite-video-intel/scripts/watch.py`.

## Syntax

```
/bq-watch <url> [question]            breakdown (template T1) unless a question narrows it
/bq-watch steps <url> "<effect>"      a tutorial's exact steps and values (T2)
/bq-watch claims <url1> <url2> ... "<topic>"   what several videos claim, agree on, contradict (T4)
/bq-watch measure <url>               cut list, shot lengths, loudness, sound at cuts (L3 --study)
/bq-watch test                        run the watch-or-transcript test for route G on this machine
```

## Preconditions

`BEQUITE_INITIALIZED`. yt-dlp and ffmpeg on PATH (`/bq-doctor` checks). Route G only if `.bequite/state/CAPABILITIES.md` says the user allowed it and the route passed `/bq-watch test`; otherwise ask once, or use the ladder.

## Steps

1. **Question → level.** Write the question in one line and pick the cheapest level that answers it (skill table). Show the choice and the expected bytes in one line before fetching anything over 5 MB.
2. **L0 receipt** for every URL: `watch.py meta URL work/<id>/research/video/<slug>/`.
3. **Route G** when allowed (public YouTube): template from `references/route-g.md`, grounding off, one video per message except `claims`. Save the answer verbatim to `research/video/<slug>.md`.
4. **Check** each value, quote or visual you will use: captions or Whisper at the cited time for speech, an L2b frame for anything on screen. Record match / wrong / UNVERIFIED.
5. **Ladder** for anything route G cannot give (`measure`, private files, TikTok, a 429 on captions).
6. **Breakdown** with `references/breakdown-template.md`, the ledger table pasted in.
7. **Clean up**: media stay in the work folder, never in git; delete them when the work closes.

## Output

`work/<id>/research/video/<slug>.md` (breakdown) and `<slug>/ledger.jsonl`. In chat: the answer in a few lines, the checks that failed, the cost.

## Never

Re-post or re-upload anyone's video. Sign in, accept terms, create an API key or change account settings in the user's browser without a yes. Use a transcript to claim what a video shows.

## Next Command Recommendations

- `/bq-dna <niche>` to measure the format of the top videos.
- `/bq-content study` to turn a breakdown into a format sheet for production.
