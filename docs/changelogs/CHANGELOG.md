# BeQuite Changelog

Format: [Keep a Changelog v1.1](https://keepachangelog.com/en/1.1.0/) · Versioning: [Semantic Versioning](https://semver.org/).

Legacy (v0.x → v2.0.0-alpha.6 heavy-direction) archived at [`docs/legacy/CHANGELOG-legacy.md`](../legacy/CHANGELOG-legacy.md) after Phase B cleanup.

## [3.0.0-alpha.22] - 2026-06-12 — Navigation & Capability Consolidation

### Addendum (2026-06-12, doc-only — same release)
- **Alpha.22 task checklist:** the full mega-prompt converted to a done/remaining task ledger at `.bequite/tasks/ALPHA_22_TASK_CHECKLIST.md` (A→Z verification: all acceptance criteria met; 6 open items listed)
- **Forgotten ChatGPT Candidate Review** (7 ideas) in `APPROVED_CAPABILITY_SHAPE_DECISIONS.md`: demo-data → `/bq-feature demo-data` argument (absorbs V3 #18; demo+fixtures profiles) · persona-sim → `/bq-review persona` argument · client-intake → `/bq-scope intake` argument · price → `/bq-proposal price` argument (+product-strategist) · demo-script → merged into `/bq-release demo-video` (demo-script profile) · template → `/bq-release template` V2 park · **`/bq-offer` confirmed as the alpha.23 build candidate (C11 queued)**. 0 new commands now — anti-bloat holds.
- V3 addendum (A1–A3 + 2 verdict changes); router addendum signals; ID map ARG notes updated

### Added
- **Catalog IDs (Option A — display-only):** every command has a stable ID (W0.1–W5.3 workflow · N navigation · O orchestrators · C capabilities · M maintenance); files never renamed. `COMMAND_NUMBERING_AND_ORDERING_STRATEGY.md` + `.bequite/commands/COMMAND_ID_MAP.md` (52 active + 1 alias mapped); Options B/C formally rejected with reasons
- **Workflow Command Router:** second routing layer — contract step 12 is now multi-command "Next Command Recommendations" (required next + 2–6 set with skills/auto-run + accelerators + do-not-run-yet); auto mode reports "Internal workflow executed: <IDs>"; `/bq-suggest` upgraded to main navigation assistant with 4 worked journey routes. `WORKFLOW_COMMAND_ROUTER.md` + `.bequite/commands/{COMMAND_ROUTER,NEXT_COMMAND_LOG}.md`
- **6 capability commands (46 → 52):** C3 `/bq-reference` (clone-safe design extraction) · C4 `/bq-knowledge` (build/ask/rag-plan/export; no vector DB default) · C5 `/bq-course` (Course Engine; user PDF framework as ONE reference) · C6 `/bq-pain-radar` (public-sources-only ethics) · C7 `/bq-integrate` (UNVERIFIED-marked blueprints) · C8 `/bq-proposal` (no-overpromise rules) — 7 specs in `docs/specs/`; memory dirs scaffolded
- **2 skills (27 → 29):** `bequite-localization-rtl` (auto-attach on Arabic/MENA/RTL) + `bequite-guard-pass` (post-work AI-failure-mode gates; guard-skills concept adapted — nothing copied/installed) + `GUARD_PASS_STRATEGY.md` + seed `GUARD_PASS_REPORT.md`
- **11 argument workflows:** `/bq-verify regressions|drift` · `/bq-release readiness|announce|proof|demo-video` · `/bq-plan from-issues|migration` · `/bq-scope from-interview` · `/bq-test from-spec|fixtures` · `/bq-handoff client` · `/bq-audit client|a11y` · `/bq-uiux-variants style=`
- **Reports:** `COMMAND_NAVIGATION_AND_CAPABILITY_CONSOLIDATION_AUDIT.md` · `APPROVED_CAPABILITY_SHAPE_DECISIONS.md` (incl. Older-V1 12-candidate review) · `GAME_CHANGER_FEATURE_DISCOVERY_V3.md` (20 fresh ranked ideas — proposals only)

### Changed
- Execution contract step 12 upgraded (alpha.20 → alpha.22); `/bequite` menu rebuilt with IDs (stale "34 commands" fixed); `/bq-help` + `/bq-suggest` counts fixed (37/39/15 stale) + ID sections; CLAUDE.md spec header alpha.19 → alpha.22 (was drifted); registry/router extended (8 new domains); taxonomy gains alpha.22 precedents; installers → alpha.22 (+7 scaffold dirs, +3 router templates; `bash -n` OK, ps1 parse 0 errors)

### Fixed
- `docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md` stale since alpha.1 ("24 commands / 7 skills") — Guard Pass seed finding #1, caught by the user

### Decided
- No file renames (Option C rejected) · no ordered aliases (Option B rejected) · `/bq-recording` PARKED to V2 · `/bq-localize` skill-first (proposal only) · no `knowledge-builder` skill (deliberate) · V1 candidates: 4 absorbed as arguments, 1 as style argument, 2 verified built, 5 parked · no beginner/advanced hiding system

---

## [Unreleased — alpha.22]

- Build approved Discovery-V2 candidates (recommended first arc: /bq-proposal · /bq-announce · /bq-client-audit · /bq-proof — the freelancer monetization arc) via the 15-step workflow
- First real confidence-calibrated task run → first CONFIDENCE_CALIBRATION_REPORT entries
- Live fire-tests (hooks · writing-dna profile · delegate cross-session with the 10-rule card) — user actions
- /bq-recording frame-extraction research (the one 50–74 band candidate)

---

## [v3.0.0-alpha.21] — 2026-06-11 — Confidence, Frontier Discipline & Discovery V2

Sharper follow-up to alpha.19/20. Three goals, all delivered. Model: **Claude Fable 5 throughout — no switch, no reroute** (per-prompt requirement honored and reported).

### Added — honest follow-up audit
- `.bequite/audits/FABLE_5_FOLLOWUP_AUDIT.md` — what alpha.19 ADDED vs only VERIFIED vs REUSED vs did NOT add; which game-changer ideas were old (most) vs new (Professional Expert alias only); internal-vs-user-facing labels for the whole surface; ruling that the V1 tracker was a ledger, not a discovery sprint.

### Added — Confidence Forecast (Part 1) · type: internal reliability with user-visible reports
- `docs/architecture/CONFIDENCE_CALIBRATION_STRATEGY.md` — bands (90–100 routine · 75–89 likely · 50–74 explore · 25–49 spike · 0–24 blocked), evidence levels (verified/inferred/assumed/unknown), the report shape, **confidence-must-move-over-time** rule (60→80→75→92→96 example, drops allowed and honest), the never-100% rule, calibration inputs, anti-patterns (flat-85% theater), forecast-vs-actual loop.
- `.bequite/state/CONFIDENCE_RULES.md` (tunable modifiers) · `.bequite/tasks/TASK_CONFIDENCE.md` (per-task trajectory template with files-to-inspect/change, unknowns, risks, tests, rollback) · `.bequite/audits/CONFIDENCE_CALIBRATION_REPORT.md` (forecast-vs-actual tracking).
- **Integrated into 9 commands** (plan/assign/auto/feature/fix/implement/review/verify/release). **No `/bq-confidence` command** — integration beats clutter, per the user's own preference ordering.
- Principle codified: *Confidence is not a feeling. It is a report based on evidence, tests, scope clarity, familiarity, dependency risk, and verification.*

### Added — Frontier Model Operating Playbook (Part 2) · type: docs + skill
- `docs/architecture/FRONTIER_MODEL_OPERATING_PLAYBOOK.md` — 16 sections of EXTERNAL operating discipline (no private chain-of-thought): complex-task approach, decomposition, context protection, anti-shallow-implementation, facts-vs-assumptions, uncertainty, evidence/decision records, no-second-source-of-truth, anti-overbuild + intent preservation, auto-mode full-scope without drift, high-risk files, UI continuity, release thinking, high-value questions, writing tasks for cheaper models, reviewing cheaper-model output, stopping drift.
- `.claude/skills/bequite-frontier-reasoning-coach/SKILL.md` — skill #27; enforces the playbook in `/bq-auto deep`, `/bq-plan deep`, `/bq-assign delegate`, `/bq-review`, `/bq-red-team`, `/bq-skill-audit`, `/bq-verify` + confidence forecasts.
- `.bequite/state/FRONTIER_REASONING_SUMMARY.md` — the 10-rule card; **embedded in every delegate task pack** so cheaper models inherit the discipline.

### Added — Game Changer Discovery V2 (Part 3) · type: roadmap
- `.bequite/plans/GAME_CHANGER_FEATURE_DISCOVERY_V2.md` — Section A quarantines 30+ already-known items so they can't be re-counted; Section B delivers **16 genuinely new type-1 candidates**, each with wow/pain/outputs/shape/lightweight-fit/deps/risks/monetization/demo-potential/difficulty/confidence%/stage/verdict. All 16 KEEP (proposals only — the 15-step workflow gates any build). Standouts: screenshot→design-system (72%), proposal generator (84%), client audit pack (81%), announce kit (86%), proof builder (82%) — the latter four form a coherent freelancer-monetization arc.

### Added — Feature Type Taxonomy (Part 4)
- `docs/architecture/FEATURE_TYPE_TAXONOMY.md` — 8 types + the mandatory shape-decision tree + honest-labeling rules ("game changer = type 1 only"; changelogs must name the type).

### Decided — Professional Expert (Part 5)
- **Ruling: composition alias is correct** — `expert` = deep + strict evidence (anti-hallucination + EVIDENCE_LOG mandatory) + safety scope (R3) + professional domain checklist. NOT a 5th mode (would bloat the conflict matrix ~25% for zero new capability). Documented in taxonomy + catalog + /bq-suggest. V1 tracker rows graduated: confidence-surfacing → BUILT · Professional Expert → DOCUMENTED.

### Changed
- Skills 26 → **27**; SKILL_REGISTRY refreshed (frontier-reasoning-coach row + counts); workflow-advisor counts synced.
- README: 3 new sections (Confidence Forecast · Frontier Model Operating Playbook · Game Changer Discovery V2) + badges.
- commands.md alpha.21 banner · /bequite menu · /bq-help (2 new sections) · /bq-suggest (confidence/rigor/expert triggers) · COMMAND_CATALOG.
- Installers → alpha.21; +3 templates (CONFIDENCE_RULES, TASK_CONFIDENCE, FRONTIER_REASONING_SUMMARY); 27-skill banner; `bash -n` clean.

### Honest notes (Article VI)
- Calibration report is seeded but EMPTY — the loop becomes meaningful only after real forecasted tasks reach verification.
- Discovery V2 candidate confidence figures are pre-inspection estimates (50–74 band = "needs exploration"), not commitments.
- Playbook effectiveness on actual cheaper models is UNVERIFIED until a live delegate run.

---

## [v3.0.0-alpha.20] — 2026-06-11 — Automatic Skill Routing

**You describe the goal; BeQuite chooses the expert procedures.** No manual skill naming, ever.

### Added
- `.bequite/skills/SKILL_REGISTRY.md` — token-cheap routing index over all 26 skills (domains, trigger keywords/intents, usual commands, compatible/conflicting, cost L/M/H, risk L/M/H, quality status, last-reviewed). Single-source-of-truth honored: detailed when-to-use/inputs/outputs stay canonical in each SKILL.md; registry holds routing metadata + pointers. Global `~/.claude/skills/` probed (empty on this machine — limitation recorded).
- `.bequite/skills/SKILL_ROUTER.md` — 24-domain → skill map + selection algorithm + 7 worked routings (cinematic site, restaurant app, human-quality writing, academic lit-review, YouTube lecture deck, auth security review, prompt-injection review) + the `Skill Selection:` output block template.
- `.bequite/skills/SKILL_USAGE_LOG.md` — selections + outcomes + routing-quality; feeds workflow-advisor learning and skill-audit orphan/over-trigger detection. Seeded with this run.
- `docs/architecture/AUTO_SKILL_ROUTING_STRATEGY.md` — 7-step routing pipeline, mode sizing (fast=smallest-safe · deep=broader · token-saver=lazy-load · delegate=skills named in task pack), cross-cutting auto-attach rules (anti-hallucination on claims · testing-gate on code · context-engineer >5 files · security-reviewer on R3 paths · frontend-design-system on >1 UI section), arbitration (master beats member), small-task 2-skill cap (over-trigger = logged routing defect).

### Changed
- **COMMAND_EXECUTION_CONTRACT: 11 → 12 steps** — skill registry check (2), task classification (3), automatic skill selection (4) inserted; writeback now includes SKILL_USAGE_LOG; enforcement-layer table + compressions updated.
- 8 action commands wired with the routing block: `/bq-auto` `/bq-feature` `/bq-fix` `/bq-plan` `/bq-implement` `/bq-review` `/bq-verify` `/bq-suggest`.
- `/bq-skill-audit` — registry refresh is now step 1 (live-dir drift check, orphan check via usage log, routing-defect scan).
- HARNESS_ENGINEERING_STRATEGY harness diagram + CONTEXT_ENGINEERING_STRATEGY core pack updated.
- README ("Automatic skill selection" principle), commands.md (alpha.20 banner), /bequite menu, /bq-help, COMMAND_CATALOG.
- Installers: `.bequite/skills/` scaffold + 3 templates; version → alpha.20. `bash -n` clean.

### Honest notes
- Routing is convention-enforced via the contract (like the rest of the harness) — Claude Code's own description-matching still operates underneath; the router makes selection deliberate, explained, and logged.
- Counts unchanged: 46 commands · 26 skills (routing is memory + contract, not a command).

---

- Build the top-ranked approved game-changers per `.bequite/plans/GAME_CHANGER_FEATURE_DISCOVERY.md`: regression ledger · drift detector · confidence surfacing · ship-readiness scorecard
- Decide Professional Expert composition-alias naming with the user (proposed in the discovery tracker — NOT a 5th mode)
- Live fire-test of the opt-in hooks across macOS/Linux/Windows; promote critical gates to default-on once validated
- Skill-audit backlog: problem-solver worked example · multi-model-planning stale-phase sweep
- First real `/bq-writing-dna` profile build + first real `/bq-presentation` render (user actions)
- Optional `/bq-deck` alias if user demand justifies

---

## [v3.0.0-alpha.19] — 2026-06-11 — Fable Strengthening Pass

**Full workflow-strengthening pass run on Claude Fable 5, Deep Mode.** Audit-first: verified alpha.17/18 already delivered hooks, context-engineering, design-continuity, and the game-changer report — this release fills the verified gaps instead of duplicating. No Studio / heavy CLI / dashboard / runtime deps.

### Added — reports
- `.bequite/audits/FABLE_5_WORKFLOW_STRENGTHENING_AUDIT.md` — current-state verification + weakness findings (context C1–C5, prompt P1–P3, harness H1–H4) + strengthening plan
- `.bequite/research/FABLE_5_SYSTEM_RESEARCH_REPORT.md` — fresh deep research (no-research-repeat applied over alpha.14/18 reports); principles adopted vs rejected

### Added — harness / context / prompt layer
- `docs/architecture/COMMAND_EXECUTION_CONTRACT.md` — **the 11-step contract every command follows** (preflight → gate → scope → skills → research-check → plan-check → action → verification → report → writeback → next)
- `docs/architecture/HARNESS_ENGINEERING_STRATEGY.md` + `CONTEXT_ENGINEERING_STRATEGY.md` — thin strategy indexes over the alpha.18 deep docs (one source of truth preserved) + alpha.19 deltas: **context-pack pattern**, **no-research-repeat rule**, generic **CONTEXT_SUMMARY**, **EVIDENCE_LOG**
- `docs/architecture/PROMPT_ENGINEERING_STANDARD.md` + `.bequite/prompts/PROMPT_PATTERNS.md` — 4 prompt classes (Complete / Compact / Neutral / Strict) with fill-in skeletons; delegate-pack neutrality rule
- `.bequite/state/CONTEXT_SUMMARY.md` (compaction-surviving snapshot, all workflows) + `.bequite/research/EVIDENCE_LOG.md` (durable verification evidence)

### Added — file-edit safety
- `docs/architecture/FILE_RISK_CLASSIFICATION.md` + `.bequite/state/FILE_RISK_RULES.md` — R3-CONFIRM / R2-ANNOUNCE / R1 tiers for env/secrets/auth/migrations/deploy/CI/payments/RLS/mass-deletes; R3 = hard human gate even in auto mode (closes the "risky change via file edit" gap — hooks only saw shell ops)
- `AUTO_MODE_STRATEGY.md` hardening: **uncertain-scope** gate (auto mode must not continue from its own assumptions into risky territory) + R3-edit gate + presentation creative-direction pause

### Added — Writing DNA (new capability)
- `/bq-writing-dna` + `bequite-writing-dna` skill + `.bequite/writing/` (WRITING_DNA, STYLE_SAMPLES, WRITING_RULES, FORBIDDEN_PATTERNS, OUTPUT_REVIEW)
- Corpus → explicit profile → constrained generation → review-against-profile; strict mode = full source fidelity; default forbidden-pattern list kills generic-AI tells
- **Ethics binding:** no fabricated citations · no academic dishonesty · no AI-detector-evasion framing
- Third DNA pillar: project / design / **writing**; `/bq-presentation` consumes it for speaker notes

### Added — Skill quality loop (new capability)
- `/bq-skill-audit` + `bequite-skill-auditor` skill — evidence-cited structural review; report-only default; seed run shipped at `.bequite/audits/SKILL_QUALITY_AUDIT.md` (26 skills: 23 PASS, 3 LOW-improve backlogged, 1 false alarm evidence-checked)

### Added — decision tracking
- `.bequite/plans/GAME_CHANGER_FEATURE_DISCOVERY.md` — keep/reject/built ledger over the alpha.18 report; 8 built · 12 kept-proposed (incl. Professional Expert as composition alias, NOT a 5th mode) · 4 rejected with reasons
- `docs/architecture/PRESENTATION_BUILDER_STRATEGY.md` — consolidates the alpha.13 design decisions (capability re-verified complete: PPTX/HTML/both/variants/strict/creative/refs/notes/brand/motion/morph + cinematic/academic/business registers)

### Changed
- Counts: **46 commands (+2) · 26 skills (+2)** — README badges, commands.md, CLAUDE.md, /bequite menu, /bq-help, /bq-suggest (writing + skill-maintenance triggers), COMMAND_CATALOG, workflow-advisor all synced
- CLAUDE.md spec → alpha.19 with execution-contract + file-risk + writing-DNA + skill-loop bullets
- Installers: version bumped (were stale at alpha.13 — drift caught), counts fixed, `.bequite/{writing,research}` scaffolded, 10 alpha.19 templates copied; **ps1 UTF-8 BOM added** (fixed a pre-existing latent parse issue — evidence: ParseFile now returns 0 errors; HEAD version had 3); sh `bash -n` clean
- `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md` → `docs/legacy/` (heavy-direction residue)

### Honest deferrals (Article VI)
- Game-changer builds (regression ledger etc.) remain proposals pending user approval
- Live verification of writing-dna / skill-audit `apply=true` / hooks fire-test = user actions
- Per-command body refresh to cite the execution contract explicitly (contract is canonical now; command bodies cite it incrementally as they're next touched)

---

## [v3.0.0-alpha.18] — 2026-06-04

### Harness, Hooks & Context-Engineering — make reliability deterministic, generalize context discipline to every workflow

Grounded in 6 cited research streams (anchored to official Anthropic docs: effective-context-engineering, effective-harnesses, reduce-hallucinations, best-practices, hooks, demystifying-evals — plus USENIX/PhantomRaven supply-chain research). Core meta-finding applied: BeQuite's rules were *advisory* (the model can skip CLAUDE.md prose) and CLAUDE.md was getting *long* (bloat → ignored rules) — so this release (a) moves the safety subset to *deterministic* opt-in hooks, and (b) pushes depth *out* of CLAUDE.md into on-demand skills.

### Added

- **Opt-in Claude Code hooks (ADR-005 implemented)** — `.claude/hooks/{pretooluse-block-destructive,pretooluse-secret-scan,stop-banned-weasel-words}.{sh,ps1}` + `.claude/settings.json.example` (+ Windows variant) + `.claude/hooks/README.md`. Machine-enforce the safety subset (destructive ops · secrets · weasel-word completion claims). **NOT active by default** — shipped as `.example` you review + merge yourself (CVE-2025-59536 / CVE-2026-21852: committed hooks are an RCE vector). Verified protocol (exit 2 blocks; `stop_hook_active` guard; fail-soft). Strategy: `docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md`.
- **`bequite-context-engineer` skill** (skills 22 → 24) — generalizes the frontend "DNA + section-map + compact-summary + continuity-gate" pattern to ALL workflows: the compact/clear/externalize primitives, compaction-survival rule, machine-state-in-JSON, path-scoped rules, session-orientation ritual, sub-agent isolation.
- **`bequite-anti-hallucination` skill** — evidence-over-claims, citation-or-strike (a finding needs a `file:line` quote or it's struck), in-session package verification (registry + age + downloads + publisher + lockfile vs slopsquatting/PhantomRaven), version-pinned API grounding, fresh-context adversarial verifier (severity-gated), and the `UNVERIFIED:` / "I don't know" forced-fork.
- **Memory:** `PROJECT_DNA.md` (the codebase's conventions/architecture contract — workflow-agnostic cousin of the Design DNA), `WORKING_NOTES.md` (per-workflow scratchpad that survives `/compact`), `FILE_RESPONSIBILITY_MAP.md` (anti-spaghetti, emitted before tasks).
- **Docs:** `CONTEXT_ENGINEERING.md` (all-workflow), `HARNESS_AND_PROMPT_QUALITY.md` (authoring standard), `GAME_CHANGER_FEATURES.md` (ranked proposal — report only).

### Changed

- **CLAUDE.md core rule 16** — one compressed "reliability discipline" rule (context · evidence · anti-spaghetti · machine-enforcement) pointing to the skills; deliberately short to avoid the bloat that gets rules ignored.
- **Commands:** `/bq-review` two-pass (spec-compliance BEFORE code-quality; fresh-context verifier; citation-or-strike); `/bq-verify` evidence (paste command + exit code + output) + Definition-of-Done gate; `/bq-discover` map-before-act + Project DNA + freshness metadata; `/bq-fix` failing-test-first + package verification; `/bq-feature` Project-DNA consistency + package verification; `/bq-plan` + `/bq-assign` File-Responsibility Map (refuse tasks without it; no-placeholder rule); `/bq-auto` confidence + uncertainty logging + 2-failed-correction reset.
- **`RESEARCH_DEPTH_STRATEGY.md`** — citation-or-strike, package verification, version-pinned API docs.
- **Installer** scaffolds the new memory templates + ships `.claude/hooks/` + the settings examples (hooks opt-in; the 2 new skills auto-propagate via the `bequite-*` glob). `/bq-doctor` reports hook presence; `bequite-updater` refreshes hook scripts but never edits your live settings.

### Deferred
- Hook *fire-testing* across all OSes (the security model requires the user to review + enable anyway).
- The game-changer features — proposed, not built, per user instruction.

---

## [v3.0.0-alpha.17] — 2026-06-04

### Frontend Design Continuity — kill "middle-section drift"

The headline frontend problem: AI-generated UIs look good at the hero, then middle sections degrade (generic cards, all-caps misuse, wide letter-spacing, text overflow, lost visual identity, "code-looking" output). Diagnosed as a context-engineering + design-continuity + visual-QA + workflow-gate problem and fixed **structurally** — lightweight, no Studio / CLI / dashboard / dependency. Researched against Impeccable (pbakaus), UI-UX-Pro-Max (nextlevelbuilder), and Superpowers (obra); principles ported, not copied.

### Added

- **Master skill `bequite-frontend-design-system`** (skills 21 → 22) — coordinates `ux-ui-designer` (design), `frontend-quality` (slop detection), `live-edit` (section edits). Owns the Design DNA, the section-by-section build loop, the Design Continuity Gate, visual QA, and product-type rules. Concise `SKILL.md` + 9 on-demand `references/` (continuity checklist, visual-QA checklist, mobile-app checklist, cinematic/3D checklist, product-type rules, DNA template, + 3 researched-reference notes) + 3 worked `examples/`.
- **Design Continuity Gate** (`docs/architecture/DESIGN_CONTINUITY_GATE.md`) — sweeps **every** section (not a 3-screen sample), comparing each to the hero and the Design DNA. New conditional gates: `DESIGN_DNA_LOCKED`, `DESIGN_CONTINUITY_PASS`, `VISUAL_QA_DONE` (apply only when a frontend exists; never bypass the 17 hard human gates).
- **Frontend context engineering** (`docs/architecture/FRONTEND_CONTEXT_ENGINEERING.md`) — persist design (DNA + section map + compact summary) instead of holding it in fading chat memory; the root cause of drift.
- **Design memory:** `.bequite/design/` (DESIGN_DNA, FRONTEND_SKILL_MAP, DESIGN_CONTINUITY_REPORT), `.bequite/audits/VISUAL_QA_REPORT.md`, `.bequite/state/FRONTEND_CONTEXT_SUMMARY.md`, `.bequite/audits/FRONTEND_SKILL_INTEGRATION_AUDIT.md`.
- **MISTAKE_MEMORY** seeded with 10 `[fe][design]` prevention rules (hero-vs-middle drift, all-caps, overflow, gray-on-color, dead buttons, mobile, nested cards, noisy motion, inconsistent type, AI gradients).
- **Product-type awareness** — `references/product-type-rules.md` (SaaS landing / dashboard / admin / mobile / restaurant / marketplace / medical / financial / dev-tool / AI / content / internal tool / automation / e-commerce / booking). Trust domains reject AI purple/pink gradients.

### Changed

- **Design Continuity Gate wired into 9 commands:** `/bq-feature`, `/bq-fix`, `/bq-auto`, `/bq-uiux-variants`, `/bq-live-edit`, `/bq-audit` (replaces "sample 3 screens" with a full section sweep), `/bq-review` (adds a continuity dimension to the review axes), `/bq-red-team` (adds the "worst-section vs hero" attack angle), `/bq-verify` (continuity + visual-QA part of the matrix when a frontend exists).
- **`/bq-auto` frontend behavior:** must not stop after a nice hero — completes all sections + visual QA before claiming done.
- **3 existing FE skills** (`frontend-quality`, `ux-ui-designer`, `live-edit`) point at the master (de-dup by designation) + gained effort awareness; `bequite-researcher` + `AUTO_MODE_STRATEGY` gained effort awareness (`${CLAUDE_EFFORT}` / Ultracode → deeper review).
- **`SECTION_MAP.md`** enriched (route / purpose / visual role / content rules / layout constraints / acceptance criteria).
- **Menus + advisor:** `/bequite`, `/bq-help`, `/bq-suggest` surface the design-continuity route.
- **Docs refreshed:** README (frontend quality promise), `commands.md`, `CLAUDE.md` (rule 15 + alpha.17 spec), `COMMAND_CATALOG`, `USING_BEQUITE_COMMANDS` (walkthrough), `MEMORY_FIRST_BEHAVIOR` (design memory), `UIUX_VARIANTS_STRATEGY`, `LIVE_EDIT_STRATEGY`, both `WORKFLOW_GATES` ledgers.
- **Installer** (`scripts/install-bequite.{ps1,sh}`) scaffolds `.bequite/design/` and copies the design templates (DESIGN_DNA, FRONTEND_SKILL_MAP, DESIGN_CONTINUITY_REPORT, FRONTEND_CONTEXT_SUMMARY, VISUAL_QA_REPORT) into target projects; the master skill auto-propagates via the existing `bequite-*` glob.

### Quality promise

Hero quality is not enough — every visible section must meet the Design DNA. No UI is complete without a Design Continuity pass + a Visual QA pass.

---

## [v3.0.0-alpha.16] — 2026-05-17

### Clean-stable-alpha release — finishes the alpha.14 audit cycle

alpha.14 wrote 7 audit reports. alpha.15 implemented the priority mechanical repairs (memory-first preflight on 16 commands + skill consistency on 19 skills + 2 new red-team angles + stale doc cleanup). alpha.16 closes the remaining items: skill description length audit, the Claude Code hooks ADR, and cross-references between architecture docs. **No new features.**

### Added

- **`docs/decisions/ADR-005-claude-code-hooks-for-machine-enforcement.md`** — proposes opt-in Claude Code hooks for machine-enforced safety: PreToolUse blocker for destructive ops, PreToolUse secret-shaped-string scan, Stop hook for banned-weasel-word detection in completion claims. Implementation deferred to alpha.17+ with full migration plan (alpha.17 prototype → alpha.18 settings integration → alpha.19 opt-in default → v3.0.0 stable cross-platform).
- **Cross-references** between architecture docs:
  - `MEMORY_FIRST_BEHAVIOR.md` → AUTO_MODE_STRATEGY (Token Saver) / RESEARCH_DEPTH_STRATEGY / MULTI_MODEL_PLANNING / WORKFLOW_GATES
  - `RESEARCH_DEPTH_STRATEGY.md` → AUTO_MODE (Deep / Fast) / MEMORY_FIRST / MULTI_MODEL_PLANNING / WORKFLOW_GATES
  - `MULTI_MODEL_PLANNING_STRATEGY.md` → AUTO_MODE (Delegate) / bequite-delegate-planner skill / RESEARCH_DEPTH / MEMORY_FIRST / WORKFLOW_GATES — repositioned as the architectural strategy doc behind Delegate Mode

### Changed

- **8 skill descriptions trimmed** for Anthropic Skills activation matching (target ~300 chars):
  - `bequite-make-money` (was ~450 → ~280)
  - `bequite-delegate-planner` (was ~370 → ~250)
  - `bequite-ux-ui-designer` (was ~325 → ~290)
  - `bequite-job-finder` (was ~330 → ~280)
  - `bequite-researcher` (was ~330 → ~270)
  - `bequite-security-reviewer` (was ~320 → ~280)
  - `bequite-devops-cloud` (was ~360 → ~270)
  - `bequite-workflow-advisor` — content refresh (39→44 commands, 15→21 skills, 3→4 operating modes; was stale from alpha.12)
- `MULTI_MODEL_PLANNING_STRATEGY.md` header — repositioned from "Phase-1 docs-only" to "Active (alpha.16); Delegate Mode is the production cross-session variant"
- `BEQUITE_VERSION.md` — bumped to alpha.16; update history extended
- `AGENT_LOG.md` — alpha.16 entry
- `LAST_RUN.md` — refreshed with alpha.16 result

### Acceptance (alpha.16)

- Skill description audit complete; all 21 ≤ ~300 chars ✅
- ADR-005 written + filed in `docs/decisions/` ✅
- Cross-references between 3 architecture docs added ✅
- workflow-advisor description content current ✅
- No new features ✅
- No Studio reintroduced ✅
- Lightweight direction preserved ✅
- alpha.16 tagged + pushed (this commit)

### Article VI honest reporting — deferred to alpha.17

- **Hooks implementation** (ADR-005 is design-only; the scripts ship in alpha.17)
- **Standardized-fields backport** to the 20 commands flagged in `COMMAND_SKILL_CONSISTENCY_AUDIT.md` — alpha.15 added the high-value sections (memory preflight / gate check / writeback) to 16 of them; remaining alpha.6 fields (Phase / When NOT to use / Quality gate / Failure behavior) are partially present per-file; explicit unified backport is alpha.17+ work that requires per-command unique content
- **AGENT_LOG sliding-window archival** — the log isn't large enough yet to warrant archival; documented as a future practice; activate when AGENT_LOG > ~5k lines
- **Live verification** by user — opening `/bq-presentation` on a real deck; running `/bq-auto deep delegate` for a real cross-session feature
- **Tool-neutrality reminder backport** to alpha.2-era skills — sampling shows all 21 skills already include the tool-neutrality language (either as a dedicated section, in "Common mistakes", or via the alpha.15-added Quality gate that references `.bequite/principles/TOOL_NEUTRALITY.md`). No explicit backport needed; verified during alpha.16 review

---

## [v3.0.0-alpha.15] — 2026-05-17

### Mechanical-repair release — audit findings implemented

alpha.14 wrote 7 audit reports identifying mechanical repairs needed. alpha.15 implements them. No new features.

### Added

- **Memory-first preflight + gate check + memory writeback** sections added to 16 commands that lacked them:
  `/bq-assign`, `/bq-audit`, `/bq-changelog`, `/bq-clarify`, `/bq-discover`, `/bq-doctor`, `/bq-handoff`, `/bq-implement`, `/bq-memory`, `/bq-recover`, `/bq-red-team`, `/bq-release`, `/bq-review`, `/bq-scope`, `/bq-test`, `/bq-verify`
  Each section instructs the agent to (1) check required gates in `.bequite/state/WORKFLOW_GATES.md` and refuse with prerequisite recommendation if unmet, (2) read core memory files (PROJECT_STATE / CURRENT_MODE / CURRENT_PHASE / LAST_RUN / MISTAKE_MEMORY) with focused reads, (3) writeback to LAST_RUN + WORKFLOW_GATES + CURRENT_PHASE + AGENT_LOG + CHANGELOG + MISTAKE_MEMORY + MODE_HISTORY as relevant.
- **`## When NOT to use this skill` + `## Quality gate` sections added** to skills lacking them:
  - Both sections added to 15 skills (backend-architect, database-architect, devops-cloud, frontend-quality, job-finder, make-money, presentation-builder, problem-solver, product-strategist, project-architect, release-gate, scraping-automation, security-reviewer, testing-gate, ux-ui-designer)
  - Only `When NOT to use` added to workflow-advisor (already had Quality gate)
  - Only `Quality gate` added to live-edit, researcher, multi-model-planning (already had When NOT to use)
- **2 new red-team attack angles** added to `/bq-red-team` (now 10 total, up from 8):
  - **Supply-chain attack** (alpha.15 #9) — PhantomRaven typo-squat, Shai-Hulud mass-publishing, dependency confusion, post-install scripts, lockfile changes touching transitive deps flagged by OSV/Snyk/Socket
  - **Prompt injection** (alpha.15 #10) — OWASP LLM Top 10 #1 — user-controlled LLM inputs, unsanitized model output rendered as HTML, indirect injection via fetched pages, prompt leakage, agent-to-agent injection chains
- **`docs/legacy/`** directory created with README explaining the archive
- **`.bequite/MEMORY_INDEX.md`** created — comprehensive index of every directory under `.bequite/` with file purposes + read-order guidance + maintainer note

### Changed

- **Stale heavy-direction docs moved to `docs/legacy/`** (per `COMMAND_CLUTTER_REVIEW.md`):
  - 9 top-level: AUTONOMOUS-MODE / DOCTRINE-AUTHORING / HOSTS / HOW-IT-WORKS / INSTALL / MAINTAINER / QUICKSTART / README / SECURITY
  - `docs/audits/` (6 files) → `docs/legacy/audits/`
  - `docs/RELEASES/` (2 files) → `docs/legacy/RELEASES/`
  - `docs/merge/` (1 file) → `docs/legacy/merge/`
  - Empty `docs/planning_runs/` moved
- **`docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md` counts refreshed** — was "24 commands / 7 skills"; now "44 active commands + 1 deprecated alias / 21 skills / 4 operating modes / orthogonal workflows". Diagram + memory tree updated.
- **`docs/runbooks/USING_BEQUITE_COMMANDS.md` extended** with 4 new walkthrough sections:
  - Operating modes (Deep / Fast / Token Saver / Delegate) — per-mode examples + composition + tracking
  - `/bq-presentation` — pattern examples + strict-vs-creative + PPTX-vs-HTML decision
  - `/bq-auto` — umbrella walkthrough showing all intents
  - Global feature-addition rule (alpha.14 reminder)
- **`bequite-workflow-advisor` SKILL.md** — internal knowledge bumped from "39 commands / 15 skills / 3 modes" to "44 + 1 deprecated / 21 / 4 composable modes". Added alpha.13 Creative + Content row to the situation routing table.
- **`/bq-red-team` description** updated to reflect 10 angles (was 8)
- **`BEQUITE_VERSION.md`** bumped to alpha.15; previous = alpha.14; update history extended

### Deferred to alpha.16 (Article VI honest reporting)

- Per-command standardized-fields template (alpha.6 schema) for the 20 commands still missing it — mechanical batch
- Skill `description:` YAML length audit (target <300 chars for Anthropic Skills activation matching)
- Backport tool-neutrality reminder blocks to alpha.2-era skills
- Live verification by user (real presentation; real delegate cross-session flow)
- ADR draft for Claude Code hooks (machine-enforcement)
- Sliding-window AGENT_LOG archival
- Cross-reference between architecture docs

### Acceptance (alpha.15)

- 16 commands have memory-first + gate-check + writeback ✅
- 18 skills have `## When NOT to use` ✅ (all 21 now have it)
- 18 skills have `## Quality gate` ✅ (all 21 now have it)
- 2 new red-team angles documented + listed in command description ✅
- Stale docs moved to legacy ✅
- `LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md` refreshed ✅
- `MEMORY_INDEX.md` created ✅
- USING_BEQUITE_COMMANDS walkthroughs added ✅
- workflow-advisor SKILL counts refreshed ✅
- No new features ✅
- No Studio reintroduced ✅
- Lightweight direction preserved ✅
- alpha.15 tagged + pushed (this commit)

---

## [v3.0.0-alpha.14] — 2026-05-17

### Added — discipline-restoration release

**Background:** alpha.13's Presentation Builder shipped without going through the full discover → research → scope → plan → tasks → verify workflow. User flagged this as unacceptable: BeQuite must follow BeQuite. alpha.14 is the corrective release.

**No new features.** This release improves alignment, not surface area.

### Added — 7 audit reports

- `.bequite/audits/FULL_SYSTEM_ALIGNMENT_AUDIT.md` — top-level repo audit + feature workflow trace + repair plan
- `.bequite/audits/COMMAND_SKILL_CONSISTENCY_AUDIT.md` — per-file consistency check across 18 command fields + 12 skill fields
- `.bequite/audits/WORKFLOW_GATE_AUDIT.md` — gate enforcement gaps + name canonicalization + mode-specific behavior + orthogonal workflows
- `.bequite/audits/FEATURE_WORKFLOW_AUDIT.md` — per-feature trace of discover → research → scope → plan → tasks → verify discipline through alpha.1–alpha.13
- `.bequite/research/BEQUITE_SYSTEM_RESEARCH_REPORT.md` — deep research on coding-agent skill packs, spec-driven development, memory systems, presentation generation, red-team workflows; principles extracted; ideas accepted vs rejected
- `.bequite/audits/COMMAND_CLUTTER_REVIEW.md` — per-command keep/merge/promote/reject decisions
- `.bequite/audits/FINAL_SYSTEM_ALIGNMENT_REPORT.md` — what was fixed in alpha.14, what's deferred to alpha.15, alpha.16 outlook

### Added — global feature-addition rule

Codified in:
- `CLAUDE.md` — core operating rules item 13 (the 15-step workflow) + item 14 (BeQuite eats its own food)
- `docs/architecture/WORKFLOW_GATES.md` — new "Feature-addition workflow (alpha.14 — global rule)" section
- `docs/specs/COMMAND_CATALOG.md` — top-of-file rule notice

Every new feature must travel through: memory entry → research → scope → plan → tasks → impl → docs (README + commands.md + `/bequite` + `/bq-help` + catalog) → log + changelog → verify → version. Exemptions for hotfixes + doc-only changes.

### Added — gate name aliasing

Both `_DONE` (COMMAND_CATALOG convention) and `_COMPLETE` (strategy doc convention) are valid spellings. Documented in `WORKFLOW_GATES.md`.

### Added — orthogonal workflow declaration

`/bq-presentation`, `/bq-job-finder`, `/bq-make-money`, `/bq-suggest`, `/bq-now`, `/bq-explain`, `/bq-help`, `/bq-update` operate **outside the 6 dev lifecycle modes**. Running them does not change phase or mode. Documented in `WORKFLOW_GATES.md`.

### Changed

- `bq-add-feature.md` — marked as DEPRECATED ALIAS for `/bq-feature`. Original spec preserved at the bottom for reference.
- `.bequite/state/OPEN_QUESTIONS.md` — Q1 (Studio deletion), Q2 (alpha.1 release), Q3 (Python CLI retirement) all closed (resolved by ADR-001 + ADR-004 long ago; never marked closed)
- `.bequite/state/PROJECT_STATE.md` — refreshed: removed stale "Python CLI + paused Studio" stack description; documented paused-on-disk assets per ADR-004
- `.bequite/state/BEQUITE_VERSION.md` — bumped to alpha.14; previous = alpha.13
- `docs/specs/COMMAND_CATALOG.md` — version + tally update + global rule
- `docs/architecture/WORKFLOW_GATES.md` — adds workflow rule + aliases + orthogonal section
- `CLAUDE.md` — rules 13 + 14 (alpha.14)
- `.bequite/logs/AGENT_LOG.md` — alpha.14 entry
- `docs/changelogs/CHANGELOG.md` — this entry

### Audit findings (per-file detail)

- **45 commands inventoried.** No placeholders. 18 lack explicit `## Files to read` (memory-first); 20 lack alpha.6 standardized-fields section. Deferred to alpha.15 — too mechanical for a single audit release.
- **21 skills inventoried.** All have valid YAML frontmatter + tool neutrality language. 18 lack explicit `## Quality gate` section; 16 lack `## When NOT to use`. Deferred to alpha.15.
- **No banned weasel words found** in completion claim contexts. The 8 mentions of "token-free" are all explicit NEGATIONS ("NOT token-free", "Token Saver — NOT token-free") — these are correct usage, not errors.
- **Studio / heavy CLI remnants** still on disk (paused per ADR-001/004) — acceptable; documented in refreshed `PROJECT_STATE.md`. No cleanup needed.
- **9 stale top-level `docs/*.md`** files + `docs/audits/*` + `docs/RELEASES/*` + `docs/merge/*` from heavy direction — not moved to `docs/legacy/` in alpha.14 (low-risk; defer to alpha.15)

### Deferred to alpha.15 (Article VI honest reporting)

- Add `## Files to read` memory-first preflight to 18 commands lacking it
- Add alpha.6 standardized fields section to 20 commands
- Add gate-refusal logic to 14 commands
- Add `## Quality gate` + `## When NOT to use` to 18 / 16 skills
- Move stale heavy-direction docs to `docs/legacy/`
- Update `LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md` counts
- USING_BEQUITE_COMMANDS.md walkthroughs (Presentation + Delegate + modes)
- Skill `description:` field length audit
- `MEMORY_INDEX.md`

These are tracked in the alpha.15 unreleased section above. Each is mechanical; none blocks alpha.14 from shipping.

### Acceptance (alpha.14)

- 7 audit reports exist ✅
- Global feature-addition rule codified in 3 docs (CLAUDE.md / WORKFLOW_GATES.md / COMMAND_CATALOG.md) ✅
- Gate name aliases documented ✅
- Orthogonal workflows declared ✅
- `bq-add-feature` deprecated alias marked ✅
- `OPEN_QUESTIONS.md` stale entries closed ✅
- `PROJECT_STATE.md` refreshed ✅
- `BEQUITE_VERSION.md` + AGENT_LOG + CHANGELOG + LAST_RUN updated ✅
- Lightweight direction preserved (no Studio / heavy CLI / dashboard added) ✅
- alpha.14 tagged + pushed ✅ (this commit)

---

## [v3.0.0-alpha.13] — 2026-05-13

### Added — Creative and Content Workflows category

- **`/bq-presentation`** — premium PPTX or HTML presentation builder. World-class output, designed to feel professional rather than generic AI.
  - Natural-language syntax (quotes optional)
  - Options: `format` (pptx / html / both / auto), `variants` (1–10), `source` (folder / pdf / word / docx / url / mixed / topic-only), `strict` / `creative`, `audience`, `style`, `duration`, `language`, `topic`, `brand`, `references`, `notes`, `motion`
  - Strict mode preserves source claims (PDF / Word / scientific source) — no unsupported facts
  - Creative mode adds structure (hooks, story arcs, examples) with assumptions marked
  - Variants 1–10: different design directions (Academic Clean / Premium Cinematic / Corporate Keynote / Medical Conference / Minimal Lecture / Dark Futuristic / Light Editorial / Data-Dashboard / Student-Friendly / Brand-Led — candidates only)
  - **Morph-like PPTX motion** — same object across sequential slides with stable IDs; duplicate slides for movement; 1–2 transformations at a time; 0.3–0.8s timing
  - **HTML motion vocabulary** — title glow, staged bullets, card focus, light sweep, smooth section transitions (every effect earns its place; no random animation)
  - Brand asset extraction (palette / typography / layout / icon style — writes `DESIGN_BRIEF.md` BEFORE any slide)
  - 14-item verification checklist
  - Operating modes composable: `deep` / `fast` / `token-saver` / `delegate`
  - Tool neutrality: python-pptx / pptxgenjs / reveal.js / Slidev / Marp / Spectacle / Impress.js / GSAP / Motion One / Playwright are CANDIDATES only — none installed by default
- **`bequite-presentation-builder`** skill — encodes the 14-step workflow, PPTX vs HTML decision rule, morph-like discipline, AI-slop reject list, variants discipline, strict-vs-creative content rules, brand-asset extraction, verification checklist
- **`.bequite/presentations/`** memory folder with 9 templates:
  - `PRESENTATION_BRIEF.md` — what / why / who / format / strict-vs-creative
  - `CONTENT_OUTLINE.md` — title / hook / story arc / slide outline / references plan
  - `SLIDE_PLAN.md` — slide-by-slide content (purpose / headline / body / visual / speaker-note pointer / source / motion ref)
  - `DESIGN_BRIEF.md` — palette / typography / grid / icon style / AI-slop reject list / brand extraction
  - `MOTION_PLAN.md` — PPTX morph-like discipline + HTML motion vocabulary + audience-fit motion baseline
  - `SPEAKER_NOTES.md` — per-slide talking points (strict-mode source-traced; creative-mode assumptions marked)
  - `REFERENCES.md` — sources, citations, attribution, anti-hallucination check
  - `PRESENTATION_VARIANTS_REPORT.md` — per-variant visual direction + pros/cons + recommendation; user picks winner
  - `EXPORT_LOG.md` — every export attempt + tool chosen + verification result
  - `assets/.gitkeep`, `outputs/.gitkeep`

### Changed

- README.md — new "Creative and Content Workflows (alpha.13)" section + version bump to alpha.13 + skill count 20 → 21 + command count 43 → 44 + skill list updated
- commands.md — new "Creative and Content Workflows (alpha.13)" section with full `/bq-presentation` spec + ToC entry + version bump
- `.claude/commands/bequite.md` — new "Creative and Content Workflows (alpha.13)" block in root menu
- `.claude/commands/bq-help.md` — added `/bq-presentation` to alpha.5+ surface list
- `.claude/commands/bq-suggest.md` — added presentation keyword triggers (slides / presentation / lecture / PowerPoint / PPTX / keynote / deck / convert PDF / Word file → slides)
- `.claude/skills/bequite-workflow-advisor/SKILL.md` — added `/bq-presentation` routing patterns + new "Creative + Content" command-table row
- `docs/specs/COMMAND_CATALOG.md` — full `/bq-presentation` entry + tallies bumped to 44 commands / 21 skills
- `CLAUDE.md` — spec bumped to alpha.13 + Creative + Content Workflows mention + presentation memory path
- `scripts/install-bequite.{ps1,sh}` — bumped to alpha.13 + scaffold `.bequite/presentations/` (+ `assets/`, `outputs/`) + copy the 9 presentation templates + updated install banner
- `BEQUITE_VERSION.md` — bumped to alpha.13

### Naming decisions

- One canonical command: `/bq-presentation`. Optional alias `/bq-deck` deferred to alpha.14 (avoid command clutter; alpha.13 is 44 commands — enough).
- Skill is `bequite-presentation-builder` (consistent with naming convention).
- Memory folder is `.bequite/presentations/` (plural, parallel to `jobs/`, `money/`, `uiux/`).

### Parser discipline (important)

- Natural language understood — quotes NOT required
- Mode words (`deep`, `fast`, `delegate`, `uiux`, `presentation`, `pptx`, `html`) treated as flags ONLY when:
  - `key=value`
  - inside brackets `[format=pptx, variants=3]`
  - immediately after the command name as known flag
  - clearly separated from the natural-language task
- If a word appears naturally inside the topic text (e.g. "explain fast learning") it stays as topic text, NOT a mode

### Acceptance (alpha.13 — all met)

- `/bq-presentation` command file exists with full spec ✅
- `bequite-presentation-builder` skill exists ✅
- README mentions presentation capability + new section ✅
- commands.md has full entry ✅
- COMMAND_CATALOG.md updated ✅
- `/bequite` root menu shows Creative + Content Workflows ✅
- `/bq-help` updated ✅
- `/bq-suggest` recommends `/bq-presentation` for slide/lecture/PowerPoint/PDF/Word keywords ✅
- `bequite-workflow-advisor` routes presentation queries ✅
- Memory folder `.bequite/presentations/` exists with 9 templates + assets/ + outputs/ ✅
- Strict vs creative documented ✅
- PPTX vs HTML decision logic documented ✅
- Variants discipline (1–10, different *directions*) documented ✅
- Morph-like PPTX motion planning documented ✅
- Source / reference handling documented ✅
- AGENT_LOG updated ✅
- CHANGELOG updated (this entry) ✅
- Installer carries the new templates ✅
- No heavy dependencies added ✅ (no python-pptx, pptxgenjs, reveal.js, Slidev, Playwright — all candidates only)

### Not done (deferred to alpha.14)

- USING_BEQUITE_COMMANDS.md walkthrough with worked presentation example
- `/bq-deck` alias (only if user demand justifies)
- Decision section example in `DECISIONS.md` for a chosen PPTX library (will run when user invokes `/bq-presentation` for real implementation)
- Live verification on a real project (user action)

---

## [v3.0.0-alpha.12] — 2026-05-12

### Added — 4 composable operating modes

- **Deep Mode** — full 11-dim research + community sources (GitHub / Reddit / HN / X / Product Hunt / niche forums / non-English) + multi-plan prompted + red-team mandatory + full audit. For new SaaS / regulated / production-bound / high-stakes work.
- **Fast Mode** — short discovery + shallow research (3 dims) + reuse memory. Still tests + verifies + logs. Not low-quality mode; just skips what isn't needed.
- **Token Saver Mode** (alias: `lean`) — read core memory first + focused files only + reuse cached research + compact reports. **Different from Fast Mode**: optimizes token cost, not speed. Naming correction: NOT "token-free".
- **Delegate Mode** (Architect Delegate pattern) — strong model architects + writes task pack at `.bequite/tasks/DELEGATE_*.md` → cheaper model implements exactly in separate session → strong model reviews at `.bequite/audits/DELEGATE_REVIEW_REPORT.md`. 40-70% cost savings on large features.

Modes compose: `deep delegate` (recommended for new features), `fast token-saver`, `deep token-saver`, `uiux variants=5 deep`, etc. Conflict resolution defaults provided.

### Added — skill + memory

- `bequite-delegate-planner` skill — full strong-model-plans-cheap-model-implements-strong-model-reviews workflow with task-pack format, hard-gate handling, mode composition, cost discipline
- 5 new memory templates: `.bequite/tasks/DELEGATE_TASKS.md`, `DELEGATE_INSTRUCTIONS.md`, `DELEGATE_ACCEPTANCE_CRITERIA.md`, `DELEGATE_TEST_PLAN.md`, `.bequite/audits/DELEGATE_REVIEW_REPORT.md`
- 1 new state file: `.bequite/state/MODE_HISTORY.md` (tracks mode usage + outcome per run; informs `/bq-suggest` and `bequite-workflow-advisor`)

### Changed

- `bequite-workflow-advisor` skill extended with mode-controller logic (decision matrix + composition table + conflict resolution + MODE_HISTORY.md learning loop)
- `/bq-auto.md` — full Mode section rewrite covering all 4 modes + composition + conflict resolution + mode tracking. Mistake-memory section now also appends to MODE_HISTORY.
- `docs/architecture/AUTO_MODE_STRATEGY.md` §11 — comprehensive new mode section
- `README.md` — top-level "Operating Modes" section near the top (major selling point). Version bumped to alpha.12. New "4 modes" badge.
- `/bequite` root menu — new "Operating modes" section
- `/bq-help` — modes table
- `commands.md` — top-level "Operating modes (alpha.12)" section with mode table + composition + conflict + delegate-specific link
- `CLAUDE.md` — version bump + 4 composable modes mention
- `docs/specs/COMMAND_CATALOG.md` — full mode decision matrix
- `BEQUITE_VERSION.md` — bumped to alpha.12

### Naming decisions

- Renamed user-suggested "Architect Delegate Mode" → **"Delegate Mode"** (short for the flag; the longer name describes the pattern in docs)
- Added `lean` as alias for `token-saver`
- No new `/bq-delegate` command — delegate is a mode flag (avoids command clutter)

### Tally after alpha.12

- Commands: 43 (unchanged — modes are flags, not new commands)
- Skills: 19 → 20 (+1: bequite-delegate-planner)
- Memory templates: +6 (5 delegate + 1 MODE_HISTORY)
- Operating modes: 0 → **4 composable**

---

## [v3.0.0-alpha.11] — 2026-05-12

### Added
- Installer scripts (PowerShell + bash) now copy alpha.10 templates into target projects on `/bq-init`:
  - jobs deep-intelligence: `HIDDEN_GEMS.md`, `COMMUNITY_SIGNALS.md`, `AI_ASSISTED_WORK.md`
  - money deep-intelligence: `HIDDEN_GEMS.md`, `COMMUNITY_SIGNALS.md`, `AI_ASSISTED_PATHS.md`
  - version + update tracking: `BEQUITE_VERSION.md`, `UPDATE_SOURCE.md`, `UPDATE_LOG.md`
- Directory scaffold extended: `.bequite/backups/`
- Final install banner now shows "Maintenance (alpha.10)" section with `/bq-update`
- CLAUDE.md template updated to surface `/bq-update`, deep intelligence flags, and memory-first principle reference

### Changed
- Installer version messaging: `v3.0.0-alpha.8` → `v3.0.0-alpha.10`
- Installer banner counts: "42 slash commands" → "43"; "18 specialist skills" → "19"

### Effect
New BeQuite installs match alpha.10 functionality immediately. `/bq-update` works from day one because BEQUITE_VERSION.md + UPDATE_SOURCE.md are present.

---

## [v3.0.0-alpha.10] — 2026-05-12

### Added

#### Maintenance command
- `/bq-update` — safely update BeQuite (commands / skills / docs / templates) from GitHub or local source. Modes: check / safe (default) / force / source=local / source=github. Backs up before changes; never overwrites project memory; surfaces conflicts as `.bequite-update.md` sibling files.
- `bequite-updater` skill — version detection / source resolution / SHA-256 diff / merge per file class / conflict handling / logging / rollback / test-after-update discipline.
- Memory files: `.bequite/state/BEQUITE_VERSION.md`, `.bequite/state/UPDATE_SOURCE.md`, `.bequite/logs/UPDATE_LOG.md`, `.bequite/backups/`

#### Deep Opportunity Intelligence
- `/bq-job-finder` + `/bq-make-money` extended with deep intelligence:
  - **Community + conversation sources:** Reddit / Indie Hackers / Hacker News / Product Hunt / X / public LinkedIn / Facebook / Discord / Slack / YouTube creator communities / app reviews
  - **Trending + short-window opportunities:** new AI task platforms, data labeling campaigns, app testing, research panels, browser panels
  - **AI-assisted work paths:** catalog of work where AI stack is a multiplier
  - **Hidden Gems** logic with full per-gem fields
- **11 new tracks:** `worldwide_hidden`, `trending_now`, `community_discovered`, `AI_assisted`, `no_calls`, `fast_first_payout`, `highest_payout`, `beginner_friendly`, `skilled_remote`, `local_country`, `non_english_platforms` — stackable
- **Multi-language search:** 13 languages + user-listed
- **Per-opportunity required fields:** confidence level added (in addition to existing trust check fields)
- 6 new memory files: `.bequite/jobs/{HIDDEN_GEMS,COMMUNITY_SIGNALS,AI_ASSISTED_WORK}.md` + `.bequite/money/{HIDDEN_GEMS,COMMUNITY_SIGNALS,AI_ASSISTED_PATHS}.md`

#### Memory-First Behavior
- `docs/architecture/MEMORY_FIRST_BEHAVIOR.md` — universal principle for all action-taking commands
- Core memory list + optional memory list + per-command read/write matrix for all 43 commands
- Token-saving memory strategy
- Auto-mode memory strategy
- Mistake memory strategy
- Standardized memory preflight + writeback templates

### Changed

- `/bequite` root menu — added "Maintenance" section with `/bq-update`
- `/bq-help` — added `/bq-update` + alpha.10 deep intelligence note
- `README.md` — version bump to alpha.10; 43-command badge; new Opportunity and Workflows + Maintenance sections in command map; deep intelligence highlighted
- `CLAUDE.md` — version bump; memory-first principle referenced; new memory paths
- `docs/specs/COMMAND_CATALOG.md` — added `/bq-update` entry; added deep intelligence flags table; tallies bumped to 43/19
- `commands.md` — added Maintenance section with full `/bq-update` entry

### Tally

- Commands: 42 → 43 (+1)
- Skills: 18 → 19 (+1)
- New memory files: +9 (6 opportunity + 3 version/update)
- New memory directory: +1 (backups/)
- Architecture docs: +1 (MEMORY_FIRST_BEHAVIOR.md)
- New tracks: +11 (deep intelligence flags)

---

## [v3.0.0-alpha.9] — 2026-05-12

### Added
- Installer scripts (PowerShell + bash) now copy alpha.8 opportunity-memory templates into target projects on `/bq-init`:
  - `.bequite/jobs/` — JOB_PROFILE, JOB_SEARCH_LOG, OPPORTUNITIES, APPLICATION_TRACKER, PITCH_TEMPLATES
  - `.bequite/money/` — MONEY_PROFILE, MONEY_SEARCH_LOG, OPPORTUNITIES, TRUST_CHECKS, ACTION_PLAN
- Directory scaffold extended: `.bequite/jobs/`, `.bequite/money/`
- Final install banner includes "Opportunity and Workflows (alpha.8)" section listing `/bq-suggest`, `/bq-job-finder`, `/bq-make-money` + the `worldwide_hidden=true` flag

### Changed
- Installer version messaging: `v3.0.0-alpha.5` → `v3.0.0-alpha.8`
- Installer banner counts: "37 slash commands" → "42"; "15 specialist skills" → "18"
- CLAUDE.md template (created on first install) now references the 3 new opportunity commands

### Effect
New BeQuite installs match alpha.8 functionality immediately — no manual file copying.

---

## [v3.0.0-alpha.8] — 2026-05-12

### Added — Opportunity and Workflows

- `/bq-suggest "<situation>"` — BeQuite workflow advisor; recommends best commands/skills/mode/gates for the goal. Read-only. Activates `bequite-workflow-advisor` skill (knows all 42 commands + 18 skills + 23 gates + 17 hard human gates).
- `/bq-job-finder` — real work opportunity finder. Intake → JOB_PROFILE.md → live research → trust check → ranked classification → pitches. Supports `worldwide_hidden=true` (multilingual hidden opportunities).
- `/bq-make-money` — earning opportunity finder. 10 tracks (highest-payout / easiest-start / fastest-first-dollar / long-term-stable / ai-assisted / no-calls / remote-global / local-only / beginner / skilled). Supports `worldwide_hidden=true` for Hidden Gems. 7-day action plan output. Repeat-search comparison.
- 3 new skills: `bequite-workflow-advisor`, `bequite-job-finder`, `bequite-make-money`
- New memory folders: `.bequite/jobs/` (5 templates: JOB_PROFILE, JOB_SEARCH_LOG, OPPORTUNITIES, APPLICATION_TRACKER, PITCH_TEMPLATES); `.bequite/money/` (5 templates: MONEY_PROFILE, MONEY_SEARCH_LOG, OPPORTUNITIES, TRUST_CHECKS, ACTION_PLAN)
- Strict safety rules across opportunity commands: no scams, fake reviews, VPN misrepresentation, upfront-fee, identity misuse, CAPTCHA farms, platform abuse, fake accounts, fake engagement, spam, unrealistic income promises

### Changed

- `/bequite` root menu — added "Opportunity and Workflows" section
- `/bq-help` — added new commands to alpha.2+ list
- `README.md` — version bump to alpha.8; 42-command badge; new commands + Worldwide Hidden Opportunity Search section in main body
- `CLAUDE.md` — version bump; new commands referenced; new memory paths in "Where things live"
- `docs/specs/COMMAND_CATALOG.md` — full entries for 3 new commands; tallies bumped
- `commands.md` — Opportunity and Workflows section with examples + Worldwide Hidden Opportunity Search explainer

### Constraints honored

- No heavy app added · no dashboard added · no big CLI added · no heavy dependencies added by default
- Commands + skills + docs + memory updates only
- No actual job APIs or browser automation runtime added — live research happens via WebFetch/WebSearch when the user invokes the command

---

## [v3.0.0-alpha.7] — 2026-05-12

### Added
- `/bq-spec "<feature>"` — Spec Kit-compatible one-page spec writer. Bridges BeQuite to the GitHub Spec Kit ecosystem. Writes `specs/<slug>/spec.md` with What / Why / Who / Acceptance / Out-of-scope / Constraints / Open questions / Success metric. Activates `bequite-product-strategist` for JTBD discipline.
- `/bq-explain "<target>"` — plain-English explainer for files / functions / decisions / concepts / BeQuite artifacts. 4-section structured output. Read-only. Use cases: onboarding, vibe-handoff prep, understanding inherited code, learning what `/bq-auto` did.

### Changed
- `bq-help.md` — added alpha.5+ alignment notice at top pointing to `commands.md`; added standardized command fields block at the end; documented updated phase names + commands added in alpha.2+
- `README.md` — version bump to alpha.7; 39-command badge; new commands added to command map + MVP roadmap
- `CLAUDE.md` — version bump; new commands referenced
- `docs/specs/COMMAND_CATALOG.md` — added `/bq-spec` + `/bq-explain` entries
- `commands.md` — added `/bq-spec` + `/bq-explain` full entries with examples + skill activation

---

## [v3.0.0-alpha.6] — 2026-05-12

### Added
- Installer scripts (both PowerShell + bash) updated to copy alpha.5 templates into target projects:
  - `.bequite/principles/TOOL_NEUTRALITY.md`
  - `.bequite/state/MISTAKE_MEMORY.md`, `ASSUMPTIONS.md`
  - `.bequite/uiux/SECTION_MAP.md`, `LIVE_EDIT_LOG.md`, `UIUX_VARIANTS_REPORT.md`, `selected-variant.md`
  - `.bequite/uiux/screenshots/`, `.bequite/uiux/archive/`
  - `commands.md` at project root
- 19 alpha.1 commands extended with "Standardized command fields (alpha.6)" section: bq-init, bq-discover, bq-doctor, bq-clarify, bq-scope, bq-assign, bq-implement, bq-test, bq-audit, bq-review, bq-red-team, bq-verify, bq-release, bq-changelog, bq-memory, bq-recover, bq-handoff, bequite (root), bq-add-feature
- Each gained: Phase / When NOT to use / Preconditions / Required previous gates / Quality gate (success criteria) / Failure behavior / Memory updates / Log updates

### Changed
- Installer CLAUDE.md template (created or appended) now references `/bq-now`, `/bq-auto`, `commands.md`, TOOL_NEUTRALITY.md, gates
- Installer end-of-install message highlights autonomous mode + new commands

---

## [v3.0.0-alpha.5] — 2026-05-12

### Added
- `/bq-now` — one-line orientation command (faster than `/bequite`)
- `commands.md` at repo root — full human-readable command reference, workflow-ordered, linked from README
- `--mode fast | deep | token-saver` flag on `/bq-auto` (depth adjustment; does NOT skip safety gates)
- Mistake-memory writes wired into 7 commands (`/bq-fix`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`, `/bq-auto`, `/bq-live-edit`)

### Removed
- `studio/` directory (full Next.js app: marketing + api + dashboard + brand)
- `docker-compose.yml` (Studio Docker orchestration)
- `scripts/docker-up.ps1`, `scripts/docker-up.sh` (Studio dev runners)
- Git history retains all of the above (ADR-004)

### Changed
- README: badge updated to 37 commands; `commands.md` link surfaced near the top; alpha.5 roadmap consolidated
- CLAUDE.md: version bump; new file paths; mistake-memory + `/bq-now` + `commands.md` referenced
- COMMAND_CATALOG.md: `/bq-now` entry added; tallies bumped; pointed at `commands.md`

### Kept (per user "remove only studio") — explicitly NOT removed
- `cli/`, `tests/`, `template/`, `evidence/`, `examples/`, `prompts/`, `state/`, `skill/`
- `.dockerignore`, `.env.example`, `Makefile`, `package.json`, `.commitlintrc.json`
- `scripts/bootstrap.{ps1,sh}`, `scripts/install.{ps1,sh}`
- `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md`, `docs/runbooks/LOCAL_DEV.md`
- `BeQuite_MASTER_PROJECT.md`, root `CHANGELOG.md`

---

## [v3.0.0-alpha.4] — 2026-05-12

### Added — workflow upgrades
- **Scoped `/bq-auto`** — parses `$ARGUMENTS` for 17 intent types (`new | existing | feature | fix | uiux | frontend | backend | database | security | testing | devops | scraping | automation | deploy | live-edit | variants | release`). Continues by default; pauses only at 17 hard human gates.
- **UI/UX variants** — `/bq-uiux-variants [N]` generates 1-10 isolated design directions. Each lives in `/uiux/v1` route or `src/uiux-variants/Variant01/` component. Original UI untouched. User picks winner; agent merges.
- **Live edit workflow** — `/bq-live-edit` lightweight section-by-section frontend edits. Maps visible sections to source files (SECTION_MAP.md). Three-tier browser inspection (Playwright MCP → project-local Playwright → code-only).
- New skill: `bequite-live-edit`
- New strategy docs: AUTO_MODE_STRATEGY, UIUX_VARIANTS_STRATEGY, LIVE_EDIT_STRATEGY
- New memory tree: `.bequite/uiux/` (SECTION_MAP, LIVE_EDIT_LOG, UIUX_VARIANTS_REPORT, selected-variant, screenshots/, archive/)

### Changed (alpha.4)
- `/bq-auto` fully rewritten — 17 intents + 17 hard human gates (replaced alpha.2's 12)
- CLAUDE.md updated to v3.0.0-alpha.4 spec; 36 commands, 15 skills
- COMMAND_CATALOG.md added bq-uiux-variants, bq-live-edit; expanded bq-auto entry
- USING_BEQUITE_COMMANDS.md added v3.0.0-alpha.4 examples section
- 5 existing skills extended with activation lists

### Tally
- Commands: 34 → 36 (+2)
- Skills: 14 → 15 (+1)
- Auto intents: 0 → 17
- Hard human gates in /bq-auto: 12 → 17
- Architecture docs: 1 → 4

---

## [v3.0.0-alpha.3] — 2026-05-11

### Added — tool neutrality
- `.bequite/principles/TOOL_NEUTRALITY.md` — canonical source of truth
- `docs/decisions/ADR-003-tool-neutrality.md` — formalizes the decision
- **10 decision questions** every major tool pick must answer
- **Decision section format** required before tool adoption
- **Do-not-auto-install defaults** — no deps / frontend libs / Docker / testing frameworks / monitoring / auth libs added by default
- **Research-depth rule** — 11 dimensions; tool choice AFTER project understanding

### Changed (alpha.3)
- CLAUDE.md — tool neutrality is now Core Operating Rule #1
- All 11 tool-touching skills updated with Tool Neutrality block
- All 8 tool-touching commands updated with Tool Neutrality block
- Standardized phrasing: "X is one candidate. Research and compare against other options. Use it only if it fits this project."

---

## [v3.0.0-alpha.2] — 2026-05-11

### Added — mandatory workflow gates + scoped modes + specialist skills
- **23 workflow gates** at `.bequite/state/WORKFLOW_GATES.md`
- **6 explicit modes** — New Project, Existing Audit, Add Feature, Fix Problem, Research Only, Release Readiness
- **10 new commands** — `/bq-mode`, `/bq-new`, `/bq-existing`, `/bq-feature` (12-type router), `/bq-auto`, `/bq-p0` through `/bq-p5`
- **Phase orchestrators** — `/bq-p0` … `/bq-p5` walk one phase end-to-end
- **Autonomous runner** — `/bq-auto` walks all phases with 12 hard human gates
- **7 new specialist skills** — researcher (11 dims), product-strategist, ux-ui-designer, backend-architect, database-architect, security-reviewer, devops-cloud
- **Add Feature 12-type router** + **Fix 15-type router**
- ADR-002 — mandatory workflow gates
- COMMAND_CATALOG.md — single source of truth

### Changed (alpha.2)
- `/bequite` root menu now gate-aware
- `/bq-research` expanded from 1 dim → 11 dims
- `/bq-plan` activates multi-skill thinking (15 sections including §11 security and §12 devops)
- `/bq-multi-plan` enforces unbiased external prompts (zero mention of Claude's plan)
- `/bq-fix` reproduce-first procedure with 15-type classification
- CLAUDE.md reflects 34 commands, 14 skills, modes, gates

---

## [v3.0.0-alpha.1] — 2026-05-11

### Added — lightweight skill pack MVP
- 24 slash commands at `.claude/commands/`
- 7 focused skills at `.claude/skills/`
- `.bequite/` memory tree (state, logs, plans, tasks, prompts, audits)
- Lightweight installer scripts (`scripts/install-bequite.{ps1,sh}`)
- ADR-001 — lightweight-skill-pack-first decision
- README rewritten to lead with skill-pack install
- CLAUDE.md shortened to point at `.claude/` + `.bequite/`

### Paused (kept on disk; not deleted in alpha.1)
- `studio/` (marketing + dashboard + api + brand)
- `docker-compose.yml`, `.dockerignore`, Dockerfiles
- `tests/e2e/`
- `scripts/docker-up.{ps1,sh}`
- Root `package.json` + `Makefile`
- `cli/` (Python CLI)

(Per DIRECTION_RESET_AUDIT.md — deletion gated on explicit user approval; delivered in alpha.5 cleanup phase B.)

---

## Pre-reset history (v0.1.0 → v2.0.0-alpha.6)

Heavy-direction lineage: Studio + Docker + heavy CLI. Archived at `docs/legacy/CHANGELOG-legacy.md` (after Phase B cleanup completes).
