---
description: Full local verification before shipping. Install + lint + typecheck + unit + integration + build + smoke + frontend test + API smoke + CLI smoke. Writes VERIFY_REPORT.md.
---

# /bq-verify — full verification

You are running the full local verification matrix. Output: `.bequite/audits/VERIFY_REPORT.md` with green/red for each gate.

## Step 1 — Read context

- `.bequite/audits/DISCOVERY_REPORT.md` (find the right commands)
- `.bequite/state/PROJECT_STATE.md`

## Step 2 — Build the gate matrix

Based on what the project has (from DISCOVERY), enumerate gates. For each, attempt to run it.

| Gate | When applicable | How to run |
|---|---|---|
| Install (clean) | always | `rm -rf node_modules && npm ci` (or `pnpm install`, `pip install -e .`) |
| Lint | linter configured | `npm run lint`, `npx biome lint`, `npx ruff check` |
| Typecheck | TS or Python with mypy | `tsc --noEmit`, `mypy` |
| Unit tests | tests exist | the test command from package.json / pyproject.toml |
| Integration tests | separate suite | the integration command if separate |
| Build | build script present | `npm run build`, `cargo build`, `go build`, `python -m build` |
| Smoke (curl) | has HTTP server | `curl /healthz` (after starting server) |
| Frontend e2e | Playwright installed | `npx playwright test` |
| API smoke | API present | as smoke; or run e2e api tests |
| CLI smoke | CLI present | `<cli> --version`, `<cli> --help` |
| Secret scan | always | grep for `password = `, `api_key = `, `AKIA`, `sk_live_` |
| Lockfile sanity | package manifest present | only one of (yarn.lock, package-lock.json, pnpm-lock.yaml); `bun.lockb` if Bun |

Skip gates that don't apply (e.g. "Frontend e2e" if no `tests/e2e/` directory).

## Step 3 — Run each gate

For each applicable gate:
- Run the command (Bash tool)
- Capture exit code + key output lines
- Note duration (rough)

Mark each:
- ✅ green (exit 0, expected output)
- ⚠️ yellow (exit 0 but warnings)
- ❌ red (exit nonzero)
- ⏸ skipped (not applicable)

**Stop on first ❌ red gate** if user passes `--strict`. Otherwise run all and report.

## Step 4 — Write VERIFY_REPORT.md

```markdown
# Verify Report

**Generated:** <ISO 8601 UTC>
**Mode:** <strict | full>
**Overall:** <PASS | FAIL>

## Gate matrix

| Gate | Status | Duration | Output summary |
|---|---|---|---|
| Install (clean) | ✅ | 24s | 487 packages added |
| Lint | ✅ | 4s |  |
| Typecheck | ✅ | 8s | tsc --noEmit OK |
| Unit tests | ✅ | 12s | 47 passed |
| Integration tests | ⏸ | - | no separate suite |
| Build | ✅ | 31s | next build OK |
| Smoke curl /healthz | ✅ | 1s | HTTP 200 |
| Playwright e2e | ✅ | 18s | 24 passed |
| API smoke | ✅ | 5s | 11 endpoints OK |
| CLI smoke | ⏸ | - | no CLI |
| Secret scan | ✅ | 2s | no findings |
| Lockfile sanity | ✅ | 0s | pnpm-lock.yaml only |

## Failures

(empty if all green; otherwise per-gate detail)

## Warnings

(any yellow / non-fatal output of interest)

## Verdict

PASS — all applicable gates green. Ship-ready.

(or)

FAIL — <count> gate(s) failed. Address before /bq-release.
```

## Step 5 — Update state + log

- `.bequite/state/LAST_RUN.md` → `/bq-verify` + verdict
- `.bequite/state/CURRENT_PHASE.md` → "Phase 4 — Ship → verified" (if PASS)
- `.bequite/logs/AGENT_LOG.md` appended

## Step 6 — Report back

```
Verify: <PASS | FAIL>

Gates: <green-count> ✅  <yellow-count> ⚠️  <red-count> ❌  <skipped-count> ⏸

Report: .bequite/audits/VERIFY_REPORT.md

Next: /bq-release  (if PASS)
      /bq-fix <gate>  (if FAIL — start with the first failing gate)
```

## Rules

- **Honest verdict.** Don't claim PASS if any gate was red.
- **Cite the actual command run.** "Tests pass" is not enough; say `npm test → 47 passed in 12s, exit 0`.
- **Don't skip gates silently.** If a gate is "skipped", say WHY.
- **Article VI compliance:** the report must say what actually ran, in this session, against this code.

See `.claude/skills/bequite-release-gate/SKILL.md` for the deeper procedure (CI parity, ship-vs-not decision tree, etc.).

## Memory files this command reads

- `.bequite/audits/DISCOVERY_REPORT.md`
- `.bequite/state/PROJECT_STATE.md`
- `package.json` / equivalent manifest

## Memory files this command writes

- `.bequite/audits/VERIFY_REPORT.md` (new — overwrites; older ones can be preserved as VERIFY-<timestamp>.md if user wants)
- `.bequite/state/LAST_RUN.md`
- `.bequite/state/CURRENT_PHASE.md`
- `.bequite/logs/AGENT_LOG.md`

## Usual next command

- PASS → `/bq-release`
- FAIL → `/bq-fix`
