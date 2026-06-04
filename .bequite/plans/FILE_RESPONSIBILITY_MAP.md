# File Responsibility Map

| Field | Value |
|---|---|
| Feature / change name | `<fill in>` |
| Generated | `<YYYY-MM-DD HH:MM>` |

> Author this BEFORE breaking work into tasks. `/bq-assign` refuses to write tasks without it.
>
> Rationale: name the files and interfaces before coding so the agent builds along a known seam instead of improvising (Anthropic Claude Code best-practices — "name the files and interfaces"; obra/superpowers — "map files before tasks, one responsibility per file").

---

## File table

One row per file. One responsibility per file. If a file needs two sentences to describe, it is doing two jobs — split it.

| File path | Single responsibility (one sentence) | Allowed import targets (dependency direction) | New / Modified | Tests that cover it |
|---|---|---|---|---|
| `src/utils/slugify.ts` | Convert a display string into a URL-safe slug. | (none — leaf utility) | New | `tests/utils/slugify.test.ts` |
| `<path>` | `<one sentence>` | `<modules this file may import>` | New / Modified | `<test file(s)>` |

The first row is a worked example. Replace or delete it once real rows are filled.

---

## Dependency direction (mini-rule)

Imports flow ONE way. Higher layers import lower layers; never the reverse.

```
utilities  →  services  →  handlers / components  →  entry points (orchestrate)
(import       (import        (import services +        (import everything below;
 nothing)      utilities)     utilities)                imported by nothing)
```

- Utilities depend on nothing in this codebase (pure, leaf-level).
- Services depend only on utilities (and other lower services).
- Handlers / components depend on services + utilities — never on each other sideways for shared logic (extract a service instead).
- Entry points orchestrate; nothing imports them.
- **No cycles.** If A imports B, B must not import A (directly or transitively).
- **No god-files.** No single file owns more than one responsibility from the table.

---

## Out of scope (do NOT touch)

List files / modules / dirs this change must leave untouched. Naming them now prevents scope creep and accidental edits.

- `<path or area>` — `<why it is off-limits>`
- ...

---

## Verification

- Every row's responsibility is checkable in one sentence — if you cannot state what a file does in one sentence, the row is wrong, not the rule.
- `/bq-review` flags any import that violates the declared direction (lower importing higher, or a cycle).
- `/bq-review` flags any file that grew a second responsibility beyond the row that describes it.
