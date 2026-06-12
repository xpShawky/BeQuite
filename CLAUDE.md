# CLAUDE.md

Claude-Code-specific operating instructions for the **BeQuite** repository.

Read this on every session start.

---

## What this repo is

BeQuite is a **lightweight Claude Code skill pack** you install into any project. v3.0.0+ direction (per `docs/decisions/ADR-001-lightweight-skill-pack-first.md`).

This repo IS the source of the skill pack. Its `.claude/commands/` + `.claude/skills/` are the files that get copied into target projects by `scripts/install-bequite.{ps1,sh}`.

**Direction:** lightweight only. No Studio. No heavy CLI / TUI. No localhost dashboard. No Docker. No frontend / API / database / 3D required by default (ADR-004).

---

## Current spec: v3.0.0-alpha.22 — Navigation & Capability Consolidation

- **52 active slash commands + 1 deprecated alias** (`.claude/commands/`) — alpha.22 adds C3 `/bq-reference` · C4 `/bq-knowledge` · C5 `/bq-course` · C6 `/bq-pain-radar` · C7 `/bq-integrate` · C8 `/bq-proposal`; alpha.19 added `/bq-writing-dna` + `/bq-skill-audit`. **Catalog IDs (alpha.22):** display-only W0–W5 / N / O / C / M IDs in `.bequite/commands/COMMAND_ID_MAP.md` — files are NEVER renamed (`docs/architecture/COMMAND_NUMBERING_AND_ORDERING_STRATEGY.md`).
- **29 skills** (alpha.22 adds `bequite-localization-rtl` (auto-attach on Arabic/MENA/RTL) + `bequite-guard-pass`; alpha.21 added `bequite-frontier-reasoning-coach`)
- **Command Router (alpha.22)** — second routing layer: Skill Router answers *which skills*; Command Router answers *which command next*. Contract step 12 = multi-command "Next Command Recommendations" (required next + 2–6 set + accelerators + do-not-run-yet); auto mode reports "Internal workflow executed: <IDs>". Files: `docs/architecture/WORKFLOW_COMMAND_ROUTER.md` · `.bequite/commands/{COMMAND_ROUTER,COMMAND_ID_MAP,NEXT_COMMAND_LOG}.md`. `/bq-suggest` (N4) is the main navigation assistant.
- **Guard Pass (alpha.22)** — reactive post-work gates for AI failure modes (code/test/docs guards; guard-skills concept adapted, nothing copied/installed): `bequite-guard-pass` + `docs/architecture/GUARD_PASS_STRATEGY.md` + `.bequite/audits/GUARD_PASS_REPORT.md`. Runs after implement/test, before verify/release.
- **Capability memory (alpha.22)** — `.bequite/{reference,knowledge,courses,pain-radar,integrations,proposals}/` (files created on first run); specs in `docs/specs/{REFERENCE_ENGINE,KNOWLEDGE_ENGINE,COURSE_ENGINE,PAIN_RADAR,INTEGRATION_BLUEPRINT,PROPOSAL_BUILDER,LOCALIZATION_RTL}.md`; shape rulings in `.bequite/plans/APPROVED_CAPABILITY_SHAPE_DECISIONS.md` (incl. the Older-V1-candidate review)
- **Automatic skill routing (alpha.20)** + **Confidence Forecast / Frontier Playbook / FEATURE_TYPE_TAXONOMY / Discovery V2 (alpha.21)** — registry/router/usage-log at `.bequite/skills/`; banded confidence on every plan/task; `expert` = composition alias, not a 5th mode
- **26 skills** (`.claude/skills/bequite-*/SKILL.md`) — adds `bequite-writing-dna` + `bequite-skill-auditor` in alpha.19; `bequite-context-engineer` + `bequite-anti-hallucination` in alpha.18; `bequite-frontend-design-system` (master) in alpha.17; `bequite-presentation-builder` in alpha.13; `bequite-delegate-planner` in alpha.12
- **Execution contract (alpha.19)** — every command follows the 11 steps in `docs/architecture/COMMAND_EXECUTION_CONTRACT.md` (preflight → gate → scope → skills → research-check → plan-check → action → verification → report → writeback → next). Strategy indexes: `HARNESS_ENGINEERING_STRATEGY.md` · `CONTEXT_ENGINEERING_STRATEGY.md` · `PROMPT_ENGINEERING_STANDARD.md` (+ `.bequite/prompts/PROMPT_PATTERNS.md`).
- **File-edit safety (alpha.19)** — risky file edits (env/secrets/auth/migrations/deploy/CI/payments/RLS/mass-deletes) tiered R3-CONFIRM / R2-ANNOUNCE / R1 per `docs/architecture/FILE_RISK_CLASSIFICATION.md` + project-tunable `.bequite/state/FILE_RISK_RULES.md`. R3 edits are a hard human gate even in auto mode.
- **Writing DNA (alpha.19)** — `/bq-writing-dna` + `bequite-writing-dna`: reusable writing profile from samples; strict mode = full source fidelity; memory at `.bequite/writing/` (5 templates). Ethics: no fabricated citations, no academic dishonesty, no detector-evasion framing. Third DNA pillar (project / design / writing).
- **Skill quality loop (alpha.19)** — `/bq-skill-audit` + `bequite-skill-auditor`: evidence-cited structural review of the pack; report-only by default; seed run at `.bequite/audits/SKILL_QUALITY_AUDIT.md`.
- **Generic context summary + evidence ledger (alpha.19)** — `.bequite/state/CONTEXT_SUMMARY.md` (compaction-surviving snapshot for ALL workflows) + `.bequite/research/EVIDENCE_LOG.md` (durable verification evidence backing anti-hallucination). No-research-repeat rule: check `.bequite/research/` before any research step.
- **Game-changer decision tracker (alpha.19)** — `.bequite/plans/GAME_CHANGER_FEATURE_DISCOVERY.md` (keep/reject/built ledger; proposals only become builds via the 15-step workflow).
- **Harness, Hooks & Context-Engineering (alpha.18)** — opt-in Claude Code **hooks** machine-enforce the safety subset (destructive ops · secrets · weasel-word completion claims; `.claude/hooks/*` + `settings.json.example`, **NOT active by default** — review before enabling, RCE-vector). `bequite-context-engineer` generalizes the frontend DNA/continuity pattern to ALL workflows (`PROJECT_DNA.md` + `WORKING_NOTES.md` + compact/clear/externalize + session-orientation). `bequite-anti-hallucination` enforces evidence-over-claims + citation-or-strike + package verification + the `UNVERIFIED` forced-fork. See core rule 16 + `docs/architecture/{CLAUDE_CODE_HOOKS_STRATEGY,CONTEXT_ENGINEERING,HARNESS_AND_PROMPT_QUALITY}.md`. Game-changer features delivered as a report (`docs/specs/GAME_CHANGER_FEATURES.md`), not built.
- **Frontend Design Continuity (alpha.17)** — master skill `bequite-frontend-design-system` + the **Design Continuity Gate** keep UI quality consistent from hero to footer, killing "middle-section drift" (generic cards, all-caps misuse, wide tracking, text overflow, lost identity in the middle). Design DNA persisted at `.bequite/design/DESIGN_DNA.md` (gate `DESIGN_DNA_LOCKED`); the gate (`DESIGN_CONTINUITY_PASS` + `VISUAL_QA_DONE`) runs in `/bq-feature` `/bq-fix` `/bq-auto` `/bq-uiux-variants` `/bq-live-edit` `/bq-audit` `/bq-review` `/bq-red-team` `/bq-verify`. **Quality promise:** every visible section must meet the Design DNA — hero quality is not enough. Section-by-section build loop + product-type awareness + visual QA. See `docs/architecture/DESIGN_CONTINUITY_GATE.md` + `docs/architecture/FRONTEND_CONTEXT_ENGINEERING.md`.
- **Creative + Content Workflows (alpha.13)** — `/bq-presentation` produces premium PPTX or HTML decks from topic / files / brand assets / research. Strict (preserves source) vs creative (adds structure). Variants 1–10. Morph-like motion for PPTX, CSS/JS for HTML. Memory at `.bequite/presentations/`.
- **4 composable operating modes** (alpha.12) — Deep / Fast / Token Saver (alias `lean`) / Delegate. Set per command with `--mode <mode>` or as positional flags. All 17 hard human gates apply regardless of mode. Tracked in `.bequite/state/CURRENT_MODE.md` and `MODE_HISTORY.md`. Full table in `commands.md` § Operating Modes and `docs/architecture/AUTO_MODE_STRATEGY.md` §11.
- **Memory-first behavior** — every action-taking command reads core memory (state / mode / phase / gates / last-run / mistake-memory / mode-history) before acting; see `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`
- **6 explicit workflow modes** — New Project, Existing Audit, Add Feature, Fix Problem, Research Only, Release Readiness (these are the workflow-level modes; the 4 operating modes above are orthogonal depth/cost flags)
- **6 workflow phases** — P0 Setup → P1 Framing → P2 Build → P3 Quality → P4 Release → P5 Memory
- **23 workflow gates** tracked in `.bequite/state/WORKFLOW_GATES.md` (block out-of-order commands)
- **Phase orchestrators** — `/bq-p0` … `/bq-p5` walk a single phase end-to-end
- **Scoped autonomous runner** — `/bq-auto [intent] [--mode fast|deep|token-saver|delegate] "task"` parses 17 intent types; pauses only at hard human gates
- **UI/UX variants** — `/bq-uiux-variants [N] "task"` generates 1-10 isolated design directions
- **Live edit** — `/bq-live-edit "task"` section-by-section frontend edits with section mapping
- **Mistake memory** — wired into 7 commands (fix / audit / review / red-team / verify / auto / live-edit); writes to `.bequite/state/MISTAKE_MEMORY.md`
- **Quick orientation** — `/bq-now` returns one-line status (faster than `/bequite`)
- **Spec Kit interop** — `/bq-spec "<feature>"` writes one-page `specs/<slug>/spec.md`
- **Plain-English explainer** — `/bq-explain "<target>"` for files / functions / decisions / artifacts
- **Workflow advisor** — `/bq-suggest "<situation>"` recommends best commands/mode for the goal (alpha.8); reads `MODE_HISTORY.md` to learn user patterns (alpha.12)
- **Job finder** — `/bq-job-finder` finds real work opportunities; supports `worldwide_hidden=true` (alpha.8)
- **Make money finder** — `/bq-make-money` finds legitimate earning opportunities; 10 tracks + Hidden Gems (alpha.8); deep intelligence with community signals + trending + AI-assisted (alpha.10)
- **BeQuite self-update** — `/bq-update` safely refreshes commands / skills / docs from GitHub or local source; never overwrites project memory (alpha.10)
- **Memory-first** — every action command reads core memory before acting (alpha.10; see MEMORY_FIRST_BEHAVIOR.md)
- **Delegate task pack** — `.bequite/tasks/DELEGATE_*.md` + `.bequite/audits/DELEGATE_REVIEW_REPORT.md`: strong-model writes, cheap-model implements, strong-model reviews (alpha.12)
- **Public command reference** — `commands.md` at repo root

---

## Where things live

| Need | Path |
|---|---|
| Slash commands (52 active + 1 alias; IDs in COMMAND_ID_MAP) | `.claude/commands/` |
| Command Router (alpha.22) | `.bequite/commands/{COMMAND_ID_MAP,COMMAND_ROUTER,NEXT_COMMAND_LOG}.md` · `docs/architecture/WORKFLOW_COMMAND_ROUTER.md` |
| Capability memory (alpha.22) | `.bequite/{reference,knowledge,courses,pain-radar,integrations,proposals}/` |
| Guard Pass (alpha.22) | `bequite-guard-pass` skill · `docs/architecture/GUARD_PASS_STRATEGY.md` · `.bequite/audits/GUARD_PASS_REPORT.md` |
| Jobs memory | `.bequite/jobs/` (JOB_PROFILE, JOB_SEARCH_LOG, OPPORTUNITIES, APPLICATION_TRACKER, PITCH_TEMPLATES, HIDDEN_GEMS, COMMUNITY_SIGNALS, AI_ASSISTED_WORK) |
| Money memory | `.bequite/money/` (MONEY_PROFILE, MONEY_SEARCH_LOG, OPPORTUNITIES, TRUST_CHECKS, ACTION_PLAN, HIDDEN_GEMS, COMMUNITY_SIGNALS, AI_ASSISTED_PATHS) |
| Version + update tracking | `.bequite/state/BEQUITE_VERSION.md`, `UPDATE_SOURCE.md`; `.bequite/logs/UPDATE_LOG.md`; `.bequite/backups/` |
| Memory-first doc | `docs/architecture/MEMORY_FIRST_BEHAVIOR.md` |
| Mode history (alpha.12) | `.bequite/state/MODE_HISTORY.md` |
| Delegate task pack (alpha.12) | `.bequite/tasks/DELEGATE_TASKS.md`, `DELEGATE_INSTRUCTIONS.md`, `DELEGATE_ACCEPTANCE_CRITERIA.md`, `DELEGATE_TEST_PLAN.md` |
| Delegate review report (alpha.12) | `.bequite/audits/DELEGATE_REVIEW_REPORT.md` |
| Presentation memory (alpha.13) | `.bequite/presentations/` (PRESENTATION_BRIEF, CONTENT_OUTLINE, SLIDE_PLAN, DESIGN_BRIEF, MOTION_PLAN, SPEAKER_NOTES, REFERENCES, PRESENTATION_VARIANTS_REPORT, EXPORT_LOG + assets/ + outputs/) |
| Skills (29) | `.claude/skills/bequite-*/SKILL.md` |
| Master frontend skill (alpha.17) | `.claude/skills/bequite-frontend-design-system/` (SKILL + references/ + examples/) |
| Design memory (alpha.17) | `.bequite/design/` (DESIGN_DNA, FRONTEND_SKILL_MAP, DESIGN_CONTINUITY_REPORT) |
| Frontend context summary (alpha.17) | `.bequite/state/FRONTEND_CONTEXT_SUMMARY.md` |
| Visual QA report (alpha.17) | `.bequite/audits/VISUAL_QA_REPORT.md` |
| Design Continuity Gate docs (alpha.17) | `docs/architecture/DESIGN_CONTINUITY_GATE.md` · `FRONTEND_CONTEXT_ENGINEERING.md` |
| Hooks (alpha.18, opt-in) | `.claude/hooks/*.{sh,ps1}` + `.claude/settings.json.example` (+ `.windows.`) ; strategy `docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md`; decision `docs/decisions/ADR-005-*.md` |
| Context engineering (alpha.18) | `bequite-context-engineer` skill · `docs/architecture/CONTEXT_ENGINEERING.md` · `.bequite/state/PROJECT_DNA.md` · `WORKING_NOTES.md` · `.bequite/plans/FILE_RESPONSIBILITY_MAP.md` |
| Anti-hallucination (alpha.18) | `bequite-anti-hallucination` skill |
| Harness/prompt authoring standard (alpha.18) | `docs/architecture/HARNESS_AND_PROMPT_QUALITY.md` |
| Game-changer feature report (alpha.18) | `docs/specs/GAME_CHANGER_FEATURES.md` (proposal only) |
| Public command reference | `commands.md` (repo root) |
| BeQuite memory | `.bequite/` |
| Workflow gate ledger | `.bequite/state/WORKFLOW_GATES.md` |
| Mode selector | `.bequite/state/CURRENT_MODE.md` |
| Phase selector | `.bequite/state/CURRENT_PHASE.md` |
| Project's own Memory Bank | `.bequite/memory/` (v2.x history, internal) |
| Direction reset audit (Cycle 1+2) | `.bequite/audits/DIRECTION_RESET_AUDIT.md` |
| GitHub-ready cleanup audit | `.bequite/audits/GITHUB_READY_CLEANUP_AUDIT.md` |
| Mistake memory | `.bequite/state/MISTAKE_MEMORY.md` |
| Assumptions | `.bequite/state/ASSUMPTIONS.md` |
| Feature expansion roadmap | `.bequite/plans/FEATURE_EXPANSION_ROADMAP.md` |
| Original brief | `BEQUITE_BOOTSTRAP_BRIEF.md` |
| Master file | `BeQuite_MASTER_PROJECT.md` |
| Install scripts | `scripts/install-bequite.{ps1,sh}` |
| ADR-001 (lightweight) | `docs/decisions/ADR-001-lightweight-skill-pack-first.md` |
| ADR-002 (mandatory gates) | `docs/decisions/ADR-002-mandatory-workflow-gates.md` |
| ADR-003 (tool neutrality) | `docs/decisions/ADR-003-tool-neutrality.md` |
| Auto-mode strategy | `docs/architecture/AUTO_MODE_STRATEGY.md` |
| UI/UX variants strategy | `docs/architecture/UIUX_VARIANTS_STRATEGY.md` |
| Live edit strategy | `docs/architecture/LIVE_EDIT_STRATEGY.md` |
| Tool neutrality principle | `.bequite/principles/TOOL_NEUTRALITY.md` |
| UI/UX memory | `.bequite/uiux/` (SECTION_MAP, LIVE_EDIT_LOG, UIUX_VARIANTS_REPORT, selected-variant, screenshots/) |
| Command catalog | `docs/specs/COMMAND_CATALOG.md` |
| Heavy-app ADRs (paused) | `.bequite/memory/decisions/ADR-008..016` |

---

## Core operating rules

1. **Tool neutrality.** Named tools are EXAMPLES, not commands. BeQuite must research, compare, justify, and choose the best tool for the current project instead of blindly using any named tool. See `.bequite/principles/TOOL_NEUTRALITY.md`.
2. **Never claim a task is "done" unless `/bq-verify` passes.**
3. **Always update `.bequite/logs/AGENT_LOG.md` when you take a real action.**
4. **Always update `.bequite/state/CURRENT_PHASE.md` when the workflow phase changes.**
5. **Always update `.bequite/state/WORKFLOW_GATES.md` when a gate is met.**
6. **Banned weasel words in completion reports:** should, probably, seems to, appears to, I think it works, might, hopefully, in theory. Replace with concrete verification or admit you didn't verify.
7. **Iron Law X:** every change ships in operationally complete state. No "feature added but needs restart."
8. **PhantomRaven defense:** never import a package without verifying it exists in the relevant registry in this session.
9. **Read before editing.** Use Read / Glob / Grep first; Edit only after.
10. **Inspect before assuming.** The `bequite-problem-solver` skill's "reproduce-first" discipline applies to every bug.
11. **No out-of-order commands.** If a command's required gates aren't met, refuse and suggest the prerequisite command.
12. **Do not auto-install dependencies.** No new deps, scraping tools, frontend libs, Docker, testing frameworks, deploy tools, monitoring, or auth libs added by default. Only when justified per the 10 decision questions.
13. **Every new BeQuite feature MUST follow the feature-addition workflow** (alpha.14). Even when the user provides a detailed spec inline. See `docs/architecture/WORKFLOW_GATES.md` § "Feature-addition workflow (alpha.14)" and `docs/runbooks/USING_BEQUITE_COMMANDS.md`. The 15 steps are:
    1. Add feature request to memory (`OPEN_QUESTIONS.md` or `FEATURE_EXPANSION_ROADMAP.md`)
    2. Run targeted research (`/bq-research` — minimum 3 dims for fast; 11 for deep) when feature touches a new domain
    3. Define scope (`/bq-scope` → `SCOPE.md`) — even one-pager
    4. Create plan (`/bq-plan` → `IMPLEMENTATION_PLAN.md`) — list files to create/modify
    5. Break into tasks (`/bq-assign` → `TASK_LIST.md`) when change touches > 5 files
    6. Implement command / skill / docs / memory
    7. Update README · 8. commands.md · 9. `/bequite` menu · 10. `/bq-help` · 11. `docs/specs/COMMAND_CATALOG.md`
    12. Update `.bequite/logs/AGENT_LOG.md` · 13. `docs/changelogs/CHANGELOG.md`
    14. Run `/bq-verify` post-implementation → `VERIFY_REPORT.md`
    15. Mark `BEQUITE_VERSION.md` + `LAST_RUN.md`
   Exemptions: hotfixes / doc-only changes can skip 2-5 but must still 6-15. Adding a skill that activates from an existing command can skip 2-5.
14. **BeQuite eats its own food** (alpha.14). Run periodic self-audits (this very rule was born from one). When discipline drift is detected, write an alignment audit before adding new features.
15. **Frontend quality promise** (alpha.17). Hero quality is not enough — **every visible section must meet the Design DNA.** For any frontend work: read/lock `.bequite/design/DESIGN_DNA.md` before coding, build section-by-section (build → check vs DNA → continue), and never claim a UI complete without a Design Continuity pass (`DESIGN_CONTINUITY_REPORT.md`) and a Visual QA pass (`VISUAL_QA_REPORT.md`). The master skill `bequite-frontend-design-system` owns this. See `docs/architecture/DESIGN_CONTINUITY_GATE.md` + `FRONTEND_CONTEXT_ENGINEERING.md`. This is a quality gate; it never bypasses the 17 hard human gates.

16. **Reliability discipline** (alpha.18 — context · evidence · anti-spaghetti · enforcement). Depth lives in skills on purpose — a bloated CLAUDE.md gets ignored (Anthropic). Keep this file lean; push detail to skills.
    - **Context:** persist state to files, not fading chat. Before a multi-step/multi-session task read `PROJECT_DNA.md` + the compact summary; re-read facts (don't trust ones buried mid-conversation); compact/clear/externalize at task boundaries; one task at a time. Critical must-not-forget facts go in **this file or auto-memory** — only those survive `/compact`. Put the most important instructions at the **top** of every file. See `bequite-context-engineer` + `docs/architecture/CONTEXT_ENGINEERING.md`.
    - **Evidence over claims:** never assert "done/works" — paste the command + exit code + output, or emit an explicit `UNVERIFIED:` / "I don't know". Every review/audit/red-team finding carries a `file:line` quote or is struck. Verify a package exists (registry + age + downloads + publisher + lockfile) before importing. See `bequite-anti-hallucination`.
    - **Anti-spaghetti:** `/bq-plan` emits a File-Responsibility Map before tasks; failing-test-first; smallest-safe-change + verify incrementally (no drive-by refactors); `/bq-review` runs spec-compliance **before** code-quality; new code matches `PROJECT_DNA.md`.
    - **Machine-enforcement:** the safety subset (destructive ops · secrets · weasel-word completion claims) ships as **opt-in** hooks (review before enabling — RCE-vector). See `docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md`.

### The 10 decision questions (apply before any major tool pick)

1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

**Do not say:** "Use X."
**Say:** "X is one candidate. Research and compare against other options. Use it only if it fits this project."

For each major pick: write a decision section (short for small projects; full ADR at `.bequite/decisions/ADR-XXX-<tool>-choice.md` for large / regulated projects). Format: Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan.

---

## The 6 modes

| Mode | Entry command | When to use |
|---|---|---|
| New Project | `/bq-new` | Empty folder, starting from scratch |
| Existing Project Audit | `/bq-existing` | Existing repo, audit what's there |
| Add Feature | `/bq-feature "title"` | Add one feature to existing project |
| Fix Problem | `/bq-fix` | Diagnose + repair a bug |
| Research Only | `/bq-mode research-only` | Just research; no code |
| Release Readiness | `/bq-mode release` | Pre-release verification + audit |

Active mode lives in `.bequite/state/CURRENT_MODE.md`.

---

## The 6 phases

| Phase | Name | Commands | Goal |
|---|---|---|---|
| P0 | Setup and Discovery | `/bq-init`, `/bq-mode`, `/bq-discover`, `/bq-doctor` | Learn what's there |
| P1 | Product Framing and Research | `/bq-clarify`, `/bq-research`, `/bq-scope`, `/bq-plan`, `/bq-multi-plan` | Decide what to build |
| P2 | Planning and Build | `/bq-assign`, `/bq-implement`, `/bq-feature`, `/bq-fix` | Build it |
| P3 | Quality and Review | `/bq-test`, `/bq-audit`, `/bq-review`, `/bq-red-team` | Confirm it works |
| P4 | Release | `/bq-verify`, `/bq-release`, `/bq-changelog` | Ship |
| P5 | Memory and Handoff | `/bq-memory`, `/bq-recover`, `/bq-handoff` | Continue / hand off |

Phase orchestrators: `/bq-p0` through `/bq-p5` (walk one phase in order). Autonomous: `/bq-auto` (walks all phases, pauses at hard gates).

---

## The 14 skills

7 baseline (existing):
- `bequite-frontend-quality` — UI quality + AI-slop detection
- `bequite-multi-model-planning` — manual-paste multi-model collaboration
- `bequite-problem-solver` — reproduce-first diagnostics
- `bequite-project-architect` — stack + ADR + scale-tier procedures
- `bequite-release-gate` — CI parity + semver + signing
- `bequite-scraping-automation` — Article VIII + polite mode
- `bequite-testing-gate` — test pyramid + coverage targets

7 specialist (new in v3.0.0-alpha.2):
- `bequite-researcher` — 11-dimension verified evidence
- `bequite-product-strategist` — JTBD + persona + MVP scoping
- `bequite-ux-ui-designer` — design principles + AI-slop anti-patterns
- `bequite-backend-architect` — API + async + caching + observability
- `bequite-database-architect` — schema + migrations + indexing
- `bequite-security-reviewer` — OWASP + supply-chain + secrets
- `bequite-devops-cloud` — CI/CD + deploys + safety gates

1 frontend live-edit (new in v3.0.0-alpha.4):
- `bequite-live-edit` — section-mapped frontend edits + browser inspection tiers

1 frontend master (new in v3.0.0-alpha.17):
- `bequite-frontend-design-system` — **master/coordinator**: owns Design DNA, the section-by-section build loop, the Design Continuity Gate, visual QA, and product-type rules. Coordinates `ux-ui-designer` (design), `frontend-quality` (slop detection), `live-edit` (section edits). Kills middle-section drift. (Total skills: 22 — this section's "14" header is historical.)

2 reliability/context (new in v3.0.0-alpha.18):
- `bequite-context-engineer` — **all-workflow context engineering**: compact/clear/externalize primitives, compaction-survival rule, `PROJECT_DNA.md` + `WORKING_NOTES.md`, session-orientation ritual, sub-agent isolation. Generalizes the frontend DNA/continuity win to backend/db/security/devops/testing.
- `bequite-anti-hallucination` — evidence-over-claims, citation-or-strike, in-session package verification, version-pinned API grounding, fresh-context adversarial verifier, `UNVERIFIED`/"I don't know" forced-fork.

(Plus the opportunity/creative/maintenance skills: `bequite-researcher`, `bequite-product-strategist`, `bequite-backend-architect`, `bequite-database-architect`, `bequite-security-reviewer`, `bequite-devops-cloud`, `bequite-workflow-advisor`, `bequite-job-finder`, `bequite-make-money`, `bequite-updater`, `bequite-delegate-planner`, `bequite-presentation-builder`.)

---

## Quick commands

```
/bequite                                    → gate-aware menu + recommended next 3
/bq-help                                    → full command reference
/bq-init                                    → initialize
/bq-mode                                    → select / show workflow mode
/bq-auto [intent] "task"                    → scoped autonomous runner (17 intents)
/bq-uiux-variants [N] "task"                → 1-10 isolated UI directions
/bq-live-edit "task"                        → section-by-section frontend edits
/bq-p0..p5                                  → walk one phase in order
/bq-verify                                  → full local verification
/bq-recover                                 → resume after session break
```

### `/bq-auto` intent types (17)

`new | existing | feature | fix | uiux | frontend | backend | database | security | testing | devops | scraping | automation | deploy | live-edit | variants | release`

Auto-mode continues by default — does NOT pause for "should I continue?" or "approve the plan?" Pauses only at hard human gates (see below).

For everything else, run `/bq-help` or `/bequite`.

---

## Required reads on every session start

(In order)

1. This `CLAUDE.md`
2. `.bequite/state/PROJECT_STATE.md`
3. `.bequite/state/CURRENT_MODE.md`
4. `.bequite/state/CURRENT_PHASE.md`
5. `.bequite/state/WORKFLOW_GATES.md`
6. `.bequite/state/LAST_RUN.md`
7. `.bequite/state/OPEN_QUESTIONS.md`
8. `.bequite/state/DECISIONS.md`
9. `.bequite/logs/AGENT_LOG.md` (last 5 entries)

If any of those are missing, run `/bq-init` first.

---

## Hard human gates (the only places /bq-auto pauses) — v3.0.0-alpha.4

Even in autonomous mode, the agent MUST pause for explicit user confirmation at:

1. **Destructive file deletion** (`rm -rf` on tracked code)
2. **Database migration against shared / production DBs**
3. **Production server change** (SSH, systemd, firewall on prod)
4. **VPS / Nginx / SSL change**
5. **Paid service activation** (new SaaS signup with payment)
6. **Secret / key handling** (rotation, generation)
7. **Changing auth / security model**
8. **Changing project architecture**
9. **Deleting old implementation** with active callers
10. **Scope contradiction** (task contradicts locked SCOPE.md)
11. **User explicit manual-approval** (`--manual-approval` or "stop and ask me")
12. **Cost ceiling reached**
13. **Wall-clock ceiling reached**
14. **Banned-weasel-word trip**
15. **3 consecutive failures on the same task**
16. **UI variant winner selection** (after `/bq-uiux-variants` finishes)
17. **Release `git push` / `git tag`** (always user-run)

Auto-mode does NOT pause after plan / scope / clarify if the intent is scoped — it continues autonomously per AUTO_MODE_STRATEGY.md.

---

## Doctrines that may be active

Per the project's `.bequite/state/DECISIONS.md`. Common ones:

- `default-web-saas` — UI rules (no Inter without recorded reason; tokens.css required; axe-core gate)
- `cli-tool` — semver discipline, exit codes, completions
- `ml-pipeline` — reproducible training, dataset versioning
- `desktop-tauri` — OS keychain (not Stronghold), notarytool, AzureSignTool
- `library-package` — public API freeze, semver-strict
- `fintech-pci` / `healthcare-hipaa` / `gov-fedramp` — regulated
- `ai-automation` — n8n / Make / Zapier discipline
- `mena-bilingual` — Arabic + RTL
- `mena-pdpl` / `eu-gdpr` — privacy compliance
- `vibe-defense` — extra-strict for vibe-handoff audience

The active Doctrine(s) are declared in `.bequite/state/DECISIONS.md`. If none declared, default to `default-web-saas` for web projects.

---

## When in doubt

- Iron Law beats Doctrine
- Doctrine beats convention
- Latest-verified-research beats memory
- Active session evidence beats memory of a previous run
- Run `/bequite` for orientation
- Refuse to run commands whose required gates aren't met

---

## History

BeQuite went through a v0.1.0 → v2.0.0-alpha.6 heavy-direction lineage (Studio + Docker + multi-app). That direction is **retired** (ADR-004 — "no heavy Studio or CLI in the GitHub-facing project"). Git history retains the heavy assets; the active main branch is lightweight-only.

The current MVP path is v3.0.0+ (lightweight command + skill pack with mandatory gates + tool neutrality). See ADR-001 (lightweight skill pack first), ADR-002 (mandatory workflow gates), ADR-003 (tool neutrality), ADR-004 (no heavy Studio or CLI).
