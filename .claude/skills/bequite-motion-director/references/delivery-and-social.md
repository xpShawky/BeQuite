# Delivery, recuts and launch posts (M9)

Most important first: **every platform gets a real recut (re-composed, bigger type), not the 16:9 film in a letterbox; posts sound like a person; and posting, DMs and automation are always done by the user** (`DELIVERY_APPROVED` covers the files and text, never a send). The ffmpeg commands for reframes, captions and encodes live in `.claude/skills/bequite-render-pipeline/references/adapter-ffmpeg.md`; this file decides *what* to deliver.

## Deliverables matrix

| Version | Size | Where | How to make it |
|---|---|---|---|
| 16:9 master | 2560×1440 or 1920×1080, 60 fps | YouTube, LinkedIn, Facebook, website | the master render |
| 16:9 phone preview | 1280×720, same fps as master | review on a phone, quick shares | small encode (a few MB/min) |
| **9:16 recut** | 1080×1920 | Reels, TikTok, Shorts | **re-compose** each beat for vertical: text re-laid out larger, UI cropped to the part in use, camera re-framed. In code/AE pipelines: a second comp per scene at 9:16 reading the same timing. Fallback only with the user's yes: the "stacked" layout (film centred, a big hook above, captions/CTA below, background in the film's stage colour, CTA pill in the film's accent and corner radius). Plain letterbox = last resort |
| 1:1 | 1080×1080 | feeds, LinkedIn | recut or centre-crop with re-placed text |
| 4:5 | 1080×1350 | Instagram/Facebook feed | recut; also the size of the making-of PDF pages |
| cut-downs | 15 s and 30 s | ads, second reel | re-edit around the best moment + lockup + CTA; never speed up |
| captions | `.srt` (+ burned-in for vertical) | every platform; feeds autoplay muted | from the voice's word timings (`bequite-sound-voice` `check_take.py --srt`) |
| cover frame | still, per ratio | thumbnail | the strongest frame, text-safe |
| stems + WAV mix | vo / music / sfx | future re-cuts | from the mixer |

Safe zones: in 9:16 keep text away from the bottom ~20 % and the right edge where platform UI sits; check against the platform's current safe-zone overlay. Frame 1 must already show text (muted autoplay). Same fps and colour on every version; name files so there is exactly one `FINAL` per version (`<film>_FINAL_16x9_2k.mp4`, `<film>_FINAL_9x16.mp4`).

## Writing the posts

Use `bequite-writing-dna` for the user's voice. Rules that make posts sound human:

- short lines, plain words, first person, one concrete detail (a number, a real struggle); at most one emoji per block
- no "In today's fast-paced world", no "game-changer", no stacked emojis, no hashtag walls
- lead with something intriguing and true (a contrast, a number, a result) — not "my first…"; don't overclaim ("it took 14 versions", not "one prompt")
- offer 2–3 tone options when unsure (simple / short / very short)

| Platform | Video | Caption shape | Hashtags (re-check current limits) |
|---|---|---|---|
| Instagram Reels | 9:16 recut | hook line · 2–3 short lines of story · keyword ask | 3–5 specific (a 5-per-post cap was reported from Dec 2025) |
| TikTok | 9:16 recut | 1–2 lines + "guide in bio" | 3–5 |
| Facebook | 16:9 master (cross-posted reels also fine) | friendly, a bit longer | a few |
| LinkedIn | 16:9 native upload with captions (autoplays muted) | 150–300 words: hook in the first 2 lines → why → how (3–5 concrete points) → what you learned → a question; links in the first comment | 0–3 |

Posting plan: day 1 the reel (reach); a few days later a making-of carousel (Instagram) / document post (LinkedIn); optionally a 15–30 s cut-down of the best moment. Reply to comments in the first hours. Tag only people and organisations really involved, with their consent.

## The comment-a-keyword → DM hook

One keyword in caps that matches the reward ("Comment GUIDE and I'll DM you the making-of PDF").

- Say it in three places: on screen at the end, in the caption's first lines, in a pinned comment.
- **Never ask people to follow in public** (caption, video, pinned comment). If a follow check is wanted, it happens privately inside the DM flow.
- Platform rules as documented in 2026 (re-verify): on Instagram/Facebook a tool may send **one private reply per comment within 7 days**; after the person replies or taps a button, a 24-hour window opens for further automated messages; non-followers receive it in Message Requests. Native comment-to-message automations exist but are limited (exact keywords, one fixed message); third-party tools add buttons, conditions and public auto-replies, often behind paid plans. TikTok had no general comment-to-DM automation (and its DM API excluded some regions): use link in bio + pinned comment + reply-with-video. LinkedIn: reply by hand.
- DM content: thanks, one button or link, one line on what's inside, an invitation to reply with questions. No pitch.
- The guide link: a share link with view access, ideally behind a short link the user controls so the file can be swapped later. The PDF is a public-safe version: no keys, no private images, no client secrets.
- **Gate:** creating automations, connecting tools to accounts and changing account settings are the user's actions; BeQuite writes the flow, the texts and the setup checklist only.

## The making-of guide (PDF)

A 4:5 portrait guide reads well on phones and doubles as carousel slides. Template: `making-of-guide-template.html` (generic; fill the placeholders). Contents that worked: the result by the numbers → the loop (describe → build → check → preview → notes) → tools and why → one page per phase with a copy-paste prompt box → "the versions, honestly" (what got rejected) → the best prompts → call to action.

Print with a headless browser (e.g. Chrome: `--headless=new --no-pdf-header-footer --print-to-pdf=out.pdf guide.html`) or hand it to `bequite-presentation-builder` for a deck version. Render every page to an image and check for overflow before sending. Frame thumbnails come from the film (`contact_sheet.py` in render-pipeline scripts).
