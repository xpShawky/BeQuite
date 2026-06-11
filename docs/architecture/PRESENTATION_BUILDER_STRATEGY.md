# Presentation Builder Strategy (alpha.19 consolidation)

> The architectural strategy behind `/bq-presentation` (alpha.13) — promised in the alpha.14 audit, delivered here. Operational detail lives in `.claude/commands/bq-presentation.md` + `.claude/skills/bequite-presentation-builder/SKILL.md`; this doc records the DESIGN DECISIONS so future changes don't re-litigate them.

**Status:** active · **Reviewed:** 2026-06-11 (Fable pass — capability re-verified complete: PPTX/HTML/both · variants 1–10 · strict/creative · references · speaker notes · brand assets · motion plan · morph-like planning ✅)

---

## Core decisions (settled — don't re-litigate)

1. **One command, arguments over command-family.** `/bq-presentation` with `format/variants/source/strict/creative/audience/style/...` options. `/bq-deck` alias remains deferred until user demand exists.
2. **Plan-first, render-on-request.** The command always produces the 9-artifact planning pack (`.bequite/presentations/`); rendering to .pptx/.html happens only on explicit request, with tool selection per tool neutrality (python-pptx / pptxgenjs / reveal.js / Slidev / Marp are CANDIDATES — decision section required before any install).
3. **Format is recommended, never silently defaulted.** PPTX = institutional/lecture/offline/Office; HTML = cinematic/responsive/demo; both = same content plan, two renders. Recommendation block in PRESENTATION_BRIEF with trade-offs.
4. **Strict beats creative on conflict.** `strict=true` → every claim traces to REFERENCES.md (Strict prompt class per PROMPT_ENGINEERING_STANDARD); `creative=true` → hooks/story allowed with assumptions marked.
5. **Morph-like motion = object-name continuity.** Stable object IDs across consecutive slides; duplicate-slide technique; 1–2 transforms at a time; 0.3–0.8s. HTML motion = restrained CSS/JS vocabulary; every effect earns its place.
6. **Style register is audience-derived:** cinematic (product keynote / demo) · academic lecture (university / medical / conference — restraint + references + speaker notes) · business keynote (executive — minimal, on-message). The skill's audience table picks; user can override via `style=`.
7. **Variants are design DIRECTIONS, not color swaps**; winner selection is a hard human gate.
8. **Design quality inherits the alpha.17 system:** DESIGN_BRIEF applies the same AI-slop rejection list as `bequite-frontend-quality`; when a deck belongs to a project with a locked `DESIGN_DNA.md`, the deck's palette/typography derive from it (brand coherence across product + deck).

## Integration map

- Context pack: `presentations/` 9 templates (see CONTEXT_ENGINEERING_STRATEGY pack table)
- Skills: presentation-builder (owner) + ux-ui-designer (design) + frontend-quality (HTML slop check) + researcher (source fetch) + anti-hallucination (strict-mode fidelity)
- Gates: variant winner selection · tool installation · external publishing · brand-asset rights — all hard human gates
- Modes: composable (deep = research-first deck; fast = tight single variant; token-saver = reuse cached outline; delegate = strong model plans deck, cheap model drafts speaker notes, strong model reviews)

## Known limits (honest)

- No deck has been rendered end-to-end in a live run yet (planning pack verified; render path awaits first real `/bq-presentation` invocation + tool decision)
- PPTX morph fidelity depends on the chosen generator's object-naming support — verify at tool-decision time
- Voice-recording workflow guidance is PPTX-centric; HTML deck narration left to the user's tooling
