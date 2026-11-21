---
name: bequite-hooks-and-copy
description: Use when writing the first seconds of a video, a post's first line, a title, a caption or a script beat for social content (/bq-content script, Shorts, Reels, TikTok, X, Telegram), or when the user asks "how do I open this", "why does nobody watch past 3 seconds", "write me a hook". Builds hooks from measured human references in the niche, checks them against the platforms' own statements, and proves them with a blind pick.
last_verified: 2026-11-21
sources:
  - https://about.instagram.com/blog/announcements/instagram-ranking-explained  # Reels: most important predictions are reshare, watch all the way through, like, visit the audio page (May 31, 2023; read 2026-11-21)
  - https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you/  # finishing a longer video is a strong signal; follower count and past hits are not direct factors (read 2026-11-21)
  - https://support.google.com/youtube/answer/16089387  # satisfaction surveys "not just watch time"; Shorts feed personalised (read 2026-11-21)
  - https://metricool.com/short-video-report-2026  # 6,177,375 videos, 375,462 accounts: Reels lead in shares at every account size; TikTok up to 42% more views than Reels (read 2026-11-21)
  - https://simonwillison.net/2024/Sep/15/how-to-succeed-in-mrbeast-production/  # MrBeast production doc: the first minute must prove the thumbnail's promise; CTR, AVD, AVP (read 2026-11-21)
  - https://github.com/Jakeschincariol/youtube-agent-skill/blob/main/skills/yt-script/hooks.json  # 21 hook formulas with shape and failure mode; its scorer "barely" separates a creator's hits from misses (MIT, read 2026-11-21)
  - references/hook-patterns.md  # 11 real Arabic AI Short openings measured 2026-11-21
---

# bequite-hooks-and-copy

A hook is the first sentence a viewer hears or reads. In the niche measured for this skill, every winning Short starts speaking at 0.0 s with one 13-15 word sentence that puts a person, a number or a bind in front of the viewer. This skill writes hooks and copy in the grammar of measured references, never from a generic formula list alone.

## When to use

- The opening of any short video or post; titles and captions; the beat sheet of a script.
- Rewriting an opening that loses people in the first seconds.

Not for: the full voice of a page (`bequite-writing-dna`), the video's form (`bequite-format-dna`), topics (`bequite-trend-radar`).

## What the platforms say (primary, dated)

- Instagram Reels: the most important predictions are reshare, watching all the way through, liking, and visiting the audio page (Instagram, May 31, 2023).
- TikTok: finishing a longer video is a strong signal; follower count and past hits are not direct factors (TikTok newsroom).
- YouTube: satisfaction surveys matter, "not just watch time"; the Shorts feed is personalised and may favour recency (YouTube Help).
- So a hook earns its place only if the rest of the video keeps the promise: the opening buys the first seconds, completion and sends are decided by what follows (MrBeast production doc: the first minute proves the thumbnail's promise).

Everything else (exact weights, "post at 7 pm", "the first 1.7 s") is not stated by the platforms: treat it as `UNVERIFIED:`.

## Procedure

1. **Load the references.** The niche's format sheet (`bequite-format-dna`) and 7-12 real openings from recent outliers (`watch.py captions` on each, first one or two lines). If none exist, collect them first: no hook without references.
2. **Pick the pattern** from `references/hook-patterns.md` that fits the topic and is proven in this niche (each pattern lists real examples and the matching formula from the 21).
3. **Write 5 hooks**, each one sentence in the niche's dialect, 13-15 words (Arabic AI Shorts), with a concrete noun: a named person, a number with its unit, a date, a place on screen. No bare superlative, no greeting, no "label:" opener.
4. **Check the promise**: each hook must be kept by the video. A hook that claims a run, a result or a price the work cannot show is cut.
5. **Tell sweep** with `bequite-writing-dna/references/tells-ar.md` or `tells-en.md`.
6. **Blind pick** (`bequite-writing-dna/references/blind-pick.md`), one fresh judge per list, each list one generated hook among seven real openings, key fixed first. Pass: one found or none.
7. **Copy around the hook** with `references/copy-frameworks.md`: the beat order measured in the niche, the ending, the caption.
8. **Owner's verdict**; corrections become rules.

## Worked example (2026-11-21, real)

Topic: "Gemini can now use your Mac" (Google, Nov 19, 2026; Egypt Trends spike). References: 11 real openings from recent Arabic AI Shorts. Five hooks written (persona + number, dated news, I tried it, direct-address warning, result first). Blind pick, five judges: 0 of 5 found; every judge chose a real line, most often a real creator's generic superlative "اقوى اداة مجانية لكشف الكتابة بالذكاء الاصطناعي". Rule added: never open on a bare superlative. Promise check: two hooks claim a run we cannot do from Egypt (U.S. rollout), so they wait.

## Quality gate

- 7+ real references with links, and the five hooks, saved in the work folder.
- Every hook: one sentence, the niche's dialect, a concrete noun, a promise the video keeps.
- Blind-pick record with key, picks and reasons in `evidence.md`.
- No platform "rule" without its primary source; the rest marked `UNVERIFIED:`.

## Boundaries

No false claims, fake numbers, bait the video does not pay off, or engagement bait the platforms penalise ("comment X to get the link" is fine when the link is real). Learn patterns; never copy another creator's line.
