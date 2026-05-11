# BeQuite — Direction Reset Audit

This audit document is **append-only** within each reset cycle. The newest cycle is at the top.

---

## Cycle 2 — v3.0.0-alpha.2 — Gate system + modes + phase orchestrators (2026-05-11)

**Trigger:** User direction refinement. Previous reset (Cycle 1) established the lightweight skill pack but lacked **mandatory workflow gates**, **explicit modes**, and **phase orchestrators**. Users could still skip steps (run `/bq-implement` without `/bq-plan`). Research was thin (stack-only).

This cycle adds:

1. **Mandatory workflow gate system** at `.bequite/state/WORKFLOW_GATES.md`. Every command reads it on entry. Running a command out of order is blocked with a clear message + next-valid-command hint.
2. **Explicit modes** at `.bequite/state/CURRENT_MODE.md`. Six modes: New Project, Existing Project Audit, Add Feature, Fix Problem, Research Only, Release Readiness.
3. **Phase orchestrator commands** `/bq-p0` through `/bq-p5`. Each runs all the commands in its phase in order, guiding the user through.
4. **Auto-mode** `/bq-auto` — runs the full workflow autonomously but **stops at hard human gates** (mode selection, scope approval, multi-plan decision, implementation approval, deployment approval, destructive operations).
5. **Deep research** — `/bq-research` expanded from "stack-only" to **11 dimensions**: stack, product, competitors, failures, success patterns, user journeys, UX/UI, security, scalability, deployment/cloud, differentiation.
6. **Unbiased multi-model planning** — `/bq-multi-plan` generates external prompts that do NOT mention Claude's plan. The external model thinks from zero.
7. **Feature + Fix workflows with type routing** — `/bq-feature` (12 feature types) and `/bq-fix` (15 problem types) activate the relevant specialist skills.
8. **7 new specialist skills** — `bequite-researcher`, `bequite-product-strategist`, `bequite-ux-ui-designer`, `bequite-backend-architect`, `bequite-database-architect`, `bequite-security-reviewer`, `bequite-devops-cloud`.
9. **DevOps + cloud safety** — production server / database / deployment changes require explicit environment identification + backup plan + rollback plan + approval before destructive operations.

### Files added in this cycle

**New commands (10):**

- `.claude/commands/bq-mode.md` — select / display current mode
- `.claude/commands/bq-new.md` — New Project workflow entry
- `.claude/commands/bq-existing.md` — Existing Project Audit workflow entry
- `.claude/commands/bq-feature.md` — Add Feature workflow with type router
- `.claude/commands/bq-auto.md` — autonomous workflow runner with hard-gate pauses
- `.claude/commands/bq-p0.md` — Phase 0 orchestrator
- `.claude/commands/bq-p1.md` — Phase 1 orchestrator
- `.claude/commands/bq-p2.md` — Phase 2 orchestrator
- `.claude/commands/bq-p3.md` — Phase 3 orchestrator
- `.claude/commands/bq-p4.md` — Phase 4 orchestrator
- `.claude/commands/bq-p5.md` — Phase 5 orchestrator

Total commands: **24 (previous) + 10 (new) = 34**. Note: `bq-add-feature.md` from Cycle 1 is being superseded by `bq-feature.md` (richer, with type router).

**New skills (7):**

- `.claude/skills/bequite-researcher/SKILL.md`
- `.claude/skills/bequite-product-strategist/SKILL.md`
- `.claude/skills/bequite-ux-ui-designer/SKILL.md`
- `.claude/skills/bequite-backend-architect/SKILL.md`
- `.claude/skills/bequite-database-architect/SKILL.md`
- `.claude/skills/bequite-security-reviewer/SKILL.md`
- `.claude/skills/bequite-devops-cloud/SKILL.md`

Total skills: **7 (previous) + 7 (new) = 14**.

**New state files:**

- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/WORKFLOW_GATES.md`
- `.bequite/research/RESEARCH_REPORT.md` (template, moved from audits/)
- `.bequite/research/SOURCES.md` (template)
- `.bequite/handoff/HANDOFF.md` (template, moved from repo-root location)

**Updated commands (24 → richer template):**

Every existing command file gets these sections added if missing:

- Preconditions
- Required previous gates
- Quality gate
- Failure behavior

`bequite.md` root command — extended to read `WORKFLOW_GATES.md` and block invalid commands.

`bq-research.md` — rewritten with 11-dimension research procedure.

`bq-plan.md` — rewritten to consume the full research report + write a complete strategy.

`bq-multi-plan.md` — rewritten to generate **unbiased external prompts** (no mention of Claude's existing plan).

`bq-fix.md` — rewritten with 15 problem-type router that activates the right specialist skill.

**New docs:**

- `docs/decisions/ADR-001-lightweight-command-pack.md` (rename of existing ADR-001)
- `docs/decisions/ADR-002-mandatory-workflow-gates.md`
- `docs/decisions/ADR-003-research-before-planning.md`
- `docs/decisions/ADR-004-no-heavy-studio-or-cli.md`
- `docs/architecture/WORKFLOW_GATES.md`
- `docs/architecture/RESEARCH_DEPTH_STRATEGY.md`
- `docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md`
- `docs/architecture/FEATURE_AND_FIX_WORKFLOWS.md`
- `docs/architecture/DEVOPS_CLOUD_SAFETY.md`
- `docs/specs/COMMAND_CATALOG.md`

### Heavy-app status (UNCHANGED from Cycle 1)

Still **paused, not deleted** — same items:

- `studio/` (marketing + dashboard + api + brand)
- `docker-compose.yml`, `.dockerignore`, all `Dockerfile`s
- `tests/e2e/`
- `scripts/docker-up.{ps1,sh}`
- Root `package.json` + `Makefile`

No file is removed in this cycle. Deletion is still gated on explicit user approval.

### Heavy-CLI status (NEW classification)

The Python CLI (`cli/` v1.0.4) was previously "optional supplemental tool." This cycle re-classifies it as **paused, available later**:

- Reason: the lightweight slash-command surface now does everything the CLI did. Maintaining the CLI in parallel adds confusion.
- Status: stays on disk. README no longer leads with the CLI install path. Bootstrap script (`scripts/bootstrap.{ps1,sh}`) still works.
- Future: v3.x may revive the CLI as a thin wrapper that invokes the slash-command files. Out of scope here.

### Migration steps (from Cycle 1 to Cycle 2)

For a user who installed BeQuite via Cycle 1's `install-bequite.ps1`:

1. Re-run the installer with `-Force` (preserves `.bequite/` memory; overwrites `.claude/commands/` and `.claude/skills/`).
2. The new files appear; old memory is preserved.
3. `/bequite` now reads `WORKFLOW_GATES.md` — if absent, it suggests `/bq-init` to scaffold it.
4. Existing decisions in `DECISIONS.md` are still valid.

### What this audit does NOT decide

- Whether the heavy assets (`studio/`, `docker-compose.yml`, `tests/e2e/`) should be deleted from the repo. **Default: keep paused.**
- Whether the Python CLI gets removed from the repo. **Default: keep, but not in MVP path.**
- Whether to tag v3.0.0-alpha.2. **Pending user live-verification in Claude Code.**
- Whether to delete duplicate / superseded files (`.claude/commands/bq-add-feature.md` replaced by `bq-feature.md`). **Plan:** keep both for one release, deprecate `bq-add-feature` with a note.

---

## Cycle 1 — v3.0.0-alpha.1 — Lightweight skill pack first (2026-05-11)

**Trigger:** User direction change — "BeQuite = lightweight project skill pack + slash command pack. Not a big standalone app."

For roughly 48 hours BeQuite was built as a heavy standalone product:

- A Python CLI (v1.0.4) shipping 21+ subcommands
- A three-app Studio (`studio/marketing/`, `studio/dashboard/`, `studio/api/`) — Next.js 15 + Tailwind v4 + R3F + xterm.js + Hono on Bun
- Docker Compose orchestration
- Multi-stage Dockerfiles
- Bootstrap one-liner installers
- 24-test Playwright e2e suite

Audit cycle (v2.0.0-alpha.6) caught 14 install-path + UX bugs across 48 hours. Recurring pattern: **shipping without verifying from fresh clone**.

### Decision in Cycle 1

**BeQuite's MVP is a lightweight Claude Code skill pack** consisting of:

```
.claude/commands/        — 24 markdown slash commands (/bequite + /bq-*)
.claude/skills/          — 7 focused skills (bequite-*/SKILL.md)
.bequite/                — persistent project memory
scripts/install-bequite.{ps1,sh}  — light installer
```

### Files paused in Cycle 1 (NOT deleted)

- `studio/` (full)
- `docker-compose.yml`, all `Dockerfile`s, `.dockerignore`
- `tests/e2e/`
- `scripts/docker-up.{ps1,sh}`
- Root `package.json` + `Makefile`

### Files kept as optional in Cycle 1

- `cli/` — Python CLI v1.0.4 as optional supplemental tool
- `skill/` — source material library
- `template/`, `examples/`, `evidence/`, `prompts/`, `state/`, `.bequite/memory/` — historical

### Files added in Cycle 1

- `.claude/commands/*` × 24 — slash commands
- `.claude/skills/bequite-*/SKILL.md` × 7 — focused skills
- `.bequite/state/*.md` — template state files
- `.bequite/logs/*.md` — append-only logs
- `.bequite/{prompts,plans,tasks,audits}/` — directory scaffold
- `scripts/install-bequite.{ps1,sh}` — light installer
- Rewritten `README.md`, shortened `CLAUDE.md`
- `docs/decisions/ADR-001-lightweight-skill-pack-first.md`
- `docs/runbooks/{INSTALL_BEQUITE_IN_PROJECT,USING_BEQUITE_COMMANDS}.md`
- `docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md`
- `docs/specs/MVP_LIGHTWEIGHT_SCOPE.md`
- This audit file's first cycle

### Cycle 1 conclusion

Lightweight architecture established. Files structurally correct (YAML frontmatter validates; SKILL.md format matches Anthropic Skills spec). Live verification inside Claude Code deferred to user.

Commits: `215ed75` + `801b893` + `6ab2778`.

---

## Cumulative status (as of Cycle 2 end)

**Total commands:** 34 (24 from Cycle 1 + 10 new) plus the `bequite.md` root.
**Total skills:** 14 (7 from Cycle 1 + 7 new).
**Total ADRs:** 4 new in `docs/decisions/`, plus 9 historical in `.bequite/memory/decisions/`.
**Heavy assets paused:** `studio/`, Docker compose, tests/e2e, docker-up scripts, root package.json + Makefile.
**Heavy-CLI paused:** `cli/` (kept on disk, no longer in MVP path).

**Open user decisions:**

1. Tag v3.0.0-alpha.2 after live verification in Claude Code? (Default: yes if `/bequite` renders correctly inside Claude Code on a sample project.)
2. Delete heavy assets (`studio/`, etc.) from the repo? (Default: keep paused indefinitely.)
3. Remove `cli/` from the repo? (Default: keep paused.)
4. Decommission `.claude/commands/bq-add-feature.md` in favor of `bq-feature.md`? (Default: deprecate with note, remove next release.)
