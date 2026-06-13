---
description: Brand Kit Generator (C14). Build a non-generic brand identity from niche, audience, competitors, and positioning — name directions, brand DNA, visual identity, color + typography strategy (with WHY-it-fits-the-niche reasoning), logo brief, do/don't associations, content tone, platform fit, asset roadmap. Researches real niche examples; extracts patterns and gaps; never clones. Avoids generic AI logos/names/colors.
---

# /bq-brand-kit — non-generic brand identity (C14)

Full spec: `docs/specs/BRAND_KIT_ENGINE.md`. Follows the 12-step contract. Skills: ux-ui-designer + frontend-design-system + researcher (niche scan) + writing-dna (tone) + localization-rtl (Arabic/MENA). Reference-safe: extracts patterns, never copies (shares C3's originality discipline).

## Syntax

```
/bq-brand-kit "<niche + audience + what the brand does>"
```
Examples: tech content creator · course platform · industrial/factory · kidswear ecommerce · academic publishing · AI automation agency · SaaS product · local business brand.

## Steps (after contract steps 1–7)

1. **Brief + positioning** — `BRAND_BRIEF.md` + `AUDIENCE_AND_POSITIONING.md` (who, what they expect, the positioning gap).
2. **Competitor/reference scan** — `COMPETITOR_AND_REFERENCE_SCAN.md`: research real successful brands in the niche (researcher skill); extract what works + where everyone looks the same (the differentiation gap). Reference-safe — patterns not pixels.
3. **Identity** — `NAMING_DIRECTIONS.md` (several directions + rationale, not one generic name) · `BRAND_DNA.md` (personality, values, promise) · `VISUAL_IDENTITY.md` · `COLOR_STRATEGY.md` (**why these colors fit THIS niche + audience**, not default purple-blue) · `TYPOGRAPHY_STRATEGY.md` (why this type fits) · `LOGO_BRIEF.md` (concept brief for a designer/tool — not a generated logo).
4. **Guardrails + reach** — `DO_AND_DONT_ASSOCIATIONS.md` (what the brand should/shouldn't be associated with) · `CONTENT_TONE.md` · platform fit (YouTube/LinkedIn/X/FB/IG/website/packaging) · `ASSET_ROADMAP.md` · `NEXT_STEPS.md`.

## Anti-generic rules

No default Inter+purple-gradient identity · every color/type choice carries niche-fit reasoning · naming avoids generic AI patterns · differentiation from the scanned competitors is explicit · no cloning of any scanned brand (originality guardrails).

## Writes

`.bequite/brand/{BRAND_BRIEF,AUDIENCE_AND_POSITIONING,COMPETITOR_AND_REFERENCE_SCAN,NAMING_DIRECTIONS,BRAND_DNA,VISUAL_IDENTITY,COLOR_STRATEGY,TYPOGRAPHY_STRATEGY,LOGO_BRIEF,DO_AND_DONT_ASSOCIATIONS,CONTENT_TONE,ASSET_ROADMAP,NEXT_STEPS}.md` (first run) + AGENT_LOG + LAST_RUN.

## Next Command Recommendations (typical)

Required next: **C3 `/bq-reference`** (turn the visual identity into a design system) or **W2.3 `/bq-feature landing`**. Set: C2 `/bq-writing-dna` (lock the tone) · C17 `/bq-start` (platform/account strategy) · C15 `/bq-community`. Do not run yet: generating a final logo image — the brief feeds a designer/tool; BeQuite specs identity, doesn't fabricate a logo.
