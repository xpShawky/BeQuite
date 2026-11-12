# Confidence Rules (project-tunable)

> Per-project calibration rules per `docs/architecture/CONFIDENCE_CALIBRATION_STRATEGY.md`. Read at forecast time; updated when the calibration report reveals systematic error.

## Base modifiers (defaults — tune per project)

| Signal | Modifier |
|---|---|
| All relevant files read this session | +15 |
| Identical pattern already in repo (DNA/precedent) | +10 |
| Tests exist on the touched surface | +10 |
| Cached research covers the domain | +5 |
| R3 path in scope | −15 (and hard gate applies) |
| External service / undocumented API | −15 |
| Scope inferred, not stated | −10 (and ASSUMPTIONS entry required) |
| MISTAKE_MEMORY hit on this pattern | −10 until prevention rule applied |
| > 5 files touched without File-Responsibility Map | −10 |

Start point: 60% for a typical scoped task before inspection; clamp to bands; never exceed 99 without the 100% rule satisfied.

## Project-specific rules

| Rule | Modifier | Why | Added |
|---|---|---|---|
| (none yet) | | | |

## Calibration corrections (from CONFIDENCE_CALIBRATION_REPORT)

| Date | Systematic error found | Correction applied |
|---|---|---|
| (none yet) | | |
