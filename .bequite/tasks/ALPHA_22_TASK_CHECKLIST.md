# Alpha.22 Task Checklist — the full prompt converted to tasks (done / remaining)

**Source:** user's alpha.22 mega-prompt (consolidation + navigation + selected game-changer planning), re-sent 2026-06-12 for A→Z verification, plus the "Forgotten ChatGPT Candidate Review" addendum.
**Shipped commit:** `5ab5c45` (pushed to xpShawky/BeQuite main) · Model: Claude Fable 5 (no switch).
**Status legend:** ✅ DONE (evidence cited) · 🔄 DONE THIS ADDENDUM · ⏳ REMAINING (with owner/when).

## Part 1 — Inspect + audit

| Task | Status | Evidence |
|---|---|---|
| Inspect repo (README, commands.md, CLAUDE.md, commands/, skills/, registries, trackers, contract, catalog, changelogs, scripts, installers, hooks) | ✅ | preflight runs logged in AGENT_LOG alpha.22 entry; counts verified 47 files pre / 53 post |
| Create COMMAND_NAVIGATION_AND_CAPABILITY_CONSOLIDATION_AUDIT.md with all 20 required points | ✅ | `.bequite/audits/COMMAND_NAVIGATION_AND_CAPABILITY_CONSOLIDATION_AUDIT.md` §1–7 |

## Part 2 — Numbering / catalog IDs

| Task | Status | Evidence |
|---|---|---|
| Evaluate Options A/B/C; no blind rename | ✅ | Option A adopted; B+C rejected with reasons — `COMMAND_NUMBERING_AND_ORDERING_STRATEGY.md` |
| COMMAND_ID_MAP.md with all required fields (ID/command/category/phase/purpose/follows/next/auto-run/hidden/shape) | ✅ | `.bequite/commands/COMMAND_ID_MAP.md` — 53 entries |

## Part 3 — Workflow Command Router

| Task | Status | Evidence |
|---|---|---|
| WORKFLOW_COMMAND_ROUTER.md + COMMAND_ROUTER.md + NEXT_COMMAND_LOG.md | ✅ | all three exist |
| Contract updated — step 12 = multi-command Next Command Recommendations | ✅ | `COMMAND_EXECUTION_CONTRACT.md` step 12 (alpha.22) |
| Auto mode reports "Internal workflow executed: <IDs>" | ✅ | `bq-auto.md` alpha.22 section |
| Update the 12 listed commands (bequite, help, suggest, auto, feature, fix, plan, implement, review, verify, release, skill-audit) | ✅ | all 12 carry alpha.22 blocks (router/IDs/args) |
| /bq-suggest = main navigation assistant (commands + skills + confidence + manual-vs-auto + gates) | ✅ | `bq-suggest.md` alpha.22 section + 4 journey routes |

## Part 4 — Capabilities + consolidation

| Task | Status | Evidence |
|---|---|---|
| /bq-reference (clone-safe, 7 outputs) · /bq-knowledge (4 modes, 9 outputs, no vector DB) · /bq-course (14 outputs) · /bq-pain-radar (ethics rules, 8 outputs) · /bq-integrate (UNVERIFIED rule, 8 outputs) · /bq-proposal (no-overpromise, 7 outputs) | ✅ | 6 command files + 7 specs in `docs/specs/`; memory dirs scaffolded in both installers |
| 8 argument consolidations (plan from-issues · scope from-interview · test from-spec · release announce/proof · handoff client · audit client) + V1-derived (verify regressions/drift · release readiness/demo-video) | ✅ | appended to the owning command files |
| Park /bq-recording, record in V2 tracker | ✅ | `GAME_CHANGER_FEATURE_DISCOVERY_V2.md` alpha.22 status section |

## Parts 5–7 — Localization, Guard Pass, Discovery V3

| Task | Status | Evidence |
|---|---|---|
| bequite-localization-rtl skill (auto-attach); /bq-localize = proposal only | ✅ | skill file + `docs/specs/LOCALIZATION_RTL.md` |
| guard-skills studied (concept only) → GUARD_PASS_STRATEGY + bequite-guard-pass + GUARD_PASS_REPORT | ✅ | WebFetch evidence in EVIDENCE_LOG; seed finding #1 = the user-caught stale INSTALL runbook |
| **GAME_CHANGER_FEATURE_DISCOVERY_V3 with 20 fresh ideas** (ranked, confidence, $$, YT, shape, overlap, keep/merge/park/reject) | ✅ | `grep -c "^| [0-9]"` → **20 rows**; verdicts: 1 future command (/bq-offer) · 13 arguments/skills · merges · parks. **Note: this WAS delivered in alpha.22 — the compaction hid it from chat; full list restated in the 2026-06-12 verification report.** |

## Parts 8–9 — Docs, router, reports

| Task | Status | Evidence |
|---|---|---|
| Update README / commands.md / bequite / help / suggest / auto / catalog / taxonomy / contract / skill-routing-strategy / router doc / CHANGELOG / AGENT_LOG / VERSION / LAST_RUN / SKILL_REGISTRY / SKILL_ROUTER / SKILL_USAGE_LOG | ✅ | all 18 updated in `5ab5c45`; registry 29 skills; router +8 domains |
| Fix INSTALL_BEQUITE_IN_PROJECT.md stale counts (user-caught) + sweep all docs | ✅ | fixed + 5 more stale spots found (menu 34 / help 37 / suggest 39/15 / commands.md 37 / CLAUDE.md header at alpha.19) — all corrected |
| Installers updated (version, scaffold, templates) + verified | ✅ | alpha.22; `bash -n` exit 0; ps1 parse 0 errors (EVIDENCE_LOG) |

## Additional requirements

| Task | Status | Evidence |
|---|---|---|
| Older V1 Candidate Review (12 candidates, full per-candidate fields) | ✅ | `APPROVED_CAPABILITY_SHAPE_DECISIONS.md` — 2 built/verified · 4→arguments · 1→style arg · 5 parked |
| Multi-command recommendation format + examples | ✅ | contract step 12 + COMMAND_ROUTER §3 + suggest journey routes |
| Independent thinking — disagreements stated | ✅ | 4 documented disagreements (demo-video owner · no knowledge-builder skill · readiness owner · /bq-offer ranking) |
| **Forgotten ChatGPT Candidate Review (7 ideas — NEW in this addendum)** | 🔄 | `APPROVED_CAPABILITY_SHAPE_DECISIONS.md` new section + V3 addendum + router/ID-map notes |
| Save this prompt as a task checklist document | 🔄 | this file |

## Remaining (open items, not blockers)

| # | Remaining task | When |
|---|---|---|
| 1 | **Live-trial** one capability command on a real task (C5 course or C3 reference recommended) — alpha.22 skeletons are untested against real input | user-initiated, anytime |
| 2 | `/bq-skill-audit` run to baseline the 2 new skills (provisionally ✓ in registry, pending first audit) | next maintenance pass |
| 3 | **alpha.23 candidate: `/bq-offer`** (V3 #1, reinforced by forgotten-candidate #3) — approved direction, NOT built; needs user go + 15-step workflow | user approval |
| 4 | Course PDF — still not provided in any session; attach it and C5 will read it directly (currently using the 12-topic summary as Reference A) | user provides file |
| 5 | Parked V2 items (recording · workflow export · automation/bot builder · data-to-product · AI service business builder · agent pack · release template) — revisit per tracker conditions | future releases |
| 6 | Calibration loop: first real Confidence Forecast entries in TASK_CONFIDENCE from live runs | accumulates with use |

**Maintainer rule:** when a remaining item completes, update this file + LAST_RUN in the same commit.
