---
name: bequite-publish-prep
description: Use when a content piece is ready to leave the machine (Telegram, Instagram Reels, YouTube Shorts, TikTok), for /bq-content package and queue, or when the user asks "post this", "schedule this", "can we auto-post". Packages each platform's files and texts within the official limits, checks every claim has a source, and stops at the owner's approval. Never posts without a yes per post.
last_verified: 2026-11-21
sources:
  - https://core.telegram.org/bots/api  # Bot API 10.4 (2026-11-09): sendVideo up to 50 MB (multipart), 20 MB by URL; caption 0-1024 characters (read 2026-11-21)
  - https://developers.facebook.com/docs/instagram-platform/content-publishing/  # professional accounts; media_type REELS; 100 API-published posts per 24 h (read 2026-11-21)
  - https://developers.google.com/youtube/v3/docs/videos/insert  # Video Uploads bucket: 100 calls/day, 1 unit; 256 GB; unverified projects not restricted to private (read 2026-11-21)
  - https://developers.tiktok.com/doc/content-sharing-guidelines  # unaudited clients: private only, 5 users per 24 h, accounts private when posting (read 2026-11-21)
  - https://developers.tiktok.com/doc/content-posting-api-get-started  # creator_info: privacy options and max_video_post_duration_sec (read 2026-11-21)
  - https://support.google.com/youtube/answer/15424877  # Shorts up to 3 minutes (read 2026-11-21)
---

# bequite-publish-prep

The last step before the world sees the work. It turns a finished piece into a package per platform, checks it against each platform's own limits, and puts it in front of the owner. Official APIs only; where there is none for us (TikTok without an audit), the owner posts by hand.

## When to use

- `/bq-content package` and `/bq-content queue`; any "post / schedule / publish" request.

Not for: writing (`bequite-hooks-and-copy`), making the video (`bequite-motion-director`), account settings (never).

## Procedure

1. **Read the matrix** (`references/platform-matrix.md`). If a row is older than 30 days, re-read that platform's page first.
2. **Build the package folder** `work/<id>/package/<piece>/`: `package.json` (platforms, texts per platform, duration, `synthetic_media`, claims with sources), `captions.srt`, the cover, the video when produced.
3. **Texts per platform**: Telegram caption ≤1024 characters; YouTube title ≤100 characters; Instagram caption with few hashtags; the same hook noun in each first line.
4. **Claims**: every factual claim in the script or texts has a URL to its primary source in `package.json`. No source, no claim.
5. **Disclosure**: set `synthetic_media` truthfully (YouTube `containsSyntheticMedia` for realistic altered or synthetic footage).
6. **Check**: `python scripts/package_check.py <package>`; fix every FAIL.
7. **Approval**: write `APPROVAL.md` with status `PENDING`, the checks output, the texts, and what will happen on yes (which platform, which route, when). Stop. Nothing is posted until the owner writes yes for that post.
8. **On yes**: post through the official route for that platform (Telegram bot; Instagram or YouTube API only when the owner set them up), or hand the files to the owner (TikTok). Log the post URL in `evidence.md`.

## Worked example (2026-11-21, scratch run)

Piece: "Gemini now uses your Mac, but not here yet" (radar W47 item 1), Egyptian Arabic, 163 words timed at the niche's 2.8 words/s with 0.5 s beat gaps = 64.2 s. Package: script (13 beats), 59-cue captions, texts for Telegram (287 characters), Instagram (192), YouTube (title 49, description 409), TikTok (78), five claims each sourced to Google's post of 2026-11-19. `package_check.py`: 15 checks, 0 FAIL, 1 warning (no video yet: pre-production draft), exit 0. A planted broken copy (1,100-character caption, an unsourced "3x faster" claim, overlapping cues) failed 3 checks, exit 1. `APPROVAL.md`: PENDING. Nothing posted.

## Quality gate

- `package_check.py` exit 0, output in `evidence.md`.
- Every claim with a primary-source URL; disclosure set.
- `APPROVAL.md` exists; nothing left the machine without the owner's yes, per post.

## Boundaries

- No browser or app automation to post (breaks the platforms' terms, risks the account). Official APIs or the owner's own hands.
- Credentials stay in the owner's local env files, never in the package, the chat or git.
- Research and preparation may run anywhere (a cloud session, a VPS, a multi-agent folder); publishing runs from the owner's own device and account. Servers never sign in to the owner's social accounts, so a data-centre IP is never tied to them. For TikTok the output is a ready folder (video, caption, hashtags, cover, suggested time) that the owner posts by hand.
