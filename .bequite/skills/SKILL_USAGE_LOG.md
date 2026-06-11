# Skill Usage Log

> Append-only record of router selections + outcomes. Written at memory-writeback (contract step 11). Read by `bequite-workflow-advisor` (pattern learning) and `/bq-skill-audit` (orphan + over-trigger detection).

## Entry format

```markdown
## <ISO date> — <command> — "<task, condensed>"
**Domains:** <classified domains> · **Mode:** <mode>
**Selected:** skill-a (reason) · skill-b (reason)
**Not selected (notable):** skill-c (reason)
**Outcome:** SUCCESS / PARTIAL / FAIL · <one line>
**Routing quality:** good / over-triggered / under-triggered (+ note → MISTAKE_MEMORY if defect)
```

Pruning: archive entries older than ~90 days to `SKILL_USAGE_LOG-<date>.md`.

---

## Entries (newest at top)

## 2026-06-11 — /bq-auto deep — "add automatic skill routing" (alpha.20 — seed entry)
**Domains:** BeQuite self-maintenance, documentation · **Mode:** deep
**Selected:** skill-auditor (registry build is its new job) · context-engineer (multi-file pass) · anti-hallucination (claims verified — global-skills probe evidence)
**Not selected (notable):** frontend-design-system (no UI touched) · security-reviewer (no R3 paths beyond installer R2)
**Outcome:** SUCCESS — registry + router + strategy shipped
**Routing quality:** good
