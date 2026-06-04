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
| Design continuity | frontend present | section-by-section vs the Design DNA → `.bequite/design/DESIGN_CONTINUITY_REPORT.md` exists + no BLOCKER/HIGH drift (alpha.17) |
| Visual QA | frontend present | render at highest browser tier → `.bequite/audits/VISUAL_QA_REPORT.md` (browser tier, or honest tier-3 note) (alpha.17) |
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

## Standardized command fields (alpha.6)

**Phase:** P4 — Release
**When NOT to use:** trivial change with no user impact (use `/bq-test` for a faster check); verify already ran < 1h ago + no new changes (cached state still valid).
**Preconditions:** `BEQUITE_INITIALIZED`, `TEST_DONE`, `REVIEW_DONE`
**Required previous gates:** `BEQUITE_INITIALIZED`, `TEST_DONE`, `REVIEW_DONE`
**Quality gate:**
- All applicable gates green
- `VERIFY_REPORT.md` written with per-gate status
- Honest PASS or FAIL (no "probably")
- Marks `VERIFY_PASS ✅` only on PASS
**Failure behavior:**
- Any required gate red → verdict = FAIL; do NOT mark `VERIFY_PASS`; recommend `/bq-fix`
- Optional gate yellow (warnings) → verdict can still be PASS; note in report
- CI ≠ local parity discovered → log to `MISTAKE_MEMORY.md`; fix the script that diverged
**Memory updates:** Sets `VERIFY_PASS ✅` on PASS. Updates `CURRENT_PHASE.md` to "P4 — verified". Appends parity-drift patterns to `MISTAKE_MEMORY.md`.
**Log updates:** `AGENT_LOG.md`. `VERIFY_REPORT.md` (overwrites or timestamps).

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

---

## Mistake memory update

When a verify gate fails, capture the **why** in MISTAKE_MEMORY if the failure is:
- A pattern (e.g. "TypeScript strict mode catches X every release; we keep silencing it without root-causing")
- Tied to a **prevention rule** that wasn't there before (e.g. "always run `npm ci` not `npm install` in CI — this release broke because of lockfile drift")
- A signal that the CI ≠ local parity is slipping

Skip MISTAKE_MEMORY for one-off transient failures (flaky e2e tests, rate-limited external API during smoke). Those are bug reports, not lessons.

See `.bequite/state/MISTAKE_MEMORY.md` template.

---

## Tool neutrality (global rule)

⚠ **Verify confirms what was built. The tools used to build it should already have decision sections from earlier phases.**

If `/bq-verify` detects a new dep or tool in the build that lacks a corresponding decision section in IMPLEMENTATION_PLAN.md, ADRs, or feature mini-specs:

- Mark `VERIFY_REPORT.md` with a "Tool justification" warning (not a blocker — verification is about working code, not architecture review)
- Suggest running `/bq-review` or `/bq-red-team` to close the gap before release

**Tool-neutrality at verify time is a documentation gap, not a runtime bug.** Fix in plan / spec, not in code.

The 10 decision questions every tool in the verified build should have answered:
1. What is the project type?
2. What is the actual problem?
3. What scale is expected?
4. What constraints exist?
5. What stack already exists?
6. What user experience is required?
7. What failure risks exist?
8. What tools are proven for this case?
9. What tools are overkill?
10. What tool gives the best output with the least complexity?

See `.bequite/principles/TOOL_NEUTRALITY.md` for the full rule.

---

## Evidence + Definition-of-Done (alpha.18)

`/bq-verify` does not PASS on assertions — it PASSes on **evidence**. For every gate, the report pastes the **actual command + exit code + key output** (not prose like "tests pass"). If you can't run a proof for a gate, mark it `UNVERIFIED` honestly — never claim a green you didn't see (Anthropic "show evidence rather than asserting success"; the trust-then-verify gap).

**Definition-of-Done gate** (before verdict = PASS): runnable + typecheck green + relevant tests green + **no stub/TODO/placeholder in changed files** + docs/memory updated + (if a `REGRESSION_LEDGER.md` exists) prior fixed-bug cases still pass. A frontend present → also the Design Continuity + Visual QA reports (below).

**Optional deterministic backstop:** teams can enable the opt-in `Stop`-hook self-verify recipe ("don't end the turn until build + tests pass") — see `docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md`. Not installed by default (BeQuite can't know your test command).

## Design Continuity Gate (alpha.17)

When a frontend exists, `/bq-verify` does not PASS on code-only checks. The matrix includes two frontend quality gates:

- **Design continuity** — a passing `.bequite/design/DESIGN_CONTINUITY_REPORT.md` (every section consistent with the DNA; no BLOCKER/HIGH drift; quality cliff closed). Run it via `bequite-frontend-design-system` if not already produced this cycle.
- **Visual QA** — a `.bequite/audits/VISUAL_QA_REPORT.md` from rendering the app at the highest available browser tier (Playwright MCP → project Playwright → code inspection + screenshots; never auto-install). Honest tier-3 is acceptable and must be labeled as such — do NOT claim a visual PASS you did not see (Article VI + banned weasel words).

If either is missing or failing when a frontend is present, verdict is **FAIL** (or PARTIAL with the specific gap). **Effort:** verification depth scales with `${CLAUDE_EFFORT}` (low/medium compact · high full · xhigh/Ultracode browser visual QA per section). Owner: `bequite-frontend-design-system`. Spec: `docs/architecture/DESIGN_CONTINUITY_GATE.md`.

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
