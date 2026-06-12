# Drift Verification — Post-Orchestration (equivalent of `/bq-verify drift`)

**Run:** 2026-06-12 · Claude Fable 5 · mechanical repo-reality checks with command evidence.

## Checks + results

| Check | Method | Result |
|---|---|---|
| Command count | `ls .claude/commands/*.md \| wc -l` → **53** (52 active + 1 deprecated alias) | ✅ matches ID map / README / commands.md / CLAUDE.md / catalog / INSTALL runbook |
| Skill count | `ls -d .claude/skills/bequite-*/ \| wc -l` → **30** | ✅ matches registry / README badge+body / CLAUDE.md / advisor / runbooks |
| Old "24 commands / 7 skills" | repo grep (excluding audits/legacy, which record history) | ✅ none |
| Old "39 / 42 commands / 18 skills" README-era counts | grep | ✅ none |
| "29 skills" stragglers | grep across public docs | ⚠ **2 found → FIXED:** `USING_BEQUITE_COMMANDS.md` current-state note (29→30) · `COMMAND_CATALOG.md` "skills 27→29" line (now notes the orchestration update → 30) |
| C11 `/bq-offer` queued marker | grep COMMAND_ID_MAP → 1 hit ("Queued for alpha.23 (approved, not built): C11") | ✅ present; no doc implies it is built |
| Live-tested claims | REMAINING ledgers + LAST_RUN + checklist all say "no live trials"; no doc claims runtime validation of C3–C8 | ✅ honest |
| Internal-prompt residue ("as the user requested", "this pass") in public docs | grep README/commands.md/install runbooks | ✅ none |
| ID map ↔ catalog ↔ commands.md ↔ README ↔ actual files | counts + family lists cross-checked | ✅ consistent |
| Registry ↔ actual skill dirs | 30 rows ↔ 30 dirs (orchestrator row added in orchestration update, verified present) | ✅ |
| Routers ↔ orchestration map | both routers carry the conflict→ORCHESTRATION_MAP rule; map §6 lists all 30 skills | ✅ |
| Version files | BEQUITE_VERSION at alpha.22 (+stabilization +orchestration update notes); changelog has all three same-release subsections; AGENT_LOG entries present | ✅ |
| Installers | version alpha.22; scaffold + templates current (router trio + 4 orchestration state cards); `bash -n` exit 0 + ps1 parse 0 errors (re-verified in orchestration update) | ✅ |

## Verdict

**2 findings, both fixed in this pass; everything else consistent.** Standing rule confirmed working: counts live canonically in COMMAND_ID_MAP + SKILL_REGISTRY; the drift check is cheap to re-run and should run inside every release verify (W4.1 `/bq-verify drift`).
