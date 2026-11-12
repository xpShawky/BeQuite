# iOS 26, "Introducing Liquid Glass" (Apple): breakdown

**File:** `inbox/New/iOS 26_ Introducing Liquid Glass.mp4` · **Source:** owner-provided (Apple keynote segment) · **Length / format:** 273.9 s (267.2 s of picture + 6.6 s silent tail), 1280x720, 29.97 fps · **Studied from:** metrics, director sheet, transcript, contact sheets at 1 s (open, title, end) and 0.5 s (a menu morph), `matches.jpg`, second-pass sync test (65 detector cuts → 78 edits). Long film: studied the opening, the title, the material demos and the ending; the middle UI tour was read from `shots.jpg`.
**Category:** UI demo · presenter-led explainer · brand film

## 1. The story in one line
An Apple presenter (named on a lower third at 00:14) introduces a new software material that behaves like real glass, shown on screens, in renders and as physical glass objects on a table. It feels considered, tactile and premium.

## 2. Story shape
Architecture (glass) → presenter: why software matters → history (iOS 7) → abstract glass → universal design across devices → **title: a droplet forms and names itself** → the material in controls → concentric layout → morphs (alerts, menus, tab bars) → icons and widgets → physical prototypes → presenter wrap → glass logo → silence. **Presenter + B-roll explainer** with three "pure motion" interludes.

## 3. Beat sheet
| Time | What we see | What we hear | Technique | Why it works |
|---|---|---|---|---|
| 00:00-12.4 | Apple Park: curved glass roof, a ring staircase, glass panels, sky | music only; first cut 3.40 | **architecture establishes the material** | glass is in the viewer's eye before the word |
| 00:13-31 | presenter in a glass-walled studio with a lower-third name card (14); cutaways to iPad, Mac and iPhone in use | VO starts; 145 wpm | presenter + cutaway cadence | |
| 00:31-52 | a single 20.7 s presenter shot (history) | VO carries | the long hold | the one place it trusts a talking head |
| 00:52-70 | abstract blue glass ribbons (52-59); at **59.87 a blue glass ribbon cuts to blue glass "9:41" numerals**; glass app icons (61.9-67) | | **material match cut** (same material, new object) | the abstract becomes the UI |
| 01:10-01:44 | presenter; the design across Mac dock, Watch, TV, Vision Pro room, a stylus on paper-like notes | | | |
| 01:45-02:00 | dark void; an arc of light becomes a glass lens, the lens shrinks to a droplet (105-110); cut to white with embossed frosted "Liquid Glass" (111-113); the lens slides along a blue slider as its knob (114-117), becomes a glass toggle (118), then a tab bar (119) | the name is spoken at 1:46-1:53 | **droplet title reveal**: the material forms, names itself, then becomes a control | one object carries you from concept to UI |
| 02:00-03:06 | slide to answer over a patterned dress, music player, Dynamic Island, lock screen glass clock, media app; **lateral and vertical moves carried across 13 cuts** (motion cosine 0.89-1.0, e.g. 2:05.85, 2:20.04, 2:22.37) | | motion carried across the cut | the camera never stops, so the tour feels like one move |
| 02:46-02:52 | physical acrylic shapes on a table, a top-down table of colour swatches and a screen | | **physical prototypes of a digital material** | proof that the material was designed as an object |
| 03:06-03:26 | presenter; a phone in hand: a menu **expands from the button that was tapped** (191-194), a context menu grows out of the touch point (195-198) | VO names each behaviour as we see it | **UI morph from the touch point** | cause and effect inside one frame |
| 03:26-04:16 | icons in layered glass (light, dark, tinted, clear), dock and widgets, a clear acrylic "hello", glass slabs pushed by hands (236-246), control centre, FaceTime | top-10 % hits at 3:36, 3:43, 3:48, 4:02, 4:09 | | |
| 04:16-04:28 | presenter wrap; home screen; a **glass Apple logo with rainbow refraction on white** (265-268) | VO ends; bed resolves | the logo made of the product | |
| 04:27-04:34 | black | silence 267.17-273.76 | silent tail | |

## 4. Signature techniques
- **Transitions:** mostly hard cuts on the VO; the craft is in **continuous motion through cuts** (13 motion-carried) and in one material match (59.87). Only 2 of 65 cuts are graphic matches: position-locking is not this film's tool.
- **Typography:** almost none on screen; the one title is the material itself (frosted embossed "Liquid Glass" on white). Labels are the real UI.
- **UI motion (the reason this film is in the library):** controls are glass lenses that magnify and refract what is under them (slider knob, toggle); menus and alerts grow from the touch point instead of appearing centred; tab bars shrink on scroll; corner radii concentric with the device. Specular highlights move with the device tilt.
- **Camera:** pull-outs 18.5 % (the highest in the set), inner-motion 39 %, locked 26 %; slow, smooth moves on 3D phone renders.
- **Colour and background:** white and pale grey stages, deep blue glass, colour from content and wallpapers; a dark void only for the title.
- **Pacing:** ASL by quarter 4.03 / 3.60 / 5.27 / 3.42 s; mean edit interval 3.47 s. The edit follows the visuals, not the sentences: 50 of 65 cuts fall mid-line, 15 in pauses.
- **Sound:** **−19.2 LUFS** (the quietest of the eight; voice-led), LRA 3.4 LU, true peak −0.6 dBFS; a music bed at ~117.5 BPM under 95 % voice coverage; 38 sudden −15 dB drops follow the gaps between spoken phrases. Low booms at 27 % of edits vs 17 % chance (×1.57, p = 0.023): the UI moments get soft hits. Picture change vs sound cross-correlation z = **4.2** (the strongest in the set).
- **Voice:** one on-camera presenter, 632 words, **145 wpm**, median F0 ≈ 154 Hz (mid register; the presenter on screen is a man), longest pause 1.4 s: calm, explanatory, unhurried. One line sums the register: "it starts with an entirely new expressive material".

## 5. When to use this style
- Fits: design-system or UI-material launches, "how it feels" explainers, keynote segments; 2-5 min.
- Avoid when: under 60 s (the presenter structure needs time), or for social ads.
- Cost and difficulty: high for the full film (presenter shoot, 3D phone renders, physical acrylic props). The reusable parts are cheaper: the droplet title (Blender glass shader, 5-10 s) and UI morphs from the touch point (Rive / Framer / AE shape morphs).

## 6. What to steal (adapt, never copy)
1. **Droplet title reveal:** the core object forms from light, names itself, then becomes the first working control. For BeQuite: a gate ring forms, "BeQuite" sits in it, then it becomes the first passing check.
2. **Establish the material before the word:** 12 s of real glass architecture before "Liquid Glass" is said.
3. **UI grows from the touch point:** every popover and menu expands from the tap, 0.3-0.5 s, never fades in centred.
4. **Physical prototypes** filmed on a table to make a digital idea tangible (acrylic or 3D-printed "commands", "gates").
5. **Keep the camera moving through cuts** so a long UI tour reads as one continuous move.

## 7. Open questions / UNVERIFIED
- Whether the physical glass objects are props or CG composites: UNVERIFIED.
- The 38 "sudden drops" are measured on the mixed track; whether the music ducks or stops between phrases needs a listen: UNVERIFIED.
