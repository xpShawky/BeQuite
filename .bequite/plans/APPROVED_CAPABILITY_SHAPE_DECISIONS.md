# Approved Capability Shape Decisions (alpha.22)

Every decision below used the FEATURE_TYPE_TAXONOMY shape tree. Model: Claude Fable 5 (no switch). Independent-judgment deviations from the user's provisional directions are marked **[DISAGREE]** with reasons.

---

## 1. New standalone commands — BUILT this pass (MVP skeletons + specs)

| ID | Command | Why standalone | Memory | Spec | Conf. |
|---|---|---|---|---|---|
| C3 | `/bq-reference` | absorbs 5 reference workflows (screenshot→design-system, competitor rebuild, flow analysis, inspiration→DNA); clone-safe language enforced — never "clone-style" | `.bequite/reference/` (7 files) | REFERENCE_ENGINE.md | 85% |
| C4 | `/bq-knowledge` | 4 modes (build/ask/rag-plan/export); extractive-without-LLM vs LLM-assisted both documented; NO vector DB / RAG runtime by default | `.bequite/knowledge/` (9 files) | KNOWLEDGE_ENGINE.md | 82% |
| C5 | `/bq-course` | serious Course Engine (validation → persona → offer → curriculum → launch); course PDF = ONE reference (not accessible this session — user's 12-topic summary used as Reference A + global research); high-value questions only | `.bequite/courses/` (14 files) | COURSE_ENGINE.md | 84% |
| C6 | `/bq-pain-radar` | distinct from make-money (mines pain → buildable ideas vs finds earning tracks); hard ethics: no login scraping, no auth bypass, no ToS violation — official APIs / user exports / public only | `.bequite/pain-radar/` (8 files) | PAIN_RADAR.md | 80% |
| C7 | `/bq-integrate` | API docs → blueprint; never invents endpoints; UNVERIFIED markings mandatory | `.bequite/integrations/` (8 files) | INTEGRATION_BLUEPRINT.md | 86% |
| C8 | `/bq-proposal` | job post → tailored honest proposal (Writing DNA + confidence + no-overpromise rule: never claim skills not in memory/user-provided) | `.bequite/proposals/` (7 files) | PROPOSAL_BUILDER.md | 85% |

## 2. Arguments under existing commands — DOCUMENTED this pass

| Argument | Replaces idea | Owner |
|---|---|---|
| `/bq-plan from-issues` | /bq-roadmap | W1.4 — issues/feedback → Now/Next/Later roadmap |
| `/bq-scope from-interview` | /bq-interview | W1.3 — transcript → spec/scope/assumptions/questions |
| `/bq-test from-spec` | /bq-spec-tests | W3.1 — spec criteria → acceptance tests + traceability |
| `/bq-release announce` | /bq-announce | W4.2 — CHANGELOG → social/email/banner kit; **publishing = hard human gate** |
| `/bq-release proof` | /bq-proof | W4.2 — project → case study / evidence pack / portfolio |
| `/bq-release readiness` | ship-readiness scorecard | W4.2 — "should this ship?" scorecard (V1 #4) |
| `/bq-release demo-video` | product movie | W4.2 — script/scenes/voiceover plan (V1 #11) **[DISAGREE: release, not presentation — launch collateral family]** |
| `/bq-handoff client` | /bq-vault | W5.3 — client bundle; credential **checklist without values** |
| `/bq-audit client` | /bq-client-audit | W3.2 — client-facing severity/impact/effort/quote table |
| `/bq-verify regressions` | regression ledger | W4.1 — fixed-bug guard records re-checked (V1 #1) |
| `/bq-verify drift` | drift detector | W4.1 — docs/counts/registry vs actual files (V1 #2) |

## 3. Skills — localization-rtl (auto-attach on Arabic/MENA/RTL signals; `/bq-localize` = optional proposal only, spec LOCALIZATION_RTL.md) + guard-pass (post-work quality gates; GUARD_PASS_STRATEGY.md). **[DISAGREE: no `knowledge-builder` skill** — researcher + anti-hallucination + the command's own procedure cover it; a third artifact would be duplication.]

## 4. Parked / rejected this pass

- **`/bq-recording` — PARKED (V2)**: video processing heavy; frame-extraction path needs research; recorded in GAME_CHANGER_FEATURE_DISCOVERY_V2.md.
- No beginner/advanced hiding system (explicitly excluded).
- Option B/C numbering (see numbering strategy).

---

## Older V1 Candidate Review (the 12)

| # | Candidate | Built? | Internal-only? | User-facing? | Shape decision | Skills | Docs/memory touched | Conf. | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Regression Ledger | no | yes | no | **`/bq-verify regressions` argument** + fix/test write guard records to `.bequite/state/REGRESSION_LEDGER.md` (created on first use) | testing-gate, problem-solver | verify/fix/test cmd docs | 85% | **V1 — integrated as argument** |
| 2 | Drift Detector | no | yes | no | **`/bq-verify drift` argument** + standing check in `/bq-skill-audit`; counts/registry/docs vs actual files | skill-auditor, anti-hallucination | verify + skill-audit docs | 88% | **V1 — integrated as argument** |
| 3 | Confidence Surfacing | **YES (alpha.21)** | partly | yes | already built as Confidence Forecast; verified present in 9 commands + CONFIDENCE_RULES + TASK_CONFIDENCE — **do not rebuild**; new C3–C8 commands inherit it via contract | frontier-reasoning-coach | none new | 95% | **BUILT — verified integrated** |
| 4 | Ship-readiness Scorecard | no | no | yes | **`/bq-release readiness` argument** **[DISAGREE with `/bq-verify ship-ready` option: verify = "does it work", release = "should it ship"]**; no `/bq-ship` | release-gate, devops-cloud | release cmd doc | 84% | **V1 — argument** |
| 5 | Professional Expert alias | **YES (alpha.21)** | no | yes | composition alias `expert` = deep + strict evidence + safety scope + domain checklist; NOT a 5th mode, NOT a command | per domain | none new | 92% | **BUILT — confirmed** |
| 6 | Workflow Export | no | no | yes | future `/bq-export workflow` argument; **needs secret-scan design first** — not trivial, not safe yet | security-reviewer | roadmap only | 65% | **V2 — PARK** |
| 7 | Automation / Bot Builder | no | no | yes (strong) | future `/bq-automation` command; tool-neutral (n8n / Activepieces / Make / Zapier / cron / GH Actions / Playwright / custom worker); scope not yet clear enough to build well | scraping-automation, backend-architect | roadmap; V2 tracker | 70% | **V2 — strongest parked candidate; spec first, then build** |
| 8 | Data-to-Product Builder | no | no | yes | park; **revisit as possible `/bq-integrate` sibling or `data` mode of it** — overlap is real (both turn external interfaces into product blueprints); merge decision after C7 sees real use | database-architect, researcher | roadmap | 60% | **PARK (merge-watch with C7)** |
| 9 | AI Service Business Builder | no | no | yes | V2 orchestrator over pain-radar + make-money + proposal + release proof + course (+ future offer); building it before its parts are road-tested would stack untested layers | product-strategist | roadmap | 68% | **V2 — after C5/C6/C8 stabilize** |
| 10 | 3D / Animated Site Builder | no | no | yes | **style direction inside existing surface**: `/bq-reference style=cinematic-3d` + `/bq-uiux-variants style=3d`; reference knowledge belongs in frontend-design-system; no standalone command | frontend-design-system, ux-ui-designer | reference spec notes it | 75% | **V1 — absorbed as style argument** |
| 11 | Product Movie Generator | no | no | yes | **`/bq-release demo-video` argument** (script · scene list · demo flow · voiceover · thumbnails · launch plan) **[DISAGREE with presentation option — launch collateral belongs with announce/proof]**; no video rendering — planning artifacts only | presentation-builder, writing-dna | release cmd doc | 78% | **V1 — argument** |
| 12 | Agent Pack Generator | no | no | yes (meta) | V2 `/bq-skill-audit generate-pack` (preferred over new command) — only after Guard Pass + Skill Audit mature one more cycle | skill-auditor, guard-pass | roadmap | 62% | **V2 — roadmap/spec only** |

**Net effect of V1 review:** 2 already built (verified) · 4 absorbed into arguments this pass (#1 #2 #4 #11) · 1 absorbed as style argument (#10) · 5 parked to V2 (#6 #7 #8 #9 #12). Zero new commands from V1. The V1 tracker is updated to match.

---

## Forgotten ChatGPT Candidate Review (alpha.22 addendum, 2026-06-12)

7 candidates discussed earlier but absent from the alpha.22 candidate lists. Doc-only review (nothing built — per the rule: no implementation until alpha.22 verification completes). Anti-bloat verdict up front: **0 new commands now · 1 confirmed for alpha.23 (/bq-offer, already V3 #1) · 4 new argument workflows approved (documented, wired into router signals) · 1 merged into an existing argument · 1 V2 park.**

| # | Idea | Covered by alpha.22? | In V3? | User-facing? | Best shape + name | Integrates with | Skills | Memory/docs | $$ | YT | Difficulty | Conf. | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `/bq-demo-data` — realistic demo data (bookings, orders, products, leads, metrics) so AI-built apps don't look empty | no (V3 #18 covered only TEST fixtures) | partially (#18) | yes — demos/dashboards/portfolio feel real | **argument `/bq-feature demo-data`** + auto-suggest in frontend/dashboard/admin workflows; **absorbs V3 #18** (one data-generation capability, two profiles: `demo` + `fixtures`); promote to command only if usage proves | feature · uiux-variants · release proof/demo-video · handoff client | frontend-design-system, database-architect (shapes), testing-gate (fixtures profile) | writes into project seed files + notes in FEATURE spec; no own dir yet | med | **high** (before/after demos) | low-med | 80% | **V1 — argument; merge V3 #18 into it** |
| 2 | `/bq-persona-sim` — simulate personas (elderly, doctor, Arabic/RTL user, first-timer) using the product; report first-5 friction points | no — visual QA checks the interface; this checks whether real user types can USE it | no (V3 #8 = market personas from data; different) | yes | **argument `/bq-review persona`** + persona-walkthrough checklist added to ux-ui-designer knowledge; auto-suggested in deep-mode UI work | review · uiux-variants · live-edit · audit a11y (overlapping lens) | ux-ui-designer, frontend-quality, localization-rtl (Arabic persona) | `PERSONA_SIM_REPORT.md` in `.bequite/audits/` on first use | med | high | med | 78% | **V1 — argument** |
| 3 | `/bq-offer` — skill/service/niche → sellable offer (name, pain, deliverables, tiers, outreach, guarantee, proof) | direction approved (V3 #1) but NOT built | **yes — V3 #1** | yes — the monetization connector | **standalone command `/bq-offer` (C11) — confirmed as the alpha.23 build candidate**; also the core of the future AI Service Business Builder orchestrator (V1 #9) | pain-radar → offer → proposal → release proof · course (paid offers) · make-money | product-strategist (pricing), writing-dna, make-money | `.bequite/offers/` (OFFER, OUTREACH, PROOF_CHECKLIST…) — designed at build time | **high** | high | med | 85% | **APPROVED for alpha.23 (pending user go + 15-step workflow)** |
| 4 | `/bq-template` — finished project → reusable starter pack / Gumroad asset / agency boilerplate | no | no | yes | **argument `/bq-release template`** (launch-kit family: announce/proof/demo-video/template); needs secret-scan discipline like Workflow Export | release · handoff · demo-data (template ships with demo data) | release-gate, security-reviewer (secret scan), devops-cloud | template checklist artifacts on first use | high | med | med | 72% | **V2 — argument; build after launch-kit args see real use** |
| 5 | `/bq-demo-script` — click-by-click screen-recording walkthrough script (what to click, what to say, before/after, CTA, platform variants) | **mostly — `/bq-release demo-video` already owns script/scenes/voiceover** | no (it's a variant of absorbed V1 #11) | yes | **MERGED into `/bq-release demo-video`** as the `demo-script` profile (live-walkthrough variant vs launch-video variant — one argument, two profiles) | release demo-video · presentation (slides-based explainers stay in C1) | presentation-builder, writing-dna | extends demo-video outputs | med | **high** | low | 82% | **COVERED — merged (doc note added to bq-release demo-video)** |
| 6 | `/bq-client-intake` — project-type-aware client intake form + asset/access checklists + red flags | no | no | yes — strong freelancer value | **argument `/bq-scope intake`** (scope owns boundaries + missing info; pairs naturally with existing `from-interview` — intake BEFORE the call, from-interview AFTER) | scope → clarify → proposal · handoff client · audit client | product-strategist, job-finder safety rules (red flags) | `CLIENT_INTAKE.md` in `.bequite/plans/` on first use | med | med | low | 80% | **V1 — argument** |
| 7 | `/bq-price` — price a project/service/course/audit (low/standard/premium, terms, exclusions, negotiation script, pricing confidence) | no | partially (V3 #11 Pricing Strategist → merged into product-strategist skill) | yes | **argument `/bq-proposal price`** + the V3 #11 product-strategist skill extension (one pricing brain, surfaced where pricing is asked: proposal price · offer tiers · course offer) | proposal · offer (alpha.23) · audit client quote table · course OFFER.md | product-strategist, make-money (market rates), writing-dna (negotiation script) | extends PRICING_OPTIONS.md with confidence + negotiation script | **high** | med | low-med | 75% | **V1 — argument (no standalone command)** |

### Net rulings

- **Build now (doc-only wiring this addendum):** argument declarations + router signals for `feature demo-data` · `review persona` · `scope intake` · `proposal price`; merge note on `release demo-video` (demo-script profile).
- **alpha.23 queue:** `/bq-offer` (C11) — the single command this review confirms; everything else stays inside existing commands.
- **V3 updates:** #18 Test-Data Factory absorbed into demo-data; #1 offer verdict upgraded; template + persona-sim added as V3 addendum entries (V3 remains a 20-idea core list + addendum).
- **Anti-bloat check:** 7 ideas → 0 immediate commands. The harness principle holds.
