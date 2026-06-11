# Context Engineering Strategy (alpha.19 index + deltas)

> **The index for BeQuite's context layer** plus the alpha.19 additions. Core mechanics live in `CONTEXT_ENGINEERING.md` (alpha.18) — this file orients and adds the context-pack pattern, the generic context summary, the evidence ledger, and the no-research-repeat rule.

**Status:** active · **Adopted:** alpha.19 (Fable Strengthening Pass)
**Deep reference:** `CONTEXT_ENGINEERING.md` (compact/clear/externalize primitives, compaction-survival rule, session-orientation ritual, sub-agent isolation) · skill: `bequite-context-engineer`

---

## The memory map (what survives where)

| Memory | File | Survives /compact? | Updated by |
|---|---|---|---|
| Project DNA (architecture invariants) | `state/PROJECT_DNA.md` | ✅ re-read per task | plan/feature/fix |
| Design DNA | `design/DESIGN_DNA.md` | ✅ | frontend commands |
| **Writing DNA** (alpha.19) | `writing/WRITING_DNA.md` | ✅ | /bq-writing-dna |
| Working notes (scratch, current task) | `state/WORKING_NOTES.md` | ✅ | any long task |
| **Context summary** (alpha.19, generic) | `state/CONTEXT_SUMMARY.md` | ✅ — its whole purpose | task boundaries |
| Frontend context summary | `state/FRONTEND_CONTEXT_SUMMARY.md` | ✅ | frontend commands |
| **Evidence log** (alpha.19) | `research/EVIDENCE_LOG.md` | ✅ | verification steps |
| Mistake memory | `state/MISTAKE_MEMORY.md` | ✅ | 8 wired commands |
| Mode history | `state/MODE_HISTORY.md` | ✅ | /bq-auto runs |
| Assumptions / decisions / open questions | `state/*.md` | ✅ | per contract |
| Handoff | `HANDOFF.md` | ✅ | /bq-handoff |
| Session recovery | LAST_RUN + all state | ✅ | /bq-recover reads |

**Compaction-survival rule (restated):** anything that must survive `/compact` goes in a file, not chat. Critical must-not-forget facts go in CLAUDE.md or PROJECT_DNA. Most important instructions at the TOP of every file.

## The context-pack pattern (alpha.19 — naming what already worked)

A **context pack** is the named minimal file set a task type loads at entry — no more, no less. Adding a new domain to BeQuite = defining its pack.

| Pack | Files loaded at entry |
|---|---|
| Core (every command) | PROJECT_STATE · CURRENT_MODE · CURRENT_PHASE · WORKFLOW_GATES · LAST_RUN · MISTAKE_MEMORY(top) |
| Frontend | + DESIGN_DNA · SECTION_MAP · FRONTEND_CONTEXT_SUMMARY · FRONTEND_SKILL_MAP |
| Presentation | + presentations/PRESENTATION_BRIEF (+ siblings on demand) |
| **Writing** (alpha.19) | + writing/WRITING_DNA · WRITING_RULES · FORBIDDEN_PATTERNS |
| Delegate | + tasks/DELEGATE_* pack |
| Opportunity | + jobs/* or money/* profiles |
| Long multi-step | + PROJECT_DNA · WORKING_NOTES · CONTEXT_SUMMARY |

Rule: a command states its pack in its "Files to read" section; everything else is on-demand.

## The no-research-repeat rule (alpha.19 — now a hard rule)

Before any research step: `ls .bequite/research/` → if a report covers the domain, **reuse and cite it; research only the delta**. New findings append to the existing report or create `<DOMAIN>_RESEARCH_REPORT.md`. Re-deriving cached research is a contract violation (step 5), not just a token waste.

## The evidence ledger (alpha.19)

`bequite-anti-hallucination` requires command + exit code + output for every "works/done" claim. For runs longer than a few tool calls, that evidence now persists in `research/EVIDENCE_LOG.md` so it survives compaction and feeds `/bq-verify` + reviews. Inline paste remains fine for short runs.

## Session recovery ritual (orientation order)

1. `CONTEXT_SUMMARY.md` (what was happening, compact) → 2. `LAST_RUN.md` → 3. `WORKING_NOTES.md` → 4. gate ledger → 5. proceed. `/bq-recover` automates this.
