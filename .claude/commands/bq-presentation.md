---
description: BeQuite Presentation Builder. Create PPTX or HTML presentations from a topic, folder, Word doc, PDF, images, transcript, brand assets, or research sources. Strict mode preserves source material; creative mode adds structure. Starts from studied reference decks, supports variants, and runs the presentation tell list on rendered slides before delivery. Installs nothing by default.
---

# /bq-presentation: a deck that looks designed by a person

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

A studio-pack route: `PIPELINE.md` stages 0, 1, 2 (reference decks), 5 (content, slide and design plans), 6 (the user approves the plan, and picks a variant), 7 (build), 9 (rendered slides pass the tell sweep), 10. The procedure, the format table with checked library versions, and the tell list are in `bequite-presentation-builder`; Arabic and right-to-left decks add `bequite-localization-rtl`; voice comes from `bequite-writing-dna`.

## Syntax

Natural language, with optional `key=value` settings anywhere:

```
/bq-presentation Create a 30-minute lecture about infection control for doctors
/bq-presentation format=pptx strict=true source=./materials Turn this Word file into slides
/bq-presentation format=both variants=3 "A keynote about our product"
```

| Option | Values | Default |
|---|---|---|
| `format` | `pptx`, `html`, `both`, `auto` | `auto`: decided by what the audience will do with the file |
| `variants` | 1 to 10 | 1 |
| `source` | a folder, PDF, Word file, URL, or none | inferred |
| `strict` / `creative` | `true` / `false` | strict when source files are given, creative for a topic alone; both set: strict wins |
| `audience`, `duration`, `language`, `style`, `brand` | free text or a path | inferred |
| `references`, `notes` | `true` / `false` | references on for academic work; notes on |
| `motion` | `none`, `subtle`, `keynote`, `cinematic` | from the audience |

A word is a setting only as `key=value` or in a leading `[...]` block. In "a lecture about fast learning", "fast" is the topic, not a mode.

## Gates

Needs `BEQUITE_INITIALIZED` and any source paths to exist. Hard human gates: installing a library or tool (each needs the ten decision questions and a yes), using brand assets the user has no rights to, publishing to any cloud slide service, and picking the winning variant. The plan is approved before any slide is built.

## Steps

1. **Parse** the request and settings; write `.bequite/presentations/PRESENTATION_BRIEF.md` (topic, audience, duration, format and why, strict or creative, sources).
2. **Take in the sources.** Strict mode: every claim on a slide traces to a source, nothing is invented, references are kept. Creative mode: hooks and structure are allowed, and every assumption is marked.
3. **Study references first:** the brand's own decks if they exist, otherwise three to five decks by real designers for this kind of talk, measured (grid, type sizes per level, palette, words per slide, how layouts vary). Write `DESIGN_BRIEF.md` with numbers, not adjectives.
4. **Plan:** `CONTENT_OUTLINE.md` (hook, promise, arc), `SLIDE_PLAN.md` (one purpose and a specific title per slide, the visual, varied layouts), `MOTION_PLAN.md` (motion only where it explains), `SPEAKER_NOTES.md` and `REFERENCES.md` when asked.
5. **Variants** (`variants>1`): different directions from different references, compared in `PRESENTATION_VARIANTS_REPORT.md`; stop for the user's pick.
6. **Approval:** show the plan and wait for a yes.
7. **Build** into `.bequite/presentations/outputs/` with the chosen, approved tool. Then render every slide to an image and look at the images, not the code.
8. **Tell sweep and side by side** on the rendered slides (the list is in the skill): every hit is fixed or justified in one line; three slides are compared with three reference slides at the same size.
9. **Verify and log:** the file opens in its target app without errors; `EXPORT_LOG.md` records the tool, the output path and the checks; the sweep result goes to `evidence.md`.

## Output

```
Presentation: <title> (<format>, <n> slides, <strict | creative>)
Output: .bequite/presentations/outputs/<slug>.pptx | <slug>/index.html
Checked: rendered <n>/<n> slides, tell sweep <clean | n fixed>, opens in <app>
```

## Quality gate

The design brief holds measurements from named references; every slide was seen rendered; strict mode has a source for every claim; nothing was installed or published without a yes.

## Next Command Recommendations (typical)

`/bq-verify` for the artifact · `/bq-writing-dna` when the deck must sound like its speaker · `/bq-handoff` when it ships to someone else.
