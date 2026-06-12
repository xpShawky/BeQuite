# Command/Skill Best-Practice Audit (alpha.23 tightening, 2026-06-12)

The 15 audit questions, answered per surface with evidence pointers. Research basis: `BEST_PRACTICE_EVIDENCE_LOG.md` (LIVE/PRIOR-LIVE/ECO labels). Detail matrices: `COMMAND_SKILL_OUTPUT_QUALITY_MATRIX.md`. Conflicts: `DUPLICATION_AND_CONFLICT_AUDIT.md`. Generic risk: `GENERIC_OUTPUT_RISK_AUDIT.md`.

| Question | Verdict | Evidence |
|---|---|---|
| Actually useful? | yes — every command maps to a real job (workflow phase, navigation, or monetizable capability); 0 vanity commands found; the anti-bloat record proves selectivity (40+ ideas → 7 commands across alpha.22–23, rest arguments/skills/parked) | shape decisions + V1/V2/V3 trackers |
| Too generic? | structurally guarded — artifact-based outputs with required fields (exclusions, proof gaps, confidence, citations) make essay-filler unable to pass; HIGH-risk class identified honestly | GENERIC_OUTPUT_RISK_AUDIT |
| Expert-level outputs? | designed-for-expert (procedures encode practitioner moves: reproduce-first, milestone curricula, risk-reversal, UNVERIFIED endpoints) — **proof pending live trials**, stated everywhere | matrix; MASTER §A |
| Reflects real best practices? | 8 domains reviewed: 2 LIVE-verified this pass (AGENTS.md standard; Slidev current), 2 PRIOR-LIVE (Scrapling/scraping; frontend refs alpha.17; course PDF primary source), rest ECO with verify-at-use rules | BEST_PRACTICE_EVIDENCE_LOG |
| Conflicts? | 11 checks; 3 fixed (C11 status flip ×6 surfaces, AGENTS/GEMINI double-bridge, offers scaffold), 1 deferred (`skill/` heavy-era dir), rest clean | DUPLICATION_AND_CONFLICT_AUDIT |
| Duplicated under another name? | no — near-miss boundaries documented in ORCHESTRATION_MAP (audit≠review, proposal≠offer, etc.); 1 deprecated alias clearly marked | map §1-5 |
| Missing workflow links? | no — 53/53 commands have "usually follows/next" in ID map; router journeys cover the major arcs incl. the completed monetization chain | COMMAND_ID_MAP, COMMAND_ROUTER |
| Knows next command? | yes — contract step 12 multi-recommendation block in every non-trivial command | contract |
| Selects right skills? | yes — registry+router+usage-log; 30/30 skills routed; conflict→orchestrator rule | SKILL_ROUTER |
| Updates memory correctly? | yes — writeback step 11 + capability memory dirs all scaffolded (offers/ added this pass) | installers |
| Output artifacts? | yes — every capability command has a named artifact set (7–15 files) | specs |
| Avoids fake confidence? | yes — banded forecast + evidence levels + never-100% + ≤89% cap under untested concurrency risks | CONFIDENCE_RULES, SYSTEM_DESIGN std §5 |
| Avoids overbuilding? | yes — MVP-first encoded (Reference A stage 11 + offer do-not-run-yet rule + parked ledger discipline) | OFFER_ENGINE, MASTER §E |
| Avoids AI-looking content? | guarded (slop lists for UI/decks; weasel bans; voice profiles) — live proof pending | GENERIC_OUTPUT_RISK_AUDIT |
| Written like real professional workflow? | yes — procedures read as practitioner checklists, not vibes; the 2 known thin spots (problem-solver example, multi-model phasing) are queued P1 | quality matrix |

## Domain verdicts (one line each, from the evidence log)

1 Memory/context: **good enough — no rework**; AGENTS.md standardization adopted into cross-agent docs. 2 Orchestration: **ahead of common practice**; honest weak spot = conventional enforcement (hooks/Guard Pass mitigate; watch-item). 3 Frontend: **strong** (alpha.17 research base holds). 4 Presentations/courses: **strong**; Slidev verified-current candidate; course = primary-source grounded. 5 Knowledge/RAG: **honest, not overpromising**. 6 Scraping: **first-class, current** (prior-live verified). 7 Security/system-design: **catches the named real failures** (stock races, payment mismatch, tenancy). 8 Monetization: **C11 grounded in field-tested practice** (primary-source PDF + productized-service patterns), not generic marketing.

## Overall

The pack passes its own bar structurally. The single material risk is repeated honestly across all four audits: **nothing user-facing has run live yet.** The tightening plan therefore prioritizes live trials over further speculative rule-adding.
