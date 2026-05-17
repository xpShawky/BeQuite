# BeQuite Memory Index

> **Purpose:** Orient new contributors + the agent itself to what's in `.bequite/`. Read this on session start when you're unsure where to look.
>
> **Created:** alpha.15 (2026-05-17) per audit finding.

---

## Directory map

```
.bequite/
├── state/         live workflow state — read FIRST on session start
├── logs/          append-only history
├── audits/        discovery + doctor + audit + verify + red-team + alignment reports
├── plans/         implementation plans + scope + roadmap
├── tasks/         task lists + delegate task packs
├── principles/    tool neutrality + memory-first behavior
├── decisions/     project-level ADRs
├── uiux/          UI/UX work artifacts
├── jobs/          opportunity discovery memory (alpha.8)
├── money/         earning opportunity memory (alpha.8)
├── presentations/ creative + content workflows (alpha.13)
├── research/      domain research reports (system + per-feature)
├── prompts/       multi-model planning artifacts
├── backups/       safety backups from /bq-update
└── memory/        v2.x legacy memory bank (paused; kept for history)
```

---

## state/ — read first

| File | Purpose | Read it when |
|---|---|---|
| `PROJECT_STATE.md` | Project type + stack + summary | every session start |
| `CURRENT_MODE.md` | Active workflow mode (one of 6) | every command run |
| `CURRENT_PHASE.md` | Active phase (P0–P5) | every command run |
| `WORKFLOW_GATES.md` | Gate ledger (which gates are ✅/❌/⚪) | before any command that has required gates |
| `LAST_RUN.md` | Most recent command + outcome | every session start; before `/bq-recover` |
| `DECISIONS.md` | Running decision log | when an architectural question comes up |
| `OPEN_QUESTIONS.md` | Pending clarifications | before `/bq-clarify` |
| `ASSUMPTIONS.md` | Working assumptions | when planning or scoping |
| `MISTAKE_MEMORY.md` | Per-project mistake log + prevention rules | every session start (top 10–20 entries); during `/bq-fix`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`, `/bq-auto`, `/bq-live-edit` |
| `MODE_HISTORY.md` | Append-only mode usage tracker | `bequite-workflow-advisor` reads to recommend modes |
| `BEQUITE_VERSION.md` | Installed BeQuite version + update history | before `/bq-update` |
| `UPDATE_SOURCE.md` | Where to pull updates from | before `/bq-update` |

---

## logs/ — append-only history

| File | Purpose |
|---|---|
| `AGENT_LOG.md` | Every BeQuite command run (newest at top) |
| `CHANGELOG.md` | Internal changelog (some commands write `[Unreleased]` here) |
| `ERROR_LOG.md` | Bugs surfaced + root cause + fix |
| `UPDATE_LOG.md` | `/bq-update` runs |

> **Canonical changelog for releases:** `docs/changelogs/CHANGELOG.md` at repo root.

---

## audits/ — produced by audit commands

| File / pattern | Producer | Purpose |
|---|---|---|
| `DISCOVERY_REPORT.md` | `/bq-discover` | What's in the repo |
| `DOCTOR_REPORT.md` | `/bq-doctor` | Environment health |
| `FULL_PROJECT_AUDIT.md` | `/bq-audit` | 10-area project audit |
| `REVIEW-<date>.md` | `/bq-review` | Diff review |
| `RED_TEAM-<date>.md` | `/bq-red-team` | Adversarial review (8 angles) |
| `VERIFY_REPORT.md` | `/bq-verify` | Full gate matrix |
| `DIRECTION_RESET_AUDIT.md` | alpha.1 history | Direction reset rationale |
| `GITHUB_READY_CLEANUP_AUDIT.md` | alpha.5 history | Pre-GitHub cleanup |
| `DELEGATE_REVIEW_REPORT.md` | `/bq-review delegate` (alpha.12) | Phase-3 delegate verdict |
| `FULL_SYSTEM_ALIGNMENT_AUDIT.md` | alpha.14 audit | First system-alignment audit |
| `COMMAND_SKILL_CONSISTENCY_AUDIT.md` | alpha.14 audit | Per-file consistency |
| `WORKFLOW_GATE_AUDIT.md` | alpha.14 audit | Gate enforcement gaps |
| `FEATURE_WORKFLOW_AUDIT.md` | alpha.14 audit | Per-feature workflow trace |
| `COMMAND_CLUTTER_REVIEW.md` | alpha.14 audit | Keep/merge/deprecate decisions |
| `FINAL_SYSTEM_ALIGNMENT_REPORT.md` | alpha.14 audit | Final repair report |

---

## plans/ — produced by planning commands

| File | Producer | Purpose |
|---|---|---|
| `SCOPE.md` | `/bq-scope` | IN / OUT / NON-GOALS |
| `IMPLEMENTATION_PLAN.md` | `/bq-plan` | 15-section plan |
| `MERGED_IMPLEMENTATION_PLAN.md` | `/bq-multi-plan` | Multi-model merged plan |
| `FEATURE_EXPANSION_ROADMAP.md` | static | Future-feature roadmap |
| `feature-<slug>.md` | `/bq-feature` | Per-feature mini-spec |

---

## tasks/ — produced by /bq-assign + delegate commands

| File | Producer | Purpose |
|---|---|---|
| `TASK_LIST.md` | `/bq-assign` | Atomic task list |
| `CURRENT_TASK.md` | `/bq-implement` | Active task |
| `DELEGATE_TASKS.md` | `/bq-auto delegate` (alpha.12) | Task pack for cheap-model implementation |
| `DELEGATE_INSTRUCTIONS.md` | same | Per-task strong-model warnings + steps |
| `DELEGATE_ACCEPTANCE_CRITERIA.md` | same | Per-task observable pass/fail |
| `DELEGATE_TEST_PLAN.md` | same | Per-task test commands |

---

## principles/

| File | Purpose |
|---|---|
| `TOOL_NEUTRALITY.md` | The 10 decision questions; decision section format |

---

## decisions/

Project-level ADRs (architecture decisions specific to this BeQuite repo). Format: `ADR-XXX-<slug>.md`.

(For BeQuite-as-a-product ADRs — see `docs/decisions/` at repo root.)

---

## uiux/

| File | Purpose |
|---|---|
| `SECTION_MAP.md` | Visible section → source file map |
| `LIVE_EDIT_LOG.md` | Per-edit log (before/after) |
| `UIUX_VARIANTS_REPORT.md` | Generated variants + user pick |
| `selected-variant.md` | The winner after user picks |
| `screenshots/` | Browser screenshots (when available) |
| `archive/` | Older variants kept for reference |

---

## jobs/ + money/ (alpha.8 + alpha.10)

Lifestyle / opportunity memory. See `.bequite/jobs/JOB_PROFILE.md` and `.bequite/money/MONEY_PROFILE.md` for the templates.

---

## presentations/ (alpha.13)

Creative + content memory for `/bq-presentation`. 9 templates + `assets/` + `outputs/`.

---

## research/

Per-domain research reports produced by deep `/bq-research` or by `/bq-auto deep`. Reusable across sessions; cached to avoid re-fetching.

Files (alpha.14 onwards):
- `BEQUITE_SYSTEM_RESEARCH_REPORT.md` (alpha.14) — research on BeQuite's own design choices

Future research reports will follow `<DOMAIN>_RESEARCH_REPORT.md` naming.

---

## prompts/

| Subdir | Purpose |
|---|---|
| `user_prompts/` | Original user prompts (when worth preserving) |
| `generated_prompts/` | Multi-model prompts BeQuite generates |
| `model_outputs/` | Pasted-back outputs from external models |

---

## backups/

Created by `/bq-update`. Timestamped snapshots of `.claude/commands/` and `.claude/skills/` before any update.

---

## memory/ (legacy)

v2.x heavy-direction memory bank (Constitution, Doctrines, ADRs 008–016). **Paused** per ADR-001. Kept for history; not loaded by current commands.

---

## Memory-first rule (alpha.10+)

Every action-taking command should:
1. Read core state files (`PROJECT_STATE.md`, `CURRENT_MODE.md`, `CURRENT_PHASE.md`, `WORKFLOW_GATES.md`, `LAST_RUN.md`)
2. Read situational files (`DECISIONS.md`, `OPEN_QUESTIONS.md`, `MISTAKE_MEMORY.md`) when relevant
3. Skip per-domain memory unless the task touches it (e.g. don't load `.bequite/jobs/*` for a code fix)

Full discipline: `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`.

---

## When you don't know where to look

1. Run `/bequite` → gate-aware menu with state summary
2. Run `/bq-now` → one-line orientation
3. Run `/bq-recover` → reads everything; finds last green checkpoint
4. Open this file (`MEMORY_INDEX.md`) for the directory map

---

## Maintainer note

When adding a new memory file or directory, update this index in the same commit. Drift here defeats the purpose.
