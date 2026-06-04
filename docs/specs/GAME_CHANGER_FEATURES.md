# Game-Changer Feature Proposals for BeQuite

**Status:** PROPOSAL / REPORT ONLY — per user instruction, none of the future-proposed features below are built yet. This is the ranked idea set with evidence + a BeQuite-specific design sketch for each, so a future release can pick them up.
**Generated:** 2026-06-04 (UTC) · alpha.18 research cycle
**Evidence base:** official Anthropic docs (hooks-guide, demystifying-evals, effective-harnesses, effective-context-engineering, best-practices) + cited security/practitioner research. Full citations at the bottom.

---

## The thesis (why a lightweight skill-pack is the right lever)

> "The problem is rarely the model. The problem is almost always the workflow around the model." — and as of Feb 2026 the best SWE-bench Verified agent still fails >20% of tasks; 66% of developers' #1 complaint is "almost right, but not quite."

The gaps below are **workflow gaps**, not model gaps — which is exactly what a markdown skill-pack can close without heavy infra. Each candidate is rated **leverage** (how much it raises output quality) × **fit** (how lightweight it is for BeQuite).

## What's being built NOW vs. proposed-for-later

| Candidate | This release (alpha.18)? |
|---|---|
| #1 Machine-enforced hard gates (`PreToolUse` deny hooks) | ✅ **BUILDING** (the hooks work you asked for) |
| #2 `Stop`-hook self-verify loop | ✅ **BUILDING** (shipped as opt-in hook + recipe) |
| #3 Regression ledger (every fixed bug → permanent test) | 🔭 proposed |
| #4 Generalized drift detection (API/schema/doc/dep) | 🔭 proposed |
| #5 Confidence + uncertainty surfacing | 🔭 proposed (partial: anti-hallucination rules land now) |
| #6 Session-memory re-injection + contradiction handling | 🔭 proposed (partial: context-engineering lands now) |
| #7 Spec→code→test traceability | 🔭 proposed |
| #8 Scoped maintenance-loop contract | 🔭 proposed |

---

## Ranked proposals (leverage × lightweight-fit)

### 1. Regression ledger — every fixed bug becomes a permanent, re-run test  ★ highest non-hook leverage
- **Gap it fills:** "almost right" regressions silently return; `MISTAKE_MEMORY.md` *records* mistakes but nothing *re-checks* them. Anthropic: start with **20–50 tasks from real failures**, keep regression suites at **~100% pass**, grade the outcome not the path, "an eval suite is a living artifact."
- **BeQuite design:** a markdown `.bequite/state/REGRESSION_LEDGER.md` (task → expected outcome → last status). `/bq-fix` appends a case on every fix; `/bq-verify` re-runs the ledger and refuses PASS if any case regressed. No DeepEval/Braintrust — markdown + the project's own test runner.
- **Leverage:** HIGH · **Effort:** S–M · **Why game-changer:** turns BeQuite's memory from *passive record* into an *active safety net* — the single biggest reliability gain after hooks, with zero deps.

### 2. Generalized drift detection (beyond UI)
- **Gap it fills:** alpha.17 catches *UI* drift; **75% of APIs drift from their specs**, and doc/schema/dependency drift rot silently. Agents that parse responses are *especially* sensitive to an undocumented field vanishing.
- **BeQuite design:** a `bequite-drift-detector` skill + `DRIFT_REPORT.md`, invoked by `/bq-audit` + `/bq-review`. Lightweight, proven pattern: on change, diff the contract (OpenAPI/schema/`docs/`/lockfile) and either flag or open a fix. Detection is markdown+diff; the comparison tools (oasdiff/Schemathesis/Spectral) stay **tool-neutral candidates**, never mandated.
- **Leverage:** HIGH (for API/data products) · **Effort:** M · **Why game-changer:** extends the proven continuity-gate idea to the parts of a system that break production silently.

### 3. Confidence + uncertainty surfacing
- **Gap it fills:** agentic **overconfidence** — agents that succeed 22% of the time predict 77%. The inverse of weasel-words: confidently wrong.
- **BeQuite design:** every `/bq-auto` step logs `confidence: high|med|low` + the single biggest unknown to `AGENT_LOG.md`; `low` confidence on a hard-gate category forces the pause. Pure memory convention; no infra. (The *enforcement half* — the `UNVERIFIED:` / "I don't know" forced-fork — lands in alpha.18's anti-hallucination rules.)
- **Leverage:** MED–HIGH · **Effort:** S · **Why game-changer:** makes risk *visible* before the agent acts, pairing with the 17 hard gates.

### 4. Session-memory re-injection + contradiction handling
- **Gap it fills:** session amnesia + **compounding bad decisions** (an agent reads its own prior bad pattern next session and follows it). What survives `/compact`: project-root CLAUDE.md + auto-memory (re-injected); path-scoped/nested rules are **lost**.
- **BeQuite design:** (a) a `SessionStart`/`compact`-matcher hook that re-injects `CURRENT_PHASE.md` + last-run + active doctrine after compaction; (b) a **"superseded-by"** field in `DECISIONS.md` / `MISTAKE_MEMORY.md` so a newer ruling explicitly retires an older one (no hallucinated hybrid). (alpha.18 lands the general context-engineering discipline; the `SessionStart` hook + superseded-by convention are the proposed next step.)
- **Leverage:** MED–HIGH · **Effort:** S–M · **Why game-changer:** stops the "memory becomes a liability" failure mode that plagues persistent-memory tools.

### 5. Spec → code → test traceability (living specs)
- **Gap it fills:** no audit trail linking a behavior change → spec change → requirement; specs rot. SDD matured fast (Spec Kit 90k+ stars, 30+ agent integrations); traceability is a **compliance requirement** in regulated industries.
- **BeQuite design:** extend the existing `/bq-spec` with a traceability table (spec item → files → tests) in `specs/<slug>/spec.md`; `/bq-verify` flags any spec item with no linked test. Pure markdown.
- **Leverage:** MED (HIGH for regulated) · **Effort:** S · **Why game-changer:** low-effort extension of a command BeQuite already ships; turns specs into a governing contract.

### 6. Scoped, report-only maintenance loop
- **Gap it fills:** recurring maintenance (CI repair, deploy-verify, dep bumps) needs an agent that inspects state, acts *in scope*, reports — on a schedule, not a held-open turn. Claude Code now has background watchers / `/autofix-pr` / Routines.
- **BeQuite design:** a `bequite-maintenance-loop` skill defining the `inspect → act-in-scope → report` contract + `MAINTENANCE_LOG.md`. Tool-neutral on the runner (Claude Code Routines / cron / GitHub Actions documented as candidates, none mandated). The *discipline* is lightweight; the *runtime* is platform infra BeQuite orchestrates but doesn't build.
- **Leverage:** MED · **Effort:** M · **Why game-changer:** unlocks unattended upkeep without BeQuite owning a daemon (stays within ADR-004).

### (Built this release) 7–8. Machine-enforced gates + self-verify loop via hooks
- Covered by the alpha.18 hooks work (`PreToolUse` deny for destructive/secret/protected; opt-in `Stop` self-verify recipe). Listed here for completeness because they ranked #1 and #8 in the research's own leverage table — they are the structural backbone the others build on.

---

## Recommended build order (for a future release, NOT now)
1. **Regression ledger** (#1) — biggest non-hook reliability gain, S–M effort, composes with the hooks shipping now.
2. **Confidence surfacing** (#3) — S effort, pairs with the 17 gates + the anti-hallucination rules landing in alpha.18.
3. **Generalized drift detection** (#2) — extends the proven alpha.17 continuity pattern to API/schema/doc/dep.

Then traceability (#5), session-memory re-injection (#4), maintenance loop (#6).

## What NOT to do (lightweight guardrails)
- Don't build a heavy eval framework, a memory database, a graph indexer, or a daemon — markdown ledgers + the project's own runner + opt-in hooks cover the same ground (ADR-001 / ADR-004).
- Don't mandate any drift/contract tool — keep them tool-neutral candidates (ADR-003).
- Don't auto-enable any hook or background runner — RCE-vector risk + the opt-in principle (see `docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md`).
- Don't add depth to CLAUDE.md — push it into skills (Anthropic: bloated CLAUDE.md → ignored rules).

## Sources
Claude Code Hooks guide · Anthropic "Demystifying evals for AI agents" · "Effective harnesses for long-running agents" · "Effective context engineering" · Claude Code best practices · 3-layer self-verify loop (dev.to) · Dosu doc-drift with Actions · PactFlow schemas-as-contracts · SDD-2026 (Devoteam) · persistent-memory + agents-repeat-questions (dev.to / Augment) · agentic overconfidence (arXiv 2602.06948) · "AI agents expectations vs reality" (aimultiple) · "skill gap not model failure" (pooya.blog). Full URLs in `.bequite/research/` research notes for this cycle.
