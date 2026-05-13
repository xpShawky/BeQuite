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

<!--
  Examples of good entries:

  ## 2026-05-12T14:30Z — Hidden text on mobile cards due to gray-on-color
  **Context:** /bq-fix run on the dashboard's PricingCards section at 360px viewport
  **Mistake:** initial fix applied `--color-fg-muted` to the card title; failed contrast on the highlighted card's brand-color background
  **Root cause:** muted gray reuses the same value across light and dark sections; doesn't pass WCAG AA on colored backgrounds
  **Fix:** components/PricingCards.tsx:42 — switched to `--color-fg` on the highlighted card; left muted on the neutral cards
  **Prevention rule:** never apply muted text on a colored card background; use the body text token instead
  **Related files:** components/PricingCards.tsx, components/Cards.tsx, tokens.css
  **Related command:** /bq-fix (15-type: frontend bug — visual/state)
  **How to detect next time:** axe-core check on cards with backgrounds != base bg; manual grayscale check during /bq-live-edit
-->

(no entries yet — this file populates as BeQuite is used in this project)

---

## Categories to organize entries (use tags in the summary)

- `[fe]` — frontend / UI
- `[be]` — backend / API
- `[db]` — database / schema / query
- `[auth]` — authentication / permissions
- `[build]` — build / compile / TS
- `[test]` — testing
- `[deploy]` — deployment / CI / env
- `[perf]` — performance
- `[sec]` — security
- `[dep]` — dependency / package
- `[config]` — configuration / env vars
- `[net]` — network / integration
- `[mem]` — memory leak / resource
- `[race]` — race condition / async
- `[xbrowser]` — cross-browser / platform
- `[design]` — design system / token / AI-slop

Examples:
```
## 2026-05-12T14:30Z — [fe][design] Hidden text on mobile cards (gray-on-color contrast)
## 2026-05-15T10:00Z — [build][dep] PhantomRaven package alert: typo-squatted dep
## 2026-05-20T16:00Z — [be][race] Missing await on email send caused dropped notifications
```

---

## Rules for good entries

- **One mistake per entry.** Don't pile unrelated lessons into one.
- **Prevention rule must be concrete.** "Be careful with X" is not concrete. "Always run axe-core before merging UI changes" is.
- **Cite file:line whenever possible.** "The pricing component is broken" is not useful. "components/PricingCards.tsx:42 — gray-on-color fails AA" is.
- **Pattern over instance.** If the root cause is "missing await on async DB call", record the pattern, not just this one instance.
- **Use tags.** They make grep + filtering work.

---

## Pruning

This file grows. To prevent bloat:
- Every 3 months: review entries; archive resolved/permanent-fixed patterns to `.bequite/state/MISTAKE_MEMORY-archive-<date>.md`
- Keep the live file under 200 entries
- The agent prefers recent + tag-matching entries; archived entries are still readable on demand
