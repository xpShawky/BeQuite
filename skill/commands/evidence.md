---
name: bequite.evidence
description: Surface evidence/<phase>/<task>/ artefacts for review. Reads state/evidence_index.json + receipts (v0.7.0+); produces a human-readable summary of what was done, what was tested, what passed, what failed, what's missing.
phase: any
persona: orchestrator (this SKILL)
---

# /bequite.evidence [phase?] [task?]

When invoked (or `bequite evidence [args]`):

## Step 1 — Resolve scope

- No args: full project evidence index.
- `--phase P5`: scope to a phase.
- `--task TASK-001`: scope to one task.
- `--since v0.5.0`: scope from a tag.

## Step 2 — Read

- `state/evidence_index.json` — manifest entries.
- `evidence/<phase>/<task>/manifest.json` per scoped task.
- `.bequite/receipts/<sha>-*.json` (v0.7.0+) — cryptographic proof.

## Step 3 — Render

Produce a structured summary:

```
PHASE p5 — IMPLEMENT
└── TASK-007 — passed
    ├── Commands:
    │   ├── pnpm test       exit 0  (12/12 passed)        evidence/p5/TASK-007/test-output.txt
    │   ├── pnpm lint       exit 0                          evidence/p5/TASK-007/lint-output.txt
    │   └── pnpm typecheck  exit 0                          evidence/p5/TASK-007/typecheck-output.txt
    ├── Screenshots: 4 (admin × 360, admin × 1440, user × 360, user × 1440)
    ├── Files changed: 6 (apps/web/src/Booking.tsx, ...)
    ├── Skeptic question: "What happens to in-flight bookings during the migration?"
    ├── Skeptic answer:   evidence/p5/TASK-007/skeptic.md  (3-step rollout plan; pg_repack)
    ├── Receipt:          .bequite/receipts/abc123-P5-TASK-007.json  (chain valid)
    └── Notes:            "..."
```

For Phase 6 evidence, include validation-mesh gate-by-gate results.

## Step 4 — Cross-reference receipts

For every evidence entry, verify:

- Receipt sha256 matches.
- Test stdout hash matches `evidence/<phase>/<task>/test-output.txt`.
- Files-touched list matches `git diff` for the relevant commit.

Any mismatch is flagged as a **chain-integrity warning** in the output.

## Step 5 — Output

Write to stdout (paste-able). Optionally save to `evidence/_summaries/<scope>-<timestamp>.md`.

## Stop condition

- Summary rendered.
- Chain integrity verified (all receipts match).
- Any chain-integrity warnings surfaced explicitly.

## Anti-patterns

- Surfacing "all green" without checking chain integrity.
- Reading `manifest.json` without cross-referencing the receipt (sloppy proof).
- Skipping failed evidence in the summary (Article VI binding — honest reporting).

## Related

- `/bequite.recover` — uses this output as input.
- `/bequite.cost` — sums tokens + dollars from receipts.
- `/bequite.audit` — Constitution drift detector.
