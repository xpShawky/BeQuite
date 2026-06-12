---
description: Reference Engine (C3). Turn a screenshot, competitor URL, or app flow into a design extraction + clone-safe rebuild blueprint with originality guardrails. Modes — screenshot / url / flow / style=<direction>. Never copies assets; extracts principles and mandates differentiation.
---

# /bq-reference — inspiration → original design direction (C3)

Full spec: `docs/specs/REFERENCE_ENGINE.md`. Follows the 12-step execution contract (`docs/architecture/COMMAND_EXECUTION_CONTRACT.md`) including automatic skill routing, Confidence Forecast, and the step-12 router block.

## Syntax

```
/bq-reference screenshot "<goal>"        ← image(s) → design-system extraction
/bq-reference url "<goal>"               ← competitor URL → clone-safe rebuild blueprint
/bq-reference flow "<goal>"              ← app flow → analysis + a better version
/bq-reference style=cinematic-3d "<goal>" ← named direction brief (3D/animated lives here)
```

## Preconditions / gates

`BEQUITE_INITIALIZED`. Read per contract step 1; plus `.bequite/design/DESIGN_DNA.md` if it exists (output merges via delta, never overwrites silently).

## Steps (after contract steps 1–7)

1. **Intake** — load the screenshot(s) / fetch the URL (public pages only) / parse the flow description. Record source + access method in `REFERENCE_BRIEF.md`.
2. **Extraction** — principles, not pixels: palette logic, type hierarchy, spacing rhythm, component patterns, motion cues, product-type signals → `DESIGN_EXTRACTION.md` + `COMPONENT_MAP.md`.
3. **Originality guardrails (mandatory)** — `ORIGINALITY_GUARDRAILS.md`: what was extracted · what must NOT be reproduced (logos, copy, assets, trademark elements) · required deltas. A request to pixel-copy is refused with this file as the answer.
4. **Rebuild blueprint** — `REBUILD_BLUEPRINT.md` (section-by-section, build-order aware) + for `url` mode the mandatory `DIFFERENTIATION_PLAN.md`.
5. **DNA merge** — `DESIGN_DNA_DELTA.md`; on user approval the delta merges into `.bequite/design/DESIGN_DNA.md` (Design Continuity Gate then governs implementation).

## Writes

`.bequite/reference/{REFERENCE_BRIEF,DESIGN_EXTRACTION,DESIGN_DNA_DELTA,COMPONENT_MAP,ORIGINALITY_GUARDRAILS,REBUILD_BLUEPRINT,DIFFERENTIATION_PLAN}.md` + AGENT_LOG + LAST_RUN.

## Skill routing (auto)

frontend-design-system (master) · ux-ui-designer · frontend-quality · researcher (`url` mode) · localization-rtl on Arabic/RTL signals.

## Next Command Recommendations (typical)

Required next: **W2.5 `/bq-uiux-variants`** (multiple directions wanted) or **W2.3 `/bq-feature`** (direction approved) — can auto-run: yes.
Set: W2.3 feature → W4.1 verify (visual QA) → W4.2 `release proof` (case study). Do not run yet: W2.x build before the user approves the delta (design direction = user decision).
