# state/recovery.md

> **Resume from this file in a new session without chat history.** Updated at the end of every task; refreshed every 5 minutes during long auto-mode runs.
>
> Master pattern (master §25). The recovery prompt at `prompts/recovery_prompt.md` references this file as the primary source.

---

## Project

- **Name:** BeQuite
- **Owner:** Ahmed Shawky (xpShawky)
- **Mode:** Safe (master §4)
- **Constitution version:** 1.0.1
- **Active doctrines:** library-package, cli-tool, mena-bilingual

## Where we are

- **Build phase:** phase-0 (Repo foundation)
- **Sub-version in progress:** `v0.1.2` (master-file merge integration)
- **Last green sub-version:** `v0.1.1` (Doctrines pack — 8 default Doctrines)
- **Last successful commit:** `50ebfe6 feat(v0.1.1): doctrines pack — 8 default Doctrines for project-type rules`
- **Last successful tag:** `v0.1.1`
- **Branch:** `main` (no remote yet — local-only; Ahmed will configure remote when ready)

## What is complete

- ✅ Repo skeleton (README, LICENSE, .gitignore, CHANGELOG)
- ✅ Constitution v1.0.0 (Iron Laws — Articles I–VII)
- ✅ Doctrine schema template
- ✅ ADR template
- ✅ 6 Memory Bank templates (.tpl)
- ✅ Memory Bank rendered for BeQuite-itself (.bequite/memory/*.md, populated)
- ✅ Memory Bank scaffolds rendered for fresh projects (template/.bequite/memory/*)
- ✅ Plan + brief snapshotted to .bequite/memory/prompts/v1/
- ✅ 8 default Doctrines (default-web-saas, cli-tool, ml-pipeline, desktop-tauri, library-package, fintech-pci, healthcare-hipaa, gov-fedramp)
- ✅ Master-merge audit (docs/merge/MASTER_MD_MERGE_AUDIT.md)
- ✅ Root CLAUDE.md + AGENTS.md
- ✅ state/ files (project.yaml, current_phase.md, recovery.md — this file)
- 🟡 state/ indexes (task_index.json, decision_index.json, evidence_index.json) — being written this turn
- 🟡 prompts/ files — pending this turn
- 🟡 evidence/README.md — pending this turn
- 🟡 Constitution amendment v1.0.0 → v1.0.1 — pending this turn
- 🟡 README + CHANGELOG + activeContext + progress updates — pending this turn
- 🟡 v0.1.2 commit + tag — pending this turn

## What is incomplete

The remainder of the v0.1.2 work listed under "What is complete 🟡" above.

## What failed last

Nothing has failed. The session was interrupted twice by the user — once to introduce a new master file and refocus the merge strategy, once to confirm the merge approach. Both interruptions were on intent, not failure. v0.1.0 and v0.1.1 are clean tagged commits.

## What evidence exists

Until the receipts system ships in v0.7.0, evidence is the git history + this file.

- `git log --oneline` shows two clean commits (v0.1.0, v0.1.1).
- `git tag -l` shows two tags (v0.1.0, v0.1.1).
- `find .bequite/memory/ template/.bequite/ skill/templates/ skill/doctrines/ -type f` lists all created artefacts.

## What is the next safe task

Continue v0.1.2:
1. Write `state/task_index.json`, `state/decision_index.json`, `state/evidence_index.json`.
2. Write `prompts/master_prompt.md`, `prompts/discovery_prompt.md`, `prompts/research_prompt.md`, `prompts/stack_decision_prompt.md`, `prompts/implementation_prompt.md`, `prompts/review_prompt.md`, `prompts/recovery_prompt.md`.
3. Write `evidence/README.md`.
4. Amend Constitution to v1.0.1 (skill/templates/constitution.md.tpl + .bequite/memory/constitution.md): add Modes section, command-safety three-tier, prompt-injection rule, three-level definition-of-done, state/ files reference.
5. Update `README.md` to reflect two-layer architecture.
6. Update `CHANGELOG.md` with v0.1.1 + v0.1.2 entries.
7. Update `.bequite/memory/activeContext.md` and `.bequite/memory/progress.md`.
8. Stage all v0.1.2 files; commit with conventional-commits message; tag `v0.1.2`.
9. Move to `v0.2.0` (Skill orchestrator).

## Commands to run first (on resume)

```bash
# Orient
cat .bequite/memory/activeContext.md
cat state/current_phase.md
cat state/recovery.md

# Verify
git -C "C:/Ahmed Shawky/Antigravity projects/BeQuite" status
git -C "C:/Ahmed Shawky/Antigravity projects/BeQuite" log --oneline
git -C "C:/Ahmed Shawky/Antigravity projects/BeQuite" tag -l
```

## Files to inspect before editing

If this session is resumed by a different agent / person:

1. `.bequite/memory/constitution.md` — Iron Laws (currently v1.0.0 on disk; v1.0.1 amendment pending in this commit).
2. `docs/merge/MASTER_MD_MERGE_AUDIT.md` — the merge plan.
3. `state/project.yaml` — operational state.
4. `state/current_phase.md` — what's in flight.
5. `.bequite/memory/projectbrief.md` — what BeQuite is for.
6. `.bequite/memory/activeContext.md` — narrative of "what I'm doing right now."
7. `BEQUITE_BOOTSTRAP_BRIEF.md` — original brief (preserved as history).
8. `BeQuite_MASTER_PROJECT.md` — master file (became tracked in v0.1.2).

## Files to NOT touch

- Anything under `.bequite/memory/prompts/v1/` — versioned snapshots; immutable history.
- `BEQUITE_BOOTSTRAP_BRIEF.md` — original brief; preserve verbatim.
- Any `.env*` file (Article IV — never read, never write secrets).
- `.git/` directory.

## Suggested next phase

After v0.1.2 commits, proceed to **v0.2.0 — Skill orchestrator** per `state/current_phase.md`. The 12-persona model is now committed (master's 10 + Skeptic + FrontendDesign).

## Last heartbeat

`2026-05-10` (this update — written during v0.1.2 in flight).
