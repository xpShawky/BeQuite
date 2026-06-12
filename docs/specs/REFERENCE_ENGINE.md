# Reference Engine — `/bq-reference` (C3) — alpha.22

Turn visual/product inspiration into an original, buildable design direction. **Clone-safe by charter**: the command is named *reference*, never "clone-style"; language throughout is reference / inspiration / design extraction / rebuild plan / originality guardrails.

## Modes

| Mode | Input | Output focus |
|---|---|---|
| `screenshot` | image file(s) | design-system extraction (palette, type, spacing, components, motion cues) |
| `url` | competitor/public URL | clone-safe rebuild blueprint + differentiation plan |
| `flow` | app flow description/screens | flow analysis + a *better* version proposal |
| `style=<name>` | named direction (e.g. `cinematic-3d`) | curated direction brief fed to frontend-design-system (V1 #10 lives here) |

Examples: `/bq-reference screenshot "extract a design system from this"` · `/bq-reference url "clone-safe rebuild blueprint for this competitor"` · `/bq-reference flow "analyze this onboarding and improve it"`.

## Originality guardrails (hard rules)

1. Extract **principles** (hierarchy, rhythm, palette logic), never pixel-copy assets, logos, copy, or trademarked elements.
2. `ORIGINALITY_GUARDRAILS.md` is always written and lists: what was extracted, what must NOT be reproduced, required deltas.
3. `DIFFERENTIATION_PLAN.md` is mandatory for `url` mode — a rebuild that isn't differentiated is refused.
4. Output feeds `.bequite/design/DESIGN_DNA.md` via `DESIGN_DNA_DELTA.md` — the Design Continuity Gate then applies as usual.

## Outputs — `.bequite/reference/`

REFERENCE_BRIEF · DESIGN_EXTRACTION · DESIGN_DNA_DELTA · COMPONENT_MAP · ORIGINALITY_GUARDRAILS · REBUILD_BLUEPRINT · DIFFERENTIATION_PLAN (created on first run; dir scaffolded by installer).

## Routing

Skills: frontend-design-system (master) + ux-ui-designer + frontend-quality; researcher for `url` mode. Next: W2.5 variants → W2.3 feature → W4.1 verify (see COMMAND_ROUTER journey "website style"). Confidence Forecast applies per contract.
