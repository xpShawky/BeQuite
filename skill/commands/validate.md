---
name: bequite.validate
description: Phase 6 — validation mesh. Loads qa-engineer + security-reviewer + devops-engineer. Runs format / lint / typecheck / unit / integration / e2e (Playwright) / a11y / build / docker compose / security scan / audit / freshness per the active Mode's gate matrix. Emits evidence + receipt.
phase: P6
persona: qa-engineer + security-reviewer + devops-engineer
prompt_pack: prompts/recovery_prompt.md (cross-references; full validation in qa-engineer.md)
---

# /bequite.validate

When invoked (or `bequite validate`):

## Step 1 — Read context

- `state/project.yaml::mode` (drives gate matrix per Constitution v1.0.1).
- All implementation receipts since the last validation.
- Active Doctrines (each contributes verification gates).

## Step 2 — Run the validation mesh

Per the active Mode (Constitution v1.0.1):

| Gate | Fast | Safe | Enterprise |
|---|---|---|---|
| Format | required | required | required |
| Lint | required | required | required |
| Typecheck | required | required | required |
| Unit tests | required | required | required |
| Integration tests | optional | required | required |
| API tests | required (if API) | required | required |
| Database migration test | required (if DB) | required | required |
| Seed test | required (if seed) | required | required |
| E2E (Playwright walks) | smoke only | full admin + user walks | full + visual diff |
| Accessibility smoke | required (frontend) | required | required |
| Build | required | required | required |
| Docker Compose up | optional | required (if applicable) | required |
| Security scan (semgrep + osv-scanner) | optional | required | required |
| `bequite audit` (Constitution drift) | required | required | required |
| `bequite freshness` (knowledge probe) | optional | required | required |
| Evidence index update | required | required | required |
| Restore-drill (DB) | optional | quarterly | monthly |

## Step 3 — Playwright walks (when frontend Doctrine active)

Planner → spec writer → generator → healer pattern (per `qa-engineer.md`).

For each user role (admin, user, plus any role declared in the project):

1. Planner explores running app; emits `tests/seed.spec.ts` + per-flow `.md` specs.
2. Generator converts specs into Playwright tests using `getByRole` accessibility-first locators.
3. Healer runs the suite, repairs broken selectors, retries flaky tests with condition-based waits.

Walks at viewport 360 + 1440. For mena-bilingual Doctrine: walks at locale `en-*` + `ar-*` (RTL).

## Step 4 — Self-walk + smoke

`scripts/self-walk.sh` boots the app; logs in admin then user; traverses every route; captures console errors + network errors + 4xx/5xx.

`scripts/smoke.sh` curls every public endpoint; expects 200/401/403 per spec.

## Step 5 — Evidence + receipt

`evidence/<phase>/<task>/` populated per qa-engineer outputs. Phase summary at `evidence/<phase>/phase_summary.md`.

Receipt (v0.7.0+) records every gate's exit code + stdout hash.

## Stop condition

P6 exits when:

- Every gate appropriate to the active Mode passes.
- All E2E walks pass for every role × viewport × locale.
- axe-core: zero violations.
- Smoke test: every endpoint returns expected code.
- Secret scan: zero matches.
- `bequite audit` clean.
- `bequite freshness` clean (Safe / Enterprise).
- Phase summary written.

## Anti-patterns

- "Tests pass on my machine" — run them in this session; capture output.
- Skipping a gate appropriate to the Mode — push back; ADR if Mode-bump avoidance.
- Marking flaky tests as `skip` silently — quarantine via tagged tracker.
- Verifying without running.
- Weasel words in the validation report.

## On failure (master §3.7 + Iron Law II)

- 3 consecutive failures of the same test → escalate to root-cause-trace + hypothesis-test + defense-in-depth (systematic-debugging).
- Still failing → Stop hook returns `{ok:false}`; force a different approach.

## Related

- `/bequite.audit` — Constitution + Doctrine drift detector.
- `/bequite.freshness` — knowledge probe.
- `/bequite.evidence` — surface evidence/<phase>/<task>/ artefacts.
