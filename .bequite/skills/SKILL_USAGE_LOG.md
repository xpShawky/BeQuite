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

## 2026-06-12 — alpha.22 consolidation pass (auto, deep)
**Task domains:** meta (command navigation, capability consolidation, guard system, localization)
**Selected:** skill-auditor (structure review) · anti-hallucination (evidence-cited audit + guard seed) · context-engineer (long multi-file pass) · workflow-advisor (router design) · frontier-reasoning-coach (deep mode)
**Not selected (notable):** frontend-design-system (no UI built) · presentation-builder (no deck)
**Outcome:** SUCCESS — 6 capability commands + 2 skills + command-router layer shipped; registry extended to 29
**Routing quality:** good — new domains added to router for C3-C8 + localization + guard-pass

## 2026-06-12 — post-alpha.22 maintenance pass (skill-audit baseline + drift + course PDF)
**Selected:** skill-auditor (3-skill baseline) · anti-hallucination (evidence-cited audits) · guard-pass (docs-guard style drift sweep) · localization-rtl (FIRST REAL EXERCISE — Arabic course PDF intake, RTL extraction artifacts identified) · orchestrator (remaining-work queryability wiring)
**Outcome:** SUCCESS — 3/3 skills PASS (structural); 2 drift findings fixed; PDF integrated as verified Reference A
**Routing quality:** good — localization-rtl auto-attach on Arabic-source work behaved as designed

## 2026-06-12 - alpha.23: /bq-offer build + tightening pass (deep)
**Selected:** product-strategist + make-money + writing-dna (offer design) · anti-hallucination (honest-selling rules + audit labels) · skill-auditor (matrices) · orchestrator (C11 wiring + conflict scan) · researcher (LIVE: agents.md standard, Slidev currency)
**Outcome:** SUCCESS - C11 built + wired; 4 audits + evidence log + tightening plan; AGENTS.md-standard finding patched into cross-agent docs
**Routing quality:** good

## 2026-06-13 - alpha.24: selected-V2 build + P1 maintenance (deep)
**Selected:** automation-engineer (NEW, merged from legacy) · product-strategist + make-money + writing-dna (offer business-system, start, local-business, brand) · researcher (brand niche scan, recording) · ux-ui-designer + frontend-design-system (brand) · skill-auditor (P1 + matrices) · orchestrator (wiring + legacy merge) · problem-solver + multi-model-planning (PATCHED)
**Outcome:** SUCCESS - 6 commands + 4 extensions + 1 skill built; legacy skill/ inventoried + legacy-marked; high-risk + okay audits; counts 59/31 synced
**Routing quality:** good - automation-engineer is the legacy-merge home; no other new skills needed
