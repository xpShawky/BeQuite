# Workflow gates strategy

**Status:** active
**Adopted:** 2026-05-11 (ADR-002)
**Updated:** 2026-05-12 (alpha.4 added UI variant + release gates → 17 hard human gates in `/bq-auto`); 2026-05-17 (alpha.14 added Feature-addition workflow rule + gate aliases + orthogonal workflows section)
**Reference:** ADR-002, AUTO_MODE_STRATEGY.md, COMMAND_CATALOG.md

---

## Feature-addition workflow (alpha.14 — global rule)

> **Every new BeQuite feature MUST follow this 15-step workflow.** Even when the user provides a detailed spec inline. The agent must not shortcut to implementation.

| Step | Action | Output |
|---|---|---|
| 1 | Add feature request to memory | `OPEN_QUESTIONS.md` or `FEATURE_EXPANSION_ROADMAP.md` |
| 2 | Run targeted research when feature touches a new domain | `.bequite/research/<DOMAIN>_RESEARCH_REPORT.md` (min 3 dims for fast; 11 for deep) |
| 3 | Define scope | `SCOPE.md` — IN / OUT / NON-GOALS |
| 4 | Create plan | `IMPLEMENTATION_PLAN.md` — files to create/modify, decisions, risks |
| 5 | Break into tasks (when > 5 files) | `TASK_LIST.md` |
| 6 | Implement command / skill / docs / memory | source files |
| 7 | Update README | docs |
| 8 | Update `commands.md` | docs |
| 9 | Update `/bequite` root menu | `.claude/commands/bequite.md` |
| 10 | Update `/bq-help` | `.claude/commands/bq-help.md` |
| 11 | Update `.claude/bequite/docs/specs/COMMAND_CATALOG.md` | docs |
| 12 | Update `.bequite/logs/AGENT_LOG.md` | log |
| 13 | Update `docs/changelogs/CHANGELOG.md` | log |
| 14 | Run `/bq-verify` post-implementation | `VERIFY_REPORT.md` |
| 15 | Bump `BEQUITE_VERSION.md` + update `LAST_RUN.md` | state |

**Exemptions:**
- **Hotfixes** can skip steps 2-5 but must still 6-15
- **Doc-only changes** can skip 2-5
- **Adding a skill** that activates only via an existing command can skip 2-5 (but must scope what the skill does)

**Why this rule exists:** alpha.13's Presentation Builder shipped without going through discover→research→scope→plan→tasks. The output was solid, but the discipline was wrong. alpha.14 codifies the rule. See `.bequite/audits/FEATURE_WORKFLOW_AUDIT.md` for the precedent.

---

## One name per gate

Each gate has exactly one name: the one in the project ledger (`templates/bequite/state/WORKFLOW_GATES.md`) or in the work template (`templates/bequite/work/_template/gates.md`). `scripts/bq_check.py` fails on any other spelling.

---

## Orthogonal workflows (alpha.14 — don't change mode)

The following commands operate **outside the 6 dev lifecycle modes**. They don't advance phase, don't set mode, don't require phase-gates beyond `BEQUITE_INITIALIZED`:

- `/bq-presentation` — creative + content (PPTX / HTML / variants)
- `/bq-job-finder` — opportunity discovery
- `/bq-make-money` — earning discovery
- `/bq-suggest` — workflow advisor (read-only)
- `/bequite short` — orientation (read-only)
- `/bq-explain` — explainer (read-only)
- `/bq-help` — reference (read-only)
- `/bq-update` — BeQuite self-maintenance

If you're mid-implementation in `Add Feature` mode and you run `/bq-presentation`, the system stays in `Add Feature` mode. The presentation workflow runs in parallel + writes to its own memory folder (`.bequite/presentations/`).

---

---

## What gates are

Workflow gates are **named conditions** tracked in `.bequite/state/WORKFLOW_GATES.md` that determine when a command can run.

States:
- `✅ done` — gate is met
- `❌ pending` — gate not yet met
- `⚪ optional` — gate is optional; can be skipped
- `[!] blocked` — gate cannot be met (blocker found; needs resolution)

## How gates work

Every BeQuite command declares:

- **Required previous gates** — gates that must be `✅` before the command runs
- **Quality gate** — gates the command marks `✅` on successful completion

When a user invokes a command whose required gates aren't met, the command **refuses** and tells the user which gate is missing + suggests the prerequisite command.

Example:
```
You:      /bq-implement
BeQuite:  Blocked — PLAN_APPROVED is ❌ pending.
          Run /bq-plan first.
```

## The gates

The list lives in one place: project gates in the ledger (`templates/bequite/state/WORKFLOW_GATES.md`), per-work gates in `templates/bequite/work/_template/gates.md`. Phases: P0 setup and discovery, P1 framing and research, P2 build, P3 quality and review, P4 release, P5 memory and handoff. The design-continuity gates apply only when a frontend exists ([`DESIGN_CONTINUITY_GATE.md`](DESIGN_CONTINUITY_GATE.md)); creative work adds the motion gates in the work template.

## Mode-specific overrides

Not every gate applies to every mode:

| Mode | Required P0 | Required P1 | Required P2 | Required P3 | Required P4 | Required P5 |
|---|---|---|---|---|---|---|
| New Project | All | All | All | All | All | All |
| Existing Audit | All | CLARIFY + RESEARCH | (none; audit only) | TEST + REVIEW | (none) | MEMORY_SNAPSHOT |
| Add Feature | BEQUITE + MODE | (none; self-contained) | FEATURE_TESTED | TEST + REVIEW | (optional) | MEMORY_SNAPSHOT |
| Fix Problem | BEQUITE + MODE | (none; reproduce-first) | FIX_VERIFIED | TEST + REVIEW | (optional) | MEMORY_SNAPSHOT |
| Research Only | BEQUITE + MODE | CLARIFY + RESEARCH | (none) | (none) | (none) | MEMORY_SNAPSHOT |
| Release Readiness | BEQUITE + MODE | (none) | (none) | All + AUDIT | All | MEMORY_SNAPSHOT |

## Hard human gates (auto-mode only)

`/bq-auto` adds 17 hard human gates on top of workflow gates. These are places auto-mode **must pause** for explicit user confirmation:

1. Destructive file deletion
2. Database migration against shared/prod DBs
3. Production server change
4. VPS / Nginx / SSL change
5. Paid service activation
6. Secret / key handling
7. Changing auth/security model
8. Changing project architecture
9. Deleting old implementation with active callers
10. Scope contradiction
11. User explicit manual-approval request
12. Cost ceiling reached
13. Wall-clock ceiling reached
14. Banned-weasel-word trip
15. 3 consecutive failures on the same task
16. UI variant winner selection (after `/bq-uiux-variants`)
17. Release `git push` / `git tag`

See [`AUTO_MODE_STRATEGY.md`](AUTO_MODE_STRATEGY.md) for full discussion.

## How gates are updated

Every command's spec lists which gates it updates. The updates happen atomically on successful completion. Failed commands don't update gates.

The agent re-reads `.bequite/state/WORKFLOW_GATES.md` at the start of every command to determine eligibility.

## Resume after break

When `/bq-recover` runs, it reads the gate ledger to find the last green checkpoint and recommend the next safe step.

## Anti-patterns

- ❌ Manually editing `WORKFLOW_GATES.md` to mark gates `✅` without running the command
- ❌ Adding new gates without documenting in this file + ADR-002
- ❌ Treating optional gates as required (or vice versa)
- ❌ Skipping gates with `--force` flags (those don't exist; gates are non-negotiable)

## See also

- ADR-002 — the decision to introduce mandatory gates
- COMMAND_CATALOG.md — which gates each command requires + sets
- AUTO_MODE_STRATEGY.md — hard human gates in `/bq-auto`
