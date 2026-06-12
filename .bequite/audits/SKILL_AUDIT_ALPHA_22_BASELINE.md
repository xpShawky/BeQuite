# Skill Audit — Alpha.22 Baseline (the 3 new/recent skills)

**Run:** 2026-06-12 · `/bq-skill-audit` scope: bequite-orchestrator · bequite-guard-pass · bequite-localization-rtl · Claude Fable 5 · **Type: structural desk audit** (file-evidence based; live-invocation validation remains pending — stated, not hidden).

## 1. bequite-orchestrator

| Field | Finding |
|---|---|
| Purpose | global brain: command/skill conflict resolution, missing-capability detection, orchestration-map enforcement |
| Auto-attaches | bequite · suggest · discover · plan · auto · implement · review · verify · skill-audit + any conflict/confusion signal (SKILL.md §When) |
| Commands that should use it | the 9 above — all 9 carry orchestrator references (verified: alpha.22 orchestration-update blocks present in each) |
| Router coverage | ✅ registry row + SKILL_ROUTER conflict rule + COMMAND_ROUTER §7 both defer to it |
| Reads | ORCHESTRATION_MAP · COMMAND_ID_MAP · SKILL_REGISTRY · gates · phase/mode |
| Writes | none of its own (directs NEXT_COMMAND_LOG + OPEN_QUESTIONS writes) — correct for a map-skill |
| Overlap | workflow-advisor (suggest engine) — boundary clean: advisor recommends routes, orchestrator resolves conflicts + enforces the map; no merge needed |
| Missing references | none found — map/model/rules files all exist at the cited paths |
| Drift risk | **MEDIUM** — the map must be updated with every command/skill change; mitigated by maintainer rule + `/bq-verify drift` |
| Quality rating | GOOD (compact, cites quality gate requiring map-section citations) |
| **Action** | **PASS** (live validation pending) |
| Evidence | `.claude/skills/bequite-orchestrator/SKILL.md` · `.bequite/state/ORCHESTRATION_MAP.md` |

## 2. bequite-guard-pass

| Field | Finding |
|---|---|
| Purpose | reactive post-work gates for AI failure modes (code/test/docs guards) |
| Auto-attaches | after implement/feature/fix/test · before verify/release · AI-diff reviews (delegate especially) |
| Commands that should use it | implement, feature, fix, test, review, verify, release — review/verify/auto carry explicit Guard Pass blocks; release inherits via verify; ✅ |
| Router coverage | ✅ registry row + router domain row ("post-work quality gate / AI-diff review") |
| Reads | produced diff/files + its checklists |
| Writes | `.bequite/audits/GUARD_PASS_REPORT.md` (seed report exists with 2 real findings — the pattern already proved itself) |
| Overlap | anti-hallucination (claims vs artifacts — complementary, documented in GUARD_PASS_STRATEGY §how-it-differs) · review (spec/quality vs failure-mode hunt) — boundaries documented; no merge |
| Missing references | none — strategy doc + report exist |
| Drift risk | LOW (checklists are stable failure-mode lists) |
| Quality rating | GOOD (has the "no findings must state coverage" anti-weasel gate) |
| **Action** | **PASS** (live validation pending) |
| Evidence | `.claude/skills/bequite-guard-pass/SKILL.md` · `docs/architecture/GUARD_PASS_STRATEGY.md` · seed `GUARD_PASS_REPORT.md` |

## 3. bequite-localization-rtl

| Field | Finding |
|---|---|
| Purpose | Arabic-first localization + RTL engineering (tone-localization, bidi, digits/dates, icon mirroring, width expansion, CLDR plurals) |
| Auto-attaches | Arabic · MENA · Egypt/Gulf · RTL · bilingual · `mena-bilingual` doctrine |
| Commands that should use it | course, feature, presentation, reference, live-edit, uiux-variants — course/reference/pain-radar name it explicitly; feature/presentation inherit via Skill Router domain row ✅ |
| Router coverage | ✅ registry row + router domain row |
| Reads | active workflow artifacts + DESIGN_DNA |
| Writes | localization sections into the active workflow's artifacts (no own dir — deliberate, documented) |
| Overlap | ux-ui-designer (general UI) — boundary: localization-rtl owns language/direction specifics; clean |
| Missing references | none — `docs/specs/LOCALIZATION_RTL.md` exists; `/bq-localize` correctly marked proposal-only |
| Drift risk | LOW |
| Quality rating | GOOD (concrete engineering rules, not vibes: logical CSS properties, +20–40% width, 6-form plurals) |
| **Action** | **PASS** — and it earned its first real exercise today: the Arabic course PDF intake (RTL extraction artifacts identified — see `COURSE_PDF_REFERENCE_NOTES.md`) |
| Evidence | `.claude/skills/bequite-localization-rtl/SKILL.md` · `docs/specs/LOCALIZATION_RTL.md` |

## Verdict + registry effect

3/3 **PASS** (structural). No new skills needed; no merges; no removals. Registry Q column flips from "provisionally ✓" to audited ✓ for these three; quality summary now 30 ✓-or-~ with the 2 pre-existing ~ items (problem-solver thin example, multi-model-planning stale phasing) still backlogged. Live-invocation validation of all three remains in REMAINING_WORK_MASTER §B.
