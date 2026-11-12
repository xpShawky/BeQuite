# Style system for THIS product

Most important first: **default to a quiet neutral stage + ONE brand accent + ONE type family.** Choose the style per product from its own UI, audience and feeling; never paste one look onto every film. The locked result goes in `spec.md` § Motion DNA (template in `phases-and-artefacts.md`).

## Four questions before any styleframe

1. What does the product's own UI look like? Start the film from that, so the film feels like the product.
2. Who watches? Pros and scientists want calm, precise, honest visuals; consumers can take more colour and energy.
3. What is the feeling? Relief → calm neutrals, slow ease-outs. Power → dark, high contrast, fast cuts. Delight → colour, springs. Trust → paper, ink, generous holds.
4. What must never happen? (e.g. no colour wash over medical images, no unpublished data, no competitor logos.)

## Plain vs living background

No authoritative rule exists; this is the working heuristic (one hero per frame):

| Use a **plain / quiet** stage when | Use a **living / busy** field when |
|---|---|
| text, UI or product detail must be read | nothing must be read: transitions, energy beats, interstitials |
| the product is the colour mass (photos, footage, UI) | the brand has a real pattern or motion system |

"Living" means slow and quiet: a soft vignette, one slowly drifting light pool, constant fine grain, real objects at depth with parallax. It never means multi-hue blurred blobs, colour washes over real content, or a gradient with no brand reason.

A gradient is fine only when it is (a) built from the brand's own two hues, (b) low in contrast, (c) slow or static, (d) behind the UI, never over the content. Fight banding with 16-bit work, a little grain, and a high-bitrate master (`bequite-render-pipeline`).

Light ↔ dark stage flips are allowed when the story motivates them (tension = dark), but two stages alternating can read as two templates. Prefer one world whose light changes.

## One brand hue

- Neutral + ONE accent. The accent marks the single thing to look at in each shot: the active button, the result, the key word. Roughly 5–8 % of the frame.
- Choose tints in a perceptual space (OKLCH/LCH) so "same lightness" really looks the same.
- Semantic colours only with their meaning: red = failure/error, green = success.
- Delivery assets (9:16 frames, call-to-action pills, PDF) use the **film's** accent and shapes, not a new colour.

## Filmed vs graphic

| Graphic (flat/2.5D) | Filmed (photographic) |
|---|---|
| clean stages, cards, kinetic type, UI | real lens: depth of field, rack focus, light wrap, contact shadows, constant grain, gentle vignette, one grade |
| fast to build and change; cheapest | needs 3D renders, footage or careful AI plates (`3d-and-filmed-look.md`) |
| fits tools, SaaS, explainers | fits hardware, lifestyle, premium consumer |

Mixing is fine if one grade, one grain and one motion-blur look cover every shot.

## Product type → style

| Product type | Background | Accent | Type | Motion |
|---|---|---|---|---|
| Pro creative / science tool | paper white or graphite | the product's one accent | neutral grotesk, 2 weights | precise ease-outs, honest demo, few springs |
| Developer tool | near-black, visible grid | one cold accent | grotesk + mono | fast, snappy, keyboard-feel cuts |
| Consumer app | warm off-white or a brand colour field | 2–3 brand colours inside illustration | friendly grotesk, bigger sizes | springs, character, playful match cuts |
| Hardware / premium | black or white seamless | product colour only | display sans at huge sizes | slow camera, macro detail, long holds |
| Fintech | white + one brand gradient field | brand primary | precise grotesk | smooth, confident data animation |

What big systems say (verify current pages before quoting): Apple's HIG — few typefaces, avoid light weights at small sizes, glass only on floating controls and sparingly; Linear — themes from base + accent + contrast in LCH, one family in two optical cuts, elevation by small lightness steps; Vercel/Geist — neutral + one blue, the grid as a visible element; Stripe — its famous gradient is a custom brand shader behind crisp UI, never on it; Material — one seed colour → tonal roles.

## Type for phone viewing

Most product films are watched on a phone. Rules of thumb for a 1920×1080 master (×1.33 for 2560×1440):

- hero line 96–160 px · supporting line 48–64 px · UI labels that must be read ≥ 28–32 px · nothing that carries meaning under ~24 px
- 3–7 words on screen at once; keep text inside the centre ~90 %; text on empty space, never over a busy object
- one family (two optical cuts at most), two or three weights, no Light/Thin at small sizes; follow the font's own tracking guidance (many grotesks tighten ≈ −2 % on display sizes; some system display fonts must not be tightened)
- **check every styleframe at phone size** (a 390 px-wide preview) before `STYLE_LOCKED`; a card that fills 25–40 % of a 16:9 frame looks elegant at 2K and too small on a phone

## Depth, shadow, glass, device frames

- Elevation = small lightness steps + ONE soft shadow (large blur, low opacity, slight Y offset).
- Glass on one floating layer at most; never a whole background or card.
- Use a device frame only when the device is part of the message. For desktop software, a cropped floating window or panel on a neutral ground reads more premium than a laptop mockup.
- Real UI, simplified: remove clutter, enlarge the one control that matters, keep real labels.

## Banned list (starter — extend per film)

multi-hue blurred blobs · purple→blue or pink→orange gradients with no brand reason · coloured overlays on real photos/medical/scientific images · lens flares · stock "tech" particles · three identical cards · mixed fonts (except where the meaning *is* "wrong fonts") · every line entering the same way · AI-drawn logos, UI or text.

## Style-lock checklist

- [ ] Background chosen and justified (neutral by default)
- [ ] ONE accent hex + what it marks in each shot
- [ ] ONE type family, weights, tracking, size scale; checked at phone size
- [ ] Grid: columns, margins, base unit
- [ ] One shadow recipe; glass rule
- [ ] Easing set + spring rule (`motion-grammar.md`)
- [ ] Graphic or filmed; grade and grain if filmed
- [ ] Banned list
