# state/current_phase.md

> Current build phase for BeQuite-itself. **Updated at the end of every sub-version.** Re-read on every session start.

---

## Build phase

- **Phase:** `phase-0` — Repo foundation
- **Sub-version:** `v0.1.2` (in progress this commit)
- **Last green sub-version:** `v0.1.1` (committed + tagged 2026-05-10)
- **Mode:** Safe Mode (master §4)
- **Active doctrines:** `library-package`, `cli-tool`, `mena-bilingual`
- **Constitution version:** `v1.0.1` (bumped from `v1.0.0` in this sub-version)

## What this sub-version is doing

`v0.1.2` is the master-file merge integration sub-version, triggered by the introduction of `BeQuite_MASTER_PROJECT.md` (2858 lines) mid-session, after `v0.1.1` was already committed and tagged. The merge plan lives at `docs/merge/MASTER_MD_MERGE_AUDIT.md`.

In flight in this commit:

- ✅ Two pending Doctrines completed (healthcare-hipaa, gov-fedramp) — closes `v0.1.1` work that was interrupted.
- ✅ `v0.1.1` committed + tagged.
- 🟡 `docs/merge/MASTER_MD_MERGE_AUDIT.md` — written.
- 🟡 Root `CLAUDE.md` + `AGENTS.md` — written.
- 🟡 `state/` files (project.yaml, current_phase.md, recovery.md, task_index.json, decision_index.json, evidence_index.json) — being written now.
- 🟠 `prompts/` (master, discovery, research, stack_decision, implementation, review, recovery) — pending.
- 🟠 `evidence/README.md` — pending.
- 🟠 Constitution amendment v1.0.0 → v1.0.1 (modes, command-safety, prompt-injection, def-of-done, state/ refs) — pending.
- 🟠 `README.md`, `CHANGELOG.md`, `.bequite/memory/activeContext.md`, `.bequite/memory/progress.md` — pending updates.
- 🟠 `BeQuite_MASTER_PROJECT.md` itself becomes a tracked file in this commit (it's the source of the merge).
- 🟠 Commit + tag `v0.1.2`.

## Next sub-version

After `v0.1.2`: **`v0.2.0` — Skill orchestrator (the brain)**.

Tasks for v0.2.0:
1. Author `skill/SKILL.md` (Anthropic Skills schema; orchestrator persona; 7-phase router; mode selector).
2. Author each persona file in `skill/agents/` — adopting master's named roles + Skeptic + token-economist:
   - `product-owner.md`
   - `research-analyst.md`
   - `software-architect.md`
   - `frontend-designer.md` (Impeccable-loaded)
   - `backend-engineer.md`
   - `database-architect.md`
   - `qa-engineer.md`
   - `security-reviewer.md`
   - `devops-engineer.md`
   - `token-economist.md`
   - `skeptic.md` (kept from current; adversarial twin)
3. Author `skill/routing.json` — default routing matrix (post brief reconciliations).
4. Author `bequite.config.toml.tpl`.
5. Wire skill into `template/.claude/skills/bequite/`.

## Open questions (none blocking v0.1.2)

- E1 — GitHub org / repo name (`xpshawky/bequite` default; confirm before remote push, no remote configured)
- E2 — PyPI package name + ownership (will block v0.5.0 release)
- E3 — Studio (v2.0.0+) timing (after v1.0.0 ships, default)
- E4 — Telemetry policy (off entirely; pending ADR-002 in v0.7.0)
- E5 — Doctrine distribution model (separate org for community; pending in v0.12.0)
- E6 — MENA bilingual Researcher seeds (Ahmed seeds list at v0.11.0)
- E7 — Codex 5.5 review-mode role (review-only default; pending v0.8.0)

None of these block v0.1.2 → v0.5.x progress.

## Cost / wall-clock telemetry (this session)

Receipts ship in v0.7.0; until then, telemetry is best-effort.

- Cost-ceiling default: $20 per session
- Wall-clock-ceiling default: 6 h per session
