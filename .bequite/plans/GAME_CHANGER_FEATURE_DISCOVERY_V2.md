# Game Changer Feature Discovery V2 (alpha.21)

> **A genuine discovery sprint — not a re-rank.** Game changer = the user can DO a new valuable thing. Better logs/memory/process don't qualify (they're internal reliability — see FEATURE_TYPE_TAXONOMY). Sources scanned by ecosystem: AI agent repos, Claude Code skill packs, browser-automation agents, AI UI builders, presentation/video tooling, writing systems, RAG assistants, automation marketplaces (n8n/Activepieces/Make-class), MCP servers, indie-hacker products, Product Hunt/HN/Reddit/X demand signals, Upwork/Fiverr service demand. Principles extracted; nothing copied; lightweight fit enforced.

**Run:** 2026-06-11 · Fable 5 · Confidence figures follow CONFIDENCE_CALIBRATION_STRATEGY (these are pre-inspection estimates — band 50–74 means "needs exploration before commitment").

---

## A. Already known — DO NOT count as new

**Built:** Presentation Builder · Live UI Edit · UI Variants · Make Money Finder · Job Finder · Writing DNA · Skill Audit · Design Continuity · Hooks · Context Engineering · Skill Routing · Spec writer · Explainer · Multi-model planning · Delegate Mode
**Already proposed (V1 tracker / alpha.18 reports / roadmap):** Regression Ledger · Drift Detector · Confidence Surfacing (now BUILT, alpha.21) · Ship Readiness · Secure Launch · Brand Voice (subsumed by Writing DNA) · Launch Kit · Automation Builder · Bot Builder · Agent Pack Generator · Product Movie Generator · 3D Site Builder · Data-to-Product · AI Service Business Builder · Workflow Export · Professional Expert alias (now DOCUMENTED, alpha.21)

## B. New candidates (16)

Format per candidate: **Wow** · Pain · User can now · Example · Outputs · Shape · Lightweight? · Deps · Safety/Scope risk · 💰 monetization · 🎬 demo/YouTube · Difficulty · Confidence · Stage · Verdict

### 1. Screenshot-to-Design-System — `/bq-clone-style`
**Wow:** point at any website screenshot → extracted design tokens, component inventory, DESIGN_DNA, and a clone-safe inspired rebuild plan. · Pain: "I want a site LIKE that one" takes designers days. · User can now: turn visual inspiration into a buildable system in minutes. · Outputs: DESIGN_DNA + tokens.css plan + component map + REBUILD_PLAN with originality guardrails. · Shape: command + extends frontend-design-system. · Lightweight ✅ (screenshot reading is native). · Deps: none default. · Safety: copyright — guardrails force divergence (palette shift, layout re-derivation, no asset copying). Scope risk M. · 💰 high (agency staple) · 🎬 very high · Difficulty M · **Confidence 72%** · MVP → **KEEP**

### 2. Recording-to-Assets — `/bq-recording`
**Wow:** one screen recording → step-by-step docs, tutorial article, clip markers, social captions. · Pain: documentation after building is the most-skipped chore. · Example: `/bq-recording ./demo.mp4 make docs + clips` · Outputs: TUTORIAL.md, CLIP_MARKERS.md, captions pack. · Shape: command. · Lightweight ⚠ (needs frame extraction per-project — tool-neutral pick at runtime). · Safety L; Scope M. · 💰 high · 🎬 very high (meta: record BeQuite itself) · Difficulty M-H · **Confidence 58%** · V1 → **KEEP (needs research on frame-extraction path)**

### 3. Docs-to-Support-Brain — `/bq-knowledge`
**Wow:** project docs → structured FAQ + onboarding KB + chatbot-ready knowledge pack (markdown; no runtime). · Pain: every product rebuilds support answers from scratch. · Outputs: KNOWLEDGE_PACK/ (FAQ, glossary, troubleshooting trees, intents). · Shape: command. · Lightweight ✅. · Deps none. · Risk L/L. · 💰 medium-high (KB-as-service) · 🎬 medium · Difficulty L-M · **Confidence 80%** · MVP → **KEEP**

### 4. Competitor Rebuild Blueprint — `/bq-rebuild-plan`
**Wow:** competitor URL → feature map, gap analysis, differentiation plan, clone-SAFE build plan with legal guardrails. · Pain: "build me X-but-for-Y" starts from a blank page. · Outputs: COMPETITOR_MAP + DIFFERENTIATION + BUILD_PLAN. · Shape: command (researcher + product-strategist composition). · Lightweight ✅. · Risk: legal-adjacent → guardrails forbid asset/copy lifting; M scope. · 💰 high · 🎬 high · Difficulty M · **Confidence 75%** · MVP → **KEEP**

### 5. API-to-Integration Blueprint — `/bq-integrate`
**Wow:** API docs URL → typed client plan, auth flow, error matrix, retry/idempotency strategy, working example skeleton. · Pain: integration grunt-work; undocumented edge cases. · Outputs: INTEGRATION_BLUEPRINT + skeleton. · Shape: command (backend-architect + researcher). · Lightweight ✅. · Risk L/M (anti-hallucination strict: only documented endpoints; UNVERIFIED for gaps). · 💰 high (most-posted Upwork task class) · 🎬 medium · Difficulty M · **Confidence 78%** · MVP → **KEEP**

### 6. Issues-to-Roadmap — `/bq-roadmap`
**Wow:** GitHub issues / feedback dump → themed, effort-impact-ranked Now/Next/Later roadmap. · Pain: issue triage paralysis. · Outputs: ROADMAP.md + theme clusters + quick-wins list. · Shape: command (product-strategist). · Lightweight ✅. · Risk L/L. · 💰 medium · 🎬 medium · Difficulty L · **Confidence 85%** · MVP → **KEEP**

### 7. Project-to-Course — `/bq-course`
**Wow:** a codebase → structured course (outline, lessons, exercises, slides via Presentation Builder). · Pain: developers sit on teachable projects with no time to coursify. · Outputs: COURSE_OUTLINE + per-lesson packs + deck briefs. · Shape: command (composes explainer + writing-dna + presentation-builder). · Lightweight ✅. · Risk L/M. · 💰 high (course economy) · 🎬 very high · Difficulty M · **Confidence 70%** · V1 → **KEEP**

### 8. Pain Radar — `/bq-pain-radar`
**Wow:** niche keyword → mined public complaints → ranked micro-SaaS/service opportunities with demand evidence. · Pain: "what should I build/sell?" — distinct from make-money (which finds EXISTING earning channels; this finds BUILDABLE gaps). · Outputs: PAIN_MAP + opportunity briefs + evidence links. · Shape: command (researcher + make-money + product-strategist). · Lightweight ✅. · Risk: scraping politeness (Article VIII) — L/M. · 💰 very high · 🎬 high · Difficulty M · **Confidence 68%** · V1 → **KEEP**

### 9. Localization Pack — `/bq-localize`
**Wow:** app → full i18n audit + extraction plan + translation memory + RTL-readiness (Arabic-first strength — MENA angle). · Pain: retrofit i18n is dreaded; RTL almost always broken. · Outputs: I18N_AUDIT + string catalog + RTL fix plan. · Shape: command + extends frontend-design-system (RTL checks join visual QA). · Lightweight ✅. · Risk L/M. · 💰 high in MENA market · 🎬 medium · Difficulty M · **Confidence 74%** · V1 → **KEEP**

### 10. Proof Builder — `/bq-proof`
**Wow:** finished project → client-ready case study: before/after evidence, metrics, walkthrough script, portfolio page copy. · Pain: freelancers under-sell finished work. · Outputs: CASE_STUDY + proof pack (pulls from EVIDENCE_LOG + VISUAL_QA — internal logs become SELLABLE artifacts). · Shape: command (writing-dna + design evidence). · Lightweight ✅. · Risk L/L. · 💰 high (wins next contract) · 🎬 high · Difficulty L-M · **Confidence 82%** · MVP → **KEEP**

### 11. Proposal Generator — `/bq-proposal`
**Wow:** job post → tailored proposal + scoped milestones + pricing options + risk caveats, in YOUR voice (Writing DNA). · Pain: proposal writing is the freelancing bottleneck; generic proposals lose. · Outputs: PROPOSAL.md + milestone/price table. · Shape: command (job-finder + writing-dna + product-strategist). · Lightweight ✅. · Risk L/L (honesty rule: never promise beyond confidence bands — Confidence Forecast feeds the milestone risk notes!). · 💰 very high · 🎬 high · Difficulty L · **Confidence 84%** · MVP → **KEEP**

### 12. Client Handoff Vault — `/bq-vault`
**Wow:** project → complete client-handoff bundle: runbooks, credentials CHECKLIST (never values), warranty checklist, walkthrough script, maintenance calendar. · Pain: handoffs leak knowledge and create support debt. · Outputs: VAULT/ bundle. · Shape: command (extends /bq-handoff for client-facing). · Lightweight ✅. · Risk: secrets discipline (checklist-only) — L/M. · 💰 medium-high · 🎬 medium · Difficulty L · **Confidence 80%** · V1 → **KEEP**

### 13. Client Audit Pack — `/bq-client-audit`
**Wow:** run BeQuite's audit machinery against a CLIENT repo → branded, severity-ranked, sellable audit report (the audit itself becomes a product). · Pain: freelancers can't productize "code review." · Outputs: branded CLIENT_AUDIT.pdf-ready md + fix-quote table. · Shape: command (composes audit + security + design-continuity + confidence bands per finding). · Lightweight ✅. · Risk L/M (claims must be evidence-cited — anti-hallucination mandatory). · 💰 very high (audit-as-a-service) · 🎬 high · Difficulty L-M · **Confidence 81%** · MVP → **KEEP**

### 14. Spec-to-Tests Oracle — `/bq-spec-tests`
**Wow:** spec.md → acceptance-test suite skeleton with every criterion mapped to a test ID (spec→code→test traceability, made user-facing). · Pain: specs and tests drift apart immediately. · Outputs: test skeletons + traceability matrix. · Shape: command (testing-gate + spec). · Lightweight ✅. · Risk L/L. · 💰 medium · 🎬 medium · Difficulty L-M · **Confidence 77%** · V1 → **KEEP**

### 15. Changelog-to-Announcement Kit — `/bq-announce`
**Wow:** CHANGELOG entry → release notes, tweet thread, email, in-app banner copy — all in brand voice. · Pain: shipping the announcement is the forgotten last mile. · Outputs: ANNOUNCEMENT_KIT/. · Shape: command (release-gate + writing-dna). · Lightweight ✅. · Risk L/L (publishing stays user-run — hard gate). · 💰 medium · 🎬 medium · Difficulty L · **Confidence 86%** · MVP → **KEEP**

### 16. Interview-to-Spec — `/bq-interview`
**Wow:** stakeholder conversation/transcript → spec + scope + plan draft (the vibe-coder wedge: clients talk, BeQuite specs). · Pain: requirements live in calls and die there. · Outputs: spec.md + SCOPE draft + open questions. · Shape: command (clarify + spec + product-strategist over a transcript). · Lightweight ✅. · Risk L/M (assumptions labeled; client confirms). · 💰 high · 🎬 high · Difficulty M · **Confidence 73%** · V1 → **KEEP**

---

## Sprint verdicts

**KEEP all 16** (none rejected this sprint — all pass the lightweight + new-thing-user-can-do bars). **Recommended first build (highest confidence × monetization × demo):** `/bq-proposal` (84%, very-high 💰), `/bq-announce` (86%), `/bq-client-audit` (81%), `/bq-proof` (82%) — note they form a coherent **freelancer monetization arc** with existing job-finder/make-money. **Needs research before commit:** `/bq-recording` (frame-extraction path, 58%). **Nothing graduates without user approval + the 15-step workflow.** Anti-clutter rule: several of these may ship as ARGUMENTS to existing commands or skills rather than 16 new slash commands — shape decision per FEATURE_TYPE_TAXONOMY at build time.

---

## alpha.22 status update (Consolidation Pass ruling)

| V2 candidate | alpha.22 ruling |
|---|---|
| Screenshot→design-system + competitor rebuild + flow analysis | **BUILT — merged into C3 `/bq-reference`** (clone-safe naming; specs/REFERENCE_ENGINE.md) |
| Knowledge pack / RAG | **BUILT as C4 `/bq-knowledge`** (build/ask/rag-plan/export; no vector DB default) |
| Course Engine | **BUILT as C5 `/bq-course`** (specs/COURSE_ENGINE.md) |
| Pain mining | **BUILT as C6 `/bq-pain-radar`** (public-sources-only ethics) |
| API integration blueprint | **BUILT as C7 `/bq-integrate`** |
| Proposal builder | **BUILT as C8 `/bq-proposal`** (no-overpromise rules) |
| Roadmap-from-issues / interview / spec-tests / announce / proof / vault / client-audit | **ABSORBED as arguments**: `/bq-plan from-issues` · `/bq-scope from-interview` · `/bq-test from-spec` · `/bq-release announce|proof` · `/bq-handoff client` · `/bq-audit client` |
| **`/bq-recording`** | **PARKED → V2-of-V2.** Reasons: video processing can be heavy; frame-extraction path needs research; not needed this phase. Revisit only with a researched lightweight path + real demand. |

Full shape reasoning: `.bequite/plans/APPROVED_CAPABILITY_SHAPE_DECISIONS.md`.
