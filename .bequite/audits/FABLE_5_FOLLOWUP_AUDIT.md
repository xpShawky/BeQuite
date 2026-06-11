# Fable 5 Follow-up Audit (alpha.21)

**Run:** 2026-06-11 · Claude Fable 5 (no model switch) · honest classification of what alpha.19 really was.

---

## 1. What alpha.19 actually ADDED (new artifacts that didn't exist)

| Item | Type |
|---|---|
| `/bq-writing-dna` + skill + 5 writing templates | **User-facing capability** (the only big one) |
| `/bq-skill-audit` + skill + seed report | User-facing-ish maintenance capability (acts on BeQuite itself) |
| COMMAND_EXECUTION_CONTRACT (11 steps) | Internal — workflow strengthening |
| FILE_RISK_CLASSIFICATION + RULES | Internal — safety strengthening |
| PROMPT_ENGINEERING_STANDARD + PROMPT_PATTERNS | Internal — docs pattern |
| CONTEXT_SUMMARY + EVIDENCE_LOG | Internal — memory pattern |
| HARNESS/CONTEXT strategy indexes | **Docs only** (thin indexes over alpha.18 content) |
| PRESENTATION_BUILDER_STRATEGY | **Docs only** (consolidation; capability existed since alpha.13) |
| GAME_CHANGER_FEATURE_DISCOVERY tracker | Docs/roadmap ledger |
| AUTO_MODE uncertain-scope + R3 gates | Internal — workflow gate |
| Installer drift fix + ps1 BOM fix | Internal — bug fixes |

## 2. What alpha.19 only VERIFIED (no new work)

Hooks (alpha.18) · context-engineering core (alpha.18: PROJECT_DNA, WORKING_NOTES, CONTEXT_ENGINEERING.md) · Design Continuity full set (alpha.17) · presentation capability completeness (alpha.13) · mode definitions (alpha.12/15) · game-changer report existence (alpha.18).

## 3. What alpha.19 REUSED from alpha.17/18

The strategy indexes deliberately point at alpha.18's deep docs rather than rewriting them (correct call — single source of truth). The context-pack pattern NAMED what alpha.17/13 had already built implicitly. The evidence-over-claims rule came from alpha.18's anti-hallucination; alpha.19 only gave it a durable file.

## 4. What alpha.19 did NOT add

- No new user-facing capability beyond Writing DNA (+ skill-audit as maintenance)
- No confidence/probability reporting (this pass adds it)
- No model-discipline transfer doc (this pass adds it)
- No genuinely NEW game-changer discovery — the tracker **re-ranked known ideas**
- No machine-enforcement expansion · no live verification of anything

## 5. Game-changer tracker honesty check

**Old ideas re-ranked (not new):** regression ledger, drift detector, confidence surfacing, ship-readiness — all four came from alpha.18's GAME_CHANGER_FEATURES report. Workflow-export, automation/bot builder, data-to-product, 3D site builder, product movie, AI-service-business builder — all from the alpha.5+ roadmap or the alpha.18/CAPABILITY reports. **Professional Expert alias** — the only fresh item, and it's a docs-level composition.
**Verdict: the V1 tracker is a good LEDGER but was not a discovery sprint.** V2 (this pass) does actual discovery.

## 6. Honest type labels for the current surface

**Real user-facing capabilities (the user can DO a new thing):** Presentation Builder · Live UI Edit · UI Variants · Writing DNA · Make Money Finder · Job Finder · Spec writer · Explainer · Multi-model planning · Delegate mode (cost capability) · Skill Audit (maintenance capability)
**Internal reliability (valuable, but not "new things users do"):** execution contract · file-risk tiers · context summaries/DNA · hooks · evidence log · prompt patterns · skill routing (alpha.20) · drift/regression/ship-readiness PROPOSALS
**Workflow gates:** 23 ledger gates + 17 hard human gates + 3 design gates + uncertain-scope/R3
**Docs-only:** strategy indexes, taxonomy (this pass), playbook (this pass — docs + 1 skill)
**Roadmap-only:** everything in the trackers not yet built

## 7. What still feels missing (drives this pass)

1. **Calibrated confidence** — BeQuite says WHAT it will do but never HOW LIKELY it is to succeed → Part 1
2. **Model-discipline portability** — the operating discipline lives across 20+ docs; a cheaper model can't absorb it → Playbook + coach skill + 10-rule summary
3. **Genuine novelty pipeline** — discovery was re-ranking → Discovery V2 sprint
4. **A taxonomy** stopping the internal-vs-user-facing confusion permanently → FEATURE_TYPE_TAXONOMY
5. (Unchanged: live verification of everything remains a user action)

## 8. Professional Expert Mode review (Part 5 ruling)

Checked: it is exactly `deep + strict evidence (anti-hallucination, EVIDENCE_LOG mandatory) + safety scope (R3 awareness) + professional domain checklist (doctrine)`. **Ruling: composition alias is CORRECT — do not create a 5th mode.** A 5th mode would expand the conflict matrix ~25% for zero new capability. Documented as the `expert` composition in FEATURE_TYPE_TAXONOMY + commands.md note. The alias graduates from "proposed" to "documented" in the V1 tracker.
