# P1 Skill Patch Audit (alpha.24, 2026-06-13)

The two backlogged skill items from the alpha.23 quality matrix, now patched.

## bequite-problem-solver — PATCHED

**Was:** okay/thin-example (a solid skill with no end-to-end worked diagnostic). **Now:** added "The diagnostic workflow (alpha.24 strengthening)" — a 10-step ordered procedure (reproduce → expected/actual → symptom-vs-root → inspect-before-edit → check recent changes → check logs → smallest fix → regression test → evidence → mistake memory), an explicit anti-pattern list (fix-by-vibes, broad refactors, unrelated edits, claim-without-rerun, symptom-suppression), and a **general worked example** ("button click does nothing" → no-request → console error → broken prop contract from a partial rename → one-line fix + regression test + evidence) that generalizes to API-500 / fresh-clone-install / CLI-on-Windows. **Verdict: thin-example resolved → PASS.**

## bequite-multi-model-planning — PATCHED

**Was:** okay/stale-phasing (phase references predated the current mode + orchestration system). **Now:** added "Current-system alignment (alpha.24 refresh)" mapping the skill onto the 4 operating modes (deep/delegate primary; fast/token-saver skip), the orchestrator + routers, the correct P0–P5 phase meaning (not retired v2 IDs), evidence-based conflict resolution (no averaging; disagreements → OPEN_QUESTIONS), banded confidence, compaction, and the no-provider-integration rule. Added a **multimodal inputs** section (screenshot/PDF/scanned/image/deck/transcript/video-notes): source maps + confidence labels mandatory, "a model may only reason over a source actually inspected," NEEDS-REVIEW gating. **Verdict: stale-phasing resolved → PASS.**

## Registry effect

Both skills' quality notes update from "~ backlogged" to PASS in the next SKILL_REGISTRY refresh; the alpha.23 quality matrix's only two non-PASS skill rows are now cleared. No structural change to either skill's activation or routing.
