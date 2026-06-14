# Command Execution Contract (alpha.20 — 12 steps)

> **The single citable contract every BeQuite command follows.** When a command file says "per the execution contract," it means these 12 steps, in this order. Commands may compress steps that don't apply (read-only commands skip 7–9) but may never reorder or silently skip an applicable step.

**Status:** active · **Adopted:** alpha.19; **upgraded alpha.20** — skill selection became automatic (steps 2–4); **upgraded alpha.22** — step 12 became the Command Router multi-recommendation block
**Deep references:** `HARNESS_AND_PROMPT_QUALITY.md` (authoring standard) · `MEMORY_FIRST_BEHAVIOR.md` · `WORKFLOW_GATES.md` · `CONTEXT_ENGINEERING.md` · `AUTO_SKILL_ROUTING_STRATEGY.md` (steps 2–4) · `WORKFLOW_COMMAND_ROUTER.md` (step 12) · `CLAUDE_CODE_HOOKS_STRATEGY.md` (machine layer)

---

## The 12 steps

### 1. Memory preflight
Read core state first, focused reads only: `PROJECT_STATE` · `CURRENT_MODE` · `CURRENT_PHASE` · `WORKFLOW_GATES` · `LAST_RUN` · `MISTAKE_MEMORY` (top entries) · `PROJECT_DNA` + `WORKING_NOTES` for multi-step work · `CONTEXT_SUMMARY` when resuming. Domain memory (design/, writing/, presentations/, jobs/, money/, skills/) only when the task touches it. Never load all of `.bequite/`.

### 2. Skill registry check (alpha.20)
Load `.bequite/skills/SKILL_REGISTRY.md` — the token-cheap routing index — NOT the skill files. If the registry is missing or drifted from the live skill dirs, rebuild via Glob and flag for `/bq-skill-audit`.

### 3. Task classification (alpha.20)
Classify the request into domains per `SKILL_ROUTER.md`, using (in priority order): user text → invoking command → files present / repo type → mode + phase → memory (PROJECT_DNA, MISTAKE_MEMORY, MODE_HISTORY) → risk tier of likely-touched paths → requested output type.

### 4. Automatic skill selection (alpha.20; **skills-first, global — alpha.25**)
Select skills per the domain map + cross-cutting auto-attach + mode sizing (fast = smallest safe set · deep = broader · token-saver = lazy-load · delegate = skills named in the task pack). **The user never has to name skills** — but an explicit user choice overrides routing. Emit the `Skill Selection:` block (selected + reasons; notable not-selected + reasons) in the output. Load only the selected SKILL.md files.

**Skills-first is a GLOBAL hard rule (alpha.25):** this happens BEFORE any real work, for **every** command — workflow commands AND capability commands (course, presentation, reference, offer, automation, brand-kit, …) AND maintenance. The `Skill Selection:` block is the first substantive thing the command emits; you do not write a plan, generate content, edit a file, or call a tool for the task until skills are selected and announced. A command that acts before announcing its skills is a contract violation. (Trivial read-only commands — now/help/explain — are exempt.)

### 5. Gate check
Verify this command's required gates are `✅` in the gate ledger. If not: **refuse**, name the missing gate, recommend the prerequisite command, stop. ("You're trying to run X, but Y must be completed first.")

### 6. Scope detection
Parse the user request. Separate **stated scope** from **inferred scope**. If scope was inferred from assumptions rather than user text: either ask ONE high-value question, or (in auto mode) log the assumption to `ASSUMPTIONS.md` and proceed only if the assumption is low-risk. **Uncertain scope on a risky action is a hard human gate** (AUTO_MODE_STRATEGY).

### 7. Required research check — the no-research-repeat rule
Before researching: check `.bequite/research/` for an existing report covering this domain. Reuse + cite it; research only the delta. New research lands in `.bequite/research/<DOMAIN>_RESEARCH_REPORT.md` so the next run can reuse it. Depth per mode: deep = 11 dims · fast = 3 dims · token-saver = reuse-only unless gap is blocking.

### 8. Plan or task check → Action
For multi-file work: confirm a plan exists (`IMPLEMENTATION_PLAN.md` or feature mini-spec) and a File-Responsibility Map for >5-file changes. New BeQuite features additionally follow the 15-step feature-addition workflow (CLAUDE.md rule 13). Plans carry a per-phase **Execution Profile** and task lists a per-task one (selected skills · recommended model+tier · effort · confidence — `TASK_EXECUTION_PROFILE.md`). Then act: smallest safe change · failing-test-first where tests exist · new code matches `PROJECT_DNA.md` · no drive-by refactors · file edits respect `FILE_RISK_RULES.md` — R3 paths require explicit user confirmation even in auto mode.

### 9. Verification (+ **post-phase verify gate — alpha.25**)
Run the relevant checks (build/test/lint/visual per scope). **Evidence over claims:** record command + exit code + key output in `EVIDENCE_LOG.md` (or paste inline for small runs). No banned weasel words. If unverified, say `UNVERIFIED:` explicitly. **After implementing any phase or task, run test + verification for what was just built — before moving on** (select the verification skills first per step 4: testing-gate, guard-pass, security-reviewer/system-design for risky domains, frontend-quality for UI). Phase is not "done" until its named tests pass with evidence; a failure routes to `/bq-fix`, not to the next phase.

### 10. Report
Lead with outcome. State: what was done · files changed · skill selection (step 4 block) · evidence · remaining issues · verification status (PASS / PARTIAL / FAIL — honestly).

### 11. Memory writeback
`LAST_RUN` · `WORKFLOW_GATES` (gate state changes) · `CURRENT_PHASE` (phase changes) · `AGENT_LOG` (always for real actions) · `CHANGELOG [Unreleased]` (when files/behavior changed — **the most-skipped step; do not skip it**) · `MISTAKE_MEMORY` (when a lesson surfaced) · `MODE_HISTORY` (mode runs) · **`SKILL_USAGE_LOG`** (selection + outcome, alpha.20) · `WORKING_NOTES` / `CONTEXT_SUMMARY` (long tasks, at task boundaries).

### 12. Next Command Recommendations (Command Router, alpha.22)
Every non-trivial command ends with the router block — vocabulary = catalog IDs (`.bequite/commands/COMMAND_ID_MAP.md`), routes from `COMMAND_ROUTER.md`:

```
Next Command Recommendations:
Required next:         <ID> <cmd> — reason — can auto-run: yes/no — why
Recommended set (2–6): <ID> <cmd> <args> | Reason | Skills likely used | Can auto-run
Optional accelerators: <cmd> — why it may help now
Do not run yet:        <cmd> — missing gate / artifact / order reason
```

Gate-aware — a command whose gates aren't met may only appear under "Do not run yet" with the missing gate named. Capability commands (C#) appear only on task signals — never pad the set. **Auto mode** doesn't invoke slash commands literally; it runs the equivalent internal workflow and reports `Internal workflow executed: <ID list>`, then emits this block for what follows. Non-trivial routing decisions append one line to `NEXT_COMMAND_LOG.md`. Trivial reads (`/bq-now`, `/bq-help`, `/bq-explain`) keep the old single-next form. Full spec: `docs/architecture/WORKFLOW_COMMAND_ROUTER.md`.

---

## Enforcement layers

| Layer | Enforces | Mechanism |
|---|---|---|
| This contract | all 12 steps | convention — the agent honors it; commands cite it |
| Skill router | steps 2–4 | registry + domain map (`AUTO_SKILL_ROUTING_STRATEGY.md`) |
| Command router | step 12 | ID map + routes (`WORKFLOW_COMMAND_ROUTER.md`) — recommends, never bypasses gates |
| Workflow gates | step 5 | gate ledger refusal |
| Hard human gates | steps 6/8 | 17 pause points in `/bq-auto` |
| File-risk rules | step 8 | `FILE_RISK_CLASSIFICATION.md` tiers |
| Hooks (opt-in) | destructive ops · secrets · weasel words | machine — exit-2 block (`CLAUDE_CODE_HOOKS_STRATEGY.md`) |

## Compressions allowed

- **Read-only commands** (`/bequite`, `/bq-now`, `/bq-help`, `/bq-explain`, `/bq-suggest`): steps 1–5 + 10 + 12 only (suggest still runs routing steps 2–4 to recommend skills)
- **Hotfixes / doc-only:** may compress 6–8 plan/research portions; never 9 or 11
- **Token-saver mode:** compresses the SIZE of each step (registry summary instead of skill files; focused reads; compact report), never the SEQUENCE
- **Trivial one-file tasks:** skill selection capped at 2 skills (over-triggering is a routing defect)
