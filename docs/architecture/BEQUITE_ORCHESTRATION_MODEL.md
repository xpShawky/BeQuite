# BeQuite Orchestration Model (global — not only Auto Mode)

One central brain map for the whole system. Every major workflow — not just `/bq-auto` — references this model via the **`bequite-orchestrator` skill** and the source-of-truth map at `.bequite/state/ORCHESTRATION_MAP.md`. When there is confusion, conflict, missing capability, duplicated workflow, or an unclear next step, the agent returns to the Orchestration Map and treats it as authoritative.

## 1. The pipeline

```
User intent
→ Workflow Command Router   (what should happen next?)
→ Skill Router              (which expert procedures?)
→ System Design Risk Check  (what breaks under concurrency/failure?)
→ Confidence Forecast       (how likely is success; what's unknown?)
→ Task Planning             (file map, atomic tasks, acceptance criteria)
→ Implementation            (smallest safe change, risk-tier aware)
→ Guard Pass                (AI-failure-mode hunt on the output)
→ Verification              (evidence: command + exit code + output)
→ Evidence Log              (durable proof)
→ Memory Writeback          (state, gates, logs, lessons)
→ Next Command Recommendations
```

## 2. Layer table

| Layer | Does | Reads | Writes | Activates | Prevents |
|---|---|---|---|---|---|
| Command Router | picks next command/step | ID_MAP, COMMAND_ROUTER, gates, phase | NEXT_COMMAND_LOG | every non-trivial command (contract step 12) | wrong-order work, dead ends |
| Skill Router | selects expert skills | SKILL_REGISTRY, SKILL_ROUTER | SKILL_USAGE_LOG | contract steps 2–4 | amateur output, forgotten expertise |
| System Design Risk Check | structured failure reasoning | SYSTEM_DESIGN_REASONING_STANDARD | risk block in plan/spec | risky domains (payments, inventory, auth, concurrency…) | pretty-but-broken features |
| Confidence Forecast | banded success % + evidence level | CONFIDENCE_RULES, TASK_CONFIDENCE | forecast blocks | every plan/task | overconfidence, hidden uncertainty |
| Task Planning | file map + atomic tasks | plan/scope artifacts | IMPLEMENTATION_PLAN, TASK_LIST, CURRENT_TASK | W1.4/W2.1 | spaghetti, scope creep |
| Implementation | smallest safe change | task + FILE_RISK_RULES | code + logs | W2.x | drive-by refactors, R3 surprises |
| Guard Pass | second-pass AI-failure hunt | guard-pass skill checklists | GUARD_PASS_REPORT | post-implement/test, pre-verify/release | hallucinated APIs, fake tests, doc drift |
| Verification | evidence-backed checks | VERIFY procedures, regression ledger | VERIFY_REPORT, EVIDENCE_LOG | W4.1 | "should work" shipping |
| Memory Writeback | persist everything durable | — | LAST_RUN, gates, AGENT_LOG, CHANGELOG, lessons | contract step 11 | amnesia, repeated mistakes |
| Context Compaction | pressure-triggered externalization | CONTEXT_COMPACTION_RULES | CONTEXT_SUMMARY, WORKING_NOTES, CURRENT_TASK | ~40/60/75/85% pressure | context rot, lost decisions |

## 3. Conflict + missing-capability protocol

**Conflict** (two commands seem right, two skills overlap, routers disagree, duplicated workflow suspected): stop choosing by vibe → open `ORCHESTRATION_MAP.md` → apply its category boundaries and "near-miss" distinctions (audit≠review, scope≠spec≠plan, pain-radar≠make-money…) → if still ambiguous, ask ONE high-value question.

**Missing capability** (no command/skill/workflow fits): never pretend. Emit:

```
Missing Capability Detected:
- Needed capability:
- Why existing commands/skills are not enough:
- Temporary workaround:
- Recommended new skill/command/spec:
- Should this be built now or parked?
- Confidence:
```

…then log it to `OPEN_QUESTIONS.md` / `FEATURE_EXPANSION_ROADMAP.md` (feature-workflow step 1) and continue with the workaround only if safe. Wired into: `/bq-suggest`, `/bq-plan`, `/bq-auto`, `/bq-skill-audit`, both routers.

## 4. Who must consult the orchestrator

`/bequite` · `/bq-suggest` · `/bq-discover` · `/bq-plan` · `/bq-auto` · `/bq-implement` · `/bq-review` · `/bq-verify` · `/bq-skill-audit` — before choosing commands or skills, these check the Orchestration Map (cheap: it's a compact index, not the full corpus). All other commands inherit orchestration through contract step 12 + the routers. This is markdown-based — a skill plus a source-of-truth map, **not** a runtime.
