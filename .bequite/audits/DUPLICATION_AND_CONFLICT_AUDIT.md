# Duplication & Conflict Audit (alpha.23 tightening, 2026-06-12)

Scanned: commands/ · skills/ · .bequite/{commands,skills,state,tasks,plans}/ · docs/{specs,architecture,runbooks}/ · README · commands.md · CLAUDE.md · changelogs · installers. Method: targeted greps + cross-reference checks (counts, names, source-of-truth claims).

## Findings

| # | Finding | Files | Source of truth | Action |
|---|---|---|---|---|
| 1 | C11 status conflict created by this very pass (queued vs built) in 6 surfaces | ID map footer · ORCHESTRATION_MAP §1-5 + boundary · COMMAND_ROUTER §6 · proposal cmd+spec · README roadmap | ID map | **FIXED this pass** (all 6 flipped to built-not-live-tested) |
| 2 | Three remaining-work ledgers exist (MASTER, ROADMAP_TASKS, ALPHA_22_CHECKLIST) | `.bequite/tasks/` | MASTER (declared canonical) | ✅ already resolved by superseded-pointers; no further action — history files stay frozen |
| 3 | Two discovery trackers (V1/V2/V3) + shape decisions partly restate verdicts | `.bequite/plans/` | shape decisions for rulings; trackers for history | acceptable duplication (history vs rulings); each tracker carries status-update sections pointing forward — no merge |
| 4 | `skill/` heavy-era root dir still present (agents/doctrines/hooks from retired v2 direction) | `skill/` | ADR-004 (retired) | **conflict-risk LOW but real** (a reader may think it's active) → tightening plan P1: add a README-pointer inside `skill/` or move to docs/legacy. NOT auto-deleted (destructive; user call) |
| 5 | `bq-add-feature` alias + `bq-spec` vs `bq-scope` vs `bq-plan` near-misses | commands | ID map near-miss boundaries | ✅ documented boundaries; alias clearly marked deprecated — keep |
| 6 | Counts drift risk across 14 surfaces every release | all docs | COMMAND_ID_MAP + SKILL_REGISTRY | standing control works (drift arg caught 2 last pass; this pass synced 53 everywhere in the same commit) |
| 7 | Old USING_BEQUITE_COMMANDS walkthroughs (alpha.14-era) coexist with newer capability commands | runbook | current-state note (added in stabilization) points forward | acceptable — refresh on first live walkthrough (already in MASTER §B) |
| 8 | GEMINI.md vs AGENTS.md double-bridge in cross-agent docs | INSTALL_FOR_OTHER_AGENTS | **NEW EVIDENCE:** AGENTS.md is now the Linux Foundation standard supported by Gemini CLI itself + 60k projects | **FIXED this pass** — AGENTS.md presented as the standard single bridge; GEMINI.md demoted to optional note |
| 9 | Skills mentioned in docs vs registry vs router | 30 dirs ↔ 30 registry rows ↔ router domains | registry | ✅ no orphans either direction (verified by listing) |
| 10 | Output folders mentioned but not scaffolded | offers/ was the gap | installers | **FIXED** — `.bequite/offers/` + installer scaffold lines added |
| 11 | Parked-described-as-built / built-described-as-planned | swept | MASTER | ✅ none found post-fix #1; no false live-test claims anywhere |

## Verdict

2 real fixes applied this pass (#1, #8, plus #10 scaffold), 1 deferred to plan (#4 heavy-era `skill/` dir), rest verified clean or intentionally layered (history vs canonical). The single-source-of-truth pattern (canonical file + pointers + drift check) is holding under growth.
