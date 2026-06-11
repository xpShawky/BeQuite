# Confidence Calibration Report

> Forecast-vs-actual tracking (alpha.21). Written at `/bq-verify` / `/bq-release`. The point: make the percentages MEAN something — systematic error becomes a MISTAKE_MEMORY rule and a CONFIDENCE_RULES correction.

## Entry format

```markdown
## <date> — <task/feature>
**Forecast at start:** NN% · **Final pre-verify forecast:** NN% · **Actual outcome:** SUCCESS / PARTIAL / FAIL
**Calibration error:** <e.g. "over-confident by ~20 — external API undocumented">
**Lesson → rule:** <correction applied to CONFIDENCE_RULES / MISTAKE_MEMORY, or "well-calibrated">
```

## Running calibration summary

| Period | Forecasts | Well-calibrated (±10) | Over-confident | Under-confident |
|---|---|---|---|---|
| (no data yet) | 0 | — | — | — |

---

## Entries (newest at top)

(none yet — first entries arrive with the first forecasted task that reaches verification)
