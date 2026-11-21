---
name: bequite-video-intel
description: "Use whenever a task needs to know what is in a video (YouTube, Shorts, TikTok, Reels, a local file): a breakdown, a tutorial's exact steps, what a creator claims, how a reference film is cut, or the format of a niche's top videos. Starts at the cheapest route that can answer, checks every claim it will act on, and reports what each step cost. Used by /bq-watch, /bq-dna, /bq-content study, /bq-motion and bequite-human-taste."
last_verified: 2026-11-21
sources:
  - https://github.com/yt-dlp/yt-dlp/blob/master/README.md  # --download-sections, -S res (short side), +size over worst, --sleep-subtitles (read 2026-11-21)
  - https://ai.google.dev/gemini-api/docs/video-understanding  # 1 FPS default, may miss rapid cuts; ~100 tokens/s; YouTube links free, public only, 8 h/day free tier; agentic mode (read 2026-11-21)
  - https://github.com/SYSTRAN/faster-whisper/blob/master/README.md  # GPU needs cuBLAS 12 + cuDNN 9; int8 on CPU (read 2026-11-21)
  - https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md  # "transcript-only evidence cannot establish visual facts"; relay Gemini's answer as Gemini's (read 2026-11-21)
  - https://github.com/HUANGCHIHHUNGLeo/claude-real-video/blob/master/benchmark/benchmark.md  # fixed 1 fps can miss caption cards; scene-aware frames (read 2026-11-21)
  - BeQuite's v1 work notes, research/video/  # local measurements and the watch-or-transcript test, 2026-11-21
---

# bequite-video-intel

Claude reads text and images, not video or audio. This skill gives it eyes at the lowest cost: a multimodal model in the user's own browser where one is allowed (route G), and a local ladder of yt-dlp, ffmpeg and Whisper steps (L0 to L3) for everything else and for checking.

## When to use

- "Watch this", "what does this video say / show", "break this down", "how did they do this transition", "what do these creators claim", "measure the top videos in my niche".
- Before any creative work that cites a video as a reference (`bequite-human-taste`).

Not for: making videos (`bequite-motion-director`, `bequite-render-pipeline`), downloading to keep or re-post (never), private videos the user has no right to.

## Routes, cheapest first

| Route | What it gives | Cost | Fails when |
|---|---|---|---|
| G1 AI Studio in the user's browser | sees picture + hears sound; whole structure, on-screen text, critique | 0 bytes; ~105 tokens/s of Google's quota; Claude reads only the answer | no Google account, the user has not allowed it, model busy ("not available right now": rerun once), non-YouTube or private video |
| G2 Gemini app | same, accepts several URLs in one message | same | less exact on small text; dropped timestamps in a multi-video table |
| L0 `meta` | title, length, views, likes, comments, caption languages | ~1-5 KB, 2-12 s | never in practice |
| L1 `captions` | the words, timed; YouTube's `ar-orig` track is clean Egyptian Arabic | ~7-40 KB, 3 s | HTTP 429 after a few requests (lifted after about 20 min); most TikToks have none |
| L1b `audio` | the words from audio + local Whisper | 0.5-5 MB + CPU minutes | music-only video; Egyptian Arabic came out as English or garbage (small and large-v3-turbo): use captions for Arabic |
| L2 `storyboard` | the whole video as thumbnail sheets | 85-300 KB, 4 s | not on TikTok; thumbnails too small for UI text |
| L2b `section` | only the seconds that matter, any resolution | 20-170 KB per 3 s, 3-6 s | a call with several ranges stalled: one range per call |
| L3 `full` (+`--study`) | cut list, shot lengths, loudness, sound at cuts | 1.5 MB (88 s Short, 360p) to 24 MB (20 min, 240p) | never needed for words alone |

Measured numbers and their sources: `references/ladder-facts.md`. Route G detail and prompt templates: `references/route-g.md`.

## Procedure

1. **Ask what the answer needs.** Words only → L1/L1b. Look and structure → G1, or L2. One moment → L2b. Cuts, pace, loudness → L3 `--study`. Write the question down; it picks the level.
2. **Check permissions once per machine.** Route G needs the user's browser, profile and account, and their yes. Read `.bequite/state/CAPABILITIES.md`; if it does not say, ask. Never sign in, accept terms, change account settings or claim credits.
3. **Run L0 first** (`scripts/watch.py meta URL OUT`) for every video: it is the receipt (date, views) and tells which levels exist.
4. **Route G** (when allowed and the video is public on YouTube): one video per message for T1-T3, up to five for T4. Turn web grounding off so the answer can only come from the video. Ask for a timestamp on every point and UNSURE / NOT SHOWN instead of guesses. Read the answer from the page, save it to `work/<id>/research/video/<slug>.md` with URL, route, model, date, template.
5. **Check before acting.** Every number, setting, quote or on-screen text you will use: spoken items against L1/L1b at the cited time; visual items against an L2b frame. Unchecked items stay `UNVERIFIED:`.
6. **Local ladder** for what route G cannot do or did not answer: `scripts/watch.py captions|audio|storyboard|section|full`. Exact caption language codes only (`ar-orig` is the original-language Arabic track). For Arabic speech prefer captions; Whisper output on Arabic dialect is UNVERIFIED until spot-checked.
7. **Report the cost.** `scripts/watch.py ledger OUT` prints bytes and seconds per level; paste it into the breakdown.
8. **Write the breakdown** with `references/breakdown-template.md`: level used, bytes, checks with their results, what stays UNVERIFIED.

## Worked example (2026-11-21, real values)

Question: "Exact steps for the whip transition in this Premiere tutorial" (Solid Coast, 3:44).

- L0: 224 s, 108,830 views. L1 captions: 7,151 bytes, 2.7 s, every spoken value with its time.
- G1, gemini-4-neon, grounding off, template T2: steps with menu paths, keyframe times (00:00:01:22 / 02:01 / 02:05), values and easing, NOT SHOWN where silent.
- Checks: all spoken values matched the captions. 8 unspoken on-screen values checked on L2b frames (3 sections, 406 KB): 7 exact, 1 wrong (VR Glow radius: 100 on screen, Gemini said 20). The recipe ships with the corrected value.
- Cost: 0 bytes for the watch, 413,309 bytes for the checks (L1 + three L2b sections).

## Quality gate

- Every breakdown names the level(s) used and the bytes fetched (from the ledger).
- No visual claim rests on a transcript; no claim from a second model is used unchecked.
- The watch-or-transcript test result for each route on this machine is recorded in `CAPABILITIES.md` before the route is trusted for visuals (`references/route-g.md`).

## Boundaries

- Study, never re-publish: downloaded media and frames stay in the work folder, are deleted when the work closes, and never enter git.
- Public videos only. Respect a platform's limits: on HTTP 429, wait or change level; do not rotate IPs or accounts.
- The user's accounts are read-and-prompt only; a new sign-in, terms screen, API key or purchase needs the user's yes.
