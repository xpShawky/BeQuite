# Motion grammar: easing, transitions, camera

Most important first: **strong ease-out on everything that arrives, motivated transitions only, cut in the middle of a move, and one constant element for the eye to follow.** This file is the single home for easing and smoothness; `bequite-kinetic-type` and the engine adapters link here.

## Smoothness — what makes motion feel expensive

- 60 fps masters; motion blur on (shutter 180–270°, 16+ samples in AE; matching blur in other engines). 30 fps + per-scene easing + no real blur read as "not smooth" in the field case.
- Never linear, except constant drifts.
- Springs / overshoot only on things that **land** (icons, pills, cards, a logo) — never on text that must be read immediately.
- Anticipation 2–4 frames before a fast move; a whip is 6–10 frames.
- Overlap and stagger sub-elements (40 ms is a good default) so groups don't move as one block.
- Exits matter as much as entrances: unwrite, a motivated whip, or a handoff — never a hard pop-off on a hold.
- Overlap handoffs: the exit of one element shares ~0.3–0.4 s with the entry of the next, so there is no empty frame.

## Easing by intent

| Intent | Curve | CSS / web | AE graph (influence %) |
|---|---|---|---|
| element **enters** and lands | decelerate (ease-out) | `cubic-bezier(0.16, 1, 0.3, 1)` (strong) · `cubic-bezier(0, 0, 0.2, 1)` (standard) | outgoing 0–15, **incoming 70–95** |
| element **exits** | accelerate (ease-in) | `cubic-bezier(0.7, 0, 0.84, 0)` · `cubic-bezier(0.4, 0, 1, 1)` | **outgoing 70–90**, incoming linear-ish |
| **transition / whip** | steep in-out, sharp peak ("burst then settle") | `cubic-bezier(0.65, 0, 0.35, 1)` or steeper | both 80–95, short duration, peak where the cut/swap is |
| **hold drift** | near-linear, tiny distance | `linear`, 1–3 % of frame over the hold | linear or 10–20 % |
| **playful pop** | overshoot (back-out) | spring or `cubic-bezier(0.34, 1.56, 0.64, 1)` | overshoot 5–10 % then settle in 4–8 frames |
| **calm / premium brand** | gentle curves, little overshoot | `cubic-bezier(0.25, 0.1, 0.25, 1)` | 33–60 |

Asymmetric curves (fast out, long landing) look more natural than symmetric ones. The AE library's named curves (`expo`, `inout`, `whip`, `in`, `soft`) implement this table (`.claude/skills/bequite-render-pipeline/assets/ae/lib/core.jsx`).

## Transition grammar

Every transition must be **motivated** and say one thing. Choose 2–4 kinds for a film and write them in the Motion DNA.

| Transition | What it is | Use when | Rule |
|---|---|---|---|
| **Match cut (graphic)** | cut between two objects that share position, size, silhouette, brightness | an object "becomes" the next idea (a full stop grows into an app icon) | four matches: anchor (±2–3 % of frame width), screen area, silhouette, luminance; cut at peak velocity; one meaning per transform |
| **Cut on action** | the motion of shot A continues in shot B | a swipe, a tap or a throw drives the next scene | for a 12-frame move, cut on frame 6, pick up on frame 7 |
| **Object wipe** | a foreground object (device edge, ribbon, white surface) fills the frame for 1–3 frames and hides the cut | changing place or subject without a visible edit | the cut sits under the wipe's widest frame |
| **Zoom-through** | push into a sub-frame (screen, lens, letter counter) and come out in the next scene | going "inside" the product or a detail | exponential scale (a linear Z move in 3D) feels constant; a linear scale feels like it slows |
| **Whip** | 6–10 frames of fast travel with heavy directional blur | energy beats, list of problems, tempo | direction consistent within a film; whoosh starts a few frames before the peak |
| **Motivated wipe** | a shape/mask wipe that starts from an object (circle from a button, line from a cursor) | UI flows, step changes | the wipe's origin is something the viewer was looking at |
| **Morph** | one shape's path becomes another's | icons, logos, simple shapes | pair objects matching in ≥ 2 of colour, shape, volume; swap at the fastest moment or behind blur |
| **Blur / focus pull** | the scene defocuses out and the next focuses in | calm reveals, after a busy beat | short (0.2–0.4 s); not more than once or twice per film |
| Cross-dissolve | — | end card, time passing | sparingly; never as the default |

Pitfalls: anchor drift of a few percent makes a match cut "jump" (check by onion-skinning the two frames at 50 %); shape matches but brightness doesn't → a flash; cutting on a still frame → the eye catches the swap; chaining transforms with no settle → leave ~1 s between consecutive transforms.

## The guide element

One continuous element that carries the eye through the film (a light comet, a line, a selection outline, a cursor, a ribbon). It draws the logo, outlines the pills, becomes the route, underlines the key word.

- It must have a **destination**: it ends somewhere meaningful (it becomes the logo, the icon, the final underline). A guide that just hovers at the end feels unfinished.
- It belongs to the product's world (a selection outline for an image tool, a cursor for a desktop app).
- One guide per film. It does many jobs; that is what ties the film together.

## Camera language

- One master camera / null per scene; slow drift always (0.5–1 % of the frame).
- Push in on interactions (a click, a result); pull out to reveal context.
- Small shake (≤ 10 px at 1080p) only on a big hit, never on readable text.
- Parallax: background moves less than midground, midground less than the subject.
- Orbit while travelling between UI stops (a 3D camera that only translates looks like a pan).
- Match the camera move across a cut on action.

## Sound sync (decided with `bequite-sound-voice`)

Sound sells continuity: a whoosh, tick or chime on the cut frame; SFX 1–3 frames **before** the visual hit (sound that arrives late reads as lag).
