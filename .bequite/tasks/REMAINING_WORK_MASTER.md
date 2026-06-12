# REMAINING WORK MASTER — the canonical "what remains now?" ledger

**This file is the single source of truth for remaining work.** When the user asks *what remains / what's left / what's next / what's parked / what's alpha.23 / what's V2 / what's built-but-untested* — BeQuite reads THIS file and answers from it, never from memory alone. Wired into: `/bequite` · `/bq-now` · `/bq-suggest` · `/bq-recover` · `/bq-memory` · `/bq-skill-audit` · ORCHESTRATION_MAP §14. Predecessors (`REMAINING_ROADMAP_TASKS.md`, `ALPHA_22_TASK_CHECKLIST.md`) remain as history; THIS file is canonical. **Updated:** 2026-06-12 (post-alpha.22 maintenance pass).

## A. Built but NOT live-tested (alpha.22 capability commands)

All six exist as full command files + specs + scaffolded memory dirs; **none has run against real input** — that is the single biggest open item.

| Command | What exists | Untested | Suggested first live trial | Expected outputs | Risk | Conf. |
|---|---|---|---|---|---|---|
| C5 /bq-course | command + spec + **verified Reference A (PDF read 2026-06-12)** + OCR intake rules | full engine flow | a real course idea (Arabic or English) — the PDF framework makes this the readiest trial | 15 files in `.bequite/courses/` | low (markdown outputs) | 86% |
| C3 /bq-reference | command + spec + originality guardrails | extraction quality on a real screenshot/URL | one screenshot you like | 7 files in `.bequite/reference/` | low | 85% |
| C4 /bq-knowledge | command + spec (4 modes) | chunking/grounding on a real docs pile | `build` over any project's docs | 9 files in `.bequite/knowledge/` | low | 82% |
| C6 /bq-pain-radar | command + spec + ethics rules | source sweep quality | one niche keyword | 8 files in `.bequite/pain-radar/` | medium (live-web variance) | 80% |
| C7 /bq-integrate | command + spec + UNVERIFIED discipline | blueprint accuracy on real API docs | any public API docs URL | 8 files in `.bequite/integrations/` | low | 86% |
| C8 /bq-proposal | command + spec + no-overpromise rules | voice + honesty on a real job post | one real job post | 7 files in `.bequite/proposals/` | low | 85% |

## B. Maintenance

| Item | Status | Owner | Blocking? | Next action |
|---|---|---|---|---|
| Skill-audit baseline (orchestrator/guard-pass/localization-rtl) | ✅ DONE 2026-06-12 — 3/3 PASS structural (`SKILL_AUDIT_ALPHA_22_BASELINE.md`) | M2 | no | live-invocation validation rides on the §A trials |
| Drift verification | ✅ DONE 2026-06-12 — 2 findings fixed (`DRIFT_VERIFICATION_POST_ORCHESTRATION.md`) | W4.1 drift | no | re-run inside every release verify |
| Stale count sweep | ✅ clean as of 2026-06-12 (52 active+1 alias / 30 skills everywhere) | W4.1 drift | no | standing |
| Install docs verification | ✅ current | — | no | standing |
| README/public docs polish | ✅ done (stabilization rewrite + sanity re-check this pass) | — | no | revisit only on real feedback |
| 2 backlogged skill ~ items (problem-solver thin example · multi-model-planning stale phasing) | open | M2 | no | patch in a future maintenance pass |
| First Confidence-Forecast calibration entries | open — accumulates with live use | any live run | no | starts with §A trials |
| Course PDF integration | ✅ DONE 2026-06-12 — verified Reference A | C5 | no | — |

## C. Alpha.23 candidate — `/bq-offer` (C11)

**Status: QUEUED, NOT BUILT** (ID reserved in COMMAND_ID_MAP footer). **Why strongest:** the monetization connector — turns pain-radar findings + proposal capability + make-money tracks into a standing sellable offer; ranked #1 in Discovery V3 (85%) and reinforced by the forgotten-candidate review; user hinted at it twice. **Dependencies:** C6 pain-radar · C8 proposal · C10 make-money · W4.2 release proof · product-strategist (pricing) · writing-dna (voice). **Must happen first:** explicit user go → 15-step feature workflow → taxonomy shape check; preferably ≥1 live trial of C6/C8. **Future acceptance criteria:** command + spec (OFFER_ENGINE.md) + `.bequite/offers/` memory (OFFER · TARGET_CLIENT · DELIVERABLES · PRICING_TIERS · OUTREACH · DEMO_IDEA · GUARANTEE · ONBOARDING_QUESTIONS · PROOF_CHECKLIST · PROPOSAL_ANGLE) + router/ID-map/registry/docs sync + no-overpromise rules inherited from C8 + Guard Pass on outputs. **Expected outputs:** a complete productized offer pack from one sentence ("AI automation for restaurants").

## D. V1 argument candidates (approved shapes; build on first real demand — each is a doc-level addition to its owner)

| Argument | Owner | Purpose | Trigger | Priority | Conf. |
|---|---|---|---|---|---|
| feature demo-data | W2.3 | realistic demo data (demo + fixtures profiles) so apps don't look empty | first demo-day/portfolio need | high | 80% |
| review persona | W3.3 | simulated-user friction review (elderly/doctor/Arabic/first-timer) | first usability doubt | high | 78% |
| scope intake | W1.3 | project-type-aware client intake form + checklists + red flags | next client kickoff | high | 80% |
| proposal price | C8 | pricing tiers + terms + negotiation script (+product-strategist) | first "how much should I charge" | high | 75% |
| plan migration | W1.4 | framework/version upgrade blueprint | first upgrade task | med | 82% |
| job-finder interview-prep | C9 | job post + profile → questions, answers in own voice, gap plan | first interview | med | 80% |
| feature landing | W2.3 | conversion-focused landing structure + copy on Design DNA | first landing build | med | 80% |
| writing-dna repurpose | C2 | one pillar piece → multi-platform calendar | first content-engine need | med | 78% |
| writing-dna seo-brief | C2 | keyword → content brief w/ gap analysis | first SEO task | low | 75% |
| proposal sow | C8 | accepted proposal → SOW (not legal advice) | first accepted proposal | med | 70% |
| audit a11y | W3.2 | WCAG audit + remediation plan deliverable | first a11y request | med | 75% |
| explain diagram | N3 | code/architecture → mermaid diagrams | first handoff needing visuals | low | 72% |
| job-finder resume | C9 | ATS-aware honest resume tailoring | first application | low | 70% |

## E. V2 / PARKED (promotion conditions explicit; stays parked until met)

| Item | Why parked | Promotion condition | Dependencies | Conf. | Review trigger |
|---|---|---|---|---|---|
| /bq-automation (or /bq-bot) | scope not crisp; strongest parked candidate | tool-neutral spec + 1 real use-case from pain-radar | scraping-automation, backend-architect | 70% | first real automation request |
| /bq-data-product | overlap with C7 unresolved | C7 sees real use → merge-vs-standalone decision | C7, database-architect | 60% | after C7 live trial |
| AI Service Business Builder | orchestrator over untested parts | C5/C6/C8 live-proven + /bq-offer built | C5 C6 C8 C10 C11 | 68% | after alpha.23 |
| Workflow Export | secret-scan design missing (hard requirement) | secret-scan design written | security-reviewer | 65% | on demand |
| Agent Pack Generator | prefers `/bq-skill-audit generate-pack`; maturity needed | Guard Pass + skill audit one more cycle | skill-auditor, guard-pass | 62% | after next skill-audit cycle |
| Release Template | secret-scan + launch-kit args unproven | launch-kit args see real use | release-gate, security-reviewer | 72% | first resale-packaging request |
| Local Business Digitizer | template/route first | 1 real pain-radar→feature run in a local-business niche | C6, W2.3 | 75% | first MENA SMB project |
| Brand Kit Generator | C3 must mature | C3 live-proven | C3, frontend-design-system | 62% | after C3 trial |
| Community Pack | demand unproven | course adoption signal | C5 | 65% | after first real course ships |
| App Store Launch Kit | no mobile launch yet | a real mobile launch | release family | 68% | first mobile project |
| Recording-to-assets (/bq-recording) | heavy media path unresearched | researched lightweight frame-extraction + real demand | — | 55% | explicit user demand |
| Cross-agent adapters (`bq` wrapper · AGENTS.md generator · Cursor rules template) | manual setup already documented (INSTALL_FOR_OTHER_AGENTS) | real cross-agent usage demand | — | 70% | first sustained non-Claude usage |
| bequite-course-architect skill | theory-before-practice risk | 1 real /bq-course run shows which pedagogy knowledge is reusable | C5 trial | 72% | after C5 live trial |

## F. Rejected / not now

Email Sequence Engine as standalone (folded into writing-dna repurpose) · `/bq-clone-style` naming (clone language banned — C3 is reference/inspiration) · knowledge-builder skill (duplication — ruled in shape decisions §3) · Option B ordered-alias commands + Option C file renames (numbering strategy) · beginner/advanced command-hiding system (explicitly excluded) · heavy Studio / CLI / TUI / dashboard / default Docker-DB-API-frontend (ADR-001/004, standing) · small-models-equal-frontier claims (banned framing).

## G. Recently completed (needs-live-validation flags)

| Item | Shipped | Live validation needed? | Docs |
|---|---|---|---|
| Global orchestrator (skill #30) + ORCHESTRATION_MAP | `9f0a43b` | yes — rides on any live run | BEQUITE_ORCHESTRATION_MODEL.md |
| System design risk checks | `9f0a43b` | yes — first risky-domain build | SYSTEM_DESIGN_REASONING_STANDARD.md |
| Context compaction rules | `9f0a43b` | yes — first long task | CONTEXT_COMPACTION_STRATEGY.md |
| Low-cost model strategy | `9f0a43b` | yes — first delegate/local-model run | LOW_COST_MODEL_EXECUTION_STRATEGY.md |
| Cross-agent setup docs (11 agents) | `9f0a43b` | yes — first non-Claude session | INSTALL_FOR_OTHER_AGENTS.md |
| Guard Pass (skill + strategy + seed report w/ real findings) | `5ab5c45` | partially exercised (docs-guard finding live) | GUARD_PASS_STRATEGY.md |
| Localization-RTL skill | `5ab5c45` | **first real exercise DONE** (Arabic PDF intake 2026-06-12) | LOCALIZATION_RTL.md |
| Command Router + catalog IDs + Skill Router extensions | `5ab5c45` / `7f6a111` | yes — observed across future runs via NEXT_COMMAND_LOG | WORKFLOW_COMMAND_ROUTER.md |
| Course PDF integration (Reference A verified) | this pass | n/a (it WAS the validation) | COURSE_PDF_REFERENCE_NOTES.md |
| Skill-audit baseline + drift verification | this pass | n/a | the two audit files |

**Maintainer rule:** every pass that changes remaining work updates THIS file + LAST_RUN in the same commit. `/bq-verify drift` flags a stale MASTER (older than the last feature commit) as a finding.
