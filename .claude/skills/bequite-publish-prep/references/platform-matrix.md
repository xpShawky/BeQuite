# Platform matrix (read at the source 2026-11-21; re-check before building on any row)

| | Telegram channel | Instagram Reels | YouTube Shorts | TikTok |
|---|---|---|---|---|
| Official API to post | Bot API `sendVideo` / `sendMessage` (Bot API 10.4, 2026-11-09) | Instagram Platform content publishing: create container `media_type=REELS`, then `media_publish` | Data API `videos.insert` | Content Posting API (`video.publish` scope) |
| Who can post | a bot the owner created, admin of the channel | Instagram professional accounts | the channel's owner via OAuth | the user who authorised the app |
| Limits | upload by multipart: 50 MB for video; by URL: 20 MB; caption 0-1024 characters after entities; text message 1-4096 | 100 API-published posts per 24-hour moving period (carousel = 1); video must be at a public URL or uploaded resumably to `rupload.facebook.com` | own "Video Uploads" quota bucket: 100 `videos.insert` calls per day, 1 unit each; file up to 256 GB; Shorts up to 3 min (vertical or square) | unaudited app: posts are private only, up to 5 users per 24 h, accounts must be private when posting; `creator_info/query` returns allowed privacy levels and `max_video_post_duration_sec` |
| Visibility catch | none | none stated | the insert page now says uploads from unverified API projects are not restricted to private | public posting needs TikTok's audit |
| Our route | post through the bot after the owner's yes | prepare the package; publish via API only if the owner has a professional account and approves each post | prepare; upload via API or by hand after the owner's yes | prepare the package; the owner posts by hand from his phone or computer |
| Never | post without approval | automate through the app or browser (breaks the terms, risks the account) | | automate the app or the website |

## Package fields we fill per platform

- **Telegram:** video file (≤50 MB), caption (≤1024 characters, Arabic counted as characters), optional cover image.
- **Instagram Reels:** video (9:16), caption (Instagram's in-app limit is 2,200 characters and 30 hashtags: `UNVERIFIED:` not found on the developer page read today), cover frame or image, alt text not available for Reels (image posts only).
- **YouTube Shorts:** title (≤100 characters per the Data API `snippet.title`: `UNVERIFIED:` not re-read today), description, tags, `status.privacyStatus`, `status.selfDeclaredMadeForKids`, `status.containsSyntheticMedia` (true when realistic altered or synthetic media is used).
- **TikTok:** video, caption, privacy level from `creator_info`, the owner posts it.

## Sources

- https://core.telegram.org/bots/api (sendVideo, Sending files, recent changes)
- https://developers.facebook.com/docs/instagram-platform/content-publishing/
- https://developers.google.com/youtube/v3/docs/videos/insert · https://developers.google.com/youtube/v3/determine_quota_cost
- https://developers.tiktok.com/doc/content-sharing-guidelines · https://developers.tiktok.com/doc/content-posting-api-get-started
- https://support.google.com/youtube/answer/15424877 (three-minute Shorts)
