# GitHub-Ready Cleanup Audit

**Generated:** 2026-05-12
**Purpose:** kill the old Studio / heavy CLI / TUI direction from the GitHub-facing project. Make the repo clean, lightweight, impressive. Polish README.

---

## 1. Current repo structure (top level)

```
.bequite/                  ← lightweight memory (KEEP — heart of BeQuite)
.claude/                   ← commands + skills (KEEP — heart of BeQuite)
.commitlintrc.json         ← was for heavy CLI commit-hooks (REMOVE)
.dockerignore              ← heavy direction (REMOVE)
.env.example               ← was for Studio environment (REMOVE)
.git, .github, .gitignore  ← KEEP
AGENTS.md                  ← AGENTS.md schema for future (KEEP minimal; rewrite to point at .claude/)
BEQUITE_BOOTSTRAP_BRIEF.md (35KB)   ← historical brief (KEEP — useful context)
BeQuite_MASTER_PROJECT.md  (49KB)   ← historical (ARCHIVE → docs/legacy/)
CHANGELOG.md              (148KB!)  ← bloated heavy-CLI changelog (ARCHIVE → docs/legacy/CHANGELOG-legacy.md; create new lightweight CHANGELOG.md)
CLAUDE.md                  ← KEEP (rewrite to drop "two-track history" framing)
LICENSE, README.md         ← KEEP (README full rewrite)
Makefile                   ← for heavy CLI/Studio (REMOVE)
cli/                       ← Python CLI (REMOVE — git history preserves)
docker-compose.yml         ← Studio Docker (REMOVE)
docs/                      ← KEEP (active docs; add 6 missing files)
evidence/                  ← heavy-direction evidence files (ARCHIVE → docs/legacy/evidence/ OR REMOVE)
examples/                  ← was for heavy direction (REMOVE — empty/stale)
package.json               ← root npm for heavy CLI (REMOVE)
prompts/                   ← top-level prompts dir (different from .bequite/prompts/) — likely heavy artifacts (REMOVE if duplicated; otherwise ARCHIVE)
scripts/                   ← MIXED:
  install-bequite.{ps1,sh} ← KEEP (lightweight installer)
  bootstrap.{ps1,sh}       ← REMOVE (heavy Python CLI bootstrap)
  install.{ps1,sh}         ← REMOVE (heavy Python CLI install)
  docker-up.{ps1,sh}       ← REMOVE (Studio Docker)
skill/                     ← top-level "skill" dir (NOT .claude/skills/) — heavy-direction (REMOVE)
state/                     ← top-level "state" dir (NOT .bequite/state/) — heavy-direction (REMOVE)
studio/                    ← Studio Next.js app (REMOVE — large, fully retired)
template/                  ← project template for heavy direction (REMOVE)
tests/                     ← heavy-direction tests/e2e/ (REMOVE)
```

---

## 2. Files that support lightweight BeQuite (KEEP)

| Path | Why |
|---|---|
| `.bequite/` (entire tree) | Persistent memory — heart of BeQuite |
| `.claude/commands/` (36 files) | Slash command pack |
| `.claude/skills/` (15 dirs) | Specialist skills |
| `.git`, `.github/`, `.gitignore` | Version control + GitHub config |
| `CLAUDE.md` | Operating instructions (rewrite to drop "paused" framing) |
| `LICENSE` | MIT license |
| `README.md` | (rewrite — see §6) |
| `BEQUITE_BOOTSTRAP_BRIEF.md` | Historical context — keep as reference |
| `docs/architecture/` (existing 6 + 4 missing) | Architecture docs |
| `docs/decisions/` (existing 3 ADRs + ADR-004) | Decision records |
| `docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md` | Install guide |
| `docs/runbooks/USING_BEQUITE_COMMANDS.md` | Usage guide |
| `docs/specs/COMMAND_CATALOG.md` | Command catalog |
| `docs/specs/MVP_LIGHTWEIGHT_SCOPE.md` | MVP scope |
| `docs/changelogs/AGENT_LOG.md` | Agent log (carry forward) |
| `scripts/install-bequite.{ps1,sh}` | Lightweight installer |

---

## 3. Files that belong to old Studio direction (REMOVE)

| Path | Size | Why |
|---|---|---|
| `studio/` | ~MB | Next.js marketing + dashboard + Hono API |
| `docker-compose.yml` | 3 KB | Studio Docker orchestration |
| `.dockerignore` | 1 KB | Docker-only |
| `tests/e2e/` (inside `tests/`) | ~KB | Studio Playwright tests |
| `scripts/docker-up.ps1` / `docker-up.sh` | – | Studio dev runner |
| `template/` | – | Studio project template |
| `.env.example` | 4 KB | Studio env template |
| `evidence/` | – | Heavy-direction screenshot/proof folder |

---

## 4. Files that belong to old heavy CLI/TUI direction (REMOVE)

| Path | Why |
|---|---|
| `cli/` | Python CLI app (Hatchling + Click + Rich) |
| `Makefile` | CLI build commands |
| `package.json` | Root npm for CLI/Studio scripts |
| `scripts/bootstrap.ps1` / `bootstrap.sh` | Python CLI bootstrap (curl/iex) |
| `scripts/install.ps1` / `install.sh` | Python CLI installer |
| `.commitlintrc.json` | Commit hooks for CLI dev |
| `docs/runbooks/LOCAL_DEV.md` | If it documents Python CLI / Studio dev |
| `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md` | CLI auth design |
| `docs/specs/MULTI_MODEL_PLANNING_REQUIREMENTS.md` | If it references CLI architecture (verify; may keep) |

---

## 5. Files to archive (keep on disk under `docs/legacy/`)

| Path | Move to |
|---|---|
| `BeQuite_MASTER_PROJECT.md` | `docs/legacy/MASTER_PROJECT.md` |
| `CHANGELOG.md` (148KB heavy history) | `docs/legacy/CHANGELOG-legacy.md` |
| `.bequite/memory/` (v2.x Memory Bank with decisions/ADR-008..016) | Stays at `.bequite/memory/` — internal, not in public docs |

(Optional: archive `prompts/`, `state/`, `skill/` top-level dirs if they're not pure duplicates of `.bequite/...`)

---

## 6. README gaps (full rewrite needed)

Current README.md (220 lines):

| Gap | Current state | Required |
|---|---|---|
| Hero/logo | Plain `# BeQuite` heading | Logo / wordmark / clear tagline |
| Studio framing | Section "Why a skill pack instead of a dashboard" mentions Studio | REMOVE all Studio references from public docs |
| Heavy CLI framing | Section "Optional: the BeQuite Python CLI" | REMOVE entirely |
| Mentions 24 commands | Out of date (now 36) | Update to 36 |
| Mentions 7 skills | Out of date (now 15) | Update to 15 |
| Phase 0-5 names | "Setup and Understanding", "Problem Framing"... | Match current: Setup and Discovery / Product Framing and Research / Planning and Build / Quality and Review / Release / Memory and Handoff |
| Beginner section | Missing | Add "I have a new project / existing project / want a feature / want a fix / want UI" |
| Advanced section | Missing | Add "Auto mode / phase orchestrators / scoped auto / variants / live edit / red-team / multi-plan / mistake memory / handoff" |
| Workflow gates | Mentioned but not detailed | Add explicit gate-prevents-skipping explanation |
| Examples | Old `/bq-add-feature` shown | Update to current commands + intent-scoped `/bq-auto` |
| Mistake memory | Not mentioned | Add (new feature) |
| Roadmap | Missing | Add MVP / V1 / V2 |
| What BeQuite is NOT | Missing | Add explicit anti-pattern list |
| Version label | Missing | Add v3.0.0-alpha.4 + previous |

---

## 7. Docs gaps

Existing:
- ✓ `docs/architecture/LIGHTWEIGHT_SKILL_PACK_ARCHITECTURE.md`
- ✓ `docs/architecture/MULTI_MODEL_PLANNING_STRATEGY.md`
- ✓ `docs/architecture/AUTO_MODE_STRATEGY.md` (alpha.4)
- ✓ `docs/architecture/UIUX_VARIANTS_STRATEGY.md` (alpha.4)
- ✓ `docs/architecture/LIVE_EDIT_STRATEGY.md` (alpha.4)
- ✓ `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md` (← REMOVE — heavy CLI)
- ✓ `docs/decisions/ADR-001-lightweight-skill-pack-first.md`
- ✓ `docs/decisions/ADR-002-mandatory-workflow-gates.md`
- ✓ `docs/decisions/ADR-003-tool-neutrality.md`
- ✓ `docs/specs/COMMAND_CATALOG.md`
- ✓ `docs/specs/MVP_LIGHTWEIGHT_SCOPE.md`
- ✓ `docs/specs/MULTI_MODEL_PLANNING_REQUIREMENTS.md`
- ✓ `docs/runbooks/INSTALL_BEQUITE_IN_PROJECT.md`
- ✓ `docs/runbooks/USING_BEQUITE_COMMANDS.md`
- ✓ `docs/runbooks/LOCAL_DEV.md` (← REMOVE if CLI/Studio-specific)
- ✓ `docs/changelogs/AGENT_LOG.md`

Missing (create this cycle):
- ❌ `docs/architecture/WORKFLOW_GATES.md`
- ❌ `docs/architecture/RESEARCH_DEPTH_STRATEGY.md`
- ❌ `docs/architecture/FEATURE_AND_FIX_WORKFLOWS.md`
- ❌ `docs/architecture/DEVOPS_CLOUD_SAFETY.md`
- ❌ `docs/decisions/ADR-004-no-heavy-studio-or-cli.md`
- ❌ `docs/changelogs/CHANGELOG.md` (lightweight, replacing 148KB legacy)

---

## 8. Slash command gaps

All 36 commands exist. Verified in registry.

Two have new template sections (Preconditions / Required gates / Quality gate / Failure behavior); 20 alpha.1 commands still lack the new template — tracked as alpha.5 work.

Two commands lack Mistake Memory integration:
- `/bq-fix`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`, `/bq-auto`, `/bq-live-edit` → should append to `.bequite/state/MISTAKE_MEMORY.md` when they detect a repeated mistake pattern

---

## 9. Skill gaps

All 15 skills exist. Tool-neutrality block (alpha.3) applied to 11; the other 4 (problem-solver, product-strategist, multi-model-planning, live-edit) inherit from their command-level reference but should get explicit tool-neutrality blocks in a future pass.

---

## 10. Workflow gate gaps

Gates exist in `.bequite/state/WORKFLOW_GATES.md`. Each command's "Required previous gates" section references them. Working as designed.

Mistake-memory commands list (above) needs writes wired to the new `.bequite/state/MISTAKE_MEMORY.md`.

---

## 11. Memory update gaps

Existing memory:
- ✓ `.bequite/state/PROJECT_STATE.md`
- ✓ `.bequite/state/CURRENT_MODE.md`
- ✓ `.bequite/state/CURRENT_PHASE.md`
- ✓ `.bequite/state/WORKFLOW_GATES.md`
- ✓ `.bequite/state/LAST_RUN.md`
- ✓ `.bequite/state/DECISIONS.md`
- ✓ `.bequite/state/OPEN_QUESTIONS.md`

Missing (create this cycle):
- ❌ `.bequite/state/MISTAKE_MEMORY.md`
- ❌ `.bequite/state/ASSUMPTIONS.md`
- ❌ `.bequite/plans/FEATURE_EXPANSION_ROADMAP.md`

---

## 12. Final cleanup plan

### Phase A — Non-destructive (this cycle)

1. Write this audit
2. Rewrite `README.md` from scratch (12 sections per spec)
3. Update `CLAUDE.md` (drop "two-track history" framing; reference clean direction only)
4. Create `docs/decisions/ADR-004-no-heavy-studio-or-cli.md`
5. Create `.bequite/state/MISTAKE_MEMORY.md` template
6. Create `.bequite/state/ASSUMPTIONS.md` template
7. Create `.bequite/plans/FEATURE_EXPANSION_ROADMAP.md`
8. Create 4 missing architecture docs (WORKFLOW_GATES, RESEARCH_DEPTH_STRATEGY, FEATURE_AND_FIX_WORKFLOWS, DEVOPS_CLOUD_SAFETY)
9. Create `docs/changelogs/CHANGELOG.md` (lightweight)
10. Update logs (`.bequite/logs/AGENT_LOG.md`, `.bequite/logs/CHANGELOG.md`)
11. Commit + push the non-destructive changes

### Phase B — Destructive (PAUSE FOR USER AUTHORIZATION)

⏸ **HARD HUMAN GATE: destructive file deletion**

I will not `git rm` any of these without explicit user OK. Here's the proposed deletion list:

#### Heavy-direction folders (entire tree)
- `studio/`
- `cli/`
- `tests/` (heavy-direction; if you want to keep generic test scaffolding, say so)
- `template/`
- `evidence/`
- `examples/`
- `prompts/` (top-level; `.bequite/prompts/` stays)
- `state/` (top-level; `.bequite/state/` stays)
- `skill/` (top-level; `.claude/skills/` stays)

#### Heavy-direction files
- `docker-compose.yml`
- `.dockerignore`
- `.env.example`
- `Makefile`
- `package.json` (root — for CLI/Studio scripts)
- `.commitlintrc.json`
- `scripts/docker-up.ps1`, `scripts/docker-up.sh`
- `scripts/bootstrap.ps1`, `scripts/bootstrap.sh`
- `scripts/install.ps1`, `scripts/install.sh`
- `docs/architecture/CLI_AUTHENTICATION_STRATEGY.md`
- `docs/runbooks/LOCAL_DEV.md`

#### Heavy-direction files to archive (move, not delete)
- `BeQuite_MASTER_PROJECT.md` → `docs/legacy/MASTER_PROJECT.md`
- `CHANGELOG.md` (148KB) → `docs/legacy/CHANGELOG-legacy.md` (replace with slim `CHANGELOG.md` pointing at `docs/changelogs/CHANGELOG.md`)

#### Keep with caveat
- `BEQUITE_BOOTSTRAP_BRIEF.md` (35KB) — historical context; KEEP at root for now (could move to `docs/legacy/` later)
- `.bequite/memory/` — internal Memory Bank from v2.x; KEEP (referenced by ADRs)
- `.github/` — workflow CI; verify it doesn't run heavy-CLI tasks (if it does, simplify)
- `AGENTS.md` — rewrite to be a minimal pointer to `.claude/`

### Phase C — Final commit + push (after user OK on Phase B)

12. Commit destructive cleanup
13. Tag (optional) v3.0.0-alpha.5
14. Push

---

## 13. After cleanup — repo size estimate

Before: ~MB tracked (much in `studio/`, `cli/`)
After: ~MB tracked (lightweight skill pack + docs)
Tracked files before: 484
Tracked files after: ~150-200

---

## 14. Risks

| Risk | Mitigation |
|---|---|
| Deleting `studio/` loses code someone might want | Git history retains it on the previous commit; user can `git checkout v3.0.0-alpha.4 -- studio/` if needed |
| Deleting `cli/` breaks an external user's CI | We never published the CLI; no external dependency |
| `.github/` workflows may still reference removed paths | Audit `.github/workflows/` after Phase B; fix any path references |
| Bootstrap scripts may be linked from old README | Old README is rewritten this cycle; no stale links |
| Branch protection on `main` may block force-cleanup | Use normal commits, not force-push |

---

## 15. What this audit is NOT

- It's not the cleanup itself — destructive ops pause for user OK
- It's not a release — alpha.5 is proposed but not auto-tagged
- It's not a guarantee that all dependencies are removed — verify after Phase B by running `/bq-doctor` on a fresh clone
