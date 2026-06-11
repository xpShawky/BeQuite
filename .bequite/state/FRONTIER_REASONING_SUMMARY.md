# Frontier Reasoning Summary — the 10 rules

> The minimum operating bar for ANY model working on BeQuite (or a BeQuite-managed project). Short on purpose — this card goes into every delegate task pack and is re-read at session start. Full playbook: `docs/architecture/FRONTIER_MODEL_OPERATING_PLAYBOOK.md`.

1. **Recover memory before acting.** CONTEXT_SUMMARY → LAST_RUN → WORKING_NOTES → gates. Never act on a stale picture.
2. **Verify current reality before modifying anything.** The repo may have moved past the request. Audit before adding; never duplicate existing work under a new name.
3. **Separate user-facing capabilities from internal reliability features.** Label honestly (FEATURE_TYPE_TAXONOMY).
4. **Never create a second source of truth.** Extend or index the existing doc.
5. **Turn vague tasks into scoped tasks.** Stated scope vs inferred scope; one artifact per task; ≤5 files or map it first.
6. **Attach confidence to tasks** — banded %, with why, that MOVES as evidence arrives. Never 100 without the rule.
7. **Mark facts, assumptions, and unknowns.** verified / inferred / assumed / UNVERIFIED — every claim gets a label.
8. **Use evidence logs for claims.** Command + exit code + output in EVIDENCE_LOG, or the claim is UNVERIFIED.
9. **Do not claim done without verification.** No weasel words. PARTIAL/FAIL honestly beats fake PASS.
10. **Update memory, logs, and next action.** LAST_RUN · AGENT_LOG · CHANGELOG · SKILL_USAGE_LOG · one recommended next command. Writeback is part of the task, not an extra.
