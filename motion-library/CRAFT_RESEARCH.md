# 06 — Motion craft research for /bq-motion

Research date: 2026-11-12. Method: live web search plus page reads (WebFetch), plus YouTube/Vimeo page and oEmbed reads to check the title, channel, length and upload date of every film in the download list (section 6). Every claim carries a source URL. Anything I could not confirm is marked **UNVERIFIED**. I did not redo the local frame analysis of the Opus 5.5, Fable 5.2, dock, button-morph, kinetic-type or Higgsfield reference films; this report builds on it.

Source-quality legend: **[P]** primary (the maker, platform, or official docs) · **[T]** trade or press · **[S]** secondary or vendor blog (treat as opinion).

---

## 0. Top findings (read first)

1. **Google Flow changed under the owner's feet.** Flow's default video model is now **Omni Flash 1.2**, not Veo. **Veo 3.1 Fast, Veo 3.1 Quality and Omni Flash 1.1 retire on 5 Dec 2026**, and **Veo Extend was retired on 5 Nov 2026**. Extending a clip now needs a paid plan plus Omni Flash 1.2. [P] https://support.google.com/flow/answer/16352836?hl=en
2. **Omni wants different prompts from Veo.** Google's prompt guide says Omni doesn't need highly prescriptive prompts and fills in details from world knowledge. It also **defaults to multiple shots**: for a single shot you have to write "In a single continuous shot … No scene cuts". There are no negative prompts, so write "Do not …" in the prompt itself. [P] https://deepmind.google/models/gemini-omni/prompt-guide/ · https://aistudio.google.com/docs/omni
3. **Professionals throw away almost everything they generate.** Paul Trillo used about 55 of roughly 700 Sora clips (~8%) [T] https://nofilmschool.com/ai-music-video. A Higgsfield tutorial reports "800 generations. 8 shots that made the cut" [P] https://www.youtube.com/watch?v=-scKERL7PK0. The "Air Head" team colour-fixed, rotoscoped and cleaned up shots in After Effects [T] https://cgpress.org/archives/shy-kid-on-using-sora-to-create-air-head.html. /bq-motion should budget for selection and finishing, not for single prompts.
4. **The cheapest anti-AI fix is cutting.** One production house puts it this way: "A skilled editor ends the scene half a second early — right before the technology gives itself away." [S] https://multiproduktion-se.pages.dev/en/articles/why-your-ai-video-looks-cheap/
5. **Loud masters lose on platforms.** YouTube and Spotify both normalise playback to −14 LUFS. A −6 LUFS master is simply turned down by about 8 dB, and its crushed transients then sound flat next to dynamic mixes ("Dynamic is the new Loud"). [P] https://support.spotify.com/artists/article/loudness-normalization/ · [T] https://productionadvice.co.uk/youtube-loudness/
6. **Who made the Claude Opus 5.5 / Fable 5.2 launch films is UNVERIFIED.** No credit was found anywhere. Anthropic does have an in-house "Creative Studio" that, per a job ad, owns "video content for our most important moments" including model launches. That makes in-house production plausible but unconfirmed. [P] https://jobs.accel.com/companies/anthropic/jobs/67758897-video-director-product-launches. The brand campaigns are credited, to Mother London with directors Daniel Wolfe, Myles McAuliffe and Jeff Low (section 2).
7. **2026 trend signal: a swing back to visibly human craft.** BUCK's predictions include "Imperfection is the signal, not the flaw" and the deliberate use of low frame rates, boil and halftone. In product marketing, captured real product screens rose from 37% to 63% of UI videos during 2026. [P] https://pencilsdown.buck.co/p/looking-ahead-bucks-2026-predictions · [S] https://advids.co/blog/ui-animation-motion-design-trends

---

## 1. Editing craft

### 1.1 Graphic match cuts and shape-continuity montage
- **Definition.** A cut where an object or shape in two shots matches graphically. Bordwell and Thompson coined "graphic match" in *Film Art*, using Ozu's "match on red" as an example. [P] https://www.davidbordwell.net/blog/2011/05/25/graphic-content-ahead/
- **What it is for.** Usually metaphor or meaningful comparison, and unlike a match on action it is meant to be noticed. [S] https://www.studiobinder.com/blog/match-cuts/ · https://en.wikipedia.org/wiki/Match_cut
- **The canonical example** is the bone-to-satellite cut in *2001*. StudioBinder notes it is a basic graphic or idea match rather than a precise action match. Clip: https://www.youtube.com/watch?v=avjdKTqiVvQ (Movieclips, 2:43).
- **Teaching video:** StudioBinder, "Creative Match Cut Examples & Editing Techniques", 6:44. https://www.youtube.com/watch?v=ptXlYulVAsM
- **For /bq-motion.** The Opus/Fable "constant horizon" montage is a *sustained* graphic match: one locked compositional anchor (the curve position, its scale and the type baseline) holds across dozens of different worlds. The rule to encode is to pick one anchor and keep its frame position identical to the pixel across every shot. With AI shots, generate each plate from the same first-frame layout (Flow's first/last frame or ingredients), so the curve sits in the same place before any motion starts.

### 1.2 J-cuts, L-cuts, smash cuts, cutting on action
- **J-cut:** the incoming shot's audio starts before its picture. **L-cut:** the outgoing audio carries on over the new picture. The names come from the shape on the timeline. [S] https://www.backstage.com/magazine/article/j-cut-film-editing-how-to-75535/ · https://www.backstage.com/magazine/article/l-cut-film-editing-how-to-75537/
- **Smash cut:** the most abrupt transition, built on contrast (loud against quiet, active against still). StudioBinder covers it in "Ultimate Guide to Scene Transitions" (19:29). https://www.youtube.com/watch?v=TKXBAaQB03U
- **Cutting on action:** cut in the middle of a movement that spans both shots, so the eye follows the motion and doesn't register the cut. [S] https://nofilmschool.com/essential-cuts-every-video-editor-needs-know
- **Murch's Rule of Six** (*In the Blink of an Eye*): emotion 51%, story 23%, rhythm 10%, eye-trace 7%, 2D plane 5%, 3D space 4%. The weights come from secondary write-ups [S] https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch · https://www.studiobinder.com/blog/walter-murch-rule-of-six/. A No Film School piece argues that eye-trace matters more in fast online video than Murch's ranking suggests [S] https://nofilmschool.com/2018/08/editing-eye-trace-mind-rule-six-incorrect. StudioBinder's video on the book runs 15:05: https://www.youtube.com/watch?v=PKYeClvvlTw
- **For /bq-motion.** In fast montage, eye-trace continuity is what makes 33 cuts in 20 s feel smooth rather than chaotic. Each new shot should put its point of interest where the eye already is. The constant-horizon film does exactly this.

### 1.3 Cutting to the beat, accelerating montage, pacing
- **Average shot length (ASL) history.** Hollywood ASL fell from about 8–11 s (1930–60) to about 3–5 s, with outliers at 2.7 s. Bordwell calls the style "intensified continuity." [P] https://www.davidbordwell.net/blog/2007/05/27/intensified-continuity-revisited/ (summary via search; the full text is in Film Quarterly 2002). For comparison, the Opus film's 33 cuts in 20 s give an ASL of about 0.6 s, which is music-video or "hip-hop montage" territory.
- **Accelerating montage precedent.** *Requiem for a Dream* has about 2,000+ cuts against the typical 600–700. Aronofsky called his rapid inserts "hip hop montage", and the montages speed up as the story escalates. [T] https://nofilmschool.com/2017/07/watch-requiem-for-a-dream-editing · [P] https://catalog.afi.com/Catalog/moviedetails/53879
- **Trailer practice: edit to music, not to silence.** One trailer composer's blog argues that editing to silence wrecks pacing. [S] https://afx-industrial-filmscores.blogspot.com/2014/07/editing-trailers-to-music.html
- **Teaching:** Every Frame a Painting (Tony Zhou and Taylor Ramos). "How Does an Editor Think and Feel?" (9:25) https://www.youtube.com/watch?v=3Q3eITC01Fg and "Edgar Wright – How to Do Visual Comedy" (8:00), on framing, camera movement, editing and sound as joke delivery: https://www.youtube.com/watch?v=3FOzD4Sfgag. StudioBinder's "How to Pace Your Film" (17:04): https://www.youtube.com/watch?v=a9reuDw4cnU
- **For /bq-motion.** Encode a *cut-density curve*, not a fixed ASL. For example, start at about 1.5–2 s per shot, compress toward about 0.3–0.5 s at the peak, then hold one long shot for the title. Snap cuts to beats or subdivisions, and leave the shot before the reveal off the grid. (These numbers are a design recommendation drawn from the sources above, not a sourced rule.)

### 1.4 The silence before the reveal
- **Drop-out.** A sudden fall to near-silence just before the final hit makes the hit feel much bigger through contrast: "Dropping everything out for a beat makes the next impact feel enormous by contrast." [S] https://violetrecording.com/sound-design-for-trailers/
- **Music stop.** Called "arguably, the most useful trick a trailer editor can ever learn." [S] https://www.filmeditingpro.com/?p=11766 (Film Editing Pro, "The Art of Trailer Editing")
- **Riser gap.** Leave about half a second between the end of a riser and the boom. [S] same Violet Recording page, via search summary.
- **For /bq-motion.** The Fable film's near-silence before the title is this technique. The rule: no more than one drop-out per film, 0.3–1.0 s long, and keep room tone or a sub tail rather than digital zero. (Duration is a recommendation and UNVERIFIED as an industry standard.)

### 1.5 Hooks in the first 1–2 s (short form)
- **TikTok (official).** "Introduce your content proposition in the first 3 seconds"; "Prioritize your hook in the first 6 seconds"; build "suspense, surprise, or other emotions"; on-screen text at 5–10 words per second. [P] https://ads.tiktok.com/help/article/creative-best-practices
- **YouTube ABCD (Google/Ipsos, about 5,000 ads analysed).** "Having multiple shots in the first five seconds is a positive factor for Ad Recall and Consideration"; introduce the brand or product in the first 5 s; open on people if they appear; design for sound-off with title cards. [P] https://services.google.com/fh/files/misc/youtube_google_abcd_reference_guide_en.pdf · https://www.thinkwithgoogle.com/intl/en-gb/marketing-strategies/video/guidelines-great-creative
- **Caveat.** Branding in the first 5 s raises recall but can also raise skip rates. [T] https://www.thedrum.com/opinion/2022/06/22/how-capture-and-keep-user-attention-with-high-performance-youtube-ads
- **Widely quoted percentages** ("71% decide in 3 s", "50% of ad impact in 2 s", "90% of recall in 6 s"): **UNVERIFIED**. I could not trace them to a primary TikTok study. [S] https://segwise.ai/blog/tiktok-ad-best-practices-improve-performance
- **Long-form creators.** The leaked "How to Succeed in MrBeast Production" guide treats the first minute as "the most important minute" (Hook → Story → Payoff). Its authenticity is unconfirmed. [T] https://www.netinfluencer.com/mrbeast-productions-leaked-internal-document-rosanna-pansino/
- **Pattern interrupt (fall, break, impact).** No primary study found. The sourced principle is "suspense, surprise, or emotion" (TikTok), plus at least two shots in the first 5 s (Google). A physical event (something drops, cracks or snaps) in frame 1, with an SFX transient on frame 1, is a recommendation built on those sources. **UNVERIFIED** as a measured effect.

### 1.6 "Story told quickly" formats
- The sourced pattern is a single-idea feature film: one capability shown as a micro-story. Apple's "iPhone 17 Pro: Detectives Solve the Mystery with 8x Zoom" (1:06) and "iPhone 17: 3x More Scratch Resistant" (0:36) are both on Apple's official channel (section 6). The Google ABCD principles above apply.
- **Mid-2026 benchmark for UI and software films:** about 8.4 scene changes per minute, with videos of 0:45 or less rising from 10% to 23%. [S] https://advids.co/blog/ui-animation-motion-design-trends

---

## 2. Kinetic typography and motion design, 2026

### 2.1 Studios: what they're doing (sourced)
- **ManvsMachine.** Won a 2026 Red Dot for **Canva Affinity "Zero Bucks Given"**: "3D, 2D motion, kinetic typography and hand-drawn illustration" in "a seamless, fast-paced journey" through the product's flow, with real UI selection boxes and cursors in frame. Sound is by Zelig Sound. [P] https://www.red-dot.org/siegerprofile/manvsmachine/2026 · https://mvsm.com/project/canva-affinity · [T] https://www.stashmedia.tv/zero-bucks-given-manvsmachine-keeps-it-kinetic-for-canva/. The same studio made **OpenAI ~ Images 2.0** (60 s, May 2026) and **Google ~ Circle To Search** (61 s), both on ManvsMachine's Vimeo (section 6). This is direct evidence that a top studio makes AI-lab launch films.
- **BUCK, 2026 predictions.** (1) mascots return, "supercharged by AI"; (2) a swing back to visibly human work: "Imperfection is the signal, not the flaw"; (3) lo-fi artefacts (low frame rate, painterly boil, halftones) used as "deliberate creative signals"; (4) motion-first identity: "Static wordmarks are the new dinosaurs"; (5) texture and noise, neo-brutalism, "impact outweighs legibility", "analog textures". [P] https://pencilsdown.buck.co/p/looking-ahead-bucks-2026-predictions
- **Ordinary Folk.** "Distance" (3:27, uploaded 22 Oct 2026) is built from 900+ hand-painted frames. [P] https://www.youtube.com/watch?v=aonkZG7mZLI · https://www.ordinaryfolk.co/work
- **Gunner, Tendril:** no 2026-specific sourced findings. **UNVERIFIED**, so not reported.
- **Apple in-house.** No credit found for Apple's in-house motion team on the 2025–26 product films. Their craft is observable in the official films (section 6). One craft reference is ManvsMachine's 2018 iMac Pro artist film for Apple, which exists only as fan reuploads, so it is not listed.
- **Google Design and DeepMind.** The official "A new era of intelligence with Gemini 3" (1:57) and "Veo 3.1 – Designed to empower creatives" (1:31) are on the Google DeepMind channel. No studio credit found (**UNVERIFIED**).
- **Trend roundups** consistently name kinetic type as the top trend (because sound-off viewing puts the message in the text), plus hybrid 2D/3D, tactile texture and vertical-first. [S] https://designity.com/blog/2d-animation-trends-2026 · https://blog.videobolt.net/post/top-motion-graphics-trends-2026
- **A counter-signal from measured UI films.** Videos carried mainly by kinetic type fell from 47% to 35% during 2026. Captured real product screens rose from 37% to 63%, 3D fell from 23% to 13%, and light-look videos rose from 35% to 55%. This is 100 videos from 92 software companies, measuring production choices, not effectiveness. [S] https://advids.co/blog/ui-animation-motion-design-trends

### 2.2 Who made the Claude launch films
- **Model-launch films** ("Introducing Claude Opus 5.5", 0:20, 22 Sep 2026; "Introducing Claude Fable 5.2", 0:19, 9 Nov 2026, both on the official "Claude" channel): **maker UNVERIFIED**. The YouTube descriptions carry no credits. Anthropic's Creative Studio is described as an "in-house creative team responsible for the brand expression across Anthropic and Claude" that cares about "making things by hand and using AI when it makes sense". It hires a Video Director to own "video content for our most important moments" (model launches and product reveals) and to direct "editors, colorists, and sound designers". [P] https://jobs.accel.com/companies/anthropic/jobs/67758897-video-director-product-launches
- **Brand campaigns (credited):**
  - "Keep thinking" (Sept 2025, 90 s): agency Mother London, director **Daniel Wolfe**, production Love Song Films. [T] https://www.campaignlive.com/article/anthropic-launches-first-work-with-mother-for-ai-agent-claude/1933083 · https://creative.salon/articles/work/anthropic-claude-mother-keep-thinking
  - "Hope in Hard Questions": Mother, director **Myles McAuliffe**. [T] https://www.contentgrip.com/claude-hard-questions-film/ · https://www.adweek.com/creativity/anthropic-confronts-the-hard-questions-about-ai-responsibility/
  - "A Time and a Place" (Super Bowl, Feb 2026; spots "Treachery", "Deception", "Violation", "Betrayal"): Mother, director **Jeff Low**, Biscuit Filmworks London. [T] https://www.famouscampaigns.com/2026/02/claude-campaign-imagines-a-dystopian-ad-filled-future/
- **OpenAI "The Intelligence Age"** (Super Bowl 2025, 60 s, pointillist dot animation): Accenture Song with production by Builders Club. It was made by humans, with Sora used for exploration. [T] https://www.stashmedia.tv/?p=109845 · https://www.adweek.com/brand-marketing/chatgpt-openai-super-bowl-ad/

### 2.3 Practical takeaways for /bq-motion type
- Pair kinetic type with real UI captures. Text-only films are declining in software marketing; type layered over genuine product states, with selection boxes and cursors, is rising (ManvsMachine for Canva, advids data).
- Add a texture pass (grain, halftone, slight boil) as an intentional signal (BUCK), which also breaks the sterile AI sheen (section 3).
- Keep on-screen text at 5–10 words per second in short form (TikTok official). For launch films, a few serif words sitting on the anchor, as in the Opus film, stays well under that ceiling.

---

## 3. AI-video tells and how professionals avoid them

### 3.1 Tells: the owner's list, extended
| # | Tell | Source |
|---|---|---|
| 1 | Loud or unnatural breaths, *or* no breaths at all in cloned voice (voice-clone breath patterns) | [S] https://www.opus.pro/blog/ai-slop-aesthetic-12-tells |
| 2 | "TTS plateau" cadence: every sentence at the same level, no emphasis or acceleration | same |
| 3 | Clip-end deceleration: generators slow the camera toward the end of a clip, so naive joins read as a freeze or abrupt stop | [S] https://ocdevel.com/podcaster/ai-video-generation/091f7362-02ec-4afa-a4ff-e30e004db6db (single source, treat as a lead) |
| 4 | Floaty, "too smooth" camera with no micro-jitter; motion that glides with no contact evidence (feet, hands, props) | [S] opus.pro (above) · https://www.veo3gen.app/blog/runway-gen-4-slow-mo-complaints-veo3gen-11-motion-readability-fixes-when-your-cl |
| 5 | Hand morphs: merging fingers, changing digit counts | [S] opus.pro · https://www.itechguides.com/how-to-spot-physics-errors-in-ai-generated-videos/ |
| 6 | Physics breaks: objects float, sink into surfaces, or pass through each other; joints bend wrong | [S] itechguides (above) |
| 7 | Gibberish in-scene text that shifts between frames | [S] opus.pro |
| 8 | Inconsistent objects across shots (Coca-Cola's trucks gaining and losing wheels, "sometimes four wheels, sometimes ten") | [T] https://www.gamepressure.com/newsroom/sometimes-four-wheels-sometimes-ten-people-on-the-internet-counte/zc897d · https://www.thedrum.com/opinion/the-truck-is-different-in-every-scene-of-coca-colas-ai-christmas-ad-surely-that-matters |
| 9 | Inconsistent characters, colours or props between shots ("Air Head" balloon colour drifted between generations) | [T] https://cgpress.org/archives/shy-kid-on-using-sora-to-create-air-head.html |
| 10 | Flat, uniform, diffuse lighting in every shot, with no hard shadows | [S] opus.pro · multiproduktion (above) |
| 11 | Over-saturated palettes, orange skin | [S] opus.pro |
| 12 | Default stock look: "golden hour backlight, shallow depth of field, slow motion" stacked by prompt habit; slow motion also hides artefacts | [S] https://www.lilachbullock.com/why-ai-generated-videos-look-like-dreams/ (search summary) · https://getimg.ai/blog/slow-vs-fast-motion-in-ai-video-how-to-choose-the-right-speed |
| 13 | Lip-sync: lips don't close on b/p/m; vowel shapes all look alike | [S] opus.pro |
| 14 | Reflection or mirror errors; repeating texture tiles; background extras with impossible gaits | [S] opus.pro |
| 15 | Emotional flatness: technically better but "emotionally flat" (Coca-Cola 2025) | [T] https://www.techradar.com/ai-platforms-assistants/coca-cola-faces-backlash-again-for-missing-the-spirit-of-the-holidays-with-another-ai-slop-ad |
| 16 | Sudden reaction zooms on faces; frames that freeze suddenly | Owner's observations. No dedicated source found (**UNVERIFIED** as a documented tell). #3 is the nearest documented mechanism. |
| 17 | Centered, symmetrical "default" framing and fixed-angle headshots with too-perfect skin and slow blinking | [S] https://focalml.com/blog/why-ai-slop-is-flooding-tiktok-facebook-and-youtube-shorts (search summary); centred framing as such is UNVERIFIED |
| 18 | A generic music swell with no relationship to the cut | No source found. **UNVERIFIED** as a documented tell; see section 5 for the craft alternative. |

### 3.2 Fixes professionals actually use
1. **Over-generate and select hard.** Trillo kept about 55 of roughly 700 clips (~8%) and spent extra days editing [T] https://nofilmschool.com/ai-music-video. Higgsfield reports "800 generations. 8 shots that made the cut", including "when to abandon a generation" and "why the keyframe matters more than the prompt" [P] https://www.youtube.com/watch?v=-scKERL7PK0. The "Air Head" team "got a whole bunch of shots" and cut them to the voice-over, documentary-style [T] https://cgpress.org/archives/shy-kid-on-using-sora-to-create-air-head.html.
2. **Cut before the artefact.** End a shot about half a second early [S] multiproduktion (above). Trim the deceleration tail of every clip and match momentum across joins [S] ocdevel (above). In a fast montage, most shots are 0.3–1.0 s, which is shorter than most failure windows. (That last point is reasoning, UNVERIFIED.)
3. **Start from a controlled still (image-to-video), not raw text-to-video.** "Create a well-lit still image first — it gives you control, not chance." [S] multiproduktion. Google's guidance agrees: use a high-resolution, sharp source and describe only the motion. [P] https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/best-practice
4. **Fix in post.** Rotoscope, recolour drifting elements, remove extra objects, stabilise and upscale, as on "Air Head" [T] https://cgpress.org/archives/shy-kid-on-using-sora-to-create-air-head.html. Hide hands by framing them out, choosing takes, or masking in real hands [S] opus.pro.
5. **Finish in a fixed order.** Normalise the footage first, then stylise with one base LUT per look so the film reads as one piece. Grade before upscaling and add grain after the grade. Grain on 35 mm footage at 8–15% opacity breaks up the over-clean surface; keep it subtle. These numbers are vendor guidance. [S] https://invideo.io/blog/luts-film-grain-ai-video/ · https://invideo.io/blog/ai-video-post-production-pipeline/
6. **Use motivated light and lens choice.** Strong contrast and a named lens (85 mm portrait, 24 mm wide) with foreground, midground and background separation for parallax. [S] multiproduktion
7. **Spend as much time on sound as on image generation.** [S] multiproduktion
8. **Hybrid workflows: use AI only where it earns its place.** Trillo mixes hand-drawn, 2D/3D and AI ("Craft always outlasts shortcuts") [T] https://motionographer.com/2025/05/20/paul-trillo-hacking-cinemas-next-level/. Anthropic's studio describes itself as "making things by hand and using AI when it makes sense" [P] (job ad above). OpenAI's Super Bowl film was human-made, with Sora used only to explore [T] https://www.stashmedia.tv/?p=109845. The trend data favours real UI captures over drawn ones [S] advids.
9. **Avoid the subjects AI handles badly.** Coca-Cola's 2025 ad swapped people for animals to dodge uncanny humans, but critics still found it emotionally flat. [T] https://www.implicator.ai/coca-cola-debuts-ai-holiday-ads-animals-replace-actors-after-2024-backlash/
10. **Voice.** Treat breaths by reducing the loud ones and keeping the natural ones, rather than deleting them all (iZotope RX Breath Control, or similar tools). [S] https://cleanvoice.ai/blog/remove-breathing-from-audio/ · https://auphonic.com/blog/2023/11/29/eliminate-breathing-sounds-and-mouth-noises/

### 3.3 Gate items for /bq-motion (recommended)
An "AI-tell QA" pass on every AI shot: hands, text, physics, end-tail deceleration, cross-shot prop consistency, uniform-lighting check and stock-look check. Run the consistency checks across shots too (same product shape, colour and wheel count). Reject on any hit; don't patch in prompts. Also log the selection ratio as evidence of having looked.

---

## 4. Google Flow / Veo / Omni: current best practice (as of 2026-11-12)

### 4.1 Models and limits in Flow (official help page)
Source: [P] https://support.google.com/flow/answer/16352836?hl=en
- **Omni Flash 1.2** (recommended: "higher visual quality and consistency, longer video lengths, and duration-based pricing")
  - Text-to-video, Frames-to-video, Ingredients/references, Video-to-video edit: 3–10 s on free plans, **3–15 s on AI Plus, Pro or Ultra**. Both aspect ratios.
  - **Extend (Omni Extend):** paid plans only, 3–10 s per extension, up to 3 images. Web only.
  - Native resolution **360p or 720p**; 360p costs one-third the credits. **Upscale** (paid) to 1080p, or 4K on Ultra.
  - Custom voices (preset base voice plus a style description); some features are region-restricted.
- **Omni Flash 1.1:** 4/6/8/10 s, no extend. **Retires 5 Dec 2026.**
- **Veo 3.1 Lite:** 720p, 4/6/8 s; ingredients 8 s only; no edit or extend.
- **Veo 3.1 Fast:** 4/6/8 s; ingredients 8 s. **Retires 5 Dec 2026.**
- **Veo 3.1 Quality:** 4/6/8 s; no ingredients, edit or extend. **Retires 5 Dec 2026.**
- **Veo Extend retired 5 Nov 2026.**
- **Image models for frames and ingredients:** Nano Banana Pro (default on Ultra), Nano Banana 2.1, Nano Banana 2 Lite (free).
- **Background:** Omni was announced at I/O on 19–20 May 2026 as Google DeepMind's model family for generating and editing video from any input. Flow was renamed "Google Flow", and all Omni output carries a SynthID watermark. [T] https://thenextweb.com/news/google-gemini-omni-flash-video-model-io-2026 · [P] https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/
- **"Veo 4"** has not been announced by Google. Pages selling it are not credible. [S] https://dev.to/tokenmixai/veo-4-doesnt-exist-yet-but-people-are-already-selling-it-3ch9

### 4.2 Editing and scene tools in Flow (official)
Source: [P] https://support.google.com/flow/answer/16935718?hl=en · https://support.google.com/flow/answer/16353334?hl=en
- **Video-to-video edit (Omni Flash 1.2).** Upload up to 60 s and 1 GB (videos over 30 s must be trimmed to 30 s), then edit a selected segment of up to 10 s, or 15 s on paid plans. You get "up to 3 conversational turns" before context is lost. Edits cost the same per second as generation.
- **Extend.** "You can add up to 3 image references to guide character and environmental consistency." Insert, remove and camera edit modes **cannot** be applied to extended clips.
- **Scenebuilder.** Add clips, reorder, trim with handles, preview and download. Save any paused frame as an image and reuse it as an ingredient, start frame or end frame.
- **Ingredients.** Reference characters with `@Name` (`@me` = your avatar). Describe *how* each ingredient appears. Use a plain or segmented background for product references. Keep ingredient images consistent in look, and don't let the text contradict them. Voice references (`@Voice: Name`) work only in ingredient-based generations.
- **Agent mode** can return batch variations, e.g. "Give me 5 variations of this video with different lighting."

### 4.3 Prompting: what works (official guidance)
- **Omni structure.** Shot framing and motion, style, lighting, location, action. Omni infers detail from world knowledge, so it needs less prescriptive prompts than Veo. [P] https://deepmind.google/models/gemini-omni/prompt-guide/
- **Camera vocabulary that Google documents:** "one continuous shot" / "oner", "static" / "locked off" / "fixed", "push in", "punch in", "dolly zoom", "natural smartphone zoom", "film camera", "webcam style". Camera angle, point of view and movement can also be edited conversationally. Moves can be sequenced in one prompt, e.g. "a close-up on his shoes, quickly tilting up to medium shot, then widening." [P] same.
- **Default is multi-shot.** For one shot, include "In a single continuous shot" and "No scene cuts." [P] https://aistudio.google.com/docs/omni
- **No negative prompts.** Write "Do not X" inside the prompt. [P] same.
- **First/last frame.** Define the first frame, the move or transition, and what the last frame reveals [P] DeepMind guide. Interpolation is 3–10 s; two-frame interpolation over 10 s errors [P] AI Studio docs. A third-party test found Veo 3.1 first-to-last interpolation unreliable [S] https://www.datacamp.com/tutorial/veo-3-1-complete-guide-with-examples.
- **References (API).** Up to 6 reference images, up to 3 images per character for up to 2 characters, and reference videos of up to 3 s each. The old `<FIRST_FRAME>` / `<IMAGE_REF_0>` tags are deprecated; describe each input's role in plain language. [P] https://aistudio.google.com/docs/omni
- **Edits.** Change one thing at a time ("Change the butterfly to a bee."). Over-descriptive edit prompts cause unintended changes. [P] DeepMind guide and AI Studio docs.
- **Storyboards.** Supply a storyboard image with "Follow the story exactly in order starting top left." [P] DeepMind guide.
- **Complex actions:** name them rather than describing them frame by frame. **On-screen text:** specify type, placement, animation and exposure. **Audio sync:** e.g. "in sync with the music". [P] DeepMind guide.
- **Consistency across scenes.** Name the character, fix their unchangeable traits, and paste the identical description into every prompt, changing only action and setting. Use the same seed where available. [P] https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/best-practice
- **What fails.** Chaining several events (A, then B, then C) in one short clip "often leads to muddled or incomplete videos". Vague "make it move" prompts. Re-describing the source image in image-to-video. Quotation marks around dialogue, which can render as on-screen text; use a colon instead. [P] same Google Cloud page.
- **Third-party tip (UNVERIFIED).** Put camera movement at the end of the prompt and avoid vague words like "dynamic camera" or "cinematic angle". [S] https://framia.converge.ai/page/en-US/news/gemini-omni-flash-prompt-guide

### 4.4 Conflicts and limits to note
- **Maximum extended length:** the DeepMind guide says 10 s increments up to **40 s** total, while the API docs say up to **30 s** total. **Unresolved**; test in Flow.
- Editing or extending uploaded videos is unavailable in the EEA, Switzerland and the UK. Uploading images of certain recognisable people is not supported. [P] https://aistudio.google.com/docs/omni
- Multi-video prompting "may result in degraded model performance or unexpected outputs." [P] same.

### 4.5 Recommended Flow recipe for /bq-motion (derived from the sources above)
1. Lock the look as stills first, using Nano Banana Pro or 2.1 for keyframes with the anchor composition (e.g. the horizon curve) in the same pixel position.
2. Generate each shot with Frames-to-video or Ingredients on **Omni Flash 1.2**, specifying "In a single continuous shot … No scene cuts." Use one action per clip and one named camera move.
3. Generate 3–6 variations per shot (Agent mode) and keep the best ~10%.
4. Trim the head and tail of every clip, since clip-end deceleration is a documented risk. Most montage shots will be under 1 s anyway.
5. Assemble, grade, add grain and sound outside Flow. Flow's Scenebuilder is for rough assembly only.
6. Plan for the 5 Dec 2026 retirements: don't build presets on Veo 3.1 Fast or Quality.

---

## 5. Sound for motion films

### 5.1 Risers, impacts, drops on the logo
- **Elements:** braams; risers (pitched plus noise, timed so "their peak lands exactly on the impact"); hits built from transient, body and sub layers with aligned attacks; whooshes on camera moves and logo reveals; sub drops under major hits (reserve the deepest for key moments); a tension bed under everything. [S] https://violetrecording.com/sound-design-for-trailers/
- **Structure:** escalate in waves and save the biggest impact, the "button", for the end. Avoid wall-to-wall sound, which leaves no contrast. Duck design elements under any title card. [S] same.
- **Music stop and drop-out before the title:** section 1.4.
- **Brand-level reference:** OpenAI's "Sound on for Sora 2" (2:14) is a sound-led launch film on the official OpenAI channel (section 6).

### 5.2 Ducking
- No universal number. Practitioners range from a gentle 3–6 dB automation dip (one mixer "maybe 4 dB", often drawn by hand rather than sidechained) to 15–20 dB+ in software presets. Ducking by only a couple of dB already makes a large difference. [S] https://gearspace.com/threads/ducking.124469/ · https://www.soundonsound.com/techniques/duck-tales · https://larryjordan.com/articles/adobe-audition-automatic-music-ducking/ · https://composer-docs.vindral.com/operators/operators-sidechain-ducking.html
- **Recommendation:** hand-draw music automation around voice-over phrases (about 4–8 dB), and duck the bed under each hit via sidechain. [S] Violet Recording.

### 5.3 Loudness for social, and why a crushed −6 LUFS trailer sounds cheap
- **Spotify:** "We adjust tracks to −14 dB LUFS, according to the ITU 1770 standard". If a master is louder than −14, keep true peak below −2 dB. [P] https://support.spotify.com/artists/article/loudness-normalization/
- **YouTube:** normalises to about −14 LUFS (since 2015; exactly −14 LUFS since 2019). Louder content is turned down, and crushed masters "will often sound worse". "Dynamic is the new Loud." [T] https://productionadvice.co.uk/youtube-loudness/ (Ian Shepherd)
- **Why −6 LUFS sounds cheap:** it gets about 8 dB of gain reduction on playback, so it ends up no louder than a −14 mix but with flattened transients, pumping and distortion. Impacts lose punch exactly where a launch film needs it. [S] https://www.masteringbox.com/learn/mastering-for-streaming · [T] productionadvice (above)
- **Instagram and TikTok:** no official loudness target published. Third-party claims range from −14 to −16 LUFS (**UNVERIFIED**). [S] https://opus.pro/blog/best-loudness-normalizers
- **Recommendation for /bq-motion:** −14 LUFS integrated, ≤ −1 dBTP (≤ −2 dBTP if the master runs hotter), and keep real dynamic range for the drop-out and the hit. This matches the existing BeQuite `promo-sound-voice` target of −14 LUFS.

### 5.4 Voice-over or none for launch films
- **Evidence from the films themselves:**
  - Apple's product films ("Introducing iPhone 17 Pro") carry narration [T] (search summary of the film; see section 6).
  - Anthropic's Opus 5.5 and Fable 5.2 launch films are about 20 s with no VO (owner's local analysis).
  - "Keep thinking" ends on on-screen text: "Keep creating, researching, learning, coding … Keep thinking." [T] https://www.campaignlive.com/article/anthropic-launches-first-work-with-mother-for-ai-agent-claude/1933083
  - Google ABCD says to design title cards that work with the sound off. [P] ABCD guide.
- **Recommendation (reasoned, not a sourced rule):**
  - Under ~30 s brand or reveal films: no VO; music plus SFX plus a few words of type.
  - 45–120 s feature-explainer films: VO earns its place, treated per section 3.2 #10.
  - Short-form social: type must carry the message regardless, because of sound-off viewing.

---

## 6. Download list (every URL was checked on 2026-11-12 for channel, length and upload date)

**Legal note.** YouTube's Terms of Service forbid downloading content except where the Service allows it, with prior written permission, or as applicable law allows. [P] https://www.youtube.com/t/terms. For a private study library, prefer Vimeo's download button where the owner has enabled it, official press kits, or store the links and watch online. Library copies must stay private and are for study, not reuse.

Already in the owner's library, not repeated: "Introducing Claude Opus 5.5" (Claude, 0:20) https://www.youtube.com/watch?v=1f13Bl1sYkw and "Introducing Claude Fable 5.2" (Claude, 0:19) https://www.youtube.com/watch?v=6a1QSJlsYpU.

| # | Title | Maker (channel) | URL | Length | What to learn |
|---|---|---|---|---|---|
| 1 | Keep thinking with Claude | Anthropic / Mother London, dir. Daniel Wolfe | https://www.youtube.com/watch?v=FDNkDBNR7AM | 1:30 | Live-action montage of real problem-solvers that resolves into a type-led sign-off |
| 2 | Introducing Claude Design by Anthropic Labs | Claude (official) | https://www.youtube.com/watch?v=t_LBECIQQqs | 1:22 | How Anthropic films its own UI: pace and restraint in a product reveal |
| 3 | This is Sora 2 | OpenAI (official) | https://www.youtube.com/watch?v=lEcg6AJ6DVY | 0:58 | An AI lab showcasing its own model: shot selection and pacing of generated clips |
| 4 | Sound on for Sora 2 | OpenAI (official) | https://www.youtube.com/watch?v=1PaoWKvcJP0 | 2:14 | Sound-led launch: how audio carries a reveal |
| 5 | OpenAI Super Bowl 2026: "You Can Just Build Things" (Codex) | OpenAI (official) | https://www.youtube.com/watch?v=aCN9iCXNJqQ | 1:00 | A broadcast-length developer-product story told quickly |
| 6 | The Intelligence Age (Super Bowl 2025) | Accenture Song / Builders Club for OpenAI (**reupload, not an official channel**) | https://www.youtube.com/watch?v=N9NeQi2pE7U | 1:00 | A single graphic system (dots) carrying a whole history: the closest cousin of the constant-horizon idea |
| 7 | OpenAI ~ Images 2.0 | ManvsMachine (Vimeo) | https://vimeo.com/1188405597 | 1:00 | A top motion studio's take on an AI-lab launch (May 2026) |
| 8 | A new era of intelligence with Gemini 3 | Google DeepMind (official) | https://www.youtube.com/watch?v=98DcoXwGX6I | 1:57 | Google's flagship-model film grammar for comparison with Anthropic's |
| 9 | Introducing Gemini Omni: Create Anything from Anything | Google (official) | https://www.youtube.com/watch?v=KUyRq7szZsM | 0:55 | What the owner's Flow model can do at its best (May 2026) |
| 10 | Veo 3.1 – Designed to empower creatives | Google DeepMind (official) | https://www.youtube.com/watch?v=I06Ef8alr2Y | 1:31 | Google's own curation of Veo shots: which shot types it trusts |
| 11 | iPhone 17 Pro: The most powerful iPhone ever | Apple (official) | https://www.youtube.com/watch?v=TNhX1uR2vO8 | 1:00 | 3D product film: material close-ups, light sweeps, VO rhythm |
| 12 | iPhone Air: Incredibly light and thin with pro-level performance | Apple (official) | https://www.youtube.com/watch?v=sKJ0_NNcJzI | 0:54 | Selling one physical idea (thinness) through camera and scale |
| 13 | AirPods Pro 3 | Apple (official) | https://www.youtube.com/watch?v=EMmKs8vMKhU | 0:48 | Small-object 3D product choreography and macro detail |
| 14 | MacBook Pro with M5 Pro and M5 Max | Apple (official) | https://www.youtube.com/watch?v=GriXfu4tL30 | 1:41 | Spec-heavy film that stays cinematic: type and spec reveals |
| 15 | iOS 26: Introducing Liquid Glass | Apple (official) | https://www.youtube.com/watch?v=jGztGfRujSE | 4:34 | Apple-level UI motion: material, refraction, component morphs |
| 16 | Created live on Mac: "Surrender" by Labrinth | Apple (official, 10 Nov 2026) | https://www.youtube.com/watch?v=YaPx9scLwfk | 0:31 | Newest Apple short: music-first 30 s product story |
| 17 | iPhone 17 Pro: Detectives Solve the Mystery with 8x Zoom | Apple (official) | https://www.youtube.com/watch?v=leYJBhat7zw | 1:06 | One feature as a micro-narrative (story told quickly) |
| 18 | iPhone 17: 3x More Scratch Resistant | Apple (official) | https://www.youtube.com/watch?v=PBrYMBacnyM | 0:36 | Single-claim demo ad with a physical-impact hook |
| 19 | Shot on iPhone: "Glad I Met You", a Film for Chinese New Year | Apple (official) | https://www.youtube.com/watch?v=XLzx58UrwGs | 11:56 | Narrative "Shot on iPhone" long-form: emotion first, product invisible |
| 20 | Shot on iPhone: The Making of "Glad I Met You" | Apple (official) | https://www.youtube.com/watch?v=J2OGTd8Zgow | 3:09 | How Apple frames craft and BTS as marketing |
| 21 | Canva Affinity ("Zero Bucks Given", 30 s cut) | ManvsMachine, sound by Zelig Sound (Vimeo) | https://vimeo.com/1132498646 | 0:30 | Red Dot 2026: kinetic type mixed with 3D, 2D and real UI selection boxes (project page https://mvsm.com/project/canva-affinity) |
| 22 | Google ~ Circle To Search | ManvsMachine (Vimeo) | https://vimeo.com/903755364 | 1:01 | Gesture-driven UI feature film; the hand as the transition |
| 23 | Samsung ~ Micro Miracles | ManvsMachine (Vimeo) | https://vimeo.com/902218343 | 1:00 | Macro 3D product world-building |
| 24 | Distance | Ordinary Folk (official, Oct 2026) | https://www.youtube.com/watch?v=aonkZG7mZLI | 3:27 | 900+ hand-painted frames: the "visibly human" 2026 counter-trend |
| 25 | Buck Sizzle Reel – Oura: Ring True to You | BUCK (Vimeo) | https://vimeo.com/1123588726 | 0:41 | BUCK's product-campaign pacing and finish |
| 26 | Introducing Linear Agent | Linear (official) | https://www.youtube.com/watch?v=mRql2VJ99gM | 0:55 | Restrained, premium software UI film with real product states |
| 27 | All the launches at Config 2025 | Figma (official) | https://www.youtube.com/watch?v=NHodnYFUT_I | 1:22 | Many launches in about 80 s: kinetic type plus UI, a fast-list structure |
| 28 | Phone (3): Come to Play | Nothing (official) | https://www.youtube.com/watch?v=MHGQRnvE9GQ | 0:30 | Brand-world 3D and dot-matrix type in a 30 s teaser |
| 29 | Do your lesson, no buts. | Duolingo (official) | https://www.youtube.com/watch?v=QPjgXWm7F6c | 0:06 | A 6-second ad: hook, joke and brand with zero setup |
| 30 | Hell Grind – Official Trailer (Higgsfield Original Series) | Higgsfield AI (official) | https://www.youtube.com/watch?v=CVzfQuC0aMU | 3:08 | State of the art in all-AI trailers; also study where it still reads as AI |

**Study videos** (craft teaching; keep as links, not library clips)

| Title | Maker | URL | Length | Why |
|---|---|---|---|---|
| How Does an Editor Think and Feel? | Every Frame a Painting | https://www.youtube.com/watch?v=3Q3eITC01Fg | 9:25 | Cutting on emotion and instinct |
| Edgar Wright – How to Do Visual Comedy | Every Frame a Painting | https://www.youtube.com/watch?v=3FOzD4Sfgag | 8:00 | Rhythm, sound-sync cuts, fast inserts |
| Ultimate Guide to Scene Transitions | StudioBinder | https://www.youtube.com/watch?v=TKXBAaQB03U | 19:29 | J/L-cuts, smash cuts, match cuts |
| Creative Match Cut Examples | StudioBinder | https://www.youtube.com/watch?v=ptXlYulVAsM | 6:44 | Graphic match catalogue |
| Walter Murch and In the Blink of an Eye | StudioBinder | https://www.youtube.com/watch?v=PKYeClvvlTw | 15:05 | Rule of Six |
| 2001: Bone to Satellite | Movieclips | https://www.youtube.com/watch?v=avjdKTqiVvQ | 2:43 | The canonical graphic match |
| "Notes To My Future Self" VFX Breakdown | Paul Trillo (Vimeo) | https://vimeo.com/939660277 | 1:12 | Hybrid AI and live-action compositing |
| How to Make AI Films That Don't Look AI | Higgsfield AI | https://www.youtube.com/watch?v=-scKERL7PK0 | 3:05:51 | Selection ratio, "slop vs cinema", keyframe-first |

**Not listed (could not confirm an official upload):** Apple "The Greatest", Apple "Underdogs", Spike Jonze's HomePod "Welcome Home" (only reuploads found), Anthropic's "A Time and a Place" Super Bowl spots (only reuploads and case studies found), and the ManvsMachine iMac Pro film (only reuploads found).

---

## 7. Gaps and open items
- Who made the Claude Opus 5.5 / Fable 5.2 launch films: **UNVERIFIED**.
- Gunner and Tendril 2026 work: not researched successfully.
- Motion Awards 2026 (edition X) winners are due in December 2026, so not yet available. [P] https://motionawards.com/
- Official Instagram and TikTok loudness targets: not published.
- Omni's maximum extended length is 30 s or 40 s depending on the source; test in Flow.
