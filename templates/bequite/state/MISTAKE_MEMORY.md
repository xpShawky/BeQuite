# Mistake Memory

Project-specific lessons. When BeQuite or the agent makes a mistake, hits an error, fixes a repeated issue, or learns a project-specific lesson, it stores the entry here. Re-read on every session start so the same mistake isn't repeated.

**Updated by:** `/bq-fix`, `/bq-audit`, `/bq-review`, `/bq-red-team`, `/bq-verify`, `/bq-auto`, `/bq-live-edit`

---

## Entry template

```markdown
## <ISO 8601 UTC> — <one-line summary>

**Context:** <where this came up — file, feature, phase, session>
**Mistake:** <what went wrong>
**Root cause:** <one sentence; the actual cause, not the symptom>
**Fix:** <file:line + what changed>
**Prevention rule:** <how to avoid this in future work>
**Related files:** <list>
**Related command:** <which BeQuite command surfaced this>
**How to detect next time:** <pattern to grep for; test to add; check to run>
```

---

## How this file is used

1. **On session start** — agent reads this file (top 10-20 entries) into context. Recent mistakes inform decisions.
2. **During `/bq-fix`** — after the fix lands, append an entry. Future bug attempts check here first.
3. **During `/bq-audit`** — entries inform what areas to scrutinize.
4. **During `/bq-review`** — diffs that touch the "Related files" trigger extra care.
5. **During `/bq-red-team`** — entries become attack-angle inputs.
6. **During `/bq-verify`** — if a "Prevention rule" hasn't been verified, add to verify checklist.
7. **During `/bq-auto`** — surfaces relevant entries before each phase based on the task.
8. **During `/bq-live-edit`** — entries tagged with frontend / responsive / contrast / spacing inform every edit.

---

## Entries (newest at top)

(none yet - entries are added newest at top as work happens)
