# BeQuite installed version

**Version:** v3.0.0-alpha.14
**Updated:** 2026-05-17
**Source:** github
**Source path / repo:** xpShawky/BeQuite (branch: main)
**Previous version:** v3.0.0-alpha.13
**Last check:** 2026-05-17
**Update count:** 0 (this is the seed file; updates from /bq-update increment)

---

## How this file works

Refreshed by `/bq-update` on successful updates. Created by `/bq-init` (or the installer scripts) on first install.

Reading this file lets `/bq-update` know:
- What version is currently installed
- When it was last checked vs. last updated
- Which source (GitHub / local) to fetch updates from

## Version numbering

`v3.0.0-alpha.<N>` where N increments per alpha release. Latest releases are listed in `docs/changelogs/CHANGELOG.md`.

## Update history

(Populated by `/bq-update` runs — newest at top.)

### 2026-05-17 — alpha.14 ship — discipline restoration
- 7 audit reports written (FULL_SYSTEM_ALIGNMENT_AUDIT, COMMAND_SKILL_CONSISTENCY_AUDIT, WORKFLOW_GATE_AUDIT, FEATURE_WORKFLOW_AUDIT, BEQUITE_SYSTEM_RESEARCH_REPORT, COMMAND_CLUTTER_REVIEW, FINAL_SYSTEM_ALIGNMENT_REPORT)
- Global feature-addition rule codified in CLAUDE.md + WORKFLOW_GATES.md + COMMAND_CATALOG.md
- Gate name aliases documented (`_DONE` and `_COMPLETE` both valid)
- Orthogonal workflows section added (Presentation / Job / Money / Suggest don't change mode)
- `/bq-add-feature` marked as deprecated alias for `/bq-feature`
- `OPEN_QUESTIONS.md` Q1-Q3 closed (resolved by ADR-001/004)
- `PROJECT_STATE.md` refreshed (removed stale Studio reference)
- `.bequite/research/` directory created with first system research report
- No new features added (this is a discipline release)
- Commands: 44 active + 1 deprecated alias; Skills: 21 (unchanged)

### 2026-05-13 — alpha.13 ship
- `/bq-presentation` added (premium PPTX / HTML builder)
- `bequite-presentation-builder` skill added
- `.bequite/presentations/` memory folder with 9 templates added
- Installer carries presentation templates
- Commands: 43 → 44; Skills: 20 → 21

### 2026-05-12 — alpha.12 ship
- 4 composable operating modes (Deep / Fast / Token Saver `lean` / Delegate)
- `bequite-delegate-planner` skill added
- Delegate task pack + MODE_HISTORY added
- Skills: 19 → 20

### 2026-05-12 — seeded
- Initial seed at v3.0.0-alpha.10 (the version this seed file was authored at)
- No prior `/bq-update` run yet
