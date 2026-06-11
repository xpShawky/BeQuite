# Task Confidence

> Per-task confidence tracking (alpha.21). `/bq-assign` seeds a block per task; `/bq-implement` and `/bq-verify` update the trajectory. Template below; entries follow.

## Task block template

```markdown
## <Task ID> — <goal, one line>
**Files to inspect:** <list> · **Files to change:** <list>
**Confidence trajectory:**
- Before work: NN% — <why>
- After inspection: NN% — <what reading the files changed>
- After implementation: NN% — <honest; can go DOWN>
- After verification: NN% — <tests/QA evidence ref → EVIDENCE_LOG>
**Evidence level:** verified | inferred | assumed | unknown
**Unknowns:** <list> · **Risks:** <list + FILE_RISK tier of touched paths>
**Required tests:** <commands> · **Rollback:** <one line>
```

Rules: trajectory must MOVE (a flat line means no calibration happened) · no 100% (see strategy) · final number cites evidence or says UNVERIFIED.

---

## Entries (newest at top)

(none yet — populates from /bq-assign onward)
