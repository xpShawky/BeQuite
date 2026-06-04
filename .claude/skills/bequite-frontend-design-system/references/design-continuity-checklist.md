# Design Continuity Checklist

The detection logic behind the Design Continuity Gate. Each row = a drift tell + how to detect it (grep heuristic and/or visual check) + the fix. Run on **every** section, not a sample. Gate spec: `docs/architecture/DESIGN_CONTINUITY_GATE.md`.

> Grep patterns are heuristics for a quick first pass (great for low/medium effort). They produce candidates, not verdicts — confirm visually. False positives are fine; the goal is to surface middle-section drift early.

## Typography

| Tell | Grep / detect | Fix |
|---|---|---|
| All-caps misuse | `text-transform:\s*uppercase` / Tailwind `uppercase` on non-label elements (>4 words) | sentence case; caps only on ≤4-word labels/badges |
| Wide letter-spacing | `letter-spacing` > `0.12em`; any positive tracking on body | tracking 0.05–0.12em on caps labels only; 0 on body |
| Flat hierarchy | heading sizes within ~10% of each other; sizes off the scale (14/15/16) | enforce type scale ratio ≥1.2; hierarchy = size+weight+color+space |
| Broken hierarchy | body font-size == h2; multiple H1 | one H1; clear step-down |
| Off-DNA font | `font-family` not matching DNA §7; new font with no recorded reason | use the DNA font; record any change |
| Oversized hero copy | `clamp(` max > ~6rem; max > 2.5× min | cap hero scale; `text-wrap: balance` |

## Color & contrast

| Tell | Grep / detect | Fix |
|---|---|---|
| Weak contrast | axe-core; manual ratio check (<4.5:1 body, <3:1 large/UI) | meet WCAG 2.2 AA; use paired on-color tokens |
| Gray-on-color | muted/gray token on colored/dark bg | darker shade of bg hue or on-color token; muted FG still ≥4.5:1 |
| Pure black / cold gray | `#000`, `#fff`, cold grays where brand wants tinted neutral | tinted neutrals (0.005–0.015 chroma toward brand) |
| AI gradient | `linear-gradient(` purple→blue / purple→pink on hero/large surfaces | solid brand color unless brand is genuinely that hue |
| Gradient text | `background-clip:\s*text` + gradient | solid color / weight / size |
| Side-stripe accent | `border-left`/`border-right` > 1px colored | full border, bg tint, or nothing |

## Layout & components

| Tell | Grep / detect | Fix |
|---|---|---|
| Inconsistent radius | `border-radius` values off the scale; `>= 32px` on cards | ≤3 radius values; cap cards 12–16px |
| Nested cards | a card class inside a card class | one card depth; group with space + hairline |
| Identical card grids | same icon+heading+text block repeated 3+ | vary section format; not every section is cards |
| Cliché SaaS layout | eyebrow kicker every section; `01/02/03` markers; big-metric+stats hero | earn numbers only in real sequences; drop default eyebrows |
| Ghost card | `border: 1px` + `box-shadow` ≥16px together | pick one, never both |
| Text overflow | long word + large clamp + narrow container; no `min-width:0` | cap scale; `min-width:0`; `text-wrap` |
| Random/uniform spacing | values off 4/8pt scale; one gap everywhere | rhythm by contrast (8–12 within, 48–96 between) |
| Mixed icon styles | two icon families; emoji as structural icons | one family + weight; no emoji icons |

## Interaction & state

| Tell | Detect | Fix |
|---|---|---|
| Dead button | styled button without handler/href | real handler or explicit disabled+reason |
| Missing focus | `outline:\s*none` with no replacement | visible `:focus-visible` ring ≥3:1 |
| Weak empty/loading/error | placeholder "no data"; spinner that never resolves | real states (acknowledge→value→CTA; skeleton; what/why/how) |
| Noisy motion | bounce/elastic easing; `img` `:hover` transform; whole-section scroll-fade; no reduced-motion | ease-out exponential; transform+opacity; reduced-motion fallback; reveal-safety |

## Identity (the comparative test)

| Tell | Detect | Fix |
|---|---|---|
| Off-DNA section | mood/density/voice differs from the hero/DNA | re-align to DNA §3–§14 |
| Quality cliff | a middle section visibly worse than the strongest section | pull it up to the strongest section's bar |
| Generic AI UI | second-order slop test: could you guess the design from the product category alone? | inject DNA-specific identity (type, color system, layout) |

## The two-second tests

- **Squint test** — blur your eyes (or downscale the screenshot): hierarchy + groupings should still read.
- **Quality-cliff test** — name the strongest and weakest sections; the gap must be closed before PASS.
- **Slop test (two altitudes)** — (1) guessable from category alone? (2) guessable aesthetic family from category + anti-refs? Both must be "no."

## Output

Record findings per route in `.bequite/design/DESIGN_CONTINUITY_REPORT.md` with severity (BLOCKER/HIGH/MEDIUM/LOW), fix applied, verification method, and the quality-cliff result.
