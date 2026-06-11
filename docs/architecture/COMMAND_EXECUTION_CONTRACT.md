# Command Execution Contract (alpha.19)

> **The single citable contract every BeQuite command follows.** When a command file says "per the execution contract," it means these 11 steps, in this order. Commands may compress steps that don't apply (read-only commands skip 6–8) but may never reorder or silently skip an applicable step.

**Status:** active · **Adopted:** alpha.19 (Fable Strengthening Pass) · consolidates alpha.15 preflight/writeback blocks + alpha.18 reliability rules into one contract
**Deep references:** `HARNESS_AND_PROMPT_QUALITY.md` (authoring standard) · `MEMORY_FIRST_BEHAVIOR.md` · `WORKFLOW_GATES.md` · `CONTEXT_ENGINEERING.md` · `CLAUDE_CODE_HOOKS_STRATEGY.md` (machine layer)

---

## The 11 steps

### 1. Memory preflight
Read core state first, focused reads only: `PROJECT_STATE` · `CURRENT_MODE` · `CURRENT_PHASE` · `WORKFLOW_GATES` · `LAST_RUN` · `MISTAKE_MEMORY` (top entries) · `PROJECT_DNA` + `WORKING_NOTES` for multi-step work · `CONTEXT_SUMMARY` when resuming. Domain memory (design/, writing/, presentations/, jobs/, money/) only when the task touches it. Never load all of `.bequite/`.

### 2. Gate check
Verify this command's required gates are `✅` in the gate ledger. If not: **refuse**, name the missing gate, recommend the prerequisite command, stop. ("You're trying to run X, but Y must be completed first.")

### 3. Scope detection
Parse the user request. Separate **stated scope** from **inferred scope**. If scope was inferred from assumptions rather than user text: either ask ONE high-value question, or (in auto mode) log the assumption to `ASSUMPTIONS.md` and proceed only if the assumption is low-risk. **Uncertain scope on a risky action is a hard human gate** (AUTO_MODE_STRATEGY).

### 4. Skill selection
Activate only the skills the scope needs (focused, not all 26). Master skills (e.g. `frontend-design-system`) coordinate their members. Record which skills activated in the final report.

### 5. Required research check — the no-research-repeat rule
Before researching: check `.bequite/research/` for an existing report covering this domain. Reuse + cite it; research only the delta. New research lands in `.bequite/research/<DOMAIN>_RESEARCH_REPORT.md` so the next run can reuse it. Depth per mode: deep = 11 dims · fast = 3 dims · token-saver = reuse-only unless gap is blocking.

### 6. Plan or task check
For multi-file work: confirm a plan exists (`IMPLEMENTATION_PLAN.md` or feature mini-spec) and a File-Responsibility Map for >5-file changes. New BeQuite features additionally follow the 15-step feature-addition workflow (CLAUDE.md rule 13).

### 7. Action
Smallest safe change. Failing-test-first where tests exist. New code matches `PROJECT_DNA.md`. No drive-by refactors. File edits respect `FILE_RISK_RULES.md` — high-risk paths require explicit user confirmation even in auto mode.

### 8. Verification
Run the relevant checks (build/test/lint/visual per scope). **Evidence over claims:** record command + exit code + key output in `EVIDENCE_LOG.md` (or paste inline for small runs). No banned weasel words. If unverified, say `UNVERIFIED:` explicitly.

### 9. Report
Lead with outcome. State: what was done · files changed · evidence · remaining issues · verification status (PASS / PARTIAL / FAIL — honestly).

### 10. Memory writeback
`LAST_RUN` · `WORKFLOW_GATES` (gate state changes) · `CURRENT_PHASE` (phase changes) · `AGENT_LOG` (always for real actions) · `CHANGELOG [Unreleased]` (when files/behavior changed — **the most-skipped step; do not skip it**) · `MISTAKE_MEMORY` (when a lesson surfaced) · `MODE_HISTORY` (mode runs) · `WORKING_NOTES` / `CONTEXT_SUMMARY` (long tasks, at task boundaries).

### 11. Next best command
End with one recommended next step. Gate-aware — never recommend a command whose gates aren't met.

---

## Enforcement layers

| Layer | Enforces | Mechanism |
|---|---|---|
| This contract | all 11 steps | convention — the agent honors it; commands cite it |
| Workflow gates | step 2 | gate ledger refusal |
| Hard human gates | steps 3/7 | 17 pause points in `/bq-auto` |
| File-risk rules | step 7 | `FILE_RISK_CLASSIFICATION.md` tiers |
| Hooks (opt-in) | destructive ops · secrets · weasel words | machine — exit-2 block (`CLAUDE_CODE_HOOKS_STRATEGY.md`) |

## Compressions allowed

- **Read-only commands** (`/bequite`, `/bq-now`, `/bq-help`, `/bq-explain`, `/bq-suggest`): steps 1–4 + 9 + 11 only
- **Hotfixes / doc-only:** may compress 5–6; never 8 or 10
- **Token-saver mode:** compresses the SIZE of each step (focused reads, compact report), never the SEQUENCE
