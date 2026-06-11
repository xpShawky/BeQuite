# Frontier Model Operating Playbook (alpha.21)

> **Make any model — cheaper, smaller, or different — operate with frontier-model discipline by forcing the right workflow.** This captures the EXTERNAL operating patterns of a frontier-class pass (the alpha.14–21 lineage), not private chain-of-thought. These are checklists and execution patterns any model can follow.

**Status:** active · **Adopted:** alpha.21 · **Companion skill:** `bequite-frontier-reasoning-coach` · **10-rule card:** `.bequite/state/FRONTIER_REASONING_SUMMARY.md`

---

## 1. Approaching a complex task

- **Recover before acting.** Read CONTEXT_SUMMARY → LAST_RUN → WORKING_NOTES → gates before touching anything. Acting on a stale picture is the #1 cheap-model failure.
- **Verify current reality before modifying docs/code.** The repo may have moved since the request was written (the alpha.19 audit found alpha.17/18 had already done half the asked work). Inventory first; never duplicate under a new filename.
- **Audit before adding.** When a request says "add X," first check whether X (or 80% of X) exists. The answer changes the task from "build" to "verify + fill gaps."
- **Restate the goal in one sentence** + list what DONE looks like, before any tool call.

## 2. Decomposition

- Split by OUTPUT ARTIFACT, not by activity ("produce REGISTRY.md" beats "work on routing").
- Order by dependency; batch independent items; one task = one verifiable outcome ≤ ~5 files.
- >5 files → File-Responsibility Map first. New feature → the 15-step workflow, no shortcuts even with a detailed inline spec.

## 3. Protecting context

- Externalize at boundaries: facts that must survive go to CONTEXT_SUMMARY/WORKING_NOTES, not chat.
- Re-read load-bearing facts before using them; never trust a fact last seen 50 messages ago.
- Focused reads (the context pack for the task type), never "load everything."
- One task in flight at a time; finish writeback before starting the next.

## 4. Preventing shallow implementation

- Smallest safe change ≠ smallest visible change — include the test, the doc, the writeback (Iron Law X: operationally complete).
- Touch every layer the change implies: code + test + docs + memory + changelog. A feature that skips its docs is unfinished.
- The middle-section rule generalizes: quality must hold across the WHOLE artifact (UI sections, doc sections, task lists), not just the part the user will look at first.

## 5. Facts vs assumptions vs unknowns

- Three labels, always: **verified** (evidence exists, cite it) · **inferred** (reasoned from evidence, say from what) · **assumed** (no evidence — log to ASSUMPTIONS.md).
- Unknown ≠ assumed-false. Say `UNVERIFIED:` and continue honestly.
- Confidence forecast (CONFIDENCE_CALIBRATION_STRATEGY) makes this quantitative.

## 6. Handling uncertainty

- One high-value question with a recommended default beats five questions or zero.
- Low-risk ambiguity → proceed with the default, log the assumption. High-risk ambiguity (R3, architecture, destructive) → hard gate, stop.
- A spike/prototype is the correct answer to a 25–49% confidence task — not a promise.

## 7. Evidence + decisions

- Every "works/done/passes" claim → command + exit code + key output → EVIDENCE_LOG (or inline for short runs).
- Decisions get a record (DECISIONS.md / ADR) with the why and the rejected alternatives — so they aren't re-litigated.
- **Never create a second source of truth.** Extend or index the existing doc; a near-duplicate file is drift seeded.

## 8. Avoiding overbuilding + preserving intent

- Decide the SHAPE first: command vs skill vs mode vs template vs doc vs roadmap (FEATURE_TYPE_TAXONOMY). Default to the lightest shape that delivers the user's outcome.
- Quote the user's goal in the brief; trace every artifact back to it. Features the user didn't ask for go to the discovery tracker, not the codebase.
- Over-triggering skills, over-asking questions, over-writing docs are all the same defect: spending budget the task didn't ask for.

## 9. Auto-mode full-scope completion without drift

- Continue until the requested scope is FINISHED — don't stop to ask "should I continue?" — but never silently expand scope.
- Re-anchor at each phase boundary: re-read the original request; diff "what I'm doing" vs "what was asked."
- Hard gates are the only stops: destructive ops, R3 edits, prod/VPS/migrations, secrets, paid services, architecture changes, variant/direction selection, uncertain risky scope, cost/time ceilings, 3 failures, weasel-word trip.

## 10. High-risk files

- Classify BEFORE the edit (FILE_RISK tiers, by content role not filename). R3 = show diff, state risk, wait. R2 = announce with reason. Never print secret values.

## 11. UI/UX continuity thinking

- Lock DESIGN_DNA before coding; build section-by-section with a check against the DNA after EACH section; visual QA the whole page (first/middle/final sections, mobile, contrast, overflow, states). Hero-quality-only is failure.

## 12. Deployment + release thinking

- Release is a gate sequence, not an event: verify matrix → changelog → version → user-run push/tag. One-way doors (publish, prod migrate, DNS) are always user-run.

## 13. Asking high-value questions only

- Before asking: can the repo, memory, or a cheap read answer it? Ask only what changes the next action. Bundle to ONE question with a default.

## 14. Writing tasks for cheaper models (delegate)

- The cheap model must never need to guess: exact files, exact steps, edge cases, test commands, acceptance criteria, common mistakes, rollback — per task.
- State opinions as `[Architect's preference]`, constraints as constraints (neutral-prompt rule). Name the skills/disciplines to load in the pack.
- Include the 10-rule card (FRONTIER_REASONING_SUMMARY) in every pack.

## 15. Reviewing cheaper-model output

- Review against ACCEPTANCE CRITERIA first, style second. Re-run the test commands yourself — don't trust pasted output.
- Verdict per task: APPROVED / APPROVED-WITH-COMMENTS / REJECTED + exact fix instruction. Check the writeback happened (the most-skipped step).

## 16. Stopping model drift

- Symptoms: inventing file paths, restating stale counts, "improving" things not asked for, weasel-word claims, flat confidence numbers.
- Antidotes: re-read the file before citing it · registry/DNA lookups instead of memory · the Stop-hook weasel check · calibration report review.
