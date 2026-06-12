# Command Classification Audit (alpha.22 stabilization)

**Run:** 2026-06-12 · scope: every row of `.bequite/commands/COMMAND_ID_MAP.md` checked for ID/category/phase/purpose/sequencing/auto-run/shape/arguments accuracy, plus category-scheme completeness.

## 1. Category scheme verdict: **complete and intuitive — keep W/N/O/C/M/X**

Considered and rejected additions: an **E (earning)** family for job-finder/make-money — rejected: they are capabilities like course/proposal; splitting C by money-vs-content adds a boundary users must learn for zero routing gain. A **G (guard/quality)** family — rejected: Guard Pass is a skill, not a command; W3 already owns quality commands. A **A (arguments)** family — rejected: arguments belong to their owning command's row (the ARG column), not separate identity. One scheme improvement adopted: the map's footer now tracks **queued** IDs (C11 `/bq-offer`) so future commands reserve IDs before build — prevents ID collisions.

## 2. Row-by-row check (53 rows + queue)

- **IDs:** all unique, all families consistent; O1–O6 deliberately share one row (p0–p5 are six files with identical shape) — acceptable, noted as intentional.
- **Phases:** correct (capabilities + navigation = "any" — correct, they're phase-independent).
- **Purpose clarity:** all rows one-line clear. Weakest purposes fixed in alpha.22 stabilization: none remaining.
- **Usually-follows / usually-next:** spot-validated against COMMAND_ROUTER spine — consistent. One correction applied earlier in alpha.22 addendum cycle (release row now names launch-kit profiles).
- **Auto-run flags:** verified — correctly marks `no` for clarify (needs user) + multi-plan (manual paste); `partial` for uiux-variants (gate 16) + release (gate 17).
- **Shapes:** WF/CAP/NAV/ORC/MNT/alias all correct; ARG annotations present for all 13 argument-bearing commands.
- **Arguments listed:** verified complete after the forgotten-candidate addendum (scope intake · feature demo-data · review persona/delegate · proposal price · release 4+template-V2 · verify 2 · test 2 · plan 2 · audit 2 · handoff 1 · uiux style= · knowledge modes · reference modes).

## 3. Special-attention items (user-flagged)

| Item | Classification status |
|---|---|
| scraping automation | correctly **absent from the map** (skill, not command); reachable via O7 auto intents + new router signal row; future `/bq-automation` correctly NOT pre-assigned an ID (queued IDs are for approved builds only) |
| localization/RTL | correctly absent (skill); `/bq-localize` proposal noted in map footer |
| guard pass | correctly absent (skill); surfaces inside W3.3/W4.1 flows |
| course / knowledge / reference / pain-radar / proposal | C5/C4/C3/C6/C8 rows verified; C5 purpose now reflects OCR intake (catalog updated) |
| offer queue | **C11 reserved in footer — correct** |
| automation/bot · data-to-product · AI service business builder | parked V2 — correctly NOT in the map (roadmap ledger holds them); listing parked items in the live map would advertise commands that don't exist |

## 4. Findings summary

0 misclassifications · 0 missing categories · 1 scheme improvement (queued-ID convention, already in place via C11 note) · 1 catalog purpose enrichment applied (C5 OCR). The map is fit for its job as the router's vocabulary.
