# Command Execution Contract (alpha.20 — 12 steps)

> **The single citable contract every BeQuite command follows.** When a command file says "per the execution contract," it means these 12 steps, in this order. Commands may compress steps that don't apply (read-only commands skip 7–9) but may never reorder or silently skip an applicable step.

**Status:** active · **Adopted:** alpha.19; **upgraded alpha.20** — skill selection became automatic (registry check + task classification + auto-selection, steps 2–4)
**Deep references:** `HARNESS_AND_PROMPT_QUALITY.md` (authoring standard) · `MEMORY_FIRST_BEHAVIOR.md` · `WORKFLOW_GATES.md` · `CONTEXT_ENGINEERING.md` · `AUTO_SKILL_ROUTING_STRATEGY.md` (steps 2–4) · `CLAUDE_CODE_HOOKS_STRATEGY.md` (machine layer)

---

## The 12 steps

### 1. Memory preflight
Read core state first, focused reads only: `PROJECT_STATE` · `CURRENT_MODE` · `CURRENT_PHASE` · `WORKFLOW_GATES` · `LAST_RUN` · `MISTAKE_MEMORY` (top entries) · `PROJECT_DNA` + `WORKING_NOTES` for multi-step work · `CONTEXT_SUMMARY` when resuming. Domain memory (design/, writing/, presentations/, jobs/, money/, skills/) only when the task touches it. Never load all of `.bequite/`.

### 2. Skill registry check (alpha.20)
Load `.bequite/skills/SKILL_REGISTRY.md` — the token-cheap routing index — NOT the skill files. If the registry is missing or drifted from the live skill dirs, rebuild via Glob and flag for `/bq-skill-audit`.

### 3. Task classification (alpha.20)
Classify the request into domains per `SKILL_ROUTER.md`, using (in priority order): user text → invoking command → files present / repo type → mode + phase → memory (PROJECT_DNA, MISTAKE_MEMORY, MODE_HISTORY) → risk tier of likely-touched paths → requested output type.

### 4. Automatic skill selection (alpha.20)
Select skills per the domain map + cross-cutting auto-attach + mode sizing (fast = smallest safe set · deep = broader · token-saver = lazy-load · delegate = skills named in the task pack). **The user never has to name skills** — but an explicit user choice overrides routing. Emit the `Skill Selection:` block (selected + reasons; notable not-selected + reasons) in the output. Load only the selected SKILL.md files.

### 5. Gate check
Verify this command's required gates are `✅` in the gate ledger. If not: **refuse**, name the missing gate, recommend the prerequisite command, stop. ("You're trying to run X, but Y must be completed first.")

### 6. Scope detection
Parse the user request. Separate **stated scope** from **inferred scope**. If scope was inferred from assumptions rather than user text: either ask ONE high-value question, or (in auto mode) log the assumption to `ASSUMPTIONS.md` and proceed only if the assumption is low-risk. **Uncertain scope on a risky action is a hard human gate** (AUTO_MODE_STRATEGY).

### 7. Required research check — the no-research-repeat rule
Before researching: check `.bequite/research/` for an existing report covering this domain. Reuse + cite it; research only the delta. New research lands in `.bequite/research/<DOMAIN>_RESEARCH_REPORT.md` so the next run can reuse it. Depth per mode: deep = 11 dims · fast = 3 dims · token-saver = reuse-only unless gap is blocking.

### 8. Plan or task check → Action
For multi-file work: confirm a plan exists (`IMPLEMENTATION_PLAN.md` or feature mini-spec) and a File-Responsibility Map for >5-file changes. New BeQuite features additionally follow the 15-step feature-addition workflow (CLAUDE.md rule 13). Then act: smallest safe change · failing-test-first where tests exist · new code matches `PROJECT_DNA.md` · no drive-by refactors · file edits respect `FILE_RISK_RULES.md` — R3 paths require explicit user confirmation even in auto mode.

### 9. Verification
Run the relevant checks (build/test/lint/visual per scope). **Evidence over claims:** record command + exit code + key output in `EVIDENCE_LOG.md` (or paste inline for small runs). No banned weasel words. If unverified, say `UNVERIFIED:` explicitly.

### 10. Report
Lead with outcome. State: what was done · files changed · skill selection (step 4 block) · evidence · remaining issues · verification status (PASS / PARTIAL / FAIL — honestly).

### 11. Memory writeback
`LAST_RUN` · `WORKFLOW_GATES` (gate state changes) · `CURRENT_PHASE` (phase changes) · `AGENT_LOG` (always for real actions) · `CHANGELOG [Unreleased]` (when files/behavior changed — **the most-skipped step; do not skip it**) · `MISTAKE_MEMORY` (when a lesson surfaced) · `MODE_HISTORY` (mode runs) · **`SKILL_USAGE_LOG`** (selection + outcome, alpha.20) · `WORKING_NOTES` / `CONTEXT_SUMMARY` (long tasks, at task boundaries).

### 12. Next best command
End with one recommended next step. Gate-aware — never recommend a command whose gates aren't met.

---

## Enforcement layers

| Layer | Enforces | Mechanism |
|---|---|---|
| This contract | all 12 steps | convention — the agent honors it; commands cite it |
| Skill router | steps 2–4 | registry + domain map (`AUTO_SKILL_ROUTING_STRATEGY.md`) |
| Workflow gates | step 5 | gate ledger refusal |
| Hard human gates | steps 6/8 | 17 pause points in `/bq-auto` |
| File-risk rules | step 8 | `FILE_RISK_CLASSIFICATION.md` tiers |
| Hooks (opt-in) | destructive ops · secrets · weasel words | machine — exit-2 block (`CLAUDE_CODE_HOOKS_STRATEGY.md`) |

## Compressions allowed

- **Read-only commands** (`/bequite`, `/bq-now`, `/bq-help`, `/bq-explain`, `/bq-suggest`): steps 1–5 + 10 + 12 only (suggest still runs routing steps 2–4 to recommend skills)
- **Hotfixes / doc-only:** may compress 6–8 plan/research portions; never 9 or 11
- **Token-saver mode:** compresses the SIZE of each step (registry summary instead of skill files; focused reads; compact report), never the SEQUENCE
- **Trivial one-file tasks:** skill selection capped at 2 skills (over-triggering is a routing defect)
