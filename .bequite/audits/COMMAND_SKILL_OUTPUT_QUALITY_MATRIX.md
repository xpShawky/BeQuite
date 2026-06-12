# Command & Skill Output Quality Matrix (alpha.23 tightening, 2026-06-12)

Quality scale: **strong** (expert procedure + artifacts + guards) · **okay** (solid, could be richer) · **weak/thin** · **generic-risk** · **conflict-risk**. Priority: P0 fix now · P1 next maintenance · P2 someday · parked. "Live?" = live-validated (almost everything is NO — stated once here instead of repeated). All commands emit router blocks (contract step 12) and write LAST_RUN/AGENT_LOG — noted only where extra memory writes exist.

## Commands (53 active + 1 alias)

| ID | Command | Quality | Outputs | Skills | Gaps / notes | Pri |
|---|---|---|---|---|---|---|
| W0.1 | bequite | strong | menu (read-only) | orchestrator, advisor | — | — |
| W0.2 | init | strong | .bequite scaffold | — | — | — |
| W0.3 | discover | strong | DISCOVERY_REPORT | researcher, orchestrator | — | — |
| W0.4 | doctor | strong | DOCTOR_REPORT | devops | — | — |
| W0.5 | mode | okay | CURRENT_MODE | — | thin by design (selector) | — |
| W0.6/0.7 | new / existing | okay | mode + route | — | thin by design (entry shims) | — |
| W1.1 | clarify | strong | OPEN_QUESTIONS | product-strategist | — | — |
| W1.2 | research | strong | RESEARCH_REPORT + EVIDENCE_LOG | researcher | — | — |
| W1.3 | scope | strong | SCOPE (+from-interview; intake arg approved not built) | product-strategist | build intake arg on demand | P2 |
| W1.4 | plan | strong | IMPLEMENTATION_PLAN + file map + risk block | architect, specialists | — | — |
| W1.5 | spec | okay | specs/<slug>/spec.md | product-strategist | near-miss with scope documented | — |
| W1.6 | multi-plan | okay | merged plan | multi-model-planning | skill has stale-phasing backlog item | P1 |
| W2.1 | assign | strong | TASK_LIST (+delegate pack) | delegate-planner | — | — |
| W2.2 | implement | strong | code + logs + risk block | per domain | — | — |
| W2.3 | feature | strong | mini-spec→build (+demo-data/landing args approved) | 12-type router | args build on demand | P2 |
| W2.4 | fix | strong | reproduce→patch→regression record | problem-solver | — | — |
| W2.5 | uiux-variants | strong | N isolated variants + report | fds, ux, quality | gate-16 honored | — |
| W2.6 | live-edit | strong | SECTION_MAP + edits | live-edit | — | — |
| W3.1 | test | strong | tests (+from-spec/fixtures) | testing-gate | — | — |
| W3.2 | audit | strong | FULL_PROJECT_AUDIT (+client/a11y) | security, quality | — | — |
| W3.3 | review | strong | REVIEW report (+delegate/persona; Guard Pass) | security, guard-pass | — | — |
| W3.4 | red-team | strong | RED_TEAM report (10 angles) | security, anti-hall | — | — |
| W4.1 | verify | strong | VERIFY_REPORT (+regressions/drift) | release-gate, guard-pass | — | — |
| W4.2 | release | strong | release prep (+readiness/announce/proof/demo-video) | release-gate | gate-17 honored | — |
| W4.3 | changelog | strong | CHANGELOG entry | release-gate | — | — |
| W5.1 | memory | okay | snapshots | context-engineer | — | — |
| W5.2 | recover | strong | resume summary (reads CONTEXT_SUMMARY first) | context-engineer | — | — |
| W5.3 | handoff | strong | HANDOFF (+client bundle) | context-eng, security | — | — |
| N1–N3 | now / help / explain | okay | read-only | — | thin by design | — |
| N4 | suggest | strong | route + skills + confidence + gates + MASTER queries | advisor, orchestrator | — | — |
| O1–O6 | p0–p5 | okay | phase walks | orchestrator | thin wrappers by design | — |
| O7 | auto | strong | full runs + 15-step sequence reporting | orchestrator + all | the pack's keystone; live validation pending | — |
| C1 | presentation | strong | 9-file presentation memory + decks | presentation-builder | Slidev verified-current as candidate (patched) | — |
| C2 | writing-dna | strong | 5-file writing memory | writing-dna | repurpose/seo-brief args on demand | P2 |
| C3 | reference | strong | 7-file reference pack | fds, ux | — | — |
| C4 | knowledge | strong | 9-file knowledge pack | researcher, anti-hall | honest two-tier rule is the differentiator | — |
| C5 | course | **strong+** | 15-file course pack | researcher, writing, loc-rtl | only command with primary-source-verified reference | — |
| C6 | pain-radar | strong / generic-risk | 8-file pain pack | researcher, make-money | HIGH generic-risk class — guards in place, live test pending | P1 (trial) |
| C7 | integrate | strong | 8-file blueprint | backend, security | — | — |
| C8 | proposal | strong / generic-risk | 7-file proposal pack | writing-dna, strategist | same risk class | P1 (trial) |
| C9 | job-finder | okay / generic-risk | jobs memory | job-finder | older command; interview-prep/resume args on demand | P1 (trial) |
| C10 | make-money | okay / generic-risk | money memory | make-money | older command; same risk class | P1 (trial) |
| C11 | offer | strong (new) | 12-file offer pack | strategist, make-money, writing | built this pass; NOT live-tested | P1 (trial) |
| M1 | update | strong | safe self-update | updater | — | — |
| M2 | skill-audit | strong | SKILL_QUALITY_AUDIT + registry refresh | skill-auditor | — | — |
| X1 | add-feature | alias | → W2.3 | — | clearly deprecated | — |

## Skills (30)

| Skill | Quality | Overlap notes | Gaps | Verdict / Pri |
|---|---|---|---|---|
| orchestrator | strong | advisor (boundary documented) | live validation pending | stay |
| context-engineer | strong | compaction rules extend it cleanly | — | stay |
| anti-hallucination | strong | guard-pass (artifacts vs claims — documented) | — | stay |
| guard-pass | strong | see above | live validation partial (docs-guard exercised) | stay |
| frontier-reasoning-coach | strong | low-cost-model rules reference it correctly | — | stay |
| researcher | strong | — | — | stay |
| project-architect | strong | — | — | stay |
| product-strategist | strong | pricing extension (V3 #11) noted | add pricing section on first /bq-offer or proposal-price live use | stay · P2 |
| backend/database-architect | strong | pair documented | — | stay |
| security-reviewer | strong | — | refresh OWASP citations at next security run | stay · P2 |
| devops-cloud | strong | — | — | stay |
| testing-gate | strong | — | — | stay |
| release-gate | strong | — | — | stay |
| **problem-solver** | okay/**thin example** | — | backlogged: needs one worked diagnostic example | **patch · P1** |
| frontend-design-system | strong (master) | coordinates 3 FE skills — roles documented | refresh refs at next FE live use | stay |
| ux-ui-designer / frontend-quality / live-edit | strong | master-coordinated | — | stay |
| localization-rtl | strong | first real exercise done (PDF intake) | — | stay |
| scraping-automation | strong | — | catalog re-verify rule built-in | stay |
| presentation-builder | strong | — | Slidev verified-current (evidence log §4) | stay |
| writing-dna | strong | — | — | stay |
| **multi-model-planning** | okay/**stale phasing** | — | backlogged: phasing text predates current mode system | **patch · P1** |
| delegate-planner | strong | low-cost tiers extend it | — | stay |
| workflow-advisor | strong | orchestrator boundary documented | — | stay |
| skill-auditor | strong | — | — | stay |
| updater | strong | — | — | stay |
| job-finder / make-money | okay | intake overlap documented (kept separate, correct) | oldest skills; refresh on first live trial | stay · P1 (trial) |
| course-architect (not a skill) | — | — | deferred until first /bq-course live run (MASTER §E) | deferred |

## Bottom line

0 weak commands · 2 thin/stale skills (known, backlogged → P1 patches queued in tightening plan) · the dominant quality risk is **unproven-live**, not structure. No merges, no splits, no removals warranted.
