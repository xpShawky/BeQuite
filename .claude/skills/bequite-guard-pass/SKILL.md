---
name: bequite-guard-pass
description: Guard Pass — reactive second-pass quality gates that catch common AI-generated failure modes after work is produced and before it ships. Code guard (hallucinated APIs, hardcoded success, catch-alls), test guard (over-mocking, fake success, missing regressions), docs guard (nonexistent functions, out-of-sync counts). Runs after implementation/tests, before verify/release/docs-claims.
---

# bequite-guard-pass — second-pass failure-mode gates

## Purpose

After the agent produces work, run a **reactive review pass** targeting the failure modes AI-generated work specifically exhibits. Concept adapted from the guard-skills pattern (amElnagdy/guard-skills — concept only: no code copied, no dependency installed; see `docs/architecture/GUARD_PASS_STRATEGY.md`). Markdown-only, no scripts, no network, no credentials.

## When this skill activates

After `/bq-implement` / `/bq-feature` / `/bq-fix` produce code · after `/bq-test` writes tests · before `/bq-verify` and `/bq-release` · before any "docs are accurate" claim · on `/bq-review` for AI-generated diffs (delegate-mode reviews especially).

## When NOT to use

During initial writing (this is a *reactive* pass, not a style guide); on unchanged code; as a replacement for `/bq-review` (review = spec + quality; guard = AI-failure-mode hunt — they complement).

## Code guard checklist

- **Hallucinated APIs** — every imported symbol/method exists (check the actual package/source, not memory; PhantomRaven rule applies)
- **Hardcoded success** — return values/statuses faked to pass; success paths that can't fail
- **Broad catch-alls** — `except Exception: pass` / empty `catch` swallowing errors
- **Premature/over-abstraction** — interfaces with one implementation, config for things that never vary
- **Copy-from-similar bugs** — code pasted from a sibling with stale identifiers/conditions
- **Bad naming / broken contracts** — function does more/less than its name; signature drift from callers

## Test guard checklist

- Tests asserting implementation details (private state, call order without reason)
- **Over-mocking** — mocks so deep nothing real is tested; mock-returns-mock chains
- Duplicate test bodies; tests that pass with the feature deleted (catch nothing)
- **Missing regression tests** — fixed bugs without a guard test (feeds `/bq-verify regressions` ledger)
- **Fake success** — skipped/`.todo` tests counted as passing; assertions on truthy instead of values

## Docs guard checklist

- Docs claiming functions/commands that don't exist (verify against actual files)
- README examples that wouldn't run as written
- commands.md / counts out of sync with `.claude/commands/` + `.claude/skills/` actual file counts (feeds `/bq-verify drift`)
- Changelog claims unsupported by the diff; broken install instructions

## Output format

`.bequite/audits/GUARD_PASS_REPORT.md` — per finding: guard type · severity · `file:line` quoted evidence (citation-or-strike; no evidence = struck) · suggested fix. Verdict: PASS / FINDINGS (n) / BLOCKED (release-stopping). Report-only by default; fixes applied on user approval or in auto mode when R1-safe.

## Quality gate

A Guard Pass that finds nothing must state what it checked (files + checklists run) — "no findings" without coverage evidence is itself a weasel claim. Platform-specific guards (WordPress/Woo etc.) are added per-project only when that project needs them — none ship by default.
