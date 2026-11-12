# Command Numbering & Ordering Strategy (alpha.22)

**Decision: Option A — display-only catalog IDs. No file renames. No alias files.**
Feasibility audit: `.bequite/audits/COMMAND_NAVIGATION_AND_CAPABILITY_CONSOLIDATION_AUDIT.md` §4.
Canonical map: `.bequite/commands/COMMAND_ID_MAP.md`.

---

## Why not rename (Option C)

Claude Code derives slash-command names from `.claude/commands/<name>.md` filenames. Renaming files therefore renames every command, which breaks:

1. **300+ cross-references** across README / commands.md / CLAUDE.md / catalog / runbooks / skills / strategy docs
2. **User muscle memory** — `/bq-fix` is learnable; `/bq-w24-fix` is not
3. **`/bq-update` migration** — every installed project would carry orphaned old-name files
4. **Registry / router / hooks examples** that quote command names
5. Numeric prefixes **freeze ordering** — inserting a future command renumbers everything (the classic BASIC line-number problem)

Gained capability: zero. **REJECTED.**

## Why not ordered aliases (Option B)

~20 duplicate files; two names per action; doubled maintenance per release; alias drift becomes a new failure mode. Violates the anti-clutter charter ("BeQuite is not a command-count project"). **REJECTED.**

## Option A — how it works

- IDs live in **docs and output only**: README, commands.md, `/bequite`, `/bq-help`, COMMAND_CATALOG, Command Router recommendations.
- Files and slash names are untouched.
- IDs are the **router's vocabulary**: "Required next: **W4.1 `/bq-verify`**".
- Auto mode reports internally executed steps by ID: "Internal workflow executed: W0.3 → W1.2 → W1.4 → W4.1".

## ID scheme

| Prefix | Family | Members |
|---|---|---|
| `W0.x`–`W5.x` | Workflow commands, by phase P0–P5 | W0 setup (7) · W1 framing (6) · W2 build (6) · W3 quality (4) · W4 release (3) · W5 memory (3) |
| `N#` | Navigation / orientation | now, help, explain, suggest (4) — `/bequite` itself is W0.1 (entry point) |
| `O#` | Orchestrators | p0–p5, auto (7) |
| `C#` | Capability commands | presentation, writing-dna, reference, knowledge, course, pain-radar, integrate, proposal, job-finder, make-money (10) |
| `M#` | Maintenance | update, skill-audit (2) |
| `X#` | Deprecated | add-feature alias (1) |

**Stability rules:** an ID never changes once assigned; new commands take the next free number in their family; a removed command's ID is retired, never reused; renumbering is forbidden. IDs identify, ordering is conveyed by phase grouping in docs.

**Arguments don't get IDs** — `/bq-release proof` is W4.2 with an argument, not a new entry. The ID map lists notable argument workflows in the shape column.

## Maintainer rule

Adding/removing a command without updating `COMMAND_ID_MAP.md` + menus/catalog = drift violation (caught by `/bq-verify drift` and the docs guard).
