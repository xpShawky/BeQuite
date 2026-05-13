---
description: Scoped autonomous workflow runner. Parses $ARGUMENTS for intent (new / fix / uiux / security / backend / frontend / database / deploy / live-edit / variants / etc.) and runs ONLY the relevant scope. Continues until complete; pauses only at hard human gates. Replaces unconditional plan-approval pauses.
---

# /bq-auto — scoped autonomous runner

## Purpose

Run the requested workflow end-to-end with **minimum interruption, maximum discipline, scoped to the actual task**. Pauses only at hard human gates (destructive ops, DB migrations, prod / VPS / SSL touches, secret rotations, paid services, scope contradictions, variant winner selection, cost ceilings, repeated failures).

**Does NOT pause for:**
- "Should I continue?"
- "Do you approve the plan?"
- "Should I fix the rest?"
- "Want me to add tests?"

If the task is safe + scoped, continue until verified, tested, and logged.

Full strategy: `docs/architecture/AUTO_MODE_STRATEGY.md`.

## When to use it

- Any time you want BeQuite to drive a complete task without per-step approval clicks
- Scoped fixes (don't restart the project lifecycle for a 1-section UI bug)
- Full new-project builds (the agent runs P0 → P5 itself)
- UI variant generation (dispatches to `/bq-uiux-variants`)
- Live frontend edits (dispatches to `/bq-live-edit`)

## Syntax

```
/bq-auto [intent] [options] "<task description>"
```

- `intent` (optional) — one of the 17 keywords below. If omitted, inferred from the task description.
- `options` (optional) — `key=value` pairs (e.g. `variants=5`, `max-cost-usd=10`, `mode=audit`)
- `"task description"` — the actual work, in quotes

## The 17 intent types

| Intent | Scope | Skills activated |
|---|---|---|
| `new` | Full P0 → P5 lifecycle | project-architect + per discovery |
| `existing` | P0 audit only | researcher + security-reviewer + frontend-quality |
| `feature` | Add Feature mini-cycle (`/bq-feature`) | per 12-type router |
| `fix` | Fix mini-cycle (`/bq-fix`) | per 15-type router + problem-solver |
| `uiux` | UI/UX workflow only | ux-ui-designer + frontend-quality |
| `frontend` | Frontend-only changes | frontend-quality |
| `backend` | Backend-only changes | backend-architect |
| `database` | DB only (hard gate for shared/prod DBs) | database-architect |
| `security` | Security review + fix | security-reviewer |
| `testing` | Test pass only | testing-gate |
| `devops` | DevOps only (hard gates for prod) | devops-cloud |
| `scraping` | Scraping workflow | scraping-automation |
| `automation` | Workflow automation | scraping-automation + backend-architect |
| `deploy` | Deploy workflow (multiple hard gates) | devops-cloud + release-gate |
| `live-edit` | Dispatch to `/bq-live-edit` | live-edit |
| `variants` | Dispatch to `/bq-uiux-variants` | ux-ui-designer + frontend-quality |
| `release` | P4 release flow | release-gate |

## Preconditions

- `BEQUITE_INITIALIZED` (run `/bq-init` if not)

## Required previous gates

- `BEQUITE_INITIALIZED`

(Mode is selected automatically based on intent. The agent sets `CURRENT_MODE.md` itself.)

## Files to read

- `.bequite/state/PROJECT_STATE.md`
- `.bequite/state/CURRENT_MODE.md`
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/state/WORKFLOW_GATES.md`
- `.bequite/state/DECISIONS.md`
- `.bequite/state/OPEN_QUESTIONS.md`
- Whatever upstream artifacts exist (DISCOVERY_REPORT, RESEARCH_REPORT, SCOPE, IMPLEMENTATION_PLAN, TASK_LIST)

## Files to write

- Every artifact each underlying command writes (per intent's scope)
- `.bequite/state/AUTO_STATE_<session>.json` (auto-mode state machine — for resume)
- `.bequite/state/WORKFLOW_GATES.md` (gates ticked)
- `.bequite/state/CURRENT_PHASE.md` (advances as phases complete)
- `.bequite/state/LAST_RUN.md` (after every step)
- `.bequite/logs/AGENT_LOG.md` (entry per step + entry per gate pause)
- `.bequite/logs/CHANGELOG.md` (`[Unreleased]` per material change)
- `.bequite/audits/VERIFY_REPORT.md` (when verification runs)

## Hard human gates (the only pauses)

The agent **MUST** pause and wait for explicit user confirmation at:

1. **Destructive file deletion** (`rm -rf` on tracked code, dropping directories)
2. **Database migration against shared / production DBs**
3. **Production server change** (SSH, systemd, firewall on prod)
4. **VPS / Nginx / SSL change**
5. **Paid service activation** (new SaaS signup with payment)
6. **Secret / key handling** (rotation, generation)
7. **Changing auth / security model**
8. **Changing project architecture** (e.g. monolith → microservices)
9. **Deleting old implementation** with active callers
10. **Scope contradiction** (task contradicts locked SCOPE.md)
11. **User explicit manual-approval request** (`--manual-approval` flag)
12. **Cost ceiling reached** (default $20/session)
13. **Wall-clock ceiling reached** (default 6h)
14. **Banned-weasel-word trip** in completion claim
15. **3 consecutive failures on the same task**
16. **UI variant winner selection** (after `/bq-uiux-variants` finishes)
17. **Release `git push` / `git tag`** (always user-run)

## Steps

### 1. Parse $ARGUMENTS

Extract:
- Intent (explicit keyword or inferred from task)
- Options (`key=value`)
- Task description (quoted)

If intent is ambiguous → ask **one** high-value question, then continue.

### 2. Read state + set mode

If `CURRENT_MODE.md` says "Not selected", set it based on intent:
- `new` → New Project
- `existing` → Existing Audit
- `feature` → Add Feature
- `fix` → Fix Problem
- `uiux` / `frontend` / `backend` / `database` / `security` / `testing` / `devops` / `scraping` / `automation` → Add Feature (with classification)
- `deploy` / `release` → Release Readiness
- `live-edit` / `variants` → Add Feature (UI subtype)

### 3. Execute per intent

#### `new`
Full lifecycle. Run P0 → P5 sequentially. Don't pause for plan approval; the agent drafts the plan and proceeds to assign + implement.

#### `existing`
Run `/bq-init` → `/bq-discover` → `/bq-doctor` → `/bq-audit` → report.

#### `feature`
Dispatch to `/bq-feature "<task>"` (12-type router). Implement + test + log.

#### `fix`
Dispatch to `/bq-fix "<task>"` (15-type router). Reproduce + root + patch + test + verify.

#### `uiux`
If `variants=N` option present → dispatch to `/bq-uiux-variants N "<task>"`.
Otherwise → audit current UI + apply targeted improvements + verify.

#### `frontend` / `backend` / `database` / `security` / `testing` / `devops` / `scraping` / `automation`
Activate the matching specialist skill. Run scoped audit + fix + verify within that domain.

#### `deploy`
Run `/bq-verify` → if PASS, plan deployment steps → pause at every prod touch.

#### `live-edit`
Dispatch to `/bq-live-edit "<task>"`.

#### `variants`
Dispatch to `/bq-uiux-variants [count] "<task>"`.

#### `release`
Run `/bq-verify` → `/bq-changelog` → print release commands → wait for user `git push` / `git tag`.

### 4. Continue without pausing (until a hard gate)

After each step:
- If success + no hard gate → proceed to next step
- If hard gate → pause with clear resume hint
- If recoverable failure (test red) → try `/bq-fix` once, then re-attempt
- If 3 consecutive failures → pause
- If banned weasel word would be in completion claim → rewrite with concrete fact, or pause

### 5. Verify before claiming done

Before final report:
- All gates required for this intent are `✅`
- All tests for changed surface pass
- If frontend involved + browser automation available → visual check
- No banned weasel words in any claim

### 6. Final output

```
✓ /bq-auto <intent> — <task>

What was requested:    <task verbatim>
What was done:         <bulleted summary>
Files changed:         <count>
  <list of paths>
Tests run:             <pass / total>
Browser checks:        <ran / skipped — reason>
Screenshots:           <paths if any>
Remaining issues:      <list or "none">
Verification:          <PASS / PARTIAL / FAIL>
Final recommendation:  <next safe step>

State updated:
  .bequite/state/LAST_RUN.md
  .bequite/state/WORKFLOW_GATES.md
  .bequite/logs/AGENT_LOG.md
  .bequite/logs/CHANGELOG.md
  .bequite/audits/VERIFY_REPORT.md (if verification ran)

Next: <suggested command>
```

If paused at a hard gate:
```
⏸ Paused at hard gate: <gate name>
  Reason: <one-line>
  Required action: <what user does>
  Resume: /bq-auto <same args>
```

## Operating modes (alpha.12 — 4 modes, composable)

`/bq-auto` accepts mode flags that adjust **depth, speed, token use, or model strategy**. Hard human gates still apply regardless of mode.

| Mode | Optimizes for | Best for | Avoid when |
|---|---|---|---|
| **balanced** (default) | sane defaults | most work | – |
| **fast** | speed | small fixes, prototypes, trusted stack | quality-critical / regulated / production-bound |
| **deep** | quality | new builds, regulated work, high-stakes | trivial tasks (overkill) |
| **token-saver** (alias: `lean`) | low token cost | long sessions, scoped fixes | greenfield (you need full discovery) |
| **delegate** | cost via model split | large features with clear shape | tiny tasks (overhead not worth it) |

### Mode flag syntax

Use either form:

```
/bq-auto fast "<task>"
/bq-auto fix "<task>" fast
/bq-auto fix "<task>" --mode fast
/bq-auto new "<task>" deep
/bq-auto fix "<task>" token-saver
/bq-auto feature "<task>" lean        # alias for token-saver
/bq-auto delegate "<task>"
/bq-auto deep delegate "<task>"        # COMPOSED
```

### Per-mode behavior

#### Fast Mode

- Short discovery (skip if `DISCOVERY_REPORT.md` exists and is recent)
- Short research (3 dims: stack + security + scalability — NOT all 11)
- Reuse known project memory
- Use existing stack (no stack research unless task forces it)
- Skip multi-plan
- Skip red-team
- **Still tests. Still verifies. Still logs.** Fast Mode is NOT low-quality mode.
- Shorter output: what was done / files changed / tests run / verification / next step

#### Deep Mode

- **No shallow research.** Full 11-dim research per `RESEARCH_DEPTH_STRATEGY.md`.
- Full discovery + competitor study + failure-mode analysis + UX deep-dive + security + scalability + deployment
- Multi-plan prompted (`/bq-multi-plan` recommended)
- Red-team mandatory at phase transitions
- Full verify + audit
- Searches **beyond obvious sources:** GitHub repos, official docs, Reddit, X/Twitter, Hacker News, Product Hunt, public communities, competitor sites, public issue trackers, niche forums, non-English sources, country-specific markets, failure stories, success patterns
- Produces: research report / decision summary / implementation plan / risks / acceptance criteria / test plan / verification checklist

Deep Mode is **structured**, not endless. The strategy doc caps research depth.

#### Token Saver Mode (alias: lean / token-lean)

- Read core memory only — not all `.bequite/` every command
- Read only files relevant to the current step
- Use summaries before full files
- Reuse previous discovery + research reports (don't re-fetch)
- Targeted Grep before broad Read
- Use focused skills only (not all 19 loaded)
- Compact reports (1-2 paragraph summaries, not multi-page)
- Ask only if needed
- Avoid loading all docs every session
- Use `.bequite/state/MISTAKE_MEMORY.md` to skip already-learned errors

**This is not the same as Fast Mode.** Token Saver can still be careful + thorough; it just avoids wasting context. Fast Mode optimizes for **speed**; Token Saver optimizes for **token cost**.

> **Note on naming:** This mode is called "Token Saver" or "token-lean", NOT "token-free". The mode reduces tokens; it doesn't eliminate them. If anywhere in docs reads "token-free", correct to "Token Saver" or "Token Saver Mode".

#### Delegate Mode (Architect Delegate pattern)

A two-session workflow where a **strong model architects + reviews** and a **cheaper model implements**. Net effect: 40-70% cost savings without quality loss when the task is large enough for the handoff overhead to pay off.

Three phases:

1. **Phase 1 — Architect (strong model, this session):** strong model does research + writes a detailed task pack at `.bequite/tasks/DELEGATE_TASKS.md`, `DELEGATE_INSTRUCTIONS.md`, `DELEGATE_ACCEPTANCE_CRITERIA.md`, `DELEGATE_TEST_PLAN.md`
2. **Phase 2 — Implement (cheaper model, separate session):** user switches Claude model (e.g. Opus → Sonnet, or to a different account/host). Cheap model runs `/bq-implement delegate` and executes exactly per the task pack — no architectural decisions, no guessing
3. **Phase 3 — Review (strong model, back here):** user switches back. Strong model runs `/bq-review delegate`; produces `.bequite/audits/DELEGATE_REVIEW_REPORT.md` with per-task verdicts (✅ approved / ⚠ approved-with-comments / ❌ rejected). Strong model fixes or re-instructs the cheap model

Full discipline: `.claude/skills/bequite-delegate-planner/SKILL.md`.

**Use Delegate Mode when:**
- A feature is large enough that strong-model end-to-end is expensive
- The work has a clear architectural shape
- You're willing to do a two-session handoff
- You can articulate acceptance criteria precisely

**Don't use Delegate Mode for:**
- Tiny tasks (handoff overhead isn't worth it)
- Exploratory / research-heavy work (cheap model can't make discovery decisions)
- Anything requiring real-time judgment (UX, design taste, security trade-offs)
- One-shot urgent fixes

### Mode composition

Modes can stack:

| Combination | Effect |
|---|---|
| `fast` + `token-saver` | quick task with compact output (recommended for one-off small fixes) |
| `deep` + `token-saver` | thorough research but compact output (recommended for follow-up planning on existing research) |
| `deep` + `delegate` | **strongly recommended for new features** — strong model researches deeply + writes task pack |
| `fast` + `delegate` | shallow research before delegation (OK for well-understood features) |
| `token-saver` + `delegate` | Phase 1 reuses cached research; suitable for follow-up tasks |

### Mode conflict resolution

Some combinations conflict:

| Conflict | Default resolution |
|---|---|
| `fast` + `deep` | Ask one question; default to `deep` for quality-critical (`new`, `security`, `release`, `deploy`) and `fast` for small scoped (`fix`, `feature` of trivial size) |
| `delegate` + tiny task | Warn: "overhead not worth it; use `fast` instead?" |
| `delegate` + greenfield + no research | Auto-add `deep` (delegate needs research to write good task pack) |

The agent picks a sane default + tells the user; doesn't silently choose.

### Mode tracking

Every `/bq-auto` run appends an entry to `.bequite/state/MODE_HISTORY.md` (mode used + outcome + cost approx + tests pass/total). `bequite-workflow-advisor` reads this to learn user's pattern.

---

## Mistake memory update

## Mistake memory + mode history update

After this command completes, if it surfaced a recurring mistake pattern, an unexpected root cause, or a project-specific lesson, append an entry to `.bequite/state/MISTAKE_MEMORY.md`.

Also append a one-line entry to `.bequite/state/MODE_HISTORY.md` (mode used + outcome + approx cost + tests pass/total). This helps `bequite-workflow-advisor` recommend the right mode next time.

Append when:
- A repeated bug pattern emerged (same root cause as a previous fix)
- A finding teaches a project-specific rule (e.g. "this codebase uses Tailwind v4 — don't apply v3 patterns")
- A failure mode tripped a banned-weasel-word check (the agent caught itself; record so it doesn't recur)
- A user correction revealed a wrong assumption

Skip if:
- Trivial one-off (typo, single missing import)
- Already captured in MISTAKE_MEMORY.md (don't duplicate)

Entry format: see `.bequite/state/MISTAKE_MEMORY.md`.

## Output format

Narrate each step + sub-step ("Running /bq-clarify…", "Implementing T-2.3…"). Don't ask "should I continue?" between steps unless a hard gate trips.

## Quality gate

- Intent correctly parsed
- Scope correctly identified
- All required gates for that intent are `✅`
- No banned weasel words in any output
- No destructive op without explicit user OK
- No new dep installed without decision section (per tool neutrality)
- Final verification ran (or `PARTIAL`/`FAIL` honestly reported)

## Failure behavior

- Intent ambiguous → ask ONE question, then continue
- Required upstream artifact missing → run the prerequisite command, then continue
- Test red → `/bq-fix` once; if still red → pause
- Build red → `/bq-fix` once; if still red → pause
- Hard gate triggered → pause with resume hint
- Cost ceiling → pause; ask user to authorize continuation
- 3 consecutive failures → pause
- Banned weasel word → rewrite or pause

## Tool neutrality (global rule)

⚠ **Every tool, library, framework, design system, or workflow this command might add during execution is a CANDIDATE, not a default.**

Auto-mode does **not** auto-install dependencies. New deps require a decision section (Problem / Options / Sources / Best option / Why it fits / Why others rejected / Risk / Cost / Test plan / Rollback plan).

**Do not say:** "Auto added Playwright."
**Say:** "Playwright was needed for browser inspection. One candidate; compared against alternatives; chosen because [reasons]. Decision section in IMPLEMENTATION_PLAN §X."

The 10 decision questions still apply to every tool the agent considers adding during the run.

See `.bequite/principles/TOOL_NEUTRALITY.md`.

## Usual next command

- After completion: `/bq-handoff` (if shipping to another engineer), or done
- After pause at hard gate: resolve the gate, then re-run `/bq-auto <same args>`
