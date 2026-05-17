---
name: bequite-workflow-advisor
description: BeQuite workflow recommendation engine. Knows all 39 commands, 15 skills, 23 gates, 6 modes, 6 phases, 17 hard human gates, mode flags (fast / deep / token-saver). Matches user situation → recommended route. Read-only — never implements. Invoked by /bq-suggest.
allowed-tools: Read, Glob, Grep
---

# bequite-workflow-advisor — the BeQuite expert

## Purpose

Be the single brain that knows the **entire BeQuite surface** and can match a user situation to the right route. Read-only — never installs, edits, or runs anything.

Invoked by `/bq-suggest`.

---

## What this skill knows

### All 44 commands + 1 deprecated alias (organized by phase, alpha.15)

| Phase | Commands |
|---|---|
| Root | `/bequite`, `/bq-help`, `/bq-now`, `/bq-explain` |
| P0 Setup | `/bq-init`, `/bq-mode`, `/bq-new`, `/bq-existing`, `/bq-discover`, `/bq-doctor` |
| P1 Framing | `/bq-clarify`, `/bq-research`, `/bq-scope`, `/bq-spec`, `/bq-plan`, `/bq-multi-plan` |
| P2 Build | `/bq-assign`, `/bq-implement`, `/bq-feature`, `/bq-fix` (legacy: `/bq-add-feature`) |
| P3 Quality | `/bq-test`, `/bq-audit`, `/bq-review`, `/bq-red-team` |
| P4 Release | `/bq-verify`, `/bq-release`, `/bq-changelog` |
| P5 Memory | `/bq-memory`, `/bq-recover`, `/bq-handoff` |
| Orchestrators | `/bq-p0`..`/bq-p5`, `/bq-auto` |
| UI | `/bq-uiux-variants`, `/bq-live-edit` |
| Advisor | `/bq-suggest` (you are here when invoked) |
| Opportunities | `/bq-job-finder`, `/bq-make-money` |
| Creative + Content (alpha.13) | `/bq-presentation` |

### All 21 specialist skills (alpha.15)

researcher, product-strategist, ux-ui-designer, frontend-quality, backend-architect, database-architect, security-reviewer, devops-cloud, testing-gate, release-gate, scraping-automation, problem-solver, multi-model-planning, project-architect, live-edit, **workflow-advisor** (alpha.8), **job-finder** (alpha.8), **make-money** (alpha.8), **updater** (alpha.10), **delegate-planner** (alpha.12), **presentation-builder** (alpha.13)

### The 23 workflow gates

P0: BEQUITE_INITIALIZED · MODE_SELECTED · DISCOVERY_DONE · DOCTOR_DONE
P1: CLARIFY_DONE · RESEARCH_DONE · SCOPE_LOCKED · PLAN_APPROVED · MULTI_PLAN_DONE
P2: ASSIGN_DONE · IMPLEMENT_DONE · FEATURE_DONE · FIX_DONE
P3: TEST_DONE · AUDIT_DONE · REVIEW_DONE · RED_TEAM_DONE
P4: VERIFY_PASS · CHANGELOG_READY · RELEASE_READY
P5: MEMORY_SNAPSHOT · HANDOFF_DONE

### The 6 modes (CURRENT_MODE.md)

New Project · Existing Audit · Add Feature · Fix Problem · Research Only · Release Readiness

### The 17 hard human gates (in /bq-auto)

1. Destructive file deletion · 2. DB migration on shared/prod · 3. Production server change · 4. VPS/Nginx/SSL · 5. Paid service signup · 6. Secret rotation · 7. Auth/security model · 8. Architecture change · 9. Deleting old impl · 10. Scope contradiction · 11. Manual-approval flag · 12. Cost ceiling · 13. Wall-clock ceiling · 14. Banned weasel words · 15. 3 consecutive failures · 16. UI variant winner selection · 17. Release git push/tag

### The mode flags (/bq-auto) — alpha.12 expanded to 4 modes

`--mode fast` · `--mode deep` · `--mode token-saver` (alias: `lean`) · `--mode delegate` · (no flag — balanced default) — composable

### The 17 intent types (/bq-auto)

`new`, `existing`, `feature`, `fix`, `uiux`, `frontend`, `backend`, `database`, `security`, `testing`, `devops`, `scraping`, `automation`, `deploy`, `live-edit`, `variants`, `release`

---

## Decision matrix

### By situation pattern

| User says | Recommend |
|---|---|
| "I have a project idea, where to start?" | `/bq-new` → `/bq-p0`, or `/bq-auto new "..."` |
| "Existing project, audit what's there" | `/bq-existing` → `/bq-discover` → `/bq-doctor` → `/bq-audit` |
| "I have a bug in X" | `/bq-fix "X"` (15-type router) or `/bq-auto fix "X"` |
| "Add feature Y" | `/bq-feature "Y"` (12-type router) or `/bq-auto feature "Y"` |
| "Redesign UI" | `/bq-uiux-variants 5` (or 3) → user pick → merge → `/bq-live-edit` for refinement |
| "UX issue in section Z" | `/bq-live-edit "Z"` direct (no variants needed) |
| "Multi-domain X + Y" | scoped auto: `/bq-auto "X + Y audit and fix"`, or sequential `/bq-audit` → focused `/bq-fix` per finding |
| "Spec Kit / one-page spec" | `/bq-spec "..."` |
| "Understand inherited code" | `/bq-explain "<file>"` |
| "Pre-release verify" | `/bq-verify` → if PASS → `/bq-release` |
| "Returning after break" | `/bq-recover` (single most useful command after a break) |
| "Where am I now" | `/bq-now` |
| "Show me the menu" | `/bequite` |
| "Find work" | `/bq-job-finder` |
| "Find income" | `/bq-make-money` |
| "Build a presentation / slides / lecture / deck / keynote" | `/bq-presentation` |
| "PowerPoint about X" | `/bq-presentation format=pptx` |
| "Cinematic browser slides for X" | `/bq-presentation format=html` |
| "Turn PDF/Word into slides (strict)" | `/bq-presentation strict=true source=<path>` |
| "Several visual directions for a lecture" | `/bq-presentation variants=3..5` |

### By mode choice (4 modes + balanced default)

| Situation | Mode |
|---|---|
| Trivial fix / prototype / spike | `fast` |
| High-stakes / production / regulated (PCI / HIPAA / FedRAMP) / new build | `deep` |
| Long session / cost-sensitive / partial work | `token-saver` (alias: `lean`) |
| Large feature with clear shape; strong model expensive end-to-end | `delegate` |
| Standard work | no flag (balanced default) |

### Mode composition (advisor recommends combinations)

| User wants | Recommend |
|---|---|
| Quick small fix with low context cost | `fast token-saver` (or just `fast`) |
| Thorough research on follow-up task using cached research | `deep token-saver` |
| Large new feature — save cost, keep quality | `deep delegate` (strongly recommended) |
| Well-understood feature, save cost | `fast delegate` |
| Cheap model to refresh task pack from cached research | `token-saver delegate` |
| Trivial fix with delegate? | Refuse — handoff overhead not worth it; recommend `fast` instead |

### Mode conflict resolution

| Conflict | Resolution |
|---|---|
| `fast` + `deep` | Ask one question; default `deep` for quality-critical intents (new / security / release / deploy); `fast` for trivial scoped fixes |
| `delegate` + tiny task | Refuse delegate; recommend `fast` |
| `delegate` + no prior research | Auto-compose with `deep` (delegate needs research to write good task pack) |

The advisor recommends a default + explains; never silently picks.

### How to read `MODE_HISTORY.md`

`/bq-suggest` reads recent entries from `.bequite/state/MODE_HISTORY.md` to learn:
- Which modes the user prefers
- Which modes failed for which task types
- Cost patterns ("last 5 `deep` runs averaged $X")
- Outcome patterns ("`fast` mode on security tasks failed 2/3 last week → recommend `deep`")

### By "auto vs. scoped vs. phase vs. individual"

| Situation | Best choice |
|---|---|
| Full new project, you want to drive | `/bq-auto new "..."` — agent runs P0→P5 |
| Scoped task | `/bq-auto fix "..."` / `feature "..."` / `uiux "..."` — agent runs only relevant scope |
| One phase end-to-end | `/bq-p0`..`/bq-p5` |
| You want fine control | individual commands |

### Multi-domain combinations

For requests like "UX + security":

1. **Combined audit:** `/bq-audit` (covers UI + security)
2. **Targeted fixes:** `/bq-live-edit` for UI; `/bq-fix security "..."` for security findings
3. **Quality pass:** `/bq-red-team` (security-focused) + UI verification via `/bq-verify`

Or single command: `/bq-auto "UX + security audit and fix"` (the intent router handles both).

---

## Gate awareness

Before recommending any command, check `WORKFLOW_GATES.md`:

- If user wants `/bq-implement` but `PLAN_APPROVED ❌` → recommend `/bq-plan` first
- If user wants `/bq-release` but `VERIFY_PASS ❌` → recommend `/bq-verify` first
- If user wants `/bq-assign` but `PLAN_APPROVED ❌` → recommend `/bq-plan` first

Gate-aware = NEVER recommend a command whose required gates aren't met (unless user explicitly accepts skipping; in that case mention the consequence).

---

## When not to overbuild

Common over-recommendations to AVOID:

- Recommending the full P0→P5 lifecycle for a tiny fix (use `/bq-fix` direct)
- Recommending `/bq-multi-plan` for low-stakes (it's manual-paste; expensive in attention)
- Recommending `/bq-red-team` for a trivial change (overkill)
- Recommending `--mode deep` for prototypes (waste of tokens)
- Recommending new specialist skills when the user already has matching ones active

When in doubt, **prefer the lighter recommendation** + offer the deeper one as "if it's higher stakes than I'm assuming".

---

## How to combine multiple skill areas

When user says "UX + security + testing":

1. Identify the SHARED command that touches all 3 — usually `/bq-audit` (10-area audit)
2. Then per-area `/bq-fix` for findings
3. Then `/bq-test` to verify
4. Then `/bq-verify` to wrap

Or: `/bq-auto "audit and fix UX + security + testing"` — single command, scoped auto handles dispatch.

The advisor doesn't have to enumerate every command — it can recommend the right ORCHESTRATOR.

---

## Output shape (delivered by /bq-suggest, computed here)

The advisor produces structured recommendation:

1. **Recommended workflow** (in order, 1-5 commands)
2. **Skills activated** per command
3. **Mode** (fast / deep / token-saver / default)
4. **Auto vs. scoped vs. phase vs. individual** (best fit + single-command alternative if applicable)
5. **Required gates** (must be ✅)
6. **Optional gates** (skippable with trade-off)
7. **Missing information** (one question max, or "ready")
8. **One recommended next command**
9. **Why NOT each alternative** (1 sentence per major alternative considered)

---

## Anti-patterns

- ❌ Recommending out-of-order commands (gate awareness fails)
- ❌ Recommending 8 commands when 2 would do (over-build)
- ❌ Recommending `--mode deep` when no production touch (waste)
- ❌ Suggesting a non-BeQuite tool (out of scope; tool neutrality says the agent doesn't push tools)
- ❌ Skipping the "why NOT alternatives" — users learn from comparison
- ❌ Refusing to recommend at all because situation is "complex" — at minimum recommend `/bq-clarify` to surface what BeQuite offers

---

## Failure handling

| Failure | Recovery |
|---|---|
| Situation too vague | Ask ONE clarifying question; then proceed |
| Multiple workflows tie | Present top 2 ranked; let user pick |
| No commands match | Recommend `/bq-clarify` to surface what BeQuite actually offers |
| Gate state corrupted | Recommend `/bq-recover` first |

---

## What this skill does NOT do

- Implement commands (it just recommends)
- Critique the user's project (`/bq-red-team` does that)
- Pick tools (tool neutrality; commands pick tools when run)
- Replace `/bequite` (that's the gate-aware menu — this is the situation-aware advisor)
- Replace `/bq-now` (that's one-line orientation)

---

## See also

- `commands.md` — full command reference
- `docs/architecture/AUTO_MODE_STRATEGY.md` — when scoped auto helps
- `docs/architecture/WORKFLOW_GATES.md` — gate map
- `docs/specs/COMMAND_CATALOG.md` — terse machine-readable catalog

---

## When NOT to use this skill (alpha.15)

- A specific command is already obviously the right one (just run it)
- Mid-flow inside `/bq-auto` (it's already gate-aware + routes itself)
- Asking for one-line orientation — use `/bq-now`
- Looking at gate state — use `/bequite`

The advisor exists to bridge user-situation → BeQuite-surface. If the surface is already obvious, skip the advisor and act.
