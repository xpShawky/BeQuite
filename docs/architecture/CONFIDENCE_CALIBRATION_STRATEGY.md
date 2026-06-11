# Confidence Calibration Strategy (alpha.21)

> **Confidence is not a feeling. It is a report** based on evidence, tests, scope clarity, project familiarity, dependency risk, and verification. BeQuite doesn't only say what it will do — it estimates how likely it is to succeed, why, what is uncertain, and what must be verified.

**Status:** active · **Adopted:** alpha.21
**Integrated into:** `/bq-plan` · `/bq-assign` · `/bq-auto` · `/bq-feature` · `/bq-fix` · `/bq-implement` · `/bq-review` · `/bq-verify` · `/bq-release` (no separate `/bq-confidence` command — integration beats clutter; revisit only if demand appears)
**Rules file (per-project tunable):** `.bequite/state/CONFIDENCE_RULES.md` · **Task fields:** `.bequite/tasks/TASK_CONFIDENCE.md` · **Calibration tracking:** `.bequite/audits/CONFIDENCE_CALIBRATION_REPORT.md`

---

## The bands

| Band | Meaning | Action implied |
|---|---|---|
| **90–100%** | routine / well-understood | proceed |
| **75–89%** | likely, manageable risk | proceed; name the risk |
| **50–74%** | uncertain, needs exploration | inspect/read before committing to approach |
| **25–49%** | high risk | spike/prototype first; don't promise outcomes |
| **0–24%** | not enough information or likely blocked | stop; gather info or escalate to user |

## The report shape (every forecast)

```
Confidence: NN% (band) — <one-line why>
Evidence level: verified | inferred | assumed | unknown
Lowers it: <factor(s)>          Raises it: <check(s) that would>
Unknowns/blockers: <list or none>   Next: <recommended action>
```

## Confidence evolves over time (mandatory)

A forecast is re-stated at each contract checkpoint — it must MOVE as evidence arrives:

```
Before inspection: 60%  →  after reading files: 80%  →  after implementation: 75%
→  after tests pass: 92%  →  after visual QA: 96%
```

(Yes, implementation can LOWER confidence — discovering complexity is honest calibration, not failure.)

## The 100% rule

Never report 100% unless: all relevant tests pass + output verified + zero unresolved assumptions + zero external unknowns. Even then prefer **95–99%** unless mathematically guaranteed. A 100% claim without an EVIDENCE_LOG entry is a contract violation.

## What moves the number (calibration inputs)

**Raises:** files read (not assumed) · prior identical pattern in this repo (PROJECT_DNA / MISTAKE_MEMORY hit) · passing tests on the touched surface · cached research covering the domain · small blast radius (R1 files, ≤2 files)
**Lowers:** unread dependencies · R3 paths in scope · external services / undocumented APIs · "works on my machine" claims without runs · scope inferred rather than stated · MISTAKE_MEMORY shows past failures on this pattern · stack unfamiliar to the project (no PROJECT_DNA precedent)

## Anti-patterns (reject)

- Flat 85% on everything (uncalibrated optimism) — the spread across a task list should VARY
- Confidence theater: a % with no "why" and no evidence level
- Never revising downward
- Treating user pressure as evidence
- 100% before verification

## Calibration loop

At `/bq-verify` / release: compare forecasted vs actual outcomes → append to `CONFIDENCE_CALIBRATION_REPORT.md` (forecast / actual / error / lesson). Systematic over- or under-confidence is a finding → MISTAKE_MEMORY rule. This is what makes the numbers MEAN something over time.
