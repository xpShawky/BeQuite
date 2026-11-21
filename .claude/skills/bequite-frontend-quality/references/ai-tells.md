# AI tells: the owner's list, validated against real sites (2026-11-21)

The starting list comes from the owner (BeQuite v1 reference-first doctrine, section 6). Each tell was checked on three human-made reference pages with `tell-sweep.js` on 2026-11-21. Result: real sites also trip some tells, so **a hit is a question, not a verdict**. Fix it, or justify it in one line (brand colour, a deliberate choice taken from a named reference). A tell becomes a defect when it is a default nobody chose, or when it dominates (the hero, every heading, every card).

## Web pages

| Tell (owner's words first) | Detector key | Linear | Stripe | Apple AirPods Pro | Typical AI test page |
|---|---|---|---|---|---|
| Purple-to-blue gradients, gradient backgrounds | `purpleToBlueGradients` | 1 | 6 (brand purple `rgb(83,58,253)`) | 0 | 1 (the hero) |
| Gradient headline text | `gradientHeadlineText` | 0 | 0 | 0 | 1 |
| "01 / 02 / 03" labels above every section | `numberedSectionLabels` | 0 | 1 | 0 | 3 |
| Thin body font with every heading bold (two weights everywhere) | `thinBodyBoldHeadings` | no (400 body / 510 headings) | no (300 body / 300 h1) | no (400 / 600) | body 300 / headings 800 |
| Glass cards everywhere | `glassCards` | 0 | 1 | 1 | 3 at desktop |
| Centred hero, three feature cards, testimonial grid | manual | no | no | no | yes |
| Emoji as icons | `emojiAsIcons` | 0 | 1 | 0 | 0 |
| One radius and one shadow for everything | `oneRadiusEverywhere` | no (9999, 8, 12, 4 px) | no (4, 6, 1 px) | no (28, 36, 10 px) | 24 px only |
| Perfect symmetry | manual | | | | |
| Vague copy ("Unlock the future", "seamlessly streamline") | manual, plus the writing tells | concrete | concrete | concrete | vague |

What the references did instead (measured):

- **Headlines** are not bold-800. Linear h1 64 px, weight 510, tracking -1.408 px (-2.2%), line-height 1.0. Stripe h1 48 px, weight 300, tracking -0.96 px (-2%). Apple h1 28 px weight 600 (the big type lives in h2-level display sizes up to 96 px).
- **Weights** are three to five steps, odd values included (Linear 400, 510, 590; variable fonts).
- **Inter is not a tell by itself.** Linear runs Inter Variable (381 of 473 text nodes). The tell is Inter at default tracking with weight 300 body and 800 headings.
- **Radii** follow component size: small controls 4 to 8 px, cards 12 px (Linear) or 28 px (Apple), pills 9999 px.
- **Text colour** is a ramp, not white and grey: Linear uses four greys from `rgb(98,102,109)` to `rgb(247,248,248)`.

## Presentations and documents (owner's list)

- Note boxes under paragraphs with a coloured left border (orange, yellow) and a "Pro tip" or "Key takeaway" label (`leftBorderNoteBoxes` catches the border).
- A title plus three bullets on every slide; every slide in the same layout.
- Emoji bullets.
- A summary slide that repeats the deck.

## Motion

The same ease on everything · fade-and-scale for every entrance · cuts that ignore the beat · letter-by-letter typing with no reason · glow on everything · a whoosh on every move · a camera that drifts with no motive · zooming in too far.

## Copy on pages (from the writing tell list)

Inflated importance ("a testament to"), groups of three, "not just X but Y", promotional adjectives ("cutting-edge", "seamless"), vague claims with no number, a closing line that states the moral. Source: Wikipedia "Signs of AI writing" (sections Content, Language and grammar, Style).

## Images

Plastic skin, garbled text, mirrored faces, the generated sheen. Prefer a real photo, a real product screenshot or a drawing made in code.

## How to run

1. Open the page in a browser tool at desktop width, then at a phone width (375 x 812). Measure only in a visible or emulated viewport: a hidden pane reported `0x0` and wrong layout values on 2026-11-21.
2. Run `tell-sweep.js` (same folder) in the page. It is read-only.
3. For each hit: fix, or write one line of justification naming the reference or brand rule.
4. Do the manual rows by looking at the full-page screenshot next to the references.
