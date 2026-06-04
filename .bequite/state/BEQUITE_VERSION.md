# BeQuite installed version

**Version:** v3.0.0-alpha.18
**Updated:** 2026-06-04
**Source:** github
**Source path / repo:** xpShawky/BeQuite (branch: main)
**Previous version:** v3.0.0-alpha.17
**Last check:** 2026-06-04
**Update count:** 0 (this is the seed file; updates from /bq-update increment)

---

## How this file works

Refreshed by `/bq-update` on successful updates. Created by `/bq-init` (or the installer scripts) on first install.

Reading this file lets `/bq-update` know:
- What version is currently installed
- When it was last checked vs. last updated
- Which source (GitHub / local) to fetch updates from

## Version numbering

`v3.0.0-alpha.<N>` where N increments per alpha release. Latest releases are listed in `docs/changelogs/CHANGELOG.md`.

## Update history

(Populated by `/bq-update` runs — newest at top.)

### 2026-06-04 — alpha.18 ship — Harness, Hooks & Context-Engineering upgrade
- ADR-005 implemented (opt-in): 3 hooks × {sh,ps1} (destructive-block, secret-scan, banned-weasel-words) + `.claude/settings.json.example` (+ Windows variant) + `CLAUDE_CODE_HOOKS_STRATEGY.md`. NOT active by default (RCE-vector security model).
- 2 new skills (skills 22 → 24): `bequite-context-engineer` (all-workflow context engineering — generalizes the frontend DNA/continuity pattern) + `bequite-anti-hallucination` (evidence-over-claims, citation-or-strike, package verification, UNVERIFIED forced-fork).
- New memory: `PROJECT_DNA.md` (codebase conventions/architecture contract) + `WORKING_NOTES.md` (per-workflow scratchpad) + `FILE_RESPONSIBILITY_MAP.md` (anti-spaghetti, emitted by /bq-plan).
- New docs: `CONTEXT_ENGINEERING.md` + `HARNESS_AND_PROMPT_QUALITY.md` + `docs/specs/GAME_CHANGER_FEATURES.md` (report-only).
- CLAUDE.md core rule 16 (reliability discipline, compressed). Command upgrades: bq-review two-pass (spec→quality), bq-verify evidence+DoD, bq-discover map-before-act+Project DNA, bq-fix test-first+package-verify, bq-feature Project-DNA+package-verify, bq-plan/bq-assign File-Responsibility-Map, bq-auto confidence+2-failure-reset, RESEARCH_DEPTH citation-or-strike.
- Research: 6 cited streams (all anchored to official Anthropic docs) — hooks, context engineering, hallucination, safe implementation, harness, game-changer gaps.
- Tool-neutral: no Studio / CLI / dashboard / runtime dependency. Hooks are opt-in shell/PowerShell only.
- New master skill `bequite-frontend-design-system` (SKILL + 9 references + 3 examples) — coordinates ux-ui-designer / frontend-quality / live-edit; kills "middle-section drift"
- Design Continuity Gate (`DESIGN_CONTINUITY_PASS` + `VISUAL_QA_DONE` + `DESIGN_DNA_LOCKED`, conditional on a frontend) wired into 9 commands
- Design memory: `.bequite/design/` (DESIGN_DNA, FRONTEND_SKILL_MAP, DESIGN_CONTINUITY_REPORT) + `.bequite/audits/VISUAL_QA_REPORT.md` + `.bequite/state/FRONTEND_CONTEXT_SUMMARY.md`
- 2 architecture docs (DESIGN_CONTINUITY_GATE, FRONTEND_CONTEXT_ENGINEERING); SECTION_MAP enriched; MISTAKE_MEMORY seeded with 10 `[fe][design]` prevention rules
- Effort awareness added to FE skills + researcher + auto-mode strategy
- Researched references: Impeccable, UI-UX-Pro-Max, Superpowers (verified + cited)
- Skills 21 → 22; no new command; no Studio / CLI / dashboard / dependency added

### 2026-05-17 — alpha.16 ship — clean stable alpha (skill desc audit + ADR-005 + cross-refs)
- Skill `description:` YAML length audit — 8 over-length descriptions trimmed (now all ≤ ~300 chars for Anthropic Skills activation matching)
- `bequite-workflow-advisor` SKILL.md description refreshed (39→44 commands, 15→21 skills, 3→4 modes — previously stale)
- ADR-005 written: `docs/decisions/ADR-005-claude-code-hooks-for-machine-enforcement.md` — proposes opt-in Claude Code hooks for machine-enforcement of safety rules (banned weasel words, secret scan, destructive op block). Implementation deferred to alpha.17+
- Cross-references added between architecture docs: MEMORY_FIRST_BEHAVIOR ↔ token-saver / delegate / research; RESEARCH_DEPTH_STRATEGY ↔ deep / fast / delegate; MULTI_MODEL_PLANNING_STRATEGY now points at Delegate Mode as the operationalized cross-session form
- No new features; no Studio reintroduced; lightweight direction preserved

### 2026-05-17 — alpha.15 ship — mechanical-repair release (audit findings implemented)
- Memory-first preflight + gate-check + writeback added to 16 commands (`/bq-assign`, `/bq-audit`, `/bq-changelog`, `/bq-clarify`, `/bq-discover`, `/bq-doctor`, `/bq-handoff`, `/bq-implement`, `/bq-memory`, `/bq-recover`, `/bq-red-team`, `/bq-release`, `/bq-review`, `/bq-scope`, `/bq-test`, `/bq-verify`)
- `## When NOT to use this skill` + `## Quality gate` added to 19 skills (everyone except delegate-planner + updater which already had both)
- 2 new red-team angles: supply-chain (PhantomRaven / Shai-Hulud) + prompt-injection (OWASP LLM Top 10 #1) — total now 10 angles
- 9 stale top-level docs + 9 docs/audits/* + 2 docs/RELEASES/* + 1 docs/merge/* moved to `docs/legacy/`
- `docs/legacy/README.md` created explaining the archive
- `LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md` counts refreshed (44 commands / 21 skills / 4 modes / orthogonal workflows)
- `.bequite/MEMORY_INDEX.md` created (new orientation doc for every directory under `.bequite/`)
- `docs/runbooks/USING_BEQUITE_COMMANDS.md` extended with walkthroughs for all 4 operating modes + Presentation Builder + `/bq-auto` + the global feature-addition rule
- `bequite-workflow-advisor` SKILL.md updated to know all 44 commands + 21 skills + 4 modes (was outdated at 39 / 15)
- No new features; no Studio reintroduced; lightweight direction preserved

### 2026-05-17 — alpha.14 ship — discipline restoration
- 7 audit reports written (FULL_SYSTEM_ALIGNMENT_AUDIT, COMMAND_SKILL_CONSISTENCY_AUDIT, WORKFLOW_GATE_AUDIT, FEATURE_WORKFLOW_AUDIT, BEQUITE_SYSTEM_RESEARCH_REPORT, COMMAND_CLUTTER_REVIEW, FINAL_SYSTEM_ALIGNMENT_REPORT)
- Global feature-addition rule codified in CLAUDE.md + WORKFLOW_GATES.md + COMMAND_CATALOG.md
- Gate name aliases documented (`_DONE` and `_COMPLETE` both valid)
- Orthogonal workflows section added (Presentation / Job / Money / Suggest don't change mode)
- `/bq-add-feature` marked as deprecated alias for `/bq-feature`
- `OPEN_QUESTIONS.md` Q1-Q3 closed (resolved by ADR-001/004)
- `PROJECT_STATE.md` refreshed (removed stale Studio reference)
- `.bequite/research/` directory created with first system research report
- No new features added (this is a discipline release)
- Commands: 44 active + 1 deprecated alias; Skills: 21 (unchanged)

### 2026-05-13 — alpha.13 ship
- `/bq-presentation` added (premium PPTX / HTML builder)
- `bequite-presentation-builder` skill added
- `.bequite/presentations/` memory folder with 9 templates added
- Installer carries presentation templates
- Commands: 43 → 44; Skills: 20 → 21

### 2026-05-12 — alpha.12 ship
- 4 composable operating modes (Deep / Fast / Token Saver `lean` / Delegate)
- `bequite-delegate-planner` skill added
- Delegate task pack + MODE_HISTORY added
- Skills: 19 → 20

### 2026-05-12 — seeded
- Initial seed at v3.0.0-alpha.10 (the version this seed file was authored at)
- No prior `/bq-update` run yet
