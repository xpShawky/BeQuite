# Technique catalogue

Every technique seen in a studied film, merged across films, with where to see it (`slug@mm:ss`, breakdowns in `refs/<slug>/`), how we make it, and whether we have made it ourselves. Plans (`/bq-motion` M1-M2) pick from here; untested rows carry a lab cost. Method: `.claude/skills/bequite-motion-director/references/learning-orchestra.md`.

**Make with:** `gen` = generated plate (Google Flow / image model, directed with the grammar below) · `post` = After Effects / Premiere / Resolve · `3D` = Blender · `code` = HTML/canvas/Remotion · `shoot` = filmed · `sound` = DAW / ffmpeg.
**Status:** `untested` · `partly` / `proven` / `failed` (see `LAB.md`).

Built 2026-11-12 from 69 studied films (58 new + 11 earlier).

## 1. Cuts that keep something fixed (Apple's core grammar)

| Technique | What it is | Seen in | Make with | How | Status |
|---|---|---|---|---|---|
| position-locked match cut | hero object stays at the same frame spot; colour, world or version changes on the cut | apple-macbook-neo@00:08.98 · apple-iphone-17-pro@00:10.9 · apple-event-sep26@48:21.97 · ig-galshirart-framer-3d-logo@00:08 | 3D / post / gen (frames-to-video from one locked still) | lock camera + object; swap material/plate; cut within ±2 frames of an onset; hold 0.5-0.8 s per step | partly (lab 001) |
| lineage flicker | versions or generations cut every 2-3 frames in one spot, accelerating into the newest, last one held | apple-event-sep26@07:10.9 · apple-iphone-18-pro-intro@00:32.6 · apple-macbook-pro-proled-touch@00:51.6 | post / 3D | holds 18→3 frames, push carried across, riser into a hit on the land; works as a visual drum roll, not on the grid | partly (lab 001) |
| position-locked ladder | 3-7 steps on one scale (zoom 13→200 mm, render passes), 0.1-0.3 s each, last held 1.5 s | apple-iphone-17-pro@00:32.2 · apple-macbook-pro-m5@01:16.2 | 3D / post | one framing, step the variable, hold the last | untested |
| centred graphic-match chain | each next object replaces the last at frame centre (chip → cloud → chamber → heat map) | apple-iphone-17-pro@00:13.4 | 3D / post / gen | size-match and centre every hero; low boom on each cut | untested |
| subject-locked swap | the character stays in place while costume or world changes | mvsm-openai-images-2@00:49.7 · openai-sound-on-sora-2@00:14 (presenter teleport) | gen (character reference, fixed framing and eyeline) / post | align each plate to a guide layer | untested |
| one-shape montage | every plate shares one shape at one spot; cuts accelerate 0.7 → 0.13 s, dead stop on the name | claude-opus-5-5-launch · claude-fable-5-2-launch · google-gemini-omni@00:00 | gen (curate plates by shape) / post | align the shape centre per plate; accelerate cut lengths | untested |
| fixed text, changing world | one line holds still while 3-6 plates cut under it | buck-oura@00:07 · anthropic-keep-thinking@01:09 · apple-iphone-18-pro-ad@00:17.59 · google-gemini-omni@00:00 | post (+ gen plates) | text layer above the edit; shared pose/shape under it | untested |
| fixed UI anchor across cuts | one UI chip, pill or player bar stays put while the content behind it changes | mvsm-canva-affinity@00:11 · apple-iphone-air@00:22.5 · apple-event-sep26-recap@00:02 · anthropic-keep-thinking@01:09 (status chip with a swapping verb) | post | chip as the top precomp; swap plates every 0.7-0.8 s | untested |
| label-synced swap | locked frame; the label word and the image change on the same frame | google-gemini-omni@00:38 | post (+ gen variants) | N image variants; swap word + image + hit on one frame | untested |
| position-locked insert ↔ reaction | the same product insert cut back to with one detail changed, intercut with faces | nothing-phone-3@00:03.6 | shoot / gen | lock-off insert; vary only the screen state | untested |
| product logo → brand logo | the product's logo cuts to the end-card logo at the identical position | apple-macbook-pro-proled-touch@01:50.26 · apple-event-sep26@02:36 (dark → light hand-over) | 3D / post | frame the last shot so its logo sits where the end card's will | untested |
| same menu across projects | the same UI menu shown on several projects in 1 s cuts | anthropic-claude-design-intro@01:06.85 · figma-config-2025 (one demo universe) | code / post | position-lock the menu across recordings | untested |
| object-to-blueprint match | real object cuts to its line drawing on the same outline | apple-iphone-18-pro-intro@00:16.02 | post | trace the outline, align, cut on a hit | untested |
| bookend match | open and close on one framing in two states | lesson-edgar-wright-visual-comedy@02:01 · mvsm-samsung-micro-miracles@00:55 · apple-macbook-pro-proled-touch@01:42 | any | duplicate the opening framing; change only the state | untested |

## 2. Cuts and rhythm

| Technique | What it is | Seen in | Make with | How | Status |
|---|---|---|---|---|---|
| burst only on impact | 6-7 cuts of 0.17 s at the one physical moment, then hold | apple-event-sep26@00:29.0 · openai-sound-on-sora-2@00:28 (staccato sound montage) | post (+ gen/3D angles) | 3-5 angles ≥30° apart, 4-8 frames each, a crack per cut, hold the last | untested |
| jagged break cut | one break as several very short angles | lesson-scene-transitions@02:02 | 3D / gen | as above | untested |
| build / release curve | shots shorten to the peak, then the longest hold so far | lesson-editor-think-feel@03:25 · ordinaryfolk-distance@01:44 · lesson-2001-bone-satellite@01:03 (tempo pivot) | post | ~1.5 → 0.3 s over 10-15 s, then 3-5 s hold; every shot after the turn longer than any before | untested |
| smash cut to stillness | loud chaos → still frame with room tone | lesson-scene-transitions@14:27 · anthropic-keep-thinking@00:20 (held breath frame) | post | cut on the peak; next shot still, no fade | untested |
| cut on action / movement match | action in A continues in B | lesson-match-cuts@02:44 · apple-iphone17pro-detectives@00:02.8 | post | cut mid-action; continue direction and speed | untested |
| motion carried across the cut | camera direction continues through cuts so a tour reads as one move | apple-ios26-liquid-glass@02:05.9 · apple-macbook-pro-14-m6@00:07.73 · apple-event-sep26@00:29 | post / 3D / gen (prompt the same move direction per clip) | same direction and speed both sides; cut mid-move | untested |
| cut on the empty frame | the object leaves, cut on clean background, it re-enters | apple-macbook-neo@00:08.23 · lesson-2001-bone-satellite@00:56 (exit → empty → enter) | any | 0.3-0.4 s after exit, 0.2 s empty, enter from the opposite edge | untested |
| cut per spoken verb | in a spoken list, one cut on each verb | apple-macbook-pro-proled-touch@00:44.2 | post + `transcribe.py` word times | cut at each verb onset; boom on most | untested |
| cut on the blink / eye-trace | cut when the shot's idea completes; next subject starts where the eye already is | lesson-murch-blink@03:20, @09:37 | post | map focal points; cut on the frame after an animation completes | untested |
| 30-degree rule | avoid near-identical framings across a cut | lesson-murch-blink@06:45 | 3D / gen | angle change ≥30° or a clear scale jump | untested |
| hold a little too long | over-held beat before the turn | lesson-editor-think-feel@07:28 | post | add 0.5-1.5 s to one hold | untested |
| long proof hold / long real-UI take | 8-20 s uncut so viewers can inspect the work | openai-this-is-sora-2@00:42 · anthropic-claude-design-intro@00:21 · linear-agent | code / gen | the best take, no overlay; slow virtual camera | untested |
| crash zoom sting | wide to extreme close-up in 0.4 s with a sting | apple-iphone17pro-detectives@00:32.3 | post / shoot | 0.4 s scale with motion blur; sting on arrival | untested |
| accelerating word cadence | word holds 0.8 → 0.2 s, ending in a colour flicker | ig-extra-blue-white-word-type@00:10 | post | keep flicker under 3 Hz (photosensitivity) | untested |
| colour-inversion cut per word | each word flips background and text colours | ig-extra-blue-white-word-type@00:00 · openai-intelligence-age@00:09 (B/W invert as era change) | post | two colours, hard cuts | untested |

## 3. Transitions

| Technique | What it is | Seen in | Make with | How | Status |
|---|---|---|---|---|---|
| graphic / idea match | a shape match that carries an idea; brightness may invert | lesson-2001-bone-satellite@01:03 · lesson-match-cuts@01:55 | gen / 3D / post | lock horizontal centre and span + silhouette, not pixels; slow the outgoing object to the incoming speed; land it in silence | untested |
| whip / motion-blur carry | blur at the end of A continues into B | anthropic-keep-thinking@00:37 · lesson-scene-transitions@13:21 · back-market | post | cut at blur peak; 2-4 frames directional blur each side; one direction per film; whoosh before the peak | untested |
| hidden cut in an FPV whip | a drone flight dives from one world into another through blur | apple-macbook-pro-proled-touch@01:41.8 | 3D / gen / shoot | stitch two paths in the blur frames | untested |
| dive into object | camera enters a headset/lens/screen to black, emerges in a new world | higgsfield-the-kiss@00:16 · lesson-scene-transitions (pass-by mask @12:26) | gen / 3D / post | push until black; cut on black | untested |
| jump scale through an instrument | eyepiece view → white flash → deeper view of the same subject | mvsm-samsung-micro-miracles@00:17.3 · apple-iphone-air@00:14.5 (white flash as the cut) | post | circular vignette matte, 2-4 frame white flash, aligned close plate | untested |
| iris / inset-window reveal | a shape opens over shot A playing shot B, then B goes full frame | ig-kryvetskyy-cgi-lens@00:02.04 · lesson-scene-transitions@09:48 · apple-macbook-pro-14-m6@00:18.25 (geometric window masks) | post | track-matte shape, 14-18 frames ease-out, sub-hit | untested |
| card-to-fullscreen / zoom-through grid | a result in a rounded card expands to full frame; camera pushes into one thumbnail | google-veo-3-1@00:00, @00:18 · apple-event-sep26-recap@01:02.70 (thumbnail → screen) | post / code | mask path to frame size, 12-18 frames ease-out | untested |
| gesture-colour ribbon / finger-to-lens wipe | a stroke in the gesture colour sweeps the frame; a fingertip blooms into the next title | mvsm-google-circle-to-search@00:11.9, @00:28 | post / shoot | trim-path stroke as matte; glow from a tracked fingertip | untested |
| title liquefies into refraction | title smears into rainbow liquid and tears away | apple-airpods-pro-3@00:02.2 | post | displacement + RGB split + turbulence, 0.25 s | untested |
| blur-to-focus handoff | elements enter and exit with blur, opacity and a small Y drift | ig-qasim-spotify-ui-ad@00:00 | post / code | blur 40 → 0, Y +20 → 0, 8-12 frames | untested |
| shape → logo match | a centred dot/ring resolves into the logo | ig-sultanmotions-explainer-anatomy@00:15.5 · mano-grocery (light comet) | post | position-lock centres; scale-morph; 6-8 frame crossfade | untested |
| match dissolve / superimposition | a match softened by a dissolve; a 50% hold comparing two states | lesson-scene-transitions@08:25, @06:24 | post | 8-16 frames; hold 0.5-1 s | untested |
| dip to black (breath) | deliberate chapter pause | lesson-scene-transitions@03:21 · apple-event-sep26 (181 cuts through black) | post | 6-12 frames, room tone, once per film | untested |
| cut-less spec ladder | features flow by dissolves, defocus and light; one hard hit saved for the brand line | apple-iphone-18-pro-ad@00:19.86 | post / 3D | cross-dissolve with defocus | untested |

## 4. Camera

| Technique | What it is | Seen in | Make with | How | Status |
|---|---|---|---|---|---|
| continuous one-camera space | the whole film is one virtual move through a space | google-gemini-3@00:00 · nexo-opus-5-5 (one-take toy 3D) | 3D / post | sections as depth zones | untested |
| FPV / drone one-take | 20 s+ push through a space full of users | apple-macbook-pro-proled-touch@00:00 · apple-event-sep26@02:09 (aerial → building → interior) | gen (one continuous motion prompt) / 3D / shoot | calm VO over it | untested |
| tilted UI plane with shallow focus | product UI on a plane in 3D, slow drift, only the active line sharp | linear-agent@00:00 · google-gemini-3@00:46 (floating UI cards) | post / 3D | AE 3D layer + camera DOF, constant slow drift | untested |
| push-in on the button about to be pressed | virtual camera pushes to a control just before the click | anthropic-claude-design-intro@00:13.9 | post / code | 0.5 s ease on a 4K recording | untested |
| pull-out screen reveal | artwork turns out to be on the product's screen | mvsm-canva-affinity@00:22.5 | 3D | screen texture = the animation; dolly back | untested |
| there and back again | camera leaves and returns to find something changed | lesson-edgar-wright-visual-comedy@05:39 | 3D / post | swap the state hidden in the blur | untested |
| pull-back exit | slow pull-back leaves the subject alone after the climax | lesson-higgsfield-ai-films@179:48 | gen / 3D | 3-5 s dolly out | untested |
| phone-POV realism | phone in frame, amateur voices, dead air | openai-this-is-sora-2@00:22 · apple-glad-i-met-you-making-of@00:12 (dual capture) | shoot / gen | keep ambience gaps, no music | untested |

## 5. Type

| Technique | What it is | Seen in | Make with | How | Status |
|---|---|---|---|---|---|
| narrated shot list | the voice says what happens next and the picture obeys, line by line | apple-event-sep26@00:12-02:36 | any (+ VO) | 97 wpm, real pauses; each line describes the next shot | untested |
| word-by-word spec build / light sweep | words sit dim in final position and brighten one by one; line never re-centres | apple-iphone-17-pro@00:29.9 · apple-iphone-18-pro-ad@00:12.5 | post / code | 40 → 100% per word over 0.1-0.4 s | untested |
| spoken-word captions | the keyword of each VO line blurs in as it is spoken | google-gemini-3@00:03 | post + word times | blur 20 → 0 over 6 frames at word onset | untested |
| keystroke type | spec letters pop one per key click | apple-macbook-pro-m5@00:24.2 · openai-intelligence-age@00:57 (typed wordmark) | post | one letter per click marker, 2-frame pop | untested |
| typed-and-deleted cursor / live typing prompt | a cursor types then deletes (writer's block); a prompt typed at ~12 chars/s | apple-macbook-pro-m5@00:10.5 · linear-agent@00:07 · ig-sultanmotions-explainer-anatomy@00:41 | post / code | real key sounds over near-silence | untested |
| one word per edit | giant slogan words, one per cut, ~0.6 s | apple-iphone-17-pro@00:03.0 | post | wide display face in the hero colour | untested |
| found-type sentence / word found in the world | each word of the line printed on a real object inside the shot | mvsm-openai-images-2@00:01 · anthropic-keep-thinking@00:00 | gen / shoot / 3D | write word-per-shot script first; ~0.7 s per word | untested |
| type split around the device / inline product in a sentence / screen as the missing word | the sentence wraps around the product, or the product sits in the gap of the sentence | apple-iphone-17-pro@00:38.0 · apple-iphone-17-colors@00:23.63 · mvsm-google-circle-to-search@00:06 · google-gemini-omni@00:02 (inline media chips) | post | split the line at one baseline; push words apart, scale the object in | untested |
| in-place word swap | one word of a fixed sentence changes in place | apple-iphone-17-colors@00:16.3 · mvsm-canva-affinity@00:00.8 · ig-qasim-spotify-ui-ad@00:02.9 · kreatively-editor · kinetic-type skill | post / code | two layers on one anchor; only the word moves | untested |
| type as editable object | key word shown with a selection box and handles, then transformed | mvsm-canva-affinity@00:19 · tobi-fable-5-2-one-prompt · ig-nicegreg-thorough-type@00:00.3 (live corner marks) | post | bounding box by `sourceRectAtTime()` | untested |
| type built across cuts | a line grows one word per cut while plates change | google-gemini-omni@00:14 | post | add a word on each cut | untested |
| two-part claim card | black card writes a claim in two steps before any image | openai-sound-on-sora-2@00:00 | post | second line ~2 s later; 5 s hold | untested |
| chapter card dressed as its own feature | each chapter title animates in that feature's own visual language | figma-config-2025@00:03 · ig-sultanmotions-explainer-anatomy@00:03 (section tab bar) · higgsfield-fable-5-2 (prompt as chapter) | post | per-title treatment | untested |
| size = emphasis / italic serif accent | small lead words over one huge key word; one italic serif among sans | ig-extra-blue-white-word-type@00:02 · ig-thearseniodev-opus-website@00:00 · tobi-fable-5-2-one-prompt | post / code | key word 2-3x; one font swap | untested |
| syllable staircase / substitution frames | a word splits into stepped syllables then stacks; an alternate logo for 5 frames before the settle | ig-nicegreg-thorough-type@00:01.87, @03:70 | post | 1-2 frame steps | untested |
| type riding mask edges / 3D tilted numbers | huge tilted spec numbers set along a window's edge | apple-macbook-pro-14-m6@00:26 | post | 3D text rotated to the edge angle | untested |
| 3D chrome type in smoke | extruded chrome brand line in volumetric smoke | apple-iphone-18-pro-ad@00:43.5 | 3D | Blender extrude + chrome + smoke sim | untested |
| word carousel | a row of verbs scrolls; active word sharp | google-gemini-3@01:00 | post / code | blur by distance from centre | untested |
| wordmark + full stop + promise | "Name. Promise." fading grey → white | linear-agent@00:47.5 | post | two layers, fill grey → white over ~1 s | untested |
| end card performs the feature | the logo animates with the product's own gesture (circled, typed, ticked) | mvsm-google-circle-to-search@00:54.3 · figma-config-2025@00:36 | post | trim-path stroke around the wordmark, hit on close | untested |
| colour-cycling logo | end logo flips through product colours ~0.2 s each | apple-macbook-neo@00:28.95 | post | hold keyframes every 5 frames | untested |
| oversized marquee ending | huge wordmark scrolls beyond the frame | ig-mitkow-3d-robotics-site@00:18 | post / code | linear 3-5 s | untested |
| form decodes into title | the film's visual code resolves into letters | ordinaryfolk-distance@02:56 | post | shapes replace into letterforms | untested |

## 6. UI motion

| Technique | What it is | Seen in | Make with | How | Status |
|---|---|---|---|---|---|
| single-container flow morph | one rounded rectangle morphs through every state of a flow | ig-adittyavisuals-blinkit-order-flow@00:01.5 · movez-motion-studio | post / code | size/roundness/fill keys, content crossfades, overshoot springs | untested |
| shared-element morph (button → result) | the pressed button grows into the output, then zoom through | ig-extra-chatgpt-image-concept@00:04.5 | post / code | one rect, swap content, scale past the frame | untested |
| UI morph from the touch point | menus and alerts expand from the tapped button | apple-ios26-liquid-glass@03:11 | code / post | 0.3-0.5 s spring anchored at the tap | untested |
| agent checklist ticking / AI wait state as a beat | the task list strikes items as the agent works; "Thinking…" as a designed title moment | anthropic-claude-design-intro@00:17.9 · figma-config-2025@00:31 | code / post | real recording or trim-path strikes; shimmer 1-1.5 s | untested |
| prompt → artifact, twice | first prompt teaches the grammar, second produces a bigger artifact | linear-agent@00:03-00:35 | code | second output 2-3x larger | untested |
| ingredient cards merge | input cards fly together into one card that becomes the result | google-veo-3-1@00:12 | post | converge on a null, merge, expand | untested |
| orbiting swarm → one hero / size-class resize | many tiles orbit then collapse; one widget grows small → large | ig-buksedits-apple-widgets@00:00.9, @00:05 | post | 3D layers on a rotating null | untested |
| logo becomes UI | the logo's ring becomes the first UI element | ig-qasim-spotify-ui-ad@00:01.5 · openai-intelligence-age@00:46 (guide element ends as product) | post | match scale and position, crossfade in a shared mask | untested |
| design-tool build-up | a mark drawn from vector shapes with a fake cursor and guides | ig-galshirart-framer-3d-logo@00:00 · tobi-fable-5-2-one-prompt | post | shape layers + cursor layer | untested |
| status card with progress bar | a status card with a filling bar as the tension beat | ig-adittyavisuals-blinkit-order-flow@00:06 | post / code | ~1.5 s linear bar | untested |
| clutter build of legacy dialogs | fake error windows pile up as the "before" problem | mvsm-canva-affinity@00:04 | post / code | retro dialog component, staggered pop-ins | untested |
| in-scene labels / HUD callouts / instrument HUD | small spec labels in the scene; technical lines on the hero; fixed scale-bar HUD as evidence | apple-macbook-pro-proled-touch@00:59 · ig-pavmotion-mouse-light-reveal@00:00 · mvsm-samsung-micro-miracles@00:19 | post | 3D camera track + null-parented text | untested |
| one demo universe | every demo uses one shared fictional project and dataset | figma-config-2025 | code | write the fake project before capture | untested |
| 9:16 sandwich | claim on top, 16:9 recording middle, blurred fill behind | ig-thearseniodev-opus-website@00:00 | post | for social recuts only | untested |

## 7. 3D, colour and light

| Technique | What it is | Seen in | Make with | How | Status |
|---|---|---|---|---|---|
| product rises from darkness / light-beam reveal / silhouette → form | the product is revealed by light moving, not by the camera | apple-iphone-17-pro@00:47.5 · apple-iphone-18-pro-ad@00:00 · ig-pavmotion-mouse-light-reveal@00:09.5 · apple-airpods-pro-3@00:06.8 | 3D | black void, animate key light intensity/height over ~1.5 s; rim light creeps | untested |
| light-blade extrusion | a thin light bar crosses a flat mark and leaves it extruded | ig-galshirart-framer-3d-logo@00:02 | 3D | emissive plane sweep + depth keys | untested |
| exploded-view assembly + hero turn | parts float in and assemble, then a 180° turn | apple-iphone-18-pro-intro@02:39 · ig-kryvetskyy-cgi-lens@00:02.94 | 3D | staggered Z keys ease-out; rim light | untested |
| X-ray ghost shell | translucent shell shows the mechanism | ig-pavmotion-mouse-light-reveal@00:12.5 · apple-event-sep26@68:27 (X-ray → screen) | 3D | transmission pass + opaque inner parts | untested |
| one material, many worlds / material match cut | every metaphor in one shared material; same material, new object across a cut | mvsm-samsung-micro-miracles@00:19 · apple-ios26-liquid-glass@00:59.9 · apple-airpods-pro-3@00:05 (glass rings) | 3D | one shader for everything | untested |
| edge-on hold | the product shown only side-on to sell thinness | apple-iphone-air@00:04.0 | 3D / shoot | shadowless white set | untested |
| no colour until the product / colour only where the data is | monochrome world; first colour is the product; hue only on status tokens | openai-intelligence-age@00:54 · linear-agent@00:12 | post / code | reserve the brand hue | untested |
| one hero colour / one accent | one hue per film carried into the closing type and logo | apple-iphone-17-pro@00:50.1 · higgsfield-hell-grind@01:36 | post | protect one hue | untested |
| warm story, cold product | tungsten story, cool blue-white product hero | nothing-phone-3@00:24.9 | post | grade per act | untested |
| eclipse horizon stage | dark arc with rim glow becomes the UI floor | ig-extra-chatgpt-image-concept@00:00.5 · claude-fable-5-2-launch (horizon) | post / gen | ellipse + inner glow | untested |
| site card over a 3D sculpture | a browser card before a soft 3D form | ig-mitkow-3d-robotics-site@00:00 | 3D + post | render the form once | untested |
| hand-made texture as anti-AI signal | scanned ink, brush, paper grain on every frame | ordinaryfolk-distance | post | grain + texture overlay, animate on 4s/5s | untested |
| native-aspect samples / mixed aspect collage | samples kept in their own aspect ratio inside black | apple-iphone-18-pro-intro@01:53 · anthropic-keep-thinking@00:07 | post | pillar/letterbox, no crop | untested |
| light-to-plate comp | generate the background first, light the product to it | trillo-notes-vfx-breakdown@00:23 | gen + 3D/post | match key direction, colour, contrast | untested |

## 8. Sound

| Technique | What it is | Seen in | Make with | How | Status |
|---|---|---|---|---|---|
| low boom under transitions (not cuts on the grid) | a designed sub hit sits under most cuts; the cuts follow the picture, not the beat grid | apple-iphone-17-pro@00:03.0 (64% of cuts vs 16% chance) | sound | sub-heavy boom ±1 frame; only on cuts that change ideas | untested |
| inner motion on the music | movement inside the shot lands on the hits (all 8 Apple 2025 films) | apple-iphone-17-pro · apple-macbook-neo (71% of events on onsets at ±2 frames) | post | key motion peaks to onsets, not the cuts | untested |
| cuts locked to percussion | hard cuts within ±1 frame of drum hits | apple-macbook-pro-14-m6@00:04.47 (×7.55) · apple-created-on-mac-surrender@00:11.3 (cut on each instrument entry) · ig-kryvetskyy-cgi-lens@00:01.1 | post + `film_study.py` | percussive-onset pass; snap cuts | untested |
| music section change on picture section change | the song's lift lands on the act cut | apple-macbook-neo@00:11.32 | sound / post | edit the music so the drop sits on the act cut | untested |
| silence before the hit / quiet before the slam | 0.5-3 s of near-silence before the key moment | apple-event-sep26@00:20.8 · apple-iphone17-scratch@00:17.0 · apple-created-on-mac-surrender@00:02.8 · higgsfield-hell-grind@01:11 (trailer stop-down) | sound | bed down 15-20 dB; slam on the action | untested |
| music hole before a key line / stop the beat on the decision | a 0.3-0.5 s stop in the music | apple-iphone-17-colors@00:05.41 · nothing-phone-3@00:17.0 · ig-qasim-spotify-ui-ad@00:02.88 | sound | gate 0.5 s; type lands as music returns | untested |
| bass as structure | no low end during the problem; bass drops in on the reveal word | mvsm-canva-affinity@00:10.5 | sound | high-pass the music under 150 Hz until the reveal | untested |
| sparse intro, beat on the first wow | clicks only until the first transformation, then the track | figma-config-2025@00:09 · apple-macbook-pro-m5@00:00 (silent typing opener, 18 s) | sound | downbeat on the first transformation frame | untested |
| sub-bass swell as the only hit | one low swell at the first prompt, the same swell when the job is done | linear-agent@00:03.4, @00:40.5 | sound | ~2 s sine swell; reuse as bookend | untested |
| silent bookends / sign-off into silence | true silence before the first sound and after the logo; logo 1-2 s before music ends, then ~5 s silence | openai-this-is-sora-2@00:00 · all 15 Apple films · anthropic-claude-design-intro@01:15 · linear-agent | sound | the house ending | untested |
| riser into a hit, dead stop | riser dies on the landing frame, sub hit on the land | tobi-fable-5-2-one-prompt · apple-event-sep26 (8 riser-in cuts in the cold open) | sound | lab 001: clicks get masked under a riser; make them cut through | partly (lab 001) |
| in-scene sound only / count-in sync | no score, each shot carries its sync sound; an on-screen count sets the beat | openai-this-is-sora-2@00:02 · openai-sound-on-sora-2@01:33 | sound / gen (Flow audio) | cut on transients | untested |
| score ducks for proof | music −10 dB so the demo's own sound is heard | google-veo-3-1@01:03 | sound | duck 8-10 s | untested |
| J-cut / L-cut | next audio starts before its picture / outgoing audio continues over the new picture | lesson-scene-transitions@16:25, @17:24 · apple-iphone-18-pro-intro (12 lines lead their cut) | post | 4-16 frames; L-cut to hide AI joins | untested |
| audio match | a sound becomes a similar sound in the next scene | lesson-match-cuts@04:09 | sound | same key; 2-3 frame crossfade | untested |
| perfectly timed SFX | SFX transient 1-3 frames before the cut | lesson-edgar-wright-visual-comedy@06:20 | sound | | untested |
| cut to silence on the logo | music drops under the final logo | mvsm-openai-images-2@00:58.9 · figma-config-2025@01:16 | sound | 1-2 s silence | untested |

## 9. Voice

| Technique | What it is | Seen in | Make with | How | Status |
|---|---|---|---|---|---|
| calm narrator under a dense edit | low male voice 97-130 wpm over 0.5-1 s cuts; the picture carries the speed | apple-event-sep26 cold open (97 wpm) · apple-iphone-18-pro-intro (112-129 wpm, ~110-130 Hz) · mvsm-samsung-micro-miracles (98 wpm) | VO / TTS | ~120 wpm, real pauses | untested |
| causal-chain VO | second person; each line's result causes the next; loops back to its first line | apple-iphone-18-pro-intro@00:15 · apple-macbook-pro-proled-touch@00:00.5 | script | A → B → C, one shot per link | untested |
| one-word antithesis | two lines that differ by one word, split by a black frame | anthropic-keep-thinking@00:15 | script / VO | identical reads | untested |
| claim per 2 s shot | one 2-4 word claim per shot slot, calm, ~86 wpm | ig-pavmotion-mouse-light-reveal@00:00 | VO | | untested |
| user-voice montage | 4-6 short prompts by different voices and languages, no narrator | openai-intelligence-age@00:48 | VO | slight overlap | untested |
| conversational female VO under kinetic type | warm read ~110 wpm; end card typed word by word with it | mvsm-canva-affinity@00:02.4 · apple-event-sep26-recap (creator voice, 140 wpm) | VO | key each word to its onset | untested |
| no VO at all | product text is the copy | linear-agent · figma-config-2025 · 7 of 8 Apple 2025 ads | - | the default for software films | untested |

## 10. Story structures

| Technique | What it is | Seen in | Make with | Status |
|---|---|---|---|---|
| pitch and reject | show wrong openings, reject each ("Forget all that"), then the classic one | apple-event-sep26@00:12-02:09 | any | untested |
| real-proof cold open | open on a real result made with the product | apple-iphone-18-pro-intro@00:00 | shoot / code | untested |
| proof by story | one scene where the product survives a social moment | apple-iphone17-scratch@00:24.6 · apple-iphone17pro-detectives (self-aware feature line) | shoot / gen | untested |
| flaw named early, paid off by one word | the climax reverses the flaw stated in minute one; music withheld through the low point; shots lengthen as emotion rises | apple-glad-i-met-you@00:03, @08:17 | shoot | untested |
| motif seeded in frame 1 / callback prop | the payoff shape appears in the first frame | ordinaryfolk-distance@00:00 · higgsfield-the-kiss@03:27 | any | untested |
| guide element ends as the product | the graphic carried through the film becomes the product UI | openai-intelligence-age@00:46 · mano-grocery | post | untested |
| open on the finale, then rewind | skip to the best reveal, then go back | apple-event-sep26-recap@00:00.6 | post | untested |
| truth caption first | an opening note stating what is real | mvsm-samsung-micro-miracles@00:00 | post | untested |
| claim → proof shot | every spoken claim cut to the shot that proves it | apple-glad-i-met-you-making-of@00:57 | post | untested |
| genre roulette / tools-of-the-trade opener | each shot a different genre; macro shots of the craft's tools first | openai-this-is-sora-2 · openai-sound-on-sora-2@00:05 | gen | untested |
| post-credits stinger / satisfying loop ending | a gag after the logo; end on a tactile open/close loop | openai-sound-on-sora-2@02:03 · apple-event-sep26-recap@01:24.5 | any | untested |
| three-act trailer + button | logo, cold open, lore, stakes, montage, title, joke, date | higgsfield-hell-grind@00:00 | gen | untested |
| hand-over in the cut | one figure walks out in the dark, the next walks in from the light | apple-event-sep26@02:25-02:36 | shoot / gen | untested |

## 11. AI-generated shots (how to direct Flow plates)

| Technique | What it is | Source | Status |
|---|---|---|---|
| style prefix | one block of light, palette, lens and audio rules pasted first in every prompt ("no music, no text") | lesson-higgsfield-ai-films@03:43 | untested |
| keyframe-first, anti-plastic | perfect the stills first (haze, colder light, grain, crushed blacks), then frames-to-video | lesson-higgsfield-ai-films@11:54 | untested |
| space reference sheet | two stitched views of a location so the camera can move | lesson-higgsfield-ai-films@31:34 | untested |
| one continuous motion | one action, one named camera move, "In a single continuous shot … No scene cuts" | lesson-higgsfield-ai-films@77:06 · `bequite-motion-director/references/ai-generation.md` | untested |
| direct emotion, not mechanics | a mood line + one micro-action instead of step lists | lesson-higgsfield-ai-films@89:58 | untested |
| batch-and-diagnose | batch 4-8; shared fault → fix the prompt; details off → batch more; budget dozens per hard shot (about 1% kept) | lesson-higgsfield-ai-films@48:55, @113:53 | untested |
| duplicate-frame QA | detect frame-rate drops and doubled frames (ffmpeg mpdecimate) | lesson-higgsfield-ai-films@123:47 | untested |
| cut around the AI error / motion-mush hiding | trim head morphs; keep fast AI action to 4-12 frames under flashes and booms; L-cut across joins | lesson-higgsfield-ai-films@83:29 · higgsfield-hell-grind@02:34 | untested |
| stylised CG to dodge AI tells | toy-like or stylised characters; realism only for slow close-ups | higgsfield-the-kiss@00:32 · nexo-opus-5-5 | untested |
| gen-video luma matte / generative fill plates | generated moving light as a matte; outpaint and clean plates | trillo-notes-vfx-breakdown@00:56, @00:42 | untested |
| style-swap on continuous action | one base action restyled N times, cut at the same timecode | google-gemini-omni@00:09 | untested |
| AI can't carry action across angles | only 8 of 92 Hell Grind cuts carry action from shot to shot: stage action within one shot, not across cuts | higgsfield-hell-grind | observed |

## Measured truths that correct common advice

1. **Apple does not cut on the beat grid.** Across 15 Apple films, cuts follow the voice or the picture; the sync comes from booms placed under cuts (iPhone 17 Pro ×4 chance), motion inside shots landing on hits (all 8 films of 2025), and music section changes on picture section changes. Only the M6 film cuts hard on drums (×7.55). The fast flicker montages are free-running.
2. **Smoothness comes from a constant**: product, type line, sentence, UI chip, player bar or mask shape held still while everything else changes; plus motion carried across cuts and long stretches with no cut (16-35 s).
3. **Narrators are slow** (97-145 wpm) under fast edits. Most product ads have no narrator at all.
4. **Every Apple film ends the same way**: logo 1-2 s before the music ends, then about 5 s of silence.
5. **Loudness is not one number**: premium films range from −9 (Canva) to −29 LUFS (Linear); several official uploads clip above 0 dBTP. Deliver at −14 LUFS / −1 dBTP; don't copy their masters.
6. **The labs selling intelligence avoid AI-looking footage** (Anthropic: real footage; OpenAI: pure graphics); the labs selling generation show generation. A BeQuite film should use Flow plates only stylised or under ~0.5 s.
7. **AI keep rates are about 1%** for hard shots (72 generations for one 10 s shot): budget credits accordingly.
