---
name: bequite-trend-radar
description: Use when the user asks what is moving in a niche ("what's trending in AI in Arabic this week", "what should I post about", "find outliers in my niche"), when /bq-content radar runs, or for a daily or weekly brief. Sweeps the platforms' own public surfaces, ranks videos by how far they beat their own channel, and writes a brief where every item has a link, a number and a reason it matters now.
last_verified: 2026-11-21
sources:
  - https://ads.tiktok.com/help/article/how-to-use-trends  # Creative Center Trends: hashtags by industry and time frame; analytics after login (updated July 2026, read 2026-11-21)
  - https://support.google.com/trends/answer/3076011  # Trending now: 100+ regions, past 4 h / 24 h / 48 h / 7 days, refreshed about every ten minutes (read 2026-11-21)
  - https://help.x.com/en/using-x/x-advanced-search  # words, accounts, language, dates; available when logged in (read 2026-11-21)
  - https://github.com/yt-dlp/yt-dlp/blob/master/README.md  # public listings as JSON without media (read 2026-11-21)
  - https://github.com/Jakeschincariol/youtube-agent-skill/blob/main/skills/yt-viral/SKILL.md  # momentum = multiple over the channel's own median, 4+ videos per channel (MIT, 6,756 stars, read 2026-11-21)
  - https://github.com/mvanhorn/last30days-skill  # cross-platform 30-day research; reads X through browser cookies (MIT, 71,866 stars, pushed 2026-11-21)
---

# bequite-trend-radar

Topics are everywhere; the radar's job is proof. Every item it reports carries a link, a number from the platform, the date it was read, and why it matters this week. It never posts, follows, likes or joins.

## When to use

- `/bq-content radar <niche>`, a daily or weekly brief, "what's working right now", competitor watch.
- Before `/bq-dna` (it picks which videos to measure) and before `bequite-hooks-and-copy` (it gives the topics).

Not for: measuring a video's form (`bequite-video-intel`, `/bq-dna`), or for any action on an account.

## Sources, cheapest and most official first

| Platform | Surface | Login | What it gives | How |
|---|---|---|---|---|
| YouTube | search filtered to this week / month; channel upload lists | no | views, date, channel median → momentum | `scripts/radar.py sweep` |
| Google Trends | Trending now, by country, category, past 7 days | no | search spikes with volume band, % rise, start time, the news behind them | browser: `trends.google.com/trending?geo=EG&hours=168&category=18` (18 = Technology) |
| TikTok | Creative Center Trends, by region and period (7/30/120 days) | top 3 without login; more and analytics with a free login | hashtags with posts and views | browser: `ads.tiktok.com/creative/creativeCenter/trends/hashtag?region=EG&period=7`; videos from `tiktok.com/tag/<tag>` |
| X | advanced search, Top tab, language + dates | yes (the user's own browser) | posts with views, likes, reposts, bookmarks | browser, read only: `<terms> lang:ar since:YYYY-MM-DD min_faves:300`, `f=top` (`min_faves` is not in X's help page; observed working) |
| Facebook groups, Reddit, HN | top posts of the month | Facebook: yes | questions people repeat | browser, read only; level 3: for "what people ask", never for facts |

Optional upgrade, only if the user creates it himself: a free TikTok for Business login unlocks the full hashtag lists, "See analytics" and top videos in Creative Center. The agent never creates the account.

The niche's watchlist (`references/watchlist-template.md`) adds named channels and accounts so the radar does not depend on search ranking.

## Procedure

1. **Frame.** Niche, language, country codes, period. Write 4-8 search terms in the language the audience searches in (for Arabic AI: الذكاء الاصطناعي, ذكاء اصطناعي, شات جي بي تي, Claude بالعربي, جيميني, أدوات الذكاء الاصطناعي).
2. **YouTube sweep.** `python scripts/radar.py sweep OUT --period week --per-query 12 --q ... [--watch watchlist.md]`. It reads each video's metadata and its channel's last 30 uploads (Shorts compared with Shorts), and writes `radar.md` ranked by multiple. Cost is metadata only (a few KB per video).
3. **Search spikes.** Google Trends, country and Technology category, past 7 days: note each relevant row's volume band, rise and start, then open "In the news" for the cause.
4. **TikTok.** Creative Center hashtags for the region; open the top tag's page for 3-5 video links; L0 metadata for each (`bequite-video-intel`).
5. **Conversation.** X search in the user's browser (only if allowed in `CAPABILITIES.md`): views, likes and bookmarks per post. A high bookmark-to-like ratio marks "save for later" content (tools, lists, guides).
6. **Score.** Keep an item if it has at least one of: multiple ≥ 2x on YouTube, a Trends spike in the niche, a top-3 TikTok tag, an X post above the niche's usual reach. Prefer items that appear on two platforms.
7. **Brief.** `references/brief-template.md`: topic, proof links with numbers, why now, format suggestion, risk. Every number has its source and read date; anything second-hand (a claim inside a post) is `UNVERIFIED:` until checked at its primary source.
8. **Watchlist.** Add new outlier channels and accounts; drop ones with no outlier in 30 days.

## Worked example (2026-11-21, "AI in Arabic", Egypt)

- Google Trends EG, Technology, 7 days: "gemini" 5K+ searches, +50%, started yesterday; news: "Let Gemini tackle repetitive chores on your Mac" (blog.google, 2 days ago). "جيميناي" 500+ the same day.
- X (lang:ar, since 2026-11-14, min_faves 300, Top): a post on Dario Amodei's advice to school leavers, 792,094 views, 14,137 bookmarks (Nov 20); "scheduled Claude tasks every morning", 79,863 views, 2,216 likes (Nov 17).
- YouTube: see the brief in the work folder for the ranked table.
- TikTok EG: #gta6 119.6M views, #دولة_التلاوة 128.6M, #pubgmobileflash 36.4M: no AI tag in the top 3, so TikTok is not where Egyptian AI interest shows this week.
- Brief item: "Gemini can now use your Mac" → why now: Google announcement 2 days ago and an Egyptian search spike since yesterday → format: 60-90 s Short, screen recording of one real chore, Egyptian Arabic voice.

## Quality gate

- No item without a link and a platform number with its read date.
- Momentum only from channels with 4+ recent uploads; the rest are listed as "no median".
- Claims made inside posts or videos are not facts; they are marked and checked before they become content.

## Boundaries

Public listings and the user's own logged-in view, read only: no posting, liking, following, joining, messaging or account settings. No scraping behind logins with scripts; the browser reads what the user could read. Respect rate limits (yt-dlp timeouts; wait on HTTP 429).
