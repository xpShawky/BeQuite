# 3D, object transformations and the filmed look

Most important first: **block the film in 2D first (animatic + music grid), then make each transition a 3D event, and keep UI, text and logos out of the 3D render** — composite them sharp on top. How to build in Blender or AE is in the engine adapters (`.claude/skills/bequite-render-pipeline/references/adapter-blender.md`, `.claude/skills/bequite-render-pipeline/references/adapter-after-effects.md`); this file is what to aim for and why. Recipes here are practitioner synthesis unless marked; prove each one small before relying on it.

## Make every transition a 3D event, not an edit

- **Content swap inside speed:** change the screen content (lock screen → app) on the frame of maximum motion blur during a fast move.
- **Object swap behind a wipe:** fly the camera into a device's edge until a white surface fills the frame; on that frame hide object A and show object B at the same spot; fly out.
- **Object becomes the stage:** ribbon bands tighten around a cup, flatten into a plinth, the next product rises out of it. No cut at all.
- **Through-object camera:** fly through an opening (a logo cut-out, a lens, a cup) into the next scene placed elsewhere in the same 3D space.
- Leave ~1 s of settle between consecutive transforms. Each transform must mean something ("the app gets you the coffee"); random morphs read as tricks.

## Pop-outs from a screen

Two kinds: a UI element lifts off the glass (a card grows out of the status area with a shadow), or objects break the screen frame.

1. The element starts **pixel-identical** to the screen image (same pixels, same place) so it reads as UI.
2. Then it gains depth: Z toward camera, +5–15 % scale, a soft shadow on the screen growing softer and further, over 0.4–0.6 s ease-out.
3. Reveal a "hole" or empty state underneath, or the trick shows.
4. For "rising out of the phone", matte the part still inside the screen; the part above sits over the bezel.

Pitfalls: a visible jump at frame 0 (not pixel-identical); no shadow → looks pasted on.

## Ribbons and swooshes around a product

Look: wide, flat, double-sided (brand colour one side, white the other), satin sheen, thin visible thickness, motion blur. Keep ribbons on the side opposite the text, and slow them to a drift during reads. Builds: curve + flat profile grown from 0→1, a mesh strip on a curve modifier hugging the product, or in 2D two masked copies (behind / in front of the product). Details per engine in the adapters.

## The filmed feel

What moves a graphic film toward "shot with a camera":

- real lens language: shallow depth of field, a rack focus on the reveal, gentle vignette, very slight lens distortion
- light wrap and soft contact shadows where objects meet a surface
- a constant fine film grain over everything (the same on 3D, UI and AI plates)
- handheld-style camera noise (recorded or noise-driven) instead of a pure sine drift, for lifestyle pieces
- one grade for the whole film: slightly lifted blacks, one LUT or curve, no over-saturated "AI teal-orange"
- a real device render (or the real UI corner-pinned at native resolution) instead of flat window cards

## Suggested 3D pipeline

1. 2D animatic with flat cards + music grid; lock timing.
2. 3D scene with the product, a camera rig (camera tracking an animated target gives smooth orbits), 2–3 large soft lights or a studio HDRI at low strength, a shadow-catcher floor.
3. Screen as a separate emission plane — or no screen at all: export the screen's four corner positions per frame so the real UI is corner-pinned in the compositor at native resolution (sharp, editable without re-rendering 3D).
4. Render passes (16-bit PNG or EXR with alpha): back ribbons · product · front ribbons · shadow · screen corners.
5. Composite: real text, real UI, grade, grain. Retime and regrade without re-rendering.

## AI video in a 3D film

Only for organic in-betweens (ribbons unfurling, a splash, beans tumbling, cloth) or to bridge two rendered frames (start/end-frame generation with identical lighting and perspective). Never for UI, text, logos or exact device geometry. Details and current tools: `ai-generation.md`.

## A studied 3D app ad (reference pattern)

From a frame study of an 18 s 3D app ad (coffee chain, music only; timings measured from contact sheets and an ffmpeg motion-energy pass; the film itself is third-party, so only the analysis is kept here):

- **Rhythm:** a new beat roughly every 2.3 s; each transition peaks for 0.3–0.5 s then decays over ~1 s; readable holds of 1–1.9 s; only one near-cut in the whole film — everything else is a continuous camera move or an object transformation.
- **Beats:** macro on extruded glass clock digits with accelerating parallax → fast pull-out reveals the phone (the only near-cut) → phone tilts while the screen content swaps inside the motion blur and satin ribbons burst out → slow orbit hold → the camera dives into the phone's edge, a white surface wipes, a white cup appears (fastest moment, object wipe + colour match) → a three-word lockup builds on the empty side with blur + slide → ribbons tighten into bands, flatten into a plinth, the phone rises from it → a status card lifts out of the screen (pop-out) → phone exits while the next line starts typing (overlap handoff) → end frame "Made for [icon] calm" → icon and word swap in place → brand name types on, ~1.6 s end hold.
- **Look:** cool palette in the opening, warm brand palette after; high-key soft light; defocused natural photo behind a big white shape; type always on clear negative space, never over ribbons.
- **What to take:** burst-then-settle rhythm; swaps hidden in speed; object wipe on a colour match; inline icon + word swap; type kept off the 3D action.
