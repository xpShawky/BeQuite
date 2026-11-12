# Craft lessons: editing and AI-film playbook

Distilled from eight studied lessons (2026-11-12). Each rule cites `slug@mm:ss` (folders under `refs/`; Higgsfield times run past 60 min, e.g. `@113:53`). This page deepens `CRAFT_RESEARCH.md`; it does not repeat it. Rules marked **(rec.)** are our design recommendation built on the sources, not a sourced rule.

## 1. How to open / hook
1. **Deliver the hook with picture and sound, not words.** A beat carried only by dialogue or type wastes cinema (`lesson-edgar-wright-visual-comedy@00:21`). The hook claim must be an event on screen with its own sound.
2. **A break is cut, not just shown.** Editors cut a glass break "jaggedly" so the cutting pattern carries the violence (`lesson-scene-transitions@02:02`). Recipe **(rec.)**: 3–5 angles of the same break, 4–8 frames each, angles ≥30° apart (`lesson-murch-blink@07:16`), one crack/impact layer per cut, the last shot held.
3. **Then smash to the opposite.** Contrast is the jolt: loud to quiet, chaos to still (`lesson-scene-transitions@14:27`).
4. **Use the frame edge.** Things entering or leaving frame are reliable beats (`lesson-edgar-wright-visual-comedy@05:15`, `@05:27`). The 2001 throw: the object exits the top, cut to an empty sky, the object enters ≈0.2 s later (`lesson-2001-bone-satellite@00:56`). The wait is the hook.
5. **Let the first action play on its own sound; bring the music after it** (`lesson-higgsfield-ai-films@65:06`).

## 2. How to cut on sound
1. **The cut and the effect land on the same frame** (`lesson-edgar-wright-visual-comedy@06:20`); move action and cuts with the music (`@06:38`). Keep SFX 1–3 frames early (`motion-grammar.md`).
2. **In a montage, pull the music down and the SFX up** so each cut is a jolt (`lesson-edgar-wright-visual-comedy@02:13`).
3. **Every graphic match gets an audio match** (sound A becomes a similar sound B); stacking them multiplies the effect (`lesson-match-cuts@04:56`; helicopter to ceiling fan `@04:09`).
4. **Pass-bys and whips need their whoosh** to keep momentum (`lesson-scene-transitions@12:52`).
5. **Not every cut needs a hit.** Trillo's 47-cuts-per-minute film lands only 23% of cuts on strong onsets (chance 16%) and puts whooshes on 15 of 57 cuts (`trillo-notes-vfx-breakdown`, summary). Mark the cuts that change ideas, not all of them.
6. **Rhythm is a drummer:** a cut early or late is wrong even if the shot is right (`lesson-murch-blink@08:51`).

## 3. J-cut or L-cut
- **J-cut (pre-lap) when the next shot is the answer:** the audience hears it first and leans in; it also bridges to memory (`lesson-scene-transitions@16:25`, waves before Normandy `@17:03`). For BeQuite: the keyboard or the "gate passed" chime before its UI appears.
- **L-cut when the feeling should linger or a join must be hidden:** narration carried over new images (`lesson-scene-transitions@17:24`); a door-close sound carried into the next generated shot so the picture cut can sit wherever the join is cleanest (`lesson-higgsfield-ai-films@68:06`, `@82:35`).
- **Either one: sound A + picture B = a third meaning** (`lesson-scene-transitions@17:46`). Pick the pairing for what it says, not only for smoothness.

## 4. How to build a match cut
1. **Choose the type:** graphic, movement or audio (`lesson-match-cuts@01:19`); combine them when you can (`@04:56`).
2. **Give it a motive.** A graphic match hits hard; use it where the idea changes (`lesson-match-cuts@02:27`).
3. **Idea match vs invisible match.** The canonical match locks the horizontal centre and span (bone and satellite both ≈0.35–0.65 of frame width) but not the height (≈0.2 frame offset), not the angle (≈38° vs ≈5°) and not brightness (mean 183 → 2) (`lesson-2001-bone-satellite@01:03`). An **idea** match needs silhouette, span and tempo; a **seamless UI morph** still needs the full four-match rule including luminance (`motion-grammar.md`).
4. **Match the speed, not peak velocity, for a calm leap:** the bone is slowed so its tumble meets the satellite's drift (`lesson-2001-bone-satellite@00:56`–`01:03`). Use peak-velocity cuts for energetic transforms.
5. **Empty backgrounds make silhouettes match.** Both 2001 shots are a lone object in an empty field.
6. **Chain one object across several cuts** as the film's through-line (`lesson-match-cuts@02:17`); bookend a sequence on the same framing in two states (taxi sign lit/dim, `lesson-edgar-wright-visual-comedy@02:01`).
7. **Soften with a match dissolve** for the calm brand beat (`lesson-scene-transitions@08:25`).
8. **Plan it before generating or shooting** (`lesson-match-cuts@05:38`): for AI plates, both sides come from keyframes with the object in the same place.

## 5. Pacing: acceleration and the stop
1. **Build short, release long.** Shots shorten to the peak, then run longer than they began; about 15 s up, 30 s down (`lesson-editor-think-feel@03:25`). In a 45 s film keep the shape **(rec.)**: shots ~1.5 s → ~0.3 s over 10–15 s, then the longest hold so far (3–5 s).
2. **The measured Hot Fuzz curve:** 2.2–2.7 s → 0.13–0.5 s → 1.0–1.5 s across 16.5 s (`lesson-edgar-wright-visual-comedy@01:42`).
3. **Flash, then stop dead:** ~40 flashes of 2–3 frames with the subject centred and the caption fixed, then a 36.5 s hold (`trillo-notes-vfx-breakdown@00:14.9`).
4. **Change tempo after the turn:** in 2001 the average shot length roughly triples after the match (5.1 → 13.5 s) (`lesson-2001-bone-satellite@01:03`).
5. **An emotion flashed for 30 frames is not believed** (`lesson-editor-think-feel@04:19`). The key claim and the logo need time.
6. **Cut when the idea completes** (the blink, `lesson-murch-blink@03:20`) and when the shot's own rhythm asks for it (`lesson-editor-think-feel@05:21`); hold one beat a little too long on purpose before the turn (`@07:28`).
7. **Eye-trace keeps fast cuts smooth:** put each incoming subject where the eye already is (`lesson-murch-blink@09:37`); a cut to a near-identical framing jars (`@06:45`).

## 6. How to use silence
- **Silence can carry the biggest cut.** The bone-to-satellite cut lands in ≈17 s of near-silence; the music arrives about 11 s later (`lesson-2001-bone-satellite@00:56.7`–`01:14`).
- **Fade/dip to black is a breath:** it pauses momentum on purpose (`lesson-scene-transitions@03:21`). Once per film.
- **Contrast makes the hit:** the smash cut works between quiet and loud (`lesson-scene-transitions@14:52`).
- **Generate AI video without music** so silence and the mix stay yours (`lesson-higgsfield-ai-films@04:08`); check anyway, the model added music against the prompt (`@177:57`).

## 7. Shoot / generate for the edit
1. **Script → shot list → assets → prompts**, in that order (`lesson-higgsfield-ai-films@04:44`); lock the script first: a rewrite cost ~100k credits (`@58:03`).
2. **Make the world first, then light the product to it** (`trillo-notes-vfx-breakdown@00:23`).
3. **Use AI as layers:** motion elements, generative fill/expand, animated luma mattes for light (`trillo-notes-vfx-breakdown@00:42`–`01:00`).
4. **Edit while generating, with the real music** (`lesson-higgsfield-ai-films@47:00`).
5. **Generate the missing coverage:** an establishing wide or an intermediate shot fixes a rough join (`lesson-higgsfield-ai-films@83:29`, `@161:57`); angles for a cut sequence ≥30° apart (`lesson-murch-blink@07:16`).
6. **One representative still per take** on a contact sheet; select from stills (`lesson-murch-blink@11:35`).

## 8. How to make AI shots not read as AI
1. **Style prefix in every prompt:** light direction, palette, lens, audio rules (`lesson-higgsfield-ai-films@03:43`).
2. **Perfect the keyframe; the video copies its flaws** (`@09:58`, `@119:46`). Fight plastic stills with haze, colder light, film grain and crushed blacks (`@11:54`, `@19:50`).
3. **A reference sheet of the space** (two views stitched) so the camera can move without inventing doors (`@28:00`, `@31:34`).
4. **One action, one camera move, written as one continuous motion**; per-second beats make the model insert cuts (`@64:42`, `@77:06`).
5. **Direct the feeling, add one physical detail** (`@89:58`, `@172:47`).
6. **Batch 4–8, then diagnose:** a shared fault means fix the prompt; right motion with wrong details means batch more (`@48:55`, `@111:10`). Scrap overgrown prompts (`@143:13`).
7. **QA for:** invented or duplicated set pieces, wrong entry side, wrong walking speed, props changing between takes, broken small faces, doubled small objects, odd hand grabs, a busy camera, inserted cuts, frame-rate drops with doubled frames, added music (`lesson-higgsfield-ai-films`, failure list).
8. **Cut around it:** trim the morph at the head, cut before the wrong reveal, L-cut across joins (`@149:37`, `@83:29`, `@68:06`).
9. **Expect the ratio:** 72 generations for one 10 s shot; 800 assets for 8 kept shots (`@113:53`, `@185:23`).

## Where this corrects or sharpens CRAFT_RESEARCH.md
- **Selection budget (§4.5 step 3, "3–6 variations, keep ~10%")** is too small for any shot with camera placement or props: the measured case is 72 generations for one 10 s shot and ≈1% of assets kept (`lesson-higgsfield-ai-films@113:53`, `@185:23`).
- **"800 generations, 8 shots" (§0.3, §3.2)** is 800 *assets* (stills and videos) for 8 kept shots, ≈1%, not comparable with Trillo's ~8% of video clips.
- **Match cuts (§1.1 and `motion-grammar.md`):** the pixel-locked anchor and luminance match are rules for invisible or sustained matches; the canonical idea match breaks height, angle and brightness on purpose (`lesson-2001-bone-satellite@01:03`).
- **Silence (§1.4, "one drop-out, 0.3–1.0 s"):** a long silent bed can carry the main cut; the 2001 cut has no hit at all.
- **AI tells (§3.1 #16, "frames that freeze", UNVERIFIED):** now observed in a pro session as frame-rate drops to ≈12–18 fps with doubled frames, plus a frozen take (`lesson-higgsfield-ai-films@123:47`, `@114:51`). New tells: model-added music, props moved instead of camera.
- **Rule of Six weights (§1.2):** the StudioBinder video gives only the order; an editor in the EFAP film calls editing "70% about rhythm" (`lesson-editor-think-feel@05:45`), which sits badly with rhythm's 10% weight. Treat the percentages as Murch's rhetoric, not a recipe.
