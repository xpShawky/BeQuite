# Frontend Skill Integration Audit

**Generated:** 2026-06-04 (UTC)
**Trigger:** "Middle-section design drift" problem report — AI-generated frontends start strong (hero), then degrade in the middle (generic cards, all-caps misuse, wide letter-spacing, text overflow, lost visual identity, "code-looking" output).
**Release target:** v3.0.0-alpha.17 — Frontend Design Continuity upgrade
**Discipline:** This audit is step 0 of the alpha.14 feature-addition workflow ("audit before adding files blindly") and honors CLAUDE.md rule 14 ("BeQuite eats its own food").

---

## 0. Why this audit exists

The reported failure is **not** "BeQuite can't make a good hero." It is that **quality is not held across the whole page/app**. Diagnosed as four overlapping problems, not one:

1. **Context-engineering problem** — the design intent lives only in conversation memory and decays as the agent moves down the page. By section 4 the original direction is half-forgotten.
2. **Design-continuity problem** — there is no gate that compares a middle section against the hero's design DNA.
3. **Workflow problem** — implementation is "build the whole page, hope it looks good," not "build section → check section → continue."
4. **Visual-QA problem** — verification is code-inspection only; nobody renders the page and looks at section 5.

This audit inventories what BeQuite already has, what's missing, and the minimal lightweight additions that fix all four — **no Studio, no CLI, no dashboard, no new runtime dependency.**

---

## 1. Existing frontend-related COMMANDS

| Command | Frontend role today | Gap vs. continuity |
|---|---|---|
| `/bq-uiux-variants` | Generates 1–10 isolated design directions; user picks winner | Builds ONE reference screen per variant — never proves the whole page holds together |
| `/bq-live-edit` | Section-by-section edits via `SECTION_MAP.md`; smallest-change discipline | Has section mapping but no per-section *quality* check against design DNA |
| `/bq-feature` | 12-type router; types 1/8/9 (Frontend UI / Admin / Dashboard) activate FE skills | No requirement that all sections of the feature meet the same bar |
| `/bq-fix` | 15-type router; types 1/15 (visual-state / cross-browser) activate FE skills | Fixes one symptom; doesn't re-check page continuity after |
| `/bq-audit` | Has a "Frontend (if present)" section — console errors, contrast, responsive, 15 slop patterns | Audits *sampled* screens; explicitly says "Sample 3 screens" — middle sections slip through |
| `/bq-review` | Reviews the diff per-file | No design-continuity dimension in the 10 review axes |
| `/bq-red-team` | Angle #6 = UX (empty/loading/error, dead clicks, invisible text, touch targets) | No "section N looks worse than section 1" attack angle |
| `/bq-verify` | Gate matrix incl. Playwright e2e, console errors, secret scan | No section-by-section visual pass; no Design Continuity gate |
| `/bq-auto` | Intents `uiux` / `frontend` / `live-edit` / `variants` dispatch to FE flows | "Don't stop after a nice hero" is not encoded; completion criteria omit continuity/visual-QA |
| `/bq-suggest` | Recommends FE workflows | No "design continuity / full-page quality" route |
| `/bequite`, `/bq-help` | Menus | No mention of design-continuity surface |

**Finding C-1:** every command that touches a frontend does *something* right, but **none holds the page accountable from top to bottom**. The fix is one shared gate referenced by all of them, not eleven separate rewrites.

---

## 2. Existing frontend-related SKILLS

| Skill | Purpose | Overlap | Verdict |
|---|---|---|---|
| `bequite-frontend-quality` | Detects "AI-looking UI" in shipped code: 10 principles + 15 slop tells + component-sourcing order + tokens.css discipline + verification gates | Shares ~60% with ux-ui-designer (same 10 principles, same 15 slop list, restated) | **KEEP** as the *detection* supporting skill |
| `bequite-ux-ui-designer` | Generates non-AI-looking UI: 10 principles + 15 anti-patterns + token contract + hierarchy/color/a11y/responsive/micro-interactions + per-command playbooks | Shares ~60% with frontend-quality | **KEEP** as the *generation/design* supporting skill |
| `bequite-live-edit` | Section-mapped edits + 3-tier browser inspection (Playwright MCP → project Playwright → code-only) + rollback | Minimal overlap; complementary | **KEEP** as the *section-edit + browser-tier* supporting skill |

**Finding S-1 (duplication):** `frontend-quality` and `ux-ui-designer` both carry "the 10 design principles" and "the 15 AI-slop patterns," with slightly different wording. This is the kind of clutter the upgrade brief warns against. **Resolution:** introduce ONE master skill that owns the *canonical* expression of the rules + the *new* continuity/DNA/visual-QA discipline, and have the two existing skills point at it as the single source of truth (rather than competing copies). We do NOT delete them — they are activated by the 12-type / 15-type routers and referenced across commands; gutting them is high-risk for low gain. We de-duplicate by **designation, not deletion.**

**Finding S-2 (missing skill):** there is **no skill that owns design continuity, design DNA, section-by-section build discipline, product-type awareness, or visual QA.** Those concepts are scattered (a sentence in audit, a checklist in live-edit) or absent. This is the real gap.

---

## 3. Existing DOCS

| Doc | Relevance | Action |
|---|---|---|
| `docs/architecture/LIVE_EDIT_STRATEGY.md` | Section-edit strategy | Add Design Continuity Gate hook + effort awareness |
| `docs/architecture/UIUX_VARIANTS_STRATEGY.md` | Variant generation strategy | Add continuity-per-variant + effort awareness |
| `docs/architecture/AUTO_MODE_STRATEGY.md` | Auto-mode behavior | Add "frontend = full scope, not just hero" + effort awareness |
| `docs/architecture/MEMORY_FIRST_BEHAVIOR.md` | Read memory before acting | Add design memory (DNA / section map / context summary) to the read-list |
| `docs/architecture/FEATURE_AND_FIX_WORKFLOWS.md` | Feature/fix flow | (light) cross-ref the gate |
| `docs/specs/COMMAND_CATALOG.md` | Command catalog | Add design-continuity coverage |
| `docs/runbooks/USING_BEQUITE_COMMANDS.md` | How-to runbook | Add a frontend-continuity walkthrough |
| **MISSING** `docs/architecture/DESIGN_CONTINUITY_GATE.md` | — | **CREATE** |
| **MISSING** `docs/architecture/FRONTEND_CONTEXT_ENGINEERING.md` | — | **CREATE** |

---

## 4. Existing design MEMORY files

| Path | State |
|---|---|
| `.bequite/uiux/SECTION_MAP.md` | Exists but **thin** — template lacks route / purpose / visual role / content rules / layout constraints / acceptance criteria. **ENRICH** |
| `.bequite/uiux/LIVE_EDIT_LOG.md` | Exists, fine |
| `.bequite/uiux/UIUX_VARIANTS_REPORT.md` | Exists, fine |
| `.bequite/uiux/selected-variant.md` | Exists, fine |
| `.bequite/uiux/screenshots/` | Referenced everywhere; ensure it exists |
| `.bequite/state/MISTAKE_MEMORY.md` | Exists; has `[fe][design]` tag category but **zero frontend prevention entries**. **SEED** with the drift lessons |
| **MISSING** `.bequite/design/DESIGN_DNA.md` | **CREATE** — the source of truth for visual identity |
| **MISSING** `.bequite/design/FRONTEND_SKILL_MAP.md` | **CREATE** |
| **MISSING** `.bequite/design/DESIGN_CONTINUITY_REPORT.md` | **CREATE** (template) |
| **MISSING** `.bequite/audits/VISUAL_QA_REPORT.md` | **CREATE** (template) |
| **MISSING** `.bequite/state/FRONTEND_CONTEXT_SUMMARY.md` | **CREATE** — the compact "what's the design + what's pending" summary |

---

## 5. Missing design GATES

| Gate | Status | Plan |
|---|---|---|
| `DESIGN_CONTINUITY_PASS` (alias `DESIGN_CONTINUITY_OK`) | **MISSING** | Add to both gate ledgers; wired into 9 commands |
| `VISUAL_QA_DONE` | **MISSING** | Optional gate; set when a visual QA pass ran (browser or documented manual) |
| `DESIGN_DNA_LOCKED` | **MISSING** | Set when `DESIGN_DNA.md` exists + is approved before P2 build of any UI |

Existing gates (`AUDIT_COMPLETE`, `REVIEW_APPROVED`, `VERIFY_PASSED`) stay; the new gates compose with them.

---

## 6. Duplicated / weak / merge / keep / archive

- **Duplicated:** the 10-principles + 15-slop list (frontend-quality ∩ ux-ui-designer). → De-duplicate by designation: master skill owns canonical; both reference it.
- **Weak:** `SECTION_MAP.md` template (too thin); `MISTAKE_MEMORY.md` frontend entries (absent); `/bq-audit` frontend section ("sample 3 screens" is the literal hole the bug falls through).
- **Merge:** none deleted. The *concepts* (DNA, continuity, visual QA, product-type) merge into one new master skill.
- **Keep:** all 3 existing FE skills (detection / design / section-edit).
- **Archive:** nothing. No heavy/legacy FE skill exists to retire.

---

## 7. New master skill plan

**`.claude/skills/bequite-frontend-design-system/`** — the coordinator + canonical owner.

- `SKILL.md` — **concise** (Superpowers word-budget discipline). Owns: the design-continuity mindset, the section-by-section loop, the role split (when to call frontend-quality vs ux-ui-designer vs live-edit), effort awareness, and pointers into `references/`. Loads reference files **on demand**, not inline.
- `references/` — heavy material, loaded only when needed:
  - `impeccable-notes.md`, `ui-ux-pro-max-notes.md`, `superpowers-notes.md` (researched references)
  - `visual-qa-checklist.md`, `design-continuity-checklist.md`, `mobile-app-ui-checklist.md`, `cinematic-ui-checklist.md`
  - `product-type-rules.md` (product-category → design-rule table — kills "everything is a cinematic SaaS landing")
  - `design-dna-template.md`
- `examples/` — `design-dna-example.md`, `section-map-example.md`, `visual-qa-report-example.md`

**Role map (no overlap):**
- Master `frontend-design-system` → **orchestrates**: defines DNA, plans section map, runs the section-by-section loop, runs the Design Continuity Gate, runs visual QA, picks product-type rules.
- `frontend-quality` → **detects** AI-slop in code (canonical 15-tell list lives here; master references it).
- `ux-ui-designer` → **generates** design + tokens (canonical 10-principle list lives here; master references it).
- `live-edit` → **executes** one section edit + owns the 3-tier browser inspection.

---

## 8. Final implementation checklist (alpha.17)

- [x] This audit (`FRONTEND_SKILL_INTEGRATION_AUDIT.md`)
- [ ] `.bequite/design/DESIGN_DNA.md` + `FRONTEND_SKILL_MAP.md` + `DESIGN_CONTINUITY_REPORT.md`
- [ ] `docs/architecture/DESIGN_CONTINUITY_GATE.md` + `FRONTEND_CONTEXT_ENGINEERING.md`
- [ ] Master skill `bequite-frontend-design-system/` (SKILL.md + references/ + examples/)
- [ ] `.bequite/audits/VISUAL_QA_REPORT.md` + `.bequite/state/FRONTEND_CONTEXT_SUMMARY.md`
- [ ] Enrich `SECTION_MAP.md`; seed `MISTAKE_MEMORY.md` with drift lessons
- [ ] Add `DESIGN_CONTINUITY_PASS` / `VISUAL_QA_DONE` / `DESIGN_DNA_LOCKED` to both gate ledgers
- [ ] Wire gate into: `/bq-feature`, `/bq-fix`, `/bq-auto`, `/bq-uiux-variants`, `/bq-live-edit`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`
- [ ] Point `frontend-quality` + `ux-ui-designer` + `live-edit` at the master (de-dup by designation) + effort awareness
- [ ] Update `/bequite`, `/bq-help`, `/bq-suggest` (surface the design-continuity route)
- [ ] Update README, commands.md, CLAUDE.md, COMMAND_CATALOG, USING_BEQUITE_COMMANDS, LIVE_EDIT_STRATEGY, UIUX_VARIANTS_STRATEGY, MEMORY_FIRST_BEHAVIOR, AUTO_MODE_STRATEGY
- [ ] Bump BEQUITE_VERSION → alpha.17; update LAST_RUN, AGENT_LOG, CHANGELOG
- [ ] Adversarial verification vs. the 26 acceptance criteria

**Constraint check:** no Studio · no CLI/TUI · no dashboard · no new runtime dependency. All additions are markdown (commands / skills / memory / docs / gates). ✅
