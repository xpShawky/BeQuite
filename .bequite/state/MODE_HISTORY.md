# Mode History

Tracks which BeQuite operating mode was used per command run, plus outcome. Append-only. Used by `/bq-suggest` and `bequite-workflow-advisor` to learn what works for this project.

---

<!--
  Template per entry:

  ## <ISO 8601 UTC> — <command> <mode>

  **Command:** /bq-auto | /bq-plan | /bq-fix | etc.
  **Mode(s):** balanced | deep | fast | token-saver | delegate | deep+delegate | fast+token-saver | etc.
  **Task:** <one-line user description>
  **Duration:** <wall clock>
  **Outcome:** ✅ success | ⚠ partial | ❌ failed | ⏸ paused-at-gate
  **Cost (approx):** $<USD> or <token count>
  **Files changed:** <count>
  **Tests:** <pass>/<total>
  **Notes:** <what worked / what didn't>

  ---
-->

(no entries yet — populated as commands run)

---

## How this file is used

- `/bq-suggest` reads recent entries to learn user's mode preferences
- `bequite-workflow-advisor` uses outcomes to refine recommendations ("fast mode failed last 2 times for security tasks — recommend deep next")
- User reads occasionally to see what cost/time pattern matches their work
- Re-evaluated on repeat searches; entries can be marked: 🆕 / ✅ / ❌ / ⚠

## Pruning

- Keep last 100 entries
- Older entries summarized into a single block at the bottom: "Avg mode usage Jan-Mar 2026: 60% balanced, 20% fast, 15% deep, 5% delegate"
