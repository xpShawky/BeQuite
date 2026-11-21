---
name: bequite-presentation-builder
description: Use for any slides, deck, lecture, keynote, pitch, PowerPoint or HTML presentation, or turning a PDF, Word file, transcript or topic into slides (/bq-presentation, /bq-auto presentation). Picks the format by audience and what must stay editable, starts from studied reference decks or the brand's own material, plans motion that earns its place, and runs the owner's presentation tell list before delivery so the deck does not look machine-made.
last_verified: 2026-11-21
sources:
  - https://support.microsoft.com/en-us/office/use-the-morph-transition-in-powerpoint-8dd1c7b2-b935-44f5-a74c-741d8d9244ea
  - https://support.microsoft.com/en-us/office/morph-transition-tips-and-tricks-bc7f48ff-f152-4ee8-9081-d3121788024f
  - https://python-pptx.readthedocs.io/en/latest/
  - https://gitbrent.github.io/PptxGenJS/
  - https://github.com/slidevjs/slidev/blob/main/docs/guide/exporting.md
  - https://github.com/marp-team/marp-cli
  - https://www.w3.org/TR/WCAG22/#contrast-minimum
  - https://support.microsoft.com/en-us/office/tips-for-creating-and-delivering-an-effective-presentation-f43156b0-20d2-4c51-8345-0c337cefb88b
---

# bequite-presentation-builder

A deck should look like a designer made it for this talk. That starts from real decks studied and measured, and ends with a check against the tells that give generated decks away. The 14-step run lives in `.claude/commands/bq-presentation.md`; this skill holds the decisions.

## When to use

- `/bq-presentation`, `/bq-auto presentation`, and any request for slides.

Not for: a document or a web page (other skills); a video (`/bq-motion`).

## Procedure

1. **Format by what the audience will do with it:**

   | Need | Format | Note (checked 2026-11-21) |
   |---|---|---|
   | Others will edit it; institutional, lecture, medical | PPTX built natively (python-pptx 1.0.2 or PptxGenJS 4.0.1, both MIT) | Neither library writes transitions; Morph is set in PowerPoint |
   | Cinematic keynote, product demo, screen-recorded explainer | HTML (reveal.js 6.0.2 has Auto-Animate, speaker view, PDF export; Slidev 53.1.0) | Needs a browser to present |
   | Both | One content plan, two renders | |
   | Markdown-first and needs a PPTX | Slidev `--format pptx-editable` or Marp `--pptx-editable` (experimental) | Plain `--format pptx` in both is pictures of slides: text not editable |

   Every library is a candidate; the ten questions decide. Write the choice and why in `PRESENTATION_BRIEF.md`.
2. **References first** (human-taste doctrine): the brand's own decks and guide if they exist, otherwise three to five reference decks from real designers for this kind of talk. Measure them: grid and margins, type families and sizes per level, palette in hex, words per slide, image treatment, how many layouts recur. Write `DESIGN_BRIEF.md` with the numbers before any slide.
3. **Content discipline.** Strict mode (source files given): every claim traces to the source; nothing invented; references kept. Creative mode (topic only): structure and hooks allowed; every assumption marked on the slide and in `ASSUMPTIONS.md`. Both flags: strict wins.
4. **Slide plan** `SLIDE_PLAN.md`: one purpose per slide in one sentence; specific titles (not "Introduction", "Overview"); text readable at the back of the room (Microsoft: avoid under 18 pt; projector body 24 pt or more); contrast at least 4.5:1, 3:1 for large text (WCAG 2.2). Vary the layout with the content: a number slide, a quote slide, a full-bleed image, a diagram, a comparison.
5. **Motion** `MOTION_PLAN.md`: only where it explains (something moves, grows, is replaced). PPTX: Morph between two slides that share objects; force matches by naming both `!!name` in the Selection Pane; same object type; charts do not morph. HTML: auto-animate between matched elements, staged reveals, one easing family. No animation on every slide.
6. **Build only when asked**, then open the file and render every slide to an image (PowerPoint export, LibreOffice, or the HTML in a browser). Look at the images, not the code.
7. **Tell sweep** (owner's list plus the web tells), on the rendered images. Every hit is fixed or justified in one line:
   - note boxes under paragraphs with a coloured left border (orange, yellow) and a "Pro tip" or "Key takeaway" label;
   - a title plus three bullets on every slide; every slide in the same layout;
   - emoji as bullets or headings; random icons in mixed styles;
   - a summary slide that repeats the deck;
   - purple-to-blue gradients, gradient headline text, "01 / 02 / 03" labels above every section;
   - thin body text with every heading in heavy bold, the same two weights everywhere;
   - one radius and one shadow on everything; stock people photos; "synergy", "leverage", "unlock".
8. **Side by side and deliver:** three rendered slides next to three reference slides at the same size; list five differences, each a choice. Variants (`variants>1`) are different directions, not colour swaps; the user picks the winner (hard gate). Then verify and write `EXPORT_LOG.md`.

## Worked example (2026-11-21)

Request: "A 12-slide Arabic lecture for doctors from my Word file; they will edit it."
- Format: native PPTX (they edit), strict mode, RTL rules from `bequite-localization-rtl`.
- References: the faculty's own template plus three conference decks; measured: 16:9, 64 px margins, one Naskh body face at 28 pt, two accents.
- Motion: one Morph sequence for the diagram that builds across slides 5 to 7 (`!!heart`, `!!valve` names), nothing else.
- Tell sweep on the rendered slides finds slides 3, 4 and 8 all "title + three bullets" and a yellow left-bordered "Key takeaway" box on slide 9: slide 4 becomes a single statistic, slide 8 a comparison table, the box is removed and its sentence becomes the slide title.

## Quality gate

- `DESIGN_BRIEF.md` holds measurements from named references, not adjectives.
- Every slide was looked at as a rendered image; the tell sweep result is in `evidence.md`.
- Strict mode: every claim traces to the source.
- The file opens in its target app without errors.

## Boundaries

Installs nothing by default; each library needs a decision. No other brand's logos or assets without permission. No publishing to cloud slide services.
