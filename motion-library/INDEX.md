# Motion reference index

`/bq-motion` reads this first. Each studied reference has a full study in `refs/<slug>/breakdown.md` (story, beat sheet with timestamps, techniques, when to use, what to steal). Frames and contact sheets are in `refs/<slug>/frames/` (local only).

## References

| Slug | Category | Story in one line | Signature technique | Use when | Status |
|---|---|---|---|---|---|
| claude-opus-5-5-launch | AI launch film | "There's more to discover" | **one-shape match-cut montage**: 33 cuts in 20 s, every shot keeps the same arc; words hold still while the world changes; cuts accelerate with the music, then stop dead on the name | abstract products, model or research launches, brand films | studied 2026-11-12 |
| claude-fable-5-2-launch | AI launch film | a lone walker's journey along one horizon, from planet to cell and back | the same arc grammar, slower (1.9 s shots); **a tiny figure / worm walks the line** across worlds; **near-silence under the title** | thoughtful flagship launches, "goes far" products | studied 2026-11-12 |
| tobi-fable-5-2-one-prompt | dev-tool promo | "Most products stall; every product that lasts starts with a system, and every system starts with the right skills" | kinetic type with **design-tool bounding boxes**, a giant "BUT" turn, italic serif for the key word, skill cards swapping, a riser into a logo impact | dev tools, AI agents, SaaS; **closest template for a BeQuite film** | studied 2026-11-12 |
| nexo-opus-5-5 | 3D character demo | a cube mascot hops across a 3D dock and makes `useless.html` | **one continuous camera**, toy-like glossy 3D, tilt-shift, the product's real words as the joke | app/OS demos, iPhone/iPad app motion, playful social | studied 2026-11-12 |
| movez-motion-studio | UI motion loop | one button morphs through a dozen UI states and back | **shared-element morph**, 60 fps with a real cursor, seamless loop | web/app micro-interactions, landing hero loops, 1:1 social | studied 2026-11-12 |
| higgsfield-fable-5-2 | agent launch trailer | one prompt builds a whole dinosaur game, chapter by chapter | **prompt cards as chapter headings**, agent status lines with numbers, escalation per chapter (avoid: crushed −6 LUFS sound, AI-footage clichés) | "watch the agent build it" films, 60–90 s | studied 2026-11-12 |
| mano-grocery | app ad | "Out of groceries? Open Mano": one app for groceries, food and pharmacy | a single **light comet** draws the logo, outlines every pill, becomes the delivery route, spirals into the app icon | consumer apps with several features that need one thread | studied earlier (PlateMaker notes) |
| back-market | app ad | refurbished phones, easy and cheaper | whip transitions with heavy directional blur; UI cards assemble with blur; price counts up | commerce/fintech demos where "easy" is the message | studied earlier |
| kreatively-editor | service ad | "Still looking for an editor?": search, book, done | per-character blur write-ons; a word morphs into an icon; a typing search bar | service/marketplace pitches, creator audiences | studied earlier |
| starbucks-app | brand/app 3D | the app made for calm or talk | 3D ribbon choreography; an inline icon replaces a word, then both swap | lifestyle brands with no voice-over | studied earlier |
| spotify | brand/app | music cards and lyrics in motion | tilted 3D card grids, lyric focus pulls, words recoloured after writing | music, media and youth brands | studied earlier |

## Directions menu (pick 2–3 per film and say why)

| # | Direction | From | Feel | Cost |
|---|---|---|---|---|
| 1 | **One shape, many worlds** (match-cut montage on a fixed shape) | Opus 5.5, Fable 5.2 | premium, curious, scientific | medium (plate curation + alignment) |
| 2 | **A tiny protagonist walks the line** | Fable 5.2 | human, patient, poetic | medium |
| 3 | **A guide element with a destination** (light, line, comet) | Mano | energetic, unifying | medium |
| 4 | **Kinetic-type argument** (claim → BUT → insight → product) with design-tool overlays | Tobi "Construct" | smart, builder-oriented | low-medium |
| 5 | **Toy 3D one-take with a mascot** | Nexo | charming, playful | medium-high (3D) |
| 6 | **One element morphs through every UI state** (loop) | Movez | crafted, product-true | low-medium (code) |
| 7 | **Prompt-as-chapter agent trailer** | Higgsfield | epic, demonstrative | high |
| 8 | **Whip-blur UI commerce** | Back Market | fast, easy | low-medium |
| 9 | **Word → icon morph** | Kreatively | clever, light | low |
| 10 | **3D ribbon / object choreography** | Starbucks | warm, branded | medium-high |
| 11 | **Tilted card grids + recolour** | Spotify | youthful, musical | medium |

## Avoid list (generic or "made by AI" tells seen in references)

- Crushed, clipped loudness (−6 LUFS, peaks above 0 dB) with no dynamics. Master around −14 LUFS with real quiet moments.
- The default "AI startup" look: black + one orange/neon accent + particles everywhere. Keep the structure, invent the motif.
- Generic epic AI faces and "everything is golden hour"; legal text dumped over footage.
- AI-video tells: loud or missing breaths, frozen frames and clip-end slowdowns, camera moves that stop dead, sudden reaction zooms, morphing hands, gibberish text, floaty physics, objects that change between shots, the golden-hour + shallow-focus + slow-motion stock look. Full sourced list and fixes: `CRAFT_RESEARCH.md` section 3; QC gate: `bequite-render-pipeline/references/qc-checklist.md` B2.

Craft research (editing, kinetic type trends, AI-video fixes, Google Flow, sound): `CRAFT_RESEARCH.md`.

## Finished work (`inbox/I finished/`)

| Film | Files | Notes |
|---|---|---|
| PlateMaker promo (2026-11) | `PlateMaker_FINAL_2K.mp4` · `PlateMaker_FINAL_720p.mp4` | 57 s, 2560x1440 60 fps, −14 LUFS; case study in `.claude/skills/bequite-motion-director/references/case-study-platemaker.md` |
