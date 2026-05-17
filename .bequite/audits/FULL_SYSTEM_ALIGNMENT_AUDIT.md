# BeQuite — Full System Alignment Audit (alpha.14)

**Audit run:** 2026-05-17
**Auditor:** `/bq-auto deep` — self-audit (BeQuite eats its own food)
**Repo:** `xpShawky/BeQuite` · v3.0.0-alpha.13 → alpha.14
**Audit triggered by:** user observation that Presentation Builder (alpha.13) was shipped without going through the full discover → research → scope → plan → tasks → impl → docs → memory → changelog → catalog → help → menu → verify workflow.

---

## 1. Audit summary (one screen)

| Area | Status | Severity |
|---|---|---|
| Skill pack core surface (commands + skills + memory) | Mostly aligned | ⚪ minor |
| Workflow gates enforcement at runtime | Partially enforced — see §6 | 🟡 medium |
| Memory-first preflight in every command | 27 / 45 commands have it | 🟡 medium |
| Memory writeback in every command | 25 / 45 commands have it | 🟡 medium |
| Standardized command fields (alpha.6 schema) | 25 / 45 commands have full schema | 🟡 medium |
| "Token Saver" wording (no "token-free") | All 8 mentions are correctly NEGATING — not errors | ✅ pass |
| Studio / heavy CLI remnants | Present on disk (paused per ADR-001/004) but referenced in PROJECT_STATE.md as live | 🟡 medium |
| Stale OPEN_QUESTIONS (Q1-Q3 from alpha.1) | Never closed; resolved by ADR-001/004 | 🟡 medium |
| Stale top-level docs from heavy direction | 9 stale `docs/*.md` + `docs/audits/*` + `docs/RELEASES/*` + `docs/merge/*` not moved to legacy | 🟡 medium |
| Feature-workflow discipline for alpha.13 | Presentation Builder shipped without proper discover→research→scope→plan→tasks→verify | 🟠 high |
| Global "every feature follows this workflow" rule | Not codified anywhere | 🟠 high |
| Command count consistency (44 vs 45) | README says 44, repo has 45 (1 menu + 44 bq-*) | ⚪ minor |
| Skill "Quality gate" + "When NOT to use" sections | 3 / 21 have Quality gate; 5 / 21 have "When NOT to use" | 🟡 medium |

**Verdict:** BeQuite v3.0.0-alpha.13 is functionally solid for its core surface, but DISCIPLINE drift has crept in. The system added 5 alphas of features without enforcing its own workflow on itself. **alpha.14 is the discipline-restoration release.**

---

## 2. Current repo structure (inventory)

```
BeQuite/
├── .claude/
│   ├── commands/          (45 files: bequite.md + 44 bq-*.md)
│   └── skills/            (21 directories: bequite-*)
├── .bequite/
│   ├── state/             (CURRENT_MODE, CURRENT_PHASE, WORKFLOW_GATES, LAST_RUN,
│   │                       DECISIONS, OPEN_QUESTIONS, PROJECT_STATE, ASSUMPTIONS,
│   │                       MISTAKE_MEMORY, MODE_HISTORY, BEQUITE_VERSION, UPDATE_SOURCE)
│   ├── logs/              (AGENT_LOG, CHANGELOG, ERROR_LOG, UPDATE_LOG)
│   ├── audits/            (DISCOVERY_REPORT, DOCTOR_REPORT, DIRECTION_RESET_AUDIT,
│   │                       GITHUB_READY_CLEANUP_AUDIT, DELEGATE_REVIEW_REPORT, ...)
│   ├── plans/             (FEATURE_EXPANSION_ROADMAP, SCOPE, IMPLEMENTATION_PLAN)
│   ├── tasks/             (TASK_LIST, CURRENT_TASK, DELEGATE_TASKS, DELEGATE_INSTRUCTIONS,
│   │                       DELEGATE_ACCEPTANCE_CRITERIA, DELEGATE_TEST_PLAN)
│   ├── principles/        (TOOL_NEUTRALITY)
│   ├── decisions/         (ADRs)
│   ├── uiux/              (SECTION_MAP, LIVE_EDIT_LOG, UIUX_VARIANTS_REPORT, selected-variant,
│   │                       screenshots/, archive/)
│   ├── jobs/              (8 templates: JOB_PROFILE, JOB_SEARCH_LOG, OPPORTUNITIES,
│   │                       APPLICATION_TRACKER, PITCH_TEMPLATES, HIDDEN_GEMS,
│   │                       COMMUNITY_SIGNALS, AI_ASSISTED_WORK)
│   ├── money/             (8 templates: MONEY_PROFILE, MONEY_SEARCH_LOG, OPPORTUNITIES,
│   │                       TRUST_CHECKS, ACTION_PLAN, HIDDEN_GEMS, COMMUNITY_SIGNALS,
│   │                       AI_ASSISTED_PATHS)
│   ├── presentations/     (9 templates + assets/ + outputs/) ← alpha.13
│   ├── research/          (BEQUITE_SYSTEM_RESEARCH_REPORT) ← alpha.14
│   ├── backups/           (created on /bq-update)
│   ├── prompts/           (multi-model paste artifacts)
│   └── memory/            (v2.x legacy memory bank — paused, kept on disk)
├── docs/
│   ├── architecture/      (11 files — current direction)
│   ├── decisions/         (4 ADRs — current)
│   ├── runbooks/          (3 files — current)
│   ├── specs/             (3 files — current)
│   ├── changelogs/        (CHANGELOG, AGENT_LOG — current)
│   ├── audits/            (6 files — STALE; heavy direction)
│   ├── RELEASES/          (v1.0.0, v2.0.0-alpha.1 — STALE; heavy direction)
│   ├── merge/             (1 file — STALE; heavy direction)
│   ├── planning_runs/     (STALE)
│   ├── AUTONOMOUS-MODE.md (STALE; v0-v2)
│   ├── DOCTRINE-AUTHORING.md (STALE; v0-v2)
│   ├── HOSTS.md           (STALE)
│   ├── HOW-IT-WORKS.md    (STALE)
│   ├── INSTALL.md         (STALE — superseded by docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md)
│   ├── MAINTAINER.md      (STALE)
│   ├── QUICKSTART.md      (STALE)
│   ├── README.md          (STALE — top-level README.md is the canonical one)
│   └── SECURITY.md        (STALE — direction-agnostic but unused)
├── scripts/
│   ├── install-bequite.{ps1,sh}    (current; bumped to alpha.13)
│   ├── install.{ps1,sh}            (STALE — heavy direction install)
│   └── bootstrap.{ps1,sh}          (STALE — heavy direction)
├── README.md              (current — alpha.13)
├── commands.md            (current — alpha.13)
├── CLAUDE.md              (current — alpha.13)
├── BEQUITE_BOOTSTRAP_BRIEF.md  (historical reference; keep)
├── BeQuite_MASTER_PROJECT.md   (historical reference; keep)
├── cli/, skill/, template/, evidence/, tests/, state/ (PAUSED per ADR-001 / ADR-004 — kept on disk, not active)
└── studio/                (PAUSED per ADR-004 — heavy direction retired)
```

---

## 3. Existing commands (45)

(Full per-command inventory in `COMMAND_SKILL_CONSISTENCY_AUDIT.md`.)

| Phase / category | Commands |
|---|---|
| Root | `/bequite`, `/bq-help`, `/bq-now`, `/bq-explain` |
| P0 | `/bq-init`, `/bq-mode`, `/bq-new`, `/bq-existing`, `/bq-discover`, `/bq-doctor` |
| P1 | `/bq-clarify`, `/bq-research`, `/bq-scope`, `/bq-spec`, `/bq-plan`, `/bq-multi-plan` |
| P2 | `/bq-assign`, `/bq-implement`, `/bq-feature`, `/bq-fix`, `/bq-add-feature` (legacy) |
| P3 | `/bq-test`, `/bq-audit`, `/bq-review`, `/bq-red-team` |
| P4 | `/bq-verify`, `/bq-release`, `/bq-changelog` |
| P5 | `/bq-memory`, `/bq-recover`, `/bq-handoff` |
| Orchestrators | `/bq-p0`, `/bq-p1`, `/bq-p2`, `/bq-p3`, `/bq-p4`, `/bq-p5`, `/bq-auto` |
| UI / UX | `/bq-uiux-variants`, `/bq-live-edit` |
| Opportunity (alpha.8) | `/bq-suggest`, `/bq-job-finder`, `/bq-make-money` |
| Maintenance | `/bq-update` |
| Creative + Content (alpha.13) | `/bq-presentation` |

**Count reconciliation:** repo has **45 files** (1 root + 44 bq-*); README badge says "44 commands" — README counts only `bq-*`. Decision: keep README badge wording as is (it counts slash commands the user runs; `/bequite` is the menu, not a workflow command). Document both numbers in the catalog.

---

## 4. Existing skills (21)

| Skill | Status | Has "Quality gate" | Has "When NOT to use" |
|---|---|---|---|
| `bequite-backend-architect` | active | ❌ | ❌ |
| `bequite-database-architect` | active | ❌ | ❌ |
| `bequite-delegate-planner` | active (alpha.12) | ✅ | ✅ |
| `bequite-devops-cloud` | active | ❌ | ❌ |
| `bequite-frontend-quality` | active | ❌ | ❌ |
| `bequite-job-finder` | active (alpha.8) | ❌ | ❌ |
| `bequite-live-edit` | active | ❌ | ✅ |
| `bequite-make-money` | active (alpha.8) | ❌ | ❌ |
| `bequite-multi-model-planning` | active | ❌ | ✅ |
| `bequite-presentation-builder` | active (alpha.13) | ❌ | ❌ |
| `bequite-problem-solver` | active | ❌ | ❌ |
| `bequite-product-strategist` | active | ❌ | ❌ |
| `bequite-project-architect` | active | ❌ | ❌ |
| `bequite-release-gate` | active | ❌ | ❌ |
| `bequite-researcher` | active | ❌ | ✅ |
| `bequite-scraping-automation` | active | ❌ | ❌ |
| `bequite-security-reviewer` | active | ❌ | ❌ |
| `bequite-testing-gate` | active | ❌ | ❌ |
| `bequite-updater` | active (alpha.10) | ✅ | ✅ |
| `bequite-ux-ui-designer` | active | ❌ | ❌ |
| `bequite-workflow-advisor` | active (alpha.8) | ✅ | ❌ |

**Tally:** 3 of 21 have explicit `Quality gate` section. 5 of 21 have `When NOT to use`. **18 skills** lack either or both — alpha.14 repair must add them.

---

## 5. Existing docs

### Current (keep)
- `README.md`, `commands.md`, `CLAUDE.md` (top level)
- `docs/architecture/AUTO_MODE_STRATEGY.md`
- `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md`
- `docs/architecture/DEVOPS_CLOUD_SAFETY.md`
- `docs/architecture/FEATURE_AND_FIX_WORKFLOWS.md`
- `docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md`
- `docs/architecture/LIVE_EDIT_STRATEGY.md`
- `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`
- `docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md`
- `docs/architecture/RESEARCH_DEPTH_STRATEGY.md`
- `docs/architecture/UIUX_VARIANTS_STRATEGY.md`
- `docs/architecture/WORKFLOW_GATES.md`
- `docs/decisions/ADR-001..004`
- `docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md`
- `docs/runbooks/LOCAL_DEV.md`
- `docs/runbooks/USING_BEQUITE_COMMANDS.md`
- `docs/specs/COMMAND_CATALOG.md`
- `docs/specs/MULTI_MODEL_PLANNING_REQUIREMENTS.md`
- `docs/specs/MVP_LIGHTWEIGHT_SCOPE.md`
- `docs/changelogs/CHANGELOG.md`
- `docs/changelogs/AGENT_LOG.md`

### Stale (heavy direction; should move to `docs/legacy/`)
- `docs/AUTONOMOUS-MODE.md`
- `docs/DOCTRINE-AUTHORING.md`
- `docs/HOSTS.md`
- `docs/HOW-IT-WORKS.md`
- `docs/INSTALL.md`
- `docs/MAINTAINER.md`
- `docs/QUICKSTART.md`
- `docs/README.md`
- `docs/SECURITY.md`
- `docs/audits/*` (6 files)
- `docs/RELEASES/*` (2 files)
- `docs/merge/*` (1 file)
- `docs/planning_runs/*`

---

## 6. Feature list (vs. workflow discipline)

| Feature | Alpha | Discover | Research | Scope | Plan | Tasks | Impl | Docs | Memory | Changelog | Catalog | Help | Menu | Verify |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Lightweight pack core | 1 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `/bq-add-feature` (legacy) | 1 | ❌ | ❌ | ❌ | ⚪ | ❌ | ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Specialist skills (7 new) | 2 | ❌ | ⚪ | ⚪ | ❌ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ |
| Tool neutrality (ADR-003) | 3 | ✅ | ⚪ | ✅ | ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ |
| `/bq-uiux-variants`, `/bq-live-edit` | 4 | ⚪ | ✅ | ✅ | ✅ | ⚪ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ |
| `/bq-now`, mistake memory | 5 | ⚪ | ⚪ | ⚪ | ⚪ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ |
| Installer alpha.5 templates | 6 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ✅ |
| `/bq-spec`, `/bq-explain` | 7 | ⚪ | ⚪ | ⚪ | ⚪ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ | ⚪ |
| `/bq-suggest`, `/bq-job-finder`, `/bq-make-money` | 8 | ⚪ | ⚪ | ⚪ | ⚪ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ |
| Installer jobs+money templates | 9 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ⚪ | ✅ | ✅ | ⚪ | ⚪ | ⚪ | ✅ |
| Deep opportunity intel + `/bq-update` + memory-first doc | 10 | ⚪ | ⚪ | ⚪ | ⚪ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ |
| Installer hotfix (template lines) | 11 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ⚪ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **4 operating modes (Deep/Fast/Token-Saver/Delegate)** | 12 | ⚪ | ⚪ | ⚪ | ⚪ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ |
| **Presentation Builder (`/bq-presentation`)** | 13 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚪ |

Legend: ✅ done · ⚪ partial / informal · ❌ skipped

**Findings:**

1. **Presentation Builder (alpha.13) was the trigger for this audit** — user is right. Workflow steps skipped:
   - No `DISCOVERY_REPORT` for presentation domain
   - No `RESEARCH_REPORT` (no formal comparison of PPTX libraries, HTML frameworks, motion approaches)
   - No `SCOPE.md` lock
   - No `IMPLEMENTATION_PLAN.md`
   - No `TASK_LIST.md`
   - No `VERIFY_REPORT.md` post-ship
   - The command + skill + templates + docs were authored straight through. Output is solid but **process was wrong**.
2. **Almost every alpha skipped formal discover→research→scope→plan→tasks** in favor of "specification straight from user prompt." This worked because the user is the project owner and provided detailed specs, but it normalizes skipping discipline.
3. **No version's verification step was a formal `/bq-verify`** — verification was acceptance-criteria checks in commit messages.

---

## 7. Missing command files / placeholders

**No commands are placeholders.** Smallest commands (under 150 lines) are all intentionally compact (orchestrators, mode selectors, workflow entry points):
- `bq-existing.md` (93 lines) — workflow entry; complete schema
- `bq-mode.md` (97 lines) — mode selector
- `bq-new.md` (98 lines) — workflow entry
- `bq-p0`..`bq-p5` (110–135 lines) — orchestrators, dispatch logic only
- `bq-now.md` (125 lines) — one-line orientation

**18 commands lack memory-first preflight (`## Files to read` section):**
- `bq-add-feature`, `bq-assign`, `bq-audit`, `bq-changelog`, `bq-clarify`, `bq-discover`, `bq-doctor`, `bq-handoff`, `bq-implement`, `bq-init`, `bq-memory`, `bq-recover`, `bq-red-team`, `bq-release`, `bq-review`, `bq-scope`, `bq-test`, `bq-verify`

**20 commands lack explicit `## Memory updates` / `## Log updates` section:**
- The same 18 above + 2 more (need per-file verification)

**20 commands lack the alpha.6 "Standardized command fields" section:**
- These are mostly older alpha.1 commands. Functional but inconsistent with the alpha.6+ schema.

---

## 8. Skills missing required sections

(Full per-skill table in §4 above.)

**18 of 21 skills lack `Quality gate` section.**
**16 of 21 skills lack `When NOT to use` section.**

Alpha.14 repair: add `## Quality gate` and `## When NOT to use` sections to the 18 / 16 affected skills.

---

## 9. Commands missing workflow-gate enforcement

(Detailed in `WORKFLOW_GATE_AUDIT.md`.)

The doc `docs/architecture/WORKFLOW_GATES.md` and the state file `.bequite/state/WORKFLOW_GATES.md` define 23 gates. Each command claims "Required previous gates" in its standardized fields. However:

- **No command file contains a runtime check that reads `.bequite/state/WORKFLOW_GATES.md` and refuses if gates aren't met.** The discipline is documented but not enforced by the agent at runtime.
- The enforcement is **convention-based**: the agent (Claude reading the command file) is expected to check gate state and refuse if unmet, but there's no machine-checkable gate.
- This is acceptable for a markdown-driven skill pack — but it must be DOCUMENTED clearly in CLAUDE.md and each command's "Failure behavior" section.

---

## 10. Docs missing command updates

After alpha.13, these docs lack the new `/bq-presentation` command:
- ✅ `README.md` — updated alpha.13
- ✅ `commands.md` — updated alpha.13
- ✅ `CLAUDE.md` — updated alpha.13
- ✅ `.claude/commands/bequite.md` — updated alpha.13
- ✅ `.claude/commands/bq-help.md` — updated alpha.13
- ✅ `.claude/commands/bq-suggest.md` — updated alpha.13
- ✅ `.claude/skills/bequite-workflow-advisor/SKILL.md` — updated alpha.13
- ✅ `docs/specs/COMMAND_CATALOG.md` — updated alpha.13
- ✅ `docs/changelogs/CHANGELOG.md` — updated alpha.13
- ❌ `docs/runbooks/USING_BEQUITE_COMMANDS.md` — **MISSING walkthrough**
- ❌ `docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md` — **MISSING the alpha.13 presentation node** (still says 24 commands / 7 skills)

---

## 11. README gaps

- ✅ Commands listed
- ✅ Operating modes section
- ✅ Skill list
- ✅ Workflow phases
- ✅ Quick start
- ✅ How to use
- ❌ Roadmap doesn't mention alpha.13 (still says "MVP — alpha.8" and "v1 — alpha.9")
- ❌ Architecture diagram still says "36 commands / 15 skills" (out of date by 4 alphas)

---

## 12. commands.md gaps

- ✅ All commands listed
- ✅ Operating modes section
- ✅ Presentation Builder section
- ❌ TOC has duplicate anchor names (some sections use mixed casing)
- ❌ Some older commands lack the alpha.6 "Required gates" field consistently

---

## 13. /bequite root menu gaps

- ✅ Creative + Content Workflows section (alpha.13)
- ✅ Operating modes block (alpha.12)
- ❌ Comment line at top of body still says "Command map (34 commands, ordered by workflow phase):" — should be 44
- ❌ "Maintenance" section duplicates `/bq-memory`, `/bq-recover`, `/bq-handoff` which already appear in Phase 5

---

## 14. /bq-help gaps

- ✅ Modes table (alpha.12)
- ✅ alpha.13 surface listed
- ❌ Phase naming inconsistency at the bottom (calls it "Phase 0 — Setup and Understanding"; canonical is "Setup and Discovery")
- ❌ Some commands' `## Files to read` not summarized in this overview

---

## 15. Memory update gaps

State files:
- ✅ `LAST_RUN.md` — fresh
- ✅ `MODE_HISTORY.md` — fresh
- ✅ `MISTAKE_MEMORY.md` — fresh (empty, expected for this repo as a project)
- ✅ `BEQUITE_VERSION.md` — fresh
- ❌ `PROJECT_STATE.md` — STALE: still says "Stack detected: Python CLI (`cli/`) + paused Studio (`studio/`)". Studio retired per ADR-004.
- ❌ `OPEN_QUESTIONS.md` — STALE: Q1 (studio deletion), Q2 (alpha.1 release), Q3 (Python CLI retirement) all from alpha.1, all resolved by ADRs, never closed.
- ⚪ `CURRENT_MODE.md` — template placeholder for installed projects; for THIS repo, the working mode is "Add Feature" implicit but never set
- ⚪ `CURRENT_PHASE.md` — template placeholder; for THIS repo, working phase is mid-cycle

---

## 16. Changelog update gaps

- ✅ alpha.12 entry — complete
- ✅ alpha.13 entry — complete
- ❌ `docs/changelogs/CHANGELOG.md` has `[Unreleased — alpha.14]` placeholder but no full alpha.14 spec yet (this audit will close it)
- ❌ Older alpha.1-alpha.7 entries condensed; some changelog entries were never written for the heavy direction → lightweight pivot

---

## 17. Files that disagree with each other

| Inconsistency | Files involved |
|---|---|
| Command count: 44 vs 45 | README badge (44), CLAUDE.md (44), commands.md (44), `/bequite` menu (says 34 at top of body), `.claude/commands/` (actual: 45 files) |
| Skill count: 14, 15, 19, 20, 21 mentioned in various places | CLAUDE.md says "14 skills" in one section + "21" in another; LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md says "7" + "11"; `/bequite` menu says "11"; reality is **21** |
| Gate names: `DISCOVERY_DONE` vs `DISCOVERY_COMPLETE` | `docs/architecture/WORKFLOW_GATES.md` (DISCOVERY_COMPLETE), `docs/specs/COMMAND_CATALOG.md` (DISCOVERY_DONE in some entries) |
| Phase naming: "Setup and Understanding" vs "Setup and Discovery" | `/bq-help.md` (older naming), most other places use canonical "Setup and Discovery" |
| `/bq-add-feature` vs `/bq-feature` | `bq-add-feature.md` still exists; `/bq-feature` supersedes it. Legacy alias not documented as deprecated. |

---

## 18. Features added without workflow

The user's hypothesis is confirmed: **most alpha-version features were added straight to implementation without going through discover→research→scope→plan→tasks→verify**. Specifically:

- alpha.5: `/bq-now` — added direct
- alpha.5: mistake memory — added direct
- alpha.7: `/bq-spec`, `/bq-explain` — added direct
- alpha.8: `/bq-suggest`, `/bq-job-finder`, `/bq-make-money` — added direct
- alpha.10: deep opportunity intelligence — added direct
- alpha.10: `/bq-update` — added direct
- alpha.10: memory-first behavior — added direct
- **alpha.12: 4 operating modes — added direct** (user explicitly prompted skip)
- **alpha.13: Presentation Builder — added direct** (the audit trigger)

The user's prompts contained the spec content, so the agent shortcut to implementation. **This is the core process drift.**

---

## 19. Features that need a research pass

For alpha.14 deep research, the following features deserve targeted research evidence to inform alpha.15+:

1. **Presentation Builder tool choice** — when user invokes `/bq-presentation` for real, the agent must decide between python-pptx / pptxgenjs / reveal.js / Slidev / Marp / Spectacle / Impress.js. Pre-research the trade-offs in `BEQUITE_SYSTEM_RESEARCH_REPORT.md`.
2. **PPTX morph technique** — research how Microsoft Morph + python-pptx + pptxgenjs handle morph-like transitions reliably.
3. **HTML slide motion patterns** — research GSAP vs Motion One vs vanilla CSS for slide motion.
4. **Spec Kit interop** — `/bq-spec` writes Spec Kit-compatible specs, but the interop hasn't been verified against the latest Spec Kit release.
5. **Skill pack distribution patterns** — research Anthropic Skills SKILL.md format vs Claude Code subagent format vs Continue.dev custom commands.
6. **BMad Method comparison** — research what BMad agents do better; extract principles.
7. **Memory system patterns** — research Cline Memory Bank, Roo Code memory, Claude Code project memory.
8. **Audit + red-team workflow patterns** — research existing red-team prompt packs.

---

## 20. Final repair plan (alpha.14)

### Priority 1 — Discipline restoration (high)

1. **Add global feature-addition rule** to:
   - `CLAUDE.md`
   - `docs/architecture/WORKFLOW_GATES.md`
   - `docs/specs/COMMAND_CATALOG.md`
   - `docs/runbooks/USING_BEQUITE_COMMANDS.md`
   - Every action command's "Failure behavior" or top-level rule section

2. **Memory-first preflight** added to all 18 missing commands.
3. **Memory writeback** section added to all 20 missing commands.
4. **Standardized command fields** added to all 20 missing commands.

### Priority 2 — Skill consistency (medium)

5. **`## Quality gate`** added to 18 missing skills.
6. **`## When NOT to use`** added to 16 missing skills.

### Priority 3 — Doc hygiene (medium)

7. **Move stale heavy-direction docs** to `docs/legacy/`:
   - 9 top-level `docs/*.md` files
   - `docs/audits/`
   - `docs/RELEASES/`
   - `docs/merge/`
   - `docs/planning_runs/`
8. **Update `PROJECT_STATE.md`** to remove "paused Studio" stale reference.
9. **Update `OPEN_QUESTIONS.md`** to close Q1-Q3.
10. **Update `LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md`** to current count (44 commands, 21 skills).
11. **Update `USING_BEQUITE_COMMANDS.md`** with Presentation Builder + Delegate Mode walkthroughs.

### Priority 4 — Number reconciliation (minor)

12. Standardize "44 commands" everywhere it appears (`/bequite` menu top comment, README badges, CLAUDE.md, COMMAND_CATALOG).
13. Standardize "21 skills" everywhere it appears.

### Priority 5 — Research (deferred to alpha.14 ship)

14. Write `BEQUITE_SYSTEM_RESEARCH_REPORT.md` with deep-mode research on the 8 topics in §19.

### Priority 6 — Verification

15. Run a self-audit pass post-repair: do the 18 commands now have memory-first? Do the 18 skills now have quality gates? Mark `FINAL_SYSTEM_ALIGNMENT_REPORT.md`.

---

## 21. Acceptance criteria for alpha.14

- All 7 audit reports exist ✅ (after this run)
- Global feature-addition rule codified in 4+ docs
- All 45 commands have memory-first preflight + memory writeback
- All 21 skills have Quality gate + When NOT to use
- Stale docs moved to `docs/legacy/`
- `PROJECT_STATE.md` + `OPEN_QUESTIONS.md` refreshed
- `LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md` count refreshed
- `USING_BEQUITE_COMMANDS.md` has Presentation + Delegate walkthroughs
- All counts (44 / 21) consistent across all files
- No new features added in alpha.14 (this is a discipline release)
- alpha.14 tagged + pushed
- `FINAL_SYSTEM_ALIGNMENT_REPORT.md` written with what landed + what didn't
