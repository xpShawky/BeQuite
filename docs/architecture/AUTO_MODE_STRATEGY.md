# Auto-mode strategy (v3.0.0-alpha.4)

**Status:** active
**Adopted:** 2026-05-12
**Command:** `/bq-auto [intent] [options] "task"`
**Skill orchestration:** all 14 BeQuite skills (activated by intent)
**Reference:** ADR-002 (mandatory workflow gates), TOOL_NEUTRALITY.md

---

## The principle

When the user invokes `/bq-auto`, the agent runs autonomously until the requested task is complete, tested, verified, and logged.

**It does NOT pause for:**
- "Should I continue?"
- "Do you approve the plan?"
- "Should I fix the rest?"
- "Should I proceed with implementation?"
- "Want me to add tests?"
- "Ready to verify?"

**It DOES pause for hard human gates** (see §5 below).

The agent decides defaults and proceeds. The user can interrupt at any point.

---

## 1. The intent router

`/bq-auto` parses `$ARGUMENTS` to determine which workflow scope to run.

### Syntax

```
/bq-auto [intent] [options] "<task description>"
```

### Intent matching order

1. **Explicit intent keyword** as the first word: `new | existing | feature | fix | uiux | frontend | backend | database | security | testing | devops | scraping | automation | deploy | live-edit | variants | release`
2. **Options** in `key=value` form: `variants=5`, `mode=audit`, `target=production`
3. **Task description** in quotes — the actual work

### Examples

| Command | Parsed intent | Options | Task |
|---|---|---|---|
| `/bq-auto new "Build pharmacy SaaS admin"` | `new` | – | "Build pharmacy SaaS admin" |
| `/bq-auto fix "Hidden text on dashboard"` | `fix` | – | "Hidden text on dashboard" |
| `/bq-auto uiux variants=5 "Five dashboard concepts"` | `uiux` | variants=5 | "Five dashboard concepts" |
| `/bq-auto security "Audit + fix issues"` | `security` | – | "Audit + fix issues" |
| `/bq-auto deploy "VPS deploy plan + execute"` | `deploy` | – | "VPS deploy plan + execute" |
| `/bq-auto live-edit "Pricing cards less crowded"` | `live-edit` | – | "Pricing cards less crowded" |
| `/bq-auto "Add CSV export"` | (inferred) `feature` | – | "Add CSV export" |
| `/bq-auto "Build full SaaS for X"` | (inferred) `new` | – | "Build full SaaS for X" |

### Intent inference

If no explicit intent keyword, the agent infers from the task description:

| Phrase pattern | Inferred intent |
|---|---|
| "build", "create", "new project", "from scratch", "saas for…" | `new` |
| "fix", "broken", "doesn't work", "bug", "error" | `fix` |
| "add", "feature", "support for…", "implement X" | `feature` |
| "redesign", "ugly", "ui issues", "make it look…", "design directions" | `uiux` |
| "security", "vulnerability", "owasp", "auth issue" | `security` |
| "slow", "perf", "scaling" | `fix` (with perf classification) |
| "deploy", "ship", "production", "vps", "release" | `deploy` or `release` |
| "audit", "review", "what's wrong with…" | `existing` |

If still ambiguous after pattern matching → ask **one** high-value question:

> "I see two possible interpretations: (A) treat this as a new feature in the existing project, or (B) audit the existing implementation first. Which?"

Only one question. After the answer → continue autonomously.

---

## 2. Scope per intent

Each intent maps to a scoped workflow. The agent runs only the relevant phases / commands.

### `new`

Full lifecycle: P0 → P1 → P2 → P3 → P4 (no auto-push) → P5.
- Setup (init + doctor + discover)
- Clarify (3-5 questions, accept defaults if user says "all defaults")
- 11-dim research
- Scope lock (agent drafts + presents; doesn't pause for approval unless conflicts found)
- Plan write (agent drafts + proceeds to assign)
- Assign + implement loop until task list empty
- Test + audit + review
- Verify + changelog + release instructions (user runs git commands)
- Memory snapshot

### `existing`

Audit only — no build phase.
- Init + discover + doctor
- 11-dim audit
- Findings report
- (No fix unless user re-runs with `fix` intent)

### `feature`

Add Feature mini-cycle.
- Mode = Add Feature (if not set)
- `/bq-feature "task"` (12-type router)
- Implement + test + log
- No full P1 research unless the feature is genuinely new domain

### `fix`

Fix mini-cycle.
- `/bq-fix "task"` (15-type router)
- Reproduce → root cause → smallest patch → regression test → verify
- No full P0/P1 unless the fix needs fresh discovery
- Doctor checks only if env-related
- Browser checks only if frontend-related

### `uiux`

UI/UX workflow.
- Activate `bequite-ux-ui-designer` + `bequite-frontend-quality`
- If `variants=N` option → dispatch to `/bq-uiux-variants N "task"`
- Otherwise → improve existing UI per the task (audit + targeted edits + verify)
- No backend rebuild unless UI task depends on it

### `frontend`

Frontend-only changes.
- Activate `bequite-frontend-quality`
- Inspect frontend, identify issue, apply targeted edits, verify
- May invoke `/bq-live-edit` for section-by-section changes
- No backend / DB changes

### `backend`

Backend-only changes.
- Activate `bequite-backend-architect`
- Inspect API, identify issue, apply targeted edits, verify
- No frontend changes

### `database`

Database-only changes.
- Activate `bequite-database-architect`
- Schema changes, indexing, migrations (with hard gate for shared/prod DBs)
- No frontend / backend code changes unless DB schema requires them

### `security`

Security review + fix.
- Activate `bequite-security-reviewer`
- Scan for the security issue type
- Apply patch + add regression test
- Rotate secrets if any were exposed (gate: user does the rotation)

### `testing`

Test-only work.
- Activate `bequite-testing-gate`
- Run existing tests; write missing tests for changed surface
- No production code changes

### `devops`

DevOps-only work.
- Activate `bequite-devops-cloud`
- CI/CD changes, env vars, monitoring setup
- Hard gates for production touches

### `scraping`

Scraping / automation work.
- Activate `bequite-scraping-automation`
- Polite-mode defaults, robots.txt respect
- Article VIII discipline

### `automation`

Workflow automation.
- Activate `bequite-scraping-automation` + `bequite-backend-architect`
- n8n / Inngest / cron pattern as candidates (per tool neutrality)

### `deploy`

Deployment workflow with hard gates.
- Activate `bequite-devops-cloud` + `bequite-release-gate`
- Plan deployment steps
- Hard gate at every prod / VPS / Nginx / SSL touch
- Print commands; user executes

### `live-edit`

Live edit workflow.
- Dispatch to `/bq-live-edit "task"`
- See LIVE_EDIT_STRATEGY.md

### `variants`

UI variant generation.
- Dispatch to `/bq-uiux-variants [count] "task"`
- See UIUX_VARIANTS_STRATEGY.md

### `release`

P4 release flow.
- Verify + changelog + release instructions
- User runs `git push` and `git tag`

---

## 3. Continue-by-default

Auto mode continues from one step to the next without pausing **as long as**:

- The previous step succeeded
- No hard human gate (§5) was triggered
- Cost ceiling not reached
- Time budget not exhausted (default 6h wall-clock; configurable via `max-wall-clock-hours`)
- No banned weasel words in completion claims (rewrite or pause)
- No 3-consecutive-failures on the same task

If any of those trip → pause with a clear resume hint.

### What "continue" means per step

| Step | Continue without asking when… |
|---|---|
| Plan written | Plan is consistent with locked scope and uses already-decided tools |
| Tasks assigned | TASK_LIST.md generated cleanly from plan |
| Task implemented | Tests for it pass; no destructive ops |
| Test red | Try `/bq-fix` once; if still red → pause |
| Build red | Try `/bq-fix` once; if still red → pause |
| Review verdict = Approved-with-comments | Continue (treat as approved) |
| Review verdict = Blocked | Pause |
| Audit findings = MEDIUM/LOW | Continue (note in report) |
| Audit findings = BLOCKER | Pause |
| Verify PASS | Continue to changelog |
| Verify FAIL | Try `/bq-fix` once; if still FAIL → pause |
| Release commands printed | Wait for user to run git push/tag (this is a hard gate) |

---

## 4. Mandatory gates per scope

The agent enforces mandatory workflow gates **scoped to the task type**. Not every task triggers every gate.

| Intent | Required gates |
|---|---|
| `new` | BEQUITE_INITIALIZED, MODE_SELECTED, CLARIFY_DONE, RESEARCH_DONE, SCOPE_LOCKED, PLAN_APPROVED, all P2/P3/P4 gates |
| `existing` | BEQUITE_INITIALIZED, MODE_SELECTED, DISCOVERY_DONE, AUDIT_DONE |
| `feature` | BEQUITE_INITIALIZED, MODE_SELECTED, FEATURE_DONE |
| `fix` | BEQUITE_INITIALIZED, MODE_SELECTED, FIX_DONE |
| `uiux` | BEQUITE_INITIALIZED, frontend exists; PLAN_APPROVED only if changing design system |
| `frontend` | BEQUITE_INITIALIZED, frontend exists |
| `backend` | BEQUITE_INITIALIZED, backend exists |
| `database` | BEQUITE_INITIALIZED, DB exists; **migration-approval gate** for shared/prod DBs |
| `security` | BEQUITE_INITIALIZED |
| `testing` | BEQUITE_INITIALIZED |
| `devops` | BEQUITE_INITIALIZED; **server-change gate** for prod touches |
| `scraping` | BEQUITE_INITIALIZED; robots.txt + ToS check |
| `automation` | BEQUITE_INITIALIZED |
| `deploy` | BEQUITE_INITIALIZED, VERIFY_PASS; **multiple hard gates** during execution |
| `live-edit` | BEQUITE_INITIALIZED, frontend exists |
| `variants` | BEQUITE_INITIALIZED, frontend exists |
| `release` | BEQUITE_INITIALIZED, VERIFY_PASS, CHANGELOG_READY |

Scoped gates: e.g. `uiux` fix doesn't force full competitor research; `fix` doesn't restart the project lifecycle; `feature` doesn't require new SCOPE.md unless it expands scope.

---

## 5. Hard human gates (the only places auto-mode pauses)

The agent **MUST** stop and wait for explicit user confirmation at:

1. **Destructive file deletion** (`rm -rf` on tracked files, dropping directories of code)
2. **Database migration** (against shared / production / multi-developer DBs)
3. **Production server change** (SSH ops on prod, firewall changes, systemd ops)
4. **VPS / Nginx / SSL change** (TLS cert ops, reverse-proxy config changes)
5. **Paid service activation** (signing up + paying for a new SaaS / API)
6. **Secret / key handling** (rotating secrets, generating new tokens)
7. **Changing auth / security model** (swapping auth library, changing session strategy)
8. **Changing project architecture** (monolith → microservices, SQL → NoSQL, etc.)
9. **Deleting old implementation** (rm of files that still have callers)
10. **Scope contradiction** (task contradicts locked SCOPE.md)
11. **User explicit manual-approval request** (passed `--manual-approval` or said "stop and ask me before…")
12. **Cost ceiling reached** (default $20/session; configurable)
13. **Wall-clock ceiling reached** (default 6h; configurable)
14. **Banned-weasel-word trip** in a completion claim
15. **3 consecutive failures on the same task**
16. **UI variant winner selection** (when `/bq-uiux-variants` finishes generating, user picks)

If none of these → continue.

---

## 6. Output discipline

When auto-mode finishes (success or pause), it prints:

```
✓ /bq-auto <intent> — <task>

What was requested: <task verbatim>
What was done:      <bulleted summary>
Files changed:      <count> (<list of paths>)
Tests run:          <pass / total>
Browser checks:     <ran / skipped — reason if skipped>
Screenshots:        <list of paths if any>
Remaining issues:   <list, or "none">
Verification:       <PASS / PARTIAL / FAIL>
Final recommendation: <next safe step>

State updated:
  .bequite/state/LAST_RUN.md
  .bequite/state/WORKFLOW_GATES.md
  .bequite/logs/AGENT_LOG.md
  .bequite/logs/CHANGELOG.md
  .bequite/audits/VERIFY_REPORT.md (if verification ran)

Next command: <suggestion>
```

If paused at a hard gate, the output includes:

```
⏸ Paused at hard gate: <gate name>
  Reason: <one-line explanation>
  Required action: <what the user does to unblock>
  Resume: /bq-auto <same args>
```

---

## 7. Cost / time discipline

- Default cost ceiling: $20/session (configurable via `bequite.config.toml::cost.session_max_usd`)
- Default wall-clock: 6h (configurable)
- Heartbeat: write `LAST_RUN.md` every 5 minutes during long runs
- Exceeding ceiling → pause + ask user to authorize continuation or stop

---

## 8. Anti-patterns to refuse

- **Restarting the whole project lifecycle** for a scoped fix
- **Pausing after every step** for confirmation when no hard gate exists
- **Asking "should I continue?"** mid-flow
- **Asking "do you approve the plan?"** when `/bq-auto` was invoked with an explicit scope
- **Auto-installing new dependencies** without justification (per TOOL_NEUTRALITY.md)
- **Auto-pushing or auto-deploying** to production (hard gates always apply)
- **Continuing past a destructive op** without user OK
- **Claiming "complete"** without verification

---

## 9. Failure handling

| Failure | Recovery |
|---|---|
| Test red after implementation | Run `/bq-fix` once; if still red, pause |
| Build red | Run `/bq-fix` once; if still red, pause |
| Lint red | Auto-fix if `--fix` available; otherwise pause |
| Typecheck red | Pause; this is structural |
| 3 consecutive task failures | Pause; ask for guidance |
| Banned weasel word in completion | Rewrite with concrete claim; if can't, pause |
| Tool / dep not found | Pause; ask user to install (do NOT auto-install per tool neutrality) |
| Frontend dev server won't start | Pause; ask for the right start command |
| Cost ceiling exceeded | Pause; ask for re-authorization |

---

## 10. Resume after pause

After a pause:
- Auto-state stored in `.bequite/state/AUTO_STATE_<session>.json`
- User runs `/bq-auto resume <session-id>` OR re-runs `/bq-auto <original args>` (agent reads LAST_RUN.md + AUTO_STATE to find where it stopped)

---

## 11. What this strategy is NOT

- **Not** "fire and forget" — the user is in the loop at hard gates
- **Not** a justification for skipping research (it scopes research to relevance, doesn't skip it)
- **Not** a substitute for `/bq-plan` for new projects (it runs `/bq-plan` itself, then continues without asking)
- **Not** a way to bypass tool neutrality (every new tool still requires a decision section)
