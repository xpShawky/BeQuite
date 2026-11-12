# How to Make AI Films That Don't Look AI (Higgsfield, feature-film series ep. 2): lesson

**File:** `inbox/New/How-to-Make-SnapYT.App.mp4` · **Source:** Higgsfield AI, https://www.youtube.com/watch?v=-scKERL7PK0 (matched by length and the closing numbers) · **Length:** ~3:05:45 · **Studied from:** full transcript, read in four chunks. Timestamps are `mmm:ss` from the transcript (e.g. 113:53 = 1 h 53 min 53 s).
**Category:** AI-film production lesson (a real-time, uncut working session)
**What it is:** day 4 of a 14-day sprint to make an 80-minute, fully generated feature for Cannes, 15 people, 10 million credits. One generalist (Adil) makes scenes 21 and 23 (a grieving man returns to a shared apartment) live, failures included, and the director must approve the result.

**Tool chain shown:** Claude with a team-built "shot list builder" skill (script → shot list → asset list → per-shot prompts in an HTML shot list) · Higgsfield canvas and "collab" projects (shared prompts, inputs and tool used per asset) · Nano Banana Pro and GPT Image 2 for stills · Seedance 2.0 ("CDS 2.0") for video with audio · a normal NLE timeline with temp music · Photoshop for compositing props.

## What it teaches
AI film is a production pipeline, not a prompt. The look is decided in the stills (location sheet, props, characters) under one shared style prefix; video generation is batch-and-diagnose against a shot list; the edit happens during generation, with music, and the cut is where most "AI-ness" is removed. Expect dozens of generations per usable shot.

## Lessons (with timestamps)
| # | Time | Lesson |
|---|---|---|
| 1 | 03:43–04:28 | **Style prefix.** One shared block (style, lighting, colour, composition, audio) goes into every prompt so 15 people produce one film. Lighting rule: natural light only, key from sky and windows. Audio rule: environmental SFX only, no music, no subtitles (the model returns one mixed track and tends to add music in emotional moments; it still did at 177:57). |
| 2 | 04:44–05:05, 46:15–46:41 | **Three phases:** (1) script → shot list in ~15 s shots with model-specific prompts; (2) the assets each shot needs (characters, locations, props); (3) map prompts and asset tags onto shots. |
| 3 | 09:58–10:02, 119:46–119:56 | **The keyframe carries the film.** Most of the lighting and style in the video comes from the location reference; the video model copies any sloppiness in the stills. Images are cheap, so perfect them before spending video credits. |
| 4 | 11:54–12:08, 19:50–20:20 | **Anti-plastic words for stills.** Nano Banana Pro textures read "plasticky"; lighting/atmosphere words fix it: atmospheric haze, colder light, film grain, crushed blacks for shadow depth, darker exterior. |
| 5 | 12:18–12:28, 20:58–21:04 | **Batches of four per prompt**, one row per prompt, so you compare like with like; with a detailed prompt the results are consistent, so a shared fault means the prompt is at fault. |
| 6 | 12:41–12:57, 21:33–21:41 | Add contrast and lore: coloured set pieces (red wall, blue couch, yellow fridge) and story props (a skateboard for skater characters). |
| 7 | 23:16–23:21, 25:03–25:47 | **Don't chain edits on one image**: each edit loses detail. After a few edits, regenerate from scratch with one complete prompt that includes every change. |
| 8 | 28:00–31:50, 29:02 | **Location reference sheet.** The room took 44 iterations. Then a reverse angle from the hallway (about 20 more) and both views stitched into one 16:9 sheet (front wide on top, reverse below), so the video model understands the space. |
| 9 | 35:41–35:53, 45:01–45:12 | Don't let the prompt re-describe what a reference image shows; describing faces made the model invent new people. Attach the reference and describe only what is new (clothing, action). |
| 10 | 42:05–43:56 | **Composite props from single images.** A 12-photo wall generated in one image broke the faces; generating each photo separately and stitching in Photoshop kept them consistent. |
| 11 | 47:00–47:21, 65:06–65:20 | **Edit as you go, with music in the timeline**, to see what is missing and how shots join. At the opening he lets the door open on its own sound and brings the music in after it. |
| 12 | 48:26–48:33 | 21:9 for the cinema screen. |
| 13 | 48:42–48:55, 62:05–62:20 | **Reference order matters:** image 1 is the character because the prompt describes him first; image 2 the location. Keep the same order in every prompt. |
| 14 | 48:55–49:11, 52:47–52:51 | **Batch, then diagnose.** Batches of eight; if several fail the same way (all eight did), stop and fix the prompt; there is no point batching further. |
| 15 | 49:11–49:34 | Prompts were written in Chinese to fit Seedance's 3,000-character cap (1–2 characters per word vs 5–10 in English). Model-specific workaround. |
| 16 | 50:29–50:50 | Write the failure modes into the prompt (e.g. the small photo must not drift). |
| 17 | 64:42–64:56 | **One camera motion.** A handheld rise plus push-in on an emotional beat "overloads the viewer"; keep one move (a push-in). |
| 18 | 68:06–68:31, 82:35–82:48 | **L-cut to join generated shots:** the door-closing sound carries into the next shot, and the picture cut moves to wherever the two shots join best. |
| 19 | 74:25–76:47 | A spatial-layout block in the prompt (where the camera stands, where the hallway is) fixed the entrance direction. |
| 20 | 77:06–80:06 | **Don't split one shot into per-second beats.** Describing what happens in seconds 0–3, 3–6, 6–9 made the model insert cuts in every take. Rewrite as one continuous motion. |
| 21 | 83:29–84:29, 161:57–162:20 | **Cut around the error.** Cut before the wrong part of the room is revealed and introduce the room from a different, generated wide shot; add an intermediate shot when a join feels rough. |
| 22 | 89:58–90:50, 99:07–99:18, 172:47–172:54 | **Direct emotions, not mechanics.** "Very upset and heartbroken" turned a brisk walk into a slow, grief-dragged walk; add one small physical detail (a trembling lower lip). |
| 23 | 96:12–96:17, 113:53 | "One little issue, fifteen batches": a simple pan-and-push shot took **72 generations for 10 s of footage**. |
| 24 | 96:29–96:42, 104:47–105:02, 109:02–109:49 | The model moved props instead of the camera (the fridge walked towards the lens). Anchoring to a prop failed; anchoring to a region of the reference sheet ("the hallway in the top-right corner") worked. |
| 25 | 100:04–100:19, 143:13–143:31 | Prompts grow with every fix until they clash and overwhelm the model; scrap and rebuild a short prompt with the same asset handles. |
| 26 | 111:10–111:24 | When to keep batching vs change the prompt: if the motion and action are right and only details fail, batch more; if the same error repeats, change the prompt. |
| 27 | 122:04–123:01 | A content-filter false positive came from the prompt wording; rewording fixed it (failed generations were not charged). |
| 28 | 123:47–124:00, 125:33–128:22, 145:48–146:44 | **Frame-rate drops:** some takes come out at roughly 12–18 fps with doubled frames. Removing duplicate frames one by one works only for an otherwise great shot, costs seconds and the audio, and still jolts. Usually reject. |
| 29 | 149:37–149:42, 165:46, 168:06–168:40 | Trim heads and tails: start after a morph at the head, cut before the actor turns, leave a beat to cut to the flashback. |
| 30 | 174:58–175:05, 179:48–179:59 | A slow pull-back after a breakdown "leaves the character alone" to feel it; keep camera ideas that the model or Claude adds when they serve the emotion. |
| 31 | 58:03–58:27 | A script change threw away ~100,000 credits of a nearly finished 2.5-minute scene: lock the script before generating. |
| 32 | 185:02–185:27 | **The numbers:** in four days the team used 4,441,352 credits and generated 48,336 images and videos (about $260,000). The presenter generated nearly 800 assets; 8 made the final cut. |

## What made shots read as "slop" in this session (observed failures)
Invented doors and duplicated set pieces (54:51–55:21, 115:13) · entering from the wrong side (55:00, 64:29) · walking too fast for the mood (78:33, 88:17) · walking through furniture (88:12) · props changing colour or position between takes (95:05) · the wrong photo picked, faces breaking in small photos (129:05–129:26) · wardrobe drift (a wrong glove, 123:21) · magnets and pins doubling (145:48) · awkward hand grabs (142:03) · a "soulless", frozen take (114:51–115:05) · camera doing too much (64:42, 94:59) · unwanted sub-shot cuts (77:06) · low frame rate (123:47) · music added against the prompt (177:57) · plasticky textures on stills (10:30).

## How it applies to a 30–60 s launch film
BeQuite's film uses AI plates only for a few shots (worlds, textures, an establishing image), with kinetic type, UI and 3D carrying the rest. Take the pipeline, not the scale:
- A **style prefix** for every Flow/Omni prompt (light direction, palette, lens, grain, "no music, no text").
- **Lock stills first** (Nano Banana) with anti-plastic words and the composition the edit needs; generate video only from approved keyframes.
- **One action, one camera move, one continuous shot** per prompt; emotions or qualities, not frame-by-frame mechanics.
- **Batch 4–8, diagnose, then batch more**; budget tens of generations for any shot with camera placement or a specific prop.
- **Edit while generating**, against the actual music; L-cut sound across AI joins; cut before any wrong reveal.
- Keep human-controlled layers (UI, type, the logo) out of the generator entirely, so the hero frames cannot drift.

## What to try in the lab
1. **Style-prefix A/B:** the same Flow shot with and without a 5-line prefix; compare consistency across 4 takes.
2. **Continuous vs beat-split prompt:** one prompt written as seconds 0–3/3–6, one as a single motion; count unwanted cuts in 4 takes each (Omni also defaults to multi-shot: CRAFT_RESEARCH §4.3).
3. **Selection log:** for one 3 s plate, log every generation (prompt change, failure type, keep/reject) until one passes the AI-tell QA; record the ratio.
4. **Duplicate-frame check:** a script that flags repeated frames (`ffmpeg -vf mpdecimate` reports dropped duplicates) on every AI clip before it enters the edit.

## Open questions / UNVERIFIED
- The YouTube title on file ("How to Make AI Films That Don't Look AI") was matched by length and the 800/8 numbers; the downloaded file name does not carry it.
- Cost figures conflict inside the series: an earlier episode's ~$70,000 (63:06–63:15) vs ~$260,000 for these four days (185:19); the first likely refers to episode 1 only.
- Prompt-language and character-cap advice (lesson 15) is specific to Seedance 2.0 at that time.
