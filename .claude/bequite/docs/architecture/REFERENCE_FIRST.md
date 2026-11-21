# Reference-first doctrine and the human test

Status: approved by the owner (2026-11-21). Skills that carry it: `bequite-human-taste` (gates and loop), `bequite-writing-dna` (voice), `bequite-video-intel` (references on video). Last verified 2026-11-21.

## 1. The rule

BeQuite does not invent a look, a voice or a motion from its own defaults. Every creative output (writing, a page, a film, a post, an image) starts from human work that was studied and measured, and it is compared with that work before it is delivered.

Two gates, in every creative work folder:

- `REFERENCES_STUDIED`: at least three references were collected from named sources and measured; the measurements are in `references.md`.
- `HUMAN_TEST_PASSED`: the output went through the test in section 5 and the result is in `evidence.md`.

No creative command produces a final output while the first gate is open. If the owner supplies the references, the agent studies those; if not, it finds them (section 3) and shows them before producing.

## 2. The loop

1. **Collect.** 3 to 10 references for a design or a film; 30 to 50 posts for a voice. Record source, date and why each was chosen.
2. **Measure, never describe.** Numbers and facts: font family and sizes, column grid, palette as hex, cut rate, hook length in seconds, sentence lengths, punctuation habits. "Clean and modern" is not a measurement.
3. **Extract the DNA.** Rules, each with one example from the references, plus a list of what the references never do.
4. **Produce in that grammar.** Deviations are allowed when they are chosen and written down.
5. **Human test** (section 5).
6. **Learn.** Every correction from the owner becomes a rule with its example (`/bq-taste`), so the same correction is never needed twice.

## 3. Where to look and what to measure (the reference orchestra)

All sites below answered on 2026-11-21 (several refuse scripts and need the browser).

| Domain | Where to look | How to capture | What to measure |
|---|---|---|---|
| Web pages | awwwards.com, godly.website, land-book.com, siteinspire.com, lapa.ninja, minimal.gallery, httpster.net, framer.com/gallery | Open the live site in the browser; full-page screenshots at desktop and phone width | Section order, grid, type scale, font families, palette, spacing rhythm, image treatment |
| Web motion (scroll, 3D, live backgrounds) | tympanus.net/codrops, awwwards "sites of the day", the live reference site itself | Inspect the page: loaded scripts, canvas/WebGL, CSS; record a scroll pass | Which technique makes the effect (GSAP ScrollTrigger, Lenis, Three.js, video, CSS scroll timeline), durations, easing, what happens on a phone |
| Components and product UI | 21st.dev, mobbin.com, refero.design, figma.com/community | Screenshots of the flow; component source where it is open | States, density, radii, shadows, empty and error states |
| Mood and art direction | pinterest.com, savee.it, cosmos.so, are.na, behance.net, dribbble.com | Board of 10 to 20 images | Palette, texture, composition, lighting |
| Type | fontsinuse.com, typewolf.com | Screenshots | Pairings, sizes, tracking, where each family is used |
| Films, ads, title design | `motion-library/` (58 studied films), vimeo.com/channels/staffpicks, motionographer.com, stashmedia.tv, artofthetitle.com | The video ladder (`bequite-video-intel`) | Cut rate, sync to the beat, type size and placement, camera moves, palette, sound arc |
| Kinetic type | A reference the owner or the agent picks | Frames at 6 fps for the showcase part | Word-by-word timing, how words push, camera travel, blur, zoom range |
| Short video in a niche | TikTok Creative Center (by region), YouTube, the niche's top accounts | Ladder L0 to L3 | First 3 seconds, cut rate, captions, structure, length, sound |
| A voice (page, account, the owner) | The real page in the owner's browser | 30 to 50 posts copied as text with date and reactions; private, never shipped | Section 4 |

## 4. Learning a voice (writing DNA from a real page)

Measured on the collected posts:

- Length: words per post and per sentence, and how much they vary.
- Punctuation: which marks are used, which are never used, spaces and line breaks.
- Language: dialect or formal, mixing, particles and fillers, spelling habits, elongations, typos that are part of the voice.
- Openers and closers: how posts start and end.
- Devices: questions, teasing, exaggeration, running jokes, how the page pokes rival fans.
- Emoji and hashtags: how many, where.
- What performs: the ten posts with the most reactions, and what they share.
- Never-list: things the page never does.

Output: `WRITING_DNA.md` with rules, ten real posts as exemplars, the never-list and the measured numbers.

Boundary: the agent learns how a kind of page writes and writes new posts in that manner. It does not copy posts, pose as that page or person, or promise to beat AI detectors. For the owner's own voice there is no limit beyond the owner's approval.

## 5. The human test

1. **Side by side.** The output next to three references at the same size. List five differences. Each one must be a choice, not a default; fix the defaults.
2. **Tell sweep.** Run the list for the medium (section 6). Every hit is fixed or justified in one line.
3. **Blind pick (writing).** Three generated posts mixed with seven real ones. A fresh subagent on a cheap model, with no context, picks the generated ones and says why. Pass: it finds one or none. Its reasons become fixes.
4. **Phone check (design, video).** Looked at on a phone-width screen, at arm's length, for five seconds: what is remembered?
5. **The owner's eye.** The owner's verdict is final and is logged. Corrections go to the DNA.

## 6. Tell lists (starting set; Opus validates and extends each against real references)

**Writing, English:** inflated importance ("stands as a testament"); groups of three; "not just X but Y"; a dash every other sentence; vague sources ("experts say"); a closing line that sums up the moral; promotional adjectives; even sentence lengths; everything in bullets; emoji as headings. Word lists drift with each model generation (mid-2026 models write short sentences in an 8-20 word band); structure outlasts vocabulary. Full list and the "ineffective indicators" not to chase: `bequite-writing-dna/references/tells-en.md`.

**Writing, Arabic** (tested 2026-11-21 on 47 human posts vs 12 default-model posts; numbers in `bequite-writing-dna/references/tells-ar.md`): a comma after every clause and a full stop after every sentence (about 2x the human rate); one unbroken paragraph where the genre breaks lines; even post lengths; a closing moral or a call on most posts; "label:" openers; no emoji, ellipsis or exclamation where the genre uses them; inline أولاً / ثانياً / ثالثاً; a dialect that does not match the page; perfect spelling where the page has habits; translated English idioms. Dropped after testing: "no particles" (same rate as humans) and formal Arabic in itself (the default model wrote Egyptian colloquial unprompted).

**Design (web pages):** purple-to-blue gradients and gradient backgrounds; gradient headline text; section labels "01 / 02 / 03" above every section; a thin body font with every heading in bold, the same two weights everywhere; glass cards everywhere; centred hero, three feature cards, testimonial grid; emoji as icons; one radius and one shadow for everything; perfect symmetry; vague copy. The first four were named by the owner as the ones that give away ChatGPT and Claude pages. Scope: the numbered-section tell is about web pages. In video, numbered chapter cards are a human device: the top Arabic Claude course of October 2026 (225K views) uses "05" / "11" cards over each chapter title.

**Presentations and documents:** note boxes under paragraphs with a coloured left border (orange, yellow) and a "Pro tip" or "Key takeaway" label; a title plus three bullets on every slide; every slide in the same layout; emoji bullets; a summary slide that repeats the deck. Named by the owner.

**Motion:** the same ease on everything; fade-and-scale for every entrance; cuts that ignore the beat; letter-by-letter typing with no reason; glow on everything; a whoosh on every move; a camera that drifts with no motive; zooming in too far.

**Images:** plastic skin, garbled text, mirrored faces, the generated sheen. Prefer a real photo, a real screenshot or a drawing made in code.

## 7. The options board (what "orchestra" means for any task)

Before a plan is approved, the plan lists every route this machine offers for the job and picks one with a reason. The routes come from `.bequite/state/CAPABILITIES.md`, which `/bq-init` builds and `/bq-doctor` refreshes:

- detected: programs on the machine (After Effects, Premiere, Photoshop, Blender, DaVinci Resolve, ffmpeg, yt-dlp, Whisper, Node, Python), connected MCP servers, browsers;
- asked once: which paid tools and accounts the user has, and which browser and profile the agent may use for research (the agent asks, it does not assume; credentials are never stored);
- suggested: when a paid tool would clearly help, the agent names it, the price and what it would replace, and the user decides.

Example for "an image for the hero section": a real photo from a free library; a screenshot of the real product; a drawing in code; a Blender render; image generation through an account the user already has. The plan shows the five and recommends one.

## Sources

- Wikipedia, "Signs of AI writing": https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing (coverage: https://techcrunch.com/2025/11/20/the-best-guide-to-spotting-ai-writing-comes-from-wikipedia/)
- blader/humanizer skill (built on that guide; warns that removing patterns is half the job, voice is the other half): https://github.com/blader/humanizer
- Reference sites: reachability checked by request on 2026-11-21.
- Owner's corrections during work 0001 (film v9 to v14): flat drawings rejected, type must follow the light's angle, whole words instead of typing, less zoom.
