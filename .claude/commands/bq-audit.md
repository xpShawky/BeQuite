---
description: Full project audit. Inspects install, run, frontend, API, CLI, tests, docs, security basics and release blockers, and writes prioritized findings with file:line evidence to .bequite/audits/FULL_PROJECT_AUDIT.md. Arguments - client (a client-facing report), a11y (a WCAG audit with a remediation plan).
---

# /bq-audit: the whole project, findings only

<!-- bq:contract -->
> **This command runs inside the BeQuite pipeline** (`.claude/bequite/docs/architecture/PIPELINE.md`):
> 1. **Up to date:** if `.claude/bequite/bin/bq-update.sh` exists, first run `bash .claude/bequite/bin/bq-update.sh` and say its one line (hourly; never blocks). A plugin install has no such file: it updates through `/plugin`, and the docs, templates and scripts this command cites are under `${CLAUDE_PLUGIN_ROOT}`.
> 2. **Orient:** announce the `Skill Selection:` block; resolve the work (`.bequite/ACTIVE.md`, `.bequite/work/<id>/`, or `/bq-work new`); refuse and name any missing gate (`.bequite/state/WORKFLOW_GATES.md`, `work/<id>/gates.md`).
> 3. **Prove and write back:** plan first for non-trivial work and stop at hard human gates; every check goes to `work/<id>/evidence.md` or is `UNVERIFIED:`; write back (work log, `.bequite/state/LAST_RUN.md`, `.bequite/logs/AGENT_LOG.md`, `.bequite/skills/SKILL_USAGE_LOG.md`, `.bequite/state/MISTAKE_MEMORY.md` on a lesson) and end with the Next Command Recommendations.
<!-- /bq:contract -->

A product-level audit that catches what `/bq-doctor` and `/bq-test` miss. It documents; it does not fix. Skills: `bequite-security-reviewer`, `bequite-frontend-quality` (a UI exists), `bequite-testing-gate`, `bequite-guard-pass`.

## Syntax

```
/bq-audit [client | a11y]
```

`client` writes the same findings for a client: severity, business impact in plain language, fix effort, and a quote table with effort and rate left for the user to fill. `a11y` audits against WCAG and delivers a prioritized remediation plan.

## Gates

Needs `BEQUITE_INITIALIZED` (`DISCOVERY_COMPLETE` recommended). Sets `AUDIT_COMPLETE`. Not for a single bug (`/bq-fix`), one diff (`/bq-review`), or a project with no code yet.

## Steps

1. **Read context:** `.bequite/audits/DISCOVERY_REPORT.md`, `DOCTOR_REPORT.md`, `PROJECT_STATE.md`, the top lessons in `MISTAKE_MEMORY.md`.
2. **Inspect each area that exists**, running what can be run:
   - **Install and run:** a clean install from the README alone; the dev and build commands; what breaks.
   - **Frontend:** every route renders; empty, loading and error states; phone width; console errors; design continuity against the Design DNA.
   - **API:** each endpoint's validation, auth, error shape, idempotency on writes.
   - **CLI:** `--help`, bad input, exit codes.
   - **Tests:** what is covered, what is not, tests that assert nothing.
   - **Docs:** README accuracy, env documentation, stale instructions.
   - **Security basics:** secrets in the tree or history, dependency advisories, auth and session handling, input reaching queries or the DOM.
   - **Release readiness:** version, changelog, CI, rollback.
3. **Classify:** BLOCKER (must fix before ship), HIGH, MEDIUM, LOW. Each finding has `file:line`, what happens, and a suggested fix.
4. **Write `.bequite/audits/FULL_PROJECT_AUDIT.md`:** an executive summary, findings by severity with IDs (B-1, H-1 ...), a coverage matrix that names every area audited and every area not audited with the reason, and the recommended next steps.

## Rules

- Verified or not verified: say which for every claim. An area that was not audited is listed as such.
- A finding without `file:line` is refined or dropped.
- A missing capability (no tests, no auth) is a BLOCKER with a pointer to `/bq-feature`.
- A dependency or tool found without a recorded decision is a finding, not a rewrite.

## Output

```
Audit: <b> blockers, <h> high, <m> medium, <l> low    areas: <audited>/<total>
Report: .bequite/audits/FULL_PROJECT_AUDIT.md
Next: /bq-fix "B-1"
```

## Quality gate

Every finding is severity-tagged, cited and has a fix; the coverage matrix is honest; systemic patterns went to `MISTAKE_MEMORY.md`.

## Next Command Recommendations (typical)

`/bq-fix "B-1"` to start on blockers · `/bq-red-team` for what an audit misses · `/bq-plan` when the findings need a plan.
