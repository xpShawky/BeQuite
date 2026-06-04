# Design Continuity Gate

**Status:** active (v3.0.0-alpha.17)
**Owner skill:** `bequite-frontend-design-system`
**Gate name:** `DESIGN_CONTINUITY_PASS` (alias `DESIGN_CONTINUITY_OK`)
**Report:** `.bequite/design/DESIGN_CONTINUITY_REPORT.md`

---

## 1. The problem this gate exists to kill

AI-generated frontends pass the eye test at the **top** (the hero gets the model's full attention and the user's most explicit direction) and often at the **bottom** (the footer is simple). The **middle drifts**:

- middle sections look unfinished or "code-looking"
- text becomes ALL CAPS for no reason
- letter-spacing widens
- cards turn generic / identical / nested
- sections lose the visual identity established by the hero
- text escapes its container
- spacing becomes random (no rhythm)
- design quality does not stay consistent top → bottom

Root cause (verified against research — see `references/` in the master skill): LLMs exhibit **distributional convergence** — without a *persisted, re-read* design constraint, they sample the statistical center of their training data (generic) as the page gets longer and the original direction falls out of the live context window.

**The fix is structural, not cosmetic:** persist the design DNA, build section-by-section, and run this gate to compare every section against the DNA and against the strongest section.

> **The quality promise (alpha.17):** Hero quality is not enough. Every visible section must meet the Design DNA. No section is allowed to look like filler. No visible UI is "complete" without a Design Continuity pass and a Visual QA pass.

---

## 2. What the gate checks (surfaces)

Run across **every** surface present — not a 3-screen sample:

**Page regions:** hero · all middle sections (each one) · final sections · navigation · footer
**Components:** cards · forms · modals · dashboards · tables · buttons · inputs · menus
**Responsive:** mobile layout (360px) · tablet (768px) · desktop (1440px) · each defined breakpoint
**States:** empty · loading · error · hover · focus · disabled · success

For each section/component, the question is binary and comparative:
> "Does this match the Design DNA *and* hold the same quality bar as the strongest section on the page? If not, what specifically dropped?"

## 3. What the gate catches (the drift checklist)

A section FAILS continuity if any of these is present without a recorded, deliberate reason:

**Typography**
- ALL-CAPS misuse (caps on anything longer than a ≤4-word label/badge; caps body copy)
- excessive letter-spacing (tracking wider than ~0.12em on caps labels; any positive tracking on body)
- inconsistent font sizes (steps too close — the "flat hierarchy" tell; sizes off the type scale)
- broken hierarchy (body == heading; H1 styled like H4)
- inconsistent font family vs. the DNA

**Color & contrast**
- weak contrast (body < 4.5:1; large text/UI < 3:1 — WCAG 2.2 AA)
- gray text on colored backgrounds (washed out; use a darker shade of the bg hue, not literal gray)
- pure black `#000` / cold gray where tinted neutrals fit the brand better
- random gradients (esp. purple→blue / purple→pink "AI slop" gradient outside a genuinely purple brand)
- gradient text (`background-clip: text`) used decoratively

**Layout & components**
- inconsistent border-radius (off the radius scale; `radius ≥ 32px` on cards)
- nested cards without reason (card-in-card)
- identical icon+heading+text card grids repeated endlessly
- repeated SaaS-cliché layouts (eyebrow kicker on every section; `01/02/03` markers by default; big-metric+stats hero template)
- ghost-card pattern (`border: 1px` + `box-shadow ≥ 16px` together)
- side-stripe accent borders (`border-left/right > 1px` colored)
- text overflow / text escaping its container
- random/uniform spacing (no rhythm — same gap everywhere, or off the 4/8pt scale)
- inconsistent icon style (mixed icon families; emoji as structural icons)

**Interaction & state**
- unclickable or unclear buttons (styled-active but no handler; or no clear affordance)
- missing focus states (`outline: none` with no replacement)
- missing/weak empty, loading, error states
- motion too noisy (bounce/elastic easing; image-on-hover transforms; whole-section fade-on-scroll; no `prefers-reduced-motion` fallback)

**Identity**
- section does not match the design DNA (different mood/density/voice than the hero)
- generic "AI-looking" UI (the second-order slop test: could you guess this design from the product category alone?)

The detection heuristics (grep patterns + visual checks) live in `references/design-continuity-checklist.md` in the master skill.

## 4. Product-type awareness

Continuity is judged **against the product type's DNA**, not a universal template. A finance dashboard SHOULD be dense, dark, high-contrast; a wellness app SHOULD be soft and airy. The same "dense data grid" is correct for one and a continuity failure for the other. The gate reads `DESIGN_DNA.md` (which records the product type) and applies the matching row of `references/product-type-rules.md`. Supported product types include: SaaS landing, SaaS dashboard, admin panel, mobile app, restaurant/food-ordering, marketplace, medical, financial, developer tool, AI product, content platform, internal business tool, automation dashboard, e-commerce, booking app.

Per-type, the gate adapts: layout · navigation · density · typography · color mood · trust level · motion · CTA style · dashboard patterns · mobile-first needs · accessibility level (e.g. WCAG-AAA for medical/gov).

## 5. Severity

| Severity | Meaning | Ship impact |
|---|---|---|
| **BLOCKER** | section is broken or unmistakably off-DNA (text overflow, invisible text, dead button, hero-vs-middle quality cliff) | do not claim complete |
| **HIGH** | clear drift (generic card grid in the middle, all-caps misuse, contrast fail) | fix before complete |
| **MEDIUM** | inconsistency that erodes quality (radius off-scale, uneven rhythm) | fix this cycle |
| **LOW** | polish nit | track |

## 6. When the gate runs (command wiring)

The gate is a shared check referenced by — not duplicated into — these commands:

| Command | How the gate applies |
|---|---|
| `/bq-feature` | UI-typed features run the gate on every section of the new surface before "done" |
| `/bq-fix` | visual/cross-browser fixes re-run the gate on the touched page (a fix must not create new drift) |
| `/bq-auto` | `uiux`/`frontend`/`live-edit`/`variants` intents: completion REQUIRES a passing Design Continuity Report + Visual QA report |
| `/bq-uiux-variants` | each variant is continuity-checked; the winner gets a full-page pass after merge |
| `/bq-live-edit` | after each section edit, re-check that section + its neighbors against the DNA |
| `/bq-audit` | replaces "sample 3 screens" with a full section-by-section continuity sweep when a frontend exists |
| `/bq-review` | adds a "design continuity" dimension to per-file review of UI diffs |
| `/bq-red-team` | adds the attack angle "which section looks worse than the hero, and why?" |
| `/bq-verify` | when a frontend exists, a passing Design Continuity Report + Visual QA report is part of the gate matrix |

## 7. Effort awareness

The depth of the gate scales with `${CLAUDE_EFFORT}` (and treats Ultracode / xhigh as the deepest design-review mode):

- **low / medium** — compact check: run the grep heuristics from the checklist + spot-check the 3 weakest-looking middle sections.
- **high** — full check: every section + every component + every state against the DNA; write the full report.
- **xhigh / max / Ultracode** — deep design reasoning: section-by-section critique with persisted snapshots, full responsive + a11y/contrast sweep, browser visual QA where available, and a final polish pass. Treat Ultracode as "senior design review mode."

If `${CLAUDE_EFFORT}` is unavailable, infer from the operating mode: `deep` → high+, `fast` → compact, `token-saver` → compact + cached DNA, `delegate` → strong model authors the gate criteria, cheap model self-checks, strong model verifies.

## 8. Report

The gate writes `.bequite/design/DESIGN_CONTINUITY_REPORT.md`. One block **per page/route**, with: sections inspected · Design DNA summary · components inspected · issues found · severity · fix applied · verification method · screenshots (if available) · remaining risks · final status. See that file for the template.

## 9. Relationship to other gates

- **Composes with**, never replaces: `AUDIT_COMPLETE`, `REVIEW_APPROVED`, `VERIFY_PASSED`, axe-core a11y.
- **Requires**: `DESIGN_DNA_LOCKED` (you can't check continuity against a DNA that doesn't exist).
- **Feeds**: `VISUAL_QA_DONE` (the browser/manual render pass) and the mistake memory (`[fe][design]` entries).
- **Safety:** this gate is a quality gate, not a human gate. It does not bypass any of the 17 hard human gates. Variant-winner selection (#16) remains a human gate.

## 10. What this gate is NOT

- Not a Studio, dashboard, or new tool. It is a checklist + a report + a memory file.
- Not a replacement for human taste — it makes drift *visible and checkable*; the user still picks the direction.
- Not a license to over-animate or force cinematic/3D. "Continuity" means consistent with the DNA, which for most products means calm and consistent, not flashy.

See also: `FRONTEND_CONTEXT_ENGINEERING.md` (why design must be persisted, not held in chat), `.bequite/design/DESIGN_DNA.md` (the source of truth), and the master skill `bequite-frontend-design-system`.
