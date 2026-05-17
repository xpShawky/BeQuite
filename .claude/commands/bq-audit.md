---
description: Full project audit. Inspect install, run, frontend (if present), API (if present), CLI (if present), tests, docs, UX, security basics, release blockers. Writes FULL_PROJECT_AUDIT.md.
---

# /bq-audit — full project audit

You are doing a **comprehensive product-level audit**. Catches what `/bq-doctor` + `/bq-test` miss. Output is `.bequite/audits/FULL_PROJECT_AUDIT.md` with prioritized findings.

## Step 1 — Read context

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/audits/DOCTOR_REPORT.md`
- `.bequite/plans/IMPLEMENTATION_PLAN.md` (if exists)
- `.bequite/state/PROJECT_STATE.md`

## Step 2 — Inspect by area

For each area present in the repo, audit it. Skip areas that don't apply.

### Install
- Can a fresh clone install + run without manual intervention?
- Are there `.env.example` for every env var the code references?
- Does the README install path actually match what works?

### Run
- Does `npm run dev` (or equivalent) boot without errors?
- Are dev-server URLs documented?
- Are there port conflicts likely?

### Frontend (if present — Next.js / Nuxt / Vite / etc.)
- Page renders without console errors
- No invisible text (text color ≈ background)
- No dead buttons (every button does something)
- No hardcoded mock data masquerading as live (Article VI)
- Honest empty / loading / error states
- Contrast passes axe-core
- Responsive at 360 + 1440
- See `.claude/skills/bequite-frontend-quality/SKILL.md` for the deeper checklist (15 AI-slop patterns).

### API (if present — REST / GraphQL / RPC)
- Health endpoint exists + returns sane
- CORS configured correctly
- 404 handler returns structured error not HTML
- Validation on every body (Zod / pydantic / schema)
- Auth surface clear
- No `/api/admin` accessible without auth (smoke test)
- Error responses include actionable info

### CLI (if present)
- `--version` + `--help` work
- Errors print human-readable messages (not stack traces by default)
- A "doctor" / first-time command exists
- Install path documented

### Tests
- Tests exist
- They actually run via the documented command
- Coverage roughly tracks the surface (not 100%, but no untested critical paths)
- E2E or smoke test exists for the user-facing flow

### Docs
- README leads with install + run + test
- CHANGELOG exists + has recent entries
- API endpoints documented (if API present)
- Architecture overview exists somewhere

### Security basics
- `.env*` not committed
- No `api_key = "..."` in source
- No `password = "..."` in source
- No personally-identifying info hardcoded
- Dependencies have no critical CVEs (sample-check via `npm audit` / `pip-audit`)
- Auth flow uses a known library (Better-Auth / Clerk / Supabase Auth) not custom

### Release readiness
- All scope-locked items shipped (per SCOPE.md)
- All tasks done (per TASK_LIST.md)
- No `[!] blocked` tasks
- Verify command works (per /bq-verify)

## Step 3 — Classify findings

Each finding gets a severity:

- **BLOCKER** — must fix before ship. Examples: secret in source, no health endpoint when API is required, install path broken.
- **HIGH** — should fix before ship. Examples: missing tests on critical flow, AI-slop UI, hardcoded mocks.
- **MEDIUM** — fix soon. Examples: outdated dep, README stale, no CHANGELOG.
- **LOW** — nice-to-have. Examples: missing docs link, code style nit, accessibility minor issue.

## Step 4 — Write FULL_PROJECT_AUDIT.md

`.bequite/audits/FULL_PROJECT_AUDIT.md`:

```markdown
# Full Project Audit

**Generated:** <ISO 8601 UTC>
**Repo:** <path>
**Stack:** <one-liner>

## Executive summary

(3-5 sentences: what's the state of this project, what's the biggest risk, what's the quickest win.)

## Findings

### Blockers (must fix before ship)

| # | Area | Finding | File / location | Suggested fix |
|---|---|---|---|---|
| B-1 | Install | `pip install -e ./cli` fails (README missing) | cli/ | Author cli/README.md |
| B-2 | ...    |  |  |  |

### High

| # | Area | Finding | File | Fix |
|---|---|---|---|---|
| H-1 | ... |

### Medium

| ... |

### Low

| ... |

## Coverage matrix

| Area | Status |
|---|---|
| Install | <green / yellow / red> |
| Run | ... |
| Frontend | ... |
| API | ... |
| CLI | ... |
| Tests | ... |
| Docs | ... |
| Security | ... |
| Release | ... |

## Recommended next steps

1. /bq-fix B-1 (first blocker)
2. /bq-fix B-2
3. /bq-verify once blockers cleared
```

## Step 5 — Update state + log

- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md` appended

## Step 6 — Report back

```
✓ Audit complete

Blockers: <count>
High:     <count>
Medium:   <count>
Low:      <count>

Report: .bequite/audits/FULL_PROJECT_AUDIT.md

Next: /bq-fix <first-blocker-id>  (or /bq-red-team for adversarial review)
```

## Rules

- **No "should work" claims.** Either you verified or you didn't — be explicit.
- **Cite file:line for every finding.** Vague "this is bad" is not useful.
- **Be honest about untested areas.** Note "not audited — no API in this repo" rather than skipping.
- **Don't fix during audit.** Just document. Fixes happen in `/bq-fix`.

## Standardized command fields (alpha.6)

**Phase:** P3 — Quality and Review
**When NOT to use:** small targeted bug (use `/bq-fix`); single-file review (use `/bq-review`); fresh project with no code yet (audit needs something to audit).
**Preconditions:** `BEQUITE_INITIALIZED`
**Required previous gates:** `BEQUITE_INITIALIZED` (`DISCOVERY_DONE` recommended)
**Quality gate:**
- `FULL_PROJECT_AUDIT.md` written
- Each finding severity-tagged (BLOCKER / HIGH / MEDIUM / LOW)
- Each finding cites file:line + suggested fix
- Mistake-memory entries appended for systemic patterns
- Marks `AUDIT_DONE ✅`
**Failure behavior:**
- Audit reveals a critical missing capability (e.g. no tests, no auth) → flag as BLOCKER + recommend `/bq-feature` for that domain
- No file:line cite-able → finding is too vague; refine or drop
**Memory updates:** Sets `AUDIT_DONE ✅` (optional gate unless Release Readiness mode). Appends systemic-pattern entries to `MISTAKE_MEMORY.md`.
**Log updates:** `AGENT_LOG.md`.

## Memory files this command reads

- `.bequite/audits/*.md` (prior audits)
- `.bequite/plans/*.md`
- `.bequite/tasks/*.md`
- `.bequite/state/*.md`
- The actual repo (broad)

## Memory files this command writes

- `.bequite/audits/FULL_PROJECT_AUDIT.md` (new or overwrites if a prior one exists — version it then with a timestamp if user wants both)
- `.bequite/state/LAST_RUN.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

- `/bq-fix B-1` — start clearing blockers
- `/bq-red-team` — adversarial review for what the audit missed

---

## Mistake memory update

Audit findings often reveal **systemic patterns** — the same class of mistake repeated across the codebase (e.g. multiple endpoints missing input validation; multiple pages without empty states). After the audit, append a MISTAKE_MEMORY entry for each pattern (not each instance):

- Category tag (e.g. `[fe][design]`, `[be][validation]`, `[sec][input]`)
- The pattern (one sentence)
- Where it appeared (file:line list, top 3-5)
- Prevention rule (what to check before adding new code)
- How to detect next time (CI rule, lint config, axe-core check, etc.)

Skip MISTAKE_MEMORY for purely cosmetic findings or one-offs.

See `.bequite/state/MISTAKE_MEMORY.md` template.

---

## Tool neutrality (global rule)

⚠ **Audit findings recommend candidates, not commitments.**

When an audit suggests adopting a new tool to address a finding (e.g. "add Sentry for error tracking", "add axe-core for accessibility"), frame it as a candidate:

**Do not write in the audit:** "Add Sentry."
**Write:** "Error tracking is missing. Sentry is one candidate; compare against Datadog, Honeycomb, or self-hosted GlitchTip based on this project's budget, data-residency needs, and team familiarity. Adopt only after a decision section is written."

Each Blocker / High / Medium recommendation that adds a tool must trigger a decision section in the follow-up `/bq-fix` or `/bq-implement` cycle:
- Problem
- Options considered
- Sources / references checked
- Best option
- Why it fits this project
- Why other options were rejected
- Risk
- Cost / complexity
- Test plan
- Rollback plan

**Audit recommendations are diagnostic, not prescriptive.** The fix cycle decides the specific tool.

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.

---

## Gate check + memory preflight (alpha.15)

Before doing any work:

1. **Gate check.** Read `.bequite/state/WORKFLOW_GATES.md`. If this command's required gates aren't `✅`, refuse:
   > "You're trying to run this command, but `<required-gate>` is pending. Run `<prerequisite-command>` first."

   Don't proceed when a required gate is missing. Recommend the prerequisite + how to resume.

2. **Memory preflight.** Read these files first (per `docs/architecture/MEMORY_FIRST_BEHAVIOR.md`):

   - `.bequite/state/PROJECT_STATE.md`
   - `.bequite/state/CURRENT_MODE.md`
   - `.bequite/state/CURRENT_PHASE.md`
   - `.bequite/state/LAST_RUN.md`
   - `.bequite/state/MISTAKE_MEMORY.md` — top 10–20 entries (skip mistakes already learned)
   - Other state files only when relevant to this command's scope (`DECISIONS.md` for architectural questions, `OPEN_QUESTIONS.md` for phase transitions, `MODE_HISTORY.md` when invoked via `/bq-auto`-style flows)

   **Use focused reads.** Don't load all of `.bequite/` every command.

## Memory writeback (alpha.15)

After successful completion:

- `.bequite/state/LAST_RUN.md` — this command + outcome
- `.bequite/state/WORKFLOW_GATES.md` — set this command's gate to `✅` if applicable
- `.bequite/state/CURRENT_PHASE.md` — advance if phase transitioned
- `.bequite/logs/AGENT_LOG.md` — append entry
- `.bequite/logs/CHANGELOG.md` `[Unreleased]` — only when material files changed (skip for read-only commands)
- `.bequite/state/MISTAKE_MEMORY.md` — append when a project-specific lesson surfaced
- `.bequite/state/MODE_HISTORY.md` — append mode + outcome (when invoked via `/bq-auto`-style mode)

**Failure behavior:** don't claim `✅ done` if any of the above wasn't completed. Report PARTIAL with the specific gap.
