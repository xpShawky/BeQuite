# Skill Quality Audit

> Produced by `/bq-skill-audit`. Report-only by default; repairs on user approval. This is the **seed run** (alpha.19, 2026-06-11) — first structured pass over all 26 skills.

**Skills audited:** 26 · **Method:** Glob + per-file section check + frontmatter check + cross-listing vs workflow-advisor/CLAUDE.md/README

---

## Summary

| Verdict | Count | Skills |
|---|---|---|
| PASS | 23 | all not listed below |
| IMPROVE (low) | 3 | problem-solver · multi-model-planning · workflow-advisor |

No merge / split / archive candidates this run. No HIGH findings.

## Findings

| # | Skill | Severity | Finding | Evidence | Proposed repair |
|---|---|---|---|---|---|
| 1 | `bequite-problem-solver` | LOW | Thinnest specialist; no worked example of the binary-search/bisect procedure | SKILL.md body ≈ shortest of the specialist tier | Add one worked diagnostic example (alpha.20 backlog) |
| 2 | `bequite-multi-model-planning` | LOW | Body retains some v0.x phasing language despite alpha.16 header fix | strategy doc cross-ref updated alpha.16; skill body lagged | Sweep stale phase references (alpha.20 backlog) |
| 3 | `bequite-workflow-advisor` | MEDIUM→resolved | Counts go stale every release (44/21 → now 46/26) | description field updated this pass (alpha.19) | ✅ fixed in alpha.19; add to release checklist: bump advisor counts at every version |
| 4 | `bq-review` command | — (false alarm) | Live skill-list showed degraded description ("/bq-review — review changes") | **Disk check: frontmatter intact at bq-review.md:2** — display truncation, not a defect | none |

## Trend baseline (for next run to compare)

26 skills · 0 HIGH · 1 MEDIUM (resolved in-pass) · 2 LOW (backlogged) · largest: frontend-design-system (master tier — exempt via references/) · all descriptions ≤ ~300 chars after alpha.16+19 trims · all have When-NOT-to-use + Quality gate (alpha.15 repairs holding)

**Next run due:** after alpha.21, or when a skill misfires.
