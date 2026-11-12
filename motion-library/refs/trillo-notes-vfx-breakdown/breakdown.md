# Notes To My Future Self: VFX Breakdown (Paul Trillo): lesson

**File:** `inbox/New/Notes To My Future Self_ VFX Breakdown _ Videos & Movies on Vimeo.mp4` · **Source:** Paul Trillo (Vimeo), https://vimeo.com/939660277 · **Length / format:** 72.2 s, 1920x1080, 23.976 fps · **Studied from:** transcript, `frames/summary.md` (measured), `shots.jpg`, `matches.jpg`, and 17 frames through the long breakdown shot (`frames/check/longshot.jpg`).
**Category:** hybrid AI + live-action VFX lesson

## What it teaches
Use generative images as **pre-production assets that become post-production assets**: generate the backgrounds first, light the live-action shoot to match them, then composite, extend and animate with generative tools. AI is a layer in a VFX pipeline, not the finished shot. Made in about 10 days (shoot, edit, composite).

## Lessons (with timestamps)
| # | Time | Lesson | Shown as |
|---|---|---|---|
| 1 | 00:07–00:17 | Turn the script into prompts: the lines the actors will read, combined with other prompts, produce a large set of images. | Script pages with highlighted lines (00:06–00:12) |
| 2 | 00:17–00:23 | That creates a paradox of choice, but also a library of pre-production assets you can use in post. | Flash montage "THE PARADOX OF CHOICE" (00:15–00:19) |
| 3 | 00:23–00:42 | **Light the set to the final background.** Bad composites come from green-screen lighting done without knowing the background. With the background chosen first, the on-set key and practicals match it. | Panels "Motivated light from final background" (≈00:26–00:29), "Source footage lit to match" (≈00:38) |
| 4 | 00:42–00:48 | Photoshop Generative Fill and Generative Expand extend and fix plates (e.g. to a wide scope frame). | "Photoshop Gen-Fill" (≈00:44), "Photoshop Gen-Expand" (≈01:06) |
| 5 | 00:48–00:52 | Runway Gen-2 generates **motion elements inside** the composite (screens, sky, foliage), not whole shots. | "Gen-2 motion elements" (≈00:41, 00:47, 01:09) |
| 6 | 00:52–01:00 | Gen-2 as an **animated luma matte**, so light subtly moves across the comp and reacts to the environment. | "Gen-2 light movement luma matte" (≈00:56) |
| 7 | ≈01:01 | Remove the subject from the generated image and upscale to get a clean plate for the real actor. | "Remove subject + upscale" |
| 8 | 01:00–01:12 | The speed came from the fluid link between pre- and post-production. | — |

**Editing lessons from the measured film** (`summary.md`): 58 shots, 47 cuts/min, median shot 0.12 s. From 00:14.9 to 00:22.9 about 40 flashes of 2–3 frames (0.083–0.125 s) run through AI stills; in almost every flash the figure stands near frame centre and the lower-third caption stays fixed, so the eye has one anchor while the worlds change. Then the film stops dead: one 36.5 s explanatory shot (00:25.2–01:01.7) made of labelled before/after panels. Sound: whoosh-ins on 15 of 57 cuts, booms on 10; cuts on strong onsets 23% vs 16% chance; −18.7 LUFS. The opening cut (00:02.7) reveals the outpainted frame (transparency checkerboard at the edges), so the technique itself becomes the transition.

## How it applies to a 30–60 s launch film
- **Generate the world, then build the product into it:** make the AI plate first (Nano Banana / Flow), then light the 3D product or UI layer to that plate (key direction, colour, contrast). This is the cheapest way to stop a comp from reading as pasted.
- **AI as elements, not shots:** use Flow clips as moving skies, screens, particles or light passes under designed foregrounds (type, UI, 3D), and as luma mattes for light sweeps across the BeQuite mark.
- **Flash montage as an idea:** 1–2 s of 2–3-frame flashes of many generated worlds, with the type and the subject locked in place, says "endless options, one harness" in a second. Then a hard stop.
- **Show the seams on purpose** once (the outpaint reveal) if the film's theme is the tool itself.

## What to try in the lab
1. **Lit-to-plate comp:** one Flow/Nano Banana background, the BeQuite 3D mark lit twice (default studio light vs light matched to the plate). Show both blind.
2. **Luma-matte light pass:** a Flow clip of moving light used as an AE luma matte over a type layer; judge whether the light "belongs".
3. **Flash montage:** 24 generated stills at 3 frames each with a fixed subject position and a fixed caption; measure with `film_study.py` and check eye comfort on a phone.

## Open questions / UNVERIFIED
- Panel times are from 3-s frame sampling (±1.5 s).
- Which image model made the "Stable Diffusion" stills (version) is not stated.
