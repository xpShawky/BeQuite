---
name: bequite.memory
description: Memory Bank operations. BeQuite-unique. Read / show / refresh / validate the six-file Memory Bank + state/ files + active ADRs. Used to ensure Article III compliance + diagnose stale state.
phase: any
persona: orchestrator (this SKILL)
---

# /bequite.memory <subcommand> [args]

Subcommands:

- `bequite memory show` — print the six Memory Bank files + state/ files + active ADRs to stdout.
- `bequite memory show <file>` — print one (e.g. `show projectbrief`, `show recovery`).
- `bequite memory show doctrine <name>` — print one Doctrine.
- `bequite memory show adr <id>` — print one ADR.
- `bequite memory refresh` — re-read everything (clear in-context cache).
- `bequite memory validate` — schema-validate every Memory Bank + state file.
- `bequite memory snapshot` — alias for `/bequite.snapshot`.
- `bequite memory diff` — show diff between current and last snapshot.

## Validate subcommand

Per-file schema checks:

- **`constitution.md`**: Iron Laws I–VII present; Doctrines section populated; Modes section (post v1.0.1).
- **`projectbrief.md`**: 7 sections (one-sentence product, who it's for, the problem, success criteria, hard constraints, explicit non-goals, hand-off bar).
- **`productContext.md`**: 8 sections (why exists, user journey, segments, competitor landscape, why-now, qualitative success, anti-patterns, open questions).
- **`systemPatterns.md`**: 8 sections (high-level shape, seams, recurring patterns, state management, cross-cutting concerns, ADR index, receipts pointer, sharp edges).
- **`techContext.md`**: 8 sections (stack at a glance, pinned versions, local dev setup, env vars, external services, dev-tool constraints, freshness contract, known stale advice).
- **`activeContext.md`**: Now / What I'm doing now / Open questions / Blockers / Next 3 / Heartbeat / Recent decisions.
- **`progress.md`**: Current state / What works / What's left / What's uncertain / Evolution log / Decisions / Failures.

For each file: `pass` / `warn (missing section)` / `fail (file missing)`.

## Refresh subcommand

Forces a re-read of every Memory Bank + state file in the next persona invocation. Useful after manual edits.

## Diff subcommand

Compares current files vs the last snapshot at `.bequite/memory/prompts/v<N>/`. Surfaces:

- Sections added.
- Sections removed.
- Sections meaningfully changed (>10% body delta).

Used at end-of-phase to confirm progress + at start-of-session to check what changed since last work.

## Stop condition

- Subcommand executed.
- Output to stdout (paste-able).
- For `validate`: exit 0 if all pass; exit 1 if any fail; exit 2 if any file missing entirely.

## Anti-patterns

- Editing Memory Bank files without running `/bequite.memory validate` — schema drift.
- `refresh` then continuing a coupled task without re-reading (defeats the refresh).
- Snapshotting without bumping the v<N> directory (overwrites history).

## Related

- `/bequite.snapshot` — write the current state to `.bequite/memory/prompts/v<N>/`.
- `/bequite.recover` — uses Memory Bank as primary input.
- `sessionstart-load-memory.sh` — surfaces Memory Bank paths on session start.
