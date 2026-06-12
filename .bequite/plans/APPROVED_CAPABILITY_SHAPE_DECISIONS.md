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
