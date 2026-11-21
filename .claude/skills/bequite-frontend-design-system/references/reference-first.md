# Reference first: collect, measure, extract (frontend, 2026-11-21)

Every design task starts from studied human work. Gate: `REFERENCES_STUDIED` in the work's `gates.md` (installed with the v1 human-taste doctrine); the second gate, the human test, is ticked only after the owner's verdict.

## 1. Collect (3 to 10 references)

Use the user's references first. Otherwise pick by domain and show the set to the user before measuring:

| Need | Where to look |
|---|---|
| Whole pages | awwwards.com (Sites of the Day), land-book.com, siteinspire.com, lapa.ninja, minimal.gallery, httpster.net, framer.com/gallery |
| Scroll, 3D, live backgrounds | tympanus.net/codrops, awwwards Sites of the Day, the live reference site |
| Components and product UI | 21st.dev, mobbin.com, refero.design, figma.com/community |
| Mood and art direction | savee.it, cosmos.so, are.na, behance.net, dribbble.com |
| Type | fontsinuse.com, typewolf.com |

Record per reference: URL, date opened, why chosen. godly.website redirected to another domain over plain HTTP on 2026-11-21; it was not followed.

## 2. Measure (numbers, never adjectives)

Open each live page in a browser tool. Run `../../bequite-frontend-quality/references/tell-sweep.js` and read computed styles (`getComputedStyle` returns resolved values). Record:

- h1, h2, body: family, size, weight, tracking, line-height, colour
- weight steps and size steps actually used (counts)
- text colour ramp and background colours
- radii in use, shadows, borders
- sections, sticky elements, canvas, video, motion libraries loaded
- phone width: h1 size and line count, horizontal scroll, what disappears

## 3. Measured examples (2026-11-21, 1920 x 945 viewport)

| Value | linear.app | stripe.com | apple.com/airpods-pro |
|---|---|---|---|
| Families | Inter Variable (381 text nodes), Berkeley Mono (92) | sohne-var (468), SourceCodePro (4) | SF Pro Text (466), SF Pro Display (176) |
| h1 | 64 px / 510 / -1.408 px / lh 64 px | 48 px / 300 / -0.96 px / lh 55.2 px | 28 px / 600 / 0.196 px |
| Body | 15 px / 400 / -0.165 px / lh 24 px | 14-16 px / 300 | 14-17 px / 400 |
| Weights used | 400, 510, 500, 590, 300 | 300, 400 | 600, 400 |
| Top text sizes (px) | 12, 13, 14, 15, 10, 16, 48, 24 | 16, 10, 26, 12, 22, 9, 14, 8 | 12, 24, 17, 28, 21, 19, 56, 96 |
| Text colours | 4-step grey ramp `rgb(98,102,109)` to `rgb(247,248,248)` | navy `rgb(6,27,49)`, slate `rgb(80,97,122)`, brand `rgb(83,58,253)` | `rgb(29,29,31)`, `rgb(51,51,54)`, alpha blacks |
| Page bg | `rgb(8,9,10)` | white with gradient canvas | `rgb(255,255,255)` |
| Radii | 9999, 8, 50%, 12, 4 px | 4, 6, 1, 5, 2 px | 28, 50%, 36, 10, 999 px |
| Sections / height | 8 / 10,054 px | 17 / 14,880 px | 19 / 29,119 px |
| Motion media | 0 canvas, 0 video, 58 gradient layers | 2 canvas (animated gradient) | 16 video, 4 sticky |

Phone check: Chrome's window resize did not change the viewport of the page (stayed 1920 px wide), so phone measurements need device emulation (the built-in browser pane's mobile preset, or DevTools device mode).

## 4. Extract the DNA

Write rules, each with its measured example, and a never-list. Example rules drawn from the table:

- "Headlines tight and medium weight": tracking about -2% at display sizes, weight 500-600 (Linear -2.2% at 510, Stripe -2% at 300).
- "Grey ramp, not grey": at least three text greys with one job each.
- "Radius follows size": controls 4-8 px, cards 12 px or one larger value, pills full.
- Never: gradient headline text; numbered section labels as decoration; 800-weight headings over 300-weight body.

Put the DNA in `.bequite/design/DESIGN_DNA.md` with the references listed at the top.
