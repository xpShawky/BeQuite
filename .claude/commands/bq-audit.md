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
