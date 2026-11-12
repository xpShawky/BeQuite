# Studying references

Most important first: **never trust memory of a film.** Study it from frames you extracted in this session, or say it is UNVERIFIED. Steal the idea, not the look.

## 1. Library first (M1)

1. Read `motion-library/INDEX.md` (one row per studied film: category, story in one line, signature technique, when to use).
2. Pick 2–3 rows that fit the brief and offer them as options with a reason each: "Like A (one guide element ties several features together) or like B (whips with heavy blur; 'easy' is the message)."
3. Open the chosen `refs/<slug>/breakdown.md` for beats and timestamps. If the row says "redo" or the breakdown is missing, study the film again before relying on it.
4. Nothing fits → ask the user for references, or research (web, studio case studies, breakdown videos), then study what they supply. Add every new study to the library (`motion-library/README.md` explains the layout and the copyright rule: media stays local, only breakdowns are tracked).

## 2. Frame study

Commands live in one place: `.claude/skills/bequite-render-pipeline/references/adapter-ffmpeg.md` § "Studying a film". The method:

| Pass | What it gives |
|---|---|
| 1 fps contact sheet of the whole film | structure, scene list, colour and layout system |
| 4 fps sheets of each fast moment | text treatments, transitions, pops (a 200 ms pop falls between 1 fps samples) |
| 12–15 fps frames of one 2–3 s moment | how a single effect is built (easing, blur, masks) |
| scene detect (thresholds 0.35 and 0.2) | hard cuts vs continuous moves |
| motion energy per 0.2 s | the rhythm: bursts, settles, holds |
| audio: voice yes/no, tempo, loudness | pace of the read, where the music drops |

Creator posts often film a monitor ("POV: you make ads…"). Study and deliver the **screen content**, not the phone framing.

## 3. What to write per reference (`research.md` or the library breakdown)

```markdown
### <name> (<source>, <length>, <format>)
- Story in one line:
- Beats: | # | time | picture | text | motion + speed | transition out |
- Signature technique(s) with timestamps (00:04.2):
- Text: entrance / emphasis / exit / duration per line
- Colour + type system: stage, accent and what it marks, family, sizes vs frame height
- Rhythm: beats per 10 s, longest hold, end-card hold, where the music drops
- Take (named): "this easing", "this word swap", "this object wipe"
- Avoid (named):
- Studied from: frames at N fps (no real-time playback) → smoothness and sound judgements UNVERIFIED
```

Split references by job: one film rarely gives you colour, type, motion, transitions, pacing and sound at once.

## 4. Model-assisted video analysis (optional)

Some multimodal models accept video. Facts that were true when this was written (re-check the vendor docs): sampling defaults can be as low as 1 frame per second, which misses fast pops; some APIs let you raise the sampling rate, clip a section and raise media resolution; timestamps drift by a second or more. Rules:

- Use the API/studio surface that exposes sampling rate and clipping, not a consumer chat app, when you need detail.
- Send a slowed copy (25 % speed) and state the factor; put the prompt after the video.
- Ask for **observable evidence** (what moves, over how many frames, how the cut is hidden), not "which plugin was used".
- Spot-check every timestamp against your own frames. Cross-check two models; where they disagree, look yourself.
- Models that take only images: send numbered frames and the fps.

Prompt templates (adapt the product line):

**Beat map** — "You are a motion-design editor. Watch the whole video, including audio. Return one row per beat: start MM:SS.f · end · duration · visual · exact on-screen text · exact VO · music event (drop, hit, silence, riser) · transition into the next beat. Then: total beats, average beat length, longest hold, where and how long the logo holds, where the music drops, VO words per second. Describe only what you can see or hear; write 'unclear' instead of guessing."

**One effect** — "Focus only on 00:12–00:16 (slowed to 25 %; real time = video time / 4). Frame by frame: what moves, scales, rotates, blurs, is masked or recoloured; direction and easing (linear / ease-out / overshoot / spring); motion blur, depth of field, camera move; how the transition hides the cut. Propose two ways to rebuild it and the visual evidence for each. Mark uncertainty."

**System extraction** — "Extract the design system: background colours (approx hex), accent(s) and what they mark, type style and weights, sizes vs frame height, grid and margins, shadow and glass use, device frames, easing and speed. Give three rules this film never breaks."

**Critique of our render** — "Draft product film for <audience>. Watch once at normal speed as a first-time viewer. With timestamps: text on screen too briefly to read twice; motion that feels jerky or too fast; moments where the eye doesn't know where to look; any frame that looks AI-generic or stock. Be blunt; fix what is there, don't add features."

## 5. Using other AIs for ideas

AI design converges on the statistical average (purple gradients, one sans-serif, centred hero, three cards); vague adjectives ("clean, modern") pull straight to it. So:

1. Ask for volume (20 concepts, 10 hooks), keep 1–2, write why.
2. Give constraints, not adjectives: product, audience, ONE accent, the type family, a banned list, a reference era or studio.
3. Ask for critique ("where does this script lose a viewer in the first 3 s?"), not taste.
4. Never paste AI art direction into the build; turn it into your own styleframe first. If the styleframe looks like stock, the idea was stock.
5. Where two models agree, the idea is probably the obvious one — fine for clarity, a red flag for originality.
6. The final arbiter is a human watching the animatic at full speed with sound.
